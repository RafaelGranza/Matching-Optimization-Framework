from src.solvers.base_solver import Solver
from src.group import Group, GroupRule
from typing import List, Type


def check_preference(prefer, n, m0, m1):
    """
    Check if element N prefers element M0 over element M1.
    """
    return prefer[wn.index(m1) < prefer[n].index(m0)


def make_stable_pairs(type_a, type_b):
    """
    Stable Marriage algorithm to find stable pairs between two types.
    """
    # Assume type_a and type_b have a 'preference' attribute that is a list of preferences
    for a in type_a:
        if not hasattr(a, 'preference'):
            raise ValueError(f"Instances of type {type(a).__name__} must have a 'preference' attribute.")
    for b in type_b:
        if not hasattr(b, 'preference'):
            raise ValueError(f"Instances of type {type(b).__name__} must have a 'preference' attribute.")

    # Build preference lists
    prefer = {a: a.preference for a in type_a}
    prefer.update({b: b.preference for b in type_b})

    w_partner = {b: None for b in type_b}  # Women's partners
    m_free = set(type_a)  # Free men

    while m_free:
        m = m_free.pop()
        for w in prefer[m]:
            if w_partner[w] is None:  # Woman is free
                w_partner[w] = m
                break
            else:  # Woman is already engaged
                m1 = w_partner[w]
                if not check_preference(prefer, w, m, m1):
                    w_partner[w] = m
                    m_free.add(m1)
                    break

    return [(m, w) for w, m in w_partner.items()]

def build_groups(stable_pairs):
    """
    Build groups from stable pairs.
    """
    groups = []
    for m, w in stable_pairs:
        group = Group()
        group.add_member(m)
        group.add_member(w)
        groups.append(group)
    return groups


class StableMarriage(Solver):
    """
    Solver using the Stable Marriage algorithm for assignment problems.
    """

    @staticmethod
    def can_solve(group_rule: GroupRule):
        """
        Check if the group rule can be solved using the Stable Marriage algorithm.
        """
        if len(group_rule.cardinality_rules) != 2:
            return False
        for _, (min_count, max_count) in group_rule.cardinality_rules.items():
            if min_count != 1 or max_count != 1:
                return False
        return group_rule.stable_match and group_rule.objective_function_name == "no_statistic"

    @staticmethod
    def solve_from_instances(group_rule: GroupRule, instances: List[object]):
        """
        Solve the problem using the Stable Marriage algorithm.
        """
        type_a = [inst for inst in instances if isinstance(inst, group_rule.types[0])]
        type_b = [inst for inst in instances if isinstance(inst, group_rule.types[1])]

        stable_pairs = make_stable_pairs(type_a, type_b)
        return build_groups(stable_pairs)

    @staticmethod
    def solve_from_valid_groups(group_rule: GroupRule, groups: List[Group]):

        unique_instances = {}
        for group in groups:
            for cls, instance in group.members.items():
                if cls not in unique_instances:
                    unique_instances[cls] = list()
                for i in instance:
                    if i not in unique_instances[cls]:
                        unique_instances[cls].append(i)

        [type_a, type_b] = unique_instances.values()

        stable_pairs = make_stable_pairs(type_a, type_b)
        return build_groups(stable_pairs)