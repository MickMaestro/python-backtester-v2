"""vo — converted from MQL5: MQL5 Indicators/Vo/vo.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Volatility indicator'}, 'levels': [], 'description': [], 'name': 'vo', 'source': 'MQL5 Indicators/Vo/vo.mq5', 'folder': 'Vo', 'inputs': [{'mql': 'XPeriod', 'py': 'XPeriod', 'param': 'XPeriod', 'type': 'uint', 'default': 20, 'label': 'extremums searching period', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'averaging method', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XPeriod = _input('XPeriod', 20)  # extremums searching period
XMA_Method = _input('XMA_Method', MODE_JJMA)  # averaging method
XLength = _input('XLength', 5)  # smoothing depth
XPhase = _input('XPhase', 15)  # smoothing parameter,
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_ = 0
min_rates_total = 0

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = _int(XPeriod)
    min_rates_total = min_rates_ + XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Vo')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    maxbar = rates_total - 1 - min_rates_
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    for bar in range(limit, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, XPeriod)]
        LL = low[ArrayMinimum(low, bar, XPeriod)]
        IndBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, _fdiv(HH - LL, Point()), bar, True)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vo(_MQL5Indicator):
    name = 'vo'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XPeriod': 20,  # extremums searching period
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # averaging method
        'XLength': 5,  # smoothing depth
        'XPhase': 15,  # smoothing parameter,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

