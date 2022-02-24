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
        self.node_handlers = {
            ast.Assign: self.handle_assign,
            ast.Constant: self.handle_constant,
            ast.Expr: self.handle_expr,
            ast.Call: self.handle_call,
            ast.Name: self.handle_name,
            ast.BinOp: self.handle_binop,
        }

    def set_ast(self, infile: str):
        """
        Turns the infile into an AST and sets the instance attribute accordingly.
        """
        with open(infile, 'r') as f:
            parser = PythonParser()
            parser.build()
            self.ast = parser.get_ast(f.read())

    def apply_handler(self, node, inner=None):
        return self.node_handlers.get(type(node), self.handle_error)(node, inner)

    def handle_constant(self, node, inner) -> str:
        return f"{node.value}"

    def handle_name(self, node, inner) -> str:
        return node.id

    def handle_assign(self, node, inner) -> str:
        var_name = node.targets[0].id
        return construct_lambda({var_name: self.apply_handler(node.value)}, inner)

    def handle_expr(self, node, inner) -> str:
        return self.apply_handler(node.value)

    def handle_call(self, node, inner) -> str:
        return f'{self.apply_handler(node.func)}({", ".join(self.apply_handler(child) for child in node.args)})'

    def handle_binop(self, node, inner) -> str:
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
        }
        return f'{self.apply_handler(node.left)} {op_map[type(node.op)]} {self.apply_handler(node.right)}'

    def handle_error(self, node, inner) -> None:
        raise ValueError(f'Handler not found for {node}')

    def unparse(self, root=None) -> str:
        """
        Unparses the ast.
        """
        curr = root if root else self.ast
        if hasattr(curr, 'body') and isinstance(curr.body, list):
            temp = None
            for node in curr.body[::-1]:
                temp = self.apply_handler(node, temp)
            return temp
        return 'Unparse unsuccessful.'


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    test = Unparser()
    test.set_ast('test_input.py')
    print(ast.dump(test.ast, indent=4))
    result = test.unparse()
    print(result)
