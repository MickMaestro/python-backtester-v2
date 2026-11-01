"""xibs — converted from MQL5: MQL5 Indicators/IBS/xibs.mq5

Internal Bar Strength
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Internal Bar Strength'}, 'levels': [60.0, 40.0], 'description': ['Internal Bar Strength'], 'name': 'xibs', 'source': 'MQL5 Indicators/IBS/xibs.mq5', 'folder': 'IBS', 'inputs': [{'mql': 'IMA_Method', 'py': 'IMA_Method', 'param': 'IMA_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'ILength', 'py': 'ILength', 'param': 'ILength', 'type': 'int', 'default': 12, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'IPhase', 'py': 'IPhase', 'param': 'IPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 0, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_LOW = 0
PRICE_HIGH_CLOSE = 1
_enum('Applied_price_', {0: 'PRICE_CLOSE_LOW', 1: 'PRICE_HIGH_CLOSE'})

# ---- inputs and global variables
IMA_Method = _input('IMA_Method', MODE_SMA)  # Smoothing method
ILength = _input('ILength', 12)  # Smoothing depth
IPhase = _input('IPhase', 15)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE_LOW)  # Applied price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
XIBS = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = XMA1.GetStartBars(IMA_Method, ILength, IPhase)
    XMA1.XMALengthCheck('ILength', ILength)
    XMA1.XMAPhaseCheck('IPhase', IPhase, IMA_Method)
    SetIndexBuffer(0, XIBS, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(IMA_Method)
    StringConcatenate(shortname, 'Internal Bar Strength(', Smooth1, ', ', ILength, ', ', IPhase, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    range_ = 0.0
    dprice = 0.0
    ibs = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if IPC:
            dprice = close[bar] - low[bar]
        else:
            dprice = high[bar] - close[bar]
        range_ = high[bar] - low[bar]
        if range_:
            ibs = _fdiv(dprice, range_)
        else:
            ibs = 0.0
        XIBS[bar] = 100 * XMA1.XMASeries(0, prev_calculated, rates_total, IMA_Method, IPhase, ILength, ibs, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xibs(_MQL5Indicator):
    name = 'xibs'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'ILength': 12,  # Smoothing depth
        'IPhase': 15,  # Smoothing parameter
        'IPC': _Choice({0: 'Close-Low', 1: 'High-Close'}, default=0),  # Applied price
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

