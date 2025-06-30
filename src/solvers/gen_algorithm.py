from src.solvers.base_solver import Solver
from src.group import Group, GroupRule
from typing import List, Type
import numpy as np


def optimize_by_instances(instances: List[object], group_rule: GroupRule, n_groups=3, n_generations=10000, pop_size=40, mutation_prob=0.5) -> List[Group]:
    '''
    The chromosome is a binary vector of size n_groups * n_instances, representing a n_groups x n_instances matrix.
    An element can belong to more than one group.
    '''
    from deap import base, creator, tools, algorithms
    import random
    import numpy as np

    m = len(instances)
    n = n_groups

    creator.create("FitnessMax", base.Fitness, weights=(2.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    def random_individual():
        # Binary vector of size n*m
        return [random.randint(0, 1) for _ in range(n * m)]

    toolbox.register("individual", tools.initIterate, creator.Individual, random_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def mate(parent1, parent2):
        # Uniform crossover per gene
        child1 = [parent1[i] if random.random() < 0.5 else parent2[i] for i in range(n * m)]
        child2 = [parent2[i] if random.random() < 0.5 else parent1[i] for i in range(n * m)]
        return creator.Individual(child1), creator.Individual(child2)

    def mutate(ind):
        for i in range(n * m):
            if random.random() < mutation_prob:
                ind[i] = 1 - ind[i]
        return (ind,)

    def eval_grouping(ind):
        # Converts vector to n x m matrix
        mat = np.array(ind).reshape((n, m))
        group_objs = []
        for i in range(n):
            members = [instances[j] for j in range(m) if mat[i, j] == 1]
            if members:
                g = Group()
                g.add_member(members)
                group_objs.append(g)
        score = 0
        # Validation
        for g in group_objs:
            if not group_rule.validate(g):
                score += -1e8
        # Statistics
        score += group_rule.objective_function(group_objs) if group_objs else 0
        return (score,)

    toolbox.register("evaluate", eval_grouping)
    toolbox.register("mate", mate)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)

    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.3, ngen=n_generations, halloffame=hof, verbose=False)

    best = hof[0]
    mat = np.array(best).reshape((n, m))
    group_objs = []
    for i in range(n):
        members = [instances[j] for j in range(m) if mat[i, j] == 1]
        if members:
            g = Group()
            g.add_member(members)
            group_objs.append(g)
    return group_objs

def optimize_by_groups(groups: List[Group], group_rule: GroupRule, n_generations=10000, pop_size=30, mutation_prob=0.2) -> List[Group]:
    """
    The chromosome is a bit mask b of size n, where n is the number of
    allowed Grouping Objects. The i-th bit in b indicates whether or not the i-th grouping object is
    selected at that solution option.
    """
    from deap import base, creator, tools, algorithms
    import random

    n = len(groups)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def eval_selection(individual):
        selected_groups = [g for i, g in enumerate(groups) if individual[i]]
        score = 0
        # Statistics
        score = group_rule.objective_function(selected_groups) if selected_groups else 0
        return (score,)

    toolbox.register("evaluate", eval_selection)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=mutation_prob)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)

    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.3, ngen=n_generations, halloffame=hof, verbose=False)

    best = hof[0]
    selected_groups = [g for i, g in enumerate(groups) if best[i]]
    return selected_groups

class GeneticAlgorithm(Solver):

    @staticmethod
    def can_solve(group_rule: GroupRule):
        return True

    @staticmethod
    def solve_from_instances(group_rule: GroupRule, instances: List[object]):
        answers = optimize_by_instances(instances, group_rule, n_groups=len(instances))
        return answers
    
    def solve_from_valid_groups(group_rule: GroupRule, groups: List[Group]):
        answers = optimize_by_groups(groups, group_rule)
        return answers