# maths_functions.py
import math

def call_function(name, args):
    """args is a list of evaluated numerical arguments"""
    # Helpers
    def to_num(x):
        return float(x)

    if name == 'sin':
        if len(args) != 1: raise TypeError("sin() takes exactly 1 argument")
        return math.sin(math.radians(to_num(args[0])))
    if name == 'cos':
        if len(args) != 1: raise TypeError("cos() takes exactly 1 argument")
        return math.cos(math.radians(to_num(args[0])))
    if name == 'tan':
        if len(args) != 1: raise TypeError("tan() takes exactly 1 argument")
        return math.tan(math.radians(to_num(args[0])))
    if name == 'sqrt':
        if len(args) != 1: raise TypeError("sqrt() takes exactly 1 argument")
        v = to_num(args[0])
        if v < 0:
            raise ValueError("sqrt() domain error for negative value")
        return math.sqrt(v)
    if name == 'log':
        # default log base 10 if one arg; if two args, log(x, base)
        if len(args) == 1:
            return math.log10(to_num(args[0]))
        elif len(args) == 2:
            x = to_num(args[0]); base = to_num(args[1])
            if x <= 0 or base <= 0:
                raise ValueError("log() domain error")
            return math.log(x, base)
        else:
            raise TypeError("log() takes 1 or 2 arguments")
    if name == 'exp':
        if len(args) != 1: raise TypeError("exp() takes exactly 1 argument")
        return math.exp(to_num(args[0]))
    if name == 'abs':
        if len(args) != 1: raise TypeError("abs() takes exactly 1 argument")
        return abs(to_num(args[0]))
    if name == 'pow':
        if len(args) == 1:
            return math.pow(to_num(args[0]), 2)  # default: square
        elif len(args) == 2:
            return math.pow(to_num(args[0]), to_num(args[1]))
        else:
            raise TypeError("pow() takes 1 or 2 arguments")

    raise NameError(f"Unknown function: {name}")
