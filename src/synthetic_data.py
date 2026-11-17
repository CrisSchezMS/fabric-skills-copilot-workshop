"""Deterministic, entirely fictional retail data; Python standard library only."""

import random
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal


@dataclass(frozen=True)
class GeneratorConfig:
    seed: int = 42
    n_sales: int = 10_000
    start_date: str = "2026-01-01"
    days: int = 90
    duplicate_rate: float = 0.02
    anomaly_rate: float = 0.01

    def __post_init__(self):
        bounds = {"seed": (0, 2**32 - 1), "n_sales": (100, 100_000), "days": (1, 3660)}
        for field, (low, high) in bounds.items():
            value = getattr(self, field)
            if type(value) is not int or not low <= value <= high:
                raise ValueError(f"{field} debe ser un entero entre {low} y {high}.")
        for field, high in (("duplicate_rate", 0.20), ("anomaly_rate", 0.10)):
            value = getattr(self, field)
            if type(value) not in (int, float) or not 0 <= value <= high:
                raise ValueError(f"{field} debe estar entre 0 y {high}.")
        start = date.fromisoformat(self.start_date)
        if start.isoformat() != self.start_date:
            raise ValueError("start_date debe usar el formato YYYY-MM-DD.")
        start + timedelta(days=self.days - 1)


def generate_data(config):
    rng = random.Random(config.seed)
    categories = ("Hogar", "Deporte", "Tecnologia", "Papeleria")
    products = [
        {
            "product_id": index + 1,
            "product_name": f"Producto {index + 1:02d}",
            "category": categories[index // 3],
            "list_price": Decimal(500 + index * 725) / 100,
        }
        for index in range(12)
    ]
    stores = [
        {"store_id": index + 1, "store_name": f"Tienda {index + 1:02d}", "city": city}
        for index, city in enumerate(("Ciudad Norte", "Ciudad Sur", "Ciudad Este", "Ciudad Oeste"))
    ]
    start = date.fromisoformat(config.start_date)
    sales = []
    for index in range(config.n_sales):
        product = rng.choice(products)
        store = rng.choice(stores)
        sales.append(
            {
                "sale_id": f"V{index + 1:07d}",
                "sale_date": start + timedelta(days=rng.randrange(config.days)),
                "product_id": product["product_id"],
                "store_id": store["store_id"],
                "channel": rng.choice(("online", "tienda")),
                "quantity": rng.randint(1, 5),
                "unit_price": product["list_price"],
                "discount_rate": Decimal(rng.choice((0, 5, 10, 15))) / 100,
                "status": "cancelled" if rng.random() < 0.10 else "completed",
                "category_raw": product["category"],
                "city_raw": store["city"],
            }
        )

    indices = list(range(config.n_sales))
    rng.shuffle(indices)
    count = int(config.n_sales * config.anomaly_rate)
    for kind in range(6):
        for index in indices[kind * count : (kind + 1) * count]:
            row = sales[index]
            if kind == 0:
                row["category_raw"] = None
            elif kind == 1:
                row["city_raw"] = None
            elif kind == 2:
                row["quantity"] = 0 if index % 2 == 0 else -1
            elif kind == 3:
                row["product_id"] = 999_999
            elif kind == 4:
                row["category_raw"] = f"  {row['category_raw'].upper()}  "
            else:
                row["city_raw"] = f"  {row['city_raw'].upper()}  "

    duplicate_count = int(config.n_sales * config.duplicate_rate)
    duplicates = [
        dict(sales[index]) for index in rng.sample(range(config.n_sales), duplicate_count)
    ]
    raw_sales = sales + duplicates
    rng.shuffle(raw_sales)
    return {"products": products, "stores": stores, "sales_raw": raw_sales}


def reference_clean_rows(data):
    """Small Python oracle for the exercise, not a production ETL implementation."""
    products = {row["product_id"]: row for row in data["products"]}
    stores = {row["store_id"]: row for row in data["stores"]}
    seen = {}
    cleaned = []
    for row in data["sales_raw"]:
        sale_id = row["sale_id"]
        if sale_id in seen:
            if row != seen[sale_id]:
                raise ValueError(f"Duplicados con contenido diferente: {sale_id}")
            continue
        seen[sale_id] = row
        product = products.get(row["product_id"])
        store = stores.get(row["store_id"])
        if not product or not store or row["quantity"] <= 0 or row["status"] != "completed":
            continue
        clean = {
            key: value for key, value in row.items() if key not in ("category_raw", "city_raw")
        }
        clean["category"] = product["category"]
        clean["city"] = store["city"]
        clean["net_amount"] = (
            row["quantity"] * row["unit_price"] * (1 - row["discount_rate"])
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        cleaned.append(clean)
    return cleaned


def expected_results(data):
    raw = data["sales_raw"]
    cleaned = reference_clean_rows(data)
    product_ids = {row["product_id"] for row in data["products"]}
    by_category = {}
    for row in cleaned:
        category = row["category"]
        by_category[category] = by_category.get(category, Decimal("0.00")) + row["net_amount"]
    return {
        "products": len(data["products"]),
        "stores": len(data["stores"]),
        "raw_rows": len(raw),
        "unique_sales": len({row["sale_id"] for row in raw}),
        "extra_duplicate_rows": len(raw) - len({row["sale_id"] for row in raw}),
        "null_category_rows": sum(row["category_raw"] is None for row in raw),
        "null_city_rows": sum(row["city_raw"] is None for row in raw),
        "invalid_quantity_rows": sum(row["quantity"] <= 0 for row in raw),
        "orphan_product_rows": sum(row["product_id"] not in product_ids for row in raw),
        "cancelled_rows": sum(row["status"] == "cancelled" for row in raw),
        "clean_rows": len(cleaned),
        "net_revenue": str(sum((row["net_amount"] for row in cleaned), Decimal("0.00"))),
        "revenue_by_category": {key: str(value) for key, value in sorted(by_category.items())},
    }
