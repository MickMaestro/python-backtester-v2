"""myccomment.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh


class MyCComment(CObject):
    _q_fields = ('st0', 'st1', 'st2', 'st3', 'st4', 'st5', 'st6', 'st7', 'st8', 'st9', 'st10', 'st11', 'st12', 'st13', 'st14', 'st15', 'st16', 'st17', 'st18', 'st19', 'st20', 'st21', 'st22', 'st23', 'st24', 'st25', 'st26', 'st27', 'st28', 'st29', 'st30', 'st31', 'st32')
    def __init__(self):
        CObject.__init__(self)
        self.st0 = ""
        self.st1 = ""
        self.st2 = ""
        self.st3 = ""
        self.st4 = ""
        self.st5 = ""
        self.st6 = ""
        self.st7 = ""
        self.st8 = ""
        self.st9 = ""
        self.st10 = ""
        self.st11 = ""
        self.st12 = ""
        self.st13 = ""
        self.st14 = ""
        self.st15 = ""
        self.st16 = ""
        self.st17 = ""
        self.st18 = ""
        self.st19 = ""
        self.st20 = ""
        self.st21 = ""
        self.st22 = ""
        self.st23 = ""
        self.st24 = ""
        self.st25 = ""
        self.st26 = ""
        self.st27 = ""
        self.st28 = ""
        self.st29 = ""
        self.st30 = ""
        self.st31 = ""
        self.st32 = ""
        self.st0 = '\r\n'
        self.ClearAll()
    def _q_dtor(self):
        self.ClearAll()
    def AddLines(self, s1, s2=None, s3=None, s4=None, s5=None, s6=None, s7=None, s8=None, s9=None, s10=None, s11=None, s12=None, s13=None, s14=None, s15=None, s16=None, s17=None, s18=None, s19=None, s20=None, s21=None, s22=None, s23=None, s24=None, s25=None, s26=None, s27=None, s28=None, s29=None, s30=None, s31=None, s32=None):
        if s1 != "":
            self.st1 = s1
        if s2 != "":
            self.st2 = s2
        if s3 != "":
            self.st3 = s3
        if s4 != "":
            self.st4 = s4
        if s5 != "":
            self.st5 = s5
        if s6 != "":
            self.st6 = s6
        if s7 != "":
            self.st7 = s7
        if s8 != "":
            self.st8 = s8
        if s9 != "":
            self.st9 = s9
        if s10 != "":
            self.st10 = s10
        if s11 != "":
            self.st11 = s11
        if s12 != "":
            self.st12 = s12
        if s13 != "":
            self.st13 = s13
        if s14 != "":
            self.st14 = s14
        if s15 != "":
            self.st15 = s15
        if s16 != "":
            self.st16 = s16
        if s17 != "":
            self.st17 = s17
        if s18 != "":
            self.st18 = s18
        if s19 != "":
            self.st19 = s19
        if s20 != "":
            self.st20 = s20
        if s21 != "":
            self.st21 = s21
        if s22 != "":
            self.st22 = s22
        if s23 != "":
            self.st23 = s23
        if s24 != "":
            self.st24 = s24
        if s25 != "":
            self.st25 = s25
        if s26 != "":
            self.st26 = s26
        if s27 != "":
            self.st27 = s27
        if s28 != "":
            self.st28 = s28
        if s29 != "":
            self.st29 = s29
        if s30 != "":
            self.st30 = s30
        if s31 != "":
            self.st31 = s31
        if s32 != "":
            self.st32 = s32
        self.PrintComment()
    def AddLineOfIndex(self, ind, st):
        _sw1 = ind
        if _sw1 == 1:
            self.st1 = st
        elif _sw1 == 2:
            self.st2 = st
        elif _sw1 == 3:
            self.st3 = st
        elif _sw1 == 4:
            self.st4 = st
        elif _sw1 == 5:
            self.st5 = st
        elif _sw1 == 6:
            self.st6 = st
        elif _sw1 == 7:
            self.st7 = st
        elif _sw1 == 8:
            self.st8 = st
        elif _sw1 == 9:
            self.st9 = st
        elif _sw1 == 10:
            self.st10 = st
        elif _sw1 == 11:
            self.st11 = st
        elif _sw1 == 12:
            self.st12 = st
        elif _sw1 == 13:
            self.st13 = st
        elif _sw1 == 14:
            self.st14 = st
        elif _sw1 == 15:
            self.st15 = st
        elif _sw1 == 16:
            self.st16 = st
        elif _sw1 == 17:
            self.st17 = st
        elif _sw1 == 18:
            self.st18 = st
        elif _sw1 == 19:
            self.st19 = st
        elif _sw1 == 20:
            self.st20 = st
        elif _sw1 == 21:
            self.st21 = st
        elif _sw1 == 22:
            self.st22 = st
        elif _sw1 == 23:
            self.st23 = st
        elif _sw1 == 24:
            self.st24 = st
        elif _sw1 == 25:
            self.st25 = st
        elif _sw1 == 26:
            self.st26 = st
        elif _sw1 == 27:
            self.st27 = st
        elif _sw1 == 28:
            self.st28 = st
        elif _sw1 == 29:
            self.st29 = st
        elif _sw1 == 30:
            self.st30 = st
        elif _sw1 == 31:
            self.st31 = st
        elif _sw1 == 32:
            self.st32 = st
        else:
            return
        self.PrintComment()
    def GetLineOfIndex(self, ind, st):
        _sw2 = ind
        if _sw2 == 1:
            return self.st1
        elif _sw2 == 2:
            return self.st2
        elif _sw2 == 3:
            return self.st3
        elif _sw2 == 4:
            return self.st4
        elif _sw2 == 5:
            return self.st5
        elif _sw2 == 6:
            return self.st6
        elif _sw2 == 7:
            return self.st7
        elif _sw2 == 8:
            return self.st8
        elif _sw2 == 9:
            return self.st9
        elif _sw2 == 10:
            return self.st10
        elif _sw2 == 11:
            return self.st11
        elif _sw2 == 12:
            return self.st12
        elif _sw2 == 13:
            return self.st13
        elif _sw2 == 14:
            return self.st14
        elif _sw2 == 15:
            return self.st15
        elif _sw2 == 16:
            return self.st16
        elif _sw2 == 17:
            return self.st17
        elif _sw2 == 18:
            return self.st18
        elif _sw2 == 19:
            return self.st19
        elif _sw2 == 20:
            return self.st20
        elif _sw2 == 21:
            return self.st21
        elif _sw2 == 22:
            return self.st22
        elif _sw2 == 23:
            return self.st23
        elif _sw2 == 24:
            return self.st24
        elif _sw2 == 25:
            return self.st25
        elif _sw2 == 26:
            return self.st26
        elif _sw2 == 27:
            return self.st27
        elif _sw2 == 28:
            return self.st28
        elif _sw2 == 29:
            return self.st29
        elif _sw2 == 30:
            return self.st30
        elif _sw2 == 31:
            return self.st31
        elif _sw2 == 32:
            return self.st32
        else:
            return ""
        return ""
    def ClearAll(self):
        self.st1 = ""
        self.st2 = ""
        self.st3 = ""
        self.st4 = ""
        self.st5 = ""
        self.st6 = ""
        self.st7 = ""
        self.st8 = ""
        self.st9 = ""
        self.st10 = ""
        self.st11 = ""
        self.st12 = ""
        self.st13 = ""
        self.st14 = ""
        self.st15 = ""
        self.st16 = ""
        self.st17 = ""
        self.st18 = ""
        self.st19 = ""
        self.st20 = ""
        self.st21 = ""
        self.st22 = ""
        self.st23 = ""
        self.st24 = ""
        self.st25 = ""
        self.st26 = ""
        self.st27 = ""
        self.st28 = ""
        self.st29 = ""
        self.st30 = ""
        self.st31 = ""
        self.st32 = ""
        self.PrintComment()
    def Update(self):
        self.PrintComment()
    def PrintComment(self):
        Comment(self.st1, self.st0, self.st2, self.st0, self.st3, self.st0, self.st4, self.st0, self.st5, self.st0, self.st6, self.st0, self.st7, self.st0, self.st8, self.st0, self.st9, self.st0, self.st10, self.st0, self.st11, self.st0, self.st12, self.st0, self.st13, self.st0, self.st14, self.st0, self.st15, self.st0, self.st16, self.st0, self.st17, self.st0, self.st18, self.st0, self.st19, self.st0, self.st20, self.st0, self.st21, self.st0, self.st22, self.st0, self.st23, self.st0, self.st24, self.st0, self.st25, self.st0, self.st26, self.st0, self.st27, self.st0, self.st28, self.st0, self.st29, self.st0, self.st30, self.st0, self.st31, self.st0, self.st32)

__all__ = ['MyCComment']
