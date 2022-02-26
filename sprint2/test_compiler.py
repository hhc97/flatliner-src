"""
Test suite for the python compiler.
"""
import ast
import os
import re
from contextlib import redirect_stdout
from io import StringIO

from python_parser import PythonParser
from unparser import Unparser


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

        with open(f'./out/{test_input_filepath.split("/")[-1]}.ast.txt', 'w') as outfile:
            outfile.write(file_contents)
            outfile.write('\n----------------AST representation below-----------------\n')
            outfile.write(ast.dump(ast_rep, indent=4))

        true_value = ast.unparse(ast.parse(file_contents))

        # if dump != true_value:
        #     print('Input:')
        #     print(true_value)
        #     print('Output:')
        #     print(dump)
        assert clean_contents(dump) == clean_contents(true_value), f'parsing error in {test_input_filepath}'


def get_exec_output(code_string: str) -> str:
    """
    returns the exec output of the code string
    """
    capture = StringIO()
    with redirect_stdout(capture):
        exec(code_string)
    return capture.getvalue()


def check_unparse_result(test_input_filepath: str) -> None:
    with open(test_input_filepath, 'r') as infile:
        file_contents = infile.read()

        unparser = Unparser()
        unparser.set_ast(file_contents)

        result = unparser.unparse()
        assert result.count('\n') == 0, 'output is not one line'  # check that its one line
        assert result.count(';') == 0, 'output contains semicolons'  # check that no semicolons are used

        original_output = get_exec_output(file_contents)
        new_output = get_exec_output(result)
        assert original_output == new_output, f'outputs different for {test_input_filepath}'


def test_assignments():
    compare_parser('code_examples/assignments.py')


def test_loops():
    compare_parser('test_inputs/loops.py')


def test_ifs():
    compare_parser('test_inputs/ifs_test.py')


def test_comprehensive():
    compare_parser('test_inputs/comprehensive.py')


def test_real_files():
    base = './code_examples'
    for file in os.listdir(base):
        if not file.endswith('advanced_types.py'):
            compare_parser(base + '/' + file)


def test_unparse_files():
    base = './code_examples'
    ignored = ['advanced_types.py', 'for_loops.py']
    for file in os.listdir(base):
        if not any(file.endswith(ending) for ending in ignored):
            check_unparse_result(base + '/' + file)


def run_tests() -> None:
    """
    Runs all tests in this file if run as main.
    """
    passed, failed = [], []
    for name, func in globals().items():
        if name.startswith('test') and callable(func):
            try:
                func()
                print(f'{name} {"-" * (35 - len(name))} Passed')
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
