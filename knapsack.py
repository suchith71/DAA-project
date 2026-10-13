# Fractional Knapsack and 0/1 Knapsack

def fractional_knapsack(items, capacity):
    items = sorted(
        items,
        key=lambda item: item[1] / item[2],
        reverse=True
    )

    total_value = 0
    selected = []

    for name, value, weight in items:
        if capacity <= 0:
            break

        fraction = min(1, capacity / weight)

        total_value += value * fraction
        capacity -= weight * fraction
        selected.append((name, fraction))

    return total_value, selected


def knapsack_01(items, capacity):
    n = len(items)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, value, weight = items[i - 1]

        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]

            if weight <= w:
                dp[i][w] = max(
                    dp[i][w],
                    value + dp[i - 1][w - weight]
                )

    selected = []
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(items[i - 1])
            w -= items[i - 1][2]

    selected.reverse()
    return dp[n][capacity], selected


if __name__ == "__main__":
    items = [
        ("Router", 60, 5),
        ("Sensors", 42, 4),
        ("Backup", 30, 3),
        ("Security", 24, 2)
    ]

    capacity = 10

    print("FRACTIONAL KNAPSACK")
    value, selected = fractional_knapsack(items, capacity)
    print("Maximum value:", value)
    print("Selected items:", selected)

    print("\n0/1 KNAPSACK")
    value, selected = knapsack_01(items, capacity)
    print("Maximum value:", value)
    print("Selected items:", selected)