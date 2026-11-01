"""Relative momentum index — converted from MQL5: MQL5 Indicators/Relative Momentum Index/Relative momentum index.mq5

Relative Momentum Index (RMI)
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [10.0, 30.0, 70.0, 90.0], 'description': ['Relative Momentum Index (RMI)'], 'name': 'Relative momentum index', 'source': 'MQL5 Indicators/Relative Momentum Index/Relative momentum index.mq5', 'folder': 'Relative Momentum Index', 'inputs': [{'mql': 'inpRmiPeriod', 'py': 'inpRmiPeriod', 'param': 'inpRmiPeriod', 'type': 'int', 'default': 14, 'label': 'Relative momentum index period', 'sinput': False}, {'mql': 'inpMomPeriod', 'py': 'inpMomPeriod', 'param': 'inpMomPeriod', 'type': 'int', 'default': 5, 'label': 'Momentum period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRmiPeriod = _input('inpRmiPeriod', 14)  # Relative momentum index period
inpMomPeriod = _input('inpMomPeriod', 5)  # Momentum period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
pbuffer = Arr(0, 0.0)
nbuffer = Arr(0, 0.0)
prices = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, pbuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, nbuffer, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Relative momentum index (' + _str(inpRmiPeriod) + ',' + _str(inpMomPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        sumn = 0.0
        sump = 0.0
        rel = 0.0
        if i < (inpRmiPeriod + inpMomPeriod):
            k = 0
            while k < inpRmiPeriod and (i - k - inpMomPeriod) >= 0:
                rel = prices[i - k] - prices[i - k - inpMomPeriod]
                if rel > 0:
                    sump += rel
                else:
                    sumn -= rel
                k += 1
            pbuffer[i] = sump / inpRmiPeriod
            nbuffer[i] = sumn / inpRmiPeriod
        else:
            rel = prices[i] - prices[i - inpMomPeriod]
            if rel > 0:
                sump = rel
            else:
                sumn = -rel
            pbuffer[i] = ((pbuffer[i - 1] * (inpRmiPeriod - 1)) + sump) / inpRmiPeriod
            nbuffer[i] = ((nbuffer[i - 1] * (inpRmiPeriod - 1)) + sumn) / inpRmiPeriod
        val[i] = (0 if ((nbuffer[i] + pbuffer[i]) == 0.0) else _fdiv(100.0 * pbuffer[i], pbuffer[i] + nbuffer[i]))
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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


class RelativeMomentumIndex(_MQL5Indicator):
    name = 'Relative momentum index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRmiPeriod': 14,  # Relative momentum index period
        'inpMomPeriod': 5,  # Momentum period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

