import unittest

from src.data_loader import load_graph, load_parcels
from src.dijkstra import dijkstra, get_path
from src.knapsack import knapsack
from src.sorting import merge_sort
from src.tsp import nearest_neighbor


class SortingTests(unittest.TestCase):
    def test_merge_sort_descending_and_stable(self):
        parcels = [
            {"id": "low", "priority": 1},
            {"id": "high-a", "priority": 5},
            {"id": "high-b", "priority": 5},
            {"id": "middle", "priority": 3},
        ]
        self.assertEqual(
            [parcel["id"] for parcel in merge_sort(parcels)],
            ["high-a", "high-b", "middle", "low"],
        )


class KnapsackTests(unittest.TestCase):
    def test_optimal_value_and_capacity(self):
        parcels = load_parcels()
        selected, total_value = knapsack(parcels, 8)
        self.assertEqual(total_value, 140)
        self.assertLessEqual(sum(parcel["weight"] for parcel in selected), 8)
        self.assertEqual(sum(parcel["value"] for parcel in selected), total_value)

    def test_invalid_capacity_and_weight(self):
        with self.assertRaisesRegex(ValueError, "positive integer"):
            knapsack([], 0)
        with self.assertRaisesRegex(ValueError, "positive integer weight"):
            knapsack([{"weight": 0, "value": 1}], 5)


class DijkstraTests(unittest.TestCase):
    def test_distance_and_reconstructed_path(self):
        graph = load_graph()
        distances, previous = dijkstra(graph, "Warehouse")
        self.assertEqual(distances["D"], 10)
        self.assertEqual(
            get_path(previous, "D", "Warehouse"),
            ["Warehouse", "B", "A", "C", "D"],
        )

    def test_unreachable_destination(self):
        distances, previous = dijkstra({"S": {}, "X": {}}, "S")
        self.assertEqual(distances["X"], float("inf"))
        with self.assertRaisesRegex(ValueError, "unreachable"):
            get_path(previous, "X", "S")


class TspTests(unittest.TestCase):
    def test_tour_visits_each_location_and_returns_to_start(self):
        graph = load_graph()
        route, distance = nearest_neighbor(graph, "Warehouse")
        self.assertEqual(route[0], "Warehouse")
        self.assertEqual(route[-1], "Warehouse")
        self.assertEqual(set(route[:-1]), set(graph))
        self.assertEqual(len(route), len(graph) + 1)
        self.assertEqual(distance, 22)
        self.assertTrue(all(route[index + 1] in graph[node] for index, node in enumerate(route[:-1])))

    def test_missing_return_edge_is_an_error(self):
        graph = {"S": {"A": 1}, "A": {"S": 1, "B": 1}, "B": {"A": 1}}
        with self.assertRaisesRegex(ValueError, "no return edge"):
            nearest_neighbor(graph, "S")


if __name__ == "__main__":
    unittest.main()