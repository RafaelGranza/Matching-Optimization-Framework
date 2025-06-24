from src.group import Group, GroupRule
from typing import List, Type

class Solver:
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
