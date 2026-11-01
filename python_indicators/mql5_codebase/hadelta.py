"""hadelta — converted from MQL5: MQL5 Indicators/HaDelta/hadelta.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 10, 2: 1, 3: 1}, 'colors': {1: [42495, 3329330], 2: [6908265], 3: [9662683]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'HaDelta histogram', 2: 'HaDelta', 3: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'hadelta', 'source': 'MQL5 Indicators/HaDelta/hadelta.mq5', 'folder': 'HaDelta', 'inputs': [{'mql': 'BetterFormula', 'py': 'BetterFormula', 'param': 'BetterFormula', 'type': 'bool', 'default': False, 'label': 'BetterFormula', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 0, 'label': 'signal line smoothing method', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 3, 'label': 'signal line period', 'sinput': False}, {'mql': 'Signal_Phase', 'py': 'Signal_Phase', 'param': 'Signal_Phase', 'type': 'int', 'default': 100, 'label': 'signal line parameter,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
BetterFormula = _input('BetterFormula', False)  # BetterFormula
Signal_Method = _input('Signal_Method', MODE_SMA)  # signal line smoothing method
Signal_XMA = _input('Signal_XMA', 3)  # signal line period
Signal_Phase = _input('Signal_Phase', 100)  # signal line parameter,
min_rates_total = 0
HaDeltaBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
HistBuffer = Arr(0, 0.0)
ColorHistBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 2 + XMA.GetStartBars(Signal_Method, Signal_XMA, Signal_Phase)
    SetIndexBuffer(0, HistBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorHistBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, HaDeltaBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    XMA.XMALengthCheck('Signal_XMA', Signal_XMA)
    XMA.XMAPhaseCheck('Signal_Phase', Signal_Phase, Signal_Method)
    shortname = Box("")
    Smooth = XMA.GetString_MA_Method(Signal_Method)
    StringConcatenate(shortname, 'HaDelta( ', BetterFormula, ', ', Signal_XMA, ', ', Smooth, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_haClose1, _s_OnCalculate_haOpen1
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    prOpen = 0.0
    prClose = 0.0
    prLow = 0.0
    prHigh = 0.0
    haClose = 0.0
    haOpen = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_haOpen1 = open[first]
        _s_OnCalculate_haClose1 = close[first]
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        prOpen = open[bar]
        prClose = close[bar]
        prLow = low[bar]
        prHigh = high[bar]
        if BetterFormula:
            if prHigh != prLow:
                haClose = ((prOpen + prClose) / 2.0) + (_fdiv(prClose - prOpen, prHigh - prLow) * MathAbs((prClose - prOpen) / 2.0))
            else:
                haClose = (prOpen + prClose) / 2.0
        else:
            haClose = (prOpen + prHigh + prLow + prClose) / 4
        haOpen = (_s_OnCalculate_haOpen1 + _s_OnCalculate_haClose1) / 2.0
        HaDeltaBuffer[bar] = haClose - haOpen
        HistBuffer[bar] = HaDeltaBuffer[bar]
        if HaDeltaBuffer[bar] > 0:
            ColorHistBuffer[bar] = 1.0
        if HaDeltaBuffer[bar] < 0:
            ColorHistBuffer[bar] = 0.0
        SignBuffer[bar] = XMA.XMASeries(1, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, HaDeltaBuffer[bar], bar, False)
        if bar < (rates_total - 1):
            _s_OnCalculate_haOpen1 = haOpen
            _s_OnCalculate_haClose1 = haClose
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()

# ---- static local variables
_s_OnCalculate_haClose1 = 0.0
_s_OnCalculate_haOpen1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Hadelta(_MQL5Indicator):
    name = 'hadelta'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BetterFormula': False,  # BetterFormula
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # signal line smoothing method
        'Signal_XMA': 3,  # signal line period
        'Signal_Phase': 100,  # signal line parameter,
    }

