# Mini-Courier Planner

A compact DAA capstone that prioritizes parcel deliveries, selects a maximum-value van load, finds shortest paths through a weighted road network, and constructs an approximate delivery tour. The application reads its operational data from the CSV files in `datasets/`.

## Features

- Stable Merge Sort orders parcels by descending priority. Deadlines are retained and displayed for dispatch awareness; they are not a secondary sort key and do not alter the knapsack objective.
- 0/1 Knapsack uses dynamic programming to maximize total parcel value without exceeding the van capacity (8 kg in the demonstration). Every parcel is either selected once or not selected.
- Dijkstra's algorithm calculates shortest distances on a non-negative weighted graph and supports predecessor-based path reconstruction.
- Nearest Neighbor constructs a complete closed delivery tour. It is a heuristic approximation and is not guaranteed to find the optimal TSP tour. It reports an error if the graph cannot support a complete tour.
- CSV validation gives actionable file, schema, row, and numeric errors. Route edges are loaded as undirected edges.
- The performance runner benchmarks Merge Sort, Knapsack DP, and Dijkstra, prints a median-runtime table, and writes the results and chart to `images/`.

## Requirements and Installation

- Python 3.13.14 (compatible with Python 3.10+)
- matplotlib

Create and activate a virtual environment if desired, then install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The notebook additionally requires Jupyter and an IPython kernel in the selected environment. Install them with `python -m pip install jupyter ipykernel` if needed.

## Run

From the project root:

```powershell
python -m src.data_loader
python main.py
python -m unittest discover -s tests -v
python -m src.performance
```

Open `mini_courier_planner.ipynb` in VS Code or Jupyter and run all cells to see the same modules, datasets, results, and benchmark workflow interactively.

## Algorithms and Complexity

Let $n$ be the number of parcels, $V$ the number of locations, $E$ the number of roads, and $W$ the integer van capacity.

| Algorithm | Time | Auxiliary space | Notes |
| --- | --- | --- | --- |
| Merge Sort | $O(n \log n)$ | $O(n)$ | Stable; descending priority |
| 0/1 Knapsack DP | $O(nW)$ | $O(nW)$ | Tabulation with backtracking to recover selected parcels |
| Dijkstra with binary heap | $O((V+E)\log V)$ | $O(V+E)$ | Requires non-negative edge weights |
| Nearest Neighbor TSP | $O(V^2)$ | $O(V)$ | Approximation; no general optimality guarantee |

## Dataset Formats

`datasets/parcels.csv` has the required header `parcel_id,priority,weight,value,deadline`. Priority, weight, and value must be integers; weights must be positive and values non-negative. Deadline is retained as a string (the provided values use ISO `YYYY-MM-DD`) and is currently informational.

`datasets/routes.csv` has the required header `source,destination,distance`. Distance must be a finite non-negative number. Each row creates edges in both directions. The sample locations are Warehouse, A, B, C, and D.

## Performance Results

Method: deterministic pseudo-random inputs seeded with 42; parcel and graph sizes are 10, 50, 100, and 200. Knapsack capacity is held at 50 for every size. Each algorithm/input pair is run five times and the median wall-clock duration from `time.perf_counter()` is reported. The graph generator guarantees connectivity using a chain and adds additional random undirected edges. The benchmark is a small local experiment, not a controlled cross-machine comparison; results vary with hardware, interpreter, and system load. Very short durations are especially noisy.

Results generated in the verified Python 3.13.14 run (seconds):

| Input size | Merge Sort | Knapsack DP | Dijkstra |
| ---: | ---: | ---: | ---: |
| 10 | 0.000005 | 0.000040 | 0.000009 |
| 50 | 0.000036 | 0.000196 | 0.000083 |
| 100 | 0.000079 | 0.000433 | 0.000254 |
| 200 | 0.000533 | 0.000903 | 0.000721 |

The reproducible outputs are `images/performance_results.csv` and `images/runtime_chart.png`; regenerate them with `python -m src.performance`.

## Tests

Run `python -m unittest discover -s tests -v`. The suite covers sorting order/stability, knapsack optimality and capacity validation, Dijkstra distance/path and unreachable handling, TSP tour validity/return-edge handling, CSV integration, and invalid data.

## Project Structure

```text
main.py                         CSV-driven application entry point
src/                            Algorithms, data loading, and benchmarks
datasets/parcels.csv            Parcel records and deadlines
datasets/routes.csv             Undirected road edges
tests/test_project.py           Automated unittest coverage
images/                          Benchmark results and chart
mini_courier_planner.ipynb       Interactive project demonstration
PROJECT_REPORT.md                Capstone project report
requirements.txt                 Runtime dependency list
```

## GitHub Submission

The project is maintained in the public GitHub repository:
https://github.com/yashverma886622-dot/Mini-Courier-Planner

The source code, datasets, notebook, documentation, tests, and performance results have been pushed to the `main` branch. The repository is ready for final review and submission through the LMS/Zosima portal.
