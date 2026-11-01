"""Container helpers — ports of ``CSOM/HashMapTemplate.mqh``, ``IndArray.mqh``
and ``CSOM/IndArray.mqh`` (Stanislav Korotky).

``HashMapTemplate``: a key → value list with tombstone removal and
``purge()`` (linear lookup, insertion order), exactly as the source.

``IndArray``: wrappers that make indicator buffers usable as arrays of
arrays (``IndicatorArray`` of ``Indicator`` buffers, each **series-indexed**:
``buf[0]`` is the newest bar, as ``ArraySetAsSeries(buffer, true)`` makes
them). In MT5 the terminal sizes the buffers; here pass ``size`` (the bar
count). ``buf.forward()`` gives the buffer oldest-first for returning to the
chart, with EMPTY_VALUE as NaN.

The MQL5 operator overloads (``ind[i] = x`` through an ``int``/``uint``
cursor trick) become plain item access: ``ind[i]`` reads, ``ind[i] = x``
writes. ``CSOM/IndArray.mqh`` is an older copy without ``empty()``/``set()``;
the same classes cover both.
"""

from __future__ import annotations

import numpy as np

from .mql_runtime import EMPTY_VALUE, to_nan


class HashMapTemplate:
    def __init__(self, nokey=None, empty=EMPTY_VALUE):
        self.keys: list = []
        self.values: list = []
        self.count = 0
        self.emptyKey = nokey
        self.emptyValue = empty

    def _add(self, key, value):
        self.keys.append(key)
        self.values.append(value)
        self.count += 1

    def reset(self):
        self.keys, self.values, self.count = [], [], 0

    def getIndex(self, key) -> int:
        for i in range(self.count):
            if self.keys[i] == key:
                return i
        return -1

    def getKey(self, index: int):
        if index < 0 or index >= self.count:
            return None
        return self.keys[index]

    def at(self, index: int):
        """``operator[](int index)``."""
        if index < 0 or index >= self.count:
            return self.emptyValue
        return self.values[index]

    def get(self, key):
        """``operator[](K key)``."""
        for i in range(self.count):
            if self.keys[i] == key:
                return self.values[i]
        return self.emptyValue

    def __getitem__(self, key):
        return self.get(key)

    def set(self, key, value):
        index = self.getIndex(key)
        if index != -1:
            self.values[index] = value
        else:
            self._add(key, value)

    __setitem__ = set

    def inc(self, key, value):
        index = self.getIndex(key)
        if index != -1:
            self.values[index] += value
        else:
            self._add(key, value)

    def remove(self, key):
        index = self.getIndex(key)
        if index != -1:
            self.keys[index] = self.emptyKey
            self.values[index] = self.emptyValue

    def purge(self):
        keep = [(k, v) for k, v in zip(self.keys, self.values) if k != self.emptyKey]
        self.keys = [k for k, _ in keep]
        self.values = [v for _, v in keep]
        self.count = len(keep)

    def getSize(self) -> int:
        return self.count


class Indicator:
    """One series-indexed indicator buffer."""

    def __init__(self, index: int = 0, empty: float = EMPTY_VALUE, size: int = 0):
        self.index = index
        self.buffer = np.full(int(size), float(empty))     # stored newest-first

    def resize(self, size: int, empty: float = EMPTY_VALUE):
        self.buffer = np.full(int(size), float(empty))

    def empty(self, empty: float = EMPTY_VALUE):
        self.buffer[:] = empty

    def __getitem__(self, b: int) -> float:
        return float(self.buffer[b])

    def __setitem__(self, b: int, x: float):
        self.buffer[b] = x

    def set(self, b: int, v):
        if np.ndim(v):
            v = np.asarray(v, dtype=float)
            self.buffer[b: b + len(v)] = v
        else:
            self.buffer[b] = v

    def edit(self) -> "IndicatorGetter":
        return IndicatorGetter(self)

    def forward(self) -> np.ndarray:
        """Oldest-first, EMPTY_VALUE → NaN, for the chart."""
        return to_nan(self.buffer[::-1])


class IndicatorGetter:
    def __init__(self, owner: Indicator):
        self.owner = owner

    def __getitem__(self, b: int) -> float:
        return self.owner[b]


class IndicatorArray:
    def __init__(self, n: int, empty: float = EMPTY_VALUE, size: int = 0):
        self.array = [Indicator(i, empty, size) for i in range(n)]

    def __getitem__(self, n: int) -> Indicator:
        return self.array[n]

    def size(self) -> int:
        return len(self.array)


class IndicatorArrayGetter:
    def __init__(self, a: IndicatorArray | None = None):
        self.array: list = []
        if a is not None:
            self.bind(a)

    def bind(self, a: IndicatorArray):
        self.array = [a[i].edit() for i in range(a.size())]

    def __getitem__(self, n: int) -> IndicatorGetter:
        return self.array[n]
