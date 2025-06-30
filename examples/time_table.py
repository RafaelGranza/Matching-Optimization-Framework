from src.group import GroupRule
import random
from typing import List, Type
from src.solve import solve

# Definições básicas das entidades
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


def valid_group(group):
    elements = group.get_members()
    # Verifica se o grupo tem exatamente 5 membros e se são do tipo correto
    if len(elements) != 5:
        return False
    # Verifica se todos os membros são do tipo correto, um de cada classe
    expected_types = {Professor, Room, Cohort, TimeWindow, Subject}
    if set(type(item) for item in elements) != expected_types:
        return False
    
    # Verifica se cada membro é uma instância da classe correta
    for item in elements:
        if not isinstance(item, (Professor, Room, Cohort, TimeWindow, Subject)):
            return False
    # Se passou por todas as verificações, o grupo é válido
    return True


def objective_function(groups):
    professors_by_time = dict()
    rooms_by_time = dict()
    penalty = 0
    for group in groups:
        if len(group.get_members()) > 5:
            penalty += (len(group.get_members())-5)*(-1e18)
            continue
        
        if not valid_group(group):
            penalty += -1e12
            continue

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

# Cada "aula" é um tuplo de todos os elementos
instances = professors + rooms + cohorts + time_windows + subjects

# Definindo regras do problema
gr = GroupRule()
gr.set_cardinality(Professor, 1, 1)   # Cada grupo deve ter exatamente 1 professor
gr.set_cardinality(Room, 1, 1)        # Cada grupo deve ter exatamente 1 sala
gr.set_cardinality(Cohort, 1, 1)      # Cada grupo deve ter exatamente 1 turma
gr.set_cardinality(TimeWindow, 1, 1)  # Cada grupo deve ter exatamente 1 horário
gr.set_cardinality(Subject, 1, 1)     # Cada grupo deve ter exatamente 1 disciplina

gr.add_statistic(valid_group)  # Estatística que conta o número de membros no grupo



gr.set_objective_function(objective_function)  # Usando a soma da estatística como função objetivo

# Otimização
result = optimize(gr, instances)

print("Solução encontrada:")
for i, group in enumerate(result):
    print(f"Aula {i+1}: {group}")