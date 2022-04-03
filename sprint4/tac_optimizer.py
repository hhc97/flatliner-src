import argparse
import ast

from code_to_tac import ASTVisitor
from python_parser import PythonParser

code = []
START = 'main'
TEMP = 't_'
BLOCK = '_L'
DEBUG = False


def printd(*args, **kwargs):
    """Printing for debugging"""
    if DEBUG:
        print(*args, **kwargs)


class TACConverter:

    def __init__(self, tac):
        self.tac = tac
        self.lineno = 0

    def convert(self, statements=None, var_d=None):
        if statements is None:
            statements = self.tac[START]  # start, otherwise we may be working on another scope
        if var_d is None: var_d = {}  # store variables here
        code = []
        index = 0
        params = []  # stack for parameters to pass
        while index < len(statements):
            statement = statements[index]
            index += 1
            op = statement[0]
            var = statement[3]
            if op == 'IF':
                pass
            if op == 'WHILE':
                pass
            if op == 'FOR':
                pass
            if op == 'DEFN':
                pass
            if op == 'START-LIST':
                pass
            if op == 'SLICE':
                pass
            if op == 'INDEX':
                pass
            if op == 'GOTO':
                pass
            if op == 'PUSH-PARAM':
                pass
            if op == 'CALL':
                pass
            self.handle_statement(statement, var_d, code)

        return code

    def handle_statement(self, statement, var_d, code):
        pass

    def constant_handler(self, constant, var_d):
        pass

    def call_handler(self, statement, var_d, params):
        pass

    def return_handler(self, statement, var_d):
        pass

    def continue_handler(self, statement=None, var_d=None):
        pass

    def break_handler(self, statement=None, var_d=None):
        pass

    def binary_handler(self, statement, var_d):
        pass

    def assignment_handler(self, statement, var_d):
        pass

    def bool_handler(self, statement, var_d):
        pass

    def comp_handler(self, statement, var_d):
        pass

    def if_handler(self, statement, var_d, else_block, outer_code):
        pass

    def while_handler(self, statement, var_d, outer_code):
        pass

    def for_handler(self, statement, var_d, outer_code):
        pass

    def function_hander(self, statement, var_d, outer_code):
        pass

    def list_handler(self, statement, var_d, index, statements):
        pass


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Take in the python source code and parses it')
    argparser.add_argument('--FILE', help='Input file with python source code', required=False)
    args = argparser.parse_args()
    file = 'test_input.py'
    if args.FILE:
        file = args.FILE

    visitor = ASTVisitor()
    infile = open(file)
    parser = PythonParser()
    parser.build()
    tree = parser.get_ast(infile.read())

    printd(ast.dump(tree, indent=4))
    visitor.visit(tree)
    printd(visitor.tac)

    converter = TACConverter(visitor.tac)
