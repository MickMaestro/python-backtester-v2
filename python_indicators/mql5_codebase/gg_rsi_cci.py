"""gg-rsi-cci — converted from MQL5: MQL5 Indicators/GG-RSI-CCI/gg-rsi-cci.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_maximum': 0.9, 'indicator_minimum': 0.4}, 'types': {1: 10}, 'colors': {1: [9639167, 8421504, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'GG-RSI-CCI'}, 'levels': [], 'description': [], 'name': 'gg-rsi-cci', 'source': 'MQL5 Indicators/GG-RSI-CCI/gg-rsi-cci.mq5', 'folder': 'GG-RSI-CCI', 'inputs': [{'mql': 'IndPeriod', 'py': 'IndPeriod', 'param': 'IndPeriod', 'type': 'int', 'default': 8, 'label': 'RSI and CCI indicators period', 'sinput': False}, {'mql': 'Applied_Price', 'py': 'Applied_Price', 'param': 'Applied_Price', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 2, 'label': 'smoothing method', 'sinput': False}, {'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'int', 'default': 14, 'label': 'rough smoothing of indicators', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'int', 'default': 20, 'label': 'specifying smoothing of indicators', 'sinput': False}, {'mql': 'Smooth_Phase', 'py': 'Smooth_Phase', 'param': 'Smooth_Phase', 'type': 'int', 'default': 100, 'label': 'smoothing parameter,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
IndPeriod = _input('IndPeriod', 8)  # RSI and CCI indicators period
Applied_Price = _input('Applied_Price', PRICE_CLOSE)  # type of price
SmoothMethod = _input('SmoothMethod', MODE_SMMA)  # smoothing method
Period1 = _input('Period1', 14)  # rough smoothing of indicators
Period2 = _input('Period2', 20)  # specifying smoothing of indicators
Smooth_Phase = _input('Smooth_Phase', 100)  # smoothing parameter,
RSI_Handle = 0
CCI_Handle = 0
min_rates = 0
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global CCI_Handle, RSI_Handle, min_rates, min_rates_total
    min_rates_1 = XMA1.GetStartBars(SmoothMethod, Period1, Smooth_Phase)
    min_rates_2 = XMA1.GetStartBars(SmoothMethod, Period2, Smooth_Phase)
    min_rates = IndPeriod
    min_rates_total = min_rates + MathMax(min_rates_1, min_rates_2)
    RSI_Handle = iRSI(None, PERIOD_CURRENT, IndPeriod, Applied_Price)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI indicator')
    CCI_Handle = iCCI(None, PERIOD_CURRENT, IndPeriod, Applied_Price)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iCCI indicator')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    XMA1.XMALengthCheck('Period1', Period1)
    XMA1.XMALengthCheck('Period2', Period2)
    XMA1.XMAPhaseCheck('Smooth_Phase', Smooth_Phase, SmoothMethod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'GG-RSI-CCI')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(RSI_Handle) < rates_total or BarsCalculated(CCI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    MaxBar = 0
    x1cci = 0.0
    x2cci = 0.0
    x1rsi = 0.0
    x2rsi = 0.0
    CCI = Arr(0, 0.0)
    RSI = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    MaxBar = rates_total - min_rates - 1
    ArraySetAsSeries(CCI, True)
    ArraySetAsSeries(RSI, True)
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        x1rsi = XMA1.XMASeries(MaxBar, prev_calculated, rates_total, SmoothMethod, Smooth_Phase, Period1, RSI[bar], bar, True)
        x2rsi = XMA2.XMASeries(MaxBar, prev_calculated, rates_total, SmoothMethod, Smooth_Phase, Period2, RSI[bar], bar, True)
        x1cci = XMA3.XMASeries(MaxBar, prev_calculated, rates_total, SmoothMethod, Smooth_Phase, Period1, CCI[bar], bar, True)
        x2cci = XMA4.XMASeries(MaxBar, prev_calculated, rates_total, SmoothMethod, Smooth_Phase, Period2, CCI[bar], bar, True)
        IndBuffer[bar] = 1.0
        if x1rsi > x2rsi and x1cci > x2cci:
            ColorIndBuffer[bar] = 2.0
        elif x1rsi < x2rsi and x1cci < x2cci:
            ColorIndBuffer[bar] = 0.0
        else:
            ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
XMA4 = _alloc(CXMA)
XMA4.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GgRsiCci(_MQL5Indicator):
    name = 'gg-rsi-cci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IndPeriod': 8,  # RSI and CCI indicators period
        'Applied_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=2),  # smoothing method
        'Period1': 14,  # rough smoothing of indicators
        'Period2': 20,  # specifying smoothing of indicators
        'Smooth_Phase': 100,  # smoothing parameter,
    }
    y_range = (0.4, 0.9)

