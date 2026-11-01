"""ttf — converted from MQL5: MQL5 Indicators/TTF/ttf.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [13382297], 2: [16711935]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TTF', 2: 'Signal'}, 'levels': [0.0], 'description': [], 'name': 'ttf', 'source': 'MQL5 Indicators/TTF/ttf.mq5', 'folder': 'TTF', 'inputs': [{'mql': 'TTFbars', 'py': 'TTFbars', 'param': 'TTFbars', 'type': 'uint', 'default': 8, 'label': 'extremums searching period', 'sinput': False}, {'mql': 'TopLine', 'py': 'TopLine', 'param': 'TopLine', 'type': 'int', 'default': 75, 'label': 'top level to trigger', 'sinput': False}, {'mql': 'BottomLine', 'py': 'BottomLine', 'param': 'BottomLine', 'type': 'int', 'default': -75, 'label': 'bottom level to trigger', 'sinput': False}, {'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'uint', 'default': 14, 'label': 'T3 smoothing period', 'sinput': False}, {'mql': 'b_', 'py': 'b_', 'param': 'b_', 'type': 'double', 'default': 70.0, 'label': 'Coefficient b x100', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
TTFbars = _input('TTFbars', 8)  # extremums searching period
TopLine = _input('TopLine', 75)  # top level to trigger
BottomLine = _input('BottomLine', -75)  # bottom level to trigger
T3Period = _input('T3Period', 14)  # T3 smoothing period
b_ = _input('b_', 70.0)  # Coefficient b x100
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
TTFBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
CP_Handle = 0
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int((2 * TTFbars) + 1)
    SetIndexBuffer(0, TTFBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(TTFBuffer, True)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SignalBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'TTF(', TTFbars, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar = 0
    HHRecent = 0.0
    LLOlder = 0.0
    HHOlder = 0.0
    LLRecent = 0.0
    BuyPower = 0.0
    SellPower = 0.0
    TTF = 0.0
    T3TTF = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    maxbar = rates_total - 2 - min_rates_total
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HHRecent = high[ArrayMaximum(high, bar, TTFbars)]
        LLRecent = low[ArrayMinimum(low, bar, TTFbars)]
        HHOlder = high[ArrayMaximum(high, bar + TTFbars, TTFbars)]
        LLOlder = low[ArrayMinimum(low, bar + TTFbars, TTFbars)]
        BuyPower = HHRecent - LLOlder
        SellPower = HHOlder - LLRecent
        TTF = _fdiv(BuyPower - SellPower, 0.5 * (BuyPower + SellPower)) * 100
        T3TTF = _s_OnCalculate_T3_.T3Series(maxbar, prev_calculated, rates_total, 0, b_, T3Period, TTF, bar, True)
        TTFBuffer[bar] = T3TTF
        if T3TTF >= 0:
            SignalBuffer[bar] = TopLine
        else:
            SignalBuffer[bar] = BottomLine
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_T3_ = CT3()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ttf(_MQL5Indicator):
    name = 'ttf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TTFbars': 8,  # extremums searching period
        'TopLine': 75,  # top level to trigger
        'BottomLine': -75,  # bottom level to trigger
        'T3Period': 14,  # T3 smoothing period
        'b_': 70.0,  # Coefficient b x100
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

