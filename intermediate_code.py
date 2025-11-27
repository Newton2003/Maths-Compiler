# intermediate_code.py

def _is_unary_minus(prev_kind):
    return prev_kind is None or prev_kind in ('PLUS','MINUS','MUL','DIV','LPAREN','COMMA','FUNC')

def infix_to_postfix(tokens):
    precedence = {'PLUS': 1, 'MINUS': 1, 'MUL': 2, 'DIV': 2, 'UMINUS': 3}
    right_assoc = {'UMINUS'}
    output = []
    stack = []
    func_arg_counts = []
    prev_kind = None
    i = 0
    while i < len(tokens):
        kind, value = tokens[i]
        if kind == 'NUMBER':
            output.append(value)
            prev_kind = 'NUMBER'
            i += 1
            continue
        if kind == 'MINUS':
            if _is_unary_minus(prev_kind):
                if i + 1 < len(tokens) and tokens[i+1][0] == 'NUMBER':
                    output.append(-tokens[i+1][1])
                    i += 2
                    prev_kind = 'NUMBER'
                    continue
                else:
                    while stack and stack[-1] in precedence and (
                        (precedence[stack[-1]] > precedence['UMINUS']) or
                        (precedence[stack[-1]] == precedence['UMINUS'] and stack[-1] not in right_assoc)
                    ):
                        output.append(stack.pop())
                    stack.append('UMINUS')
                    prev_kind = 'MINUS'
                    i += 1
                    continue
            else:
                kind = 'MINUS'
        if kind in ('PLUS','MINUS','MUL','DIV'):
            while stack and stack[-1] != 'LPAREN' and (
                (stack[-1] in precedence and precedence[stack[-1]] >= precedence[kind]) or
                (isinstance(stack[-1], tuple) and stack[-1][0] == 'FUNC')
            ):
                output.append(stack.pop())
            stack.append(kind)
            prev_kind = kind
            i += 1
            continue
        if kind == 'FUNC':
            stack.append(('FUNC', value))
            func_arg_counts.append(0)
            prev_kind = 'FUNC'
            i += 1
            continue
        if kind == 'LPAREN':
            stack.append('LPAREN')
            prev_kind = 'LPAREN'
            i += 1
            continue
        if kind == 'COMMA':
            while stack and stack[-1] != 'LPAREN':
                output.append(stack.pop())
            if func_arg_counts:
                func_arg_counts[-1] += 1
            prev_kind = 'COMMA'
            i += 1
            continue
        if kind == 'RPAREN':
            while stack and stack[-1] != 'LPAREN':
                output.append(stack.pop())
            if not stack:
                raise SyntaxError("Mismatched parentheses")
            stack.pop()
            if stack and isinstance(stack[-1], tuple) and stack[-1][0] == 'FUNC':
                func_tuple = stack.pop()
                cnt = func_arg_counts.pop() + 1 if func_arg_counts else 0
                output.append(('FUNC', func_tuple[1], cnt))
            prev_kind = 'RPAREN'
            i += 1
            continue
        if kind == 'EOF':
            break
        i += 1
    while stack:
        item = stack.pop()
        if item == 'LPAREN':
            raise SyntaxError("Mismatched parentheses")
        output.append(item)
    return output
