import ast
from z3 import *
import utils as ut

MIN_INT = -1000
MAX_INT = 1000
MIN_STR_LEN = 1
MAX_STR_LEN = 10

type_mapping = {
    int: Int,
    float: Real,
    str: String,
    bool: Bool,
    'int': Int,
    'float': Real,
    'str': String,
    'bool': Bool
}


def build_constraints_from_dict(data_type, data):
    constraints = []

    for param, operations in data.items():
        # ut.print_info(f"Processing parameter: {param}")
        for operation_info in operations:
            op_type = operation_info['type']
            if op_type == 'Call':
                continue
            
            if op_type == 'BinOp':

                left_var = type_mapping.get(data_type)('x')
                right_var = type_mapping.get(data_type)('y')

                if isinstance(operation_info['op'][1], ast.Add):
                    constraints.append(Or(left_var + right_var <= MAX_INT, left_var - right_var >= MIN_INT))
                elif isinstance(operation_info['op'][1], ast.Sub):
                    constraints.append(Or(left_var - right_var <= MAX_INT, left_var + right_var >= MIN_INT))
                elif isinstance(operation_info['op'][1], ast.Mult):
                    constraints.append(Or(left_var * right_var <= MAX_INT, left_var * right_var >= MIN_INT))
                elif isinstance(operation_info['op'][1], ast.Div):
                    constraints.append(right_var != 0)
                elif isinstance(operation_info['op'][1], ast.Mod):
                    constraints.append(right_var != 0)


            elif op_type == 'BoolOp':
                x = type_mapping.get(data_type)('x')

                if isinstance(operation_info['op'][1], ast.And):
                    constraints.append(x == True)
                    constraints.append(x == False)
                elif isinstance(operation_info['op'][1], ast.Or):
                    constraints.append(x == False)
                    constraints.append(x == True)
                elif isinstance(operation_info['op'][1], ast.Not):
                    constraints.append(x == True)
                    constraints.append(x == False)


            elif op_type == 'Compare':
                for i in range(len(operation_info['comparators'])):
                    x = type_mapping.get(data_type)('x')
                    y = type_mapping.get(data_type)('y')

                    if isinstance(operation_info['ops'][i][1], ast.Eq):
                        constraints.append(x == y)
                    elif isinstance(operation_info['ops'][i][1], ast.NotEq):
                        constraints.append(x != y)
                    elif isinstance(operation_info['ops'][i][1], ast.Lt):
                        constraints.append(x < y)
                    elif isinstance(operation_info['ops'][i][1], ast.LtE):
                        constraints.append(x <= y)
                    elif isinstance(operation_info['ops'][i][1], ast.Gt):
                        constraints.append(x > y)
                    elif isinstance(operation_info['ops'][i][1], ast.GtE):
                        constraints.append(x >= y)

            elif op_type == 'UnaryOp':
                x = type_mapping.get(data_type)('x')
                if isinstance(operation_info['op'][1], ast.USub):
                    constraints.append(x >= 0)
                    constraints.append(x <= 0)
                elif isinstance(operation_info['op'][1], ast.UAdd):
                    x = type_mapping.get(data_type)('x')
                    constraints.append(x <= 0)
                    constraints.append(x >= 0)
                elif (operation_info['op'][1], ast.Not):
                    x = type_mapping.get(data_type)('x')
                    constraints.append(x == True)
                    constraints.append(x == False)
                elif (operation_info['op'][1], ast.Invert):
                    x = type_mapping.get(data_type)('x')
                    constraints.append(x >= 0)
                    constraints.append(x <= 0)

            elif op_type == 'Assign':
                x = type_mapping.get(data_type)('x')

                if isinstance(operation_info['value'], ast.Constant):
                    constraints.append(x == operation_info['value'].value)

            elif op_type == 'Return':
                x = type_mapping.get(data_type)('x')

                if isinstance(operation_info['value'], ast.Constant):
                    constraints.append(x == operation_info['value'].value)

    return constraints
