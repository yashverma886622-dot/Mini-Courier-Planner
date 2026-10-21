
import random
import csv
import statistics
import time
from pathlib import Path

import matplotlib.pyplot as plt

from src.sorting import merge_sort
from src.knapsack import knapsack
from src.dijkstra import dijkstra


def measure_time(function, *args, repeats=5):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(*args)
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)


def generate_parcels(n):
    return [
        {
            "id": f"P{i}",
            "priority": random.randint(1, 10),
            "weight": random.randint(1, 10),
            "value": random.randint(10, 100),
        }
        for i in range(n)
    ]


def generate_graph(n):
    graph = {f"N{i}": {} for i in range(n)}

    # Connect consecutive nodes so every node is reachable.
    for i in range(n - 1):
        a, b = f"N{i}", f"N{i + 1}"
        graph[a][b] = 1
        graph[b][a] = 1

    # Add additional weighted edges.
    for i in range(n):
        for j in range(i + 2, n):
            if random.random() < 0.08:
                weight = random.randint(1, 20)
                graph[f"N{i}"][f"N{j}"] = weight
                graph[f"N{j}"][f"N{i}"] = weight

    return graph


def run_benchmarks(sizes=None, repeats=5, output_dir=None):
    sizes = sizes or [10, 50, 100, 200]
    output_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parent.parent / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    random.seed(42)
    results = []

    print("\nRUNTIME PERFORMANCE ANALYSIS")
    print("Median of", repeats, "runs; seconds")
    print("-" * 78)
    print(f"{'Input size':<14}{'Merge Sort':<18}{'Knapsack DP':<18}{'Dijkstra':<18}")

    for n in sizes:
        parcels = generate_parcels(n)
        graph = generate_graph(n)

        # Keep capacity fixed for a fair, simple experiment.
        capacity = 50

        result = {
            "input_size": n,
            "merge_sort_seconds": measure_time(merge_sort, parcels, repeats=repeats),
            "knapsack_dp_seconds": measure_time(knapsack, parcels, capacity, repeats=repeats),
            "dijkstra_seconds": measure_time(dijkstra, graph, "N0", repeats=repeats),
        }
        results.append(result)
        print(
            f"{n:<14}{result['merge_sort_seconds']:<18.6f}"
            f"{result['knapsack_dp_seconds']:<18.6f}"
            f"{result['dijkstra_seconds']:<18.6f}"
        )

    results_path = output_dir / "performance_results.csv"
    with results_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    figure, axis = plt.subplots(figsize=(9, 5))
    for key, label in (
        ("merge_sort_seconds", "Merge Sort"),
        ("knapsack_dp_seconds", "Knapsack DP (capacity 50)"),
        ("dijkstra_seconds", "Dijkstra"),
    ):
        axis.plot(sizes, [result[key] for result in results], marker="o", label=label)
    axis.set_xlabel("Number of parcels / graph nodes")
    axis.set_ylabel("Median execution time (seconds)")
    axis.set_title("Algorithm Runtime Comparison")
    axis.legend()
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    chart_path = output_dir / "runtime_chart.png"
    figure.savefig(chart_path, dpi=160)
    plt.close(figure)

    print(f"\nResults saved to {results_path}")
    print(f"Chart saved to {chart_path}")
    return results


def main():
    run_benchmarks()


if __name__ == "__main__":
    main()
