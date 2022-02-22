import ast

from python_parser import PythonParser


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

    def unparse(self):
        """
        Unparses the ast.
        """
        if self.ast is not None:
            print(ast.dump(self.ast, indent=4))


if __name__ == '__main__':
    test = Unparser()
    test.set_ast('test_input.py')
    test.unparse()
