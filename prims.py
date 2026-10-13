
import json
import heapq
from pathlib import Path


def load_network():
    """Load the sample network dataset."""
    project_folder = Path(__file__).resolve().parent.parent
    data_file = project_folder / "data" / "sample_network.json"

    if not data_file.exists():
        raise FileNotFoundError(f"Dataset not found: {data_file}")

    with data_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def kruskal(nodes, edges):
    """Find an MST using Kruskal's algorithm."""

    parent = {node: node for node in nodes}
    rank = {node: 0 for node in nodes}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(a, b):
        root_a = find(a)
        root_b = find(b)

        if root_a == root_b:
            return False

        if rank[root_a] < rank[root_b]:
            parent[root_a] = root_b
        elif rank[root_a] > rank[root_b]:
            parent[root_b] = root_a
        else:
            parent[root_b] = root_a
            rank[root_a] += 1

        return True

    mst = []
    total_cost = 0

    for edge in sorted(edges, key=lambda e: e["cost"]):
        if union(edge["source"], edge["target"]):
            mst.append(edge)
            total_cost += edge["cost"]

            if len(mst) == len(nodes) - 1:
                break

    if len(mst) != len(nodes) - 1:
        raise ValueError("Network is disconnected.")

    return mst, total_cost


def prim(nodes, edges):
    """Find an MST using Prim's algorithm and a min-heap."""

    if not nodes:
        return [], 0

    adjacency = {node: [] for node in nodes}

    for edge in edges:
        u = edge["source"]
        v = edge["target"]
        cost = edge["cost"]

        adjacency[u].append((cost, v))
        adjacency[v].append((cost, u))

    start = nodes[0]
    visited = {start}
    min_heap = []

    for cost, neighbor in adjacency[start]:
        heapq.heappush(min_heap, (cost, start, neighbor))

    mst = []
    total_cost = 0

    while min_heap and len(visited) < len(nodes):
        cost, source, target = heapq.heappop(min_heap)

        if target in visited:
            continue

        visited.add(target)
        mst.append({
            "source": source,
            "target": target,
            "cost": cost
        })
        total_cost += cost

        for next_cost, neighbor in adjacency[target]:
            if neighbor not in visited:
                heapq.heappush(
                    min_heap,
                    (next_cost, target, neighbor)
                )

    if len(visited) != len(nodes):
        raise ValueError("Network is disconnected.")

    return mst, total_cost


def display_result(name, mst, total_cost):
    print(f"\n{name}")
    print("-" * 40)

    for edge in mst:
        print(
            f'{edge["source"]} -- {edge["target"]}: '
            f'{edge["cost"]} thousand INR'
        )

    print(f"Connections selected: {len(mst)}")
    print(f"Total cost: {total_cost} thousand INR")


if __name__ == "__main__":
    network = load_network()

    nodes = [node["id"] for node in network["nodes"]]
    edges = network["edges"]

    kruskal_mst, kruskal_cost = kruskal(nodes, edges)
    prim_mst, prim_cost = prim(nodes, edges)

    print("=" * 45)
    print("NETOPTIMA: MINIMUM SPANNING TREE COMPARISON")
    print("=" * 45)

    display_result("KRUSKAL'S ALGORITHM", kruskal_mst, kruskal_cost)
    display_result("PRIM'S ALGORITHM", prim_mst, prim_cost)

    print("\nCOMPARISON")
    print("-" * 40)

    if kruskal_cost == prim_cost:
        print("SUCCESS: Both algorithms found the same MST cost.")
    else:
        print("ERROR: The MST costs do not match.")

    print(f"Kruskal cost: {kruskal_cost} thousand INR")
    print(f"Prim cost:    {prim_cost} thousand INR")
