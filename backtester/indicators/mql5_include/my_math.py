"""``MyMath`` (A. Emelyanov, 2014) — line-by-line ports of
``MyMath/Extremum/MyCExtremum.mqh``, ``MyMath/Pattern/MyCPattern.mqh`` and
``MyMath/Pattern/MyCPatternZigzag.mqh`` (used by the FivePattern indicator).

- ``MyCExtremum``: the classic MetaQuotes ZigZag in three flavours —
  ``GetClassicZigzag`` (forward-indexed arrays), ``GetModZigzag`` (series-
  indexed), and the high/low maps on their own.
- ``MyCPattern``: Merrill's 32 five-point M/W patterns (A…E), their
  "evolution" and "mutation" successors, and the Fibonacci correction of an
  unfinished point E.
- ``MyCPatternZigzag``: finds A…E on the zigzag, classifies the pattern,
  keeps evolution/mutation statistics and projects the next points.

``_Point``/``_Digits`` come from the ``point``/``digits`` attributes (set them
from the chart: ``mql5.point(df)``, ``mql5.digits(df)``). ``EnumToString`` of
a pattern is :func:`pattern_name`. The chart comment (``MyCComment``) is a
chart-text object; attach any object with ``AddLineOfIndex(i, text)`` to
receive the lines ``PrintComment`` would write.
"""

from __future__ import annotations

from .mql_runtime import NormalizeDouble, fdiv, idiv

EXTREMUM_RESERVE = 1000
PATTERN_ZIG_RESERVE = 50
# enum looling_for
Pike, Sill = 1, -1


# ============================================================ MyCExtremum


class MyCExtremum:
    def __init__(self, point: float = 0.00001):
        self.HighMapBuffer: list = []
        self.LowMapBuffer: list = []
        self.ZigzagBuffer: list = []
        self.point = point

    @staticmethod
    def iHighest(array, depth: int, startPos: int) -> int:
        index = startPos
        if startPos < 0:
            return 0
        if startPos - depth < 0:
            depth = startPos
        mx = array[startPos]
        i = startPos
        while i > startPos - depth:
            if array[i] > mx:
                index = i
                mx = array[i]
            i -= 1
        return index

    @staticmethod
    def iLowest(array, depth: int, startPos: int) -> int:
        index = startPos
        if startPos < 0:
            return 0
        if startPos - depth < 0:
            depth = startPos
        mn = array[startPos]
        i = startPos
        while i > startPos - depth:
            if array[i] < mn:
                index = i
                mn = array[i]
            i -= 1
        return index

    def GetHighMapZigzag(self, inp, ExtDepth, ExtDeviation, ExtBackstep) -> int:
        lasthigh = 0.0
        rates_total = len(inp)
        deviation = ExtDeviation * self.point
        if rates_total < 100:
            return -1
        self.HighMapBuffer = [0.0] * rates_total
        H = self.HighMapBuffer
        for shift in range(ExtDepth, rates_total):
            val = inp[self.iHighest(inp, ExtDepth, shift)]
            if val == lasthigh:
                val = 0.0
            else:
                lasthigh = val
                if (val - inp[shift]) > deviation:
                    val = 0.0
                else:
                    for back in range(1, ExtBackstep + 1):
                        res = H[shift - back]
                        if res != 0 and res < val:
                            H[shift - back] = 0.0
            H[shift] = val if inp[shift] == val else 0.0
        return rates_total

    def GetLowMapZigzag(self, inp, ExtDepth, ExtDeviation, ExtBackstep) -> int:
        lastlow = 0.0
        rates_total = len(inp)
        deviation = ExtDeviation * self.point
        if rates_total < 100:
            return -1
        self.LowMapBuffer = [0.0] * rates_total
        Lb = self.LowMapBuffer
        for shift in range(ExtDepth, rates_total):
            val = inp[self.iLowest(inp, ExtDepth, shift)]
            if val == lastlow:
                val = 0.0
            else:
                lastlow = val
                if (inp[shift] - val) > deviation:
                    val = 0.0
                else:
                    for back in range(1, ExtBackstep + 1):
                        res = Lb[shift - back]
                        if res != 0 and res > val:
                            Lb[shift - back] = 0.0
            Lb[shift] = val if inp[shift] == val else 0.0
        return rates_total

    def CorrectMapClassicZigzag(self) -> None:
        Z, H, Lb = self.ZigzagBuffer, self.HighMapBuffer, self.LowMapBuffer
        for i in range(len(Z) - 1):
            if Z[i] != 0:
                if Lb[i] != 0:
                    for a in range(i, 0, -1):
                        if H[a] != 0:
                            Z[a] = H[a]
                            return
                    return
                if H[i] != 0:
                    for a in range(i, 0, -1):
                        if Lb[a] != 0:
                            Z[a] = Lb[a]
                            return
                    return

    def _walk(self, high, low, shifts, apply_correction: bool) -> None:
        Z, H, Lb = self.ZigzagBuffer, self.HighMapBuffer, self.LowMapBuffer
        whatlookfor = 0
        lasthighpos = lastlowpos = 0
        lasthigh = lastlow = 0.0
        for shift in shifts:
            if whatlookfor == 0:
                if lastlow == 0 and lasthigh == 0:
                    if H[shift] != 0:
                        lasthigh = high[shift]
                        lasthighpos = shift
                        whatlookfor = Sill
                        Z[shift] = lasthigh
                    if Lb[shift] != 0:
                        lastlow = low[shift]
                        lastlowpos = shift
                        whatlookfor = Pike
                        Z[shift] = lastlow
            elif whatlookfor == Pike:
                if Lb[shift] != 0.0 and Lb[shift] < lastlow and H[shift] == 0.0:
                    Z[lastlowpos] = 0.0
                    lastlowpos = shift
                    lastlow = Lb[shift]
                    Z[shift] = lastlow
                if H[shift] != 0.0 and Lb[shift] == 0.0:
                    lasthigh = H[shift]
                    lasthighpos = shift
                    Z[shift] = lasthigh
                    whatlookfor = Sill
            elif whatlookfor == Sill:
                if H[shift] != 0.0 and H[shift] > lasthigh and Lb[shift] == 0.0:
                    Z[lasthighpos] = 0.0
                    lasthighpos = shift
                    lasthigh = H[shift]
                    Z[shift] = lasthigh
                if Lb[shift] != 0.0 and H[shift] == 0.0:
                    lastlow = Lb[shift]
                    lastlowpos = shift
                    Z[shift] = lastlow
                    whatlookfor = Pike
        if apply_correction:
            self.CorrectMapClassicZigzag()

    def GetClassicZigzag(self, high, low, ExtDepth, ExtDeviation, ExtBackstep) -> int:
        """Forward-indexed ``high``/``low`` (bar 0 = oldest)."""
        rates_total = min(len(high), len(low))
        if rates_total < 100:
            return -1
        self.ZigzagBuffer = [0.0] * rates_total
        if self.GetHighMapZigzag(high, ExtDepth, ExtDeviation, ExtBackstep) < 0:
            return 0
        if self.GetLowMapZigzag(low, ExtDepth, ExtDeviation, ExtBackstep) < 0:
            return 0
        self._walk(high, low, range(ExtDepth, rates_total), apply_correction=True)
        return rates_total

    def _GetHighMapZigzag(self, inp, ExtDepth, ExtDeviation, ExtBackstep) -> int:
        lasthigh = 0.0
        rates_total = len(inp)
        limit = rates_total - ExtDepth
        deviation = ExtDeviation * self.point
        if rates_total < 100:
            return -1
        self.HighMapBuffer = [0.0] * rates_total
        H = self.HighMapBuffer
        for shift in range(limit, -1, -1):
            val = inp[self.iHighest(inp, ExtDepth, shift)]
            if val == lasthigh:
                val = 0.0
            else:
                lasthigh = val
                if (val - inp[shift]) > deviation:
                    val = 0.0
                else:
                    for back in range(1, ExtBackstep + 1):
                        res = H[shift + back]
                        if res != 0 and res < val:
                            H[shift + back] = 0.0
            H[shift + 1] = val if inp[shift] == val else 0.0
        self.CorrectMapHigh(inp)
        return rates_total

    def _GetLowMapZigzag(self, inp, ExtDepth, ExtDeviation, ExtBackstep) -> int:
        lastlow = 0.0
        rates_total = len(inp)
        limit = rates_total - ExtDepth
        deviation = ExtDeviation * self.point
        if rates_total < 100:
            return -1
        self.LowMapBuffer = [0.0] * rates_total
        Lb = self.LowMapBuffer
        for shift in range(limit, -1, -1):
            val = inp[self.iLowest(inp, ExtDepth, shift)]
            if val == lastlow:
                val = 0.0
            else:
                lastlow = val
                if (inp[shift] - val) > deviation:
                    val = 0.0
                else:
                    for back in range(1, ExtBackstep + 1):
                        res = Lb[shift + back]
                        if res != 0 and res > val:
                            Lb[shift + back] = 0.0
            Lb[shift + 1] = val if inp[shift] == val else 0.0
        self.CorrectMapLow(inp)
        return rates_total

    def CorrectMapHigh(self, inp) -> None:
        for i in range(len(self.HighMapBuffer)):
            if self.HighMapBuffer[i] != 0:
                self.HighMapBuffer[i] = inp[i]

    def CorrectMapLow(self, inp) -> None:
        for i in range(len(self.LowMapBuffer)):
            if self.LowMapBuffer[i] != 0:
                self.LowMapBuffer[i] = inp[i]

    def CorrectMapZigzag(self) -> None:
        for i in range(len(self.HighMapBuffer)):
            if self.HighMapBuffer[i] != 0 and self.LowMapBuffer[i] != 0:
                self.HighMapBuffer[i] = 0.0
                self.LowMapBuffer[i] = 0.0

    def GetModZigzag(self, high, low, ExtDepth, ExtDeviation, ExtBackstep) -> int:
        """Series-indexed ``high``/``low`` (index 0 = newest)."""
        rates_total = min(len(high), len(low))
        limit = rates_total - ExtDepth
        if rates_total < 100:
            return -1
        self.ZigzagBuffer = [0.0] * rates_total
        if self._GetHighMapZigzag(high, ExtDepth, ExtDeviation, ExtBackstep) < 0:
            return 0
        if self._GetLowMapZigzag(low, ExtDepth, ExtDeviation, ExtBackstep) < 0:
            return 0
        self.CorrectMapZigzag()
        self._walk(high, low, range(limit, -1, -1), apply_correction=False)
        return rates_total


# ============================================================ MyCPattern

# enum NamePattern
ERROR, NOPATTERN = 2, 3
W15, W16, M8, M4, M3, W9, W13, W14 = 8, 12, 64, 80, 112, 512, 640, 896
M13, M12, M7, W4, W5, W10, M11, M10 = 4096, 5120, 7168, 32768, 40960, 57344, 262144, 327680
M5, M6, M16, M15, M14, M9 = 393216, 458752, 2097152, 2621440, 3145728, 3670016
W1, W2, W3, W8, W6, W7 = 16777216, 20971520, 25165824, 29360128, 134217728, 167772160
W11, W12, M1, M2 = 201326592, 234881024, 536870912, 805306368

_PATTERN_NAMES = {v: k for k, v in dict(
    ERROR=ERROR, NOPATTERN=NOPATTERN, W15=W15, W16=W16, M8=M8, M4=M4, M3=M3, W9=W9,
    W13=W13, W14=W14, M13=M13, M12=M12, M7=M7, W4=W4, W5=W5, W10=W10, M11=M11, M10=M10,
    M5=M5, M6=M6, M16=M16, M15=M15, M14=M14, M9=M9, W1=W1, W2=W2, W3=W3, W8=W8, W6=W6,
    W7=W7, W11=W11, W12=W12, M1=M1, M2=M2).items()}


def pattern_name(p: int) -> str:
    """``EnumToString(NamePattern)``."""
    return _PATTERN_NAMES.get(int(p), str(int(p)))


# Strict orderings from high to low that define each pattern, in test order.
_ORDERINGS = (
    (M1, "BADCE"), (M2, "BADEC"), (M3, "BDACE"), (M4, "BDAEC"), (M5, "DBACE"),
    (M6, "DBAEC"), (M7, "BDCAE"), (M8, "BDEAC"), (M9, "DBCAE"), (M10, "DBEAC"),
    (M11, "DEBAC"), (M12, "BDCEA"), (M13, "BDECA"), (M14, "DBCEA"), (M15, "DBECA"),
    (M16, "DEBCA"), (W1, "ACBED"), (W2, "ACEBD"), (W3, "AECBD"), (W4, "ACEDB"),
    (W5, "AECDB"), (W6, "CABED"), (W7, "CAEBD"), (W8, "EACBD"), (W9, "CAEDB"),
    (W10, "EACDB"), (W11, "CEABD"), (W12, "ECABD"), (W13, "CEADB"), (W14, "ECADB"),
    (W15, "CEDAB"), (W16, "ECDAB"),
)
_EVOLUTION = {
    M1: NOPATTERN, M2: M1, M3: NOPATTERN, M4: M3, M8: M4, M5: NOPATTERN, M6: M5, M10: M6,
    M11: M10, M7: NOPATTERN, M12: M7, M13: M12, M9: NOPATTERN, M14: M9, M15: M14, M16: M15,
    W8: NOPATTERN, W3: W8, W2: W3, W1: W2, W10: NOPATTERN, W5: W10, W4: W5, W12: NOPATTERN,
    W11: W12, W7: W11, W6: W7, W14: NOPATTERN, W13: W14, W9: W13, W16: NOPATTERN, W15: W16,
}
_MUTATION = {}
for _src, _dst in (((M1, M3, M7, M12), W1), ((M2, M4, M8, M13), W4), ((M5, M9, M14), W6),
                   ((M6, M10, M15), W9), ((M11, M16), W15), ((W1, W6), M2),
                   ((W2, W7, W11), M8), ((W3, W8, W12), M11), ((W4, W9, W13, W15), M13),
                   ((W5, W10, W14, W16), M16)):
    for _p in _src:
        _MUTATION[_p] = _dst
# Minimum Fibonacci extension of the D→E leg before E counts as "real".
_E_RATIO = {
    M1: 1.618, M2: 0.5, M3: 1.2720, M4: 0.618, M5: 1.2720, M6: 0.618, M7: 3.0000, M8: 0.3819,
    M9: 1.618, M10: 0.5, M11: 0.25, M12: 1.618, M13: 0.5, M14: 1.2720, M15: 0.618, M16: 0.3819,
    W1: 0.3819, W2: 0.618, W3: 1.2720, W4: 0.5, W5: 1.618, W6: 0.25, W7: 0.5, W8: 1.618,
    W9: 0.3819, W10: 3.0000, W11: 0.618, W12: 1.2720, W13: 0.618, W14: 1.2720, W15: 0.5,
    W16: 1.618,
}
_M_PATTERNS = {M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15, M16}


class MyCPattern:
    def __init__(self, digits: int = 5):
        self.A = self.B = self.C = self.D = self.E = 0.0
        self.IsPointNotReal = False
        self.pattern = NOPATTERN
        self.oldPattern = NOPATTERN
        self.digits = digits

    def GetLastPattern(self):
        return self.pattern

    def GetPrevPattern(self):
        return self.oldPattern

    def GetA(self): return self.A
    def GetB(self): return self.B
    def GetC(self): return self.C
    def GetD(self): return self.D
    def GetE(self): return self.E
    def SetA(self, a): self.A = a
    def SetB(self, b): self.B = b
    def SetC(self, c): self.C = c
    def SetD(self, d): self.D = d
    def SetE(self, e): self.E = e

    def IsPointENotReal(self):
        return self.IsPointNotReal

    def Set(self, a, b, c, d, e):
        self.A, self.B, self.C, self.D, self.E = a, b, c, d, e

    def Get(self, a=None, b=None, c=None, d=None, e=None):
        if a is not None:
            self.Set(a, b, c, d, e)
        self.IsPointNotReal = False
        self.oldPattern = self.pattern
        v = {"A": self.A, "B": self.B, "C": self.C, "D": self.D, "E": self.E}
        for pat, order in _ORDERINGS:
            if all(v[order[k]] > v[order[k + 1]] for k in range(4)):
                self.pattern = pat
                self.AnalysisPointE()
                return self.pattern
        self.pattern = NOPATTERN
        return self.pattern

    def GetNextEvolution(self):
        return _EVOLUTION.get(self.pattern, NOPATTERN)

    def GetNextMutation(self):
        return self.GetMutation(self.pattern)

    @staticmethod
    def GetMutation(NowPattern):
        return _MUTATION.get(NowPattern, NOPATTERN)

    def IsRightEvolution(self) -> int:
        if self.oldPattern != self.pattern:
            return 1 if (self.oldPattern & self.pattern) != 0 else 0
        return -1

    def IsRightMutation(self) -> int:
        if self.oldPattern != self.pattern:
            return 1 if (self.GetMutation(self.oldPattern) & self.pattern) != 0 else 0
        return -1

    def AnalysisPointE(self) -> None:
        self.IsPointNotReal = False
        p = self.pattern
        if p in (NOPATTERN, ERROR) or p not in _E_RATIO:
            return
        r = _E_RATIO[p]
        A, B, C, D, E = self.A, self.B, self.C, self.D, self.E
        if p in _M_PATTERNS:
            if fdiv(D - E, D - C) < r:
                self.E = NormalizeDouble(D - r * (D - C), self.digits)
                self.IsPointNotReal = True
        else:
            if fdiv(E - D, C - D) < r:
                self.E = NormalizeDouble(r * (C - D) + D, self.digits)
                self.IsPointNotReal = True


# ======================================================= MyCPatternZigzag

# CalcPrognozPoint: (evolution target or None, mutation target)
def _prog(p, A, B, C, D, E):
    table = {
        M1: (None, 0.3819 * (D - E) + E), M2: (D - 1.618 * (D - C), 0.5 * (D - E) + E),
        M3: (None, 0.3819 * (D - E) + E), M4: (D - 1.272 * (D - C), 0.5 * (D - E) + E),
        M5: (None, 0.25 * (D - E) + E), M6: (D - 1.272 * (D - C), 0.3819 * (D - E) + E),
        M7: (None, 0.3819 * (D - E) + E), M8: (D - 0.618 * (D - C), 0.5 * (D - E) + E),
        M9: (None, 0.25 * (D - E) + E), M10: (D - 0.618 * (D - C), 0.3819 * (D - E) + E),
        M11: (D - 0.5 * (D - C), 0.5 * (D - E) + E), M12: (D - 3.0 * (D - C), 0.3819 * (D - E) + E),
        M13: (D - 1.618 * (D - C), 0.5 * (D - E) + E), M14: (D - 1.618 * (D - C), 0.25 * (D - E) + E),
        M15: (C - (C - A) / 1.618, E + (B - E) / 1.618), M16: (D - 0.618 * (D - C), 0.5 * (D - E) + E),
        W1: (0.618 * (C - D) + D, E - 0.5 * (E - D)), W2: (1.272 * (C - D) + D, E - 0.3819 * (E - D)),
        W3: (1.618 * (C - D) + D, E - 0.25 * (E - D)), W4: (1.618 * (C - D) + D, E - 0.5 * (E - D)),
        W5: (3.0 * (C - D) + D, E - 0.3819 * (E - D)), W6: (0.5 * (C - D) + D, E - 0.5 * (E - D)),
        W7: (0.618 * (C - D) + D, E - 0.3819 * (E - D)), W8: (None, E - 0.25 * (E - D)),
        W9: (0.618 * (C - D) + D, E - 0.5 * (E - D)), W10: (None, E - 0.3819 * (E - D)),
        W11: (1.272 * (C - D) + D, E - 0.3819 * (E - D)), W12: (None, E - 0.25 * (E - D)),
        W13: (1.272 * (C - D) + D, E - 0.5 * (E - D)), W14: (None, E - 0.3819 * (E - D)),
        W15: (1.618 * (C - D) + D, E - 0.5 * (E - D)), W16: (None, E - 0.3819 * (E - D)),
    }
    return table.get(p)


class MyCPatternZigzag(MyCPattern):
    def __init__(self, point: float = 0.00001, digits: int = 5, period_seconds: int = 60):
        super().__init__(digits)
        self.Depth = 24
        self.Deviation = 12
        self.Backstep = 9
        self.SizeBuffers = 500
        self.NumberLineComment = 2
        self.pE = self.pM = self.pEv1 = self.pM1 = 0.0
        self.tA = self.tB = self.tC = self.tD = self.tE = self.tEv = self.tM = 0
        self.iA = self.iB = self.iC = self.iD = self.iE = self.iEv = self.iM = 0
        self.countEvolution = self.countMutation = self.countError = 0
        self.Extremum = MyCExtremum(point)
        self.MyComment = None
        self.point = point
        self.period_seconds = period_seconds

    def SetDepth(self, depth): self.Depth = depth
    def SetDeviation(self, dev): self.Deviation = dev
    def SetBackstep(self, back): self.Backstep = back
    def SetSizeBuffers(self, size): self.SizeBuffers = size

    def SetNumberLineComment(self, NL):
        self.NumberLineComment = NL if 0 < NL < 31 else 1

    def GetDepth(self): return self.Depth
    def GetDeviation(self): return self.Deviation
    def GetBackstep(self): return self.Backstep
    def GetSizeBuffers(self): return self.SizeBuffers
    def GetNumberLineComment(self): return self.NumberLineComment
    def GetCountLineComment(self): return 4
    def GetNameLastPattern(self): return pattern_name(self.GetLastPattern())
    def GetNamePrevPattern(self): return pattern_name(self.GetPrevPattern())
    def GetNameEvolution(self): return pattern_name(self.GetNextEvolution())
    def GetNameMutation(self): return pattern_name(self.GetNextMutation())
    def GetPointEvolution(self): return self.pE
    def GetPointMutation(self): return self.pM
    def GetPointEvolutionLevel1(self): return self.pEv1
    def GetPointMutationLevel1(self): return self.pM1
    def GetTimeA(self): return self.tA
    def GetTimeB(self): return self.tB
    def GetTimeC(self): return self.tC
    def GetTimeD(self): return self.tD
    def GetTimeE(self): return self.tE
    def GetTimeEvolution(self): return self.tEv
    def GetTimeMutation(self): return self.tM
    def GetIndexA(self): return self.iA
    def GetIndexB(self): return self.iB
    def GetIndexC(self): return self.iC
    def GetIndexD(self): return self.iD
    def GetIndexE(self): return self.iE
    def GetIndexEvolution(self): return self.iEv
    def GetIndexMutation(self): return self.iM

    def AddPointerCommet(self, pComment):
        if pComment is not None:
            self.MyComment = pComment

    def GetNamePattern(self, high, low, time) -> str:
        """Forward-indexed ``high``/``low``/``time`` of length ``SizeBuffers``."""
        if self.SeachParams(high, low, time):
            self.Get()
            if self.IsPointENotReal():
                self.iE = self.SizeBuffers - 1
                self.tE = time[self.SizeBuffers - 1]
            self.CalcModelCount()
            self.CalcPrognozPoint()
            return pattern_name(self.GetLastPattern())
        return "ERROR"

    def PrintComment(self) -> None:
        c = self.MyComment
        if c is None:
            return
        n = self.NumberLineComment
        c.AddLineOfIndex(n, "Now is pattern: " + pattern_name(self.GetLastPattern()))
        c.AddLineOfIndex(n + 1, "Next pattern(Evolution): " + self.GetNameEvolution()
                         + ", price = " + f"{self.GetPointEvolution():.{self.digits}f}")
        c.AddLineOfIndex(n + 2, "Next pattern(Mutation ): " + self.GetNameMutation()
                         + ", price = " + f"{self.GetPointMutation():.{self.digits}f}")
        total = self.countEvolution + self.countMutation + self.countError
        if total < 10:
            c.AddLineOfIndex(n + 3, "No counter calculation.")
        else:
            c.AddLineOfIndex(n + 3, "Evolution: %.2f%% Mutation: %.2f%% Error: %.2f%%" % (
                idiv(100 * self.countEvolution, total), idiv(100 * self.countMutation, total),
                idiv(100 * self.countError, total)))

    def GetSumModel(self) -> float:
        ret = float(self.countEvolution + self.countMutation)
        if ret != 0:
            return self.countEvolution / ret
        return 0

    def SeachParams(self, high, low, time) -> bool:
        Z = None
        indD = 0
        if len(high) < self.SizeBuffers or len(low) < self.SizeBuffers or len(time) < self.SizeBuffers:
            return False
        ret = self.Extremum.GetClassicZigzag(high, low, self.Depth, self.Deviation, self.Backstep)
        if ret > 0:
            Z = self.Extremum.ZigzagBuffer
            ind = ret - 1
            while ind > 0:
                if Z[ind] != 0:
                    self.tD = time[ind]
                    self.SetD(Z[ind])
                    indD = ind
                    self.iD = ind
                    break
                ind -= 1
            if ind > ret - self.Backstep:
                self.tE, self.iE = self.tD, self.iD
                self.SetE(self.GetD())
                indD = -1
                ind -= 1
                while ind > 0:
                    if Z[ind] != 0:
                        self.tD = time[ind]
                        self.SetD(Z[ind])
                        self.iD = ind
                        break
                    ind -= 1
            for setter, attr_t, attr_i in ((self.SetC, "tC", "iC"), (self.SetB, "tB", "iB"),
                                           (self.SetA, "tA", "iA")):
                ind -= 1
                while ind > 0:
                    if Z[ind] != 0:
                        setter(Z[ind])
                        setattr(self, attr_t, time[ind])
                        setattr(self, attr_i, ind)
                        break
                    ind -= 1
        else:
            return False
        if indD < 0:
            return True
        start, count = indD + 1, self.SizeBuffers - indD - 1
        if self.GetC() > self.GetD():
            ind = max(range(start, start + count), key=lambda k: (high[k], -k)) if count > 0 else -1
            if ind > 0:
                self.SetE(high[ind])
                self.tE, self.iE = time[ind], ind
            else:
                self.SetE(high[self.SizeBuffers - 2])
                self.tE, self.iE = time[self.SizeBuffers - 2], self.SizeBuffers - 2
        else:
            ind = min(range(start, start + count), key=lambda k: (low[k], k)) if count > 0 else -1
            if ind > 0:
                self.SetE(low[ind])
                self.tE, self.iE = time[ind], ind
            else:
                self.SetE(low[self.SizeBuffers - 2])
                self.tE, self.iE = time[self.SizeBuffers - 2], self.SizeBuffers - 2
        deltaED = abs(self.GetE() - self.GetD())
        dnED = int(deltaED / self.point) if self.point else 0
        if dnED < self.Deviation:
            self.SetE(self.GetD()); self.tE, self.iE = self.tD, self.iD
            self.SetD(self.GetC()); self.tD, self.iD = self.tC, self.iC
            self.SetC(self.GetB()); self.tC, self.iC = self.tB, self.iB
            self.SetB(self.GetA()); self.tB, self.iB = self.tA, self.iA
            ind = self.iB - 1
            while ind > 0:
                if Z[ind] != 0:
                    self.SetA(Z[ind])
                    self.tA, self.iA = time[ind], ind
                    break
                ind -= 1
        return True

    def CalcModelCount(self) -> None:
        if (self.countEvolution == 0 and self.countMutation == 0 and self.countError == 0
                and self.oldPattern == NOPATTERN):
            return
        if self.oldPattern == self.pattern:
            return
        if self.pattern == NOPATTERN:
            self.countError += 1
            return
        if self.oldPattern == NOPATTERN:
            return
        if self.IsRightEvolution() == 1:
            self.countEvolution += 1
            return
        if self.IsRightMutation() == 1:
            self.countMutation += 1
            return
        self.countError += 1

    def CalcRegress(self, nLast, a, nA, b, nB, c=0.0, nC=0):
        """Returns ``(value_at_nLast, intercept, slope)`` (the source writes the
        intercept/slope back into ``a``/``b``)."""
        xs = [nA, nB] + ([nC] if nC > 0 else [])
        ys = [a, b] + ([c] if nC > 0 else [])
        dA, dB = self.MyCRegressia(xs, ys)
        return dB * nLast + dA, dA, dB

    @staticmethod
    def MyCRegressia(fMassX, fMassY):
        a = b = c = d = 0.0
        i = 0
        for i in range(len(fMassX)):
            a += fMassX[i]
            b += fMassY[i]
            c += fMassX[i] ** 2
            d += fMassX[i] * fMassY[i]
        i = len(fMassX)
        fB1 = fdiv(a * b - i * d, a ** 2 - i * c)
        fB0 = (b - fB1 * a) / i
        return fB0, fB1

    def CalcPrognozPoint(self) -> None:
        p = self.pattern
        if p == NOPATTERN:
            self.pE = self.pM = 0.0
            self.iEv = self.iM = 0
            self.CalcPrognozLevel1()
            return
        step = idiv(self.iE - self.iA, 5)
        if step < 3 and step > self.Backstep * 2:
            iTemp = self.iE + step
        else:
            iTemp = self.iE + self.Backstep * 2
        self.tEv = (iTemp - self.iE) * self.period_seconds + self.GetTimeE()
        self.tM = (iTemp - self.iE) * self.period_seconds + self.GetTimeE()
        targets = _prog(p, self.A, self.B, self.C, self.D, self.E)
        if targets is None:
            self.pE = self.pM = 0.0
            self.iEv = self.iM = 0
        else:
            ev, mu = targets
            if ev is None:
                self.pE, self.iEv = 0.0, 0
            else:
                self.pE, self.iEv = NormalizeDouble(ev, self.digits), iTemp
            self.pM, self.iM = NormalizeDouble(mu, self.digits), iTemp
        self.CalcPrognozLevel1()

    def CalcPrognozLevel1(self) -> None:
        A, B, C, D, E = self.A, self.B, self.C, self.D, self.E
        p = self.pattern
        nd = lambda v: NormalizeDouble(v, self.digits)          # noqa: E731
        if p == M1 or p == M3:
            self.pEv1, self.pM1 = 0.0, nd(E + (B - D) * 1.618)
        elif p in (M5, W12):
            value, _, _ = self.CalcRegress(self.iM, B, self.iB, D, self.iD)
            self.pEv1, self.pM1 = 0.0, nd(value)
        elif p == M13:
            self.pEv1, self.pM1 = nd(E - (B - A) * 0.618), nd(E + (B - A) * 0.618)
        elif p == M15:
            self.pEv1, self.pM1 = nd(E - (D - E) * 1.618), nd(E + (D - E) * 1.618)
        elif p == M16:
            self.pEv1, self.pM1 = nd(A - (B - A) * 0.618), nd(E + (D - E) * 1.618)
        elif p == W1:
            self.pEv1, self.pM1 = nd(E + (A - B) * 1.618), nd(E - (C - D) * 0.618)
        elif p == W2:
            self.pEv1, self.pM1 = nd(E + (E - D) * 1.618), nd(E - (E - D) * 1.618)
        elif p == W4:
            self.pEv1, self.pM1 = nd(E + (B - A) * 0.618), nd(E - (B - A) * 0.618)
        elif p in (W14, W16):
            self.pEv1, self.pM1 = 0.0, nd(E - (C - B) * 1.618)
        else:
            self.pEv1, self.pM1 = 0.0, 0.0
