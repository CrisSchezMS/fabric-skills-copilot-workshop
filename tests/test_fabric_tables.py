import unittest
from unittest.mock import Mock

from src.fabric_tables import require_default_lakehouse, table_names, write_tables


class FabricWriteTests(unittest.TestCase):
    def setUp(self):
        self.spark = Mock()
        self.spark.catalog.tableExists.return_value = False
        self.frames = {}
        self.writers = {}
        for key in ("products", "stores", "sales_raw"):
            frame = Mock()
            writer = Mock()
            frame.write.format.return_value = writer
            writer.mode.return_value = writer
            writer.option.return_value = writer
            frame.count.return_value = 10
            self.frames[key] = frame
            self.writers[key] = writer
        self.spark.table.return_value.count.return_value = 10

    def test_existing_last_table_prevents_all_writes(self):
        self.spark.catalog.tableExists.side_effect = [False, False, True]
        with self.assertRaises(FileExistsError):
            write_tables(self.spark, self.frames, "dbo")
        for frame in self.frames.values():
            frame.write.format.assert_not_called()

    def test_default_mode_is_error_if_exists_and_only_workshop_tables_are_targets(self):
        result = write_tables(self.spark, self.frames, "dbo")
        self.assertEqual(result, dict.fromkeys(self.frames, 10))
        for key, name in table_names("dbo").items():
            self.frames[key].write.format.assert_called_once_with("delta")
            self.writers[key].mode.assert_called_once_with("errorifexists")
            self.writers[key].saveAsTable.assert_called_once_with(name)
            self.writers[key].option.assert_not_called()

    def test_explicit_overwrite_is_required_to_replace_tables(self):
        self.spark.catalog.tableExists.return_value = True
        write_tables(self.spark, self.frames, "", allow_overwrite=True)
        for writer in self.writers.values():
            writer.mode.assert_called_once_with("overwrite")
            writer.option.assert_called_once_with("overwriteSchema", "true")
        self.spark.sql.assert_not_called()

    def test_unsafe_schema_missing_frames_and_non_boolean_consent_fail_before_writes(self):
        for schema in ("dbo; DROP TABLE example", "other.table", "../dbo", None):
            with self.subTest(schema=schema), self.assertRaises(ValueError):
                write_tables(self.spark, self.frames, schema)
        with self.assertRaises(ValueError):
            write_tables(self.spark, {"sales_raw": self.frames["sales_raw"]}, "dbo")
        with self.assertRaises(ValueError):
            write_tables(self.spark, self.frames, "dbo", allow_overwrite="False")
        for writer in self.writers.values():
            writer.saveAsTable.assert_not_called()

    def test_readback_count_mismatch_fails(self):
        self.spark.table.return_value.count.return_value = 9
        with self.assertRaisesRegex(RuntimeError, "Recuento incorrecto"):
            write_tables(self.spark, self.frames, "dbo")

    def test_missing_lakehouse_fails_with_actionable_message(self):
        with self.assertRaisesRegex(RuntimeError, "predeterminado"):
            require_default_lakehouse({})
        require_default_lakehouse({"defaultLakehouseId": "local-test"})


if __name__ == "__main__":
    unittest.main()
