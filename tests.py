from dataclasses import dataclass


@dataclass
class A:
    a: int
    b: float
    c: str


JOHN = "ASA"


def testable_int(a: int, b: int):
    if a < 0:  # 2
        return 5
    pass
    pass
    if b < 10:  # 3
        pass
        if a > 6:  # 4
            pass
        else:
            pass
            pass
    pass
    g = A(a, 0.0, JOHN)
    return 3


def testable_float(a: float, b: float):
    if a < 3.0:
        return 5
    pass
    pass
    pass
    if b != 7.0:
        return 5
    pass
    if a > b:
        return 3
    else:
        return 5


def testable_str(a: str, b: str):
    if "x" in a:
        return 1
    pass
    pass
    if b in a:
        return 2
    pass
    if "a" in b or "b" in b or "c" in b:
        return 5
