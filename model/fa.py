import pandas as pd
import re
from header.defs import EPSILONSTATE, REGEXES
from model.production import Production


class FA:

    productions = None
    alphabet = None
    noNT = None
    table = None
    nextNT = 0
    HAS_EPSILON = False
    pHash: dict = dict()

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
                for production in productions:
                    if "<"+production.left+">" == leftSide:
                        raise Exception(
                            f"Production {leftSide} already exists")

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

        self.productions = productions
        self.alphabet = sorted(list(set(alphabet)))
        self.alphabet.remove("&")

        self.noNT = noNT + 1

        for (p, production) in enumerate(self.productions):
            self.pHash.update({production.left: p})

        for (p, production) in enumerate(self.productions):  # remove & transitions
            reachable = set()
            toRemove = set()
            for (r, rule) in enumerate(production.rules):
                if rule.non_terminal is not None and rule.terminal == "&":
                    reachable.add(rule.non_terminal)
                    toRemove.add(rule)

            needToRepeat = True
            while needToRepeat:
                needToRepeat = False
                addToReachable = set()
                for symbol in reachable:
                    if symbol not in self.pHash:
                        continue
                    for rule in self.productions[self.pHash[symbol]].rules:
                        if rule.non_terminal not in self.pHash \
                                or rule.non_terminal in reachable:
                            continue
                        addToReachable.add(rule.non_terminal)
                        needToRepeat = True
                reachable.update(addToReachable)

            for prod in toRemove:
                self.productions[p].rules.remove(prod)

            for prod in reachable:
                if self.productions[self.pHash[prod]].is_final:
                    self.productions[p].is_final = True
                for rule in self.productions[self.pHash[prod]].rules:
                    for prodRule in self.productions[p].rules:
                        if prodRule.non_terminal == rule.non_terminal \
                                and prodRule.terminal == rule.terminal:
                            break
                    else:
                        self.productions[p].rules.add(rule)

        self.table = [[[] for _ in self.alphabet] for _ in self.productions]

        for (p, production) in enumerate(self.productions):

            for (s, symbol) in enumerate(self.alphabet):
                for rule in production.rules:
                    if symbol == rule.terminal:
                        if rule.non_terminal is not None:
                            self.table[p][s].append(
                                rule.non_terminal)
                        if self.HAS_EPSILON is False \
                                and rule.non_terminal == EPSILONSTATE:
                            self.HAS_EPSILON = True

    def determinize(self):
        self.nextNT = len(self.productions)

        needToRepeat = True

        while needToRepeat:  # while the automata is not deterministic
            needToRepeat = False
            toMerge = set()
            for production in self.table:
                for rule in production:
                    if len(rule) >= 2:  # if the rule has more than one symbol
                        rule.sort()
                        hash = self.pHash.get(tuple(rule))
                        # if it has already been hashed, just update to the
                        # new production
                        if hash:
                            rule = hash
                        # else, add it to the list of rules to be merged
                        # into a new production
                        elif EPSILONSTATE not in rule:
                            toMerge.add(tuple(rule))
                            needToRepeat = True

            for production in toMerge:  # create the new productions

                self.pHash.update({production: self.nextNT})
                isFinal = False
                rules = set()

                for symbol in production:
                    hash = self.pHash.get(symbol)

                    if hash is None:
                        continue
                    if self.productions[hash].is_final:
                        isFinal = True
                    rules.update(self.productions[hash].rules)

                # Update the productions
                self.productions.append(Production(
                    list(production), rules, isFinal))

                # Update the table
                newRow: list = [[] for _ in self.alphabet]
                for(s, symbol) in enumerate(self.alphabet):
                    for rule in rules:
                        if symbol == rule.terminal:
                            if rule.non_terminal is not None:
                                newRow[s].append(rule.non_terminal)
                self.table.append(newRow)
                self.nextNT += 1

    def toCSV(self, filename):

        if self.HAS_EPSILON:
            self.table.append([[] for _ in self.alphabet])

        df = pd.DataFrame(self.table, columns=self.alphabet)

        column = []
        for production in self.productions:
            column.append(
                f"*{production.left}" if production.is_final
                else production.left)

        if self.HAS_EPSILON:

            column.append("*" + EPSILONSTATE)

        df.insert(0, "left", column)
        df.to_csv(f"./files/{filename}.csv", index=False)

        if self.HAS_EPSILON:
            self.table.pop()

    def __str__(self):

        string = ""
        for row in self.table:
            for col in row:
                string += ("\t") + f"{col} "
            string += "\n"
        return string
