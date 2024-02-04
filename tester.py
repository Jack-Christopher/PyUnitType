import os
import pytest

def run_tests(dst):
    """ Iterate over all files in dst and run all files 
    matching the pattern 'test_*.py' """

    for filename in os.listdir(dst):
        if filename.startswith('test_') and filename.endswith('.py'):
          pytest.main([os.path.join(dst, filename)])

if __name__ == '__main__':
    run_tests()
