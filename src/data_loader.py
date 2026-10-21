
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASETS = ROOT / "datasets"


def _read_table(filename, required_columns):
    path = Path(filename)
    try:
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            rows = [
                [cell.strip() for cell in row]
                for row in csv.reader(file, skipinitialspace=True)
                if any(cell.strip() for cell in row)
            ]
    except FileNotFoundError as error:
        raise FileNotFoundError(f"CSV file not found: {path}") from error

    if not rows:
        raise ValueError(f"CSV header is missing: {path}")

    headers = [header.strip() for header in rows[0]]
    missing = set(required_columns) - set(headers)
    if missing:
        raise ValueError(
            f"Missing columns in {path}: {sorted(missing)}. Found: {headers}"
        )
    if len(headers) != len(set(headers)):
        raise ValueError(f"Duplicate columns in {path}: {headers}")

    records = []
    for line_number, values in enumerate(rows[1:], start=2):
        if len(values) != len(headers):
            raise ValueError(
                f"Malformed row in {path} at line {line_number}: "
                f"expected {len(headers)} fields, found {len(values)}"
            )
        records.append((line_number, dict(zip(headers, values))))
    return path, records


def load_parcels(filename=None):
    if filename is None:
        filename = DATASETS / "parcels.csv"

    path, rows = _read_table(
        filename, {"parcel_id", "priority", "weight", "value", "deadline"}
    )
    parcels = []
    for line_number, row in rows:
        try:
            parcel = {
                "id": row["parcel_id"],
                "priority": int(row["priority"]),
                "weight": int(row["weight"]),
                "value": int(row["value"]),
                "deadline": row["deadline"],
            }
        except (ValueError, KeyError) as error:
            raise ValueError(
                f"Invalid parcel data in {path} at line {line_number}: {error}"
            ) from error
        if not parcel["id"] or not parcel["deadline"]:
            raise ValueError(
                f"Parcel ID and deadline must not be empty in {path} "
                f"at line {line_number}"
            )
        if parcel["weight"] <= 0:
            raise ValueError(
                f"Parcel weight must be positive in {path} at line {line_number}"
            )
        if parcel["value"] < 0:
            raise ValueError(
                f"Parcel value must be non-negative in {path} at line {line_number}"
            )
        parcels.append(parcel)

    return parcels


def load_graph(filename=None):
    if filename is None:
        filename = DATASETS / "routes.csv"

    path, rows = _read_table(filename, {"source", "destination", "distance"})
    graph = {}
    for line_number, row in rows:
        source = row["source"]
        destination = row["destination"]
        if not source or not destination:
            raise ValueError(
                f"Route endpoints must not be empty in {path} "
                f"at line {line_number}"
            )
        try:
            distance = float(row["distance"])
        except ValueError as error:
            raise ValueError(
                f"Invalid route distance in {path} at line {line_number}: "
                f"{row['distance']!r}"
            ) from error
        if not math.isfinite(distance) or distance < 0:
            raise ValueError(
                f"Route distance must be finite and non-negative in {path} "
                f"at line {line_number}"
            )

        graph.setdefault(source, {})
        graph.setdefault(destination, {})
        graph[source][destination] = distance
        graph[destination][source] = distance

    return graph


if __name__ == "__main__":
    parcels = load_parcels()
    graph = load_graph()

    print("Parcels loaded:", len(parcels))
    print("Locations loaded:", len(graph))
    print("First parcel:", parcels[0])
    print("Warehouse connections:", graph["Warehouse"])
