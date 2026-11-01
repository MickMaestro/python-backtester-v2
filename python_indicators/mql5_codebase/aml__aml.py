"""AML — converted from MQL5: MQL5 Indicators/AML/AML.mq5

Adaptive Market Level indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [14772545, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'AML'}, 'levels': [], 'description': ['Adaptive Market Level indicator'], 'name': 'AML', 'source': 'MQL5 Indicators/AML/AML.mq5', 'folder': 'AML', 'inputs': [{'mql': 'InpFractal', 'py': 'InpFractal', 'param': 'InpFractal', 'type': 'uint', 'default': 6, 'label': 'Period', 'sinput': False}, {'mql': 'InpLag', 'py': 'InpLag', 'param': 'InpLag', 'type': 'uint', 'default': 7, 'label': 'Dimension', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFractal = _input('InpFractal', 6)  # Period
InpLag = _input('InpLag', 7)  # Dimension
BufferAML = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferFR = Arr(0, 0.0)
period_max = 0
fractal = 0
lag = 0
lag2 = 0.0

def OnInit():
    global fractal, lag, lag2, period_max
    if Point() == 0:
        Print('Error! Point() value is zero.')
        return INIT_FAILED
    fractal = (1 if (InpFractal < 1) else InpFractal)
    lag = (1 if (InpLag < 1) else InpLag)
    period_max = fmax(fractal, lag)
    lag2 = lag * lag * Point()
    SetIndexBuffer(0, BufferAML, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferFR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adaptive Market Level (' + _str(fractal) + ',' + _str(lag) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferAML, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferFR, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferAML, EMPTY_VALUE)
        ArrayInitialize(BufferFR, 0)
    for i in range(limit, 0 - 1, -1):
        R = Range(fractal, i, high, low)
        if R == EMPTY_VALUE:
            continue
        R1 = _fdiv(R, fractal)
        R = Range(fractal, i + fractal, high, low)
        if R == EMPTY_VALUE:
            continue
        R2 = _fdiv(R, fractal)
        R = Range(2 * fractal, i, high, low)
        if R == EMPTY_VALUE:
            continue
        R3 = _fdiv(R, 2.0 * fractal)
        dim = ((1.44269504088896 * (log(R1 + R2) - log(R3))) if ((R1 + R2) > 0 and R3 > 0) else 0)
        alpha = exp(-1.0 * lag * (dim - 1.0))
        alpha = fmin(alpha, 1.0)
        alpha = fmax(alpha, 0.01)
        price = (high[i] + low[i] + (2.0 * open[i]) + (2.0 * close[i])) / 6.0
        BufferFR[i] = (alpha * price) + ((1.0 - alpha) * BufferFR[i + 1])
        BufferAML[i] = (BufferAML[i + 1] if (fabs(BufferFR[i] - BufferFR[i + lag]) < lag2) else BufferFR[i])
        BufferColors[i] = (1 if (BufferAML[i] > BufferAML[i + 1]) else 2 if (BufferAML[i] < BufferAML[i + 1]) else 0)
    return rates_total

def Range(count, index, high, low):
    bl = Lowest(count, index)
    bh = Highest(count, index)
    if bl == WRONG_VALUE or bh == WRONG_VALUE:
        return EMPTY_VALUE
    return high[bh] - low[bl]

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AML(_MQL5Indicator):
    name = 'AML'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFractal': 6,  # Period
        'InpLag': 7,  # Dimension
    }

