"""``ArrayUtils.mqh`` (MQL5 Book) — port. In-place helpers on Python lists."""

from __future__ import annotations

import math


def ArrayUnique(array: list) -> int:
    """Collapse runs of equal neighbours (sort first for a true unique);
    returns how many elements were removed."""
    n = len(array)
    if n <= 1:
        return 0
    w = 0
    for i in range(1, n):
        if array[i] == array[w]:
            pass
        elif w < i - 1:
            w += 1
            array[w] = array[i]
        else:
            w += 1
    del array[w + 1:]
    return n - len(array)


def ArrayPurge(array: list, empty) -> None:
    """Remove every element equal to ``empty``, keeping the order."""
    array[:] = [x for x in array if x != empty]


def ArrayPurger(array: list, func) -> None:
    """Remove every element for which ``func(element)`` is true."""
    array[:] = [x for x in array if not func(x)]


def ByteArrayPrint(data, row: int = 16, separator: str = " | ", start: int = 0, count: int = -1) -> None:
    _hex_print(list(data), 2, row, separator, start, count)


def HexArrayPrint(data, size_bytes: int = 1, row: int = 16, separator: str = " | ",
                  start: int = 0, count: int = -1) -> None:
    _hex_print(list(data), size_bytes * 2, row, separator, start, count)


def _hex_print(data, width, row, separator, start, count):
    total = len(data)
    if count < 0:
        count = total
    n = int(math.ceil(math.log10(total + 1))) if total else 1
    line = ""
    for i in range(start, min(start + count, total)):
        if i % row == 0 or i == start:
            if line:
                print(line)
            line = f"[{i:0{n}d}] "
        line += f"{data[i] & ((1 << (4 * width)) - 1):0{width}X}" + separator
    if line:
        print(line)
