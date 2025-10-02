from .base_solver import BaseSolver

class BacktrackingKnapsack(BaseSolver):
    def solve(self, instance):
        self.best_value = 0
        self.best_solution = [0] * len(instance.items)
        self._backtrack(instance, 0, 0, 0, [0] * len(instance.items))
        return self.best_solution, self.best_value

    def _backtrack(self, instance, index, current_value, current_weight, current_solution):
        if index == len(instance.items):
            if current_weight <= instance.capacity and current_value > self.best_value:
                self.best_value = current_value
                self.best_solution = current_solution[:]
            return
        # Skip item
        self._backtrack(instance, index + 1, current_value, current_weight, current_solution)
        # Take item
        value, weight = instance.items[index]
        if current_weight + weight <= instance.capacity:
            current_solution[index] = 1
            self._backtrack(instance, index + 1, current_value + value, current_weight + weight, current_solution)
            current_solution[index] = 0

class BacktrackingTSP(BaseSolver):
    def solve(self, instance):
        raise NotImplementedError("BacktrackingTSP solver is not implemented yet.")
