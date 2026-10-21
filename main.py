
from src.data_loader import load_graph, load_parcels
from src.sorting import merge_sort
from src.knapsack import knapsack
from src.dijkstra import dijkstra, get_path
from src.tsp import nearest_neighbor


def main():
    print("=" * 50)
    print("         MINI COURIER PLANNER")
    print("=" * 50)

    parcels = load_parcels()
    graph = load_graph()
    capacity = 8

    # 1. Sorting
    print("\n1. PARCEL PRIORITIZATION")
    sorted_parcels = merge_sort(parcels)

    for parcel in sorted_parcels:
        print(
            f"{parcel['id']} | Priority: {parcel['priority']} "
            f"| Weight: {parcel['weight']} kg | Deadline: {parcel['deadline']}"
        )

    # 2. Knapsack
    print("\n2. OPTIMAL PACKING PLAN")
    selected, total_value = knapsack(parcels, capacity)
    total_weight = sum(p["weight"] for p in selected)

    for parcel in selected:
        print(f"{parcel['id']} | {parcel['weight']} kg | Value: {parcel['value']}")

    print(f"Total weight: {total_weight} kg / {capacity} kg")
    print(f"Total parcel value: {total_value}")

    # 3. Dijkstra
    print("\n3. SHORTEST PATH: WAREHOUSE TO D")
    distances, previous = dijkstra(graph, "Warehouse")
    path = get_path(previous, "D", "Warehouse")

    print("Route:", " -> ".join(path))
    print(f"Shortest distance: {distances['D']} km")

    # 4. Nearest Neighbor TSP
    print("\n4. DELIVERY TOUR")
    route, distance = nearest_neighbor(graph, "Warehouse")

    print("Route:", " -> ".join(route))
    print(f"Tour distance: {distance} km")

    print("\n" + "=" * 50)
    print("         PLANNING COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    main()
