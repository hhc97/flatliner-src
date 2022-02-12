#!/usr/bin/env python3

import argparse
import ast

from ply import yacc

from lexer import PythonLexer
# Get the token map from the lexer. This is required.
from lexer import tokens


class PythonParser:
    """
    MiniJavaParser follows similar language defined in MiniJava.cup file
    (available on Quercus). There are slight differences, such as no hard
    coded print statement, but this should give basic understanding
    of how you can use PLY yacc to parse more standard language.

    Note that current grammar rule is pretty rigid:
        - Main class can only contain main method, nothing else
        - Program can contain one or no additional class
        - There can only be one class variable
        - There can only be one method for class

    As an exercise, you could try to extend this parser such that all of
    these issues are addressed.
    """

    precedence = (
        ('left', 'AND'),
        ('left', 'EQOP', 'NEQ'),
        ('left', 'LESS', 'LESSEQ', 'GREATER', 'GREATEREQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UNARY')
    )

    # Let the parser know that symbol "program" is the starting point
    start = 'program'

    ################################
    ## Program (starting point)
    ################################

    def p_program(self, p):
        """
        program : main_class_decl class_decl_or_empty
        """
        p[0] = ast.Program(p[1], p[2])

    ################################
    ## Main Method / Class
    ################################

    def p_main_class_decl(self, p):
        """
        main_class_decl : CLASS ID LBRACE main_method_decl RBRACE
        """
        p[0] = ast.ClassDecl(p[2], None, None, p[4])

    def p_main_method_decl(self, p):
        """
        main_method_decl : PUBLIC STATIC VOID MAIN main_method_param scope
        """
        void_type = ast.Type("void", "void")
        p[0] = ast.MethodDecl("main", void_type, p[5], p[6])

    def p_main_method_param(self, p):
        """
        main_method_param : LPAREN STRING LBRACK RBRACK ID RPAREN
        """
        p[0] = ast.ParamList([])

    ################################
    ## Class Declarations
    ################################

    def p_class_decl_or_empty(self, p):
        """
        class_decl_or_empty : class_decl
                            | empty
        """
        p[0] = p[1]

    def p_class_decl(self, p):
        """
        class_decl : CLASS ID ext_or_empty LBRACE class_var_decl_or_empty method_decl_or_empty RBRACE
        """
        p[0] = ast.ClassDecl(p[2], p[3], p[5], p[6])

    def p_extend_or_empty(self, p):
        """
        ext_or_empty : extends
                     | empty
        """
        p[0] = p[1]

    def p_extend(self, p):
        """
        extends : EXTENDS ID
        """
        p[0] = ast.Extend(p[2])

    def p_class_var_decl_or_empty(self, p):
        """
        class_var_decl_or_empty : class_var_decl
                                | empty
        """
        p[0] = p[1]

    def p_class_var_decl(self, p):
        """
        class_var_decl : type ID SEMICOL
        """
        p[0] = ast.DeclStmt(p[2], p[1])

    ################################
    ## Method Declarations
    ################################

    def p_method_decl_or_empty(self, p):
        """
        method_decl_or_empty : method_decl
                             | empty
        """
        p[0] = p[1]

    def p_method_decl(self, p):
        """
        method_decl : PUBLIC type ID method_param LBRACE stmts_or_empty ret_stmt RBRACE
        """
        p[0] = ast.MethodDecl(p[3], p[2], p[4], p[6])

    ################################
    ## Formals / Parameters
    ################################

    def p_method_param(self, p):
        """
        method_param : LPAREN formals_or_empty RPAREN
        """
        p[0] = ast.ParamList(p[2])

    def p_formals_or_empty(self, p):
        """
        formals_or_empty : formal_lst
                         | empty
        """
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]

    def p_formal_lst(self, p):
        """
        formal_lst : formal_lst COMMA formal
                   | formal
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_formal(self, p):
        """
        formal : type ID
        """
        p[0] = ast.Formal(p[2], p[1])

    ################################
    ## Statements
    ################################

    def p_scope(self, p):
        """
        scope : LBRACE stmts_or_empty RBRACE
        """
        p[0] = p[2]

    def p_statements_or_empty(self, p):
        """
        stmts_or_empty : stmt_lst
                       | empty
        """
        p[0] = ast.StmtList(p[1])

    def p_statement_list(self, p):
        """
        stmt_lst : stmt_lst stmt
                 | stmt
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """
        stmt : decl_stmt
             | assign_stmt
             | if_stmt
             | while_stmt
        """
        p[0] = p[1]

    def p_decl_statement(self, p):
        """
        decl_stmt : type ID EQ expr SEMICOL
        """
        p[0] = ast.DeclStmt(p[2], p[1], p[4])

    def p_assignment_statement(self, p):
        """
        assign_stmt : ID EQ expr SEMICOL
        """
        p[0] = ast.AssignStmt(p[1], p[3])

    def p_if_statement(self, p):
        """
        if_stmt : IF LPAREN expr RPAREN scope ELSE scope
        """
        p[0] = ast.IfStmt(p[3], p[5], p[7])

    def p_while_statement(self, p):
        """
        while_stmt : WHILE LPAREN expr RPAREN scope
        """
        p[0] = ast.WhileStmt(p[3], p[5])

    def p_return_statement(self, p):
        """
        ret_stmt : RETURN expr SEMICOL
        """
        p[0] = ast.RetStmt(self, p[2])

    ################################
    ## Expressions
    ################################

    def p_expr_object_instance(self, p):
        """
        expr : NEW ID LPAREN RPAREN
        """
        p[0] = ast.ObjInstance(p[2])

    def p_expr_binops(self, p):
        """
        expr : expr PLUS expr
             | expr MINUS expr
             | expr TIMES expr
             | expr DIVIDE expr
             | expr LESS expr
             | expr LESSEQ expr
             | expr GREATER expr
             | expr GREATEREQ expr
             | expr EQOP expr
             | expr NEQ expr
             | expr AND expr
        """
        p[0] = ast.BinOp(p[2], p[1], p[3])

    def p_expr_group(self, p):
        """
        expr : LPAREN expr RPAREN
        """
        p[0] = p[2]

    def p_expr_unary(self, p):
        """
        expr : MINUS expr %prec UNARY
             | BANG expr %prec UNARY
        """
        p[0] = ast.UnaryOp(p[1], p[2])

    def p_expr_number(self, p):
        """
        expr : NUMBER
        """
        p[0] = ast.Constant('int', p[1])

    def p_expr_bool(self, p):
        """
        expr : TRUE
             | FALSE
        """
        p[0] = ast.Constant('bool', p[1])

    def p_expr_null(self, p):
        """
        expr : NULL
        """
        p[0] = ast.Constant('null', p[1])

    def p_expr_id(self, p):
        """
        expr : ID
        """
        p[0] = ast.Constant('id', p[1])

    def p_expr_this(self, p):
        """
        expr : THIS
        """
        p[0] = ast.Constant('this', p[1])

    ################################
    ## Types
    ################################

    def p_type(self, p):
        """
        type : base_type
             | ID
        """
        p[0] = ast.Type(p[1])

    def p_base_type(self, p):
        """
        base_type : INT
                  | BOOLEAN
                  | STRING
                  | VOID
        """
        p[0] = p[1]

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
        print("Syntax error at token", p)

    def build(self, **kwargs):
        self.tokens = tokens
        self.lexer = PythonLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)

    def test(self, data):
        result = self.parser.parse(data)
        visitor = ast.NodeVisitor()
        visitor.visit(result)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Take in the miniJava source code and parses it')
    argparser.add_argument('FILE', help='Input file with miniJava source code')
    args = argparser.parse_args()

    f = open(args.FILE, 'r')
    data = f.read()
    f.close()

    m = PythonParser()
    m.build()
    m.test(data)
