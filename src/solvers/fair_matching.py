from src.solvers.base_solver import Solver
from src.group import Group, GroupRule
from typing import List, Type

import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import random as rd

class quota:
    def __init__(self, characteristic, distribution, scale=True):
        self.characteristic = characteristic
        self.distribution = distribution
        total = sum([ x[1] for x in self.distribution ])
        if scale:
            map(lambda x: [x[0], x[1]/total] , self.distribution)
        elif total < 1:
            distribution.append(['Remaining', 1-total])

    def __str__(self):
        return "{ " + str(self.characteristic) + ": " + str(self.distribution) + " }"

    def __mul__(self, obj):
        if len(self.distribution) == 0:
            return obj 

        if len(obj.distribution) == 0:
            return self

        new_distribution = []
        for distribution_1 in self.distribution:
            for distribution_2 in obj.distribution:
                new_distribution.append([distribution_1[0] + '+' + distribution_2[0], distribution_1[1] * distribution_2[1]])
        return quota(self.characteristic + '/' + obj.characteristic, new_distribution)

class quotas_description:
    def __init__(self, quotas):
        self.requirement = self.combine_quotas(quotas)

    def __str__(self):
        return str(self.requirement)
    
    def characteristic(self):
        return self.requirement.characteristic

    def distribution(self):
        return self.requirement.distribution

    def combine_quotas(self, quotas):
        new_requirement = quota("", [])
        for requirement in quotas:
            new_requirement *= requirement
        return new_requirement
proxy={}
class mapper:
    def __init__(self, group_a, group_b, matches, quotas_group_a):
        self.group_a = group_a
        self.group_b = group_b
        self.matches = matches
        self.quotas_group_a = quotas_group_a
        self.number_of_matches = len(group_b)

        self.graph = self.build_graph()

    def build_graph(self):
        global proxy
        proxy={}
        g = ig.Graph(directed=True)
        G = nx.Graph()
        G.add_node(len(g.vs), subset=0, name="source", label='Source')
        g.add_vertex(type='source', name="source")

        
        remaining_matches = self.number_of_matches
        for group in self.quotas_group_a.requirement.distribution:
            G.add_node(len(g.vs), name=group[0], label='Fair Group', quotas=group[1], subset=1, obj=group)
            g.add_vertex(name=group[0], quotas=group[1], type='Fair Group', obj=group)
            G.add_edge(0, len(g.vs)-1, capacity=group[1], weight=0)
            g.add_edge(0, len(g.vs)-1, capacity=group[1], weight=0)
            remaining_matches-=group[1]

        # Remaining
        if len(self.quotas_group_a.requirement.distribution):
            G.add_node(len(g.vs), name="Remaining", label='Fair Group', subset=1, obj={'extra': True})
            g.add_vertex(name="Remaining", type='Fair Group', obj={'extra': True})
            G.add_edge(0, len(g.vs)-1, capacity=remaining_matches, weight=0)
            g.add_edge(0, len(g.vs)-1, capacity=remaining_matches, weight=0)

        for obj in self.group_a:
            G.add_node(len(g.vs), obj=obj, subset=3, name="Worker", label='Worker')
            g.add_vertex(obj=obj, type='group_a')

        self.add_edges_group_and_requirement(self.group_a, self.quotas_group_a, 0, g, G)


        for obj in self.group_b:
            G.add_node(len(g.vs), obj=obj, subset=4, name="Job", label='Job')
            g.add_vertex(obj=obj, type='group_b')

        
        for hash in self.matches:
            [[_, u], [_, v], [_, w]] = hash.items()
            G.add_edge(g.vs.find(obj=self.group_a[u]).index, g.vs.find(obj=self.group_b[v]).index, capacity=1, weight=w)
            g.add_edge(g.vs.find(obj=self.group_a[u]).index, g.vs.find(obj=self.group_b[v]).index, capacity=1, weight=w)

        G.add_node(len(g.vs), subset=6, name="target", label='Target')
        g.add_vertex(type='target', name="target")

        self.add_edges_group_and_requirement(self.group_b, quotas_description([]), len(g.vs)-1, g, G)
        

        return G

    def has_quotas(self, quotas):
        return len(quotas.requirement.distribution) >= 1

    def add_edges_group_and_requirement(self, group, requirement, in_case_its_empty, g, G):
        list_of_characteristics = requirement.requirement.characteristic.split('/')
        if len(requirement.requirement.distribution) == 0:
            for obj in group:
                g.add_edge(in_case_its_empty, g.vs.find(obj=obj).index, capacity=1, weight=0)
                G.add_edge(in_case_its_empty, g.vs.find(obj=obj).index, capacity=1, weight=0)

        else:

            
            list_proxy=[]
            for dist in requirement.requirement.distribution:
                list_of_distribution = dist[0].split('/')    
                for obj in group:
                    if not any([getattr(obj, list_of_characteristics[i], None) != list_of_distribution[i] for i in range(len(list_of_distribution))]):
                        if obj not in proxy.values():
                            key = rd.random()
                            G.add_node(len(g.vs), subset=2, obj=key, name="proxy", label='proxy')
                            g.add_vertex(name='proxy', type='proxy', obj=key)
                            g.add_edge(len(g.vs)-1, g.vs.find(obj=obj).index, capacity=1, weight=0, type='proxy')
                            G.add_edge(len(g.vs)-1, g.vs.find(obj=obj).index, capacity=1, weight=0, type='proxy')
                            proxy[key] = obj
                        g.add_edge(g.vs.find(obj=dist).index, len(g.vs)-1, capacity=1, weight=0)
                        G.add_edge(g.vs.find(obj=dist).index, len(g.vs)-1, capacity=1, weight=0)

                        

            
            for obj in group:
                if obj not in proxy.values():
                    key=rd.random()
                    G.add_node(len(g.vs), subset=2, obj=key, name="proxy", label='proxy')
                    g.add_vertex(name='proxy', type='proxy', obj=key)
                    g.add_edge(len(g.vs)-1, g.vs.find(obj=obj).index, capacity=1, weight=0, type='proxy')
                    G.add_edge(len(g.vs)-1, g.vs.find(obj=obj).index, capacity=1, weight=0, type='proxy')
                    proxy[key] = obj
                proxy_obj = [i for i in proxy if proxy[i]==obj][0]
                g.add_edge(g.vs.find(obj={'extra': True}).index, g.vs.find(obj=proxy_obj).index, capacity=1, weight=0)
                G.add_edge(g.vs.find(obj={'extra': True}).index, g.vs.find(obj=proxy_obj).index, capacity=1, weight=0)

def update_graph(G, mincostFlow):
    for u in mincostFlow:
        for v in mincostFlow[u]:
            if u>v and G.edges[u, v].get('type') == 'proxy' and  G.edges[u, v]["used"]==0:
                 G.edges[u, v]["used"] = mincostFlow[u][v]
            if u > v: continue
            G.edges[u, v]["used"] = mincostFlow[u][v]

def solve(G):
    mincostFlow = nx.max_flow_min_cost(G, 0, len(G.nodes)-1)
    update_graph(G, mincostFlow)
    return[nx.maximum_flow_value(G, 0, len(G.nodes)-1), nx.cost_of_flow(G, mincostFlow)]


def gen_matching_from_instances(gr, type_a, type_b):
    list = []
    for source in range(len(type_a)):
        for destiny in range(len(type_b)):
            group = Group()
            group.add_member(type_a[source])
            group.add_member(type_b[destiny])
            list.append({
                "source": source,
                "destiny": destiny,
                'weight': gr.statistics[0](group.members)
            })
    return list

def gen_matching_from_groups(gr, groups):
    list = []
    for group in groups:
        for a in group.members[0]:
            for b in group.members[1]:
                list.append({
                    "source": a.ID,
                    "destiny": b.ID,
                    'weight': gr.statistics[0](group.members)
                })
    return list

def build_groups(m):
    used_edges = [(u, v) for u, v, d in m.graph.edges(data=True) if 'used' in d and d['used'] > 0]
    global proxy
    fair_pairs = []
    for u, v in used_edges:
        if m.graph.nodes[u]['label'] == 'Worker' and m.graph.nodes[v]['label'] == 'Job':
            fair_pairs.append((m.graph.nodes[u]['obj'], m.graph.nodes[v]['obj']))

    groups = []
    for a, b in fair_pairs:
        group = Group()
        group.add_member(a)
        group.add_member(b)
        groups.append(group)
    return groups

class FairBipartiteMatching(Solver):
    """
    Solver using the Fair Bipartite algorithm for assignment problems.
    """

    @staticmethod
    def can_solve(group_rule: GroupRule):
        if len(group_rule.cardinality_rules) != 2:
            return False
        for _, (min_count, max_count) in group_rule.cardinality_rules.items():
            if min_count != 1 or max_count != 1:
                return False

        # check if there is a validator called "fair_matching"
        return len(group_rule.quotas) > 0

    @staticmethod
    def solve_from_instances(group_rule: GroupRule, instances: List[object]):

        quotas = quotas_description([quota(quota_name, quota_definition) for quota_name, quota_definition in group_rule.quotas.items()])

        type_a = [inst for inst in instances if isinstance(inst, group_rule.types[0])]
        type_b = [inst for inst in instances if isinstance(inst, group_rule.types[1])]

        matching = gen_matching_from_instances(group_rule, type_a, type_b)
        m = mapper(type_a, type_b, matching, quotas)
        solve(m.graph)

        return build_groups(m)
    

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

        matching = gen_matching_from_groups(group_rule, groups)

        m = mapper(type_a, type_b, matching, quotas)
        solve(m.graph)

        return build_groups(m)