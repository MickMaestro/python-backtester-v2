"""MyCPattern.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh

# enum NamePattern
ERROR = 2
NOPATTERN = 3
W15 = 8
W16 = 12
M8 = 64
M4 = 80
M3 = 112
W9 = 512
W13 = 640
W14 = 896
M13 = 4096
M12 = 5120
M7 = 7168
W4 = 32768
W5 = 40960
W10 = 57344
M11 = 262144
M10 = 327680
M5 = 393216
M6 = 458752
M16 = 2097152
M15 = 2621440
M14 = 3145728
M9 = 3670016
W1 = 16777216
W2 = 20971520
W3 = 25165824
W8 = 29360128
W6 = 134217728
W7 = 167772160
W11 = 201326592
W12 = 234881024
M1 = 536870912
M2 = 805306368
_enum('NamePattern', {2: 'ERROR', 3: 'NOPATTERN', 8: 'W15', 12: 'W16', 64: 'M8', 80: 'M4', 112: 'M3', 512: 'W9', 640: 'W13', 896: 'W14', 4096: 'M13', 5120: 'M12', 7168: 'M7', 32768: 'W4', 40960: 'W5', 57344: 'W10', 262144: 'M11', 327680: 'M10', 393216: 'M5', 458752: 'M6', 2097152: 'M16', 2621440: 'M15', 3145728: 'M14', 3670016: 'M9', 16777216: 'W1', 20971520: 'W2', 25165824: 'W3', 29360128: 'W8', 134217728: 'W6', 167772160: 'W7', 201326592: 'W11', 234881024: 'W12', 536870912: 'M1', 805306368: 'M2'})


class MyCPattern(CObject):
    _q_fields = ('A', 'B', 'C', 'D', 'E', 'pattern', 'oldPattern', 'IsPointNotReal')
    def __init__(self):
        CObject.__init__(self)
        self.A = 0.0
        self.B = 0.0
        self.C = 0.0
        self.D = 0.0
        self.E = 0.0
        self.pattern = 0
        self.oldPattern = 0
        self.IsPointNotReal = False
        self.A = 0.0
        self.B = 0.0
        self.C = 0.0
        self.D = 0.0
        self.E = 0.0
        self.IsPointNotReal = False
        self.pattern = NOPATTERN
        self.oldPattern = NOPATTERN
    def _q_dtor(self):
        pass
    def Get_0(self):
        self.IsPointNotReal = False
        self.oldPattern = self.pattern
        if ((self.B > self.A and self.A > self.D) and self.D > self.C) and self.C > self.E:
            self.pattern = M1
            self.AnalysisPointE()
            return self.pattern
        if ((self.B > self.A and self.A > self.D) and self.D > self.E) and self.E > self.C:
            self.pattern = M2
            self.AnalysisPointE()
            return self.pattern
        if ((self.B > self.D and self.D > self.A) and self.A > self.C) and self.C > self.E:
            self.pattern = M3
            self.AnalysisPointE()
            return self.pattern
        if ((self.B > self.D and self.D > self.A) and self.A > self.E) and self.E > self.C:
            self.pattern = M4
            self.AnalysisPointE()
            return self.pattern
        if ((self.D > self.B and self.B > self.A) and self.A > self.C) and self.C > self.E:
            self.pattern = M5
            self.AnalysisPointE()
            return self.pattern
        if ((self.D > self.B and self.B > self.A) and self.A > self.E) and self.E > self.C:
            self.pattern = M6
            self.AnalysisPointE()
            return self.pattern
        if ((self.B > self.D and self.D > self.C) and self.C > self.A) and self.A > self.E:
            self.pattern = M7
            self.AnalysisPointE()
            return self.pattern
        if ((self.B > self.D and self.D > self.E) and self.E > self.A) and self.A > self.C:
            self.pattern = M8
            self.AnalysisPointE()
            return self.pattern
        if ((self.D > self.B and self.B > self.C) and self.C > self.A) and self.A > self.E:
            self.pattern = M9
            self.AnalysisPointE()
            return self.pattern
        if ((self.D > self.B and self.B > self.E) and self.E > self.A) and self.A > self.C:
            self.pattern = M10
            self.AnalysisPointE()
            return self.pattern
        if ((self.D > self.E and self.E > self.B) and self.B > self.A) and self.A > self.C:
            self.pattern = M11
            self.AnalysisPointE()
            return self.pattern
        if ((self.B > self.D and self.D > self.C) and self.C > self.E) and self.E > self.A:
            self.pattern = M12
            self.AnalysisPointE()
            return self.pattern
        if ((self.B > self.D and self.D > self.E) and self.E > self.C) and self.C > self.A:
            self.pattern = M13
            self.AnalysisPointE()
            return self.pattern
        if ((self.D > self.B and self.B > self.C) and self.C > self.E) and self.E > self.A:
            self.pattern = M14
            self.AnalysisPointE()
            return self.pattern
        if ((self.D > self.B and self.B > self.E) and self.E > self.C) and self.C > self.A:
            self.pattern = M15
            self.AnalysisPointE()
            return self.pattern
        if ((self.D > self.E and self.E > self.B) and self.B > self.C) and self.C > self.A:
            self.pattern = M16
            self.AnalysisPointE()
            return self.pattern
        if ((self.A > self.C and self.C > self.B) and self.B > self.E) and self.E > self.D:
            self.pattern = W1
            self.AnalysisPointE()
            return self.pattern
        if ((self.A > self.C and self.C > self.E) and self.E > self.B) and self.B > self.D:
            self.pattern = W2
            self.AnalysisPointE()
            return self.pattern
        if ((self.A > self.E and self.E > self.C) and self.C > self.B) and self.B > self.D:
            self.pattern = W3
            self.AnalysisPointE()
            return self.pattern
        if ((self.A > self.C and self.C > self.E) and self.E > self.D) and self.D > self.B:
            self.pattern = W4
            self.AnalysisPointE()
            return self.pattern
        if ((self.A > self.E and self.E > self.C) and self.C > self.D) and self.D > self.B:
            self.pattern = W5
            self.AnalysisPointE()
            return self.pattern
        if ((self.C > self.A and self.A > self.B) and self.B > self.E) and self.E > self.D:
            self.pattern = W6
            self.AnalysisPointE()
            return self.pattern
        if ((self.C > self.A and self.A > self.E) and self.E > self.B) and self.B > self.D:
            self.pattern = W7
            self.AnalysisPointE()
            return self.pattern
        if ((self.E > self.A and self.A > self.C) and self.C > self.B) and self.B > self.D:
            self.pattern = W8
            self.AnalysisPointE()
            return self.pattern
        if ((self.C > self.A and self.A > self.E) and self.E > self.D) and self.D > self.B:
            self.pattern = W9
            self.AnalysisPointE()
            return self.pattern
        if ((self.E > self.A and self.A > self.C) and self.C > self.D) and self.D > self.B:
            self.pattern = W10
            self.AnalysisPointE()
            return self.pattern
        if ((self.C > self.E and self.E > self.A) and self.A > self.B) and self.B > self.D:
            self.pattern = W11
            self.AnalysisPointE()
            return self.pattern
        if ((self.E > self.C and self.C > self.A) and self.A > self.B) and self.B > self.D:
            self.pattern = W12
            self.AnalysisPointE()
            return self.pattern
        if ((self.C > self.E and self.E > self.A) and self.A > self.D) and self.D > self.B:
            self.pattern = W13
            self.AnalysisPointE()
            return self.pattern
        if ((self.E > self.C and self.C > self.A) and self.A > self.D) and self.D > self.B:
            self.pattern = W14
            self.AnalysisPointE()
            return self.pattern
        if ((self.C > self.E and self.E > self.D) and self.D > self.A) and self.A > self.B:
            self.pattern = W15
            self.AnalysisPointE()
            return self.pattern
        if ((self.E > self.C and self.C > self.D) and self.D > self.A) and self.A > self.B:
            self.pattern = W16
            self.AnalysisPointE()
            return self.pattern
        self.pattern = NOPATTERN
        return self.pattern
    def Get_5(self, a, b, c, d, e):
        self.Set(a, b, c, d, e)
        return self.Get_0()
    def GetLastPattern(self):
        return self.pattern
    def GetPrevPattern(self):
        return self.oldPattern
    def GetA(self):
        return self.A
    def GetB(self):
        return self.B
    def GetC(self):
        return self.C
    def GetD(self):
        return self.D
    def GetE(self):
        return self.E
    def Set(self, a, b, c, d, e):
        self.A = a
        self.B = b
        self.C = c
        self.D = d
        self.E = e
    def SetA(self, a):
        self.A = a
    def SetB(self, b):
        self.B = b
    def SetC(self, c):
        self.C = c
    def SetD(self, d):
        self.D = d
    def SetE(self, e):
        self.E = e
    def GetNextEvolution(self):
        if self.pattern == M1:
            return NOPATTERN
        if self.pattern == M2:
            return M1
        if self.pattern == M3:
            return NOPATTERN
        if self.pattern == M4:
            return M3
        if self.pattern == M8:
            return M4
        if self.pattern == M5:
            return NOPATTERN
        if self.pattern == M6:
            return M5
        if self.pattern == M10:
            return M6
        if self.pattern == M11:
            return M10
        if self.pattern == M7:
            return NOPATTERN
        if self.pattern == M12:
            return M7
        if self.pattern == M13:
            return M12
        if self.pattern == M9:
            return NOPATTERN
        if self.pattern == M14:
            return M9
        if self.pattern == M15:
            return M14
        if self.pattern == M16:
            return M15
        if self.pattern == W8:
            return NOPATTERN
        if self.pattern == W3:
            return W8
        if self.pattern == W2:
            return W3
        if self.pattern == W1:
            return W2
        if self.pattern == W10:
            return NOPATTERN
        if self.pattern == W5:
            return W10
        if self.pattern == W4:
            return W5
        if self.pattern == W12:
            return NOPATTERN
        if self.pattern == W11:
            return W12
        if self.pattern == W7:
            return W11
        if self.pattern == W6:
            return W7
        if self.pattern == W14:
            return NOPATTERN
        if self.pattern == W13:
            return W14
        if self.pattern == W9:
            return W13
        if self.pattern == W16:
            return NOPATTERN
        if self.pattern == W15:
            return W16
        return NOPATTERN
    def GetNextMutation(self):
        return self.GetMutation(self.pattern)
    def IsRightEvolution(self):
        if self.oldPattern != self.pattern:
            if (self.oldPattern & self.pattern) != 0:
                return 1
            return 0
        return -1
    def IsRightMutation(self):
        if self.oldPattern != self.pattern:
            MajorMutation = self.GetMutation(self.oldPattern)
            if (MajorMutation & self.pattern) != 0:
                return 1
            return 0
        return -1
    def IsPointENotReal(self):
        return self.IsPointNotReal
    def GetMutation(self, NowPattern):
        if ((NowPattern == M1 or NowPattern == M3) or NowPattern == M7) or NowPattern == M12:
            return W1
        if ((NowPattern == M2 or NowPattern == M4) or NowPattern == M8) or NowPattern == M13:
            return W4
        if (NowPattern == M5 or NowPattern == M9) or NowPattern == M14:
            return W6
        if (NowPattern == M6 or NowPattern == M10) or NowPattern == M15:
            return W9
        if NowPattern == M11 or NowPattern == M16:
            return W15
        if NowPattern == W1 or NowPattern == W6:
            return M2
        if (NowPattern == W2 or NowPattern == W7) or NowPattern == W11:
            return M8
        if (NowPattern == W3 or NowPattern == W8) or NowPattern == W12:
            return M11
        if ((NowPattern == W4 or NowPattern == W9) or NowPattern == W13) or NowPattern == W15:
            return M13
        if ((NowPattern == W5 or NowPattern == W10) or NowPattern == W14) or NowPattern == W16:
            return M16
        return NOPATTERN
    def AnalysisPointE(self):
        self.IsPointNotReal = False
        if self.pattern != NOPATTERN and self.pattern != ERROR:
            if self.pattern == M1:
                if _fdiv(self.D - self.E, self.D - self.C) < 1.618:
                    self.E = NormalizeDouble(self.D - (1.618 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M2:
                if _fdiv(self.D - self.E, self.D - self.C) < 0.5:
                    self.E = NormalizeDouble(self.D - (0.5 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M3:
                if _fdiv(self.D - self.E, self.D - self.C) < 1.272:
                    self.E = NormalizeDouble(self.D - (1.272 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M4:
                if _fdiv(self.D - self.E, self.D - self.C) < 0.618:
                    self.E = NormalizeDouble(self.D - (0.618 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M5:
                if _fdiv(self.D - self.E, self.D - self.C) < 1.272:
                    self.E = NormalizeDouble(self.D - (1.272 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M6:
                if _fdiv(self.D - self.E, self.D - self.C) < 0.618:
                    self.E = NormalizeDouble(self.D - (0.618 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M7:
                if _fdiv(self.D - self.E, self.D - self.C) < 3.0:
                    self.E = NormalizeDouble(self.D - (3.0 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M8:
                if _fdiv(self.D - self.E, self.D - self.C) < 0.3819:
                    self.E = NormalizeDouble(self.D - (0.3819 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M9:
                if _fdiv(self.D - self.E, self.D - self.C) < 1.618:
                    self.E = NormalizeDouble(self.D - (1.618 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M10:
                if _fdiv(self.D - self.E, self.D - self.C) < 0.5:
                    self.E = NormalizeDouble(self.D - (0.5 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M11:
                if _fdiv(self.D - self.E, self.D - self.C) < 0.25:
                    self.E = NormalizeDouble(self.D - (0.25 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M12:
                if _fdiv(self.D - self.E, self.D - self.C) < 1.618:
                    self.E = NormalizeDouble(self.D - (1.618 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M13:
                if _fdiv(self.D - self.E, self.D - self.C) < 0.5:
                    self.E = NormalizeDouble(self.D - (0.5 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M14:
                if _fdiv(self.D - self.E, self.D - self.C) < 1.272:
                    self.E = NormalizeDouble(self.D - (1.272 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M15:
                if _fdiv(self.D - self.E, self.D - self.C) < 0.618:
                    self.E = NormalizeDouble(self.D - (0.618 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == M16:
                if _fdiv(self.D - self.E, self.D - self.C) < 0.3819:
                    self.E = NormalizeDouble(self.D - (0.3819 * (self.D - self.C)), Digits())
                    self.IsPointNotReal = True
            if self.pattern == W1:
                if _fdiv(self.E - self.D, self.C - self.D) < 0.3819:
                    self.E = NormalizeDouble((0.3819 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W2:
                if _fdiv(self.E - self.D, self.C - self.D) < 0.618:
                    self.E = NormalizeDouble((0.618 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W3:
                if _fdiv(self.E - self.D, self.C - self.D) < 1.272:
                    self.E = NormalizeDouble((1.272 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W4:
                if _fdiv(self.E - self.D, self.C - self.D) < 0.5:
                    self.E = NormalizeDouble((0.5 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W5:
                if _fdiv(self.E - self.D, self.C - self.D) < 1.618:
                    self.E = NormalizeDouble((1.618 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W6:
                if _fdiv(self.E - self.D, self.C - self.D) < 0.25:
                    self.E = NormalizeDouble((0.25 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W7:
                if _fdiv(self.E - self.D, self.C - self.D) < 0.5:
                    self.E = NormalizeDouble((0.5 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W8:
                if _fdiv(self.E - self.D, self.C - self.D) < 1.618:
                    self.E = NormalizeDouble((1.618 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W9:
                if _fdiv(self.E - self.D, self.C - self.D) < 0.3819:
                    self.E = NormalizeDouble((0.3819 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W10:
                if _fdiv(self.E - self.D, self.C - self.D) < 3.0:
                    self.E = NormalizeDouble((3.0 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W11:
                if _fdiv(self.E - self.D, self.C - self.D) < 0.618:
                    self.E = NormalizeDouble((0.618 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W12:
                if _fdiv(self.E - self.D, self.C - self.D) < 1.272:
                    self.E = NormalizeDouble((1.272 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W13:
                if _fdiv(self.E - self.D, self.C - self.D) < 0.618:
                    self.E = NormalizeDouble((0.618 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W14:
                if _fdiv(self.E - self.D, self.C - self.D) < 1.272:
                    self.E = NormalizeDouble((1.272 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W15:
                if _fdiv(self.E - self.D, self.C - self.D) < 0.5:
                    self.E = NormalizeDouble((0.5 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True
            if self.pattern == W16:
                if _fdiv(self.E - self.D, self.C - self.D) < 1.618:
                    self.E = NormalizeDouble((1.618 * (self.C - self.D)) + self.D, Digits())
                    self.IsPointNotReal = True

__all__ = ['ERROR', 'NOPATTERN', 'W15', 'W16', 'M8', 'M4', 'M3', 'W9', 'W13', 'W14', 'M13', 'M12', 'M7', 'W4', 'W5', 'W10', 'M11', 'M10', 'M5', 'M6', 'M16', 'M15', 'M14', 'M9', 'W1', 'W2', 'W3', 'W8', 'W6', 'W7', 'W11', 'W12', 'M1', 'M2', 'MyCPattern']
