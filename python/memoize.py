class Memoize (object):
    def __init__(self, f):
        self.f = f
        self.mem = {}

    def __call__(self, *args, **kwargs):
        if (args, str(kwargs)) in self.mem:
            return self.mem[args, str(kwargs)]
        else:
            tmp = self.f(*args, **kwargs)
            self.mem[(args, str(kwargs))] = tmp
            return tmp

