import ast
from os import stat
from python_parser import PythonParser
from code_to_3ac import ASTVisitor

code = []

class TACConverter:

    def __init__(self, tac):
        self.code = []
        self.tac = tac
        self.lineno = 0

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
            if var:
                var_d[var] = node
            if var and var.startswith('t_'):
                # don't count temp vars
                continue
            self.code.append(node)
            self.lineno += 1
            

    def constant_handler(self, constant, var_d):
        type_map = {
            int: 'int',
            str: 'str',
            bool: 'bool',
            float: 'float'
        }
        return var_d.get(constant, 
                ast.Constant(constant, type_map[type(constant)]))

    def binary_handler(self, statement, var_d):
        print('BIN')
        op, left, right, var = statement
        op_map = {
            '+': ast.Add(),
            '-': ast.Sub(),
            '*': ast.Mult(),
            '/': ast.Div(),
        }
        left = self.constant_handler(left, var_d)
        right = self.constant_handler(right, var_d)
        return ast.BinOp(left, op_map[op], right)

    def assignment_handler(self, statement, var_d):
        _, expr, _, var = statement
        expr = self.constant_handler(expr, var_d)
        return ast.Assign([ast.Name(var, ast.Store())], expr, lineno = self.lineno)
    
    def bool_handler(self, statement, var_d):
        print('BOOL')
        op, left, right, var = statement
        op_map = {
            'AND': ast.And(),
            'OR': ast.Or(),
        }
        left = self.constant_handler(left, var_d)
        right = self.constant_handler(right, var_d)
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
        left = self.constant_handler(left, var_d)
        right = self.constant_handler(right, var_d)
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
    wrap = ast.Module(converter.code, [])
    print(ast.unparse(wrap))
    