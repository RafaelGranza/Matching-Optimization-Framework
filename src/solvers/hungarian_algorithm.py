from src.solvers.base_solver import Solver
from src.group import Group, GroupRule
from typing import List, Type
import numpy as np
from scipy.optimize import linear_sum_assignment


def build_cost_matrix_from_groups(group_rule, groups):
    """
    Build a cost matrix from the given groups, considering two types of objects.
    """
    # count the unique instances of each type in the groups
    unique_instances = {}
    for group in groups:
        for cls, instance   in group.members.items():
            if cls not in unique_instances:
                unique_instances[cls] = list()
            for i in instance:
                if i not in unique_instances[cls]:
                    unique_instances[cls].append(i)

    [type_a, type_b] = unique_instances.values()
    n = len(type_a)
    m = len(type_b)
    cost_matrix = np.zeros((n, m))

    for i in range(n):
        for j in range(m):
            group = Group()
            group.add_member(unique_instances[group_rule.types[0]][i])
            group.add_member(unique_instances[group_rule.types[1]][j])
            cost_matrix[i][j] = group_rule.statistics[0](group.members)
    
    return cost_matrix

def recover_groups_from_groups(matching, groups):
    """
    Recover the groups from the matching result.
    """
    unique_instances = {}
    for group in groups:
        for cls, instance   in group.members.items():
            if cls not in unique_instances:
                unique_instances[cls] = list()
            for i in instance:
                if i not in unique_instances[cls]:
                    unique_instances[cls].append(i)

    types = list(unique_instances.keys())
    
    result_groups = []
    for i, j in matching:
        group = Group()
        group.add_member(unique_instances[types[0]][i])
        group.add_member(unique_instances[types[1]][j])
        result_groups.append(group)
    return result_groups


def build_cost_matrix(group_rule, type_a, type_b):
    """
    Build a cost matrix from the given instances, considering two types of objects.
    """
    n, m = len(type_a), len(type_b)
    cost_matrix = np.zeros((n, m))
    
    for i in range(n):
        for j in range(m):
            group = Group()
            group.add_member(type_a[i])
            group.add_member(type_b[j])
            cost_matrix[i][j] = group_rule.statistics[0](group.members)
    
    return cost_matrix

def recover_groups(matching, type_a, type_b):
    """
    Recover the groups from the matching result.
    """
    groups = []
    for i, j in matching:
        group = Group()
        group.add_member(type_a[i])
        group.add_member(type_b[j])
        groups.append(group)
    return groups

class HungarianAlgorithm(Solver):
    """
    Solver using the Hungarian algorithm for assignment problems.
    """

    @staticmethod
    def can_solve(group_rule: GroupRule):
        if len(group_rule.cardinality_rules) != 2:
            return False
        for cls, (min_count, max_count) in group_rule.cardinality_rules.items():
            if min_count != 1 or max_count != 1:
                return False
        return group_rule.objective_function_name == "minimize_sum_of_single_statistic"

    @staticmethod
    def solve_from_instances(group_rule: GroupRule, instances: List[object]):

        type_a = [inst for inst in instances if isinstance(inst, group_rule.types[0])]
        type_b = [inst for inst in instances if isinstance(inst, group_rule.types[1])]

        matrix = build_cost_matrix(group_rule, type_a, type_b)
        row_ind, col_ind = linear_sum_assignment(matrix)
        matching = list(zip(row_ind, col_ind))
        return recover_groups(matching, type_a, type_b)

    @staticmethod
    def solve_from_valid_groups(group_rule: GroupRule, groups: List[Group]):
        matrix = build_cost_matrix_from_groups(group_rule, groups)
        row_ind, col_ind = linear_sum_assignment(matrix)
        matching = list(zip(row_ind, col_ind))
        return recover_groups_from_groups(matching, groups)