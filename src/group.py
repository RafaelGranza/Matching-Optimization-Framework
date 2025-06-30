from collections import defaultdict

class Group:
    """
    A container of members, which can be any type of object.
    Members are organized by their class type.
    """

    def __init__(self):
        self.members = defaultdict(list)

    def add_member(self, *instances):
        if len(instances) == 1 and isinstance(instances[0], (list, set, tuple)):
            instances = instances[0]
        for instance in instances:
            cls = type(instance)
            self.members[cls].append(instance)
        return self

    def remove_member(self, *instances):
        if len(instances) == 1 and isinstance(instances[0], (list, set, tuple)):
            instances = instances[0]
        for instance in instances:
            cls = type(instance)
            if instance in self.members[cls]:
                self.members[cls].remove(instance)
            else:
                raise ValueError(f"Instance {instance} not found in group.")
        return self

    def get_members(self, cls=None):
        if cls is None:
            return self.members
        return self.members.get(cls, [])

    def get_members_as_list(self, cls=None):
        if cls is None:
            return [instance for instances in self.members.values() for instance in instances]
        return self.members.get(cls, [])

    def __repr__(self):
        members_repr = (instance for instances in self.members.values() for instance in instances)
        return f"Group({', '.join(map(str, members_repr))})"

class GroupRule:
    """
    A class to manage a group of objects with cardinality constraints and validation.
    It allows setting cardinality rules, adding statistics and validators, and defining objective functions.
    """

    objective_function = lambda stats: 0
    objective_function_name = "no_statistic"

    """
    A flag to indicate if the matching should be stable.
    If True, the matching will be stable.
    The instances MUST have a "preference" attribute for this to work.
    """
    stable_match = False

    valid_functions = {
        "minimize_sum_of_single_statistic": lambda stats: sum(stats),
        "minimize_min_of_single_statistic": lambda stats: min(stats),
        "minimize_max_of_single_statistic": lambda stats: max(stats),
        "maximize_sum_of_single_statistic": lambda stats: -sum(stats),
        "maximize_min_of_single_statistic": lambda stats: -min(stats),
        "maximize_max_of_single_statistic": lambda stats: -max(stats),
        "no_statistic": lambda stats: 0, # No statistic, just return 0
    }

    def __init__(self):
        self.cardinality_rules = {}
        self.statistics = []
        self.validators = []
        self.types = []
        self.objective_function_name = None

    def set_objective_function(self, function):
        if isinstance(function, str):
            function_name = function.lower()
            if function_name not in self.valid_functions:
                raise ValueError(f"Invalid objective function name: {function_name}")
            self.objective_function_name = function_name
            self.objective_function = self.valid_functions[function_name]
        else:
            if not callable(function):
                raise ValueError("Objective function must be callable.")
            self.objective_function = function
            self.objective_function_name = "arbitrary"

    def set_cardinality(self, cls, min_count, max_count):
        self.cardinality_rules[cls] = (min_count, max_count)
        if cls not in self.types:
            self.types.append(cls)

    def add_validator(self, validator_fn):
        self.validators.append(validator_fn)

    def add_statistic(self, statistic):
        if not callable(statistic):
            raise ValueError("statistic must be a callable.")
        self.statistics.append(statistic)

    def validate_or_raise(self, group: Group):
        for cls, (min_count, max_count) in self.cardinality_rules.items():
            count = len(group.members[cls])
            if not (min_count <= count <= max_count):
                raise ValueError(f"Cardinality constraint violated for class {cls.__name__}: found {count}, expected from {min_count} to {max_count}.")

        for validator in self.validators:
            if not validator(group.members):
                raise ValueError(f"Custom validator '{validator.__name__}' failed.")

    def validate(self, groups: Group):
        try:
            self.validate_or_raise(groups)
        except ValueError as e:
            return False
        return True

    def set_stable_match(self, stable_match: bool):
        self.stable_match = stable_match