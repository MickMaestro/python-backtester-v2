"""is7n_trend — converted from MQL5: MQL5 Indicators/is7n_trend.mq5 (new)/is7n_trend.mq5

Copyright 2010, SHOOTER777
s7n@mail.ru
Copyright: Copyright 2010, ARIES Software Corp.; Link: http://ariess.mp

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, ARIES Software Corp.', 'link': 'http://ariess.mp', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [9109504, 15128749]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'iTrend'}, 'levels': [], 'description': ['Copyright 2010, SHOOTER777', 's7n@mail.ru'], 'name': 'is7n_trend', 'source': 'MQL5 Indicators/is7n_trend.mq5 (new)/is7n_trend.mq5', 'folder': 'is7n_trend.mq5 (new)', 'inputs': [{'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'iMax', 'py': 'iMax', 'param': 'iMax', 'type': 'int', 'default': 200, 'label': 'Maximum number of bars to proceed', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
Per = _input('Per', 20)  # Period
iMax = _input('iMax', 200)  # Maximum number of bars to proceed
dPlot = Arr(0, 0.0)
dColor = Arr(0, 0.0)
dBuf_1 = Arr(0, 0.0)
dBuf_2 = Arr(0, 0.0)
dBuf_I = Arr(0, 0.0)
ihMA_1 = 0
ihMA_2 = 0
P0 = 0
P2 = 0
P4 = 0

def OnInit():
    global P0, P2, P4, ihMA_1, ihMA_2
    SetIndexBuffer(0, dPlot, INDICATOR_DATA)
    SetIndexBuffer(1, dColor, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, dBuf_I, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, dBuf_1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, dBuf_2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(dPlot, True)
    ArraySetAsSeries(dColor, True)
    ArraySetAsSeries(dBuf_I, True)
    ArraySetAsSeries(dBuf_1, True)
    ArraySetAsSeries(dBuf_2, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() - 1)
    P0 = Per
    P2 = _idiv(Per, 2)
    P4 = _int(MathSqrt(Per))
    ihMA_1 = iMA(Symbol(), Period(), P0, 0, MODE_EMA, PRICE_CLOSE)
    ihMA_2 = iMA(Symbol(), Period(), P2, 0, MODE_EMA, PRICE_CLOSE)
    if ihMA_1 < 0 or ihMA_1 < 0:
        return -1
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    if BarsCalculated(ihMA_1) < rates_total:
        return 0
    if BarsCalculated(ihMA_2) < rates_total:
        return 0
    to_copy = MathMin(rates_total, rates_total - prev_calculated + 1)
    if prev_calculated < 0 or prev_calculated > rates_total:
        to_copy = rates_total
    if (10 * P0) > rates_total:
        return 0
    if to_copy > iMax:
        to_copy = iMax
    if to_copy > 0:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - (iMax - Per))
    if CopyBuffer(ihMA_1, 0, 0, to_copy, dBuf_1) != to_copy:
        return 0
    if CopyBuffer(ihMA_2, 0, 0, to_copy, dBuf_2) != to_copy:
        return 0
    for i in range(0, to_copy):
        dBuf_I[i] = (2.0 * dBuf_2[i]) - dBuf_1[i]
    LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, P4, dBuf_I, dPlot, _GlobRef(globals(), '_s_OnCalculate_sum_'))
    for i in range(0, to_copy):
        if dPlot[i] > dPlot[i + 1]:
            dColor[i] = 0.0
        else:
            dColor[i] = 1.0
    return rates_total

# ---- static local variables
_s_OnCalculate_sum_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Is7nTrend(_MQL5Indicator):
    name = 'is7n_trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Per': 20,  # Period
        'iMax': 200,  # Maximum number of bars to proceed
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

