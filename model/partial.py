from model.afnd import *
from header.regexes import *

class Partial:

    productions = None
    alphabet = None
    noNT = None

    def __init__(self, productions, alphabet, noNT):
        self.productions = productions
        self.alphabet = alphabet
        self.alphabet.add("&")
        self.noNT = noNT + 1

    def create_AFND(self):

        HAS_EPSILON = False

        table = [[[] for _ in self.alphabet] for _ in self.productions]

        for (pIndex, production) in enumerate(self.productions):
            for (sIndex, symbol) in enumerate(self.alphabet):
                for rule in production.rules:
                    if symbol == rule.terminal:
                        if rule.non_terminal != None:
                            table[pIndex][sIndex].append(rule.non_terminal)
                        if HAS_EPSILON is False and rule.non_terminal == EPSILONSTATE:
                            HAS_EPSILON = True
                            
        if HAS_EPSILON:
            table.append([[] for _ in self.alphabet])

        return AFND(table, HAS_EPSILON, self)