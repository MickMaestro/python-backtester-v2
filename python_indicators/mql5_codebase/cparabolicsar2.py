"""cparabolicsar2 — converted from MQL5: MQL5 Indicators/Color Parabolic 2/cparabolicsar2.mq5

Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [16711680, 8388736, 8519755, 2970272, 11829830, 16776960, 8388352, 55295, 65535, 15134970, 16449525]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'cparabolicsar2', 'source': 'MQL5 Indicators/Color Parabolic 2/cparabolicsar2.mq5', 'folder': 'Color Parabolic 2', 'inputs': [{'mql': 'InpSARStep', 'py': 'InpSARStep', 'param': 'InpSARStep', 'type': 'double', 'default': 0.02, 'label': 'Step', 'sinput': False}, {'mql': 'InpSARMaximum', 'py': 'InpSARMaximum', 'param': 'InpSARMaximum', 'type': 'double', 'default': 0.2, 'label': 'Maximum', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSARStep = _input('InpSARStep', 0.02)  # Step
InpSARMaximum = _input('InpSARMaximum', 0.2)  # Maximum
ExtSARBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
c_parab = None
ExtSarStep = 0.0
ExtSarMaximum = 0.0

class CParabolic(MqlObject):
    _q_fields = ('c_SARStep', 'c_SARMaximum', 'c_AF', 'MaxHigh', 'MinLow', 'Sar_P', 'TmpFlag', 'Flag', 'totlSar')
    def __init__(self, *args):
        self.c_SARStep = 0.0
        self.c_SARMaximum = 0.0
        self.c_AF = 0.0
        self.MaxHigh = 0.0
        self.MinLow = 0.0
        self.Sar_P = 0.0
        self.TmpFlag = Arr(4, 0.0, dyn=False)
        self.Flag = 0
        self.totlSar = 0
    def GetColor(self):
        return _int(MathCeil(_fdiv(self.c_AF, self.c_SARStep))) - 1
    def Init(self, SARStep, SARMaximum, high, low, totl):
        self.totlSar = totl
        self.c_SARStep = SARStep
        self.c_SARMaximum = SARMaximum
        self.MaxHigh = high[0]
        self.MinLow = low[0]
        self.Sar_P = low[0]
        self.Flag = 1
        self.c_AF = self.c_SARStep
    def Calc(self, high, low, i):
        if i < (self.totlSar - 1):
            if self.Flag == 1:
                if self.MaxHigh < high[i]:
                    self.MaxHigh = high[i]
                    self.c_AF += self.c_SARStep
                    if self.c_AF > self.c_SARMaximum:
                        self.c_AF = self.c_SARMaximum
                self.Sar_P = self.Sar_P + (self.c_AF * (self.MaxHigh - self.Sar_P))
                self.TmpFlag[1] = self.Sar_P
            if self.Flag == -1:
                if self.MinLow > low[i]:
                    self.MinLow = low[i]
                    self.c_AF += self.c_SARStep
                    if self.c_AF > self.c_SARMaximum:
                        self.c_AF = self.c_SARMaximum
                self.Sar_P = self.Sar_P + (self.c_AF * (self.MinLow - self.Sar_P))
                self.TmpFlag[1] = self.Sar_P
            if self.Flag == 1:
                if low[i] < self.Sar_P:
                    self.Flag = -1
                    self.c_AF = self.c_SARStep
                    self.Sar_P = self.MaxHigh
                    self.MinLow = low[i]
                    self.MaxHigh = high[i]
            if self.Flag == -1:
                if high[i] > self.Sar_P:
                    self.Flag = 1
                    self.c_AF = self.c_SARStep
                    self.Sar_P = self.MinLow
                    self.MinLow = low[i]
                    self.MaxHigh = high[i]
        if i >= (self.totlSar - 1):
            if self.Flag == 1:
                if self.MaxHigh < high[i]:
                    self.MaxHigh = high[i]
                    if (self.TmpFlag[0] == i and self.TmpFlag[2] == 1) and self.TmpFlag[3] == 1:
                        self.c_AF += self.c_SARStep
                        if self.c_AF > self.c_SARMaximum:
                            self.c_AF = self.c_SARMaximum
                        self.TmpFlag[2] = 0.0
                if self.TmpFlag[0] != i:
                    self.Sar_P = self.TmpFlag[1] + (self.c_AF * (self.MaxHigh - self.TmpFlag[1]))
                    self.TmpFlag[1] = self.Sar_P
                    self.TmpFlag[0] = i
                    self.TmpFlag[2] = 1.0
                    self.TmpFlag[3] = self.Flag
                if low[i] < self.Sar_P:
                    self.Flag = -1
                    self.c_AF = self.c_SARStep
                    self.Sar_P = self.MaxHigh
                    self.TmpFlag[1] = self.Sar_P
                    self.MinLow = low[i]
                    self.MaxHigh = high[i]
            if self.Flag == -1:
                if self.MinLow > low[i]:
                    self.MinLow = low[i]
                    if (self.TmpFlag[0] == i and self.TmpFlag[2] == 1) and self.TmpFlag[3] == -1:
                        self.c_AF += self.c_SARStep
                        if self.c_AF > self.c_SARMaximum:
                            self.c_AF = self.c_SARMaximum
                        self.TmpFlag[2] = 0.0
                if self.TmpFlag[0] != i:
                    self.Sar_P = self.TmpFlag[1] + (self.c_AF * (self.MinLow - self.TmpFlag[1]))
                    self.TmpFlag[1] = self.Sar_P
                    self.TmpFlag[0] = i
                    self.TmpFlag[2] = 1.0
                    self.TmpFlag[3] = self.Flag
                if high[i] > self.Sar_P:
                    self.Flag = 1
                    self.c_AF = self.c_SARStep
                    self.Sar_P = self.MinLow
                    self.TmpFlag[1] = self.Sar_P
                    self.MinLow = low[i]
                    self.MaxHigh = high[i]
        return self.Sar_P

def OnInit():
    global ExtSarMaximum, ExtSarStep, c_parab
    if InpSARStep < 0.0:
        ExtSarStep = 0.02
        Print('The input parameter InpSARStep has incorrect value. Indicator will use value', ExtSarStep, 'for calculations.')
    else:
        ExtSarStep = InpSARStep
    if InpSARMaximum < 0.0:
        ExtSarMaximum = 0.2
        Print('The input parameter InpSARMaximum has incorrect value. Indicator will use value', ExtSarMaximum, 'for calculations.')
    else:
        ExtSarMaximum = InpSARMaximum
    SetIndexBuffer(0, ExtSARBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'SAR(' + DoubleToString(ExtSarStep, 2) + ',' + DoubleToString(ExtSarMaximum, 2) + ')')
    c_parab = CParabolic()
    return 0

def OnDeinit(reason):
    _delete(c_parab)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        if i == 0:
            c_parab.Init(ExtSarStep, ExtSarMaximum, high, low, rates_total)
        if i > 0:
            ExtSARBuffer[i] = c_parab.Calc(high, low, i)
            ExtColorBuffer[i] = c_parab.GetColor()
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Cparabolicsar2(_MQL5Indicator):
    name = 'cparabolicsar2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpSARStep': 0.02,  # Step
        'InpSARMaximum': 0.2,  # Maximum
    }

