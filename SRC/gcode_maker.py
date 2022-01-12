import os, sys
import contextlib
import serial
import gcode
from gcode import _gcodes

usable_gpio = [0, 3, 4, 13, 14, 15, 17, 18, 19, 20, 21, 22, 26]
linlimit_io = 5
rotatlimit_io = 6

try:
    import gpiozero as gpio
except Exception as e:
    print(f"No Pi GPIO {e}")
    print(f"GPIO UNAVAILABLE {e}")
    raise ImportError

global serialPort

@contextlib.contextmanager
def open_serial_port():
    if os.name == 'nt':
        port = 'COM1'
    else:
        port = '/dev/ttyUSB0'
    try:
        serialPort = _openSerialPort(port)
        print(f"Serial Port name={serialPort.name}.")
        sys.stdout.flush()
        yield serialPort
    except ValueError as ex:
        print(f"Serial Port parameter error={ex}")
        raise ValueError
    except (serial.SerialException, AttributeError) as ex:
        print(f"Serial Port not found. {ex}")
        serialPort = None
    except Exception as ex:
        print(f'{ex}')
    finally:
        serialPort.close()


def _openSerialPort(comport):
    """Opens the serial port name passed in comport. Returns the stream id"""
    #debuglog.info("Check if serial module is available in sys {}".format(sys.modules["serial"]))
    s = None
    try:
        s = serial.Serial(
            port=comport,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
    except serial.SerialException as ex:
        print(f"Failed to capture serial port: {ex}")
        raise serial.SerialException
    finally:
        return s


class GCodeMaker:
    def __init__(self):
        self.linear_limit = gcode.linlimit
        self.rotation_limit = gcode.rotatlimit

    def motorspeed(self, value, axis):
        scale = value if value <= 10 else 10
        return str(gcode.flow.get(axis) * value/scale)

    def send(self, command):
        try:
            self.serial.write(command)
        except (NameError, AttributeError):
            print(command)

    def go_home(self):
        self.send(_gcodes.get(gcode.HOME))

    def set_absolute(self):
        self.relative_mode = False
        self.send(_gcodes.get(gcode.ABSOLUTE))

    def set_relative(self):
        self.relative_mode = True
        self.send(_gcodes.get(gcode.RELATIVE))

    def move_lin(self, value, rmode=False, speed=10):
        flow = ' F' + str(self.motorspeed(speed, 'linMaxFlow'))
        self.set_relative() if rmode is True else self.set_absolute()
        self.send(_gcodes.get(gcode.MOVE_LIN) + str(value) + flow)

    def move_rot(self, value, rmode=False, speed=10):
        flow = ' F' + str(self.motorspeed(speed, 'rotMaxFlow'))
        self.set_relative() if rmode is True else self.set_absolute()
        self.send(_gcodes.get(gcode.MOVE_ROT) + str(value) + flow)

    def wait(self, value):
        self.send(_gcodes.get(gcode.WAIT) + str(value))
