from header.defs import EPSILONSTATE
from .rule import Rule

# This class represents a production rule of a grammar;


class Production:

    left = ""
    rules: set = set()
    is_final = False

    def __init__(self, left, right, is_final=False):

        if is_final:
            self.is_final = True

        if type(left) is list:
            self.left = str(left)
        else:
            self.left = left.strip("*<>")
        if type(right) is set:
            self.rules = right
        else:
            self.rules = set()

            rules = right
            for rule in rules:
                newRule = Rule(rule)
                print(newRule.terminal, newRule.non_terminal)
                if (newRule.terminal and newRule.non_terminal == EPSILONSTATE)\
                        or newRule.non_terminal is None:
                    self.is_final = True
                self.rules.add(newRule)

    def __str__(self):
        separator = " | "
        return f"{self.left} ::= \
            {separator.join([str(rule) for rule in self.rules])}"
