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
        ("left", "EQ", "GREATER", "LESSER", "NEQ", "GREATEREQ", "LESSEREQ",),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
    )

    ################################
    ## Statements
    ################################
    # def p_block(self, p):
    #     """
    #     block : INDENT stmt_lst DEDENT
    #     """
    #     print("block")
    #     p[0] = p[2]

    def p_statements_or_empty(self, p):
        """
        stmts_or_empty : stmt_lst
                       | empty
        """
        print("statements or empty")
        p[0] = p[1]

    def p_statement_list(self, p):
        """
        stmt_lst : stmt_lst stmt
                 | stmt
        """
        print("statement list")
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """
        stmt : assign_stmt
             | if_stmt
             | while_stmt
             | for_stmt
        """
        print("statement")
        p[0] = p[1]

    def p_for_stmt(self, p):
        """
        for_stmt : FOR ID IN expr COLON NEWLINE INDENT stmt_lst DEDENT
        """
        print("For")
        p[2] = ast.Name(p[2], ast.Store())
        p[0] = ast.For(p[2], p[4], p[8], [], lineno=p.lineno)

    def p_while_stmt(self, p):
        """
        while_stmt : WHILE expr COLON NEWLINE INDENT stmt_lst DEDENT
        """
        p[0] = ast.While(p[2], [p[6]], [])

    def p_if_statement(self, p):
        """
        if_stmt : IF expr COLON NEWLINE INDENT stmt_lst DEDENT
                | IF expr COLON NEWLINE INDENT stmt_lst DEDENT elif_stmt
                | IF expr COLON NEWLINE INDENT stmt_lst DEDENT else_stmt
        """
        print("if statement")
        if len(p) == 9:
            p[0] = ast.If(p[2], [p[6]], [p[8]])
        else:
            p[0] = ast.If(p[2], [p[6]], [])

    def p_elif(self, p):
        """
        elif_stmt : ELIF expr COLON NEWLINE INDENT stmt_lst DEDENT elif_stmt
                  | ELIF expr COLON NEWLINE INDENT stmt_lst DEDENT else_stmt
                  | ELIF expr COLON NEWLINE INDENT stmt_lst DEDENT
        """
        print("or else")
        if len(p) == 9:
            p[0] = ast.If(p[2], [p[6]], [p[8]])
        else:
            p[0] = ast.If(p[2], [p[6]], [])

    def p_else(self, p):
        """
        else_stmt : ELSE COLON NEWLINE INDENT stmt_lst DEDENT
        """
        print("or else")
        p[0] = p[5]

    def p_assignment_statement(self, p):
        """
        assign_stmt :  ID ASSIGN expr NEWLINE
        """
        print("assign")
        p[0] = ast.Assign([ast.Name(p[1], ast.Store())], p[3], lineno=p.lineno)

    ################################
    ## Expressions
    ################################
    def p_expr_boolop(self, p):
        """
        expr : expr OR expr
             | expr AND expr
        """
        print("bool op")
        op_map = {
            'and': ast.And(),
            'or': ast.Or(),
        }
        p[0] = ast.BoolOp(op_map[p[2]], [p[1], p[3]])

    def p_expr_compare(self, p):
        """
        expr : expr GREATER expr
             | expr LESSER expr
             | expr GREATEREQ expr
             | expr LESSEREQ expr
             | expr EQ expr
             | expr NEQ expr
             | expr IN expr
        """
        print("compare op")
        op_map = {
            '>': ast.Gt(),
            '<': ast.Lt(),
            '>=': ast.GtE(),
            '<=': ast.LtE(),
            '==': ast.Eq(),
            '!=': ast.NotEq(),
            'in': ast.In(),
        }
        p[0] = ast.Compare(p[1], [op_map[p[2]]], [p[3]])

    def p_expr_binops(self, p):
        """
        expr : expr PLUS expr
             | expr MINUS expr
             | expr TIMES expr
             | expr DIVIDE expr
        """
        print("binary op")
        op_map = {
            '+': ast.Add(),
            '-': ast.Sub(),
            '*': ast.Mult(),
            '/': ast.Div(),
        }
        p[0] = ast.BinOp(p[1], op_map[p[2]], p[3])

    def p_expr_number(self, p):
        """
        expr : NUMBER
        """
        print("number")
        p[0] = ast.Constant(p[1], 'int')

    def p_expr_bool(self, p):
        """
        expr : BOOLEAN
        """
        print('bool')
        p[0] = ast.Constant(p[1], 'bool')

    def p_expr_float(self, p):
        """
        expr : FLOAT
        """
        print("float")
        p[0] = ast.Constant(p[1], 'float')

    def p_expr_string(self, p):
        """
        expr : STRING
        """
        print("string")
        p[0] = ast.Constant(p[1], 'str')

    def p_expr_id(self, p):
        """
        expr : ID
        """
        p[0] = ast.Name(p[1], ast.Load())

    ################################
    ## if statements
    ################################

    # def p_logic_if(self, p):
    #     """
    #
    #     """

    ################################
    ## Misc
    ################################

    # This can be used to handle the empty production, by using 'empty'
    # as a symbol. For example:
    #
    #       optitem : item
    #               | empty
    def p_empty(self, p):
        """empty :"""
        pass

    def p_error(self, p):
        if p:
            print("Syntax error at token", repr(p.value), p)
        else:
            print("None type:", p)

    def build(self, **kwargs):
        self.tokens = tokens
        self.lexer = PythonLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)

    def get_ast(self, data):
        """
        returns the ast representation of <data>
        """
        return ast.Module(self.parser.parse(data, tokenfunc=self.lexer.get_token_external), [])

    def test(self, data):
        result = self.get_ast(data)
        try:
            print(result)
            print(ast.dump(result, indent=4))
            print(ast.unparse(result))
        except Exception as e:
            print("Something went wrong lmao 😂")
            print(e)
            raise
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
