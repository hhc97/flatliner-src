import ast

TO_TEST = """
a = 1 + 2
b = 3 + 4
c = a + b
"""

ast_rep = ast.parse(TO_TEST)
print(ast.dump(ast_rep, indent=4))
print('-----')
print(ast.unparse(ast_rep))
