# parser.py

from maths_functions import call_function

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def advance(self):
        self.pos += 1

    def parse(self):
        result = self.expr()
        kind, _ = self.peek()
        if kind != 'EOF':
            raise SyntaxError("Unexpected token at end")
        return result

    # Grammar:
    # expr -> term ((PLUS|MINUS) term)*
    # term -> factor ((MUL|DIV) factor)*
    # factor -> MINUS factor | NUMBER | FUNC LPAREN arg_list RPAREN | LPAREN expr RPAREN

    def expr(self):
        result = self.term()
        while True:
            kind, _ = self.peek()
            if kind == 'PLUS':
                self.advance()
                result += self.term()
            elif kind == 'MINUS':
                self.advance()
                result -= self.term()
            else:
                return result

    def term(self):
        result = self.factor()
        while True:
            kind, _ = self.peek()
            if kind == 'MUL':
                self.advance()
                result *= self.factor()
            elif kind == 'DIV':
                self.advance()
                divisor = self.factor()
                if divisor == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= divisor
            else:
                return result

    def factor(self):
        kind, value = self.peek()

        if kind == 'MINUS':
            self.advance()
            return -self.factor()

        if kind == 'NUMBER':
            self.advance()
            return value

        if kind == 'FUNC':
            func_name = value
            self.advance()
            kind, _ = self.peek()
            if kind != 'LPAREN':
                raise SyntaxError("Expected '(' after function name")
            self.advance()  # consume '('
            args = self.arg_list()
            kind, _ = self.peek()
            if kind != 'RPAREN':
                raise SyntaxError("Expected ')' after function arguments")
            self.advance()  # consume ')'
            return call_function(func_name, args)

        if kind == 'LPAREN':
            self.advance()
            result = self.expr()
            kind, _ = self.peek()
            if kind != 'RPAREN':
                raise SyntaxError("Expected ')'")
            self.advance()
            return result

        raise SyntaxError(f"Unexpected token: {kind}")

    def arg_list(self):
        """Parse zero or more comma-separated expressions inside function parentheses.
           Returns a list of evaluated arguments."""
        args = []
        kind, _ = self.peek()
        if kind == 'RPAREN':
            return args  # empty arg list
        # At least one argument
        args.append(self.expr())
        while True:
            kind, _ = self.peek()
            if kind == 'COMMA':
                self.advance()
                args.append(self.expr())
            else:
                break
        return args
