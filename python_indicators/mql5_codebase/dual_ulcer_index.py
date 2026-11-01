"""Dual Ulcer index — converted from MQL5: MQL5 Indicators/Dual Ulcer index/Dual Ulcer index.mq5

Dual ulcer index
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [11119017], 2: [11119017], 3: [11119017, 16748574, 6333684]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'Index up', 2: 'Index down', 3: 'Ulcer index'}, 'levels': [], 'description': ['Dual ulcer index'], 'name': 'Dual Ulcer index', 'source': 'MQL5 Indicators/Dual Ulcer index/Dual Ulcer index.mq5', 'folder': 'Dual Ulcer index', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Ulcer index period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpType', 'py': 'inpType', 'param': 'inpType', 'type': 'int', 'default': 0, 'label': 'Calculation mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enCalcType
uind_regular = 0
uind_inverted = 1
_enum('enCalcType', {0: 'uind_regular', 1: 'uind_inverted'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Ulcer index period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpType = _input('inpType', uind_regular)  # Calculation mode
uindu = Arr(0, 0.0)
uindd = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, uindu, INDICATOR_DATA)
    SetIndexBuffer(1, uindd, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dual' + (' inverted' if (inpType == uind_inverted) else '') + ' ulcer index (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        if i < inpPeriod:
            uindd[i] = EMPTY_VALUE
            uindu[i] = uindd[i]
            val[i] = uindu[i]
            valc[i] = 0.0
            i += 1
            continue
        sumsqd = 0.0
        sumsqu = 0.0
        if inpType == uind_regular:
            max_ = prices[i - inpPeriod + 1]
            min_ = prices[i - inpPeriod + 1]
            for k in range(inpPeriod - 2, 0 - 1, -1):
                if prices[i - k] > max_:
                    max_ = prices[i - k]
                else:
                    sumsqd += MathPow(100.0 * _fdiv(max_ - prices[i - k], max_), 2)
                if prices[i - k] < min_:
                    min_ = prices[i - k]
                else:
                    sumsqu += MathPow(100.0 * _fdiv(prices[i - k] - min_, min_), 2)
        else:
            max_ = prices[i]
            min_ = prices[i]
            for k in range(1, inpPeriod):
                if prices[i - k] > max_:
                    max_ = prices[i - k]
                else:
                    sumsqu += MathPow(100.0 * _fdiv(max_ - prices[i - k], max_), 2)
                if prices[i - k] < min_:
                    min_ = prices[i - k]
                else:
                    sumsqd += MathPow(100.0 * _fdiv(prices[i - k] - min_, min_), 2)
        uindu[i] = MathSqrt(sumsqu / inpPeriod)
        uindd[i] = MathSqrt(sumsqd / inpPeriod)
        valc[i] = (1 if (uindu[i] > uindd[i]) else 2 if (uindu[i] < uindd[i]) else valc[i])
        val[i] = (uindu[i] if (valc[i] == 1) else uindd[i])
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


class DualUlcerIndex(_MQL5Indicator):
    name = 'Dual Ulcer index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # Ulcer index period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpType': _Choice({0: 'Regular ulcer index calculation', 1: 'Inverted ulcer index calculation'}, default=0),  # Calculation mode
    }

