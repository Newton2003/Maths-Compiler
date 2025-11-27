# main.py

from lexer import tokenize
from my_parser import Parser
from intermediate_code import infix_to_postfix
from code_generator import generate_TAC
from assembly_generator import tac_to_assembly
from machine_code import assembly_to_machine_code

def evaluate_expression(expr):
    # Tokens
    tokens = tokenize(expr)
    # Postfix
    postfix = infix_to_postfix(tokens)
    # TAC
    tac = generate_TAC(postfix)
    # Assembly
    assembly_code = tac_to_assembly(tac)
    # Machine code
    machine_code = assembly_to_machine_code(assembly_code)
    # Parser result
    parser = Parser(tokens)
    result = parser.parse()
    return {
        "tokens": tokens,
        "postfix": postfix,
        "tac": tac,
        "assembly": assembly_code,
        "machine_code": machine_code,
        "result": result
    }

def main():
    while True:
        expr = input("Enter expression (or 'exit'): ")
        if expr.lower() == 'exit':
            break
        try:
            data = evaluate_expression(expr)
            print("Tokens:", data['tokens'])
            print("Postfix:", data['postfix'])
            print("TAC:")
            for line in data['tac']:
                print("  ", line)
            print("Assembly:")
            for line in data['assembly']:
                print("  ", line)
            print("Machine Code:")
            for code in data['machine_code']:
                print("  ", code)
            print("Result:", data['result'])
            print()
        except Exception as e:
            print("Error:", e)
            print()

if __name__ == "__main__":
    main()
