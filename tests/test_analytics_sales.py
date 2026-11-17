import unittest
from unittest.mock import Mock, patch

from src.analytics_sales import analytics_table_names, write_analytics_tables


class AnalyticsWriteTests(unittest.TestCase):
    def setUp(self):
        self.spark = Mock()
        self.spark.catalog.tableExists.return_value = False
        self.frames = {key: Mock() for key in ("sales_clean", "sales_daily", "calendar")}
        for frame in self.frames.values():
            frame.count.return_value = 10
            frame.write.format.return_value.mode.return_value = frame.write
        self.spark.table.return_value.count.return_value = 10

    def test_missing_approval_prevents_even_catalog_access(self):
        for approval in (False, None, "True", 1):
            with self.subTest(approval=approval), self.assertRaises(PermissionError):
                write_analytics_tables(self.spark, self.frames, "dbo", approved=approval)
        self.assertEqual(self.spark.mock_calls, [])
        for frame in self.frames.values():
            frame.write.format.assert_not_called()

    def test_existing_last_output_prevents_all_writes(self):
        self.spark.catalog.tableExists.side_effect = [False, False, True]
        with self.assertRaises(FileExistsError):
            write_analytics_tables(self.spark, self.frames, "dbo", approved=True)
        for frame in self.frames.values():
            frame.write.format.assert_not_called()

    def test_approved_publication_reconciles_then_writes_only_derived_tables(self):
        totals = {"clean_rows": 10, "units": 20, "net_revenue": "42.00"}
        with patch("src.analytics_sales.validate_analytics_frames", return_value=totals) as check:
            actual = write_analytics_tables(self.spark, self.frames, "", approved=True)
        self.assertEqual(actual, totals)
        self.assertEqual(check.call_count, 2)
        for key, name in analytics_table_names("").items():
            self.frames[key].write.format.assert_called_once_with("delta")
            self.frames[key].write.format.return_value.mode.assert_called_once_with("errorifexists")
            self.frames[key].write.saveAsTable.assert_called_once_with(name)
        self.spark.sql.assert_not_called()

    def test_invalid_destinations_and_incomplete_frames_fail_before_writing(self):
        for schema in (None, "dbo.other", "dbo;DROP", "../dbo"):
            with self.subTest(schema=schema), self.assertRaises(ValueError):
                write_analytics_tables(self.spark, self.frames, schema, approved=True)
        with self.assertRaises(ValueError):
            write_analytics_tables(self.spark, {"sales_clean": Mock()}, "dbo", approved=True)
        self.assertEqual(self.spark.mock_calls, [])

    def test_failed_reconciliation_prevents_writes(self):
        with patch(
            "src.analytics_sales.validate_analytics_frames", side_effect=ValueError("totales")
        ):
            with self.assertRaisesRegex(ValueError, "totales"):
                write_analytics_tables(self.spark, self.frames, "dbo", approved=True)
        for frame in self.frames.values():
            frame.write.format.assert_not_called()

    def test_readback_mismatch_is_reported_without_retry(self):
        with patch("src.analytics_sales.validate_analytics_frames", side_effect=[{}, {"bad": 1}]):
            with self.assertRaisesRegex(RuntimeError, "totales publicados"):
                write_analytics_tables(self.spark, self.frames, "", approved=True)
        for frame in self.frames.values():
            frame.write.saveAsTable.assert_called_once()
