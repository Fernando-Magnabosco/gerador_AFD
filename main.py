from model.partial import Partial


def read_file(file):

    with open(file, "r") as f:
        lines = f.readlines()
    return lines


def main():

    lines = read_file("./files/test.txt")

    AFPartial = Partial(lines)
    AFND = AFPartial.create_AFND()
    # print(AFND)
    AFND.toCSV()
    AFND.determinize()


main()
