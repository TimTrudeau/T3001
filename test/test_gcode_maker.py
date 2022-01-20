

import gcode_maker as gm
import pytest
from gcode import linlimit, rotatlimit
from gcode_maker import GCodeMaker


def test_GCodeMaker():
    GCM = GCodeMaker()
    assert GCM.linear_limit == linlimit
    assert GCM.rotation_limit == rotatlimit

@pytest.mark.skip
def test_GCodeMaker_exception():
    with pytest.raises(ValueError):
        GCM = GCodeMaker()
        pass
    assert GCM is not None

def test_open_serial_port():
    serial = gm.open_serial_port()
    assert serial is not None





if __name__ == '__main__':
    pytest.main()

