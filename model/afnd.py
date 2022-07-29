import pandas as pd

from header.regexes import EPSILONSTATE

class AFND:

    HAS_EPSILON = None
    table = None
    partial = None

    def __init__(self, table, hasEpsilon, partial):
        self.HAS_EPSILON = hasEpsilon
        self.table = table
        self.partial = partial

    def __str__(self):

        string = ""
        for row in self.table:
            for col in row:
                string += ("\t") + f"{col} "
            string += "\n"
        return string

    def determinize(self):
        
        for row in self.table:
            for col in row:
                if len(col) >= 2:
                    print(col)
                


    def toCSV(self):
        df = pd.DataFrame(self.table, columns=self.partial.alphabet)
        
        column = []
        for production in self.partial.productions:
            string = ""
            if production.is_final:
                string += "*"
            column.append(string + production.left)

        if self.HAS_EPSILON:
            column.append(str(EPSILONSTATE) + "*")
        

        df.insert(0, "left", column)
        df.to_csv("./files/AFND.csv", index=False)
