import re

# Non terminal allowed chars
NT = "<[A-z]+>"

# Terminal allowed chars
T = "[A-z0-9&]+"


REGEXES = {
    "LEFT_SIDE": f"({NT})::",
    "RIGHT_SIDE": "[=\\|]+\\s" + f"({T}{NT}|{NT}{T}|{T}|{NT})",
}


def read_file(file):

    with open(file, "r") as f:
        lines = f.readlines()
    return lines


def strFormatter(str):

    newStr = ""
    for char in str:
        if char == "|":
            newStr = ""
        else:
            newStr += char

    return newStr


def create_AFND(lines):

    pass


def main():

    lines = read_file("test.txt")

    for line in lines:
        print("LINHA:", line, end="")

        print("LEFT SIDE: ", re.findall(REGEXES["LEFT_SIDE"], line))
        print("RIGHT SIDE: ", re.findall(REGEXES["RIGHT_SIDE"], line))
        print()


main()
