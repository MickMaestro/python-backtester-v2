"""waddah_attar_def_rsi — converted from MQL5: MQL5 Indicators/Waddah_Attar_Def_RSI/waddah_attar_def_rsi.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [9639167, 16711935, 8421504, 16748574, 2330219]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: '2pbIdealXOSMA'}, 'levels': [], 'description': [], 'name': 'waddah_attar_def_rsi', 'source': 'MQL5 Indicators/Waddah_Attar_Def_RSI/waddah_attar_def_rsi.mq5', 'folder': 'Waddah_Attar_Def_RSI', 'inputs': [{'mql': 'RSIPeriod1', 'py': 'RSIPeriod1', 'param': 'RSIPeriod1', 'type': 'uint', 'default': 14, 'label': 'fast RSI period', 'sinput': False}, {'mql': 'RSIPeriod2', 'py': 'RSIPeriod2', 'param': 'RSIPeriod2', 'type': 'uint', 'default': 28, 'label': 'slow  RSI period', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'smoothing method', 'sinput': False}, {'mql': 'Smooth_XMA', 'py': 'Smooth_XMA', 'param': 'Smooth_XMA', 'type': 'uint', 'default': 9, 'label': 'smoothing period', 'sinput': False}, {'mql': 'Smooth_Phase', 'py': 'Smooth_Phase', 'param': 'Smooth_Phase', 'type': 'int', 'default': 100, 'label': 'smoothing parameter,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
RSIPeriod1 = _input('RSIPeriod1', 14)  # fast RSI period
RSIPeriod2 = _input('RSIPeriod2', 28)  # slow  RSI period
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # smoothing method
Smooth_XMA = _input('Smooth_XMA', 9)  # smoothing period
Smooth_Phase = _input('Smooth_Phase', 100)  # smoothing parameter,
min_rates_ = 0
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
FRSI_Handle = 0
SRSI_Handle = 0

def OnInit():
    global FRSI_Handle, SRSI_Handle, min_rates_, min_rates_total
    min_rates_ = _int(MathMax(RSIPeriod1, RSIPeriod2))
    min_rates_total = min_rates_ + XMA1.GetStartBars(SmoothMethod, Smooth_XMA, Smooth_Phase)
    FRSI_Handle = iRSI(None, 0, RSIPeriod1, PRICE_WEIGHTED)
    if FRSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI indicator')
    SRSI_Handle = iRSI(None, 0, RSIPeriod2, PRICE_WEIGHTED)
    if SRSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI indicator')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'Ind')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    XMA1.XMALengthCheck('Smooth_XMA', Smooth_XMA)
    XMA1.XMAPhaseCheck('Smooth_Phase', Smooth_Phase, SmoothMethod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Waddah_Attar_Def_RSI')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(FRSI_Handle) < rates_total or BarsCalculated(SRSI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    drsi = 0.0
    FRSI = Arr(0, 0.0)
    SRSI = Arr(0, 0.0)
    maxbar = rates_total - 1 - min_rates_
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(FRSI_Handle, 0, 0, to_copy, FRSI) <= 0:
        return 0
    if CopyBuffer(SRSI_Handle, 0, 0, to_copy, SRSI) <= 0:
        return 0
    ArraySetAsSeries(FRSI, True)
    ArraySetAsSeries(SRSI, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        drsi = FRSI[bar] - SRSI[bar]
        IndBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, SmoothMethod, Smooth_Phase, Smooth_XMA, drsi, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorIndBuffer[bar] = 2.0
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 4.0
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 3.0
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 0.0
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WaddahAttarDefRsi(_MQL5Indicator):
    name = 'waddah_attar_def_rsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod1': 14,  # fast RSI period
        'RSIPeriod2': 28,  # slow  RSI period
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # smoothing method
        'Smooth_XMA': 9,  # smoothing period
        'Smooth_Phase': 100,  # smoothing parameter,
    }

