import tempfile
import unittest
from pathlib import Path

from src.data_loader import load_graph, load_parcels


ROOT = Path(__file__).resolve().parents[1]


class DataLoaderTests(unittest.TestCase):
    def test_loads_project_datasets(self):
        parcels = load_parcels(ROOT / "datasets" / "parcels.csv")
        graph = load_graph(ROOT / "datasets" / "routes.csv")
        self.assertEqual(len(parcels), 8)
        self.assertEqual(len(graph), 5)
        self.assertEqual(graph["Warehouse"]["A"], 4)
        self.assertEqual(graph["A"]["Warehouse"], 4)

    def test_missing_file_has_clear_error(self):
        with self.assertRaisesRegex(FileNotFoundError, "CSV file not found"):
            load_graph(ROOT / "datasets" / "missing.csv")

    def test_invalid_columns_have_clear_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "routes.csv"
            path.write_text("from,to,cost\nA,B,2\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Missing columns"):
                load_graph(path)

    def test_malformed_values_and_non_positive_weight(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "parcels.csv"
            path.write_text(
                "parcel_id,priority,weight,value,deadline\nP1,2,0,10,2026-10-22\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "weight must be positive"):
                load_parcels(path)

            path.write_text(
                "parcel_id,priority,weight,value,deadline\nP1,high,2,10,2026-10-22\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Invalid parcel data"):
                load_parcels(path)

    def test_malformed_header_and_route_number(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "routes.csv"
            path.write_text("\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "header is missing"):
                load_graph(path)
            path.write_text("source,destination,distance\nA,B,bad\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid route distance"):
                load_graph(path)


if __name__ == "__main__":
    unittest.main()
