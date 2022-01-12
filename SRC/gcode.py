linlimit = 300
rotatlimit = 360
flow = {'linMaxFlow': 1300, 'rotMaxFlow': 9000}


HOME     = 'HOME'
ABSOLUTE = 'ABSOLUTE'
RELATIVE = 'RELATIVE'
MOVE_LIN = 'MOVE_LIN'
MOVE_ROT = 'MOVE_ROT'
WAIT     = 'WAIT'

_gcodes = {
    HOME:     'G28 X,Z',
    ABSOLUTE: 'G90',
    RELATIVE: 'G91',
    MOVE_LIN: 'G1 X',
    MOVE_ROT: 'G1 Z',
    WAIT:     'G4 ',
}