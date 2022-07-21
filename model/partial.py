class Partial:

    productions = None
    alphabet = None
    noNT = None

    def __init__(self, productions, alphabet, noNT):
        self.productions = productions
        self.alphabet = alphabet
        alphabet.add("&")
        self.noNT = noNT + 1