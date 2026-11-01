"""frama — converted from MQL5: MQL5 Indicators/Fractal Adaptive Moving Average (FrAMA)/frama.mq5

Fractal Adaptive Moving Average
Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9109504]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'FrAMA'}, 'levels': [], 'description': ['Fractal Adaptive Moving Average'], 'name': 'frama', 'source': 'MQL5 Indicators/Fractal Adaptive Moving Average (FrAMA)/frama.mq5', 'folder': 'Fractal Adaptive Moving Average (FrAMA)', 'inputs': [{'mql': 'InpPeriodFrAMA', 'py': 'InpPeriodFrAMA', 'param': 'InpPeriodFrAMA', 'type': 'int', 'default': 14, 'label': 'FrAMA period', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 0, 'label': "Indicator's shift", 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFrAMA = _input('InpPeriodFrAMA', 14)  # FrAMA period
InpShift = _input('InpShift', 0)  # Indicator's shift
FrAmaBuffer = Arr(0, 0.0)
High = Arr(0, 0.0)
Low = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, FrAmaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, High, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, Low, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (2 * InpPeriodFrAMA) - 1)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FrAMA(' + _str(InpPeriodFrAMA) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'FrAMA(' + _str(InpPeriodFrAMA) + ')')

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (2 * InpPeriodFrAMA):
        return 0
    limit = 0
    copied = 0
    Hi1 = 0.0
    Hi2 = 0.0
    Hi3 = 0.0
    Lo1 = 0.0
    Lo2 = 0.0
    Lo3 = 0.0
    N1 = 0.0
    N2 = 0.0
    N3 = 0.0
    D = 0.0
    ALFA = 0.0
    if False:
        return 0
    copied = CopyHigh(Symbol(), Period(), 0, rates_total, High)
    if copied != rates_total:
        Print("Can't load High prices.")
        return 0
    if False:
        return 0
    copied = CopyLow(Symbol(), Period(), 0, rates_total, Low)
    if copied != rates_total:
        Print("Can't load Low prices.")
        return 0
    if prev_calculated == 0:
        limit = (2 * InpPeriodFrAMA) - 1
        for i in range(0, limit + 1):
            FrAmaBuffer[i] = price[i]
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        Hi1 = iHighest_u(i, InpPeriodFrAMA)
        Lo1 = iLowest_u(i, InpPeriodFrAMA)
        Hi2 = iHighest_u(i - InpPeriodFrAMA, InpPeriodFrAMA)
        Lo2 = iLowest_u(i - InpPeriodFrAMA, InpPeriodFrAMA)
        Hi3 = iHighest_u(i, 2 * InpPeriodFrAMA)
        Lo3 = iLowest_u(i, 2 * InpPeriodFrAMA)
        N1 = (Hi1 - Lo1) / InpPeriodFrAMA
        N2 = (Hi2 - Lo2) / InpPeriodFrAMA
        N3 = (Hi3 - Lo3) / (2 * InpPeriodFrAMA)
        D = _fdiv(log(N1 + N2) - log(N3), log(2.0))
        ALFA = exp(-4.6 * (D - 1.0))
        FrAmaBuffer[i] = (ALFA * price[i]) + ((1 - ALFA) * FrAmaBuffer[i - 1])
    return rates_total

def iHighest_u(StartPos, Depth):
    res = 0.0
    if (StartPos < 0 or (StartPos - Depth + 1) < 0) or Depth < 0:
        Print('Invalid parameter in function', 'iHighest', ': StartPos =', StartPos, ', Depth = ', Depth)
        return 0.0
    res = High[StartPos]
    for i in range(StartPos - Depth + 1, StartPos):
        if High[i] > res:
            res = High[i]
    return res

def iLowest_u(StartPos, Depth):
    res = 0.0
    if (StartPos < 0 or (StartPos - Depth + 1) < 0) or Depth < 0:
        Print('Invalid parameter in function', 'iLowest', ': StartPos =', StartPos, ', Depth = ', Depth)
        return 0.0
    res = Low[StartPos]
    for i in range(StartPos - Depth + 1, StartPos):
        if Low[i] < res:
            res = Low[i]
    return res


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Frama(_MQL5Indicator):
    name = 'frama'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFrAMA': 14,  # FrAMA period
        'InpShift': 0,  # Indicator's shift
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

