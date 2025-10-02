def dp_knapsack(items, W):
    n = len(items)
    dp = [[0]*(W+1) for _ in range(n+1)]

    for i in range(1, n+1):
        v, w, _ = items[i-1]
        for j in range(W+1):
            if w <= j:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-w] + v)
            else:
                dp[i][j] = dp[i-1][j]
    res = []
    j = W
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i-1][j]:
            res.append(items[i-1][2])
            j -= items[i-1][1]
    return res[::-1]


def dp_tsp(cities):
    # Held-Karp dynamic programming (small n)
    import itertools, math
    n = len(cities)
    if n == 0:
        return []

    dist = [[math.dist(cities[i], cities[j]) for j in range(n)] for i in range(n)]
    C = {}
    for k in range(1, n):
        C[(1<<k, k)] = (dist[0][k], 0)

    for s in range(3, n+1):
        for subset in itertools.combinations(range(1, n), s-1):
            bits = 0
            for bit in subset:
                bits |= 1<<bit
            for k in subset:
                prev = bits & ~(1<<k)
                res = []
                for m in subset:
                    if m == k:
                        continue
                    res.append((C[(prev, m)][0] + dist[m][k], m))
                C[(bits, k)] = min(res)

    bits = (1<<n) - 2
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dist[k][0], k))
    opt, parent = min(res)

    # Reconstruct path
    path = [0]
    current = parent
    current_bits = bits
    while current != 0:
        path.append(current)
        prev_bits = current_bits & ~(1 << current)
        _, prev = C[(current_bits, current)]
        current = prev
        current_bits = prev_bits
    path.reverse()
    total_dist = opt
    return path, total_dist
