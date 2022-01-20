""" Lexer module for CLIQ test robot interpreter"""

###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

from token_types import *

class Token(object):
    """Tokens contain a type and a value"""
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __eq__(self, other):
        if self.type == other.type and self.value == other.value:
            return True
        else:
            return False

    def __str__(self):
        """String representation of the token class instance. Used to
        convert a token to a string.
        
        Examples:
            Token(INTEGER_CONST, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        """Same as __str__
        """
        return self.__str__()


VAR_TYPES = [INTEGER, BOOL, REAL, INTEGER_CONST, BOOL_CONST, REAL_CONST]
"""Dictionary of reserved words
"""
RESERVED_KEYWORDS: dict[str, Token] = {
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'BOOL': Token('BOOL', 'BOOL'),
    'DIV': Token('INTEGER_DIV', 'DIV'),
    'ELSE': Token('ELSE', 'ELSE'),
    'END': Token('END', 'END'),
    'ENDIF': Token('ENDIF', 'ENDIF'),
    'FALSE': Token('BOOL_CONST', 'FALSE'),
    'HOME': Token('HOME', 'HOME'),
    'IF': Token('IF', 'IF'),
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'IO': Token('IO', 'PIN'),
    'LOOP': Token('LOOP', 'LOOP'),
    'MOVETO': Token('MOVETO', 'MOVETO'),
    'NOT': Token('NOT', 'NOT'),
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'REAL': Token('REAL', 'REAL'),
    'ROTATE': Token('ROTATE', 'ROTATE'),
    'STOP' : Token('STOP', 'STOP'),
    'THEN': Token('THEN', 'THEN'),
    'TRUE': Token('BOOL_CONST', 'TRUE'),
    'TURN': Token('TURN', 'TURN'),
    'UNTIL': Token('UNTIL', 'UNTIL'),
    'VAR': Token('VAR', 'VAR'),
    'WAIT': Token('WAIT', 'WAIT'),
    'WAYPOINT': Token('WAYPOINT', 'WAYPOINT'),
}


class Lexer(object):
    """ This CLASS is responsible for breaking a program text
        apart into token objects.
        Tokenize string, e.g. '(4 + 2) * 3 - 6 / 2'.
        Each character is represented by a token
        """
    def __init__(self, text):
        """self.pos:  an index into self.text
           self.line: the line number count used to report error location.
           self.line_pos: index within active line used to report position of error.
        """
        self.text = text
        # self.pos is an index into self.text.
        #line_count and line_pos are used to report the location of syntax errors.
        self.line_count = 0
        self.line_pos = 0
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        """ Reports the location of an invalid character in the input text
        """
        raise ValueError(f"Invalid character '{self.current_char}' in line {self.line_count} at position {self.line_pos}")

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable.
           Also keeps track of where we are in the line
        """
        self.pos += 1
        self.line_pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        """Look at next character in text without consuming it.
        """
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        """White space is removed by skipping.
        """
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line_count += 1
                self.line_pos = 0
            self.advance()

    def skip_comment(self):
        """Scans text for closing brace of a comment. Raises exception on EOL.
        """
        while self.current_char != '}':
            self.advance()
            if self.current_char == '\n':
                raise Exception(f'Missing closing brace at line {self.line_count} position {self.line_pos}')
        self.advance()  # the closing curly brace

    def number(self):
        """Return a (multi-digit) integer or float consumed from the input.
        """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            token = Token('REAL_CONST', float(result))
        else:
            token = Token('INTEGER_CONST', int(result))
        return token

    def _id(self):
        """Handle identifiers and reserved keywords
        """
        result = ''
        while self.current_char is not None and self.current_char.isidentifier():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        """Identifies operators and return a token for the operator.
        Removes whitespace from input and skips over {comments}
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isidentifier():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(EQUAL, '==')

            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(NEQUAL, '!=')

            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(LTE, '<=')

            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(GTE, '>=')

            if self.current_char == '<' and self.peek() != '=':
                self.advance()
                return Token(LT, '<')

            if self.current_char == '>' and self.peek() != '=':
                self.advance()
                return Token(GT, '>')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(FLOAT_DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')
            else:
                self.error()
        return Token(EOF, None)
