from src.group import Group, GroupRule
from typing import List, Type

class Solver:
    _abstract = True
    """
    Abstract class for solvers. All solvers should inherit from this class.
    """

    @staticmethod
    def can_solve(group_rule: GroupRule):
        """
        Check if the solver can solve the given group_rule.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @staticmethod
    def solve(group_rule: GroupRule, instances=List[object]):
        """
        Solve the given group.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    @staticmethod
    def solve(group_rule: GroupRule, groups: List[Group]):
        """
        Solve the given group.
        """
        raise NotImplementedError("Subclasses should implement this method.")

class StableMarriage(Solver):
    """
    Solver using the Gale-Shapley algorithm for stable marriage problems.
    """

    @staticmethod
    def can_solve(group_rule: GroupRule):
        # Check if the group can be solved using the stable marriage algorithm
        return True  # Placeholder for actual logic

    @staticmethod
    def solve(group_rule: GroupRule, *instances):
        # Implement the Gale-Shapley algorithm to solve the stable marriage problem
        pass  # Placeholder for actual logic

class GeneticAlgorithm(Solver):
    """
    Solver using a genetic algorithm for optimization problems.
    """

    @staticmethod
    def can_solve(group_rule: GroupRule):
        # Check if the group can be solved using the genetic algorithm
        return True  # Placeholder for actual logic

    @staticmethod
    def solve(group_rule: GroupRule, *instances):
        # Implement the genetic algorithm to solve the assignment problem
        pass  # Placeholder for actual logic