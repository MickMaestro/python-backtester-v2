"""FX Fish 2MA — converted from MQL5: MQL5 Indicators/FX Fish 2MA/FX Fish 2MA.mq5

Copyright: Copyright © 2005, Kiko Segui; Link: webtecnic@terra.es; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Kiko Segui', 'link': 'webtecnic@terra.es', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 10, 2: 1, 3: 1}, 'colors': {1: [42495, 11829830], 2: [16711680], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'FX Fish 2MA', 'source': 'MQL5 Indicators/FX Fish 2MA/FX Fish 2MA.mq5', 'folder': 'FX Fish 2MA', 'inputs': [{'mql': 'CalculatePeriod', 'py': 'CalculatePeriod', 'param': 'CalculatePeriod', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'CalculatePrice', 'py': 'CalculatePrice', 'param': 'CalculatePrice', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'MA1period', 'py': 'MA1period', 'param': 'MA1period', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'MA2period', 'py': 'MA2period', 'param': 'MA2period', 'type': 'int', 'default': 45, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
CalculatePeriod = _input('CalculatePeriod', 10)
CalculatePrice = _input('CalculatePrice', PRICE_MEDIAN)
MA1period = _input('MA1period', 9)
TypeMA1 = MODE_SMA
MA2period = _input('MA2period', 45)
TypeMA2 = MODE_LWMA
Color_HistogramBuffer = Arr(0, 0.0)
Color_HistogramColors = Arr(0, 0.0)
MA1buffer = Arr(0, 0.0)
MA2buffer = Arr(0, 0.0)
Value = 0.0
Value1 = 0.0
Fish = 0.0
Fish1 = 0.0
weightsum_ma2 = 0

def OnInit():
    global Fish, Fish1, Value, Value1, weightsum_ma2
    Value = 0.0
    Value1 = 0.0
    Fish = 0.0
    Fish1 = 0.0
    weightsum_ma2 = 0
    SetIndexBuffer(0, Color_HistogramBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Color_HistogramColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, MA1buffer, INDICATOR_DATA)
    SetIndexBuffer(3, MA2buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Fish')
    PlotIndexSetString(1, PLOT_LABEL, 'Fish Aver(' + IntegerToString(MA1period) + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'Fish Aver Aver(' + IntegerToString(MA2period) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Fish, Fish1, Value, Value1
    limit = 0
    if prev_calculated > 0:
        limit = prev_calculated - 1
    _price = 0.0
    MinL = 0.0
    MaxH = 0.0
    Threshold = 1.2
    for i in range(limit, rates_total):
        start = (0 if ((i - CalculatePeriod) < 0) else (i - CalculatePeriod))
        index_max = ArrayMaximum(high, start, CalculatePeriod)
        index_min = ArrayMinimum(low, start, CalculatePeriod)
        MaxH = high[ArrayMaximum(high, start, CalculatePeriod)]
        MinL = low[ArrayMinimum(low, start, CalculatePeriod)]
        _sw1 = CalculatePrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        else:
            _price = (high[i] + low[i] + close[i] + open[i]) / 4.0
        Value = (((0.33 * 2 * (_fdiv(_price - MinL, MaxH - MinL) - 0.5)) + (0.67 * Value1)) if ((MaxH - MinL) != 0.0) else (0.67 * Value1))
        Value = MathMin(MathMax(Value, -0.999), 0.999)
        Fish = (0.5 * MathLog(_fdiv(1.0 + Value, 1.0 - Value))) + (0.5 * Fish1)
        Color_HistogramBuffer[i] = Fish
        Color_HistogramColors[i] = (0 if (Color_HistogramBuffer[i] < 0.0) else 1)
        Value1 = Value
        Fish1 = Fish
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, MA1period, Color_HistogramBuffer, MA1buffer)
    LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, MA2period, MA1buffer, MA2buffer, _GlobRef(globals(), 'weightsum_ma2'))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FXFish2MA(_MQL5Indicator):
    name = 'FX Fish 2MA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CalculatePeriod': 10,
        'CalculatePrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),
        'MA1period': 9,
        'MA2period': 45,
    }

