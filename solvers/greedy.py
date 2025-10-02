from .base_solver import BaseSolver
import random

class GreedyTSP(BaseSolver):
    def solve(self, instance):
        n = len(instance.nodes)
        start = self.seed % n if self.seed else 0
        tour = [start]
        unvisited = set(range(n)) - {start}
        while unvisited:
            cur = tour[-1]
            nxt = min(unvisited, key=lambda j: instance.dist_matrix[cur][j])
            tour.append(nxt)
            unvisited.remove(nxt)
        return tour, instance.evaluate_solution(tour)

class GreedyKnapsack(BaseSolver):
    def solve(self, instance):
        items = sorted(instance.items, key=lambda x: x[0] / x[1], reverse=True)
        solution = [0] * len(instance.items)
        total_weight = 0
        for i, (value, weight) in enumerate(items):
            if total_weight + weight <= instance.capacity:
                solution[i] = 1
                total_weight += weight
        return solution, instance.evaluate_solution(solution)

class GreedyMatching(BaseSolver):
    def solve(self, instance):
        # Placeholder: greedy matching
        pass
