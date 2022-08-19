import re

from model.afnd import AFND
from model.production import Production
from header.defs import REGEXES, EPSILONSTATE

# This is a partial AFND; Basically, it is an auxiliar class
# that contains the productions of a grammar, but still not
# processed to an AFND;


class Partial:

    productions = None
    alphabet = None
    noNT = None

    def __init__(self, lines):

        productions = []

        nextNT = 0
        noNT = 0

        alphabet = set()

        # processing tokens
        for line in lines:
            line = line.strip()

            if re.match(REGEXES["LEFT_SIDE"], line):  # It is a grammar rule;

                leftSide = re.search(REGEXES["LEFT_SIDE"], line).group(1)
                rightSide = re.findall(REGEXES["RIGHT_SIDE"], line)
                alphabet.update(re.findall(REGEXES["TERMINAL"], line))

                productions.append(Production(leftSide, rightSide))
                noNT += 1
            else:                                    # It is a token;
                for char in line[:-1]:
                    if char == "\n":
                        continue
                    leftSide = f"<{nextNT}>"
                    rightSide = [f"{char}<{nextNT + 1}>"]
                    productions.append(Production(leftSide, rightSide))

                    nextNT += 1
                    noNT += 1
                    alphabet.add(char)

                productions.append(Production(
                    f"<{nextNT}", [f"{line[-1]}"], True))
                alphabet.add(line[-1])
                nextNT += 1

        self.productions = productions
        self.alphabet = alphabet
        self.noNT = noNT + 1
        self.alphabet.add("&")

    def create_AFND(self):

        HAS_EPSILON = False

        table = [[[] for _ in self.alphabet] for _ in self.productions]

        for (pIndex, production) in enumerate(self.productions):
            for (sIndex, symbol) in enumerate(self.alphabet):
                for rule in production.rules:
                    if symbol == rule.terminal:
                        if rule.non_terminal is not None:
                            table[pIndex][sIndex].append(rule.non_terminal)
                        if HAS_EPSILON is False \
                                and rule.non_terminal == EPSILONSTATE:
                            HAS_EPSILON = True

        if HAS_EPSILON:
            table.append([[] for _ in self.alphabet])

        return AFND(table, HAS_EPSILON, self)
