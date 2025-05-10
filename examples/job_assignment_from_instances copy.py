from src.group import Group, GroupRule
import random
from typing import List, Type
from src.optimizer import optimize

class Worker:
    def __init__(self, name):
        self.name = name
        self.skills = random.randint(1, int(1e6)) # Simulating skills
    def __repr__(self): return f"Worker({self.name})"

class Job:
    def __init__(self, title):
        self.title = title
        self.skills = random.randint(1, int(1e6)) # Simulating skills required
    def __repr__(self): return f"Job({self.title})"

def skill_allignment(members: dict[Type, List]):
    """
    Example statistic function that calculates the difference between Workers' and Jobs' skills.
    """
    workers = members.get(Worker, [None])[0]
    jobs = members.get(Job, [None])[0]

    if workers is None or jobs is None:
        return float('inf')  # Return a high value if either is missing

    return abs(workers.skills - jobs.skills)

# Create instances
workers = [
    Worker("Alice"), Worker("Bob"), Worker("Charlie"),
    Worker("Diana"), Worker("Eve"), Worker("Frank"),
    Worker("Grace"), Worker("Hank"), Worker("Ivy"),
    Worker("Jack"), Worker("Karen")
]

jobs = [
    Job("Painting"), Job("Electrical"), Job("Plumbing"),
    Job("Cleaning"), Job("Gardening")
]

random.seed(42)  # For reproducibility

gr = GroupRule()
gr.set_cardinality(Worker, 1, 1) # exactly 1 worker per job
gr.set_cardinality(Job, 1, 1) # exactly 1 job per worker

gr.set_optimized_objective_function("minimize_sum_of_single_statistic") # using the sum of the statistic as the objective function
gr.add_statistic(skill_allignment) # adding the skill alignment statistic

print("Awnser: ", optimize(gr, workers + jobs))