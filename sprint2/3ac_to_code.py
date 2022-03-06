import ast
from os import stat

from numpy import var
from python_parser import PythonParser
from code_to_3ac import ASTVisitor

code = []
START = 'main'
class TACConverter:

    def __init__(self, tac):
        #self.code = []
        self.tac = tac
        self.lineno = 0

    def convert(self, statements = None, var_d=None):
        if statements is None:
            statements = self.tac[START] #start
        if var_d is None: var_d = {} # store variables here
        code = []
        index = 0
        while index < len(statements):
            statement = statements[index]
            index += 1
            op = statement[0]
            var = statement[3]
            if op == 'IF':
                # everything till GOTO is else
                else_block = statements[index:]
                self.if_handler(statement, var_d, else_block, code)
                return code # it'll handle the rest of the main block too
            if op == 'GOTO':
                return code
            self.handle_statement(statement, var_d, code)
        
        return code
            
    def handle_statement(self, statement, var_d, code):
        op, var = statement[0], statement[3]
        handlers = {'+': self.binary_handler, '-': self.binary_handler, '*': self.binary_handler, '/': self.binary_handler,
                    'OR': self.bool_handler, 'AND': self.bool_handler, '==': self.comp_handler, '>': self.comp_handler,
                    '<': self.comp_handler, '<=': self.comp_handler, '>=': self.comp_handler,
                    '=': self.assignment_handler,
                    'IN': self.comp_handler
                    }
        node = handlers[op](statement, var_d)
        if var:
            var_d[var] = node
        
        if var and var.startswith('t_'):
                # don't count temp vars
                return
        code.append(node)
        self.lineno += 1

    def constant_handler(self, constant, var_d):
        type_map = {
            int: 'int',
            str: 'str',
            bool: 'bool',
            float: 'float'
        }
        if constant in var_d:
            if not constant.startswith('t_'):
                return ast.Name(constant, ast.Load())
            return var_d[constant]
        return ast.Constant(constant, type_map[type(constant)])

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

    def if_handler(self, statement, var_d, else_block, outer_code):
        print('IF')
        cond = var_d[statement[1]]
        if_block = statement[3]
        index = 0
        while index < len(else_block):
            statement = else_block[index]
            op, var = statement[0], statement[3]
            if var and var.startswith('t_'):
                # need to load temp variables
                self.handle_statement(statement, var_d, [])
            else:
                break
            index += 1
        body = self.convert(self.tac[if_block], var_d.copy())
        else_block = self.convert(else_block[index:], var_d.copy())

        # handles elif to prevent duplication
        if statement[0] == 'IF':
            else_block = else_block[:1]

        outer_code.append(ast.If(cond, body, else_block))     
        goto_block = self.tac[if_block][-1][3]
        # add goto code to outer code
        outer_code.extend(self.convert(self.tac[goto_block], var_d))

    
if __name__ == '__main__':
    visitor = ASTVisitor()
    infile = open('test_input.py')
    parser = PythonParser()
    parser.build()
    tree = parser.get_ast(infile.read())
    visitor.visit(tree)
    print(visitor.tac)

    converter = TACConverter(visitor.tac)
    code = converter.convert()
    wrap = ast.Module(code, [])
    #print(ast.dump(wrap, indent=4))
    print(f'Code:\n{ast.unparse(wrap)}')
    