from src.group import Group, GroupRule
import random
from typing import List, Type
from src.solve import solve

class Man:
    def __init__(self, name, preferences=None):
        self.name = name
        self.preferences = preferences if preferences is not None else []
    def add_preference(self, preference):
        if preference not in self.preferences:
            self.preferences.append(preference)
    def __repr__(self): return f"Man({self.name})"

class Woman:
    def __init__(self, name, preferences=None):
        self.name = name
        self.preferences = preferences if preferences is not None else []
    def add_preference(self, preference):
        if preference not in self.preferences:
            self.preferences.append(preference)
    def __repr__(self): return f"Woman({self.name})"

def stable_matching_validator(members):
    males = members.get(Male, [])
    females = members.get(Female, [])
    # Cria dicionário para achar parceiro atual
    male_partner = {m: f for m, f in zip(males, females)}
    female_partner = {f: m for m, f in zip(males, females)}

    # Checa todos os pares possíveis
    for m in males:
        for w_name in preferences[m.name]:
            w = next((f for f in females if f.name == w_name), None)
            if w is None:
                continue
            # Se (m,w) não estão juntos, testamos se bloqueiam
            if female_partner[w] != m:
                current_w = male_partner[m]
                current_m = female_partner[w]

                # m prefere w mais que seu parceiro atual?
                m_prefers_w = preferences[m.name].index(w.name) < preferences[m.name].index(current_w.name)
                # w prefere m mais que seu parceiro atual?
                w_prefers_m = preferences[w.name].index(m.name) < preferences[w.name].index(current_m.name)

                if m_prefers_w and w_prefers_m:
                    # Par bloqueador encontrado
                    return False
    return True

men = {
    "John": Man("John"), "Paul": Man("Paul"), "Mike": Man("Mike"),
    "George": Man("George"), "Ringo": Man("Ringo"), "Pete": Man("Pete"),
    "Brian": Man("Brian"), "Roger": Man("Roger"), "Freddie": Man("Freddie")
}

women = {
    "Mary": Woman("Mary"), "Linda": Woman("Linda"), "Susan": Woman("Susan"),
    "Patricia": Woman("Patricia"), "Jennifer": Woman("Jennifer"), "Jessica": Woman("Jessica"),
    "Sarah": Woman("Sarah"), "Karen": Woman("Karen"), "Nancy": Woman("Nancy")
}

men_preferences = {
    "John": [women["Mary"], women["Linda"], "Susan"],
    "Paul": [women["Linda"], women["Mary"], "Susan"],
    "Mike": [women["Susan"], women["Mary"], women["Linda"]],
    "George": [women["Patricia"], women["Jennifer"], women["Jessica"]],
    "Ringo": [women["Jennifer"], women["Patricia"], women["Jessica"]],
    "Pete": [women["Jessica"], women["Patricia"], women["Jennifer"]],
    "Brian": [women["Sarah"], women["Karen"], women["Nancy"]],
    "Roger": [women["Karen"], women["Sarah"], women["Nancy"]],
    "Freddie": [women["Nancy"], women["Sarah"], women["Karen"]]
}

woman_preferences = {
    "Mary": [men["John"], men["Paul"]],
    "Linda": [men["Paul"], men["Mike"]],
    "Susan": [men["Mike"], men["George"]],
    "Patricia": [men["George"], men["Ringo"]],
    "Jennifer": [men["Ringo"], men["Pete"]],
    "Jessica": [men["Pete"], men["Brian"]],
    "Sarah": [men["Brian"], men["Roger"]],
    "Karen": [men["Roger"], men["Freddie"]],
    "Nancy": [men["Freddie"], men["John"]]
}

for name, man in woman_preferences.items():
    women[name].add_preference(man)

for name, woman in men_preferences.items():
    men[name].add_preference(woman)

instances = list(men.values()) + list(women.values())

gr = GroupRule()
gr.set_cardinality(Woman, 1, 1)
gr.set_cardinality(Man, 1, 1)
gr.set_stable_match(True)
gr.add_validator(stable_matching_validator)

print("Awnser: ", solve(gr, instances))