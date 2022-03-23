### Visitor ###
class NodeVisitor(object):
    """
    A base NodeVisitor class for visiting MiniJava nodes.
    Define your own visit_X methods to, where X is the class
    name you want to visit with these methods.
    Refer to visit_Program, for example
    """

    def visit(self, node, offset=0):
        """
        Your compiler can call this method to traverse through your AST
        """
        method = 'visit_' + node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node, offset)

    def generic_visit(self, node, offset=0):
        """
        Default visit method that simply prints out given node's attributes,
        then traverses through its children. This is called if no explicit
        visitor function exists for a node.
        NOTE: A method within Node object with similar behaviour might be
              useful when debugging your project
        """
        lead = ' ' * offset
        output = lead + node.__class__.__name__ + ': '
        if node.attr_names:
            vlist = [getattr(node, n) for n in node.attr_names]
            output += ', '.join('%s' % v for v in vlist)
        print(output)
        for (child_name, child) in node.children():
            self.visit(child, offset=offset + 2)

    def visit_Program(self, node, offset=0):
        """
        Custom visit method for "Program" node
        """
        print("====== PROGRAM START ======")
        self.visit(node.main_class, offset=2)
        self.visit(node.class_decl, offset=2)
        print("====== PROGRAM END ======")


### Nodes ###

class Node(object):
    """
    Abstract base class for AST nodes
    Things to implement:
        __init__: Initialize attributes / children
        children: Method to return list of children. Alternatively, you can
                  look into __iter__ method, which allow nodes to be
                  iterable.
    """

    def children(self):
        """
        A sequence of all children that are Nodes
        """
        pass

    # Set of attributes for a given node
    attr_names = ()


# top most
class Program(Node):
    def __init__(self, main_class, class_decl, coord=None):
        self.main_class = main_class
        self.class_decl = class_decl

    def children(self):
        nodelist = []
        # TODO: this will be changed
        if self.main_class is not None:
            nodelist.append(('main_class', self.main_class))
        if self.class_decl is not None:
            nodelist.append(('class_decl', self.class_decl))
        return tuple(nodelist)

    attr_names = ()


# Strings, Numbers
class Constant(Node):
    def __init__(self, type, value, coord=None):
        self.type = type
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('type', 'value',)


class AssignStmt(Node):
    def __init__(self, name, expr, coord=None):
        self.name = name
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)

    attr_names = ('name',)


# Covers math and boolean operators
class BinOp(Node):
    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord

    def children(self):
        nodelist = []
        if self.left is not None:
            nodelist.append(('left', self.left))
        if self.right is not None:
            nodelist.append(('right', self.right))
        return tuple(nodelist)

    attr_names = ('op',)


class IfStmt(Node):
    def __init__(self, cond, true_body, false_body, coord=None):
        self.cond = cond
        self.true_body = true_body
        self.false_body = false_body

    def children(self):
        nodelist = []
        if self.cond is not None:
            nodelist.append(('cond', self.cond))
        if self.true_body is not None:
            nodelist.append(('true_body', self.true_body))
        if self.false_body is not None:
            nodelist.append(('false_body', self.false_body))
        return tuple(nodelist)

    attr_names = ()


class FunctionDecl(Node):
    def __init__(self, name, params, body, coord=None):
        self.name = name
        self.params = params
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.body is not None:
            nodelist.append(('body', self.body))
        if self.params is not None:
            nodelist.append(('params', self.params))
        return tuple(nodelist)

    attr_names = ('name',)


class ParamList(Node):
    def __init__(self, params, coord=None):
        self.params = params
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.params or []):
            nodelist.append(('params[%d]' % i, child))
        return tuple(nodelist)

    attr_names = ()


class RetStmt(Node):
    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)

    attr_names = ()


# TODO: figure out why we need this?
class StmtList(Node):
    def __init__(self, stmt_lst, coord=None):
        self.stmt_lst = stmt_lst

    def children(self):
        nodelist = []
        for i, stmt in enumerate(self.stmt_lst or []):
            nodelist.append(('stmt[%d]' % i, stmt))
        return nodelist

    attr_names = ()


class UnaryOp(Node):
    def __init__(self, op, expr, coord=None):
        self.op = op
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(('expr', self.expr))
        return tuple(nodelist)

    attr_names = ('op',)


class WhileStmt(Node):
    def __init__(self, cond, body, coord=None):
        self.cond = cond
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None:
            nodelist.append(('cond', self.cond))
        if self.body is not None:
            nodelist.append(('body', self.body))
        return tuple(nodelist)

    attr_names = ()


class ForStmt(Node):
    def __init__(self, iterator, body, coord=None):
        self.iter = iterator
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.iter is not None:
            nodelist.append(('iter', self.iter))
        if self.body is not None:
            nodelist.append(('body', self.body))
        return tuple(nodelist)

    attr_names = ()


class RangeNode(Node):
    def __init__(self, start, stop, step, coord=None):
        self.start = start
        self.stop = stop
        self.step = step
        self.coord = coord

    def children(self):
        nodelist = []
        if self.start is not None:
            nodelist.append(('start', self.start))
        if self.stop is not None:
            nodelist.append(('stop', self.stop))
        if self.step is not None:
            nodelist.append(('step', self.step))
        return tuple(nodelist)

    attr_names = ()
