
import re
from numpy import product
import pandas as pd

# Non terminal allowed chars;
NT = "<[A-z]+>"
NTI = "<([A-z])+>"

# Terminal allowed chars;
T = "[A-z0-9&]+"

# Left and right recognizers;
REGEXES = {
    "LEFT_SIDE":    f"({NT})::",
    "RIGHT_SIDE":   "[=\\|]+\\s*" + f"({T}{NT}|{T}|{NT})",
    "TERMINAL":     "[=\\|]+\\s*" + f"({T})",
    "ISFINAL":      "^([*])"
}

EPSILONSTATE = -1


class Rule:

    terminal = ""
    non_terminal = ""

    def __init__(self, string):

        string = string.strip()
        symbols = string.split("<")

        if len(symbols) == 1:
            self.terminal = symbols[0]
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
            print(newRule)
            if newRule.terminal and newRule.non_terminal == -1:
                self.is_final = True
            self.rules.append(newRule)

    def __str__(self):
        separator = " | "
        return f"{self.left} ::= {separator.join([str(rule) for rule in self.rules])}"


class Partial:

    productions = None
    alphabet = None
    noNT = None

    def __init__(self, productions, alphabet, noNT):
        self.productions = productions
        self.alphabet = alphabet
        alphabet.add("&")
        self.noNT = noNT + 1


class AFND:

    table = None
    partial = None

    def __init__(self, table, partial):
        self.table = table
        self.partial = partial

    def __str__(self):

        string = ""
        for row in self.table:
            for col in row:
                string += ("\t") + f"{col} "
            string += "\n"
        return string


def read_file(file):

    with open(file, "r") as f:
        lines = f.readlines()
    return lines


def identify_Tokens(lines):

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
            thisAlphabet = re.findall(REGEXES["TERMINAL"], line)
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

            productions.append(Production(f"<{nextNT}", [f"{line[-1]}"], True))
            alphabet.add(line[-1])
            nextNT += 1

    return Partial(productions, alphabet, noNT)


def create_AFND(Partial):

    table = [[[] for _ in Partial.alphabet] for _ in Partial.productions]

    for (pIndex, production) in enumerate(Partial.productions):
        for (sIndex, symbol) in enumerate(Partial.alphabet):
            for rule in production.rules:
                if symbol == rule.terminal:
                    if rule.non_terminal:
                        table[pIndex][sIndex].append(rule.non_terminal)
                    else:
                        table[pIndex][sIndex].append(EPSILONSTATE)

    return AFND(table, Partial)


def AFtoCSV(AF):

    df = pd.DataFrame(AF.table, columns=AF.partial.alphabet)

    column = []
    for production in AF.partial.productions:
        string = ""
        if production.is_final:
            string += "*"
        column.append(string + production.left)

    df.insert(0, 'left', column)
    df.to_csv("AFND.csv", index=False)


def main():

    lines = read_file("test.txt")

    AFPartial = identify_Tokens(lines)
    AFND = create_AFND(AFPartial)

    AFtoCSV(AFND)


main()
