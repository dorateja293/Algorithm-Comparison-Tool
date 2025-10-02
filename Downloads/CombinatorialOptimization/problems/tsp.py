import math
import random
from .base_problem import BaseProblem

class TSP(BaseProblem):
    def __init__(self, nodes=None, dist_matrix=None):
        self.nodes = nodes
        self.dist_matrix = dist_matrix
        if nodes and not dist_matrix:
            self.dist_matrix = self._compute_dist_matrix()

    def _compute_dist_matrix(self):
        n = len(self.nodes)
        dist = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    x1, y1 = self.nodes[i]
                    x2, y2 = self.nodes[j]
                    dist[i][j] = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return dist

    def generate_instance(self, seed, n, params):
        random.seed(seed)
        nodes = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
        return TSP(nodes)

    def evaluate_solution(self, solution):
        if not solution or len(solution) != len(self.nodes):
            return float('inf'), False
        total = 0
        for i in range(len(solution) - 1):
            total += self.dist_matrix[solution[i]][solution[i+1]]
        total += self.dist_matrix[solution[-1]][solution[0]]  # close tour
        return total, True
