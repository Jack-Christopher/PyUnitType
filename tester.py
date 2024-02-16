import os

def run_tests(dst):
    current_directory = os.path.dirname(os.path.realpath(__file__))

    tests_path = os.path.join(current_directory, dst)

    print(f'Running tests from {tests_path}')

    file_paths = []

    for file_name in os.listdir(tests_path):
        if file_name.startswith('test_') and file_name.endswith('.py'):
            test_file_path = os.path.join(tests_path, file_name)

            print(f'Running coverage for {file_name}')
            file_paths.append(test_file_path)

    os.system(f'coverage run -m pytest {" ".join(file_paths)}')
