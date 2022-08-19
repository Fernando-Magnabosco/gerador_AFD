from model.ndfa import NDFA


def read_file(file):

    with open(file, "r") as f:
        lines = f.readlines()
    return lines


def main():

    lines = read_file("./files/test.txt")

    afnd = NDFA(lines)
    print(afnd)
    afnd.toCSV()
    # AFPartial.determinize()


main()
