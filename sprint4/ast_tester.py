import ast

from flatline import Flatliner

TO_TEST = """
a = 1 + 2
b = 3 + 4
c = a + b
"""

ast_rep = ast.parse(TO_TEST)
print(ast.dump(ast_rep, indent=4))
print('-----')
print(ast.unparse(ast_rep))
print('-----')
flattener = Flatliner()
flattener.ast = ast_rep
flattened = flattener.unparse()
print(flattened)
print('===== lambda output =====')
exec(flattened)
print('===== original output =====')
exec(TO_TEST)
