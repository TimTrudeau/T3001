# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis

# RESERVED WORDS
PROGRAM       = 'PROGRAM'
BEGIN         = 'BEGIN'
END           = 'END'
VAR           = 'VAR'
IO            = 'IO'
WAYPOINT      = 'WAYPOINT'
TRUE          = 'TRUE'
FALSE         = 'FALSE'
IF            = 'IF'
THEN          = 'THEN'
ELSE          = 'ELSE'
ENDIF         = 'ENDIF'
LOOP          = 'LOOP'
UNTIL         = 'UNTIL'
WAIT          = 'WAIT'
MOVETO        = 'MOVETO'
ROTATE        = 'ROTATE'
HOME          = 'HOME'
STOP          = 'STOP'

#VAR TYPES
ID            = 'ID'
INTEGER       = 'INTEGER'
BOOL          = 'BOOL'
REAL          = 'REAL'
INTEGER_CONST = 'INTEGER_CONST'
BOOL_CONST    = 'BOOL_CONST'
REAL_CONST    = 'REAL_CONST'
PININ         = 'PININ'
PINOUT        = 'PINOUT'
WAYPOINT      = 'WAYPOINT'

# OPERATORS
PLUS          = 'PLUS'
MINUS         = 'MINUS'
MUL           = 'MUL'
INTEGER_DIV   = 'INTEGER_DIV'
FLOAT_DIV     = 'FLOAT_DIV'
LTE           = 'LTE'
LT            = 'LT'
GTE           = 'GTE'
GT            = 'GT'
LPAREN        = 'LPAREN'
RPAREN        = 'RPAREN'
ASSIGN        = 'ASSIGN'
EQUAL         = 'EQUAL'
NEQUAL        = 'NEQUAL'
STEP          = 'STEP'

# SYNTAX SYMBOLS
SEMI          = 'SEMI'
DOT           = 'DOT'
COLON         = 'COLON'
COMMA         = 'COMMA'
EOF           = 'EOF'
