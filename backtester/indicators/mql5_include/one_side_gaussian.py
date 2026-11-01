"""``OneSideGaussian.mqh`` and ``OneSideGaussianLibrary.mqh`` (Tinytjan, 2007)
— line-by-line ports of both.

One-sided Gaussian smoothing over the current and *older* bars. Both
libraries index ``array[index + i]`` for older bars, i.e. they expect
**series-ordered** arrays (index 0 = newest), which is how the indicators
that include them set their buffers up. Pass reversed arrays
(``x[::-1]``) from forward-indexed data, and reverse the result back.

Fidelity note — integer arithmetic: the weight function is
``MathExp(-X*X*9/((Size+1)*(Size+1)))`` with ``int`` operands, so the
exponent is an *integer* division truncated toward zero. For small X the
exponent is 0 and the weight 1; the weights are therefore much flatter than
a real Gaussian. That is how MT5 computes them, and so this port.

``OneSideGaussian.mqh`` also sums ``N+1`` taps (``i<=N``) over an ``N``-tap
normalised kernel; the extra tap reads the zero-initialised slot ``N`` of the
global buffer and contributes nothing.
"""

from __future__ import annotations

from .mql_runtime import MathExp, PRICE_CLOSE, PRICE_HIGH, PRICE_LOW, PRICE_MEDIAN, PRICE_OPEN, \
    PRICE_TYPICAL, PRICE_WEIGHTED, idiv

# enum Applied_price_ (1-based extended price set, same as SmoothAlgorithms)
PRICE_CLOSE_, PRICE_OPEN_, PRICE_HIGH_, PRICE_LOW_ = 1, 2, 3, 4
PRICE_MEDIAN_, PRICE_TYPICAL_, PRICE_WEIGHTED_, PRICE_SIMPL_ = 5, 6, 7, 8
PRICE_QUARTER_, PRICE_TRENDFOLLOW0_, PRICE_TRENDFOLLOW1_, PRICE_DEMARK_ = 9, 10, 11, 12


def Gaussian(Size: int, X: int) -> float:
    """``MathExp(-X*X*9/((Size+1)*(Size+1)))`` with C integer division."""
    return MathExp(idiv(-X * X * 9, (Size + 1) * (Size + 1)))


def CountPrice(PriceMode, index, Open, Low, High, Close) -> float:
    """The library's applied price (note the Open, Low, High, Close order)."""
    pm = int(PriceMode)
    if pm == PRICE_CLOSE:
        return Close[index]
    if pm == PRICE_OPEN:
        return Open[index]
    if pm == PRICE_HIGH:
        return High[index]
    if pm == PRICE_LOW:
        return Low[index]
    if pm == PRICE_MEDIAN:
        return (High[index] + Low[index]) / 2.0
    if pm == PRICE_TYPICAL:
        return (Close[index] + High[index] + Low[index]) / 3.0
    if pm == PRICE_WEIGHTED:
        return (2 * Close[index] + High[index] + Low[index]) / 4.0
    if pm == 8:
        return (Open[index] + Close[index]) / 2.0
    if pm == 9:
        return (Open[index] + Close[index] + High[index] + Low[index]) / 4.0
    if pm == 10:
        if Close[index] > Open[index]:
            return High[index]
        return Low[index] if Close[index] < Open[index] else Close[index]
    if pm == 11:
        if Close[index] > Open[index]:
            return (High[index] + Close[index]) / 2.0
        return (Low[index] + Close[index]) / 2.0 if Close[index] < Open[index] else Close[index]
    if pm == 12:
        res = High[index] + Low[index] + Close[index]
        if Close[index] < Open[index]:
            res = (res + Low[index]) / 2
        if Close[index] > Open[index]:
            res = (res + High[index]) / 2
        if Close[index] == Open[index]:
            res = (res + Close[index]) / 2
        return ((res - Low[index]) + (res - High[index])) / 2
    return Close[index]


# ======================================================== OneSideGaussian.mqh

MaxLength = 22
_SIZES = (1, 2, 3, 5, 8, 13, 21)


class OneSideGaussian:
    """The include's global buffers and ``Smooth_N`` functions, held on an
    object (call :meth:`BuffersInit` once, as ``OnInit`` does)."""

    def __init__(self):
        self.buffers = {size: [0.0] * MaxLength for size in _SIZES}

    def BuffersInit(self) -> None:
        for size in _SIZES:
            buf = self.buffers[size]
            for i in range(MaxLength - 1):
                buf[i] = 0.0
            for i in range(size):
                buf[i] = Gaussian(size, i)
            total = 0.0
            for i in range(size):
                total += buf[i]
            for i in range(size):
                buf[i] /= total

    def _smooth(self, size, Rates_total, PriceMode, index, Open, Low, High, Close) -> float:
        if Rates_total <= index + size:
            return 0
        buf = self.buffers[size]
        total = 0.0
        for i in range(size + 1):
            total += buf[i] * CountPrice(PriceMode, i + index, Open, Low, High, Close)
        return total

    def Smooth_1(self, Rates_total, PriceMode, index, Open, Low, High, Close):
        return self._smooth(1, Rates_total, PriceMode, index, Open, Low, High, Close)

    def Smooth_2(self, Rates_total, PriceMode, index, Open, Low, High, Close):
        return self._smooth(2, Rates_total, PriceMode, index, Open, Low, High, Close)

    def Smooth_3(self, Rates_total, PriceMode, index, Open, Low, High, Close):
        return self._smooth(3, Rates_total, PriceMode, index, Open, Low, High, Close)

    def Smooth_5(self, Rates_total, PriceMode, index, Open, Low, High, Close):
        return self._smooth(5, Rates_total, PriceMode, index, Open, Low, High, Close)

    def Smooth_8(self, Rates_total, PriceMode, index, Open, Low, High, Close):
        return self._smooth(8, Rates_total, PriceMode, index, Open, Low, High, Close)

    def Smooth_13(self, Rates_total, PriceMode, index, Open, Low, High, Close):
        return self._smooth(13, Rates_total, PriceMode, index, Open, Low, High, Close)

    def Smooth_21(self, Rates_total, PriceMode, index, Open, Low, High, Close):
        return self._smooth(21, Rates_total, PriceMode, index, Open, Low, High, Close)


# ================================================= OneSideGaussianLibrary.mqh

MAXLENGTH = 34
levels = (1, 2, 3, 5, 8, 13, 21, MAXLENGTH)
# enum SmoothMode
Smooth1, Smooth2, Smooth3, Smooth4, Smooth5, Smooth6, Smooth7, Smooth8 = range(8)


class OneSideGaussianLibrary:
    """``GaussianInit`` / ``Smooth`` / ``SmoothArray`` with an 8-level kernel
    table (1, 2, 3, 5, 8, 13, 21, 34 taps)."""

    def __init__(self):
        self.GaussianBuffer = [[0.0] * 8 for _ in range(MAXLENGTH)]

    def GaussianInit(self) -> None:
        for k in range(8):
            total = 0.0
            for i in range(MAXLENGTH):
                if i >= levels[k]:
                    break
                self.GaussianBuffer[i][k] = Gaussian(levels[k], i)
                total += self.GaussianBuffer[i][k]
            for i in range(MAXLENGTH):
                if i >= levels[k]:
                    break
                self.GaussianBuffer[i][k] /= total

    def Smooth(self, level, Rates_total, PriceMode, index, Open, Low, High, Close) -> float:
        limit = levels[int(level)]
        if index >= Rates_total - limit:
            return CountPrice(PriceMode, index, Open, Low, High, Close)
        total = 0.0
        for i in range(limit):
            total += self.GaussianBuffer[i][int(level)] * CountPrice(PriceMode, index + i, Open, Low, High, Close)
        return total

    def SmoothArray(self, level, array, Rates_total, PriceMode, index) -> float:
        limit = levels[int(level)]
        if index >= Rates_total - limit:
            return array[index]
        total = 0.0
        for i in range(limit):
            total += self.GaussianBuffer[i][int(level)] * array[index + i]
        return total
