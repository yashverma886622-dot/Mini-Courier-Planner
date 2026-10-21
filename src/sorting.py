
def merge_sort(parcels):
    """Sort parcels by priority from highest to lowest."""

    if len(parcels) <= 1:
        return parcels

    mid = len(parcels) // 2

    left = merge_sort(parcels[:mid])
    right = merge_sort(parcels[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i]["priority"] >= right[j]["priority"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


if __name__ == "__main__":
    parcels = [
        {"id": "P101", "priority": 2},
        {"id": "P102", "priority": 5},
        {"id": "P103", "priority": 1},
        {"id": "P104", "priority": 4},
        {"id": "P105", "priority": 3},
    ]

    sorted_parcels = merge_sort(parcels)

    print("\nPARCEL SORTING RESULT")
    print("-" * 30)

    for parcel in sorted_parcels:
        print(f"Parcel: {parcel['id']} | Priority: {parcel['priority']}")
