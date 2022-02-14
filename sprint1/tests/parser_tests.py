"""
Test suite for the python compiler.
"""
import ast
import re

from python_parser import PythonParser


def clean_contents(s: str) -> str:
    return re.sub(r'[()]', '', s)


def compare_parser(test_input_filepath: str) -> None:
    """
    Checks that the parser can parse the input file properly by ensuring that it will be able to
    reconstruct the source code.
    """
    with open(test_input_filepath, 'r') as infile:
        file_contents = infile.read()

        parser = PythonParser()
        parser.build()
        ast_rep = parser.get_ast(file_contents)
        dump = ast.unparse(ast_rep)

        true_value = ast.unparse(ast.parse(file_contents))

        # if dump != true_value:
        #     print('Input:')
        #     print(true_value)
        #     print('Output:')
        #     print(dump)
        assert clean_contents(dump) == clean_contents(true_value), 'parsing error, contents not parsed properly'


def test_assignments():
    compare_parser('../code_examples/assignments.py')


def test_loops():
    compare_parser('./samples/loops.py')


def run_tests() -> None:
    """
    Runs all tests in this file if run as main.
    """
    passed, failed = [], []
    for name, func in globals().items():
        if name.startswith('test') and callable(func):
            try:
                func()
            except Exception as err:
                failed.append(f'{name}: {str(err)}')
                continue
            passed.append(name)
    if not failed:
        print(f'All {len(passed)} tests passed.')
    else:
        print(f'Total {len(passed) + len(failed)} tests, failed {len(failed)}:')
        for test in failed:
            print(test)


if __name__ == '__main__':
    run_tests()
