import pytest
from token_types import *

token_list = [
    ('WAIT', WAIT, 'WAIT'),
    ('TRUE', BOOL_CONST, TRUE),
    ('FALSE', BOOL_CONST, FALSE),
    ('234', INTEGER_CONST, 234),
    ('3.14', REAL_CONST, 3.14),
    ('*', MUL, '*'),
    ('DIV', INTEGER_DIV, 'DIV'),
    ('/', FLOAT_DIV, '/'),
    ('+', PLUS, '+'),
    ('-', MINUS, '-'),
    ('(', LPAREN, '('),
    (')', RPAREN, ')'),
    (':=', ASSIGN, ':='),
    ('==', EQUAL, '=='),
    ('!=', NEQUAL, '!='),
    ('<=', LTE, '<='),
    ('>=', GTE, '>='),
    ('<', LT, '<'),
    ('>', GT, '>'),
    ('.', DOT, '.'),
    (';', SEMI, ';'),
    ('IF', IF, 'IF'),
    ('ELSE', ELSE, 'ELSE'),
    ('ENDIF', ENDIF, 'ENDIF'),
    ('LOOP', LOOP, 'LOOP'),
    ('UNTIL', UNTIL, 'UNTIL'),
    ('MOVETO', MOVETO, 'MOVETO'),
    ('ROTATE', ROTATE, 'ROTATE'),
    ('STOP', STOP, 'STOP'),
    ('HOME', HOME, 'HOME'),
    ('number', ID, 'number'),
    ('BEGIN', BEGIN, 'BEGIN'),
    ('WAYPOINT', WAYPOINT, 'WAYPOINT'),
    ('IO', IO, 'PIN'),
    ('END', END, 'END'),
]


def makeLexer(text):
    from lexer import Lexer
    lexer = Lexer(text)
    return lexer


@pytest.mark.parametrize("text, tok_type, tok_val", token_list)
def test_tokens(text, tok_type, tok_val):
    lexer = makeLexer(text)
    token = lexer.get_next_token()
    assert token.type == tok_type
    assert token.value == tok_val


def test_comment():
    lexer = makeLexer('{this is a comment}  \n')
    try:
        lexer.get_next_token()
    except Exception as ex:
        assert False, f"Comment test failed {ex}"

    with pytest.raises(Exception):
        lexer = makeLexer('{missing closing brace  \n')
        lexer.skip_comment()

def test_number():
    lexer = makeLexer('12345  )))')
    token = lexer.number()
    assert token.type == 'INTEGER_CONST'
    assert token.value == 12345

    lexer = makeLexer('123.45')
    token = lexer.number()
    assert token.type == 'REAL_CONST'
    assert token.value == 1.2345e+2

def test_get_next_token():
    lexer = makeLexer('  !=  ')
    token = lexer.get_next_token()
    assert token.type == NEQUAL
    lexer = makeLexer('  ==  ')
    token = lexer.get_next_token()
    assert token.type == EQUAL
    lexer = makeLexer('  <= ')
    token = lexer.get_next_token()
    assert token.type == LTE
    with pytest.raises(ValueError):
        lexer = makeLexer('  @')
        _ = lexer.get_next_token()
    assert lexer.line_count == 0
    assert lexer.line_pos == 2

if __name__ == '__main__':
    pytest.main()
