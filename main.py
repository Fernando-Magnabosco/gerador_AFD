
import re
import pandas as pd

# Non terminal allowed chars;
NT = "<[A-z]+>"
NTI = "<([A-z])+>"

# Terminal allowed chars;
T = "[A-z0-9&]+"

# Left and right recognizers;
REGEXES = {
    "LEFT_SIDE":    f"({NT})::",
    "RIGHT_SIDE":   "[=\\|]+\\s*" + f"({T}{NT}|{NT}{T}|{T}|{NT})",
    "TERMINAL":     "[=\\|]+\\s*" + f"({T})",
    "ISFINAL":      "^([*])"
}

class Rule:

    terminal = None
    non_terminal = None

    def __init__(self, string):

        symbols = string.split("<")

        if len(symbols) == 1:
            self.terminal = symbols[0]
        elif len(symbols) == 2:
            self.terminal = re.search(T, symbols[0]).group(0)
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
            if newRule.terminal and not newRule.non_terminal:
                self.is_final = True
            self.rules.append(newRule)
        
        

    def __str__(self):
        separator = "\t|"
        return f"{self.left} ::= {separator.join([str(rule) for rule in self.rules])}"


class Partial:

    productions = None
    alphabet = None
    alphabetNT = None

    def __init__(self, productions, alphabet, alphabetNT):
        self.productions = productions
        self.alphabet = alphabet
        self.alphabetNT = alphabetNT



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

        if re.match(REGEXES["LEFT_SIDE"], line): # It is a grammar rule;

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
            
            productions.append(Production(f"<{nextNT}", [f"{line[-1]}"]))
            nextNT += 1
    
    return Partial(productions, alphabet, noNT)

def create_AFND(Partial):
    
    
    for production in Partial.productions:
        print (production)

    
    


def AFtoCSV(AF):

    pass
    # toDF = AF.copy()
    # for i in range(len(toDF)):
    #     toDF[i][1] = " | ".join(toDF[i][1])

    # df = pd.DataFrame(AF, columns=["Left", "Right"])
    # df.to_csv("AFND.csv", index=False)

def main():

    lines = read_file("test.txt")

    AFPartial = identify_Tokens(lines)
    AFND = create_AFND(AFPartial)
    
    AFtoCSV(AFND)



main()
