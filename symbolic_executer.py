import ast
import inspect
from z3 import *

def get_z3_variable(variable, annotation): 
    # Map Python types to Z3 types
    type_mapping = {
        int: Int,
        float: Real,
        str: String,
        bool: Bool,
    }
    
    # Get Z3 type for the annotation
    z3_type = type_mapping.get(annotation, None)
    print(f"[INFO] Creating SymVar: '{variable}' type: {annotation.__name__}, Z3_type: {z3_type.__name__}")

    # Create a symbolic variable of the Z3 type if it exists
    if z3_type is not None:
        temp = z3_type(variable)
        return temp
    else:
        temp = Int(variable)
        return temp


def func_parser(func):
    source = inspect.getsource(func)
    tree = ast.parse(source)

    content = []
    for node in ast.iter_child_nodes(tree.body[0]):
        if (node.__class__.__name__ not in ['arguments', 'Load', 'Store', 'NameConstant', 'Name', 'Pass', 'Break', 'Continue']):
            content.append(node)

    return content
    

def analyze_node(node: ast.AST, args: dict):
    # iterate over the node's body and children recursively
    # and add the constraints to the solver
    constraints = []
    
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Assign):
            # create a new symbolic variable
            # and add it to the args dict
            var_name = child.targets[0].id
            var_type = child.annotation
            args[var_name] = get_z3_variable(var_name, var_type)
            print(f"[INFO] Added new variable: '{var_name}' type: {var_type.__name__}")
            
            # add the constraint to the solver
            constraints.append(child.value)

        elif isinstance(child, ast.AugAssign):
            # add the constraint to the solver
            constraints.append(child.value)

        elif isinstance(child, ast.Return):
            # add the constraint to the solver
            constraints.append(child.value)

        elif isinstance(child, ast.If):
            # add the constraint to the solver
            constraints.append(child.test)

            # add the body of the if statement to the solver
            constraints.extend(analyze_node(child, args))

            # add the body of the else statement to the solver
            if child.orelse:
                constraints.extend(analyze_node(child.orelse[0], args))

        elif isinstance(child, ast.While):
            # add the constraint to the solver
            constraints.append(child.test)

            # add the body of the while statement to the solver
            constraints.extend(analyze_node(child, args))

        elif isinstance(child, ast.For):
            # add the constraint to the solver
            constraints.append(child.iter)

            # add the body of the for statement to the solver
            constraints.extend(analyze_node(child, args))
            
        elif isinstance(child, ast.Expr):
            # add the constraint to the solver
            constraints.append(child.value)

        elif (
            isinstance(child, ast.Call) or isinstance(child, ast.Compare) or isinstance(child, ast.BinOp) or
            isinstance(child, ast.UnaryOp) or isinstance(child, ast.BoolOp) or isinstance(child, ast.IfExp) or
            isinstance(child, ast.Subscript) or isinstance(child, ast.Attribute) or isinstance(child, ast.Constant)
        ):
            # add the constraint to the solver
            constraints.append(analyze_node(child, args))

        elif (
            isinstance(child, ast.Pass) or isinstance(child, ast.Break) or isinstance(child, ast.Continue) or
            isinstance(child, ast.arguments) or isinstance(child, ast.Load) or isinstance(child, ast.Name) 
        ):
            pass
        
        else:
            print(f"[WARNING] Unhandled node: {child.__class__.__name__}")
            constraints.append(child)
            print(ast.dump(child, indent=4))
            # print(child.__dict__)

    return constraints
    

def traverse(node, deep=0):
    print(" "*deep, "-"*8, node.__class__.__name__, "-"*8)

    # if it is a leaf node, print its value otherwise traverse its children
    if (
        isinstance(node, ast.Constant) or isinstance(node, ast.Constant) or
        isinstance(node, ast.Attribute) or isinstance(node, ast.Subscript) or
        isinstance(node, ast.Starred) or isinstance(node, ast.List) or isinstance(node, ast.Tuple) or
        isinstance(node, ast.Set) or isinstance(node, ast.Dict)
    ):
        print(" "*deep, node.value)

    elif (
        isinstance(node, ast.Name)
    ):
        print(" "*deep, node.id)
    else:
      for child_node in ast.iter_child_nodes(node):
          traverse(child_node, deep+4)

    


def analyze(func):
    source = inspect.getsource(func)

    annotations = func.__annotations__
    args = {var: get_z3_variable(var, annotations[var]) for var in annotations}

    constraints = []

    content = func_parser(func)

    for node in content:
        traverse(node)


    # print("\n[INFO] AST tree content: ")
    # for node in content:
    #     print("-"*25, node.__class__.__name__, "-"*25)
    #     print(ast.dump(node, indent=4))
    #     # print(node.__dict__)

    #     temp = analyze_node(node, args)
    #     constraints.extend(temp)


    print("\n[INFO] Constraints: ")
    for constraint in constraints:
        if isinstance(constraint, ast.AST):
            print("\t", ast.dump(constraint, indent=4))


    # create a solver and add the constraints
    solver = Solver()
    solver.add(constraints)

    print("\n[INFO] Solver: ")
    
    # check if the constraints are satisfiable
    if solver.check() == sat:
        print("\n[INFO] Constraints are satisfiable!")
        model = solver.model()
        print("\n[INFO] Model: ")
        for var in args:
            print(f"{var} = {model[args[var]]}")
    else:
        print("\n[INFO] Constraints are unsatisfiable!")

    return solver







from data.arithmetics import gcd
from data.is_odd import is_odd
from data.sum import add_two_numbers

# temp = analyze(add_two_numbers)
# temp = analyze(gcd)
temp = analyze(is_odd)
print('temp: ', temp)
