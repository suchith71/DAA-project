import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "sample_network.json"


def floyd_warshall(nodes, edges):
    INF = float("inf")

    dist = {
        u: {v: (0 if u == v else INF) for v in nodes}
        for u in nodes
    }

    for u, v, weight in edges:
        dist[u][v] = min(dist[u][v], weight)
        dist[v][u] = min(dist[v][u], weight)

    for k in nodes:
        for i in nodes:
            for j in nodes:
                dist[i][j] = min(
                    dist[i][j],
                    dist[i][k] + dist[k][j]
                )

    return dist


def load_network():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    nodes = [node["id"] for node in data["nodes"]]
    edges = [
        (edge["source"], edge["target"], edge["cost"])
        for edge in data["edges"]
    ]

    return nodes, edges


if __name__ == "__main__":
    nodes, edges = load_network()
    distances = floyd_warshall(nodes, edges)

    print("FLOYD-WARSHALL ALL-PAIRS SHORTEST PATHS\n")
    print("     " + " ".join(f"{node:>5}" for node in nodes))

    for u in nodes:
        print(
            f"{u:>5} "
            + " ".join(
                f"{distances[u][v]:5.0f}"
                if distances[u][v] != float("inf")
                else f"{'INF':>5}"
                for v in nodes
            )
        )



