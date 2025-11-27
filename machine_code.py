# machine_code.py

def assembly_to_machine_code(assembly):
    """
    Convert pseudo x86-like assembly to a simple binary string format.
    For demonstration purposes only.
    """
    opcode_map = {
        'MOV':'0001',
        'ADD':'0010',
        'SUB':'0011',
        'MUL':'0100',
        'DIV':'0101',
        'NEG':'0110',
        'CALL':'0111',
        'OUT':'1000'
    }
    machine = []
    for instr in assembly:
        parts = instr.split()
        op = parts[0]
        operands = parts[1:] if len(parts)>1 else []
        code = opcode_map.get(op,'1111') + ''.join([f"{hash(o)%256:08b}" for o in operands])
        machine.append(code)
    return machine
