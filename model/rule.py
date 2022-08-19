from header.defs import EPSILONSTATE, T
import re

# This class represents a string of a grammar;
# Note that the class name is not string, but "Rule"
# by lack of a better name, as string is a keyword in Python;


class Rule:

    terminal = None
    non_terminal = None

    def __init__(self, string):

        string = string.strip()
        symbols = string.split("<")

        # if it has only a symbol after split("<"), then it is a terminal
        if len(symbols) == 1:
            self.terminal = symbols[0]
            if self.terminal != "&":
                self.non_terminal = EPSILONSTATE

        # if the split returns an array with two elements,
        #  we have a non-terminal
        elif len(symbols) == 2:

            # though, if the first element is empty, then we have a rule
            # with only a non_terminal (e.g. <A>)
            if symbols[0] != "":  # terminal and non_terminal
                self.terminal = re.search(T, symbols[0]).group(0)
                self.non_terminal = symbols[1].replace(">", "")
            # else we have a complete rule (e.g. a<A>)
            else:
                self.terminal = "&"
                self.non_terminal = symbols[1].replace(">", "")

    def __str__(self):

        if self.non_terminal:
            return f"{self.terminal}<{self.non_terminal}>"
        else:
            return self.terminal
