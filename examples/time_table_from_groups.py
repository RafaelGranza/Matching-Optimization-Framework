from src.group import Group, GroupRule
import itertools
from itertools import product
from src.solve import solve

# Definições das entidades (iguais ao seu exemplo)
class Professor:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Professor({self.name})"

class Room:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Room({self.name})"

class Cohort:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Cohort({self.name})"

class TimeWindow:
    def __init__(self, slot): self.slot = slot
    def __repr__(self): return f"TimeWindow({self.slot})"

class Subject:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Subject({self.name})"
    
def objective_function(groups):
    professors_by_time = dict()
    rooms_by_time = dict()
    penalty = 0
    for group in groups:
        elements = group.get_members()
        time = elements[TimeWindow][0]
        professor = elements[Professor][0]
        room = elements[Room][0]

        if time not in professors_by_time:
            professors_by_time[time] = set()
        if time not in rooms_by_time:
            rooms_by_time[time] = set()

        if professor in professors_by_time[time]:
            penalty += -1e6
        else:
            penalty += 1e6
        if room in rooms_by_time[time]:
            penalty += -1e6
        else:
            penalty += 1e6

        professors_by_time[time].add(professor)
        rooms_by_time[time].add(room)

    return penalty


# Instâncias de exemplo
professors = [Professor("ProfA"), Professor("ProfB"), Professor("ProfC")]
rooms = [Room("Room1"), Room("Room2"), Room("Room3")]
cohorts = [Cohort("Cohort1"), Cohort("Cohort2"), Cohort("Cohort3")]
time_windows = [TimeWindow("8h"), TimeWindow("10h"), TimeWindow("12h")]
subjects = [Subject("Math"), Subject("History"), Subject("Science")]

# Gera todos os grupos possíveis (cartesiano)

instances = [professors, rooms, cohorts, time_windows, subjects]
all_groups = [Group().add_member(*comb) for comb in itertools.product(*instances)]


# Definindo regras do problema
gr = GroupRule()
gr.set_cardinality(Professor, 1, 1)
gr.set_cardinality(Room, 1, 1)
gr.set_cardinality(Cohort, 1, 1)
gr.set_cardinality(TimeWindow, 1, 1)
gr.set_cardinality(Subject, 1, 1)
gr.add_statistic(valid_group)
gr.set_objective_function(objective_function)

# Otimização sobre os grupos válidos
result = solve(gr, all_groups)

print("Solução encontrada:")
for i, group in enumerate(result):
    print(f"Aula {i+1}: {group}")