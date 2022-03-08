import ast


def construct_lambda(vals: dict[str, str], body: str = '{}') -> str:
    """
    Returns a lambda function string with the arguments provided.
    >>> construct_lambda({'a': '1', 'b': '2'})
    '(lambda a, b: {})(1, 2)'
    >>> exec(construct_lambda({'a': '1', 'b': '2'}, 'print(a + b)'))
    3
    """
    return f'(lambda {", ".join(vals.keys())}: {body})({", ".join(vals.values())})'


def provide_y(body: str) -> str:
    """
    provides the Y combinator.
    """
    return construct_lambda({'_Y': '(lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args))))'}, body)


def wrap_globals(body: str):
    """
    Wraps a lambda body with the globals dict.
    >>> wrap_globals('print(a)')
    '(lambda __g: print(a))(globals())'
    """
    return construct_lambda({'__g': 'globals()'}, body)


class Flatliner:
    def __init__(self):
        self.ast = None
        self.needs_y = False
        self.loop_no = 1
        self.node_handlers = {
            ast.Assign: self.handle_assign,
            ast.AugAssign: self.handle_augassign,
            ast.Constant: self.handle_constant,
            ast.Expr: self.handle_expr,
            ast.Call: self.handle_call,
            ast.Name: self.handle_name,
            ast.While: self.handle_while,
            ast.For: self.handle_for,
            ast.List: self.handle_list,
            ast.Tuple: self.handle_tuple,
            ast.Set: self.handle_set,
            ast.Dict: self.handle_dict,
            ast.Subscript: self.handle_subscript,
            ast.Slice: self.handle_slice,
            ast.Attribute: self.handle_attribute,
            ast.BinOp: self.handle_binop,
            ast.If: self.handle_if,
            list: self.unparse_list,
            ast.Compare: self.handle_compare,
            ast.BoolOp: self.handle_boolop,
            ast.UnaryOp: self.handle_unaryop,
            ast.FunctionDef: self.handle_functiondef,
            ast.ClassDef: self.handle_classdef,
            ast.Return: self.handle_return,
            ast.Import: self.handle_import,
        }

    def set_ast(self, infile: str):
        """
        Turns the infile into an AST and sets the instance attribute accordingly.
        """
        file = open(infile, 'r')
        self.ast = ast.parse(file.read())
        close = file.close()

    def apply_handler(self, node):
        node_repr = self.node_handlers.get(type(node), self.handle_error)(node, None)
        return node_repr

    def apply_handler2(self, node, cont):
        node_repr = self.node_handlers.get(type(node), self.handle_error)(node, cont)
        return node_repr

    def handle_constant(self, node, cont) -> str:
        return repr(node.value)

    def handle_name(self, node, cont) -> str:
        return node.id

    def handle_while(self, node, cont) -> str:
        self.needs_y = True
        assigned_in_loop = {self.apply_handler(n.targets[0]) for n in ast.walk(node) if
                            isinstance(n, ast.Assign) and not isinstance(n.targets[0], (ast.Attribute, ast.Subscript))}
        assigned_in_loop |= {self.apply_handler(n.target) for n in ast.walk(node) if
                             isinstance(n, ast.AugAssign) and not isinstance(n.target, (ast.Attribute, ast.Subscript))}
        args = ', '.join(assigned_in_loop)
        loop_test = self.apply_handler(node.test)
        loop_id = f'_loop{self.loop_no}'
        self.loop_no += 1
        loop_body = self.apply_handler2(node.body, f'{loop_id}({args})')
        loop_repr = construct_lambda(
            {loop_id: f'_Y(lambda {loop_id}: (lambda {args}: ({loop_body}) if {loop_test} else {cont}))'},
            f'{loop_id}({args})')
        return construct_lambda({v: f'{v} if "{v}" in dir() else None' for v in assigned_in_loop}, loop_repr)

    def handle_for(self, node, cont) -> str:
        target = self.apply_handler(node.target)
        iter_id = f'_items{self.loop_no}'
        term_id = f'_term{self.loop_no}'
        post = ast.parse(f'{target} = next({iter_id}, {term_id})').body
        body_list = node.body + post
        while_test = ast.parse(f'{target} is not {term_id}').body[0]
        while_equivalent = ast.While(while_test, body_list)
        return construct_lambda({term_id: '[]', iter_id: f'iter({self.apply_handler(node.iter)})'},
                                construct_lambda({target: f'next({iter_id}, {term_id})'},
                                                 self.apply_handler2(while_equivalent, cont)))

    def _handle_container(self, node) -> str:
        return ', '.join(self.apply_handler(child) for child in node.elts)

    def handle_list(self, node, cont) -> str:
        return f'[{self._handle_container(node)}]'

    def handle_tuple(self, node, cont) -> str:
        return f'({self._handle_container(node)})'

    def handle_set(self, node, cont) -> str:
        return '{' + self._handle_container(node) + '}'

    def handle_dict(self, node, cont) -> str:
        return '{' + ', '.join(f'{k}: {v}' for k, v in zip(map(self.apply_handler, node.keys),
                                                           map(self.apply_handler, node.values))) + '}'

    def handle_slice(self, node, cont) -> str:
        parts = [self.apply_handler(n) if n is not None else '' for n in [node.lower, node.upper, node.step]]
        return ':'.join(parts)

    def handle_subscript(self, node, cont) -> str:
        return f'{self.apply_handler(node.value)}[{self.apply_handler(node.slice)}]'

    def handle_attribute(self, node, cont) -> str:
        return f'{self.apply_handler(node.value)}.{node.attr}'

    def handle_assign(self, node, cont) -> str:
        target = node.targets[0]
        if isinstance(target, (ast.Attribute, ast.Subscript)):
            if not cont:
                return f'[None for {self.apply_handler(target)} in [{self.apply_handler(node.value)}]]'
            return f'[[None for {self.apply_handler(target)} in [{self.apply_handler(node.value)}]], {cont}][-1]'
        return construct_lambda({self.apply_handler(target): self.apply_handler(node.value)}, cont)

    def handle_augassign(self, node, cont) -> str:
        assign_equivalent = ast.Assign([node.target], ast.BinOp(node.target, node.op, node.value))
        return self.apply_handler2(assign_equivalent, cont)

    def handle_expr(self, node, cont) -> str:
        return self.apply_handler2(node.value, cont)

    def handle_call(self, node, cont) -> str:
        call = f'{self.apply_handler(node.func)}({", ".join(self.apply_handler(child) for child in node.args)})'
        return call if not cont else f'[{call}, {cont}][-1]'

    def handle_binop(self, node, cont) -> str:
        op_map = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.Mod: '%',
            ast.BitOr: '|',
            ast.BitAnd: '&',
        }
        return f'({self.apply_handler(node.left)} {op_map[type(node.op)]} {self.apply_handler(node.right)})'

    def handle_boolop(self, node, cont) -> str:
        op_map = {
            ast.And: 'and',
            ast.Or: 'or',
        }
        return f' {op_map[type(node.op)]} '.join(self.apply_handler(child) for child in node.values)

    def handle_unaryop(self, node, cont) -> str:
        op_map = {
            ast.UAdd: '+',
            ast.USub: '-',
            ast.Not: 'not ',
            ast.Invert: '~',
        }
        return f'{op_map[type(node.op)]}{self.apply_handler(node.operand)}'

    def handle_if(self, node, cont) -> str:
        return f'{self.apply_handler2(node.body, cont)} if {self.apply_handler(node.test)} else {self.apply_handler2(node.orelse, cont)}'

    def handle_compare(self, node, cont) -> str:
        op_map = {
            ast.Gt: '>',
            ast.Lt: '<',
            ast.GtE: '>=',
            ast.LtE: '<=',
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.In: 'in',
            ast.Is: 'is',
            ast.IsNot: 'is not',
            ast.NotIn: 'not in',
        }
        return f'{self.apply_handler(node.left)} {op_map[type(node.ops[0])]} {self.apply_handler(node.comparators[0])}'

    def handle_methoddef(self, node, cont) -> str:
        args = ', '.join(arg.arg for arg in node.args.args)
        if cont.endswith('__init__'):
            return f'lambda{" " if args else ""}{args}: [{self.apply_handler(node.body)}, None][-1]'
        if cont:
            for n in ast.walk(node):
                if isinstance(n, ast.Call) and self.apply_handler(n.func) == cont.split('.')[0]:
                    n.func.id = 'self.__class__'
        if any(isinstance(n, ast.Call) and self.apply_handler(n.func) == node.name for n in ast.walk(node)):
            self.needs_y = True
            return f'_Y(lambda {node.name}: (lambda {args}: {self.apply_handler(node.body)}))'
        return f'lambda{" " if args else ""}{args}: {self.apply_handler(node.body)}'

    def handle_functiondef(self, node, cont) -> str:
        return construct_lambda({node.name: self.handle_methoddef(node, '')}, cont)

    def handle_classdef(self, node, cont) -> str:
        attr_dict = {}
        for n in node.body:
            if isinstance(n, ast.FunctionDef):
                attr_dict[n.name] = self.handle_methoddef(n, f'{node.name}.{n.name}')
        attr_repr = '{' + ', '.join(f'{repr(k)}: {v}' for k, v in attr_dict.items()) + '}'
        return construct_lambda({node.name: f'type("{node.name}", (), {attr_repr})'}, cont)

    def handle_return(self, node, cont) -> str:
        if node.value is None:
            return 'None'
        return self.apply_handler(node.value)

    def handle_import(self, node, cont) -> str:
        imports = [(a.asname if a.asname else a.name, a.name) for a in node.names]
        return construct_lambda({name: f"__import__('{mod}')" for name, mod in imports}, cont)

    def handle_error(self, node, cont) -> str:
        return ast.unparse(node)

    def unparse_list(self, body: list, cont) -> str:
        temp = cont
        for node in body[::-1]:
            if not isinstance(node, ast.Expr) or isinstance(node.value, ast.Call):
                temp = self.apply_handler2(node, temp)
        return temp

    def unparse(self) -> str:
        """
        Unparses the ast.
        """
        self.needs_y = False
        self.loop_no = 1
        curr = self.ast
        if hasattr(curr, 'body') and isinstance(curr.body, list):
            body = self.apply_handler(curr.body)
            return provide_y(body) if self.needs_y else body
        return 'Unparse unsuccessful.'


if __name__ == '__main__':
    test = Flatliner()
    test.set_ast('test_input.py')
    result = test.unparse()
    print(result)