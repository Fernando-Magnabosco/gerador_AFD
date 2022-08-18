from header.defs import *
from model.afnd import *
from model.partial import *
from model.production import *
from model.rule import *




def read_file(file):

    with open(file, "r") as f:
        lines = f.readlines()
    return lines


def main():

    lines = read_file("./files/test.txt")

    AFPartial = Partial(lines)
    AFND = AFPartial.create_AFND()
    print(AFND)
    AFND.toCSV()
    AFND.determinize()

main()
