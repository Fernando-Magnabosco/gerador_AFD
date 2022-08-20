import pandas as pd
from header.defs import EPSILONSTATE


class FA:

    productions = None
    alphabet = None
    noNT = None
    table = None
    nextNT = 0
    HAS_EPSILON = False
    pHash: dict = dict()

    def toCSV(self, filename):

        if self.HAS_EPSILON:
            self.table.append([[] for _ in self.alphabet])

        df = pd.DataFrame(self.table, columns=self.alphabet)

        column = []
        for production in self.productions:
            string = ""
            if production.is_final:
                string += "*"
            column.append(string + production.left)

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
