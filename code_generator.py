# code_generator.py

def generate_TAC(postfix):
    tac = []
    stack = []
    temp_count = 1
    for token in postfix:
        if isinstance(token, (int,float)):
            stack.append(token)
            continue
        if token in ('PLUS','MINUS','MUL','DIV'):
            right = stack.pop()
            left = stack.pop()
            op_sym = {'PLUS': '+','MINUS':'-','MUL':'*','DIV':'/'}[token]
            temp = f"t{temp_count}"
            temp_count += 1
            tac.append(f"{temp} = {left} {op_sym} {right}")
            stack.append(temp)
            continue
        if token == 'UMINUS':
            a = stack.pop()
            temp = f"t{temp_count}"
            temp_count += 1
            tac.append(f"{temp} = -{a}")
            stack.append(temp)
            continue
        if isinstance(token, tuple) and token[0]=='FUNC':
            _, fname, arity = token
            args = [stack.pop() for _ in range(arity)][::-1]
            temp = f"t{temp_count}"
            temp_count += 1
            arg_str = ", ".join(str(a) for a in args)
            tac.append(f"{temp} = {fname}({arg_str})")
            stack.append(temp)
            continue
        stack.append(token)
    if stack:
        tac.append(f"print {stack[-1]}")
    return tac

def generate_full_backends(postfix):
    """
    Converts postfix to TAC, assembly-like, and binary-like machine code.
    """
    tac = generate_TAC(postfix)
    
    # Simple assembly: map operators to assembly instructions
    op_map = {'PLUS':'ADD', 'MINUS':'SUB', 'MUL':'MUL', 'DIV':'DIV', 'UMINUS':'NEG'}
    assembly = []
    machine = []

    temp_count = 1
    for token in postfix:
        if isinstance(token, (int,float)):
            assembly.append(f"LOAD R{temp_count}, {token}")
            machine.append(f"{int(token):08b}")  # simple 8-bit binary
            temp_count += 1
        elif token in op_map:
            assembly.append(f"{op_map[token]} R{temp_count-2}, R{temp_count-1}")
            machine.append(f"{bin(temp_count-1)[2:].zfill(4)} {bin(temp_count-2)[2:].zfill(4)} {op_map[token][0:4]}") 
            temp_count -= 1
        elif isinstance(token, tuple) and token[0]=='FUNC':
            fname = token[1]
            arity = token[2]
            assembly.append(f"CALL {fname}, {arity} args")
            machine.append(f"FUNC {fname} {arity}")
    
    return tac, assembly, machine
