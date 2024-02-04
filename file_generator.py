import os
import sys
import inspect
from random import randint

import utils as ut
import constants as c
import settings as sett
import random_generator as rg

def file_inspector(src, module_name):
    sys.path.append(src)
    the_module = __import__(module_name)

    functions = {}

    for function_name, function in the_module.__dict__.items():
        if function_name != '__builtins__' and not function_name.startswith('__'):
            functions[function_name] = function

    ut.print_info('Number of functions in module: {}'.format(len(functions)))

    return functions


def test_generator(f, typed_parameters, idx, n_functions, function_name, function):
    RG = rg.random_generator()

    random_inputs = []
    for i in range(len(typed_parameters)):
        random_inputs.append(RG.generate(typed_parameters[i][1]))

    result = function(*random_inputs)

    var_idx = 0
    f.write('def test_{}_{}():\n'.format(function_name, idx))
    for var_name, var_type in typed_parameters:
        if var_type == str:
            f.write('    var_{} = \'{}\'\n'.format(var_idx, random_inputs[var_idx]))
        else:
            f.write('    var_{} = {}\n'.format(var_idx, random_inputs[var_idx]))
        var_idx += 1
    f.write('    result = module_0.{}({})\n'.format(function_name, ', '.join(['var_{}'.format(i) for i in range(len(typed_parameters))])))
    f.write('    assert result == {}\n\n'.format(result))


def file_generator(src, dst, module_name):
    functions = file_inspector(src, module_name)
    settings = sett.get_settings(src)
    number_of_tests_per_function = settings['number_of_tests_per_function']
    filename = os.path.join(dst, 'test_{}.py'.format(module_name))
    n_functions = len(functions)
    
    with open(filename, 'w') as f:
        f.write(c.HeaderText)
        f.write('import sys\n')
        f.write('import pytest\n')
        f.write('sys.path.append(\'../\')\n')

        f.write('import {} as module_0\n\n'.format(module_name))

        idx=0
        for function_name, function in functions.items():
            # Header for each function
            f.write('\n# Tests for: {}\n\n'.format(function_name))

            # Use inspect.signature to get the function's signature
            signature = inspect.signature(function)
            # Extract the parameter names and their types
            parameter_info = [(param.name, param.annotation) for param in signature.parameters.values()]
            # Filter out parameters with no type annotation
            typed_parameters = [(name, annotation) for name, annotation in parameter_info if annotation != inspect.Parameter.empty]
            # print(typed_parameters)
            idx+=1

            for i in range(number_of_tests_per_function):
                test_generator(f, typed_parameters, i, n_functions, function_name, function)

        ut.print_info('File generated: {}'.format(filename))
    
    ut.print_separator(c.LightHorizontalLine)

