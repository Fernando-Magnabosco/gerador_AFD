import pandas as pd

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

    def toCSV(self):
        df = pd.DataFrame(self.table, columns=self.partial.alphabet)

        column = []
        for production in self.partial.productions:
            string = ""
            if production.is_final:
                string += "*"
            column.append(string + production.left)

        df.insert(0, 'left', column)
        df.to_csv("./files/AFND.csv", index=False)
