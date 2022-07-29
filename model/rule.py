from header.regexes import *
import re

class Rule:

    terminal = None
    non_terminal = None

    def __init__(self, string):

        string = string.strip()
        symbols = string.split("<")

        if len(symbols) == 1:
            self.terminal = symbols[0]
            if self.terminal != "&":
                self.non_terminal = EPSILONSTATE
        elif len(symbols) == 2:
            if symbols[0] != "":
                self.terminal = re.search(T, symbols[0]).group(0)
                self.non_terminal = symbols[1].replace(">", "")
            else:
                self.terminal = "&"
                self.non_terminal = symbols[1].replace(">", "")

    def __str__(self):

        if self.non_terminal:
            return f"{self.terminal}<{self.non_terminal}>"
        else:
            return self.terminal