from curses import (
    KEY_DOWN,
    KEY_END,
    KEY_HOME,
    KEY_LEFT,
    KEY_NPAGE,
    KEY_PPAGE,
    KEY_RIGHT,
    KEY_UP,
)
from enum import IntEnum, unique


@unique
class Key(IntEnum):
    ARROW_DOWN = KEY_DOWN
    ARROW_LEFT = KEY_LEFT
    ARROW_RIGHT = KEY_RIGHT
    ARROW_UP = KEY_UP
    END = KEY_END
    HOME = KEY_HOME
    L_A = ord("a")
    L_B = ord("b")
    L_C = ord("c")
    L_D = ord("d")
    L_E = ord("e")
    L_F = ord("f")
    L_G = ord("g")
    L_H = ord("h")
    L_I = ord("i")
    L_J = ord("j")
    L_K = ord("k")
    L_L = ord("l")
    L_M = ord("m")
    L_N = ord("n")
    L_O = ord("o")
    L_P = ord("p")
    L_Q = ord("q")
    L_R = ord("r")
    L_S = ord("s")
    L_T = ord("t")
    L_U = ord("u")
    L_V = ord("v")
    L_W = ord("w")
    L_X = ord("x")
    L_Y = ord("y")
    L_Z = ord("z")
    PAGE_DOWN = KEY_NPAGE
    PAGE_UP = KEY_PPAGE
    U_A = ord("A")
    U_B = ord("B")
    U_C = ord("C")
    U_D = ord("D")
    U_E = ord("E")
    U_F = ord("F")
    U_G = ord("G")
    U_H = ord("H")
    U_I = ord("I")
    U_J = ord("J")
    U_K = ord("K")
    U_L = ord("L")
    U_M = ord("M")
    U_N = ord("N")
    U_O = ord("O")
    U_P = ord("P")
    U_Q = ord("Q")
    U_R = ord("R")
    U_S = ord("S")
    U_T = ord("T")
    U_U = ord("U")
    U_V = ord("V")
    U_W = ord("W")
    U_X = ord("X")
    U_Y = ord("Y")
    U_Z = ord("Z")
