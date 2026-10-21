
def knapsack(parcels, capacity):
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
        raise ValueError("Capacity must be a positive integer.")

    for parcel in parcels:
        weight = parcel.get("weight")
        value = parcel.get("value")
        if not isinstance(weight, int) or isinstance(weight, bool) or weight <= 0:
            raise ValueError("Every parcel must have a positive integer weight.")
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("Every parcel must have a non-negative integer value.")

    n = len(parcels)

    # DP table
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]

        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    value + dp[i - 1][w - weight]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    # Find selected parcels
    selected = []
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            w -= parcel["weight"]

    selected.reverse()
    return selected, dp[n][capacity]


if __name__ == "__main__":
    parcels = [
        {"id": "P101", "weight": 2, "value": 30},
        {"id": "P102", "weight": 3, "value": 40},
        {"id": "P103", "weight": 4, "value": 50},
        {"id": "P104", "weight": 5, "value": 60},
    ]

    capacity = 8

    selected, total_value = knapsack(parcels, capacity)

    print("\nKNAPSACK PACKING PLAN")
    print("-" * 35)
    print(f"Van capacity: {capacity} kg")

    total_weight = sum(p["weight"] for p in selected)

    for parcel in selected:
        print(
            f"{parcel['id']} | Weight: {parcel['weight']} kg"
            f" | Value: {parcel['value']}"
        )

    print(f"Total weight: {total_weight} kg")
    print(f"Maximum total value: {total_value}")
