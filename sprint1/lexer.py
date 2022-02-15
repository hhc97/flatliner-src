import argparse

from ply import lex

NO_INDENT = 0
MUST_INDENT = 2

# Reserved words
reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    ':': 'COLON',
    ',': 'COMMA',
    'or': 'OR',
    'and': 'AND',
    'def': 'DEF',
    'None': 'NONE',
    'elif': 'ELIF',
    'in': 'IN',
    'not': 'NOT',
    'pass': 'PASS',
}
# List of token names. This is always required
tokens = [
             'ID',
             'BOOLEAN',
             'FLOAT',
             'NUMBER',
             'STRING',
             'ASSIGN',
             'PLUS',
             'MINUS',
             'TIMES',
             'DIVIDE',
             'DOT',

             'PE',  # +=
             'ME',  # -=
             'MODULO',

             'GREATER',
             'LESSER',
             'GREATEREQ',
             'LESSEREQ',
             'EQ',
             'NEQ',

             'COMMENT',
             'NEWLINE',

             'LPAREN',
             'RPAREN',
             'LBRACE',
             'RBRACE',
             'WS',

             'DEDENT',
             'INDENT'
         ] + list(reserved.values())


class PythonLexer:
    states = (
        ("COMMENT", "exclusive"),
    )

    def t_start_comment(self, t):
        r'\"\"\"'
        t.lexer.push_state("COMMENT")

    def t_COMMENT_error(self, t):
        print("Illegal COMMENT character '%s'" % t.value[0])
        t.lexer.skip(1)

    t_COMMENT_ignore = ''

    def t_COMMENT_contents(self, t):
        r'[^"][^"][^"]*'

    def t_COMMENT_end(self, t):
        r'\"\"\"'
        t.lexer.pop_state()

    def t_BOOLEAN(self, t):
        r'(?:True|False)'
        t.value = t.value == 'True'
        return t

    t_ignore_COMMENT = r'\#.*'

    def t_STRING(self, t):
        r'[\'][^\']*[\']|[\"][^\"]*[\"]'
        t.value = t.value[1:-1]
        return t

    def t_ID(self, t):
        r'[a-zA-Z_:,][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    # Regular expression rule with some action code

    # math
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_PE = r'\+\='
    t_ME = r'\-\='

    t_DOT = r'\.'
    t_MODULO = r'\%'

    # boolean algebra
    t_GREATER = r'>'
    t_LESSER = r'<'
    t_GREATEREQ = r'>='
    t_EQ = r'=='
    t_ASSIGN = r'='
    t_LESSEREQ = r'<='
    t_NEQ = r'!='

    # other 

    t_LBRACE = r'\['
    t_RBRACE = r'\]'

    def t_LPAREN(self, t):
        r'\('
        return t

    def t_RPAREN(self, t):
        r'\)'
        return t

    def t_WS(self, t):
        r' [ ]+ '
        if self.lexer.at_line_start:
            return t

    def t_FLOAT(self, t):
        '[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
        t.value = float(t.value)
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers. DO NOT MODIFY
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.type = "NEWLINE"
        return t

    # Error handling rule. DO NOT MODIFY
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Lexer functions
    def build(self, **kwargs):
        self.tokens = tokens
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.at_line_start = False

    def make_token(self, type, lineno, lexpos):
        tok = lex.LexToken()
        tok.type = type
        tok.value = None
        tok.lineno = lineno
        tok.lexpos = lexpos
        return tok

    def dedent(self, lineno, lexpos):
        return self.make_token('DEDENT', lineno, lexpos)

    def indent(self, lineno, lexpos):
        return self.make_token('INDENT', lineno, lexpos)

    def track_tokens_filter(self, lexer, tokens):
        lexer.at_line_start = True
        at_line_start = True
        indent = NO_INDENT
        for token in tokens:
            token.at_line_start = at_line_start

            if token.type == "COLON":
                at_line_start = False
                indent = MUST_INDENT
                token.must_indent = False

            elif token.type == "NEWLINE":
                at_line_start = True
                token.must_indent = False

            elif token.type == "WS":
                at_line_start = True
                token.must_indent = False

            else:
                if indent == MUST_INDENT:
                    token.must_indent = True
                else:
                    token.must_indent = False
                at_line_start = False
                indent = NO_INDENT

            yield token
            lexer.at_line_start = at_line_start

    def process_indentation(self, tokens):
        levels = [0]
        token = None
        depth = 0
        prev_was_ws = False
        for token in tokens:
            if token.type == "WS":
                assert depth == 0
                depth = len(token.value)
                prev_was_ws = True
                # WS tokens are never passed to the parser
                continue

            if token.type == "NEWLINE":
                depth = 0
                if prev_was_ws or token.at_line_start:
                    continue
                yield token
                continue
            prev_was_ws = False
            if token.must_indent:
                # The current depth must be larger than the previous level
                if not (depth > levels[-1]):
                    raise IndentationError("expected an indented block")

                levels.append(depth)
                yield self.indent(token.lineno, token.lexpos)

            elif token.at_line_start:
                # Must be on the same level or one of the previous levels
                if depth == levels[-1]:
                    # At the same level
                    pass
                elif depth > levels[-1]:
                    raise IndentationError(
                        "indentation increase but not in new block")
                else:
                    # Back up; but only if it matches a previous level
                    try:
                        i = levels.index(depth)
                    except ValueError:
                        raise IndentationError("inconsistent indentation")
                    for _ in range(i + 1, len(levels)):
                        yield self.dedent(token.lineno, token.lexpos)
                        levels.pop()

            yield token
        if len(levels) > 1:
            for _ in range(1, len(levels)):
                yield self.dedent(token.lineno, token.lexpos)

    def process(self, lexer):
        tokens = iter(lexer.token, None)
        tokens = self.track_tokens_filter(lexer, tokens)
        for token in self.process_indentation(tokens):
            yield token

    def get_token_external(self):
        if not hasattr(self, 'token_generator'):
            self.token_generator = self.process(self.lexer)
        return next(self.token_generator, None)

    def test(self, data):
        self.lexer.input(data)
        self.token_generator = self.process(self.lexer)
        for token in self.token_generator:
            print(token)


# Main function. DO NOT MODIFY
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Take in the Python source code and perform lexical analysis.')
    parser.add_argument('FILE', help="Input file with Python source code")
    args = parser.parse_args()
    f = open(args.FILE, 'r')
    data = f.read()
    f.close()
    m = PythonLexer()
    m.build()
    m.test(data)
