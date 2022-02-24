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

    def set_ast(self, infile: str):
        """
        Turns the infile into an AST and sets the instance attribute accordingly.
        """
        with open(infile, 'r') as f:
            parser = PythonParser()
            parser.build()
            self.ast = parser.get_ast(f.read())

    def unparse(self, root=None):
        """
        Unparses the ast.
        """
        # if self.ast is not None:
        #     print(ast.dump(self.ast, indent=4))
        curr = root if root else self.ast
        print(curr)
        print(dir(curr))
        if hasattr(curr, 'body') and isinstance(curr.body, list):
            for node in curr.body:
                print('f', node)
                self.unparse(node)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    test = Unparser()
    test.set_ast('test_input.py')
    print(ast.dump(test.ast, indent=4))
    test.unparse()
