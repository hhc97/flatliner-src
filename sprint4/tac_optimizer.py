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


class TACOptimizer:

    def __init__(self, tac):
        self.tac = tac
        self.lineno = 0

    def optimize_block(self, block, var_d=None):
        statements = self.tac[block]
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
                if var in var_d:
                    var_d[var][1] = var_d[var][1] + 1
                continue
            if op == 'CALL':
                continue
            self.handle_statement(statement, var_d, code)
        opt_statements = []
        #print(var_d)
        for statement in statements:
            var = statement[3]
            if not var.startswith(TEMP) and var in var_d and var_d[var][1] == 0:
                continue
            opt_statements.append(statement)

        return opt_statements

    def handle_statement(self, statement, var_d, code):
        op, var = statement[0], statement[3]
        var1, var2 = statement[1], statement[2]
        handlers = {'+': self.binary_handler, '-': self.binary_handler, '*': self.binary_handler,
                    '/': self.binary_handler,
                    'OR': self.bool_handler, 'AND': self.bool_handler, '==': self.comp_handler, '>': self.comp_handler,
                    '<': self.comp_handler, '<=': self.comp_handler, '>=': self.comp_handler, '!=': self.comp_handler,
                    '=': self.assignment_handler,
                    'in': self.comp_handler,
                    'RETURN': self.return_handler,
                    'CONTINUE': self.continue_handler,
                    'BREAK': self.break_handler
                    }
        if var:
            var_d[var] = [statement, 0] # 0 occurences, we're counting
        
        if var1 in var_d: # is a variable and now used in an expression
            var_d[var1][1] = var_d[var1][1] + 1
        
        if var2 in var_d: # is a variable and now used in an expression
            var_d[var2][1] = var_d[var2][1] + 1

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

    optimizer = TACOptimizer(visitor.tac)

    print(optimizer.optimize_tac())