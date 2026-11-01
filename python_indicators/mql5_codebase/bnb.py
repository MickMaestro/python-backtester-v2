"""BnB — converted from MQL5: MQL5 Indicators/BnB/BnB.mq5

BnB
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [13850042, 16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'BnB'}, 'levels': [], 'description': ['BnB'], 'name': 'BnB', 'source': 'MQL5 Indicators/BnB/BnB.mq5', 'folder': 'BnB', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 14, 'label': 'глубина усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_T3)  # метод усреднения
XLength = _input('XLength', 14)  # глубина усреднения
XPhase = _input('XPhase', 15)  # параметр сглаживания,
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BnB')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    tic = 0.0
    diff = 0.0
    bears = 0.0
    bulls = 0.0
    first = 0
    bar = 0
    vol = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if VolumeType == VOLUME_TICK:
            vol = tick_volume[bar]
        else:
            vol = volume[bar]
        if not vol:
            vol = 1
        tic = _fdiv(high[bar] - low[bar], vol)
        diff = 0.0
        if open[bar] > close[bar]:
            diff = _fdiv(high[bar] - low[bar] - (open[bar] - close[bar]), 2 * tic)
        if open[bar] < close[bar]:
            diff = _fdiv(high[bar] - low[bar] - (close[bar] - open[bar]), 2 * tic)
        if open[bar] > close[bar]:
            bulls = _fdiv(open[bar] - close[bar], tic) + diff
        else:
            bulls = diff
        if open[bar] < close[bar]:
            bears = _fdiv(close[bar] - open[bar], tic) + diff
        else:
            bears = diff
        UpBuffer[bar] = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, bulls, bar, False)
        DnBuffer[bar] = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, bears, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BnB(_MQL5Indicator):
    name = 'BnB'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения
        'XLength': 14,  # глубина усреднения
        'XPhase': 15,  # параметр сглаживания,
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
    }

