from imp import new_module
from code import InteractiveConsole

class Console(InteractiveConsole):

    def __init__(self, names=None):
        self.superspace = new_module('superspace')
        names = names or {}
        names['console'] = self
        names['superspace'] = self.superspace
        super().__init__(names)

    def enter(self, source):
        self.runcode(source)

cnsl = Console()
cnsl.interact()
print(cnsl.superspace.a)
