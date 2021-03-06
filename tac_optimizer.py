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
                var = statement[1]
                if var in var_d:
                    var_d[var].append('if')
                continue
            if op == 'WHILE':
                var = statement[1]
                if var in var_d:
                    var_d[var].append('if')
                continue
            if op == 'FOR':
                continue
            if op == 'DEFN':
                continue
            if op == 'START-LIST':
                continue
            if op == 'SLICE':
                continue
            if op == 'INDEX':
                lst = statement[1]
                next_stmt = statements[index]
                index_var = next_stmt[2]
                if lst in var_d:
                    var_d[lst].append('list')
                if index_var in var_d:
                    var_d[index_var].append('index')
                index += 1
                continue
            if op == 'GOTO':
                continue
            if op == 'PUSH-ELMT' or op == 'PUSH-PARAM':
                if var in var_d:
                    var_d[var].append('call')
                continue
            if op == 'CALL':
                continue
            self.handle_statement(statement, var_d, code)
        opt_statements = []
        print(var_d)
        for statement in statements:
            var = statement[3]
            op = statement[0]
            removing = ['+', '-', '*', '/', 'OR',
                        'AND', '==', '>', '<', '<=',
                        '>=', '!=', '=', 'in']
            if op in removing and statement[2] != 'ret' and self._removed_var(var_d, var):
                var_d[var] = None
                continue
            opt_statements.append(statement)
        return opt_statements

    def handle_statement(self, statement, var_d, code):
        op, var = statement[0], statement[3]
        var1, var2 = statement[1], statement[2]
        if var:
            var_d[var] = []  # 0 occurences, we're counting

        if var1 in var_d:  # is a variable and now used in an expression
            var_d[var1].append(var)

        if var2 in var_d:  # is a variable and now used in an expression
            var_d[var2].append(var)

    def _removed_var(self, var_d, var):
        """
        Return True if variable has been or will be removed.
        """
        if not var in var_d:
            return False

        # has been removed
        if var_d[var] is None:
            return True

        # will be removed
        if not var.startswith(TEMP) and len(var_d[var]) == 0:
            return True

        for var2 in var_d[var]:
            if not self._removed_var(var_d, var2):
                return False
        return True

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
