import argparse
import ast

from code_to_tac import ASTVisitor
from python_parser import PythonParser

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
        self.lineno = 0
        self.short_string_index = 0

    def generate_small_string(self):
        index = self.short_string_index
        generated_string = ''
        amount = index // len(alphabet)

        #handles multiple 
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

    def optimize_block(self, block, var_d=None):
        statements = self.tac[block]
        opt_statements = []
        for statement in statements:
            
            #Basic statements
            if statement[0] == '=':
                self.assignment_handler(opt_statements, statement)
            else:
                opt_statements.append(statement)
        return opt_statements

    def constant_handler(self, constant):
        pass

    def call_handler(self, statement, params):
        pass

    def return_handler(self, statement):
        pass

    def continue_handler(self, statement=None):
        pass

    def break_handler(self, statement=None):
        pass

    def binary_handler(self, statement):
        pass

    def assignment_handler(self, statement):
        pass

    def bool_handler(self, statement):
        pass

    def comp_handler(self, statement):
        pass

    def if_handler(self, statement, else_block, outer_code):
        pass

    def while_handler(self, statement, outer_code):
        pass

    def for_handler(self, statement, outer_code):
        pass

    def function_hander(self, statement, outer_code):
        pass

    def list_handler(self, statement, index, statements):
        pass

    def optimize_tac(self):
        optimized_tac = {}
        for scope in self.tac:
            optimized_tac[scope] = self.optimize_block(scope)
        return optimized_tac

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
    for i in range(10000):
        print(optimizer.generate_small_string())

    print(optimizer.optimize_tac())