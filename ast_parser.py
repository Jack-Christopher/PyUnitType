import ast
import inspect

import pprint

def traverse(node, arg, indent=0):
    if isinstance(node, (ast.arguments, ast.Load, ast.Store, ast.Name, ast.Pass, ast.Break, ast.Continue)):
        return []
   
    content = []

    children = ast.iter_child_nodes(node)
    if children:
        for child in children:
            
            # if isinstance(child, ast.Name):
            #     print('[CH] ' + '  ' * indent + str(child) + " <" + child.id + ">", arg==child.id, node)
            # else:
            #     print('[CH] ' + '  ' * indent + str(child))
                
            if isinstance(child, ast.Name) and child.id == arg:
                # print("found arg: ", child.id, " in ", node)
                content.append(node)
            else:
                content += traverse(child, arg, indent + 2)

    return content


def func_parser(func, arg):
    source = inspect.getsource(func)
    tree = ast.parse(source)

    content = traverse(tree.body[0], arg)

    return content
    
    
            
def sanitize(content):
    temp = []
    for node in content:
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module, ast.Return)):
            temp.append(node)
    content.clear()

    return temp
            




def analyze(func):
    # source = inspect.getsource(func)
    # annotations = func.__annotations__
    
    args = list(inspect.signature(func).parameters.keys())
    print("args:", args)

    result = {}
    for arg in args:
        # print("\n[ARG] ", arg, "<"+(type(arg)).__name__+">")
        content = func_parser(func, arg)
        content = sanitize(content)
        temp = []
        for node in content:
            sub_content = {}
            # print("  [NODE] ", "<"+(type(node)).__name__+">")
            for k, v in node.__dict__.items():
                if k not in ["lineno", "col_offset", "end_lineno", "end_col_offset"]:
                    # print("    ", k, "<"+(type(v)).__name__+">:", (v.id if isinstance(v, ast.Name) else v))
                    sub_content[k] = [type(v).__name__, v]

            sub_content['type'] = type(node).__name__
            temp.append(sub_content)
            # print()
        result[arg] = temp

    pprint.pprint(result)


    return result



        





from data.arithmetics import gcd
from data.is_odd import is_odd
from data.sum import add_two_numbers
from data.foo import bar

# analyze(add_two_numbers)
# analyze(gcd)
# res = analyze(is_odd)
res = analyze(bar)

# print(res)
