import re

from model.fa import FA
from model.production import Production
from header.defs import REGEXES, EPSILONSTATE

# This class represents a non deterministic finite automata;


class NDFA(FA):

    def __init__(self, lines):

        productions = []

        self.nextNT = 0
        noNT = 0

        alphabet = list()

        # processing tokens
        for line in lines:
            line = line.strip()

            if re.match(REGEXES["LEFT_SIDE"], line):  # It is a grammar rule;

                leftSide = re.search(REGEXES["LEFT_SIDE"], line).group(1)
                rightSide = re.findall(REGEXES["RIGHT_SIDE"], line)
                alphabet.extend(re.findall(REGEXES["TERMINAL"], line))

                productions.append(Production(leftSide, rightSide))
                noNT += 1
            else:                                    # It is a token;
                for char in line[:-1]:
                    if char == "\n":
                        continue
                    leftSide = f"<{self.nextNT}>"
                    rightSide = [f"{char}<{self.nextNT + 1}>"]
                    productions.append(Production(leftSide, rightSide))

                    self.nextNT += 1
                    noNT += 1
                    alphabet.append(char)

                productions.append(Production(
                    f"<{self.nextNT}", [f"{line[-1]}"]))
                alphabet.append(line[-1])
                self.nextNT += 1

        alphabet.append("&")
        self.productions = productions
        self.alphabet = sorted(list(set(alphabet)))

        self.noNT = noNT + 1

        self.table = [[[] for _ in self.alphabet] for _ in self.productions]

        for (p, production) in enumerate(self.productions):
            self.pHash.update({production.left: p})
            for (s, symbol) in enumerate(self.alphabet):
                for rule in production.rules:
                    if symbol == rule.terminal:
                        if rule.non_terminal is not None:
                            self.table[p][s].append(
                                rule.non_terminal)
                        if self.HAS_EPSILON is False \
                                and rule.non_terminal == EPSILONSTATE:
                            self.HAS_EPSILON = True


