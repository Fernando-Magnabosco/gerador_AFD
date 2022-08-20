

from model.fa import FA
from model.ndfa import NDFA
from model.production import Production


class DFA(FA):

    def __init__(self, ndfa: NDFA):

        self.productions = ndfa.productions.copy()
        self.alphabet = ndfa.alphabet.copy()
        self.noNT = ndfa.noNT
        self.table = ndfa.table.copy()
        self.nextNT = len(self.productions)
        self.HAS_EPSILON = ndfa.HAS_EPSILON
        self.pHash = ndfa.pHash.copy()

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
                        else:
                            toMerge.add(tuple(rule))
                            needToRepeat = True

            for production in toMerge:  # create the new productions
                self.pHash.update({production: self.nextNT})
                isFinal = False
                rules = set()

                for symbol in production:
                    hash = self.pHash.get(symbol)
                    if not hash:
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
