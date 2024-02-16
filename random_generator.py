from z3 import *
from random import randint, uniform, choice
from string import ascii_lowercase, ascii_uppercase

MIN_INT = -1000
MAX_INT = 1000
MIN_STR_LEN = 1
MAX_STR_LEN = 10

class RandomGenerator:
    def __init__(self):
        self.chars = ascii_lowercase + ascii_uppercase

    def generate(self, data_type, constraints=[], kind=None):
        if kind is None:
            kind = choice(['meet', 'dont meet'])

        if data_type == int or data_type == 'int':
            return self.generate_int(constraints, kind)
        elif data_type == float or data_type == 'float':
            return self.generate_float(constraints, kind)
        elif data_type == str or data_type == 'str':
            return self.generate_string(constraints, kind)
        elif data_type == bool or data_type == 'bool':
            return self.generate_boolean(constraints, kind)
        else:
            raise ValueError("Unsupported data type")


    def generate_int(self, constraints=[], kind='meet'):
        while True:
            value = randint(MIN_INT, MAX_INT)
            satisfies_constraints = self.satisfies_constraints(value, constraints, int)
            if self.check_constraints(value, satisfies_constraints, kind) is not None:
                return value
                
    def generate_float(self, constraints=[], kind='meet'):
        while True:
            value = round(uniform(MIN_INT, MAX_INT), 3)
            satisfies_constraints = self.satisfies_constraints(value, constraints, float)
            if self.check_constraints(value, satisfies_constraints, kind) is not None:
                return value
            
    def generate_string(self, constraints=[], kind='meet'):
        while True:
            value =  ''.join(choice(self.chars) for _ in range(randint(MIN_STR_LEN, MAX_STR_LEN)))
            satisfies_constraints = self.satisfies_constraints(value, constraints, str)
            if self.check_constraints(value, satisfies_constraints, kind) is not None:
                return value

    def generate_boolean(self, constraints=[], kind='meet'):
        while True:
            value = choice([True, False])
            satisfies_constraints = self.satisfies_constraints(value, constraints, bool)
            if self.check_constraints(value, satisfies_constraints, kind) is not None:
                return value


    def satisfies_constraints(self, value, z3_constraints, value_type):
        solver = Solver()
        solver.add(z3_constraints)

        # Create a Z3 expression for the concrete value
        concrete_value = self.create_z3_value(value, value_type)
        solver.add(concrete_value)

        return solver.check() == sat
    
    
    def check_constraints(self, value, satisfies_constraints, kind='meet'):
        if kind == 'meet' and satisfies_constraints:
                return value
        elif kind == 'dont meet' and not satisfies_constraints:
            return value
        else:
            return None


    def create_z3_value(self, value, value_type):
        if value_type == int:
            return Int('x') == value
        elif value_type == float:
            return Real('x') == value
        elif value_type == str:
            return String('x') == value
        elif value_type == bool:
            return Bool('x') == value
        else:
            raise ValueError("Unsupported value type")


