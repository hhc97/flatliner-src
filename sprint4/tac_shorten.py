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
        self.mapping = {}
        self.handlers = {'+': self.comparison_handler, '-': self.comparison_handler, '*': self.comparison_handler,
                    '/': self.comparison_handler,
                    #'OR': self.bool_handler, 'AND': self.bool_handler, 
                    '==': self.comparison_handler, '>': self.comparison_handler,
                    '<': self.comparison_handler, '<=': self.comparison_handler, '>=': self.comparison_handler, '!=': self.comparison_handler,
                    '=': self.assignment_handler,
                   # 'in': self.comp_handler
                    }

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

    def get_new_name(self, name):
        if name in self.mapping:
            return self.mapping[name]
        else:
            new_var = self.generate_small_string()
            self.mapping[name] = new_var
            return new_var

    def optimize_block(self, block, var_d=None):
        statements = self.tac[block]
        opt_statements = []
        for statement in statements:
            
            #Basic statements
            if statement[0] in self.handlers:
                self.handlers[statement[0]](opt_statements, statement)
            else:
                opt_statements.append(statement)
        return opt_statements

    def call_handler(self, statement, params):
        pass

    def binary_handler(self, statement):
        pass

    def comparison_handler(self, list_of_statements, statement):
        op, arg1, arg2, mainAssign = statement 

        if type(arg1) == str and arg1 in self.mapping:
            arg1 = self.mapping[arg1]
        
        if type(arg2) == str and arg2 in self.mapping:
            arg2 = self.mapping[arg2]
        list_of_statements.append((op, arg1, arg2, mainAssign))
    
    def assignment_handler(self, list_of_statements, statement):

        op, arg1, arg2, mainAssign = statement
        if type(arg1) == str and not arg1.startswith(TEMP):
            #variable
            arg1 = self.get_new_name(arg1)
        
        if not mainAssign.startswith(TEMP):
            mainAssign = self.get_new_name(mainAssign)
        list_of_statements.append((op, arg1, arg2, mainAssign))


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

    print(optimizer.optimize_tac())