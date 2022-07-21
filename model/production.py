from .rule import Rule

class Production:

    left = ""
    rules = []
    is_final = False

    def __init__(self, left, right, is_final=False):

        if is_final:
            self.is_final = True

        self.rules = []
        self.left = left.strip("*<>")

        rules = right
        for rule in rules:
            newRule = Rule(rule)
            if newRule.terminal and newRule.non_terminal == -1:
                self.is_final = True
            self.rules.append(newRule)

    def __str__(self):
        separator = " | "
        return f"{self.left} ::= {separator.join([str(rule) for rule in self.rules])}"