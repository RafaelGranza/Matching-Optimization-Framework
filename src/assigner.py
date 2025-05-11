from src.solvers.base_solver import *
from src.solvers.hungarian_algorithm import HungarianAlgorithm 
from src.solvers.bin_search_hungarian_algorithm import BinSearchHungarianAlgorithm
from typing import List, Type

class Assigner:

    solvers: List[Solver] = [
        HungarianAlgorithm,
        BinSearchHungarianAlgorithm,
        StableMarriage,
        GeneticAlgorithm, # Metaheuristic solver
        # Add more solvers here as needed
        # e.g., SimulatedAnnealing, TabuSearch, etc.
    ]

    def choose_solver(self, group_rule: GroupRule) -> Solver:
        """
        Choose the best solver based on the group members and their cardinality.
        """
        for solver in self.solvers:
            if solver.can_solve(group_rule):
                return solver
        raise ValueError("No suitable solver found for the given group.")

    def add_solver(self, solver: Type[Solver]):
        """
        Add a new solver to the list of available solvers.
        """
        self.solvers.append(solver)
    
    def remove_solver(self, solver: Type[Solver]):
        """
        Remove a solver from the list of available solvers.
        """
        self.solvers.remove(solver)
