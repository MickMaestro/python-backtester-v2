"""Axis.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *

# enum ENUM_AXIS_TYPE
AXIS_TYPE_DOUBLE = 0
AXIS_TYPE_DATETIME = 1
AXIS_TYPE_CUSTOM = 2
_enum('ENUM_AXIS_TYPE', {0: 'AXIS_TYPE_DOUBLE', 1: 'AXIS_TYPE_DATETIME', 2: 'AXIS_TYPE_CUSTOM'})


class CAxis(MqlObject):
    _q_fields = ('m_min', 'm_max', 'm_step', 'm_clr', 'm_name', 'm_name_size', 'm_values_size', 'm_values_width', 'm_values_format', 'm_values_fontname', 'm_values_fontflags', 'm_values_fontangle', 'm_auto_scale', 'm_zero_lever', 'm_default_step', 'm_max_labels', 'm_min_grace', 'm_max_grace', 'm_values_dt_mode', 'm_values_func', 'm_values_cbdata', 'm_type')
    def __init__(self):
        self.m_min = 0.0
        self.m_max = 0.0
        self.m_step = 0.0
        self.m_clr = 0
        self.m_name = ""
        self.m_name_size = 0
        self.m_values_size = 0
        self.m_values_width = 0
        self.m_values_format = ""
        self.m_values_fontname = ""
        self.m_values_fontflags = 0
        self.m_values_fontangle = 0
        self.m_auto_scale = False
        self.m_zero_lever = 0.0
        self.m_default_step = 0.0
        self.m_max_labels = 0.0
        self.m_min_grace = 0.0
        self.m_max_grace = 0.0
        self.m_values_dt_mode = 0
        self.m_values_func = None
        self.m_values_cbdata = 0
        self.m_type = 0
        self.m_auto_scale = True
        self.m_zero_lever = 0.25
        self.m_default_step = 25.0
        self.m_max_labels = 15.0
        self.m_min_grace = 0.01
        self.m_max_grace = 0.01
        self.m_clr = clrBlack
        self.m_name_size = 0
        self.m_values_size = 12
        self.m_values_fontname = 'arial'
        self.m_values_fontflags = 0
        self.m_values_fontangle = 0
        self.m_values_func = None
        self.m_values_cbdata = None
        self.m_values_dt_mode = TIME_MINUTES
        self.m_type = AXIS_TYPE_DOUBLE
        self.m_values_width = 30
    def _q_dtor(self):
        pass
    def Step(self):
        return self.m_step
    def Min_0(self):
        return self.m_min
    def Min_1(self, min_):
        self.m_min = min_
    def Max_0(self):
        return self.m_max
    def Max_1(self, max_):
        self.m_max = max_
    def Name_0(self):
        return self.m_name
    def Name_1(self, name):
        self.m_name = name
    def Type_0(self):
        return self.m_type
    def Type_1(self, type_):
        self.m_type = type_
    def Color_0(self):
        return self.m_clr
    def Color_1(self, clr):
        self.m_clr = clr
    def AutoScale_0(self):
        return self.m_auto_scale
    def AutoScale_1(self, auto):
        self.m_auto_scale = auto
    def ValuesSize_0(self):
        return self.m_values_size
    def ValuesSize_1(self, size):
        self.m_values_size = size
    def ValuesWidth_0(self):
        return self.m_values_width
    def ValuesWidth_1(self, width):
        self.m_values_width = width
    def ValuesFormat_0(self):
        return self.m_values_format
    def ValuesFormat_1(self, format):
        self.m_values_format = format
    def ValuesDateTimeMode_0(self):
        return self.m_values_dt_mode
    def ValuesDateTimeMode_1(self, mode):
        self.m_values_dt_mode = mode
    def ValuesFunctionFormat_0(self):
        return self.m_values_func
    def ValuesFunctionFormat_1(self, func):
        self.m_values_func = func
    def ValuesFunctionFormatCBData_0(self):
        return self.m_values_cbdata
    def ValuesFunctionFormatCBData_1(self, cbdata):
        self.m_values_cbdata = cbdata
    def ValuesFontName_0(self):
        return self.m_values_fontname
    def ValuesFontName_1(self, fontname):
        self.m_values_fontname = fontname
    def ValuesFontAngle_0(self):
        return self.m_values_fontangle
    def ValuesFontAngle_1(self, fontangle):
        self.m_values_fontangle = fontangle
    def ValuesFontFlags_0(self):
        return self.m_values_fontflags
    def ValuesFontFlags_1(self, fontflags):
        self.m_values_fontflags = fontflags
    def NameSize_0(self):
        return self.m_name_size
    def NameSize_1(self, size):
        self.m_name_size = size
    def ZeroLever_0(self):
        return self.m_zero_lever
    def ZeroLever_1(self, value):
        self.m_zero_lever = value
    def DefaultStep_0(self):
        return self.m_default_step
    def DefaultStep_1(self, value):
        self.m_default_step = value
    def MaxLabels_0(self):
        return self.m_max_labels
    def MaxLabels_1(self, value):
        self.m_max_labels = value
    def MinGrace_0(self):
        return self.m_min_grace
    def MinGrace_1(self, value):
        self.m_min_grace = value
    def MaxGrace_0(self):
        return self.m_max_grace
    def MaxGrace_1(self, value):
        self.m_max_grace = value
    def SelectAxisScale(self):
        if self.m_min > self.m_max:
            self.m_max = self.m_min
        if not self.m_auto_scale:
            if self.m_max <= self.m_min:
                self.ExtensionBoundaries()
            self.m_step = (self.m_default_step if ((self.m_max - self.m_min) > self.m_default_step and self.m_default_step > 0) else (self.m_max - self.m_min))
            return
        self.ExtensionBoundaries()
        if (self.m_max - self.m_min) < 1e-30:
            self.m_max = self.m_max + (0.2 * (1.0 if (self.m_max == 0) else MathAbs(self.m_max)))
            self.m_min = self.m_min - (0.2 * (1.0 if (self.m_min == 0) else MathAbs(self.m_min)))
        if self.m_min > 0 and _fdiv(self.m_min, self.m_max - self.m_min) < self.m_zero_lever:
            self.m_min = 0.0
        if self.m_max < 0 and MathAbs(_fdiv(self.m_max, self.m_max - self.m_min)) < self.m_zero_lever:
            self.m_max = 0.0
        target_step = (self.m_default_step if (self.m_default_step != 0) else (self.m_max - self.m_min))
        self.m_step = self.CalcStepSize(self.m_max - self.m_min, target_step)
        labels = MathCeil(_fdiv(self.m_max - self.m_min, self.m_step))
        if self.m_max_labels < labels and self.m_max_labels > 0:
            self.m_step = self.CalcBoundedStepSize(self.m_max - self.m_min, self.m_max_labels)
        else:
            self.m_step = self.CalcBoundedStepSize(self.m_max - self.m_min, labels)
        self.m_min = self.m_min - self.Mod(self.m_min, self.m_step)
        self.m_max = (self.m_max if (self.Mod(self.m_max, self.m_step) == 0.0) else (self.m_max + self.m_step - self.Mod(self.m_max, self.m_step)))
    def ExtensionBoundaries(self):
        range_ = self.m_max - self.m_min
        if self.m_min < 0 or (self.m_min - (self.m_min_grace * range_)) >= 0.0:
            self.m_min = self.m_min - (self.m_min_grace * range_)
        if self.m_max > 0 or (self.m_max + (self.m_max_grace * range_)) <= 0.0:
            self.m_max = self.m_max + (self.m_max_grace * range_)
        if self.m_max == self.m_min:
            if MathAbs(self.m_max) > 1e-100:
                self.m_max *= (0.95 if (self.m_min < 0) else 1.05)
                self.m_min *= (1.05 if (self.m_min < 0) else 0.95)
            else:
                self.m_max = 1.0
                self.m_min = -1.0
    def CalcStepSize(self, range_, steps):
        temp = _fdiv(range_, steps)
        mag = MathFloor(MathLog10(temp))
        magPow = MathPow(10.0, mag)
        magMsd = NormalizeDouble(_fdiv(temp, magPow) + 0.5, 0)
        if magMsd > 5.0:
            magMsd = 10.0
        elif magMsd > 2.0:
            magMsd = 5.0
        elif magMsd > 1.0:
            magMsd = 2.0
        return magMsd * magPow
    def Mod(self, x, y):
        if y == 0:
            return 0.0
        return (MathMod(x, y) if (x > 0) else (MathMod(x, y) + y))
    def CalcBoundedStepSize(self, range_, max_steps):
        temp = _fdiv(range_, max_steps)
        mag = MathFloor(MathLog10(temp))
        magPow = MathPow(10.0, mag)
        magMsd = MathCeil(_fdiv(temp, magPow))
        if magMsd > 5.0:
            magMsd = 10.0
        elif magMsd > 2.0:
            magMsd = 5.0
        elif magMsd > 1.0:
            magMsd = 2.0
        return magMsd * magPow

__all__ = ['AXIS_TYPE_DOUBLE', 'AXIS_TYPE_DATETIME', 'AXIS_TYPE_CUSTOM', 'CAxis']
