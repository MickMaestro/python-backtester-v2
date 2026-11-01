"""ArrayUtils.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class ArrayPurger(MqlObject):
    _q_fields = ()
    def __init__(self, array, func):
        count = ArraySize(array)
        write = 0
        i = 0
        while i < count:
            while i < count and func(array[i]):
                i += 1
            while i < count and (not func(array[i])):
                if write < i:
                    array[write] = array[i]
                i += 1
                write += 1
        ArrayResize(array, write)

def ArrayUnique(array):
    n = ArraySize(array)
    if n <= 1:
        return 0
    w = 0
    for i in range(1, n):
        if array[i] == array[w]:
            pass
        elif w < (i - 1):
            array[(w := w + 1)] = array[i]
        else:
            w += 1
    return n - ArrayResize(array, w + 1)

def ArrayPurge(array, empty):
    count = ArraySize(array)
    write = 0
    i = 0
    while i < count:
        while i < count and array[i] == empty:
            i += 1
        while i < count and array[i] != empty:
            if write < i:
                array[write] = array[i]
            i += 1
            write += 1
    ArrayResize(array, write)

def ByteArrayPrint(bytes, row=16, separator=' | ', start=0, count=WHOLE_ARRAY):
    hex = ''
    n = _int(MathCeil(MathLog10(ArraySize(bytes) + 1)))
    for i in range(start, MathMin(start + count, ArraySize(bytes))):
        if _imod(i, row) == 0 or i == start:
            if hex != '':
                Print(hex)
            hex = StringFormat('[%0*d]', n, i) + ' '
        hex += StringFormat('%02X', bytes[i]) + separator
    if hex != '':
        Print(hex)

def HexArrayPrint(bytes, row=16, separator=' | ', start=0, count=WHOLE_ARRAY):
    size = _idiv(8, 1) * 2
    hex = ''
    n = _int(MathCeil(MathLog10(ArraySize(bytes) + 1)))
    for i in range(start, MathMin(start + count, ArraySize(bytes))):
        if _imod(i, row) == 0 or i == start:
            if hex != '':
                Print(hex)
            hex = StringFormat('[%0*d]', n, i) + ' '
        hex += StringFormat('%0*x', size, bytes[i]) + separator
    if hex != '':
        Print(hex)

__all__ = ['ArrayPurger', 'ArrayUnique', 'ArrayPurge', 'ByteArrayPrint', 'HexArrayPrint']
