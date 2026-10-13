
import subprocess
import sys
from pathlib import Path

# Folder containing this test file
BASE_DIR = Path(__file__).resolve().parent

TESTS = [
    ("Prim and Kruskal", "algorithms.py"),
    ("Floyd-Warshall", "floyd_warshall.py"),
    ("Knapsack", "knapsack.py"),
    ("Travelling Salesman (TSP)", "tsp.py"),
    ("B-Tree", "b_tree.py"),
    ("Red-Black Tree", "red_black_tree.py"),
    ("Binomial Heap", "binomial_heap.py"),
    ("Fibonacci Heap", "fibonacci_heap.py"),
]

passed = []
failed = []

print("=" * 55)
print("          NETOPTIMA - ALGORITHM TEST RUNNER")
print("=" * 55)

for name, filename in TESTS:
    filepath = BASE_DIR / filename

    print(f"\nTesting: {name}")
    print("-" * 55)

    if not filepath.exists():
        print(f"FAIL: File not found: {filename}")
        failed.append(name)
        continue

    try:
        result = subprocess.run(
            [sys.executable, str(filepath)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=BASE_DIR.parent
        )

        if result.returncode == 0:
            print("PASS")
            if result.stdout.strip():
                print(result.stdout.strip())
            passed.append(name)
        else:
            print("FAIL")
            if result.stderr.strip():
                print(result.stderr.strip())
            elif result.stdout.strip():
                print(result.stdout.strip())
            failed.append(name)

    except subprocess.TimeoutExpired:
        print("FAIL: Test timed out after 30 seconds.")
        failed.append(name)

    except Exception as error:
        print(f"FAIL: {error}")
        failed.append(name)

print("\n" + "=" * 55)
print("                 FINAL TEST REPORT")
print("=" * 55)

print(f"Passed: {len(passed)}/{len(TESTS)}")
for name in passed:
    print(f"[PASS] {name}")

print(f"\nFailed: {len(failed)}/{len(TESTS)}")
for name in failed:
    print(f"[FAIL] {name}")

print("=" * 55)
