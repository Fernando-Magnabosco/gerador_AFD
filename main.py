from model.ndfa import NDFA
from model.dfa import DFA


def read_file(file):

    with open(file, "r") as f:
        lines = f.readlines()
    return lines


def main():

    lines = read_file("./files/test.txt")

    afnd = NDFA(lines)

    afd = DFA(afnd)

    afnd.toCSV("afnd")
    afd.toCSV("afd")


if __name__ == "__main__":
    main()
