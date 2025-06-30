from src.group import GroupRule
import random
from typing import List, Type
from src.solve import solve

class Worker:
    def __init__(self, ID, Disabilities):
        self.ID = ID
        self.skills = random.randint(1, int(1e6)) # Simulating skills
        self.Disabilities = Disabilities
    def __repr__(self):
        return f"Worker(ID={self.ID}, Disabilities='{self.Disabilities}')"
class Job:
    def __init__(self, ID):
        self.ID = ID
        self.skills = random.randint(1, int(1e6)) # Simulating skills required
    def __repr__(self):
        return f"Job({self.ID})"

def skill_allignment(members: dict[Type, List]):
    """
    Example statistic function that calculates the difference between Workers' and Jobs' skills.
    """
    workers = members.get(Worker, [None])[0]
    jobs = members.get(Job, [None])[0]

    if workers is None or jobs is None:
        return float('inf')  # Return a high value if either is missing

    return abs(workers.skills - jobs.skills)


def gen_jobs(qnt):
    # Generate a list of Job instances
    list = []
    for i in range(qnt):
        list.append(Job(ID=i))
    return list

def gen_workers(qnt):
    # Generate a list of Worker instances, with some having disabilities
    list = []
    disabilities = ["Low Visibility", "Low Mobility", "None"]
    for i in range(0, int(qnt*0.8)):
        list.append(Worker(
            ID=i,
            Disabilities=disabilities[2]
        ))
    for i in range(int(qnt*0.8), qnt):
        list.append(Worker(
            ID=i,
            Disabilities=disabilities[random.randint(0,len(disabilities)-1)]
        ))
    return list

instances = gen_jobs(10) + gen_workers(100)

# Define the problem rules
gr = GroupRule()
gr.quotas = {"Disabilities":
            [
                ["Low Visibility", 1],
                ["Low Mobility",   1]
            ]}
gr.set_cardinality(Job, 1, 1)           # Each group must have exactly 1 job
gr.set_cardinality(Worker, 1, 1)        # Each group must have exactly 1 worker
gr.add_statistic(skill_allignment)      # Add the skill alignment statistic
gr.set_objective_function("maximize_sum_of_single_statistic")  # Use the sum of the statistic as the objective function

# Optimization
print("Answer: ", solve(gr, instances))