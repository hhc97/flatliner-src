import argparse
import ast
from copy import deepcopy

from code_to_tac import ASTVisitor
from python_parser import PythonParser
from tac_to_code import TACConverter

code = []
START = 'main'
TEMP = 't_'
BLOCK = '_L'
DEBUG = False
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def printd(*args, **kwargs):
    """Printing for debugging"""
    if DEBUG:
        print(*args, **kwargs)


class TACShortener:

    def __init__(self, tac):
        self.tac = tac
        self.short_string_index = 0
        self.mapping = {}
        self.handlers = {'+': self.comparison_handler, '-': self.comparison_handler, '*': self.comparison_handler,
                         '/': self.comparison_handler,
                         'OR': self.comparison_handler, 'AND': self.comparison_handler,
                         '==': self.comparison_handler, '>': self.comparison_handler,
                         '<': self.comparison_handler, '<=': self.comparison_handler, '>=': self.comparison_handler,
                         '!=': self.comparison_handler,
                         '=': self.assignment_handler,
                         'in': self.comparison_handler,
                         'DEFN': self.function_handler,
                         'ADD-PARAM': self.add_param_handler,
                         'PUSH-PARAM': self.push_param_handler,
                         'PUSH-ELMT': self.push_elmt_handler,
                         'CALL': self.call_handler,
                         'INDEX': self.index_handler,
                         'SLICE': self.slice_handler,
                         'GOTO': self.goto_handler,
                         'IF': self.control_flow_handler,
                         'WHILE': self.control_flow_handler,
                         'FOR': self.control_flow_handler,
                         'RETURN': self.return_handler
                         }
        self.optimized_tac_statements = {}
        self.keys_done = set()

    def generate_small_string(self):
        index = self.short_string_index
        generated_string = ''
        amount = index // len(alphabet)

        # handles multiple
        while amount > len(alphabet):
            generated_string += alphabet[-1]
            amount -= len(alphabet)
        if amount > 0:
            generated_string = alphabet[amount - 1]
        index = index % len(alphabet)

        if index >= 0:
            generated_string += alphabet[index]
        self.short_string_index += 1
        return generated_string

    def get_new_name(self, name):
        if name in self.mapping:
            return self.mapping[name]
        else:
            new_var = self.generate_small_string()
            self.mapping[name] = new_var
            return new_var

    def call_handler(self, list_of_statements, statement):
        op, objName, length, var = statement

        if objName != None:
            objName = self.mapping[objName]

        if var in self.mapping:
            var = self.mapping[var]
        list_of_statements.append((op, objName, length, var))

    def add_param_handler(self, list_of_statements, statement):
        list_of_statements.append((statement[0], None, None, self.get_new_name(statement[-1])))

    def push_param_handler(self, list_of_statements, statement):
        op, _, _, var = statement

        if type(var) == str and var in self.mapping:
            var = self.mapping[var]
        list_of_statements.append((op, None, None, var))

    def push_elmt_handler(self, list_of_statements, statement):

        op, arg1, arg2, value = statement
        if type(value) == str and value in self.mapping:
            value = self.mapping[value]

        list_of_statements.append((op, arg1, arg2, value))

    def function_handler(self, list_of_statements, statement):
        # Add statement to old key
        statement_name = statement[-1]
        list_of_statements.append((statement[0], None, None, self.get_new_name(statement_name)))

        old_mapping = self.mapping
        self.mapping = deepcopy(self.mapping)
        self.optimize_tac(statement_name, self.get_new_name(statement_name))
        self.mapping = old_mapping

    def comparison_handler(self, list_of_statements, statement):
        op, arg1, arg2, mainAssign = statement

        if type(arg1) == str and arg1 in self.mapping:
            arg1 = self.mapping[arg1]

        if type(arg2) == str and arg2 in self.mapping:
            arg2 = self.mapping[arg2]
        list_of_statements.append((op, arg1, arg2, mainAssign))

    def return_handler(self, list_of_statements, statement):
        op, arg1, arg2, mainAssign = statement
        if type(mainAssign) == str and mainAssign in self.mapping:
            mainAssign = self.mapping[mainAssign]
        list_of_statements.append((op, arg1, arg2, mainAssign))

    def assignment_handler(self, list_of_statements, statement):

        op, arg1, arg2, mainAssign = statement
        if type(arg1) == str and not arg1.startswith(TEMP):
            # variable
            arg1 = self.get_new_name(arg1)

        if not mainAssign.startswith(TEMP):
            mainAssign = self.get_new_name(mainAssign)
        list_of_statements.append((op, arg1, arg2, mainAssign))

    def index_handler(self, list_of_statements, statement):
        op, arg1, arg2, var = statement

        if arg1 in self.mapping:
            arg1 = self.mapping[arg1]

        if arg2 in self.mapping and not arg2.startswith(TEMP):
            arg2 = self.mapping[arg2]

        list_of_statements.append((op, arg1, arg2, var))

    def slice_handler(self, list_of_statements, statement):
        op, arg1, arg2, var = statement
        if arg1 in self.mapping:
            arg1 = self.mapping[arg1]
        list_of_statements.append((op, arg1, arg2, var))

    def control_flow_handler(self, list_of_statements, statement):

        op, arg1, arg2, key = statement

        if type(arg1) == str and not arg1.startswith(TEMP):
            arg1 = self.get_new_name(arg1)

        if type(arg2) == str and not arg2.startswith(TEMP):
            arg2 = self.get_new_name(arg2)

        list_of_statements.append((op, arg1, arg2, key))
        if not key in self.keys_done and key in self.tac:
            self.optimize_tac(key, key)
            self.keys_done.add(key)

    def goto_handler(self, list_of_statements, statement):
        list_of_statements.append(statement)
        key = statement[-1]
        if not key in self.keys_done and key in self.tac:
            self.optimize_tac(key, key)
            self.keys_done.add(key)

    def optimize_tac(self, block='main', new_key='main'):
        statements = self.tac[block]
        opt_statements = []
        for statement in statements:

            # Basic statements
            if statement[0] in self.handlers:
                self.handlers[statement[0]](opt_statements, statement)
            else:
                opt_statements.append(statement)
        self.optimized_tac_statements[new_key] = opt_statements


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

    optimizer = TACShortener(visitor.tac)

    optimizer.optimize_tac()
    print('optimized_tac:')
    print(optimizer.optimized_tac_statements)

    converter = TACConverter(optimizer.optimized_tac_statements)
    wrap = converter.get_ast()

    printd(ast.dump(wrap, indent=4))
    print(f'Code:\n{ast.unparse(wrap)}')
