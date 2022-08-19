from .rule import Rule

# This class represents a production rule of a grammar;


class Production:

    left = ""
    rules = set()
    is_final = False

    def __init__(self, left, right, is_final=False):

        if is_final:
            self.is_final = True

        self.rules = set()
        self.left = left.strip("*<>")

        rules = right
        for rule in rules:
            newRule = Rule(rule)
            if newRule.terminal and newRule.non_terminal == -1:
                self.is_final = True
            self.rules.add(newRule)

    def __str__(self):
        separator = " | "
        return f"{self.left} ::= \
            {separator.join([str(rule) for rule in self.rules])}"
