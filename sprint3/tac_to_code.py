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
            statements = self.tac[START]  # start
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
                # everything till GOTO is else
                else_block = statements[index:]
                self.if_handler(statement, var_d, else_block, code)
                return code  # it'll handle the rest of the main block too
            if op == 'WHILE':
                self.while_handler(statement, var_d.copy(), code)
                return code  # it'll handle the rest of the main block too
            if op == 'FOR':
                self.for_handler(statement, var_d.copy(), code)
                return code  # it'll handle the rest of the main block too
            if op == 'DEFN':
                self.function_hander(statement, var_d.copy(), code)
                continue
            if op == 'START-LIST':
                node, index = self.list_handler(statement, var_d, index, statements)
                self.lineno += 1
                if index < len(statements):
                    next_stmt = statements[index]
                    if var in next_stmt:
                        continue
                expr_node = ast.Expr(node)
                code.append(expr_node)
                continue
            if op == 'GOTO':
                return code
            if op == 'PUSH-PARAM':
                params.append(var)
                continue
            if op == 'CALL':
                node = self.call_handler(statement, var_d, params)
                self.lineno += 1
                var_d['ret'] = node
                if index < len(statements):
                    next_stmt = statements[index]
                    if 'ret' in next_stmt:
                        continue
                expr_node = ast.Expr(node)
                code.append(expr_node)
                continue
            self.handle_statement(statement, var_d, code)

        return code

    def handle_statement(self, statement, var_d, code):
        op, var = statement[0], statement[3]
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
        node = handlers[op](statement, var_d)
        if var:
            var_d[var] = node

        if op != 'RETURN' and var and var.startswith(TEMP):
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
            if not (constant.startswith(TEMP) or constant == 'ret'):
                return ast.Name(constant, ast.Load())
            return var_d[constant]
        if DEBUG and isinstance(constant, str):
            print(f'const {constant} not found in {var_d}')
        return ast.Constant(constant, type_map[type(constant)])

    def call_handler(self, statement, var_d, params):
        printd('CALL')
        num_params = statement[2]
        call_params = params[-num_params:]
        for _ in range(num_params): 
            if params: params.pop()
        name = ast.Name(statement[3], ast.Load())
        for i, p in enumerate(call_params):
            call_params[i] = self.constant_handler(p, var_d)
        return ast.Call(name, call_params, [], lineno = self.lineno)

    def return_handler(self, statement, var_d):
        printd('RETURN')
        right_side = self.constant_handler(statement[3], var_d)
        return ast.Return(right_side)

    def continue_handler(self, statement=None, var_d=None):
        return ast.Continue()
    
    def break_handler(self, statement=None, var_d=None):
        return ast.Break()

    def binary_handler(self, statement, var_d):
        printd('BIN')
        op, left, right, var = statement
        op_map = {
            '+': ast.Add(),
            '-': ast.Sub(),
            '*': ast.Mult(),
            '/': ast.Div(),
            '%': ast.Mod()
        }
        left = self.constant_handler(left, var_d)
        right = self.constant_handler(right, var_d)
        return ast.BinOp(left, op_map[op], right)

    def assignment_handler(self, statement, var_d):
        _, expr, _, var = statement
        expr = self.constant_handler(expr, var_d)
        return ast.Assign([ast.Name(var, ast.Store())], expr, lineno=self.lineno)

    def bool_handler(self, statement, var_d):
        printd('BOOL')
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
            'in': ast.In(),
        }
        left = self.constant_handler(left, var_d)
        right = self.constant_handler(right, var_d)
        return ast.Compare(left, [op_map[op]], [right])

    def if_handler(self, statement, var_d, else_block, outer_code):
        printd('IF')
        cond = self.constant_handler(statement[1], var_d)
        if_block = statement[3]
        index = 0
        while index < len(else_block):
            statement = else_block[index]
            op, var = statement[0], statement[3]
            if var and var.startswith(TEMP):
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
        outer_code.extend(self.convert(self.tac.get(goto_block, []), var_d))

    def while_handler(self, statement, var_d, outer_code):
        printd('WHILE')
        cond = self.constant_handler(statement[1], var_d)
        block = statement[3]
        body = self.convert(self.tac[block], var_d.copy())

        outer_code.append(ast.While(cond, body, []))
        goto_block = self.tac[block][-1][3]
        # add goto code to outer code
        outer_code.extend(self.convert(self.tac.get(goto_block, []), var_d))

    def for_handler(self, statement, var_d, outer_code):
        printd('FOR')
        var, iterator, block = statement[1:]
        iterator = self.constant_handler(iterator, var_d)
        var_d[var] = var
        var = ast.Name(var, ast.Store())
        body = self.convert(self.tac[block], var_d.copy())
        outer_code.append(ast.For(var, iterator, body, [], lineno=self.lineno))
        goto_block = self.tac[block][-1][3]
        # add goto code to outer code
        outer_code.extend(self.convert(self.tac.get(goto_block, []), var_d))

    def function_hander(self, statement, var_d, outer_code):
        printd("FUNC")
        func_block = statement[3]
        func_code = self.tac.get(func_block, [])
        params = []
        index = 0
        while index < len(func_code):
            statement = func_code[index]
            if statement[0] != 'ADD-PARAM':
                break
            param = statement[3]
            params.append(ast.arg(param))
            var_d[param] = param
            index += 1
        printd(func_code[index:])
        func_code = self.convert(func_code[index:], var_d)
        param_lst = ast.arguments([], params, [], [], [], [], [])
        node = ast.FunctionDef(func_block, param_lst, func_code, decorator_list=[], lineno=self.lineno)
        outer_code.append(node)

    def list_handler(self, statement, var_d, index, statements):
        lst = []
        while index < len(statements):
            if statements[index][0] != 'PUSH-ELMT':
                index += 1
                break
            element = self.constant_handler(statements[index][3], var_d)
            lst.append(element)
            index += 1
        var = statement[3]
        var_d[var] = ast.List(lst)
        return var_d[var], index

    def get_ast(self):
        body = self.convert()
        return ast.Module(body, [])


if __name__ == '__main__':
    visitor = ASTVisitor()
    infile = open('test_input.py')
    parser = PythonParser()
    parser.build()
    tree = parser.get_ast(infile.read())


    printd(ast.dump(tree, indent=4))
    visitor.visit(tree)
    print(visitor.tac)

    converter = TACConverter(visitor.tac)
    wrap = converter.get_ast()
   
    printd(ast.dump(wrap, indent=4))
    print(f'Code:\n{ast.unparse(wrap)}')
