from model.fa import FA


def read_file(file):

    with open(file, "r") as f:
        lines = f.readlines()
    return lines


def main():

    lines = read_file("./files/test.txt")

    fa = FA(lines)
    fa.toCSV("afnd")
    fa.determinize()
    fa.toCSV("afd")


if __name__ == "__main__":
    main()
