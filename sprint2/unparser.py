import ast

from python_parser import PythonParser


def construct_lambda(vals: dict[str, str], body: str = '{}') -> str:
    """
    Returns a lambda function string with the arguments provided.
    >>> construct_lambda({'a': '1', 'b': '2'})
    '(lambda a, b: {})(1, 2)'
    >>> exec(construct_lambda({'a': '1', 'b': '2'}, 'print(a + b)'))
    3
    """
    return f'(lambda {", ".join(vals.keys())}: {body})({", ".join(vals.values())})'


def provide_imports(imports: list[str], body: str) -> str:
    """
    Provides imports to our one lined program.
    """
    return construct_lambda({k: f"__import__('{k}')" for k in imports}, body) if imports else body


def wrap_globals(body: str):
    """
    Wraps a lambda body with the globals dict.
    >>> wrap_globals('print(a)')
    '(lambda __g: print(a))(globals())'
    """
    return construct_lambda({'__g': 'globals()'}, body)


class Unparser:
    def __init__(self):
        self.ast = None
        self.imports = []
        self.node_handlers = {
            ast.Assign: self.handle_assign,
            ast.Constant: self.handle_constant,
            ast.Expr: self.handle_expr,
            ast.Call: self.handle_call,
            ast.Name: self.handle_name,
            ast.List: self.handle_list,
            ast.Tuple: self.handle_tuple,
            ast.Attribute: self.handle_attribute,
            ast.BinOp: self.handle_binop,
            ast.If: self.handle_if,
            list: self.unparse_list,
            ast.Compare: self.handle_compare,
            ast.BoolOp: self.handle_boolop,
            ast.UnaryOp: self.handle_unaryop,
            ast.FunctionDef: self.handle_functiondef,
            ast.Return: self.handle_return,
            ast.Import: self.handle_import,
        }

    def set_ast(self, infile: str, read_from_file: bool = False):
        """
        Turns the infile into an AST and sets the instance attribute accordingly.
        """
        parser = PythonParser()
        parser.build()
        if read_from_file:
            with open(infile, 'r') as f:
                self.ast = parser.get_ast(f.read())
        else:
            self.ast = parser.get_ast(infile)

    def apply_handler(self, node, cont=None):
        return self.node_handlers.get(type(node), self.handle_error)(node, cont)

    def handle_constant(self, node, cont) -> str:
        return repr(node.value)

    def handle_name(self, node, cont) -> str:
        return node.id

    def handle_list(self, node, cont) -> str:
        return f'[{", ".join(self.apply_handler(child) for child in node.elts)}]'

    def handle_tuple(self, node, cont) -> str:
        return f'({", ".join(self.apply_handler(child) for child in node.elts)})'

    def handle_attribute(self, node, cont) -> str:
        return f'{self.apply_handler(node.value)}.{node.attr}'

    def handle_assign(self, node, cont) -> str:
        var_name = node.targets[0].id
        return construct_lambda({var_name: self.apply_handler(node.value)}, cont)

    def handle_expr(self, node, cont) -> str:
        return self.apply_handler(node.value, cont)

    def handle_call(self, node, cont) -> str:
        if not cont:
            return f'{self.apply_handler(node.func)}({", ".join(self.apply_handler(child) for child in node.args)})'
        return f'[{self.apply_handler(node.func)}({", ".join(self.apply_handler(child) for child in node.args)}), {cont}][-1]'

    def handle_binop(self, node, cont) -> str:
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
        }
        return f'{self.apply_handler(node.left)} {op_map[type(node.op)]} {self.apply_handler(node.right)}'

    def handle_boolop(self, node, cont) -> str:
        op_map = {
            ast.And: 'and',
            ast.Or: 'or',
        }
        return f' {op_map[type(node.op)]} '.join(self.apply_handler(child) for child in node.values)

    def handle_unaryop(self, node, cont) -> str:
        op_map = {
            ast.UAdd: '+',
            ast.USub: '-',
            ast.Not: 'not ',
            ast.Invert: '~',
        }
        return f'{op_map[type(node.op)]}{self.apply_handler(node.operand)}'

    def handle_if(self, node, cont) -> str:
        return f'{self.apply_handler(node.body, cont)} if {self.apply_handler(node.test)} else {self.apply_handler(node.orelse, cont)}'

    def handle_compare(self, node, cont) -> str:
        op_map = {
            ast.Gt: '>',
            ast.Lt: '<',
            ast.GtE: '>=',
            ast.LtE: '<=',
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.In: 'in',
        }
        return f'{self.apply_handler(node.left)} {op_map[type(node.ops[0])]} {self.apply_handler(node.comparators[0])}'

    def handle_functiondef(self, node, cont) -> str:
        args = ', '.join(arg.arg for arg in node.args.args)
        return construct_lambda({node.name: f'lambda{" " if args else ""}{args}: {self.unparse_list(node.body)}'}, cont)

    def handle_return(self, node, cont) -> str:
        return self.apply_handler(node.value)

    def handle_import(self, node, cont) -> str:
        self.imports.extend(a.name for a in node.names)
        return cont

    def handle_error(self, node, cont) -> None:
        raise ValueError(f'Handler not found for {node}')

    def unparse_list(self, body: list, cont=None) -> str:
        temp = cont
        for node in body[::-1]:
            temp = self.apply_handler(node, temp)
        return temp

    def unparse(self, root=None) -> str:
        """
        Unparses the ast.
        """
        self.imports.clear()
        curr = root if root else self.ast
        if hasattr(curr, 'body') and isinstance(curr.body, list):
            body = self.unparse_list(curr.body)
            return provide_imports(self.imports, body)
        return 'Unparse unsuccessful.'


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    test = Unparser()
    test.set_ast('test_input.py', True)
    print(ast.dump(test.ast, indent=4))
    result = test.unparse()
    print(result)
