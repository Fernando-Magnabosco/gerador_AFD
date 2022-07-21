
import re
import pandas as pd


from header.regexes import *
from model.afnd import *
from model.partial import *
from model.production import *
from model.rule import *




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


def main():

    lines = read_file("test.txt")

    AFPartial = identify_Tokens(lines)
    AFND = create_AFND(AFPartial)

    AFND.toCSV()


main()
