from src.group import Group, GroupRule
from typing import List, Type
from src.assigner import Assigner

def optimize(gr: GroupRule, instances: List[object]):
    assigner = Assigner()
    solver = assigner.choose_solver(gr)

    if all(isinstance(inst, Group) for inst in instances):
        return solver.solve_from_valid_groups(gr, instances)
    return solver.solve_from_instances(gr, instances)
