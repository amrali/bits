import sys
import inspect

_line_number = None
_frame = None
def jump_to(line_number, frame):
    global _line_number, _frame
    print("Set jump to line", line_number, "in", inspect.getfile(frame))

    _frame = frame
    _line_number = line_number


def _trace(frame, event, arg):
    global _line_number, _frame

    try:
        if _line_number is not None:
            if inspect.getfile(frame) and inspect.getfile(_frame) and \
                    inspect.getfile(_frame) == inspect.getfile(frame):
                print("Jumping to line", _line_number, "in", inspect.getfile(frame))
                frame.f_lineno = _line_number
                _line_number = None

    except ValueError as e:
        print(e)

    return _trace

def install():
    sys.settrace(_trace)
    frame = sys._getframe().f_back
    while frame:
        frame.f_trace = _trace
        frame = frame.f_back
