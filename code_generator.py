# code_generator.py

def generate_TAC(postfix):
    tac = []
    stack = []
    temp_count = 1

    for token in postfix:
        # numeric operand
        if isinstance(token, (int, float)):
            stack.append(token)
            continue

        # binary operators
        if token in ('PLUS','MINUS','MUL','DIV'):
            if len(stack) < 2:
                raise SyntaxError("Invalid postfix - insufficient operands for binary operator")
            right = stack.pop()
            left = stack.pop()
            op_sym = {'PLUS': '+', 'MINUS': '-', 'MUL': '*', 'DIV': '/'}[token]
            temp = f"t{temp_count}"
            temp_count += 1
            tac.append(f"{temp} = {left} {op_sym} {right}")
            stack.append(temp)
            continue

        # unary minus
        if token == 'UMINUS':
            if len(stack) < 1:
                raise SyntaxError("Invalid postfix - insufficient operands for unary minus")
            a = stack.pop()
            temp = f"t{temp_count}"
            temp_count += 1
            # represent as negation
            tac.append(f"{temp} = -{a}")
            stack.append(temp)
            continue

        # function tokens: ('FUNC', name, arity)
        if isinstance(token, tuple) and token[0] == 'FUNC':
            _, fname, arity = token
            if arity > len(stack):
                raise SyntaxError(f"Not enough arguments for function {fname}")
            args = [stack.pop() for _ in range(arity)][::-1]
            temp = f"t{temp_count}"
            temp_count += 1
            arg_str = ", ".join(str(a) for a in args)
            tac.append(f"{temp} = {fname}({arg_str})")
            stack.append(temp)
            continue

        # fallback: push unknowns
        stack.append(token)

    if stack:
        tac.append(f"print {stack[-1]}")
    return tac
