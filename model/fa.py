import pandas as pd
import re
from header.defs import EPSILONSTATE, REGEXES
from model.production import Production
from model.rule import Rule


class FA:

    def __init__(self, lines):

        self.productions = []
        self.pMap = dict()
        self.nextP = 1
        self.alphabet = list()

        self.pMap["S"] = 0

        # finding initial production
        for line in lines:
            line = line.strip()

            if re.search(REGEXES["LEFT_SIDE"], line).group(1) == "<S>":
                break
        else:
            raise Exception("No start symbol found")

        rightSide = re.findall(REGEXES["RIGHT_SIDE"], line)
        self.initial = Production(0, rightSide)
        for rule in self.initial.rules:
            if rule.non_terminal is not None and \
                    not self.pMap.get(rule.non_terminal):

                self.pMap[rule.non_terminal] = self.nextP
                self.productions.append(Production(self.nextP, {}))
                self.nextP += 1
            rule.non_terminal = self.pMap.get(rule.non_terminal)
        self.productions.append(self.initial)
        for line in lines:
            line = line.strip()

            if re.match(REGEXES["LEFT_SIDE"], line):

                left = re.search(REGEXES["LEFT_SIDE"],
                                 line).group(1).strip("<>")
                if left == "S":
                    continue

                rightSide = re.findall(REGEXES["RIGHT_SIDE"], line)

                self.alphabet.extend(re.findall(REGEXES["TERMINAL"], line))

                if self.pMap.get(left) is None:
                    self.pMap[left] = self.nextP
                    self.nextP += 1
                    lastProduction = Production(self.pMap[left], rightSide)
                    self.productions.append(lastProduction)
                else:

<<<<<<< HEAD
                    for production in self.productions:
                        if production.left == self.pMap[left]:

                            lastProduction = production
                            lastProduction.addRules(rightSide)
                            break
                    else:
                        lastProduction = Production(self.pMap[left], rightSide)
                        self.productions.append(lastProduction)

                for rule in lastProduction.rules:

                    if rule.non_terminal is not None and \
                            self.pMap.get(rule.non_terminal) is None:

                        self.pMap[rule.non_terminal] = self.nextP
                        self.productions.append(Production(self.nextP, {}))
                        self.nextP += 1
                    rule.non_terminal = self.pMap.get(rule.non_terminal)

            else:
                rule = Rule(f"{line[0]}<{self.nextP}>")
                rule.non_terminal = self.nextP
                self.initial.addRules({rule})
                self.alphabet.append(line[0])
                for char in line[1:]:
                    rule = Rule(f"{char}<{self.nextP + 1}>")
                    rule.non_terminal = int(rule.non_terminal)
                    self.productions.append(Production(self.nextP, {rule}))
                    self.pMap[self.nextP] = self.nextP
                    self.nextP += 1
                    self.alphabet.append(char)

                self.productions.append(Production(
                    self.nextP, {}, True))
                self.pMap[self.nextP] = self.nextP
                self.nextP += 1

        self.productions.sort(key=lambda x: x.left)
        if(self.pMap.get("eps") is not None):
            self.productions[self.pMap["eps"]].is_final = True

        self.alphabet = sorted(list(set(self.alphabet)))
=======
        self.productions = productions
        self.alphabet = sorted(list(set(alphabet)))
        self.alphabet.remove("&")

        self.noNT = noNT + 1
>>>>>>> 049bc75d1894da5000485994cbd8fc782800fdcb

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
<<<<<<< HEAD
=======

>>>>>>> 049bc75d1894da5000485994cbd8fc782800fdcb
            for (s, symbol) in enumerate(self.alphabet):
                for rule in production.rules:
                    if symbol == rule.terminal:
                        if rule.non_terminal is not None:
                            self.table[p][s].append(
                                rule.non_terminal)
<<<<<<< HEAD
=======
                        if self.HAS_EPSILON is False \
                                and rule.non_terminal == EPSILONSTATE:
                            self.HAS_EPSILON = True
>>>>>>> 049bc75d1894da5000485994cbd8fc782800fdcb

    def determinize(self):

        needToRepeat = True

        while needToRepeat:  # while the automata is not deterministic
            needToRepeat = False
            toMerge = set()
            for production in self.table:
                for rule in production:
                    if len(rule) >= 2:  # if the rule has more than one symbol
                        rule.sort()
                        hash = self.pMap.get(tuple(rule))
                        # if it has already been hashed, just update to the
                        # new production
                        if hash:
                            rule = hash
                        # else, add it to the list of rules to be merged
                        # into a new production
                        elif EPSILONSTATE not in rule:
                            for p in self.productions:
                                if(list(set(p.left)) == rule):
                                    break
                                if p.left == str(list(set(rule))):
                                    break
                            else:
                                toMerge.add(tuple(rule))
                                needToRepeat = True

            for production in toMerge:  # create the new productions
<<<<<<< HEAD

                self.pMap.update({production: self.nextP})
=======
                self.pHash.update({production: self.nextNT})

>>>>>>> 049bc75d1894da5000485994cbd8fc782800fdcb
                isFinal = False
                rules = set()

                for symbol in production:
                    if self.productions[symbol].is_final:
                        isFinal = True
                    rules.update(self.productions[symbol].rules)

                # Update the productions
                self.productions.append(Production(
                    list(set(production)), rules, isFinal))

                # Update the table
                newRow: list = [[] for _ in self.alphabet]
                for(s, symbol) in enumerate(self.alphabet):
                    for rule in rules:
                        if symbol == rule.terminal:
                            if rule.non_terminal is not None:
                                newRow[s].append(rule.non_terminal)
                self.table.append(newRow)
                self.nextP += 1

    def removeEpsilon(self):
        for (p, production) in enumerate(self.table):
            reachable = set()
            if not len(production[0]):
                continue

            for symbol in production[0]:
                reachable.add(symbol)

            needToRepeat = True
            while needToRepeat:
                needToRepeat = False
                addToReachable = set()
                for symbol in reachable:
                    for rule in self.table[int(symbol)]:
                        if len(rule):
                            for rsymbol in rule:

                                if rsymbol in reachable:
                                    continue
                                addToReachable.add(rsymbol)
                                needToRepeat = True
                reachable.update(addToReachable)
            print(reachable)
            for prod in reachable:
                if self.productions[prod].is_final:
                    self.productions[p].is_final = True
                self.productions[p].addRules(
                    self.productions[prod].rules)

    def toCSV(self, filename):

        df = pd.DataFrame(self.table, columns=self.alphabet)

        column = []
        for production in self.productions:
            column.append(
                f"*{production.left}" if production.is_final
                else production.left)

        df.insert(0, "left", column)
        df.to_csv(f"./files/{filename}.csv", index=False)

    def __str__(self):
        string = ""
        for production in self.productions:
            string += "* " if production.is_final else "  "
            string += str(production) + "\n"
        return string
