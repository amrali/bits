import sys
import types
import queue
import goto

from contextlib import ContextDecorator, contextmanager

goto.install()

# replace `sys.excepthook` with FIFO queue of chains where when assigning to
# `sys.excepthook` adds to the queue and reading its value pops from the queue.

class EphemeralModule(types.ModuleType):

    def __init__(self):
        super().__init__('ephemeral_sys')
        sys.__sys__ = sys
        self.__excepthooks = queue.Queue()

    def __excepthook_getter(self):
        if self.__excepthooks.qsize() == 0:
            return sys.__sys__.__excepthook__
        sys.__sys__.excepthook = self.__excepthooks.get()
        return sys.__sys__.excepthook

    def __excepthook_setter(self, value):
        self.__excepthooks.put(value)
        sys.__sys__.excepthook = value

    def __getattr__(self, name):
        if name == 'excepthook':
            return self.__class__.excepthook.fget(self)
        return getattr(sys.__sys__, name)

    def __setattr__(self, name, value):
        if name == 'excepthook':
            return self.__class__.excepthook.fset(self, value)
        return setattr(sys.__sys__, name, value)

    excepthook = property(__excepthook_getter, __excepthook_setter)

class resume_on_error(ContextDecorator):
    def __enter__(self):
        return self

    def __exit__(self, e, v, tb):
        if e == NameError:
            token = v.args[0].split("'")[1]
            globals()[token] = 0
            print('worked:', token);
            goto.jump_to(tb.tb_next.tb_lineno, tb.tb_next.tb_frame)
        return True

@contextmanager
def resume_on_error():
    try:
        yield
    except NameError:
        e, v, tb = sys.exc_info()
        if e == NameError:
            token = v.args[0].split("'")[1]
            globals()[token] = 0
            print('worked:', token);
            goto.jump_to(tb.tb_next.tb_next.tb_lineno, tb.tb_next.tb_next.tb_frame)

def install():
    global sys
    sys.modules['sys'] = EphemeralModule()
    import sys

def uninstall():
    global sys
    sys.modules['sys'] = sys.__sys__
    import sys

@resume_on_error()
def main():
    #import new_language
    #new_language.install()

    print(a)
    def exch(e, v, tb):
        if e == NameError:
            token = v.args[0].split("'")[1]
            globals()[token] = 0
            print('worked:', token);
            goto.jump_to(tb.tb_next.tb_lineno + 1, tb.tb_next.tb_frame)
        sys.__excepthook__(e, v, tb)

    #sys.excepthook = exch

if __name__ == '__main__':
    main()

