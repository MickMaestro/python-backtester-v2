"""``SmoothAlgorithms.mqh`` (Nikolay Kositsin, v3.24, 25 Jan 2015) — a
faithful, line-by-line port.

This is the include behind more than a thousand of the Codebase indicators
(every ``X*`` / ``*_HTF`` / ``Color*`` indicator by Kositsin and the many that
borrowed it). ``SmoothAlgorithms45.mqh`` is the same library made MQL4-
compatible (``#property strict``, lower-case price parameter names); its maths
is identical, so it maps to this module too.

How to use it from a converted indicator
----------------------------------------
The classes keep their MQL5 names and call signatures, because indicators call
them **once per bar** from inside their ``OnCalculate`` loop and the warm-up
logic depends on ``begin``/``bar``/``set``::

    xma = CXMA()
    for bar in range(first, rates_total):
        out[bar] = xma.XMASeries(min_rates, prev_calculated, rates_total,
                                 XMA_Method, XPhase, XLength, price[bar], bar, False)

Values come back exactly as MQL5 returns them — including ``EMPTY_VALUE``
(``DBL_MAX``) during warm-up — so code that compares against EMPTY_VALUE
behaves the same. Convert a finished buffer with
:func:`mql_runtime.to_nan` before handing it to the chart.

For whole-array use there are wrappers at the bottom (:func:`xma_series`,
:func:`ma_series`, …) that run the per-bar classes over a forward-indexed
array in one pass and return NaN where the library returns EMPTY_VALUE.

Fidelity notes
--------------
- ``BarCheck4``/``BarCheck5`` — saving the state at the second-to-last bar and
  restoring it after the last bar so the forming bar can be recalculated on
  the next tick — are reproduced. In a single full pass they do not change any
  output, but they keep incremental (``prev_calculated > 0``) use correct.
- CJJMA's per-element "changed" flags around that save/restore are replaced by
  whole-array copies; the restored state is the same.
- Member variables MQL5 leaves uninitialised start at 0 here (the terminal
  zero-fills global objects, which is how these classes are used).
- ``CParMA`` keeps its sums of x, x², x³, x⁴ in 32-bit ``int`` members; for
  ``Length > 100`` the x⁴ sum overflows in MQL5. The port reproduces the
  wrap-around (see :func:`mql_runtime.as_int32`) so results match the terminal
  — garbage included — rather than silently being "fixed".
- Messages the library ``Print``s for out-of-range inputs are not reproduced;
  the clamping it applies is.
"""

from __future__ import annotations

import math

import numpy as np

from .mql_runtime import (
    EMPTY_VALUE, MODE_EMA, MODE_LWMA, MODE_SMA, MODE_SMMA,
    PRICE_CLOSE, PRICE_HIGH, PRICE_LOW, PRICE_MEDIAN, PRICE_OPEN,
    PRICE_TYPICAL, PRICE_WEIGHTED,
    MathAbs, MathCeil, MathFloor, MathLog, MathPow, MathSqrt,
    as_int32, as_uint, fdiv, to_nan,
)

# ----------------------------------------------------------------- enumerations

#: enum Smooth_Method
MODE_SMA_, MODE_EMA_, MODE_SMMA_, MODE_LWMA_ = 0, 1, 2, 3
MODE_JJMA, MODE_JurX, MODE_ParMA, MODE_T3, MODE_VIDYA, MODE_AMA = 4, 5, 6, 7, 8, 9

SMOOTH_METHOD_NAMES = {
    MODE_SMA_: "SMA", MODE_EMA_: "EMA", MODE_SMMA_: "SMMA", MODE_LWMA_: "LWMA",
    MODE_JJMA: "JJMA", MODE_JurX: "JurX", MODE_ParMA: "ParMA", MODE_T3: "T3",
    MODE_VIDYA: "VIDYA", MODE_AMA: "AMA",
}

#: enum Applied_price_ (the library's extended, 1-based applied price)
PRICE_CLOSE_, PRICE_OPEN_, PRICE_HIGH_, PRICE_LOW_ = 1, 2, 3, 4
PRICE_MEDIAN_, PRICE_TYPICAL_, PRICE_WEIGHTED_, PRICE_SIMPL_ = 5, 6, 7, 8
PRICE_QUARTER_, PRICE_TRENDFOLLOW0_, PRICE_TRENDFOLLOW1_, PRICE_DEMARK_ = 9, 10, 11, 12

APPLIED_PRICE_NAMES = {
    1: "Close", 2: "Open", 3: "High", 4: "Low", 5: "Median Price (HL/2)",
    6: "Typical Price (HLC/3)", 7: "Weighted Close (HLCC/4)",
    8: "Simpl Price (OC/2)", 9: "Quarted Price (HLOC/4)",
    10: "TrendFollow_1 Price", 11: "TrendFollow_2 Price", 12: "Demark Price",
}


def _new_array(size: int) -> list:
    return [0.0] * max(int(size), 0)


# ======================================================== CMovSeriesTools


class CMovSeriesTools:
    """Shared helpers: warm-up checks and the ring-buffer bookkeeping."""

    # -- warm-up checks (all take plain ints, as in the source)

    @staticmethod
    def BarCheck1(begin: int, bar: int, Set: bool) -> bool:
        return (not Set and bar < begin) or (Set and bar > begin)

    @staticmethod
    def BarCheck2(begin: int, bar: int, Set: bool, Length: int) -> bool:
        return (not Set and bar == begin + Length - 1) or (Set and bar == begin - Length + 1)

    @staticmethod
    def BarCheck3(begin: int, bar: int, Set: bool, Length: int) -> bool:
        return (not Set and bar < begin + Length - 1) or (Set and bar > begin - Length + 1)

    @staticmethod
    def BarCheck4(rates_total: int, bar: int, Set: bool) -> bool:
        return (not Set and bar == rates_total - 2) or (Set and bar == 1)

    @staticmethod
    def BarCheck5(rates_total: int, bar: int, Set: bool) -> bool:
        return (not Set and bar == rates_total - 1) or (Set and bar == 0)

    @staticmethod
    def BarCheck6(rates_total: int, bar: int, Set: bool) -> bool:
        # Declared in the class but never defined or called by the library.
        raise NotImplementedError("BarCheck6 is declared but not implemented in SmoothAlgorithms.mqh")

    @staticmethod
    def LengthCheck(ExternLength):
        """``LengthCheck(&ExternLength)`` — returns the clamped value."""
        return 1 if ExternLength < 1 else ExternLength

    @staticmethod
    def MALengthCheck(LengthName: str, ExternLength) -> None:
        """Only prints a warning in MQL5; nothing to do here."""

    @staticmethod
    def Recount_ArrayZeroPos(count: int, Length: int, prev_calculated: int,
                             rates_total: int, series: float, bar: int,
                             Array: list, set: bool) -> int:
        """Write ``series`` into the ring and return the updated ``count``."""
        if set:
            if as_uint(bar) != as_uint(rates_total - prev_calculated):
                count -= 1
                if count < 0:
                    count = Length - 1
        else:
            if as_uint(bar) != as_uint(prev_calculated - 1):
                count -= 1
                if count < 0:
                    count = Length - 1
        Array[count] = series
        return count

    @staticmethod
    def Recount_ArrayNumber(count: int, Length: int, Number: int) -> int:
        ArrNumber = Number + count
        if ArrNumber > Length - 1:
            ArrNumber -= Length
        return ArrNumber

    @staticmethod
    def SeriesArrayResize(FunctionsName: str, Length: int, Array: list, Size_: int) -> int:
        """Grow ``Array`` (in place) to ``Length + 1`` if needed; returns the new
        ``Size_``. (The MQL5 version returns false only if the allocation
        fails, which cannot happen here.)"""
        if Length > Size_:
            Size = Length + 1
            Array.extend([0.0] * (Size - len(Array)))
            return Size
        return Size_


# ======================================================== CMoving_Average


class CMoving_Average(CMovSeriesTools):
    """SMA / EMA / SMMA / LWMA, one bar per call.

    The four methods share the same member variables, exactly as in MQL5: use
    one instance per averaging method and per series.
    """

    def __init__(self):
        self.m_SeriesArray: list = []
        self.m_Size_ = 0
        self.m_count = 0
        self.m_weight = 0
        self.m_Moving = self.m_MOVING = self.m_Pr = 0.0
        self.m_sum = self.m_SUM = self.m_lsum = self.m_LSUM = 0.0

    def MASeries(self, begin, prev_calculated, rates_total, Length, MA_Method,
                 series, bar, set):
        if MA_Method == MODE_SMA:
            return self.SMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        if MA_Method == MODE_EMA:
            return self.EMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        if MA_Method == MODE_SMMA:
            return self.SMMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        if MA_Method == MODE_LWMA:
            return self.LWMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        return self.SMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)

    def SMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set):
        begin, bar, Length = int(begin), int(bar), int(Length)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        Length = self.LengthCheck(Length)
        if bar == begin:
            self.m_Size_ = self.SeriesArrayResize("SMASeries", Length, self.m_SeriesArray, self.m_Size_)
        self.m_count = self.Recount_ArrayZeroPos(self.m_count, Length, prev_calculated,
                                                 rates_total, series, bar, self.m_SeriesArray, set)
        if self.BarCheck2(begin, bar, set, Length):
            self.m_sum = 0.0
            for iii in range(1, Length):
                kkk = self.Recount_ArrayNumber(self.m_count, Length, iii)
                self.m_sum += self.m_SeriesArray[kkk]
        elif self.BarCheck3(begin, bar, set, Length):
            return EMPTY_VALUE
        self.m_sum += series
        sma = self.m_sum / Length
        kkk = self.Recount_ArrayNumber(self.m_count, Length, Length - 1)
        self.m_sum -= self.m_SeriesArray[kkk]
        if self.BarCheck4(rates_total, bar, set):
            self.m_SUM = self.m_sum
        if self.BarCheck5(rates_total, bar, set):
            self.m_sum = self.m_SUM
        return sma

    def EMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set):
        begin, bar = int(begin), int(bar)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        Length = self.LengthCheck(float(Length))
        if bar == begin:
            self.m_Pr = 2.0 / (Length + 1.0)
            self.m_Moving = series
        self.m_Moving = series * self.m_Pr + self.m_Moving * (1 - self.m_Pr)
        ema = self.m_Moving
        if self.BarCheck4(rates_total, bar, set):
            self.m_MOVING = self.m_Moving
        if self.BarCheck5(rates_total, bar, set):
            self.m_Moving = self.m_MOVING
        return ema

    def SMMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set):
        begin, bar, Length = int(begin), int(bar), int(Length)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        Length = self.LengthCheck(Length)
        if bar == begin:
            self.m_Size_ = self.SeriesArrayResize("SMMASeries", Length, self.m_SeriesArray, self.m_Size_)
        self.m_count = self.Recount_ArrayZeroPos(self.m_count, Length, prev_calculated,
                                                 rates_total, series, bar, self.m_SeriesArray, set)
        if self.BarCheck2(begin, bar, set, Length):
            self.m_sum = 0.0
            for iii in range(Length):
                self.m_sum += self.m_SeriesArray[iii]
            # Length == 1 divides by zero in MQL5 (inf/nan), and so here.
            self.m_Moving = fdiv(self.m_sum - series, Length - 1)
        elif self.BarCheck3(begin, bar, set, Length):
            return EMPTY_VALUE
        self.m_sum = self.m_Moving * (Length - 1) + series
        self.m_Moving = self.m_sum / Length
        smma = self.m_Moving
        if self.BarCheck4(rates_total, bar, set):
            self.m_SUM = self.m_sum
            self.m_MOVING = self.m_Moving
        if self.BarCheck5(rates_total, bar, set):
            self.m_sum = self.m_SUM
            self.m_Moving = self.m_MOVING
        return smma

    def LWMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set):
        begin, bar, Length = int(begin), int(bar), int(Length)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        Length_ = Length + 1          # computed before LengthCheck, as in the source
        Length = self.LengthCheck(Length)
        if bar == begin:
            self.m_Size_ = self.SeriesArrayResize("LWMASeries", Length_, self.m_SeriesArray, self.m_Size_)
        self.m_count = self.Recount_ArrayZeroPos(self.m_count, Length_, prev_calculated,
                                                 rates_total, series, bar, self.m_SeriesArray, set)
        if self.BarCheck2(begin, bar, set, Length_):
            self.m_sum = 0.0
            self.m_lsum = 0.0
            self.m_weight = 0
            rrr = Length
            for iii in range(1, Length + 1):
                kkk = self.Recount_ArrayNumber(self.m_count, Length_, iii)
                self.m_sum += self.m_SeriesArray[kkk] * rrr
                self.m_lsum += self.m_SeriesArray[kkk]
                self.m_weight += iii
                rrr -= 1
        elif self.BarCheck3(begin, bar, set, Length_):
            return EMPTY_VALUE
        self.m_sum += series * Length - self.m_lsum
        kkk = self.Recount_ArrayNumber(self.m_count, Length_, Length)
        self.m_lsum += series - self.m_SeriesArray[kkk]
        lwma = fdiv(self.m_sum, self.m_weight)
        if self.BarCheck4(rates_total, bar, set):
            self.m_SUM = self.m_sum
            self.m_LSUM = self.m_lsum
        if self.BarCheck5(rates_total, bar, set):
            self.m_sum = self.m_SUM
            self.m_lsum = self.m_LSUM
        return lwma


# ========================================================== CStdDeviation


class CStdDeviation(CMovSeriesTools):
    """Standard deviation of ``series`` around a supplied moving average."""

    def __init__(self):
        self.m_Size_ = 0
        self.m_count = 0
        self.m_Sum = self.m_SUM = self.m_Sum2 = self.m_SUM2 = 0.0
        self.m_SeriesArray: list = []

    def StdDevSeries(self, begin, prev_calculated, rates_total, Length, deviation,
                     series, MovSeries, bar, set):
        begin, bar, Length = int(begin), int(bar), int(Length)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        if bar == begin:
            self.m_Size_ = self.SeriesArrayResize("StdDevSeries", Length, self.m_SeriesArray, self.m_Size_)
        Length = self.LengthCheck(Length)
        self.m_count = self.Recount_ArrayZeroPos(self.m_count, Length, prev_calculated,
                                                 rates_total, series, bar, self.m_SeriesArray, set)
        if self.BarCheck2(begin, bar, set, Length):
            self.m_Sum = 0.0
            self.m_Sum2 = 0.0
            for iii in range(1, Length):
                kkk = self.Recount_ArrayNumber(self.m_count, Length, iii)
                self.m_Sum += self.m_SeriesArray[kkk]
                self.m_Sum2 += MathPow(self.m_SeriesArray[kkk], 2)
        elif self.BarCheck3(begin, bar, set, Length):
            return EMPTY_VALUE
        self.m_Sum += series
        self.m_Sum2 += MathPow(series, 2)
        m_SumX2 = Length * MathPow(MovSeries, 2) - 2 * MovSeries * self.m_Sum + self.m_Sum2
        kkk = self.Recount_ArrayNumber(self.m_count, Length, Length - 1)
        self.m_Sum2 -= MathPow(self.m_SeriesArray[kkk], 2)
        self.m_Sum -= self.m_SeriesArray[kkk]
        StdDev = deviation * MathSqrt(m_SumX2 / Length)
        # Note the source's order: restore (BarCheck5) before save (BarCheck4).
        if self.BarCheck5(rates_total, bar, set):
            self.m_Sum = self.m_SUM
            self.m_Sum2 = self.m_SUM2
        if self.BarCheck4(rates_total, bar, set):
            self.m_SUM = self.m_Sum
            self.m_SUM2 = self.m_Sum2
        return StdDev


# ================================================================== CJJMA


_JJMA_STATE = (
    "m_JMA", "m_djma", "m_ser1", "m_ser2", "m_Sum2", "m_pos1", "m_pos2",
    "m_Sum1", "m_Loop1", "m_Loop2", "m_count1", "m_count2", "m_count3",
    "m_storage1", "m_storage2", "m_midd1", "m_midd2",
)


class CJJMA(CMovSeriesTools):
    """Jurik's JMA as the library implements it (``JJMASeries``).

    ``Din != 0`` re-reads ``Phase``/``Length`` on every bar (dynamic
    parameters); ``Din == 0`` fixes them at ``begin``.
    """

    def __init__(self):
        self.m_start = False
        self.m_array = [0.0] * 62
        self.m_degree = self.m_Phase = self.m_sense = 0.0
        self.m_Krx = self.m_Kfd = self.m_Krj = self.m_Kct = 0.0
        self.m_var1 = self.m_var2 = 0.0
        self.m_pos2 = self.m_pos1 = 0
        self.m_Loop1 = self.m_Loop2 = 0
        self.m_midd1 = self.m_midd2 = 0
        self.m_count1 = self.m_count2 = self.m_count3 = 0
        self.m_ser1 = self.m_ser2 = 0.0
        self.m_Sum1 = self.m_Sum2 = self.m_JMA = 0.0
        self.m_storage1 = self.m_storage2 = self.m_djma = 0.0
        self.m_hoop1 = [0.0] * 128
        self.m_hoop2 = [0.0] * 11
        self.m_data = [0.0] * 128
        self._saved: dict | None = None

    # -------------------------------------------------------------- JJMAInit

    def JJMAInit(self, begin, Din, Phase, Length, series, bar):
        if bar == begin or Din != 0:
            if bar == begin:
                self.m_midd1 = 63
                self.m_midd2 = 64
                self.m_start = False
                for numb in range(0, self.m_midd1 + 1):
                    self.m_data[numb] = -1000000.0
                for numb in range(self.m_midd2, 128):
                    self.m_data[numb] = +1000000.0
                self.m_hoop1 = [0.0] * 128
                self.m_hoop2 = [0.0] * 11
                self.m_array = [0.0] * 62
                self.m_djma = 0.0
                self.m_Sum1 = 0.0
                self.m_Sum2 = 0.0
                self.m_ser1 = 0.0
                self.m_ser2 = 0.0
                self.m_pos1 = 0
                self.m_pos2 = 0
                self.m_Loop1 = 0
                self.m_Loop2 = 0
                self.m_count1 = 0
                self.m_count2 = 0
                self.m_count3 = 0
                self.m_storage1 = 0.0
                self.m_storage2 = 0.0
                self.m_JMA = series
                self._saved = None
            if -100 <= Phase <= 100:
                self.m_Phase = Phase / 100.0 + 1.5
            if Phase > +100:
                self.m_Phase = 2.5
            if Phase < -100:
                self.m_Phase = 0.5
            if Length >= 1.0000000002:
                velA = (Length - 1.0) / 2.0
            else:
                velA = 0.0000000001
            velA *= 0.9
            self.m_Krj = velA / (velA + 2.0)
            velC = MathSqrt(velA)
            velD = MathLog(velC)
            self.m_var1 = velD
            self.m_var2 = self.m_var1
            velB = MathLog(2.0)
            self.m_sense = (self.m_var2 / velB) + 2.0
            if self.m_sense < 0.0:
                self.m_sense = 0.0
            self.m_Kfd = self.m_sense
            if self.m_Kfd >= 2.5:
                self.m_degree = self.m_Kfd - 2.0
            else:
                self.m_degree = 0.5
            self.m_Krx = velC * self.m_Kfd
            self.m_Kct = self.m_Krx / (self.m_Krx + 1.0)

    # ------------------------------------------------------------ JJMASeries

    def JJMASeries(self, begin, prev_calculated, rates_total, Din, Phase, Length,
                   series, bar, set):
        begin, bar = int(begin), int(bar)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        self.JJMAInit(begin, Din, Phase, Length, series, bar)

        data = self.m_data
        extent = 0.0
        if self.m_Loop1 < 61:
            self.m_Loop1 += 1
            self.m_array[self.m_Loop1] = series

        if self.m_Loop1 > 30:
            if not self.m_start:
                self.m_start = True
                back = 29
                self.m_ser2 = self.m_array[1]
                self.m_ser1 = self.m_ser2
            else:
                back = 0

            for rrr in range(back, -1, -1):
                if rrr == 0:
                    ser0 = series
                else:
                    ser0 = self.m_array[31 - rrr]
                dser1 = ser0 - self.m_ser1
                dser2 = ser0 - self.m_ser2
                if MathAbs(dser1) > MathAbs(dser2):
                    self.m_var2 = MathAbs(dser1)
                else:
                    self.m_var2 = MathAbs(dser2)
                Res = self.m_var2
                newvel = Res + 0.0000000001

                if self.m_count1 <= 1:
                    self.m_count1 = 127
                else:
                    self.m_count1 -= 1
                if self.m_count2 <= 1:
                    self.m_count2 = 10
                else:
                    self.m_count2 -= 1
                if self.m_count3 < 128:
                    self.m_count3 += 1

                self.m_Sum1 += newvel - self.m_hoop2[self.m_count2]
                self.m_hoop2[self.m_count2] = newvel
                if self.m_count3 > 10:
                    SmVel = self.m_Sum1 / 10.0
                else:
                    SmVel = self.m_Sum1 / self.m_count3

                if self.m_count3 > 127:
                    hoop1 = self.m_hoop1[self.m_count1]
                    self.m_hoop1[self.m_count1] = SmVel
                    numb = 64
                    posB = numb
                    while numb > 1:
                        if data[posB] < hoop1:
                            numb = int(numb / 2.0)
                            posB += numb
                        elif data[posB] <= hoop1:
                            numb = 1
                        else:
                            numb = int(numb / 2.0)
                            posB -= numb
                else:
                    self.m_hoop1[self.m_count1] = SmVel
                    if self.m_midd1 + self.m_midd2 > 127:
                        self.m_midd2 -= 1
                        posB = self.m_midd2
                    else:
                        self.m_midd1 += 1
                        posB = self.m_midd1
                    self.m_pos2 = 96 if self.m_midd1 > 96 else self.m_midd1
                    self.m_pos1 = 32 if self.m_midd2 < 32 else self.m_midd2

                numb = 64
                posA = numb
                while numb > 1:
                    if data[posA] >= SmVel:
                        if data[posA - 1] <= SmVel:
                            numb = 1
                        else:
                            numb = int(numb / 2.0)
                            posA -= numb
                    else:
                        numb = int(numb / 2.0)
                        posA += numb
                    if posA == 127:
                        if SmVel > data[127]:
                            posA = 128

                pos1, pos2 = self.m_pos1, self.m_pos2
                if self.m_count3 > 127:
                    # Brace-less if/else chains, resolved as C binds them.
                    if posB >= posA:
                        if pos2 + 1 > posA:
                            if pos1 - 1 < posA:
                                self.m_Sum2 += SmVel
                            elif pos1 + 0 > posA:
                                if pos1 - 1 < posB:
                                    self.m_Sum2 += data[pos1 - 1]
                    elif pos1 >= posA:
                        if pos2 + 1 < posA:
                            if pos2 + 1 > posB:
                                self.m_Sum2 += data[pos2 + 1]
                    elif pos2 + 2 > posA:
                        self.m_Sum2 += SmVel
                    elif pos2 + 1 < posA:
                        if pos2 + 1 > posB:
                            self.m_Sum2 += data[pos2 + 1]

                    if posB > posA:
                        if pos1 - 1 < posB:
                            if pos2 + 1 > posB:
                                self.m_Sum2 -= data[posB]
                            elif pos2 < posB:
                                if pos2 + 1 > posA:
                                    self.m_Sum2 -= data[pos2]
                    else:
                        if pos2 + 1 > posB and pos1 - 1 < posB:
                            self.m_Sum2 -= data[posB]
                        elif pos1 + 0 > posB:
                            if pos1 - 0 < posA:
                                self.m_Sum2 -= data[pos1]

                if posB <= posA:
                    if posB == posA:
                        data[posA] = SmVel
                    else:
                        for numb in range(posB + 1, posA):
                            data[numb - 1] = data[numb]
                        data[posA - 1] = SmVel
                else:
                    for numb in range(posB - 1, posA - 1, -1):
                        data[numb + 1] = data[numb]
                    data[posA] = SmVel

                if self.m_count3 <= 127:
                    self.m_Sum2 = 0.0
                    for numb in range(pos1, pos2 + 1):
                        self.m_Sum2 += data[numb]

                resalt = self.m_Sum2 / (pos2 - pos1 + 1.0)

                if self.m_Loop2 > 30:
                    self.m_Loop2 = 31
                else:
                    self.m_Loop2 += 1

                if self.m_Loop2 <= 30:
                    if dser1 > 0.0:
                        self.m_ser1 = ser0
                    else:
                        self.m_ser1 = ser0 - dser1 * self.m_Kct
                    if dser2 < 0.0:
                        self.m_ser2 = ser0
                    else:
                        self.m_ser2 = ser0 - dser2 * self.m_Kct
                    self.m_JMA = series
                    if self.m_Loop2 != 30:
                        continue
                    self.m_storage1 = series
                    if MathCeil(self.m_Krx) >= 1:
                        dSupr = float(MathCeil(self.m_Krx))
                    else:
                        dSupr = 1.0
                    if dSupr > 0:
                        Suprem2 = float(MathFloor(dSupr))
                    elif dSupr < 0:
                        Suprem2 = float(MathCeil(dSupr))
                    else:
                        Suprem2 = 0.0
                    if MathFloor(self.m_Krx) >= 1:
                        self.m_var2 = float(MathFloor(self.m_Krx))
                    else:
                        self.m_var2 = 1.0
                    if self.m_var2 > 0:
                        Suprem1 = float(MathFloor(self.m_var2))
                    elif self.m_var2 < 0:
                        Suprem1 = float(MathCeil(self.m_var2))
                    else:
                        Suprem1 = 0.0
                    if Suprem2 == Suprem1:
                        factor = 1.0
                    else:
                        dSupr = Suprem2 - Suprem1
                        factor = (self.m_Krx - Suprem1) / dSupr
                    shift1 = int(Suprem1) if Suprem1 <= 29 else 29
                    shift2 = int(Suprem2) if Suprem2 <= 29 else 29
                    dser3 = series - self.m_array[self.m_Loop1 - shift1]
                    dser4 = series - self.m_array[self.m_Loop1 - shift2]
                    self.m_djma = dser3 * (1.0 - factor) / Suprem1 + dser4 * factor / Suprem2
                else:
                    if resalt:
                        ResPow = MathPow(Res / resalt, self.m_degree)
                    else:
                        ResPow = 0.0
                    if self.m_Kfd >= ResPow:
                        self.m_var1 = ResPow
                    else:
                        self.m_var1 = self.m_Kfd
                    if self.m_var1 < 1.0:
                        self.m_var2 = 1.0
                    else:
                        if self.m_Kfd >= ResPow:
                            self.m_sense = ResPow
                        else:
                            self.m_sense = self.m_Kfd
                        self.m_var2 = self.m_sense
                    extent = self.m_var2
                    Pow1 = MathPow(self.m_Kct, MathSqrt(extent))
                    if dser1 > 0.0:
                        self.m_ser1 = ser0
                    else:
                        self.m_ser1 = ser0 - dser1 * Pow1
                    if dser2 < 0.0:
                        self.m_ser2 = ser0
                    else:
                        self.m_ser2 = ser0 - dser2 * Pow1

            if self.m_Loop2 > 30:
                Pow2 = MathPow(self.m_Krj, extent)
                self.m_storage1 *= Pow2
                self.m_storage1 += (1.0 - Pow2) * series
                self.m_storage2 *= self.m_Krj
                self.m_storage2 += (series - self.m_storage1) * (1.0 - self.m_Krj)
                Extr = self.m_Phase * self.m_storage2 + self.m_storage1
                Pow2x2 = Pow2 * Pow2
                ratio = Pow2x2 - 2.0 * Pow2 + 1.0
                self.m_djma *= Pow2x2
                self.m_djma += (Extr - self.m_JMA) * ratio
                self.m_JMA += self.m_djma

        if self.m_Loop1 <= 30:
            return EMPTY_VALUE
        jjma = self.m_JMA

        if self.BarCheck5(rates_total, bar, set) and self._saved is not None:
            s = self._saved
            self.m_hoop1 = list(s["m_hoop1"])
            self.m_hoop2 = list(s["m_hoop2"])
            self.m_data = list(s["m_data"])
            for name in _JJMA_STATE:
                setattr(self, name, s[name])
        if self.BarCheck4(rates_total, bar, set):
            s = {name: getattr(self, name) for name in _JJMA_STATE}
            s["m_hoop1"] = list(self.m_hoop1)
            s["m_hoop2"] = list(self.m_hoop2)
            s["m_data"] = list(self.m_data)
            self._saved = s
        return jjma

    def JJMALengthCheck(self, LengthName, ExternLength):
        """Prints a warning in MQL5 only."""

    def JJMAPhaseCheck(self, PhaseName, ExternPhase):
        """Prints a warning in MQL5 only."""


# ===================================================================== CT3


class CT3(CMovSeriesTools):
    """Tillson's T3; ``Curvature`` is the volume factor × 100."""

    def __init__(self):
        self.m_b2 = self.m_b3 = 0.0
        self.m_e1 = self.m_e2 = self.m_e3 = self.m_e4 = self.m_e5 = self.m_e6 = 0.0
        self.m_E1 = self.m_E2 = self.m_E3 = self.m_E4 = self.m_E5 = self.m_E6 = 0.0
        self.m_c1 = self.m_c2 = self.m_c3 = self.m_c4 = self.m_w1 = self.m_w2 = 0.0

    def T3Init(self, begin, Din, Curvature, Length, series, bar):
        if bar == begin or Din != 0:
            b = Curvature / 100.0
            self.m_b2 = b * b
            self.m_b3 = self.m_b2 * b
            self.m_c1 = -self.m_b3
            self.m_c2 = (3 * (self.m_b2 + self.m_b3))
            self.m_c3 = -3 * (2 * self.m_b2 + b + self.m_b3)
            self.m_c4 = (1 + 3 * b + self.m_b3 + 3 * self.m_b2)
            n = 1 + 0.5 * (Length - 1)
            self.m_w1 = 2 / (n + 1)
            self.m_w2 = 1 - self.m_w1
            if bar == begin:
                self.m_e1 = self.m_e2 = self.m_e3 = series
                self.m_e4 = self.m_e5 = self.m_e6 = series

    def T3Series(self, begin, prev_calculated, rates_total, Din, Curvature, Length,
                 series, bar, set):
        begin, bar = int(begin), int(bar)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        Length = self.LengthCheck(float(Length))
        self.T3Init(begin, Din, Curvature, Length, series, bar)
        e0 = series
        self.m_e1 = self.m_w1 * e0 + self.m_w2 * self.m_e1
        self.m_e2 = self.m_w1 * self.m_e1 + self.m_w2 * self.m_e2
        self.m_e3 = self.m_w1 * self.m_e2 + self.m_w2 * self.m_e3
        self.m_e4 = self.m_w1 * self.m_e3 + self.m_w2 * self.m_e4
        self.m_e5 = self.m_w1 * self.m_e4 + self.m_w2 * self.m_e5
        self.m_e6 = self.m_w1 * self.m_e5 + self.m_w2 * self.m_e6
        T3_ = self.m_c1 * self.m_e6 + self.m_c2 * self.m_e5 + self.m_c3 * self.m_e4 + self.m_c4 * self.m_e3
        if self.BarCheck5(rates_total, bar, set):
            self.m_e1, self.m_e2, self.m_e3 = self.m_E1, self.m_E2, self.m_E3
            self.m_e4, self.m_e5, self.m_e6 = self.m_E4, self.m_E5, self.m_E6
        if self.BarCheck4(rates_total, bar, set):
            self.m_E1, self.m_E2, self.m_E3 = self.m_e1, self.m_e2, self.m_e3
            self.m_E4, self.m_E5, self.m_E6 = self.m_e4, self.m_e5, self.m_e6
        return T3_


# =================================================================== CJurX


class CJurX(CMovSeriesTools):
    """Jurik's JurX: three chained two-pole smoothers."""

    def __init__(self):
        self.m_AB = self.m_AC = 0.0
        self.m_f1 = self.m_f2 = self.m_f3 = self.m_f4 = self.m_f5 = self.m_f6 = 0.0
        self.m_Kg = self.m_Hg = self.m_w = 0.0
        self.m_F1 = self.m_F2 = self.m_F3 = self.m_F4 = self.m_F5 = self.m_F6 = 0.0

    def JurXInit(self, begin, Din, Length, series, bar):
        if bar == begin or Din != 0:
            self.m_w = Length - 1 if Length >= 6 else 5
            self.m_Kg = 3 / (Length + 2.0)
            self.m_Hg = 1.0 - self.m_Kg
            if bar == begin:
                self.m_f1 = self.m_f2 = self.m_f3 = series
                self.m_f4 = self.m_f5 = self.m_f6 = series
                self.m_AB = 0.5
                self.m_AC = 1.5

    def JurXSeries(self, begin, prev_calculated, rates_total, Din, Length, series, bar, set):
        begin, bar = int(begin), int(bar)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        Length = self.LengthCheck(float(Length))
        self.JurXInit(begin, Din, Length, series, bar)
        self.m_f1 = self.m_Hg * self.m_f1 + self.m_Kg * series
        self.m_f2 = self.m_Kg * self.m_f1 + self.m_Hg * self.m_f2
        V1 = self.m_AC * self.m_f1 - self.m_AB * self.m_f2
        self.m_f3 = self.m_Hg * self.m_f3 + self.m_Kg * V1
        self.m_f4 = self.m_Kg * self.m_f3 + self.m_Hg * self.m_f4
        V2 = self.m_AC * self.m_f3 - self.m_AB * self.m_f4
        self.m_f5 = self.m_Hg * self.m_f5 + self.m_Kg * V2
        self.m_f6 = self.m_Kg * self.m_f5 + self.m_Hg * self.m_f6
        JurX_ = self.m_AC * self.m_f5 - self.m_AB * self.m_f6
        if self.BarCheck5(rates_total, bar, set):
            self.m_f1, self.m_f2, self.m_f3 = self.m_F1, self.m_F2, self.m_F3
            self.m_f4, self.m_f5, self.m_f6 = self.m_F4, self.m_F5, self.m_F6
        if self.BarCheck4(rates_total, bar, set):
            self.m_F1, self.m_F2, self.m_F3 = self.m_f1, self.m_f2, self.m_f3
            self.m_F4, self.m_F5, self.m_F6 = self.m_f4, self.m_f5, self.m_f6
        return JurX_


# ================================================================== CParMA


class CParMA(CMovSeriesTools):
    """Parabolic MA: least-squares parabola through the last ``Length`` bars,
    evaluated at the newest bar."""

    def __init__(self):
        self.m_SeriesArray: list = []
        self.m_Size_ = 0
        self.m_count = 0
        self.m_sum_x = self.m_sum_x2 = self.m_sum_x3 = self.m_sum_x4 = 0

    def ParMAInit(self, Length):
        self.m_sum_x = 0
        self.m_sum_x2 = 0
        self.m_sum_x3 = 0
        self.m_sum_x4 = 0
        iii = 1
        while iii <= Length:
            var_tmp = iii
            self.m_sum_x = as_int32(self.m_sum_x + var_tmp)
            var_tmp = as_int32(var_tmp * iii)
            self.m_sum_x2 = as_int32(self.m_sum_x2 + var_tmp)
            var_tmp = as_int32(var_tmp * iii)
            self.m_sum_x3 = as_int32(self.m_sum_x3 + var_tmp)
            var_tmp = as_int32(var_tmp * iii)
            self.m_sum_x4 = as_int32(self.m_sum_x4 + var_tmp)
            iii += 1

    def ParMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set):
        begin, bar, Length = int(begin), int(bar), int(Length)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        if bar == begin:
            self.m_Size_ = self.SeriesArrayResize("ParMASeries", Length, self.m_SeriesArray, self.m_Size_)
        Length = self.LengthCheck(Length)
        self.m_count = self.Recount_ArrayZeroPos(self.m_count, Length, prev_calculated,
                                                 rates_total, series, bar, self.m_SeriesArray, set)
        if self.BarCheck2(begin, bar, set, Length):
            self.ParMAInit(Length)
        elif self.BarCheck3(begin, bar, set, Length):
            return EMPTY_VALUE
        sum_y = 0.0
        sum_xy = 0.0
        sum_x2y = 0.0
        for iii in range(1, Length + 1):
            kkk = self.Recount_ArrayNumber(self.m_count, Length, Length - iii)
            var_tmp = self.m_SeriesArray[kkk]
            sum_y += var_tmp
            sum_xy += iii * var_tmp
            sum_x2y += iii * iii * var_tmp
        A = float(Length)
        B = float(self.m_sum_x)
        C = float(self.m_sum_x2)
        F = float(self.m_sum_x3)
        M = float(self.m_sum_x4)
        P = sum_y
        R = sum_xy
        S = sum_x2y
        D = B
        E = C
        K = C
        L = F
        Q = D / A
        E = E - Q * B
        F = F - Q * C
        R = R - Q * P
        Q = K / A
        L = L - Q * B
        M = M - Q * C
        S = S - Q * P
        Q = fdiv(L, E)
        B2 = fdiv(S - R * Q, M - F * Q)
        B1 = fdiv(R - F * B2, E)
        B0 = (P - B * B1 - C * B2) / A
        return B0 + (B1 + B2 * A) * A


# ==================================================================== CCMO


class CCMO(CMovSeriesTools):
    """Chande's |CMO| and the VIDYA built on it."""

    def __init__(self):
        self.m_dSeriesArray: list = []
        self.m_Size_ = 0
        self.m_count = 0
        self.m_UpSum_ = self.m_UpSum = self.m_DnSum_ = self.m_DnSum = 0.0
        self.m_Vidya = self.m_Vidya_ = 0.0
        self.m_AbsCMO_ = self.m_AbsCMO = 0.0
        self.m_series1 = self.m_series1_ = self.m_SmoothFactor = 0.0

    def CMOSeries(self, begin, prev_calculated, rates_total, CMO_Length, series, bar, set):
        begin, bar, CMO_Length = int(begin), int(bar), int(CMO_Length)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        size = CMO_Length + 1
        if bar == begin:
            self.m_Size_ = self.SeriesArrayResize("CMOSeries", size, self.m_dSeriesArray, self.m_Size_)
        CMO_Length = self.LengthCheck(CMO_Length)
        # The first bar returns before m_series1 is ever set, so the change
        # stored at begin+1 is measured from 0. It falls outside every window.
        if self.BarCheck1(begin + 1, bar, set):
            return EMPTY_VALUE
        self.m_count = self.Recount_ArrayZeroPos(self.m_count, size, prev_calculated, rates_total,
                                                 series - self.m_series1, bar,
                                                 self.m_dSeriesArray, set)
        if self.BarCheck2(begin, bar, set, CMO_Length + 3):
            self.m_UpSum = 0.0
            self.m_DnSum = 0.0
            for iii in range(1, CMO_Length):
                rrr = self.Recount_ArrayNumber(self.m_count, size, iii)
                dseries = self.m_dSeriesArray[rrr]
                if dseries > 0:
                    self.m_UpSum += dseries
                if dseries < 0:
                    self.m_DnSum -= dseries
            self.m_AbsCMO = 0.000000001
        elif self.BarCheck3(begin, bar, set, CMO_Length + 3):
            self.m_series1 = series
            return EMPTY_VALUE
        dseries = self.m_dSeriesArray[self.m_count]
        if dseries > 0:
            self.m_UpSum += dseries
        if dseries < 0:
            self.m_DnSum -= dseries
        if self.m_UpSum + self.m_DnSum > 0:
            self.m_AbsCMO = MathAbs((self.m_UpSum - self.m_DnSum) / (self.m_UpSum + self.m_DnSum))
        abcmo = self.m_AbsCMO
        rrr = self.Recount_ArrayNumber(self.m_count, size, CMO_Length - 1)
        dseries = self.m_dSeriesArray[rrr]
        if dseries > 0:
            self.m_UpSum -= dseries
        if dseries < 0:
            self.m_DnSum += dseries
        if self.BarCheck5(rates_total, bar, set):
            self.m_AbsCMO = self.m_AbsCMO_
            self.m_UpSum = self.m_UpSum_
            self.m_DnSum = self.m_DnSum_
            self.m_series1 = self.m_series1_
        else:
            self.m_series1 = series
        if self.BarCheck4(rates_total, bar, set):
            self.m_AbsCMO_ = self.m_AbsCMO
            self.m_UpSum_ = self.m_UpSum
            self.m_DnSum_ = self.m_DnSum
            self.m_series1_ = self.m_series1
        return abcmo

    def VIDYASeries(self, begin, prev_calculated, rates_total, CMO_Length, EMA_Length,
                    series, bar, set):
        CMO_ = self.CMOSeries(begin, prev_calculated, rates_total, CMO_Length, series, bar, set)
        begin, bar, CMO_Length = int(begin), int(bar), int(CMO_Length)
        if self.BarCheck2(begin, bar, set, CMO_Length + 3):
            self.m_Vidya = series
            self.m_SmoothFactor = 2.0 / (EMA_Length + 1.0)
        elif self.BarCheck3(begin, bar, set, CMO_Length + 3):
            return EMPTY_VALUE
        CMO_ *= self.m_SmoothFactor
        self.m_Vidya = CMO_ * series + (1 - CMO_) * self.m_Vidya
        vidya = self.m_Vidya
        if self.BarCheck5(rates_total, bar, set):
            self.m_Vidya = self.m_Vidya_
        if self.BarCheck4(rates_total, bar, set):
            self.m_Vidya_ = self.m_Vidya
        return vidya


# ==================================================================== CAMA


class CAMA(CMovSeriesTools):
    """Kaufman's adaptive MA with the smoothing constant raised to ``Rate``."""

    def __init__(self):
        self.m_SeriesArray: list = []
        self.m_dSeriesArray: list = []
        self.m_NOISE = self.m_noise = 0.0
        self.m_Ama = self.m_AMA_ = self.m_slowSC = self.m_fastSC = self.m_dSC = 0.0
        self.m_Size_1 = self.m_Size_2 = 0
        self.m_count = 0

    def AMASeries(self, begin, prev_calculated, rates_total, Length, Fast_Length,
                  Slow_Length, Rate, series, bar, set):
        begin, bar, Length = int(begin), int(bar), int(Length)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        size = Length + 1
        if bar == begin:
            self.m_Size_1 = self.SeriesArrayResize("AMASeries", size, self.m_SeriesArray, self.m_Size_1)
            self.m_Size_2 = self.SeriesArrayResize("AMASeries", size, self.m_dSeriesArray, self.m_Size_2)
        Length = self.LengthCheck(Length)
        self.m_count = self.Recount_ArrayZeroPos(self.m_count, size, prev_calculated,
                                                 rates_total, series, bar, self.m_SeriesArray, set)
        if self.BarCheck1(begin + 1, bar, set):
            return EMPTY_VALUE
        kkk = self.Recount_ArrayNumber(self.m_count, size, 1)
        dprice = series - self.m_SeriesArray[kkk]
        self.m_dSeriesArray[self.m_count] = dprice
        if self.BarCheck2(begin, bar, set, Length + 3):
            rrr = self.Recount_ArrayNumber(self.m_count, size, 1)
            self.m_Ama = self.m_SeriesArray[rrr]
            self.m_slowSC = (2.0 / (Slow_Length + 1))
            self.m_fastSC = (2.0 / (Fast_Length + 1))
            self.m_dSC = self.m_fastSC - self.m_slowSC
            self.m_noise = 0.000000001
            for iii in range(1, Length):
                rrr = self.Recount_ArrayNumber(self.m_count, size, iii)
                self.m_noise += MathAbs(self.m_dSeriesArray[rrr])
        elif self.BarCheck3(begin, bar, set, Length + 3):
            return EMPTY_VALUE
        self.m_noise += MathAbs(dprice)
        rrr = self.Recount_ArrayNumber(self.m_count, size, Length)
        signal = MathAbs(series - self.m_SeriesArray[rrr])
        ER = fdiv(signal, self.m_noise)
        ERSC = ER * self.m_dSC
        SSC = ERSC + self.m_slowSC
        self.m_Ama = self.m_Ama + (MathPow(SSC, Rate) * (series - self.m_Ama))
        ama = self.m_Ama
        kkk = self.Recount_ArrayNumber(self.m_count, size, Length - 1)
        self.m_noise -= MathAbs(self.m_dSeriesArray[kkk])
        if self.BarCheck5(rates_total, bar, set):
            self.m_noise = self.m_NOISE
            self.m_Ama = self.m_AMA_
        if self.BarCheck4(rates_total, bar, set):
            self.m_AMA_ = self.m_Ama
            self.m_NOISE = self.m_noise
        return ama


# ================================================ momentum / rate of change


class _LagBase(CMovSeriesTools):
    def __init__(self):
        self.m_SeriesArray: list = []
        self.m_Size_ = 0
        self.m_count = 0

    def _lagged(self, name, begin, prev_calculated, rates_total, Length, series, bar, set):
        """Returns (series, value Length bars ago) or None during warm-up."""
        begin, bar, Length = int(begin), int(bar), int(Length)
        if self.BarCheck1(begin, bar, set):
            return None
        Length_ = Length + 1
        Length = self.LengthCheck(Length)
        if bar == begin:
            self.m_Size_ = self.SeriesArrayResize(name, Length_, self.m_SeriesArray, self.m_Size_)
        self.m_count = self.Recount_ArrayZeroPos(self.m_count, Length_, prev_calculated,
                                                 rates_total, series, bar, self.m_SeriesArray, set)
        if self.BarCheck3(begin, bar, set, Length_):
            return None
        kkk = self.Recount_ArrayNumber(self.m_count, Length_, Length)
        return self.m_SeriesArray[kkk]


class CMomentum(_LagBase):
    def MomentumSeries(self, begin, prev_calculated, rates_total, Length, series, bar, set):
        old = self._lagged("MomentumSeries", begin, prev_calculated, rates_total, Length, series, bar, set)
        return EMPTY_VALUE if old is None else series - old


class CnMomentum(_LagBase):
    """Normalised momentum: (price − price[Length]) / price[Length]."""

    def nMomentumSeries(self, begin, prev_calculated, rates_total, Length, series, bar, set):
        old = self._lagged("nMomentumSeries", begin, prev_calculated, rates_total, Length, series, bar, set)
        return EMPTY_VALUE if old is None else fdiv(series - old, old)


class CROC(_LagBase):
    """Rate of change as a percentage: 100 · price / price[Length]."""

    def ROCSeries(self, begin, prev_calculated, rates_total, Length, series, bar, set):
        old = self._lagged("ROCSeries", begin, prev_calculated, rates_total, Length, series, bar, set)
        return EMPTY_VALUE if old is None else fdiv(100 * series, old)


# =========================================== FATL / SATL / RFTL / RSTL filters

FATL_TABLE = (
    +0.4360409450, +0.3658689069, +0.2460452079, +0.1104506886, -0.0054034585, -0.0760367731,
    -0.0933058722, -0.0670110374, -0.0190795053, +0.0259609206, +0.0502044896, +0.0477818607,
    +0.0249252327, -0.0047706151, -0.0272432537, -0.0338917071, -0.0244141482, -0.0055774838,
    +0.0128149838, +0.0226522218, +0.0208778257, +0.0100299086, -0.0036771622, -0.0136744850,
    -0.0160483392, -0.0108597376, -0.0016060704, +0.0069480557, +0.0110573605, +0.0095711419,
    +0.0040444064, -0.0023824623, -0.0067093714, -0.0072003400, -0.0047717710, +0.0005541115,
    +0.0007860160, +0.0130129076, +0.0040364019,
)
SATL_TABLE = (
    +0.0982862174, +0.0975682269, +0.0961401078, +0.0940230544, +0.0912437090, +0.0878391006,
    +0.0838544303, +0.0793406350, +0.0743569346, +0.0689666682, +0.0632381578, +0.0572428925,
    +0.0510534242, +0.0447468229, +0.0383959950, +0.0320735368, +0.0258537721, +0.0198005183,
    +0.0139807863, +0.0084512448, +0.0032639979, -0.0015350359, -0.0059060082, -0.0098190256,
    -0.0132507215, -0.0161875265, -0.0186164872, -0.0205446727, -0.0219739146, -0.0229204861,
    -0.0234080863, -0.0234566315, -0.0231017777, -0.0223796900, -0.0213300463, -0.0199924534,
    -0.0184126992, -0.0166377699, -0.0147139428, -0.0126796776, -0.0105938331, -0.0084736770,
    -0.0063841850, -0.0043466731, -0.0023956944, -0.0005535180, +0.0011421469, +0.0026845693,
    +0.0040471369, +0.0052380201, +0.0062194591, +0.0070340085, +0.0076266453, +0.0080376628,
    +0.0083037666, +0.0083694798, +0.0082901022, +0.0080741359, +0.0077543820, +0.0073260526,
    +0.0068163569, +0.0062325477, +0.0056078229, +0.0049516078, +0.0161380976,
)
RFTL_TABLE = (
    -0.0025097319, +0.0513007762, +0.1142800493, +0.1699342860, +0.2025269304,
    +0.2025269304, +0.1699342860, +0.1142800493, +0.0513007762, -0.0025097319,
    -0.0353166244, -0.0433375629, -0.0311244617, -0.0088618137, +0.0120580088,
    +0.0233183633, +0.0221931304, +0.0115769653, -0.0022157966, -0.0126536111,
    -0.0157416029, -0.0113395830, -0.0025905610, +0.0059521459, +0.0105212252,
    +0.0096970755, +0.0046585685, -0.0017079230, -0.0063513565, -0.0074539350,
    -0.0050439973, -0.0007459678, +0.0032271474, +0.0051357867, +0.0044454862,
    +0.0018784961, -0.0011065767, -0.0031162862, -0.0033443253, -0.0022163335,
    +0.0002573669, +0.0003650790, +0.0060440751, +0.0018747783,
)
RSTL_TABLE = (
    -0.00514293, -0.00398417, -0.00262594, -0.00107121, +0.00066887, +0.00258172, +0.00465269,
    +0.00686394, +0.00919334, +0.01161720, +0.01411056, +0.01664635, +0.01919533, +0.02172747,
    +0.02421320, +0.02662203, +0.02892446, +0.03109071, +0.03309496, +0.03490921, +0.03651145,
    +0.03788045, +0.03899804, +0.03984915, +0.04042329, +0.04071263, +0.04071263, +0.04042329,
    +0.03984915, +0.03899804, +0.03788045, +0.03651145, +0.03490921, +0.03309496, +0.03109071,
    +0.02892446, +0.02662203, +0.02421320, +0.02172747, +0.01919533, +0.01664635, +0.01411056,
    +0.01161720, +0.00919334, +0.00686394, +0.00465269, +0.00258172, +0.00066887, -0.00107121,
    -0.00262594, -0.00398417, -0.00514293, -0.00609634, -0.00684602, -0.00739452, -0.00774847,
    -0.00791630, -0.00790940, -0.00774085, -0.00742482, -0.00697718, -0.00641613, -0.00576108,
    -0.00502957, -0.00423873, -0.00340812, -0.00255923, -0.00170217, -0.00085902, -0.00004113,
    +0.00073700, +0.00146422, +0.00213007, +0.00272649, +0.00324752, +0.00368922, +0.00405000,
    +0.00433024, +0.00453068, +0.00465046, +0.00469058, +0.00466041, +0.00457855, +0.00442491,
    +0.00423019, +0.00399201, +0.00372169, +0.00342736, +0.00311822, +0.00280309, +0.00249088,
    +0.00219089, +0.00191283, +0.00166683, +0.00146419, +0.00131867, +0.00124645, +0.00126836,
    -0.00401854,
)


class _DigitalFilter(CMovSeriesTools):
    """Shared body of CFATL / CSATL / CRFTL / CRSTL: a fixed FIR filter,
    ``sum(table[k] * price[bar-k])``, newest bar weighted by ``table[0]``."""

    TABLE: tuple = ()

    def __init__(self):
        self.m_Size_ = len(self.TABLE)
        self.m_SeriesArray = [0.0] * self.m_Size_
        self.m_count = 0
        self.m_value = 0.0               # m_FATL / m_SATL / m_RFTL / m_RSTL
        self._table = self.TABLE

    def _series(self, begin, prev_calculated, rates_total, series, bar, set):
        begin, bar = int(begin), int(bar)
        if self.BarCheck1(begin, bar, set):
            return EMPTY_VALUE
        size = self.m_Size_
        self.m_count = self.Recount_ArrayZeroPos(self.m_count, size, prev_calculated,
                                                 rates_total, series, bar, self.m_SeriesArray, set)
        if self.BarCheck3(begin, bar, set, size):
            return EMPTY_VALUE
        table, arr, count = self._table, self.m_SeriesArray, self.m_count
        value = 0.0
        if self.BarCheck5(rates_total, bar, set):
            # On the newest bar the older taps are cached between ticks.
            if prev_calculated != rates_total:
                self.m_value = 0.0
                for iii in range(1, size):
                    self.m_value += table[iii] * arr[self.Recount_ArrayNumber(count, size, iii)]
            value = self.m_value + table[0] * arr[self.Recount_ArrayNumber(count, size, 0)]
        else:
            for iii in range(size):
                value += table[iii] * arr[self.Recount_ArrayNumber(count, size, iii)]
        return value


class CFATL(_DigitalFilter):
    TABLE = FATL_TABLE

    def FATLSeries(self, begin, prev_calculated, rates_total, series, bar, set):
        return self._series(begin, prev_calculated, rates_total, series, bar, set)


class CSATL(_DigitalFilter):
    TABLE = SATL_TABLE

    def SATLSeries(self, begin, prev_calculated, rates_total, series, bar, set):
        return self._series(begin, prev_calculated, rates_total, series, bar, set)


class CRFTL(_DigitalFilter):
    TABLE = RFTL_TABLE

    def RFTLSeries(self, begin, prev_calculated, rates_total, series, bar, set):
        return self._series(begin, prev_calculated, rates_total, series, bar, set)


class CRSTL(_DigitalFilter):
    TABLE = RSTL_TABLE

    def RSTLSeries(self, begin, prev_calculated, rates_total, series, bar, set):
        return self._series(begin, prev_calculated, rates_total, series, bar, set)


# ==================================================================== CXMA


def GetStartBars(Method: int, Length: int, Phase: int) -> int:
    """Bars a smoothing method needs before its first value."""
    return {
        MODE_SMA_: Length, MODE_EMA_: 0, MODE_SMMA_: Length + 1, MODE_LWMA_: Length,
        MODE_JJMA: 30, MODE_JurX: 0, MODE_ParMA: Length, MODE_T3: 0,
        MODE_VIDYA: Phase + 2, MODE_AMA: Length + 2,
    }.get(int(Method), 0)


class CXMA:
    """The universal smoother: one of ten methods, chosen on the first call.

    ``Phase`` is method-specific, as in the library: JJMA's phase (−100…+100),
    T3's curvature (volume factor × 100), VIDYA's CMO period, AMA's slow
    period. It is ignored by the others.
    """

    def __init__(self):
        self.m_init = False
        self.m_Method = None
        self._engine = None

    def XMAInit(self, Method: int) -> None:
        if self.m_init:
            return
        self.m_init = True
        self.m_Method = int(Method)
        Method = int(Method)
        if Method in (MODE_SMA_, MODE_EMA_, MODE_SMMA_, MODE_LWMA_):
            self._engine = CMoving_Average()
        elif Method == MODE_JJMA:
            self._engine = CJJMA()
        elif Method == MODE_JurX:
            self._engine = CJurX()
        elif Method == MODE_ParMA:
            self._engine = CParMA()
        elif Method == MODE_T3:
            self._engine = CT3()
        elif Method == MODE_VIDYA:
            self._engine = CCMO()
        elif Method == MODE_AMA:
            self._engine = CAMA()

    def XMASeries(self, begin, prev_calculated, rates_total, Method, Phase, Length,
                  series, bar, set):
        self.XMAInit(Method)
        Method = int(Method)
        Phase, Length = int(Phase), int(Length)
        e = self._engine
        if Method == MODE_SMA_:
            return e.SMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        if Method == MODE_EMA_:
            return e.EMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        if Method == MODE_SMMA_:
            return e.SMMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        if Method == MODE_LWMA_:
            return e.LWMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        if Method == MODE_JJMA:
            return e.JJMASeries(begin, prev_calculated, rates_total, 0, Phase, Length, series, bar, set)
        if Method == MODE_JurX:
            return e.JurXSeries(begin, prev_calculated, rates_total, 0, Length, series, bar, set)
        if Method == MODE_ParMA:
            return e.ParMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        if Method == MODE_T3:
            return e.T3Series(begin, prev_calculated, rates_total, 0, Phase, Length, series, bar, set)
        if Method == MODE_VIDYA:
            return e.VIDYASeries(begin, prev_calculated, rates_total, Phase, Length, series, bar, set)
        if Method == MODE_AMA:
            return e.AMASeries(begin, prev_calculated, rates_total, Length, 2, Phase, 2.0, series, bar, set)
        return 0.0

    GetStartBars = staticmethod(GetStartBars)

    @staticmethod
    def GetString_MA_Method(Method: int) -> str:
        # The source really does return " VIDYA" with a leading space.
        return " VIDYA" if int(Method) == MODE_VIDYA else SMOOTH_METHOD_NAMES.get(int(Method), "")

    def XMAPhaseCheck(self, PhaseName, ExternPhase, Method):
        """Prints a warning in MQL5 only."""

    def XMALengthCheck(self, LengthName, ExternLength):
        """Prints a warning in MQL5 only."""


# ============================================================ applied prices


def PriceSeries(applied_price, bar, Open, Low, High, Close) -> float:
    """``PriceSeries()`` — note the library's argument order (Open, Low, High,
    Close) and its extended 1-based applied-price numbering."""
    ap = int(applied_price)
    if ap == PRICE_CLOSE:
        return Close[bar]
    if ap == PRICE_OPEN:
        return Open[bar]
    if ap == PRICE_HIGH:
        return High[bar]
    if ap == PRICE_LOW:
        return Low[bar]
    if ap == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    if ap == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    if ap == PRICE_WEIGHTED:
        return (2 * Close[bar] + High[bar] + Low[bar]) / 4.0
    if ap == 8:
        return (Open[bar] + Close[bar]) / 2.0
    if ap == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    if ap == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        if Close[bar] < Open[bar]:
            return Low[bar]
        return Close[bar]
    if ap == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        if Close[bar] < Open[bar]:
            return (Low[bar] + Close[bar]) / 2.0
        return Close[bar]
    if ap == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return ((res - Low[bar]) + (res - High[bar])) / 2
    return Close[bar]


def price_series(applied_price, open_, low, high, close) -> np.ndarray:
    """:func:`PriceSeries` over whole forward-indexed arrays (vectorised)."""
    o = np.asarray(open_, dtype=float)
    l = np.asarray(low, dtype=float)
    h = np.asarray(high, dtype=float)
    c = np.asarray(close, dtype=float)
    ap = int(applied_price)
    if ap == 2:
        return o.copy()
    if ap == 3:
        return h.copy()
    if ap == 4:
        return l.copy()
    if ap == 5:
        return (h + l) / 2.0
    if ap == 6:
        return (c + h + l) / 3.0
    if ap == 7:
        return (2 * c + h + l) / 4.0
    if ap == 8:
        return (o + c) / 2.0
    if ap == 9:
        return (o + c + h + l) / 4.0
    if ap == 10:
        return np.where(c > o, h, np.where(c < o, l, c))
    if ap == 11:
        return np.where(c > o, (h + c) / 2.0, np.where(c < o, (l + c) / 2.0, c))
    if ap == 12:
        res = h + l + c
        res = np.where(c < o, (res + l) / 2, np.where(c > o, (res + h) / 2, (res + c) / 2))
        return ((res - l) + (res - h)) / 2
    return c.copy()


def iPriceSeries(rates, applied_price, bar, set) -> float:
    """``iPriceSeries(symbol, timeframe, applied_price, bar, set)``.

    The MQL5 version reads another symbol/timeframe with ``CopyXxx``. Here
    ``rates`` stands in for that (symbol, timeframe): any object with
    forward-indexed ``open``/``high``/``low``/``close`` (a bar DataFrame works).
    ``set=False`` means ``bar`` counts from the oldest bar, ``set=True`` from
    the newest — the same convention as the source.
    """
    o, h, l, c = (np.asarray(rates[k], dtype=float) for k in ("open", "high", "low", "close"))
    n = len(c)
    index = int(bar) if not set else n - 1 - int(bar)
    return PriceSeries(applied_price, index, o, l, h, c)


def bPriceSeries(rates, rates_total, applied_price, bar, set):
    """``bPriceSeries(...)`` → ``(ok, Price_)``. See :func:`iPriceSeries`."""
    o, h, l, c = (np.asarray(rates[k], dtype=float) for k in ("open", "high", "low", "close"))
    Bar = int(rates_total) - 1 - int(bar) if not set else int(bar)   # series index
    index = len(c) - 1 - Bar
    if not 0 <= index < len(c):
        return False, 0.0
    return True, PriceSeries(applied_price, index, o, l, h, c)


def bPriceSeriesOnArray(rates, applied_price, start_pos, count):
    """``bPriceSeriesOnArray(...)`` → ``(ok, series)`` with ``series`` in
    *series* order (index 0 = newest), as the source returns it."""
    o, h, l, c = (np.asarray(rates[k], dtype=float) for k in ("open", "high", "low", "close"))
    full = price_series(applied_price, o, l, h, c)[::-1]
    start_pos, count = int(start_pos), int(count)
    if start_pos < 0 or start_pos + count > len(full):
        return False, np.empty(0)
    return True, full[start_pos:start_pos + count].copy()


def iPriceSeriesAlert(applied_price) -> None:
    """Only raises a terminal alert for out-of-range input in MQL5."""


# ===================================================== whole-array wrappers


def _run(values, begin, call) -> np.ndarray:
    values = np.asarray(values, dtype=float).tolist()     # Python floats: MQL-like scalar maths
    n = len(values)
    out = np.full(n, np.nan)
    begin = max(int(begin), 0)
    for bar in range(begin, n):
        out[bar] = call(0, n, values[bar], bar)
    return to_nan(out)


def xma_series(values, method: int, length: int, phase: int = 0, begin: int = 0) -> np.ndarray:
    """``CXMA::XMASeries`` over a whole forward-indexed array (one pass,
    ``prev_calculated = 0``). NaN where the library returns EMPTY_VALUE."""
    x = CXMA()
    return _run(values, begin, lambda pc, rt, v, bar: x.XMASeries(
        begin, pc, rt, method, phase, length, v, bar, False))


def ma_series(values, length: int, ma_method: int = MODE_SMA, begin: int = 0) -> np.ndarray:
    m = CMoving_Average()
    return _run(values, begin, lambda pc, rt, v, bar: m.MASeries(
        begin, pc, rt, length, ma_method, v, bar, False))


def jjma_series(values, length: float, phase: float, begin: int = 0) -> np.ndarray:
    j = CJJMA()
    return _run(values, begin, lambda pc, rt, v, bar: j.JJMASeries(
        begin, pc, rt, 0, phase, length, v, bar, False))


def stddev_series(values, mov, length: int, deviation: float = 1.0, begin: int = 0) -> np.ndarray:
    """``CStdDeviation::StdDevSeries`` with ``mov`` the average per bar
    (NaN in ``mov`` is passed through as EMPTY_VALUE, as the source would)."""
    values = np.asarray(values, dtype=float).tolist()
    mov = np.asarray(mov, dtype=float)
    mov = np.where(np.isnan(mov), EMPTY_VALUE, mov).tolist()
    s = CStdDeviation()
    n = len(values)
    out = np.full(n, np.nan)
    begin = max(int(begin), 0)
    for bar in range(begin, n):
        out[bar] = s.StdDevSeries(begin, 0, n, length, deviation, values[bar], mov[bar], bar, False)
    return to_nan(out)


def _filter_series(cls, method, values, begin):
    f = cls()
    fn = getattr(f, method)
    return _run(values, begin, lambda pc, rt, v, bar: fn(begin, pc, rt, v, bar, False))


def fatl_series(values, begin: int = 0) -> np.ndarray:
    return _filter_series(CFATL, "FATLSeries", values, begin)


def satl_series(values, begin: int = 0) -> np.ndarray:
    return _filter_series(CSATL, "SATLSeries", values, begin)


def rftl_series(values, begin: int = 0) -> np.ndarray:
    return _filter_series(CRFTL, "RFTLSeries", values, begin)


def rstl_series(values, begin: int = 0) -> np.ndarray:
    return _filter_series(CRSTL, "RSTLSeries", values, begin)


def momentum_series(values, length: int, begin: int = 0) -> np.ndarray:
    m = CMomentum()
    return _run(values, begin, lambda pc, rt, v, bar: m.MomentumSeries(begin, pc, rt, length, v, bar, False))


def nmomentum_series(values, length: int, begin: int = 0) -> np.ndarray:
    m = CnMomentum()
    return _run(values, begin, lambda pc, rt, v, bar: m.nMomentumSeries(begin, pc, rt, length, v, bar, False))


def roc_series(values, length: int, begin: int = 0) -> np.ndarray:
    m = CROC()
    return _run(values, begin, lambda pc, rt, v, bar: m.ROCSeries(begin, pc, rt, length, v, bar, False))


def cmo_series(values, length: int, begin: int = 0) -> np.ndarray:
    c = CCMO()
    return _run(values, begin, lambda pc, rt, v, bar: c.CMOSeries(begin, pc, rt, length, v, bar, False))
