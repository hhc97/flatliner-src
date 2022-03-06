import ast
from os import stat
from python_parser import PythonParser
from code_to_3ac import ASTVisitor

code = []

class TACConverter:

    def __init__(self, tac):
        self.code = []
        self.tac = tac
        

    def convert(self, start = 'main'):
        handlers = {'+': self.binary_handler, '-': self.binary_handler, '*': self.binary_handler, '/': self.binary_handler,
                    'OR': self.bool_handler, 'AND': self.bool_handler, '==': self.comp_handler, '>': self.comp_handler,
                    '<': self.comp_handler, '<=': self.comp_handler, '>=': self.comp_handler,
                    'IF': self.if_handler,
                    '=': self.assignment_handler,
                    'IN': self.comp_handler
                    }
        var_d = {} # store variables here
        for statement in self.tac[start]:
            #op, left, right, var = statement
            op = statement[0]
            var = statement[3]
            node = handlers[op](statement, var_d)
            self.code.append(node)
            if var:
                var_d[var] = node

    def binary_handler(self, statement, var_d):
        print('BIN')
        op, left, right, var = statement
        op_map = {
            '+': ast.Add(),
            '-': ast.Sub(),
            '*': ast.Mult(),
            '/': ast.Div(),
        }
        left = var_d.get(left, left) # see if it's a variable
        right = var_d.get(left, right) # see if it's a variable
        return ast.BinOp(left, op_map[op], right)

    def assignment_handler(self, statement, var_d):
        _, expr, _, var = statement
        expr = var_d.get(expr, expr)
        return ast.Assign([ast.Name(var, ast.Store())], expr)
    
    def bool_handler(self, statement, var_d):
        print('BOOL')
        op, left, right, var = statement
        op_map = {
            'AND': ast.And(),
            'OR': ast.Or(),
        }
        left = var_d.get(left, left) # see if it's a variable
        right = var_d.get(left, right) # see if it's a variable
        return ast.BoolOp(op_map[op], [left, right])

    
    def comp_handler(self, statement, var_d):
        op, left, right, var = statement
        op_map = {
            '>': ast.Gt(),
            '<': ast.Lt(),
            '>=': ast.GtE(),
            '<=': ast.LtE(),
            '==': ast.Eq(),
            '!=': ast.NotEq(),
            'IN': ast.In(),
        }
        left = var_d.get(left, left) # see if it's a variable
        right = var_d.get(left, right) # see if it's a variable
        return ast.Compare(left, [op_map[op]], [right])

    def if_handler(self, statement, var_d):
        print('IF')
        pass

    
if __name__ == '__main__':
    visitor = ASTVisitor()
    infile = open('test_input.py')
    parser = PythonParser()
    parser.build()
    tree = parser.get_ast(infile.read())
    visitor.visit(tree)
    print(visitor.tac)

    converter = TACConverter(visitor.tac)
    converter.convert()
    print(converter.code)
    