# Travelling Salesperson Problem
# Backtracking and Branch and Bound

import heapq
import json
from pathlib import Path

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "sample_network.json"
)


def load_network():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    nodes = [node["id"] for node in data["nodes"]]
    edges = [
        (edge["source"], edge["target"], edge["cost"])
        for edge in data["edges"]
    ]

    return nodes, edges


def create_distance_matrix(nodes, edges):
    n = len(nodes)
    index = {node: i for i, node in enumerate(nodes)}
    infinity = float("inf")

    matrix = [[infinity] * n for _ in range(n)]

    for i in range(n):
        matrix[i][i] = 0

    for u, v, weight in edges:
        i, j = index[u], index[v]
        matrix[i][j] = weight
        matrix[j][i] = weight

    return matrix


# -------------------- BACKTRACKING --------------------

def tsp_backtracking(matrix):
    n = len(matrix)

    if n == 0:
        return float("inf"), []

    best_cost = float("inf")
    best_path = []

    def search(current, visited, cost, path):
        nonlocal best_cost, best_path

        if cost >= best_cost:
            return

        if len(path) == n:
            return_cost = matrix[current][0]

            if return_cost != float("inf"):
                total = cost + return_cost

                if total < best_cost:
                    best_cost = total
                    best_path = path + [0]

            return

        for next_node in range(n):
            if next_node not in visited:
                weight = matrix[current][next_node]

                if weight != float("inf"):
                    search(
                        next_node,
                        visited | {next_node},
                        cost + weight,
                        path + [next_node]
                    )

    search(0, {0}, 0, [0])

    return best_cost, best_path


# -------------------- BRANCH AND BOUND --------------------

def tsp_branch_bound(matrix):
    n = len(matrix)

    if n == 0:
        return float("inf"), []

    best_cost = float("inf")
    best_path = []

    # Minimum outgoing edge for each vertex
    min_outgoing = []

    for i in range(n):
        weights = [
            matrix[i][j]
            for j in range(n)
            if i != j and matrix[i][j] != float("inf")
        ]

        min_outgoing.append(
            min(weights) if weights else float("inf")
        )

    # Queue: lower bound, current cost, path, visited vertices
    queue = [(0, 0, (0,), frozenset({0}))]

    while queue:
        bound, cost, path, visited = heapq.heappop(queue)

        if bound >= best_cost:
            continue

        current = path[-1]

        if len(path) == n:
            return_cost = matrix[current][0]

            if return_cost != float("inf"):
                total = cost + return_cost

                if total < best_cost:
                    best_cost = total
                    best_path = list(path) + [0]

            continue

        for next_node in range(n):
            if next_node in visited:
                continue

            weight = matrix[current][next_node]

            if weight == float("inf"):
                continue

            new_cost = cost + weight
            remaining = [
                v for v in range(n)
                if v not in visited and v != next_node
            ]

            # Lower-bound estimate
            lower_bound = new_cost
            possible = True

            if remaining:
                options = [
                    matrix[next_node][v]
                    for v in remaining
                    if matrix[next_node][v] != float("inf")
                ]

                if not options:
                    possible = False
                else:
                    lower_bound += min(options)

                for v in remaining:
                    if min_outgoing[v] == float("inf"):
                        possible = False
                        break

                    lower_bound += min_outgoing[v]

            else:
                if matrix[next_node][0] == float("inf"):
                    possible = False
                else:
                    lower_bound += matrix[next_node][0]

            if possible and lower_bound < best_cost:
                heapq.heappush(
                    queue,
                    (
                        lower_bound,
                        new_cost,
                        path + (next_node,),
                        visited | {next_node}
                    )
                )

    return best_cost, best_path


# -------------------- TESTING --------------------

if __name__ == "__main__":
    nodes, edges = load_network()
    matrix = create_distance_matrix(nodes, edges)

    print("TSP - BACKTRACKING")

    cost1, path1 = tsp_backtracking(matrix)

    if path1:
        print("Tour:", " -> ".join(nodes[i] for i in path1))
        print("Minimum cost:", cost1)
    else:
        print("No complete tour exists.")

    print("\nTSP - BRANCH AND BOUND")

    cost2, path2 = tsp_branch_bound(matrix)

    if path2:
        print("Tour:", " -> ".join(nodes[i] for i in path2))
        print("Minimum cost:", cost2)
    else:
        print("No complete tour exists.")

    print("\nCOMPLEXITY")
    print("Backtracking: O(n!) worst-case time")
    print("Branch and Bound: O(n!) worst-case time")
    print("Optimization TSP is NP-Hard.")
    print("Decision TSP is NP-Complete.")