#!/usr/bin/env python3

import argparse
import ast

from ply import yacc

from lexer import PythonLexer
# Get the token map from the lexer. This is required.
from lexer import tokens


class PythonParser:
    """
    A parser for a small subset of the Python programming language.
    """

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
    )

    # basic operators

    def p_expr_id(self, p):
        """
        expr : NUMBER
        """
        p[0] = ast.Constant(int(p[1]))

    def p_expr_assign(self, p):
        """
        expr : ID ASSIGN expr
        """
        p[0] = ast.Assign([ast.Name(p[1], ast.Store())], p[3], lineno=self.lexer.lexer.lineno)

    def p_BinOp(self, p):
        """
        expr : expr PLUS expr
             | expr MINUS expr
             | expr TIMES expr
             | expr DIVIDE expr
        """
        op_map = {
            '+': ast.Add(),
            '-': ast.Sub(),
            '*': ast.Mult(),
            '/': ast.Div(),
        }
        p[0] = ast.BinOp(p[1], op_map[p[2]], p[3])

    ################################
    ## Misc
    ################################

    # This can be used to handle the empty production, by using 'empty'
    # as a symbol. For example:
    #
    #       optitem : item
    #               | empty
    # def p_empty(self, p):
    #     """empty :"""
    #     pass

    def p_error(self, p):
        print("Syntax error at token", p)

    def build(self, **kwargs):
        self.tokens = tokens
        self.lexer = PythonLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)

    def test(self, data):
        result = self.parser.parse(data)
        # result = ast.Module([result], [])
        print(result)
        print(ast.dump(result, indent=4))
        print(ast.unparse(result))
        visitor = ast.NodeVisitor()
        visitor.visit(result)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Take in the python source code and parses it')
    argparser.add_argument('FILE', help='Input file with python source code')
    args = argparser.parse_args()

    f = open(args.FILE, 'r')
    data = f.read()
    f.close()

    m = PythonParser()
    m.build()
    m.test(data)
