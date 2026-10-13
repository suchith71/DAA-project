
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def find_file(filename):
    """Find a project file without assuming its exact folder."""
    for path in ROOT.rglob(filename):
        if path.is_file() and "__pycache__" not in path.parts:
            return path
    return None


def load_network():
    dataset = find_file("sample_network.json")

    if dataset is None:
        raise FileNotFoundError(
            "sample_network.json was not found. "
            "Keep it inside the project folder."
        )

    print("Dataset:", dataset)

    with open(dataset, "r", encoding="utf-8") as file:
        data = json.load(file)

    nodes = [
        node["id"] if isinstance(node, dict) else node
        for node in data["nodes"]
    ]

    return nodes, data["edges"]


def choose_mst_algorithm(nodes, edges):
    """Choose an algorithm using graph density as a heuristic."""
    n = len(nodes)

    if n <= 1:
        return "Prim", 0.0

    density = len(edges) / (n * (n - 1) / 2)

    # Configurable heuristic; benchmark results may suggest another rule.
    if density < 0.5:
        return "Kruskal", density

    return "Prim", density


def run_script(name, filename):
    script = find_file(filename)

    print(f"\n--- {name} ---")

    if script is None:
        print(f"NOT FOUND: {filename}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=script.parent,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.stdout:
            print(result.stdout.strip())

        if result.returncode != 0:
            print("FAILED:")
            print(result.stderr.strip())
            return False

        print("Execution successful.")
        return True

    except subprocess.TimeoutExpired:
        print("FAILED: execution timed out.")
        return False


def main():
    print("=" * 55)
    print("NETOPTIMA - ADAPTIVE NETWORK FRAMEWORK")
    print("=" * 55)

    try:
        nodes, edges = load_network()
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as error:
        print("Could not load the network:", error)
        return

    print("\nNETWORK ANALYSIS")
    print("Nodes:", len(nodes))
    print("Edges:", len(edges))

    selected, density = choose_mst_algorithm(nodes, edges)

    print(f"Graph density: {density:.3f}")
    print("Selected MST algorithm:", selected)

    # Run existing MST demonstration.
    mst_ok = run_script("Prim and Kruskal", "algorithms.py")

    algorithms = [
        ("Floyd-Warshall", "floyd_warshall.py"),
        ("B-Tree", "b_tree.py"),
        ("Red-Black Tree", "red_black_tree.py"),
        ("Binomial Heap", "binomial_heap.py"),
        ("Fibonacci Heap", "fibonacci_heap.py"),
        ("Knapsack", "knapsack.py"),
        ("TSP", "tsp.py"),
    ]

    results = []

    for name, filename in algorithms:
        results.append((name, run_script(name, filename)))

    print("\n" + "=" * 55)
    print("FINAL SUMMARY")
    print("=" * 55)
    print("Dataset loaded successfully.")
    print("Selected MST algorithm:", selected)
    print("Prim/Kruskal demonstration:", "PASS" if mst_ok else "FAIL")

    for name, passed in results:
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    print("\nFramework execution completed.")


if __name__ == "__main__":
    main()
