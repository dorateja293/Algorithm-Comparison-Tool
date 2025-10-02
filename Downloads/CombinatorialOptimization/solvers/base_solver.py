import abc

class BaseSolver(abc.ABC):
    def __init__(self, time_limit=None, seed=None):
        self.time_limit = time_limit
        self.seed = seed

    @abc.abstractmethod
    def solve(self, instance):
        """Solve the instance and return solution and objective."""
        pass
