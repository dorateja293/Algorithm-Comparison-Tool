from .base_problem import BaseProblem
import random

class Knapsack(BaseProblem):
    def __init__(self, items=None, capacity=0):
        self.items = items or []
        self.capacity = capacity

    def generate_instance(self, seed, n, params):
        random.seed(seed)
        items = []
        for _ in range(n):
            value = random.randint(1, 100)
            weight = random.randint(1, 50)
            items.append((value, weight))
        capacity = params.get('capacity', 50)
        return Knapsack(items, capacity)

    def evaluate_solution(self, solution):
        total_value = 0
        total_weight = 0
        for i, selected in enumerate(solution):
            if selected:
                value, weight = self.items[i]
                total_value += value
                total_weight += weight
        feasible = total_weight <= self.capacity
        return total_value if feasible else 0, feasible
