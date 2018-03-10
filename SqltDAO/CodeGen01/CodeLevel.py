# Author: Soft9000.com
# 2018/03/08: Class Created

class CodeLevel:
    """ A simple class created to manage the indentations needed when generating Python source code. """

    def __init__(self, level=0, tab_str='    '):
        self.tab_str = tab_str
        self.level = level
        self.stack = []

    def push(self):
        self.stack.append(self.level)

    def pop(self):
        sz = len(self.stack)
        if sz is not 0:
            self.level = self.stack[sz - 1]
            self.stack = self.stack[0:sz-1]

    def set(self, value):
        self.level = value

    def inc(self, count=1):
        self.level += count

    def dec(self, count=1):
        self.level -= count

    def print(self, line, end='\n'):
        return str(self) + line + end

    def __str__(self):
        return self.tab_str * self.level