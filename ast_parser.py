import ast
import inspect

def traverse(node, arg, indent=0):
    if isinstance(node, (ast.arguments, ast.Load, ast.Store, ast.Name, ast.Pass, ast.Break, ast.Continue)):
        return []
   
    content = []

    children = ast.iter_child_nodes(node)
    if children:
        for child in children:
            if isinstance(child, ast.Name) and child.id == arg:
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

    result = {}
    for arg in args:
        content = func_parser(func, arg)
        content = sanitize(content)
        temp = []
        for node in content:
            sub_content = {}
            for k, v in node.__dict__.items():
                if k not in ["lineno", "col_offset", "end_lineno", "end_col_offset"]:
                    # sub_content[k] = [type(v).__name__, v]
                    # if type(v).__name__ == 'list' iterate over them and capture the type of every item inside
                    if type(v).__name__ == 'list':
                        sub_content[k] = []
                        for item in v:
                            sub_content[k].append([type(item).__name__, item])
                    else:
                        sub_content[k] = [type(v).__name__, v]

            sub_content['type'] = type(node).__name__
            temp.append(sub_content)
        result[arg] = temp

    return result


def process_result(result):
    temp = {}
    for k, v in result.items():
        temp[k] = []
        for item in v:
            if 'func' in item.keys() and item['type'] == 'Call':
                temp[k].append(item['func'][1].id)
            elif 'op' in item.keys():
                temp[k].append(item['op'][0])
            elif 'ops' in item.keys():
                # it's a list of operations, so we need to extract the names
                temp[k] += [op[0] for op in item['ops']]
    
    return temp
