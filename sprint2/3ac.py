import ast
from python_parser import PythonParser

VAR_COUNT = 0

def fresh_variable():
    global VAR_COUNT
    var = f't_{VAR_COUNT}'
    VAR_COUNT += 1
    return var

class ASTVisitor(ast.NodeVisitor):
    """ example recursive visitor """

    # def recursive(func):
    #     """ decorator to make visitor work recursive """
    #     def wrapper(self,node):
    #         func(self,node)
    #         for child in ast.iter_child_nodes(node):
    #             self.visit(child)
    #     return wrapper

    
    def visit_Assign(self, node, new_var = False):
        """ visit a Assign node and visits it recursively"""
        s = f'{node.targets[0].id} = ' # assuming there's one target, I'm not supporting more
        s += f'{self.visit(node.value)}'
        print(s)

    
    def visit_Name(self, node, new_var = False):
        """ visit a Name node and visits it recursively"""
        return node.id


    def visit_BinOp(self, node, new_var = False):
        """ visit a BinOp node and visits it recursively"""
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
        }
        left = self.visit(node.left, new_var = True) # make new var if required
        right = self.visit(node.right, new_var = True)# make new var if required
        s = f'{left} {op_map[type(node.op)]} {right}'
        if new_var:
            var = fresh_variable()
            s = f'{var} = ' + s
            print(s)
            return var
        return s

    # TODO: figure out
    
    def visit_Call(self, node, new_var = False):
        """ visit a Call node and visits it recursively"""
        print(type(node).__name__)

    
    def visit_Lambda(self, node, new_var = False):
        """ visit a Function node """
        print(type(node).__name__)

    
    def visit_FunctionDef(self, node, new_var = False):
        """ visit a Function node and visits it recursively"""
        print(f'_{node.name}:')
        for stmt in node.body:
            self.visit(stmt)

    
    def visit_Constant(self, node, new_var = False):
        """ visit a Module node and the visits recursively"""
        return node.value
    
    def visit_If(self, node, new_var = False):
        """ Visit an If node and the visits recursively"""
        s = []
        curNode = node
        while type(curNode) == ast.If:
            s.append(curNode)
            if len(curNode.orelse) > 0:
                curNode = curNode.orelse[0]
            else:
                curNode = None
                break
        count = 0
        for ifStmt in s:
            print(f'IFZ {self.visit(ifStmt.test)} GOTO _L{count}')
            count += 1
        newCount = 0
        for ifStmt in s:
            print(f'_L{newCount}:')
            for body in ifStmt.body:
                self.visit(body[0])
            newCount += 1
            print(f'GOTO _L{count + 1}')
    
    def visit_Module(self, node, new_var = False):
        """ visit a Module node and the visits recursively"""
        for child in ast.iter_child_nodes(node):
                 self.visit(child)
                 # TODO: if it was an if statement, add an extending line 

    def visit(self, node, new_var = False):
        support_new_var = [ast.BinOp, ast.BoolOp]
        if new_var and type(node) in support_new_var:
            return self.visit_BinOp(node, new_var)
        else:
            return super().visit(node)
            

    def generic_visit(self, node, new_var = False):
        print('here')
        pass

visitor = ASTVisitor()
infile = open('test_input.py')
parser = PythonParser()
parser.build()
tree = parser.get_ast(infile.read())
visitor.visit(tree)