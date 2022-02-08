import argparse
from ply import lex

#Reserved words
reserved ={
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN'
}
# List of token names. This is always required
tokens = [
    'ID',
    'BOOLEAN',
    'FLOAT',
    'NUMBER',
    'LETTER',

    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',

    'LT',           # <
    'GT',           # >
    'LTE',          # <=
    'GTE',          # >=
    'DOUBLEEQUAL',  # ==
    'NE',           # #

    'LBRACE',       # [
    'RBRACE',       # ]

    'OR',
    'AND',
    'GREATER',
    'LESSER',
    'GREATEREQ',
    'LESSEREQ',
    'EQ',

    'LPAREN',
    'RPAREN'
] + list(reserved.values())


class pythonLexer():
    t_ignore = ' \t'

    t_ignore_COMMENT = r'\#.*'


    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value,'ID')    # Check for reserved words
        return t

    # Regular expression rule with some action code
    t_LETTER = r'[\'\"][a-zA-Z]+[\'\"]'
    t_BOOLEAN = r'(?:True|False)'

    # math
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'

    # boolean
    t_OR = r'or'
    t_AND = r'and'
    t_GREATER = r'>'
    t_LESSER = r'<'
    t_GREATEREQ = r'>='
    t_LESSEREQ = r'<='
    t_EQ = r'=='

    # other 
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_FLOAT(self, t):
        r'\d+.\d*'
        t.value = float(t.value)
        return t

    # Define a rule so we can track line numbers. DO NOT MODIFY
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule. DO NOT MODIFY
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer. DO NOT MODIFY
    def build(self, **kwargs):
        self.tokens = tokens
        self.lexer = lex.lex(module=self, **kwargs)
    # Test the output. DO NOT MODIFY

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

# Main function. DO NOT MODIFY
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Take in the Python source code and perform lexical analysis.')
    parser.add_argument('FILE', help="Input file with Python source code")
    args = parser.parse_args()
    f = open(args.FILE, 'r')
    data = f.read()
    f.close()
    m = pythonLexer()
    m.build()
    m.test(data)