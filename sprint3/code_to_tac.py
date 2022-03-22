import ast

from python_parser import PythonParser


class ASTVisitor(ast.NodeVisitor):
    """ example recursive visitor """

    # def recursive(func):
    #     """ decorator to make visitor work recursive """
    #     def wrapper(self,node):
    #         func(self,node)
    #         for child in ast.iter_child_nodes(node):
    #             self.visit(child)
    #     return wrapper

    def __init__(self, use_smallest_name = False):
        super().__init__()
        self.tac = {"main": []}
        self.key = "main"
        self.L = 0
        self.exitL = None
        self.previousL = []  # anytime we go into a scope, add to this and
        self.var_count = 0
        self.mapping = {}
        self.use_smallest_name = use_smallest_name


    def fresh_variable(self):
        var = f't_{self.var_count}'
        self.var_count += 1
        return var

    def addToTac(self, value):
        if self.key in self.tac:
            self.tac[self.key].append(value)
        else:
            self.tac[self.key] = [value]

    def getL(self):
        self.L += 1
        return self.L - 1

    def visit_Assign(self, node):
        """ visit a Assign node and visits it recursively"""
        visitedNode = self.visit(node.value)
        s = f'{node.targets[0].id} = '  # assuming there's one target, I'm not supporting more
        s += f'{visitedNode}'

        self.addToTac(('=', visitedNode, None, node.targets[0].id))

    def visit_Name(self, node):
        """ visit a Name node and visits it recursively"""
        return node.id

    def visit_BinOp(self, node):
        """ visit a BinOp node and visits it recursively"""
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.Mod: '%'
        }
        left = self.visit(node.left)
        right = self.visit(node.right)
        operator = op_map[type(node.op)]
        var = self.fresh_variable()
        self.addToTac((operator, left, right, var))
        return var

    def visit_BoolOp(self, node):
        s = []
        op_map = {
            ast.And: 'AND',
            ast.Or: 'OR'
        }
        for curNode in node.values:
            s.append(self.visit(curNode))

        operator = op_map[type(node.op)]
        var = self.fresh_variable()
        self.addToTac((operator, s[0], s[1], var))
        return var

    def visit_Compare(self, node):
        """ visit a Compare node and visits it recursively"""
        op_map = {
            ast.Gt: '>',
            ast.Lt: '<',
            ast.GtE: '>=',
            ast.LtE: '<=',
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.In: 'in',
        }
        left = self.visit(node.left)  # make new var if required
        curOpList = node.ops
        curCompList = node.comparators
        while len(curOpList) > 1:
            curOp = curOpList[0]
            operator = op_map[type(curOp)]

            curComp = self.visit(curCompList[0])
            curComp2 = self.visit(curCompList[1])
            var = self.fresh_variable()
            self.addToTac((operator, curComp, curComp2, var))
            curOpList = curOpList[1:]
            curCompList = [var] + curCompList[3:]

            # temp variables
        var = self.fresh_variable()
        operator = op_map[type(curOpList[0])]
        right = curCompList[0]
        if (type(right) != str):
            right = self.visit(right)
        self.addToTac((operator, left, right, var))
        return var

    def visit_Lambda(self, node):
        """ visit a Function node """
        print(type(node).__name__)

    def visit_Break(self, node):
        self.addToTac(("BREAK", None, None, None))

    def visit_Continue(self, node):
        self.addToTac(("CONTINUE", None, None, None))

    def visit_FunctionDef(self, node):
        """ visit a Function node and visits it recursively"""
        self.addToTac(('DEFN', None, None, node.name))
        oldKey = self.key
        self.key = node.name

        cur_end_segment  = None
        for arg in node.args.args:
            self.addToTac(("ADD-PARAM", None, None, arg.arg))
        for stmt in node.body:
            if type(stmt) in [ast.If, ast.While, ast.For]:
                cur_end_segment = f'_L{self.getL()}'

            self.visit(stmt, end_segment=cur_end_segment)

            if type(stmt) in [ast.If, ast.While, ast.For]:
                self.key = cur_end_segment
        self.key = oldKey

    def visit_Constant(self, node):
        """ visit a Module node and the visits recursively"""
        return node.value

    def visit_List(self, node):
        """ visit a List node"""
        var = self.fresh_variable()
        self.addToTac(("START-LIST",None,None,var))
        for element in node.elts:
            self.addToTac(("PUSH-ELMT", None, None, self.visit(element)))
        self.addToTac(("END-LIST",None,None,var))
        return var

    def visit_If(self, node, end_segment=None, go_to_end_segment = True):
        """ Visit an If node and the visits recursively"""
        # two paths to consider, if it satisfies or if it doesnt
        curNode = node
        ifStatements = []
        while type(curNode) == ast.If:
            ifStatements.append((curNode, self.getL()))
            if len(curNode.orelse) >= 1:
                curNode = curNode.orelse[0]
            else:
                curNode = None
                break

        for ifstmt, L in ifStatements:
            tempVar = self.visit(ifstmt.test)
            self.addToTac(('IF', tempVar, None, f'_L{L}'))

        if curNode != None:
            for val in curNode:
                self.visit(val, end_segment=end_segment if go_to_end_segment else None, go_to_end_segment=False)

        if go_to_end_segment and end_segment:
            self.addToTac(('GOTO', None, None, end_segment if go_to_end_segment else None))

        # visit each if else block
        keys = []

        for ifStmt, L in ifStatements:
            self.key = f'_L{L}'
            for body in ifStmt.body:
                i = 0
                self.key = f'_L{L}'
                while i < len(body):
                    element = body[i]
                    if type(element) in [ast.For,ast.If,ast.While] and i < len(body) - 1:
                        new_segment = f'_L{self.getL()}'
                        self.visit(element, end_segment=(new_segment if go_to_end_segment else None), go_to_end_segment = go_to_end_segment)
                        self.key = new_segment
                    else:
                        self.visit(element,end_segment=(end_segment if go_to_end_segment else None), go_to_end_segment = False)
                    i += 1
            self.key = f'_L{L}'
            keys.append(f'_L{L}')
        
        if go_to_end_segment and end_segment:
            for key in keys[:-1]:
                self.tac[key].append(('GOTO', None, None, end_segment))

    def visit_While(self, node, end_segment=None, go_to_end_segment = True):
        tempVar = self.visit(node.test)

        new_L = self.getL()
        self.addToTac(("WHILE", tempVar, None, f'_L{new_L}'))
        #self.addToTac(("GOTO-3", None, None, end_segment if go_to_end_segment else None))
        self.key = f'_L{new_L}'

        i = 0
        while i < len(node.body[0]):
            expr = node.body[0][i]
            if type(expr) in [ast.For,ast.If,ast.While] and i < len(node.body[0]) - 1:
                new_segment = f'_L{self.getL()}'

                self.visit(expr, end_segment=(new_segment if go_to_end_segment else None), go_to_end_segment = True)
                self.key = new_segment
            else:
                self.visit(expr,end_segment=(end_segment if go_to_end_segment else None), go_to_end_segment = False)
            i += 1
        # tempVar = self.visit(node.test, end_segment=end_segment)
        # self.addToTac(("IFZ",tempVar,None, f'_L{new_L}'))
        self.key = f'_L{new_L}' 
        if go_to_end_segment and end_segment:
            self.addToTac(("GOTO", None, None, end_segment))

    def visit_Slice(self, node):
        lower = self.visit(node.lower) if node.lower else None 
        upper = self.visit(node.upper) if node.upper else None 
        step = self.visit(node.step) if node.step else None  

        self.addToTac(("SLICE",lower,upper,step))

    def visit_Subscript(self, node):
        var = self.visit(node.value)
        temp = self.fresh_variable()
        if type(node.slice) == ast.Slice:
            self.addToTac(('SLICE',var,None,temp))
            self.visit(node.slice)
        else:
            self.addToTac(('INDEX',var,None,temp))
            self.addToTac(("INDEX", var, self.visit(node.slice), None))
        return temp

    def visit_For(self, node, end_segment=None, go_to_end_segment = True):
        identifier = self.visit(node.target)
        iterates = self.visit(node.iter)

        jumpL = self.getL()
        self.addToTac(('FOR', identifier, iterates, f'_L{jumpL}'))
        #self.addToTac(("GOTO-5", None, None, end_segment))
        self.key = f'_L{jumpL}'

        i = 0
        while i < len(node.body):
            body = node.body[i]
            if type(body) in [ast.For,ast.If,ast.While] and i < len(node.body) - 1:
                new_segment = f'_L{self.getL()}'
                self.visit(body, end_segment=new_segment if go_to_end_segment else None, go_to_end_segment = True)
                self.key = new_segment
            else:
                self.visit(body,end_segment=end_segment if go_to_end_segment else None, go_to_end_segment = False)
            i += 1
        self.key = f'_L{jumpL}'       
        if go_to_end_segment:   
            self.addToTac(("GOTO", None, None, end_segment))

    def visit_Return(self, node):
        tempVar = self.visit(node.value)
        self.addToTac(("RETURN", None, None, tempVar))

    def visit_Assert(self, node):
        var1 = self.visit(node.test)
        var2 = None 
        if (node.msg):
            var2 = self.visit(node.msg)
        self.addToTac(("ASSERT", None, var2, var1))

    def visit_Call(self, node):
        temp = self.fresh_variable()
        for arg in node.args:
            tempVar = self.visit(arg)
            self.addToTac(("PUSH-PARAM", None, None, tempVar))
        if type(node.func) == ast.Attribute:
            objectName = self.visit(node.func.value)
            methodName = node.func.attr
            self.addToTac(("CALL",objectName, len(node.args), methodName))
        else:
            self.addToTac(("CALL", None, len(node.args), self.visit(node.func)))

        self.addToTac(("=",None, "ret", temp))
        return temp

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Module(self, node, go_to_end_segment = True):
        """ visit a Module node and the visits recursively"""
        for child in ast.iter_child_nodes(node):
            if type(child) in [ast.If, ast.While, ast.For]:
                # New flows added
                end_segment = f'_L{self.getL()}'
                self.visit(child, end_segment=end_segment,go_to_end_segment = go_to_end_segment)
                self.key = end_segment
            else:
                self.visit(child)

    def visit(self, node, end_segment=None, go_to_end_segment = True):
        op_map = {
            ast.If: self.visit_If,
            ast.While: self.visit_While,
            ast.For: self.visit_For
        }
        if end_segment and type(node) in op_map:
            return op_map[type(node)](node, end_segment=end_segment, go_to_end_segment = go_to_end_segment)
        else:
            return super().visit(node)

    def generic_visit(self, node):
        print('here')
        print(node)
        pass


if __name__ == '__main__':
    visitor = ASTVisitor()
    infile = open('test_input.py')
    parser = PythonParser()
    parser.build()
    tree = parser.get_ast(infile.read())
    visitor.visit(tree)
    print(visitor.tac)
