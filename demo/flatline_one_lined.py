(lambda _Y: (lambda ast: (lambda construct_lambda: (lambda provide_y: (lambda wrap_globals: (lambda Flatliner: (lambda test: [test.set_ast('test_input.py'), (lambda result: print(result))(test.unparse())][-1])(Flatliner()) if __name__ == '__main__' else None)(type("Flatliner", (), {'__init__': lambda self: [[[None for self.ast in [None]], [[None for self.needs_y in [False]], [[None for self.loop_no in [1]], [None for self.node_handlers in [{ast.Assign: self.handle_assign, ast.AugAssign: self.handle_augassign, ast.Constant: self.handle_constant, ast.Expr: self.handle_expr, ast.Call: self.handle_call, ast.Name: self.handle_name, ast.While: self.handle_while, ast.For: self.handle_for, ast.List: self.handle_list, ast.Tuple: self.handle_tuple, ast.Set: self.handle_set, ast.Dict: self.handle_dict, ast.Subscript: self.handle_subscript, ast.Slice: self.handle_slice, ast.Attribute: self.handle_attribute, ast.BinOp: self.handle_binop, ast.If: self.handle_if, list: self.unparse_list, ast.Compare: self.handle_compare, ast.BoolOp: self.handle_boolop, ast.UnaryOp: self.handle_unaryop, ast.FunctionDef: self.handle_functiondef, ast.ClassDef: self.handle_classdef, ast.Return: self.handle_return, ast.Import: self.handle_import}]]][-1]][-1]][-1], None][-1], 'set_ast': lambda self, infile: (lambda file: [[None for self.ast in [ast.parse(file.read())]], (lambda close: None)(file.close())][-1])(open(infile, 'r')), 'apply_handler': lambda self, node: (lambda node_repr: node_repr)(self.node_handlers.get(type(node), self.handle_error)(node, None)), 'apply_handler2': lambda self, node, cont: (lambda node_repr: node_repr)(self.node_handlers.get(type(node), self.handle_error)(node, cont)), 'handle_constant': lambda self, node, cont: repr(node.value), 'handle_name': lambda self, node, cont: node.id, 'handle_while': lambda self, node, cont: [[None for self.needs_y in [True]], (lambda assigned_in_loop: (lambda assigned_in_loop: (lambda args: (lambda loop_test: (lambda loop_id: [[None for self.loop_no in [(self.loop_no + 1)]], (lambda loop_body: (lambda loop_repr: construct_lambda({v: f'{v} if "{v}" in dir() else None' for v in assigned_in_loop}, loop_repr))(construct_lambda({loop_id: f'_Y(lambda {loop_id}: (lambda {args}: ({loop_body}) if {loop_test} else {cont}))'}, f'{loop_id}({args})')))(self.apply_handler2(node.body, f'{loop_id}({args})'))][-1])(f'_loop{self.loop_no}'))(self.apply_handler(node.test)))(', '.join(assigned_in_loop)))((assigned_in_loop | {self.apply_handler(n.target) for n in ast.walk(node) if isinstance(n, ast.AugAssign) and (not isinstance(n.target, (ast.Attribute, ast.Subscript)))})))({self.apply_handler(n.targets[0]) for n in ast.walk(node) if isinstance(n, ast.Assign) and (not isinstance(n.targets[0], (ast.Attribute, ast.Subscript)))})][-1], 'handle_for': lambda self, node, cont: (lambda target: (lambda iter_id: (lambda term_id: (lambda post: (lambda body_list: (lambda while_test: (lambda while_equivalent: construct_lambda({term_id: '[]', iter_id: f'iter({self.apply_handler(node.iter)})'}, construct_lambda({target: f'next({iter_id}, {term_id})'}, self.apply_handler2(while_equivalent, cont))))(ast.While(while_test, body_list)))(ast.parse(f'{target} is not {term_id}').body[0]))((node.body + post)))(ast.parse(f'{target} = next({iter_id}, {term_id})').body))(f'_term{self.loop_no}'))(f'_items{self.loop_no}'))(self.apply_handler(node.target)), '_handle_container': lambda self, node: ', '.join((self.apply_handler(child) for child in node.elts)), 'handle_list': lambda self, node, cont: f'[{self._handle_container(node)}]', 'handle_tuple': lambda self, node, cont: f'({self._handle_container(node)})', 'handle_set': lambda self, node, cont: (('{' + self._handle_container(node)) + '}'), 'handle_dict': lambda self, node, cont: (('{' + ', '.join((f'{k}: {v}' for (k, v) in zip(map(self.apply_handler, node.keys), map(self.apply_handler, node.values))))) + '}'), 'handle_slice': lambda self, node, cont: (lambda parts: ':'.join(parts))([self.apply_handler(n) if n is not None else '' for n in [node.lower, node.upper, node.step]]), 'handle_subscript': lambda self, node, cont: f'{self.apply_handler(node.value)}[{self.apply_handler(node.slice)}]', 'handle_attribute': lambda self, node, cont: f'{self.apply_handler(node.value)}.{node.attr}', 'handle_assign': lambda self, node, cont: (lambda target: f'[None for {self.apply_handler(target)} in [{self.apply_handler(node.value)}]]' if not cont else f'[[None for {self.apply_handler(target)} in [{self.apply_handler(node.value)}]], {cont}][-1]' if isinstance(target, (ast.Attribute, ast.Subscript)) else construct_lambda({self.apply_handler(target): self.apply_handler(node.value)}, cont))(node.targets[0]), 'handle_augassign': lambda self, node, cont: (lambda assign_equivalent: self.apply_handler2(assign_equivalent, cont))(ast.Assign([node.target], ast.BinOp(node.target, node.op, node.value))), 'handle_expr': lambda self, node, cont: self.apply_handler2(node.value, cont), 'handle_call': lambda self, node, cont: (lambda call: call if not cont else f'[{call}, {cont}][-1]')(f"{self.apply_handler(node.func)}({', '.join((self.apply_handler(child) for child in node.args))})"), 'handle_binop': lambda self, node, cont: (lambda op_map: f'({self.apply_handler(node.left)} {op_map[type(node.op)]} {self.apply_handler(node.right)})')({ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/', ast.Mod: '%', ast.BitOr: '|', ast.BitAnd: '&'}), 'handle_boolop': lambda self, node, cont: (lambda op_map: f' {op_map[type(node.op)]} '.join((self.apply_handler(child) for child in node.values)))({ast.And: 'and', ast.Or: 'or'}), 'handle_unaryop': lambda self, node, cont: (lambda op_map: f'{op_map[type(node.op)]}{self.apply_handler(node.operand)}')({ast.UAdd: '+', ast.USub: '-', ast.Not: 'not ', ast.Invert: '~'}), 'handle_if': lambda self, node, cont: f'{self.apply_handler2(node.body, cont)} if {self.apply_handler(node.test)} else {self.apply_handler2(node.orelse, cont)}', 'handle_compare': lambda self, node, cont: (lambda op_map: f'{self.apply_handler(node.left)} {op_map[type(node.ops[0])]} {self.apply_handler(node.comparators[0])}')({ast.Gt: '>', ast.Lt: '<', ast.GtE: '>=', ast.LtE: '<=', ast.Eq: '==', ast.NotEq: '!=', ast.In: 'in', ast.Is: 'is', ast.IsNot: 'is not', ast.NotIn: 'not in'}), 'handle_methoddef': lambda self, node, cont: (lambda args: f"lambda{(' ' if args else '')}{args}: [{self.apply_handler(node.body)}, None][-1]" if cont.endswith('__init__') else (lambda _term1, _items1: (lambda n: (lambda n: (lambda _loop1: _loop1(n))(_Y(lambda _loop1: (lambda n: ([[None for n.func.id in ['self.__class__']], (lambda n: _loop1(n))(next(_items1, _term1))][-1] if isinstance(n, ast.Call) and self.apply_handler(n.func) == cont.split('.')[0] else (lambda n: _loop1(n))(next(_items1, _term1))) if n is not _term1 else [[None for self.needs_y in [True]], f'_Y(lambda {node.name}: (lambda {args}: {self.apply_handler(node.body)}))'][-1] if any((isinstance(n, ast.Call) and self.apply_handler(n.func) == node.name for n in ast.walk(node))) else f"lambda{(' ' if args else '')}{args}: {self.apply_handler(node.body)}"))))(n if "n" in dir() else None))(next(_items1, _term1)))([], iter(ast.walk(node))) if cont else [[None for self.needs_y in [True]], f'_Y(lambda {node.name}: (lambda {args}: {self.apply_handler(node.body)}))'][-1] if any((isinstance(n, ast.Call) and self.apply_handler(n.func) == node.name for n in ast.walk(node))) else f"lambda{(' ' if args else '')}{args}: {self.apply_handler(node.body)}")(', '.join((arg.arg for arg in node.args.args))), 'handle_functiondef': lambda self, node, cont: construct_lambda({node.name: self.handle_methoddef(node, '')}, cont), 'handle_classdef': lambda self, node, cont: (lambda attr_dict: (lambda _term2, _items2: (lambda n: (lambda n: (lambda _loop2: _loop2(n))(_Y(lambda _loop2: (lambda n: ([[None for attr_dict[n.name] in [self.handle_methoddef(n, f'{node.name}.{n.name}')]], (lambda n: _loop2(n))(next(_items2, _term2))][-1] if isinstance(n, ast.FunctionDef) else (lambda n: _loop2(n))(next(_items2, _term2))) if n is not _term2 else (lambda attr_repr: construct_lambda({node.name: f'type("{node.name}", (), {attr_repr})'}, cont))((('{' + ', '.join((f'{repr(k)}: {v}' for (k, v) in attr_dict.items()))) + '}'))))))(n if "n" in dir() else None))(next(_items2, _term2)))([], iter(node.body)))({}), 'handle_return': lambda self, node, cont: 'None' if node.value is None else self.apply_handler(node.value), 'handle_import': lambda self, node, cont: (lambda imports: construct_lambda({name: f"__import__('{mod}')" for (name, mod) in imports}, cont))([(a.asname if a.asname else a.name, a.name) for a in node.names]), 'handle_error': lambda self, node, cont: ast.unparse(node), 'unparse_list': lambda self, body, cont: (lambda temp: (lambda _term3, _items3: (lambda node: (lambda node, temp: (lambda _loop3: _loop3(node, temp))(_Y(lambda _loop3: (lambda node, temp: ((lambda temp: (lambda node: _loop3(node, temp))(next(_items3, _term3)))(self.apply_handler2(node, temp)) if not isinstance(node, ast.Expr) or isinstance(node.value, ast.Call) else (lambda node: _loop3(node, temp))(next(_items3, _term3))) if node is not _term3 else str(temp)))))(node if "node" in dir() else None, temp if "temp" in dir() else None))(next(_items3, _term3)))([], iter(body[::-1])))(cont), 'unparse': lambda self: [[None for self.needs_y in [False]], [[None for self.loop_no in [1]], (lambda curr: (lambda body: provide_y(body) if self.needs_y else body)(self.apply_handler(curr.body)) if hasattr(curr, 'body') and isinstance(curr.body, list) else 'Unparse unsuccessful.')(self.ast)][-1]][-1]})))(lambda body: construct_lambda({'__g': 'globals()'}, body)))(lambda body: construct_lambda({'_Y': '(lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args))))'}, body)))(lambda vals, body: f"(lambda {', '.join(vals.keys())}: {body})({', '.join(vals.values())})"))(__import__('ast')))((lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))))
