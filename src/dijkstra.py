
import heapq
import math


def dijkstra(graph, start):
    if start not in graph:
        raise ValueError(f"Start location is not in the graph: {start}")

    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            if neighbor not in graph:
                raise ValueError(f"Unknown graph location: {neighbor}")
            if not isinstance(weight, (int, float)) or not math.isfinite(weight):
                raise ValueError(f"Invalid edge weight from {node} to {neighbor}")
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights.")

    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}

    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(
                    priority_queue, (new_distance, neighbor)
                )

    return distances, previous


def get_path(previous, destination, start=None):
    if destination not in previous:
        raise ValueError(f"Destination is not in the graph: {destination}")

    if start is None:
        roots = [node for node, predecessor in previous.items() if predecessor is None]
        start = roots[0] if len(roots) == 1 else None

    path = []
    current = destination

    while current is not None and current in previous:
        path.append(current)
        if current == start:
            break
        current = previous.get(current)

    if not path or (start is not None and path[-1] != start):
        raise ValueError(f"Destination is unreachable: {destination}")

    return path[::-1]


if __name__ == "__main__":
    graph = {
        "Warehouse": {"A": 4, "B": 2},
        "A": {"Warehouse": 4, "B": 1, "C": 5},
        "B": {"Warehouse": 2, "A": 1, "C": 8, "D": 10},
        "C": {"A": 5, "B": 8, "D": 2},
        "D": {"B": 10, "C": 2},
    }

    start = "Warehouse"
    destination = "D"

    distances, previous = dijkstra(graph, start)
    path = get_path(previous, destination)

    print("\nDIJKSTRA SHORTEST PATH")
    print("-" * 35)
    print("Start:", start)
    print("Destination:", destination)
    print("Shortest route:", " -> ".join(path))
    print("Total distance:", distances[destination], "km")
