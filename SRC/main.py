from parser import Parser
from lexer import Lexer
from gcode_maker import open_serial_port
from interpreter import Interpreter

def main():
    import sys
    try:
        text = open(sys.argv[1], 'r').read()
    except IndexError:
        text = open('../cliq_test.txt', 'r').read()

    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        with open_serial_port():
            interpreter.interpret()
        for k, v in sorted(interpreter.GLOBAL_SCOPE.items()):
            print('{} = {}'.format(k, v))
    except Exception as ex:
        raise ex

if __name__ == "__main__":
    main()
