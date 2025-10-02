import abc

class BaseProblem(abc.ABC):
    @abc.abstractmethod
    def generate_instance(self, seed, n, params):
        """Generate a problem instance."""
        pass

    @abc.abstractmethod
    def evaluate_solution(self, solution):
        """Evaluate solution: return objective value and feasibility boolean."""
        pass

    def get_neighborhood(self, solution):
        """Optional: get neighborhood for local search."""
        return []

    def decode_representation(self, representation):
        """Optional: decode solver representation to solution."""
        return representation
