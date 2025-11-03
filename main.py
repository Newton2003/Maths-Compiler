from lexer import tokenize
from parser import Parser
from intermediate_code import infix_to_postfix
from code_generator import generate_TAC

def evaluate_expression(expr):
    tokens = tokenize(expr)
    postfix = infix_to_postfix(tokens)
    tac = generate_TAC(postfix)
    parser = Parser(tokens)
    result = parser.parse()
    return postfix, tac, result

def main():
    while True:
        expr = input("Enter expression (or 'exit'): ")
        if expr.lower() == 'exit':
            break
        try:
            tokens = tokenize(expr)
            print("Tokens:", tokens)
            postfix = infix_to_postfix(tokens)
            print("Intermediate code (postfix):", postfix)
            tac = generate_TAC(postfix)
            print("Three Address Code (TAC):")
            for line in tac:
                print(" ", line)
            parser = Parser(tokens)
            result = parser.parse()
            print("Result:", result)
            print()
        except Exception as e:
            print("Error:", e)
            print()

if __name__ == "__main__":
    main()
