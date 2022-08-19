import re
import pandas as pd

from model.production import Production
from header.defs import REGEXES, EPSILONSTATE

# This class represents a non deterministic finite automata;


class NDFA:

    productions = None
    alphabet = None
    noNT = None
    table = None
    HAS_EPSILON = False

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

        self.table = [[[] for _ in self.alphabet] for _ in self.productions]

        for (pIndex, production) in enumerate(self.productions):
            for (sIndex, symbol) in enumerate(self.alphabet):
                for rule in production.rules:
                    if symbol == rule.terminal:
                        if rule.non_terminal is not None:
                            self.table[pIndex][sIndex].append(
                                rule.non_terminal)
                        if self.HAS_EPSILON is False \
                                and rule.non_terminal == EPSILONSTATE:
                            self.HAS_EPSILON = True

        if self.HAS_EPSILON:
            self.table.append([[] for _ in self.alphabet])

    def toCSV(self):
        df = pd.DataFrame(self.table, columns=self.alphabet)

        column = []
        for production in self.productions:
            string = ""
            if production.is_final:
                string += "*"
            column.append(string + production.left)

        if self.HAS_EPSILON:
            column.append(str(EPSILONSTATE) + "*")

        df.insert(0, "left", column)
        df.to_csv("./files/AFND.csv", index=False)

    def __str__(self):

        string = ""
        for row in self.table:
            for col in row:
                string += ("\t") + f"{col} "
            string += "\n"
        return string
