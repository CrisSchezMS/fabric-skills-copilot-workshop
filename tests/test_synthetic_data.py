import unittest
from dataclasses import replace
from datetime import date
from decimal import Decimal

from src.synthetic_data import (
    GeneratorConfig,
    expected_results,
    generate_data,
    reference_clean_rows,
)


class SyntheticDataTests(unittest.TestCase):
    def setUp(self):
        self.config = GeneratorConfig(n_sales=1000)
        self.data = generate_data(self.config)

    def test_seed_controls_data_and_dates_stay_inside_requested_window(self):
        self.assertEqual(self.data, generate_data(self.config))
        other_seed = generate_data(replace(self.config, seed=7))
        self.assertNotEqual(self.data["sales_raw"], other_seed["sales_raw"])
        dated = generate_data(replace(self.config, start_date="2024-02-29", days=1))
        self.assertEqual({row["sale_date"] for row in dated["sales_raw"]}, {date(2024, 2, 29)})

    def test_anomalies_are_disjoint_before_exact_duplicates_are_added(self):
        unique = {row["sale_id"]: row for row in self.data["sales_raw"]}
        self.assertEqual(len(unique), self.config.n_sales)
        self.assertEqual(len(self.data["sales_raw"]) - len(unique), 20)
        issues = {
            "category_null": set(),
            "city_null": set(),
            "quantity": set(),
            "product": set(),
            "category_text": set(),
            "city_text": set(),
        }
        for sale_id, row in unique.items():
            if row["category_raw"] is None:
                issues["category_null"].add(sale_id)
            elif row["category_raw"].startswith(" "):
                issues["category_text"].add(sale_id)
            if row["city_raw"] is None:
                issues["city_null"].add(sale_id)
            elif row["city_raw"].startswith(" "):
                issues["city_text"].add(sale_id)
            if row["quantity"] <= 0:
                issues["quantity"].add(sale_id)
            if row["product_id"] == 999_999:
                issues["product"].add(sale_id)
        for affected in issues.values():
            self.assertEqual(len(affected), 10)
        self.assertEqual(len(set.union(*issues.values())), 60)
        for row in self.data["sales_raw"]:
            self.assertEqual(row, unique[row["sale_id"]])

    def test_zero_rates_remove_quality_errors_but_not_business_cancellations(self):
        data = generate_data(replace(self.config, duplicate_rate=0, anomaly_rate=0))
        report = expected_results(data)
        self.assertEqual(report["extra_duplicate_rows"], 0)
        self.assertEqual(report["null_category_rows"], 0)
        self.assertEqual(report["orphan_product_rows"], 0)
        self.assertEqual(report["invalid_quantity_rows"], 0)
        self.assertGreater(report["cancelled_rows"], 0)

    def test_reference_recovers_raw_nulls_and_uses_half_up_per_line(self):
        product = self.data["products"][0]
        store = self.data["stores"][0]
        row = dict(self.data["sales_raw"][0])
        row.update(
            product_id=product["product_id"],
            store_id=store["store_id"],
            category_raw=None,
            city_raw=None,
            quantity=1,
            unit_price=Decimal("0.05"),
            discount_rate=Decimal("0.10"),
            status="completed",
        )
        data = {**self.data, "sales_raw": [row, dict(row)]}
        clean = reference_clean_rows(data)
        self.assertEqual(len(clean), 1)
        self.assertEqual(clean[0]["category"], product["category"])
        self.assertEqual(clean[0]["city"], store["city"])
        self.assertEqual(clean[0]["net_amount"], Decimal("0.05"))

    def test_reference_does_not_choose_between_conflicting_versions(self):
        row = dict(self.data["sales_raw"][0])
        other = {**row, "quantity": row["quantity"] + 1}
        with self.assertRaisesRegex(ValueError, "contenido diferente"):
            reference_clean_rows({**self.data, "sales_raw": [row, other]})

    def test_invalid_configuration_fails_before_generation(self):
        for change in (
            {"n_sales": 0},
            {"n_sales": 100_001},
            {"n_sales": True},
            {"seed": -1},
            {"days": 0},
            {"duplicate_rate": 0.21},
            {"anomaly_rate": 0.11},
            {"anomaly_rate": float("nan")},
            {"duplicate_rate": True},
            {"start_date": "2026-02-30"},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                replace(self.config, **change)


if __name__ == "__main__":
    unittest.main()
