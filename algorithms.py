import json
import heapq
from pathlib import Path


def load_network():
    path = Path(__file__).parent.parent / "data" / "sample_network.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = [
        n["id"] if isinstance(n, dict) else n
        for n in data["nodes"]
    ]

    return nodes, data["edges"]


def prim(nodes, edges):
    graph = {n: [] for n in nodes}

    for e in edges:
        u, v, w = e["source"], e["target"], e["cost"]
        graph[u].append((w, v))
        graph[v].append((w, u))

    if not nodes:
        return [], 0

    visited = {nodes[0]}
    heap = []

    for w, v in graph[nodes[0]]:
        heapq.heappush(heap, (w, nodes[0], v))

    mst = []
    total = 0

    while heap and len(visited) < len(nodes):
        w, u, v = heapq.heappop(heap)

        if v in visited:
            continue

        visited.add(v)
        mst.append({"source": u, "target": v, "cost": w})
        total += w

        for nw, nv in graph[v]:
            if nv not in visited:
                heapq.heappush(heap, (nw, v, nv))

    if len(visited) != len(nodes):
        raise ValueError("Graph is disconnected")

    return mst, total


def kruskal(nodes, edges):
    parent = {n: n for n in nodes}
    rank = {n: 0 for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)

        if a == b:
            return False

        if rank[a] < rank[b]:
            a, b = b, a

        parent[b] = a

        if rank[a] == rank[b]:
            rank[a] += 1

        return True

    mst = []
    total = 0

    for e in sorted(edges, key=lambda x: x["cost"]):
        u, v, w = e["source"], e["target"], e["cost"]

        if union(u, v):
            mst.append({"source": u, "target": v, "cost": w})
            total += w

            if len(mst) == len(nodes) - 1:
                break

    if len(mst) != max(0, len(nodes) - 1):
        raise ValueError("Graph is disconnected")

    return mst, total


if __name__ == "__main__":
    nodes, edges = load_network()

    p_mst, p_cost = prim(nodes, edges)
    k_mst, k_cost = kruskal(nodes, edges)

    print("Nodes:", len(nodes))
    print("Edges:", len(edges))
    print("\nPrim MST cost:", p_cost)
    print("Kruskal MST cost:", k_cost)

    print("\nPrim MST:")
    for edge in p_mst:
        print(edge)

    print("\nKruskal MST:")
    for edge in k_mst:
        print(edge)

    assert p_cost == k_cost, "MST costs do not match!"
    print("\nBoth algorithms agree!")