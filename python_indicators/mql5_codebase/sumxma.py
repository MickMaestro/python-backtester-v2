"""sumxma — converted from MQL5: MQL5 Indicators/SumXMA/sumxma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13458026]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'SumXMA'}, 'levels': [], 'description': [], 'name': 'sumxma', 'source': 'MQL5 Indicators/SumXMA/sumxma.mq5', 'folder': 'SumXMA', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'smoothing method', 'sinput': False}, {'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'uint', 'default': 20, 'label': 'initial smoothing period', 'sinput': False}, {'mql': 'EndLength', 'py': 'EndLength', 'param': 'EndLength', 'type': 'uint', 'default': 100, 'label': 'final smoothing period', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in pointsх', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA)  # smoothing method
StartLength = _input('StartLength', 20)  # initial smoothing period
EndLength = _input('EndLength', 100)  # final smoothing period
XPhase = _input('XPhase', 15)  # smoothing parameter,
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in pointsх
SumXMABuffer = Arr(0, 0.0)
Init = False
min_rates_total = 0
xSize = 0
dPriceShift = 0.0

def OnInit():
    global Init, dPriceShift, min_rates_total, xSize
    if StartLength > EndLength:
        Init = False
        Print('The initial period of the indicator can not be greater than the final period!')
        return
    xSize = _int(EndLength - StartLength + 1)
    if ArrayResize(XMA, xSize) < xSize:
        Init = False
        Print('Failed to distribute the memory for XMA[] object array!')
        return
    else:
        Init = True
    min_rates_total = XMA[0].GetStartBars(XMA_Method, EndLength, XPhase)
    XMA[0].XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, SumXMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SumXMABuffer, True)
    Smooth = XMA[0].GetString_MA_Method(XMA_Method)
    shortname = Box("")
    StringConcatenate(shortname, 'SumXMA(', Smooth, ', ', StartLength, ', ', EndLength, ', ', XPhase, ', ', Shift, ', ', PriceShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, begin, price):
    if (not Init) or (rates_total + begin) < min_rates_total:
        return 0
    MaxBar = 0
    limit = 0
    bar = 0
    Sum = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1 - begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        limit = rates_total - prev_calculated
    MaxBar = rates_total - min_rates_total - 1 - begin
    ArraySetAsSeries(price, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Sum = 0.0
        number = 0
        while number < xSize:
            Sum += XMA[number].XMASeries(MaxBar, prev_calculated, rates_total, XMA_Method, XPhase, StartLength + number, price[bar], bar, True)
            number += 1
        SumXMABuffer[bar] = (Sum / (EndLength - StartLength + 1)) + dPriceShift
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = Arr(0, 0, factory=CXMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Sumxma(_MQL5Indicator):
    name = 'sumxma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # smoothing method
        'StartLength': 20,  # initial smoothing period
        'EndLength': 100,  # final smoothing period
        'XPhase': 15,  # smoothing parameter,
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in pointsх
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

