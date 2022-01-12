import pytest
from token_types import *
from lexer import Token

def makeProgramSyntax(intAssign='345', realAssign='2.22', boolAssign='TRUE', syntax=None, breakcode=None):
    testcode = \
        f"""PROGRAM Test;
            VAR
                turned: BOOL;
                aa : INTEGER;
                BB, x : REAL;
                cc : INTEGER;
            BEGIN
                aa := {intAssign};
                BB := {realAssign};
                turned := {boolAssign};
                MOVETO -10, 200;
                cc := 1;
                IF turned == TRUE:
                    cc := 100;
                ENDIF;
            END.
         """
    if breakcode is not None:
        brokecode = testcode.replace(syntax, breakcode, 1)
        return brokecode
    else:
        return testcode


def makeInterpreter(aprogram):
    from interpreter import Lexer, Parser, Interpreter
    lexer = Lexer(aprogram)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    return interpreter


Wait_expressions = [
    ('WAIT  6 + 3;\n', 6 + 3),
    ('WAIT  5;\n', 5),
    ('WAIT  1.5;\n', 1.5),
    ('WAIT  1 - 1;\n', 1 - 1),
    ('WAIT  1.5 * 2;\n', 1.5 * 2),
    ('WAIT  4 / 2;\n', 4 / 2),
]


@pytest.mark.parametrize("expr, answer", Wait_expressions)
def test_parse_wait(expr, answer):
    interpreter = makeInterpreter(expr)
    node = interpreter.parser.wait_statement()
    results = interpreter.visit(node)
    assert node.token.type == WAIT
    assert results == answer
    pass


arithmetic_expressions = [
    ('5.5 - - - + - (3 + 4) - +2', 10),
    ('- 3', -3),
    ('14 + 2 * 3 - 6 DIV 2', 17),
    ('2 + 7 * 5', 37),
    ('3+1', 4),
    ('7 - 8 DIV 4', 5),
    ('7 + 3 * (10 DIV (12 DIV (3 + 1) - 1))', 22),
    ('7 + 3 * (10 DIV (12 DIV (3 + 1) - 1)) DIV (2 + 3) - 5 - 3 + (8)', 10),
    ('7 + (((3 + 2)))', 12),
    ('+ 3', 3),
    ('5 - - - + - 3', 8),
    ('-5 + 5', 0),
    ('5/2', 2),
    ('5 DIV 2', 2),
]


@pytest.mark.parametrize("expr, result", arithmetic_expressions)
def test_integer_arithmetic_expressions(expr, result):
    progText = makeProgramSyntax(intAssign=expr)
    interpreter = makeInterpreter(progText)
    interpreter.interpret()
    id_table = interpreter.GLOBAL_SCOPE
    assert id_table['aa'] == result


float_expressions = [
    ('100', 100.00),
    ('3.14', 3.14),
    ('2.14 + 7 * 5', 37.14),
    ('(2.14 + 7) * 5', 45.7),
    ('7.14 - 8 / 4', 5.14),
    ('(7.14 - 8) / 4', -0.215),
    ('-3.14', -3.14),
    ('5/2', 2.5),
    ('5 DIV 2', 2),
]


@pytest.mark.parametrize("expr, result", float_expressions)
def test_float_arithmetic_expressions(expr, result):
    progText = makeProgramSyntax(realAssign=expr)
    interpreter = makeInterpreter(progText)
    interpreter.interpret()
    id_table = interpreter.GLOBAL_SCOPE
    assert (id_table['BB']) == pytest.approx(result)


bool_expressions = [
    ('3 > 2', True),
    ('2 > 3', False),
    ('2 < 3', True),
    ('3 < 2', False),
    ('3 >= 2', True),
    ('3 >= 3', True),
    ('2 <= 3', True),
    ('3 <= 2', False),
    ('3 == 3', True),
    ('3 == 2', False),
    ('3 != 2', True),
    ('3 != 3', False),
]


@pytest.mark.parametrize("expr, result", bool_expressions)
def test_bool_expressions(expr, result):
    progText = makeProgramSyntax(boolAssign=expr)
    interpreter = makeInterpreter(progText)
    interpreter.interpret()
    id_table = interpreter.GLOBAL_SCOPE
    assert id_table['turned'] == result


bad_syntax = [
    ('VAR', 'var'),  # lower case keyword
    ('VAR', 'VAR:'),  # invalid colon
    (':=', '='),  # invalid assignment operator
    ('cc : INTEGER;', 'cc  INTEGER;'),  # missing colon
    ('cc : INTEGER;', 'cc : INTEGER'),  # missing semicolon
    ('INTEGER', 'INTIGER'),  # misspelled keyword
    ('END.', 'END')  # missing dot
]


@pytest.mark.parametrize("expr, repl", bad_syntax)
def test_expression_invalid_syntax_01(expr, repl):
    progText = makeProgramSyntax(syntax=expr, breakcode=repl)
    interpreter = makeInterpreter(progText)
    with pytest.raises(Exception):
        interpreter.interpret()


# "TODO These should be caught by the interpreter"
bad_expr = [
    #('aa := 345;', 'aa := 3.14;'),  #assign float to int. This is legal!
    ('aa := 345;', 'aa := "string";'),  # Does not support strings
    ('cc := 1;', 'cc := 1 (2+3);'),  # missing operator
    ('345;', '345'),  # missing semicolon
    ('aa', 'xx'),  # assign to an undeclared var
]


@pytest.mark.parametrize("expr, repl", bad_expr)
def test_expression_invalid_syntax_02(expr, repl):
    progText = makeProgramSyntax(syntax=expr, breakcode=repl)
    interpreter = makeInterpreter(progText)
    with pytest.raises(Exception):
        interpreter.interpret()


def test_program():
    text = """\
PROGRAM Full;
VAR
   number     : INTEGER;
   a, b, c    : INTEGER;
   y, x       : REAL;
   
IO
    limit   : PININ 6;

WAYPOINT
    approach := 250, -90;
    pullout := -10, -20;
    
BEGIN {Part10}
{ Test of comment }
    HOME;
    MOVETO  +3.6, 240;   
    number := 5;
    a := (number + 11) / 2;
    b := (10 * a) + (11 * number) DIV 4;
    IF 3 == 3:
        c := a;
    ELSE:
        c := 1;
    ENDIF;
    MOVETO pullout;
    LOOP:
        number := number + 1;
        WAIT 0.5;
        MOVETO approach;
    UNTIL number > 10;  
    x := 11 / 2;
    y := 20 / 7 + 3.14;
END.  {Part10}
"""

    interpreter = makeInterpreter(text)
    interpreter.interpret()

    globals = interpreter.GLOBAL_SCOPE
    assert len(globals.keys()) == 8
    assert 'approach' in globals.keys()
    assert 'pullout' in globals.keys()
    assert globals['number'] == 11
    assert globals['a'] == 8
    assert globals['b'] == 93
    assert globals['c'] == globals['a']
    assert globals['x'] == 5.5
    pytest.approx(globals['y'], pytest.approx(20.0 / 7 + 3.14))  # 5.9971...


if __name__ == '__main__':
    pytest.main()

