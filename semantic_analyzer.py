# semantic_analyzer.py

import math

class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.valid_funcs = {'sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'abs', 'pow'}

    def analyze(self):
        """Perform semantic checks on the list of tokens."""
        for i, (kind, value) in enumerate(self.tokens):

            # ✅ Check for invalid function names
            if kind == 'FUNC' and value not in self.valid_funcs:
                raise ValueError(f"Semantic Error: Unknown function '{value}'")

            # ✅ Check for division by zero
            if kind == 'DIV':
                if i + 1 < len(self.tokens):
                    next_kind, next_val = self.tokens[i + 1]
                    if next_kind == 'NUMBER' and next_val == 0:
                        raise ZeroDivisionError("Semantic Error: Division by zero detected")

            # ✅ Check for sqrt() of a negative number
            if kind == 'FUNC' and value == 'sqrt':
                if i + 1 < len(self.tokens) and self.tokens[i + 1][0] == 'LPAREN':
                    # look ahead for possible '-NUMBER' inside parentheses
                    if i + 3 < len(self.tokens):
                        k1, v1 = self.tokens[i + 2]
                        k2, v2 = self.tokens[i + 3]
                        if k1 == 'MINUS' and k2 == 'NUMBER' and v2 < 0:
                            raise ValueError("Semantic Error: sqrt() of negative number")
                        elif k1 == 'MINUS' and k2 == 'NUMBER':
                            raise ValueError("Semantic Error: sqrt() of negative number")
                        elif k1 == 'NUMBER' and v1 < 0:
                            raise ValueError("Semantic Error: sqrt() of negative number")

        return True
