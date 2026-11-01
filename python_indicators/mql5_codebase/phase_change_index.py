"""Phase change index — converted from MQL5: MQL5 Indicators/Phase Change Index/Phase change index.mq5

Phase change index
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [14474460, 14474460], 2: [11119017, 6333684, 16760576]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Phase change trend zone', 2: 'Phase change index'}, 'levels': [], 'description': ['Phase change index'], 'name': 'Phase change index', 'source': 'MQL5 Indicators/Phase Change Index/Phase change index.mq5', 'folder': 'Phase Change Index', 'inputs': [{'mql': 'inpLength', 'py': 'inpLength', 'param': 'inpLength', 'type': 'int', 'default': 30, 'label': 'Phase change index period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevelHigh', 'py': 'inpLevelHigh', 'param': 'inpLevelHigh', 'type': 'double', 'default': 80.0, 'label': 'Level high', 'sinput': False}, {'mql': 'inpLevelLow', 'py': 'inpLevelLow', 'param': 'inpLevelLow', 'type': 'double', 'default': 20.0, 'label': 'Level low', 'sinput': False}, {'mql': 'inpInverted', 'py': 'inpInverted', 'param': 'inpInverted', 'type': 'int', 'default': 1, 'label': 'Display type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enInverted
inv_regular = 0
inv_inverted = 1
_enum('enInverted', {0: 'inv_regular', 1: 'inv_inverted'})

# ---- inputs and global variables
inpLength = _input('inpLength', 30)  # Phase change index period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLevelHigh = _input('inpLevelHigh', 80.0)  # Level high
inpLevelLow = _input('inpLevelLow', 20.0)  # Level low
inpInverted = _input('inpInverted', inv_inverted)  # Display type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levup = Arr(0, 0.0)
levdn = Arr(0, 0.0)
prices = Arr(0, 0.0)
state = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, levup, INDICATOR_DATA)
    SetIndexBuffer(1, levdn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, state, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevelHigh)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpLevelLow)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Phase change index (' + _str(inpLength) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        momentum = ((prices[i] - prices[i - inpLength]) if (i >= inpLength) else 0)
        sumUpDi = 0.0
        sumDnDi = 0.0
        j = 1
        while (j < inpLength and (i - j) >= 0) and (i - inpLength) >= 0:
            gradient = prices[i - inpLength] + ((momentum * (inpLength - j)) / inpLength)
            deviation = prices[i - j] - gradient
            if deviation > 0:
                sumUpDi += deviation
            else:
                sumDnDi -= deviation
            j += 1
        val[i] = (_fdiv(100.0 * sumUpDi, sumUpDi + sumDnDi) if ((sumUpDi + sumDnDi) != 0) else 0)
        if inpInverted == inv_inverted:
            val[i] = 100 - val[i]
        levdn[i] = 50.0
        levup[i] = (100 if (val[i] > inpLevelHigh) else 0 if (val[i] < inpLevelLow) else 50)
        valc[i] = (2 if (val[i] > inpLevelHigh) else 1 if (val[i] < inpLevelLow) else 0)
        i += 1
    return i

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PhaseChangeIndex(_MQL5Indicator):
    name = 'Phase change index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpLength': 30,  # Phase change index period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLevelHigh': 80.0,  # Level high
        'inpLevelLow': 20.0,  # Level low
        'inpInverted': _Choice({0: 'Display regular value', 1: 'Display inverted value'}, default=1),  # Display type
    }

