
def nearest_neighbor(graph, start):
    if start not in graph:
        raise ValueError(f"Start location is not in the graph: {start}")

    current = start
    visited = {start}
    route = [start]
    total_distance = 0

    while len(visited) < len(graph):
        nearest = None
        shortest_distance = float("inf")

        for neighbor, distance in graph[current].items():
            if neighbor not in visited and distance < shortest_distance:
                nearest = neighbor
                shortest_distance = distance

        if nearest is None:
            raise ValueError("Not all locations are reachable from the start.")

        route.append(nearest)
        visited.add(nearest)
        total_distance += shortest_distance
        current = nearest

    # Return to warehouse to complete the tour
    if start not in graph[current]:
        raise ValueError(
            f"Cannot complete delivery tour: no return edge from {current} to {start}."
        )
    total_distance += graph[current][start]
    route.append(start)

    return route, total_distance


if __name__ == "__main__":
    graph = {
        "Warehouse": {"A": 4, "B": 2},
        "A": {"Warehouse": 4, "B": 1, "C": 5},
        "B": {"Warehouse": 2, "A": 1, "C": 8, "D": 10},
        "C": {"A": 5, "B": 8, "D": 2},
        "D": {"B": 10, "C": 2},
    }

    route, distance = nearest_neighbor(graph, "Warehouse")

    print("\nNEAREST NEIGHBOR TSP ROUTE")
    print("-" * 35)
    print("Delivery route:", " -> ".join(route))
    print("Total tour distance:", distance, "km")
