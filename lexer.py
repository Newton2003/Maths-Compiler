# lexer.py
import re

TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('FUNC',     r'sin|cos|tan|log|sqrt|exp|abs|pow'),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('MUL',      r'\*'),
    ('DIV',      r'/'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('COMMA',    r','),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]

TOK_REGEX = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC)
_get_token = re.compile(TOK_REGEX).match

def tokenize(expression):
    tokens = []
    pos = 0
    mo = _get_token(expression, pos)
    while mo is not None:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append((kind, float(value)))
        elif kind == 'FUNC':
            tokens.append((kind, value))
        elif kind in ('PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'COMMA'):
            tokens.append((kind, value))
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character: {value!r} at position {pos}")
        pos = mo.end()
        mo = _get_token(expression, pos)
    tokens.append(('EOF', None))
    return tokens
