# Non terminal allowed chars;
NT = "<[A-z]+>"


# Terminal allowed chars;
T = "[A-z0-9&]+"

# Left and right recognizers;
REGEXES = {
    "LEFT_SIDE":    f"({NT})::",
    "RIGHT_SIDE":   "[=\\|]+\\s*" + f"({T}{NT}|{T}|{NT})",
    "TERMINAL":     "[=\\|]+\\s*" + f"({T})",
    "ISFINAL":      "^([*])"
}

EPSILONSTATE = "eps"
