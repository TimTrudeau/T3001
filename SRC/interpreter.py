""" Interpreter for CLIQ key tester robot"""

###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################
from __init__ import logger
from token_types import *
from parser import Parser
from lexer import Lexer
from gcode_maker import GCodeMaker
from gcode_maker import open_serial_port

import time


class NodeVisitor(object):
    def __init__(self):
        logger.info("STARTING LOG")

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        try:
            logger.info(f'method name {method_name} attr {node.__dict__.keys()}')
        except Exception:
            logger.info(f'method name {method_name}')
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        NodeVisitor.__init__(self)
        self.gcode = GCodeMaker()
        self.parser = parser
        self.GLOBAL_SCOPE = {}
        self.declaredDict = {}
        self.waypointDict = {}
        self.io_Dict = {}

    def getType(self, node):
        """Recursive call to find terminal node.
        Not used.
        """
        if hasattr(node, 'right'):
            return self.getType(node.right)
        if hasattr(node, 'expr'):
            return self.getType(node.expr)
        if hasattr(node.token, 'type_'):
            return node.token.type
        else:
            return None

    # def handleTypeConversion(self, lName, lType, rValue):
    """ This code is used if type conversion is allowed."""
    #     if type(rValue).__name__ == float:
    #         rType = REAL
    #     elif type(rValue).__name__ == bool:
    #         rType = BOOL
    #     elif type(rValue).__name__ == int:
    #         rType = INTEGER
    #     else:
    #         raise ValueError(f'Unknown rValue type {type(rValue).__name__}')
    #     self.declaredDict[lName] = rType

    def handleTypeConversion(self, lType, rValue):
        """ This code is be used if type conversion is NOT allowed."""
        import math
        if lType == INTEGER:
            rValue = math.trunc(rValue)
        elif lType == REAL:
            rValue = float(rValue)
        elif lType == BOOL:
            rValue = False if rValue == 0 else True
        else:
            raise TypeError(f'Illegal lValue type {lType}')
        return rValue

    def visit_Program(self, node):
        self.declarations = node.block.declarations
        self.waypointDict = node.block.waypoint_list
        self.io_Dict = node.block.io_list
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        for declaration in node.io_list:
            self.visit(declaration)
        for declaration in node.waypoint_list:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        self.declaredDict[node.var_node.value] = node.type_node.value

    def visit_IO_(self,node):
        # TODO add IO functionality
        pass

    def visit_Type(self, node):
        pass

    def visit_BinOp(self, node):
        try:
            rightvalue = self.visit(node.right)
            leftvalue = self.visit(node.left)

            if node.op.type == PLUS:
                return (leftvalue + rightvalue)
            elif node.op.type == MINUS:
                return (leftvalue - rightvalue)
            elif node.op.type == MUL:
                return (leftvalue * rightvalue)
            elif node.op.type == INTEGER_DIV:
                return (leftvalue // rightvalue)
            elif node.op.type == FLOAT_DIV:
                return float(leftvalue) / float(rightvalue)
            elif node.op.type == EQUAL:
                return (leftvalue == rightvalue)
            elif node.op.type == LT:
                return (leftvalue < rightvalue)
            elif node.op.type == GT:
                return (leftvalue > rightvalue)
            elif node.op.type == LTE:
                return (leftvalue <= rightvalue)
            elif node.op.type == GTE:
                return (leftvalue >= rightvalue)
            elif node.op.type == NEQUAL:
                return (leftvalue != rightvalue)
            else:
                return False
        except Exception as e:
            print(e)
            raise e

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        if hasattr(node, 'children'):
            for child in node.children:
                self.visit(child)

    def visit_Assign(self, node):
        lVarName = node.left.value
        try:
            lType = self.declaredDict[lVarName]  # test var has been declared
        except KeyError:
            raise Exception(f"Variable {lVarName} not declared")
        rvalue = self.visit(node.right)
        rvalue = self.handleTypeConversion(lType, rvalue)
        self.GLOBAL_SCOPE[lVarName] = rvalue

    def visit_Bool(self, node):
        value = node.value
        return value

    def visit_Var(self, node):
        var_name = node.value
        var_value = self.GLOBAL_SCOPE.get(var_name)
        if var_value is None:
            raise NameError(f'{repr(var_name)} is not in the GLOBAL Table.')
        else:
            return var_value

    def visit_Waypoint(self, node):
        self.GLOBAL_SCOPE[node.value] = node.point

    def visit_NoOp(self, node):
        pass

    def visit_IfNode(self, node):
        if self.visit(node.logicNode) is True:
            self.visit(node.true)
        else:
            self.visit(node.false)

    def visit_Loop(self, node):
        while True:
            self.visit(node.statements)
            if self.visit(node.logicNode) is True:
                break

    def visit_Wait(self, node):
        pause = self.visit(node.token.value)
        # TODO Use GPIO delay
        self.gcode.wait(pause)
        return pause

    def visit_Moveto(self, node):
        distance = node.value['distance']
        angle = node.value['angle']
        if type(distance).__name__ == 'Var':
            waypoint = self.visit(distance)
            distance = waypoint.get('distance')
            angle = waypoint.get('angle')
        relative = False if type(distance).__name__ == 'Num' else True
        self.gcode.move_lin(self.visit(distance), relative)
        relative = False if type(angle).__name__ == 'Num' else True
        self.gcode.move_rot(self.visit(angle), relative)

    def visit_Turn(self, node):
        move = self.visit(node.moveTo)
        self.gcode.send(move)

    def visit_Home(self, node):
        self.gcode.go_home()
        # self.gcode.send(0, 0)
        # self.gcode.send('RELATIVE')
        # while self.gcode.input(self.gcode.linear_limit) is False:
        #     self.gcode.send(-1, 0)
        # self.gcode.send('ABSOLUTE')

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        # TODO test the tree.GLOBAL_SCOPE and tree.declarations agree
        return self.visit(tree)

