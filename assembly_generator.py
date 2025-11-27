# assembly_generator.py

def tac_to_assembly(tac):
    """
    Convert TAC to x86-like pseudo assembly.
    """
    assembly = []
    for line in tac:
        if line.startswith("print"):
            temp = line.split()[1]
            assembly.append(f"OUT {temp}")
        elif "=" in line:
            left, expr = line.split("=",1)
            left = left.strip()
            expr = expr.strip()
            # check for binary operation
            for op in ('+','-','*','/'):
                if op in expr:
                    a,b = expr.split(op)
                    a,b = a.strip(),b.strip()
                    assembly.append(f"MOV R1, {a}")
                    assembly.append(f"MOV R2, {b}")
                    asm_op = {'+':'ADD','-':'SUB','*':'MUL','/':'DIV'}[op]
                    assembly.append(f"{asm_op} R1, R2")
                    assembly.append(f"MOV {left}, R1")
                    break
            else:
                # unary or function
                if expr.startswith("-"):
                    val = expr[1:]
                    assembly.append(f"MOV R1, {val}")
                    assembly.append(f"NEG R1")
                    assembly.append(f"MOV {left}, R1")
                elif "(" in expr:  # function call
                    fname, args = expr.split("(",1)
                    args = args.rstrip(")").split(",")
                    for idx,arg in enumerate(args):
                        assembly.append(f"MOV R{idx+1}, {arg.strip()}")
                    assembly.append(f"CALL {fname.strip()}")
                    assembly.append(f"MOV {left}, R1")
                else:
                    assembly.append(f"MOV {left}, {expr}")
    return assembly
