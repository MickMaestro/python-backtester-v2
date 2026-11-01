"""TRIX log — converted from MQL5: MQL5 Indicators/TRIX Log/TRIX log.mq5

Trix
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Trix'}, 'levels': [], 'description': ['Trix'], 'name': 'TRIX log', 'source': 'MQL5 Indicators/TRIX Log/TRIX log.mq5', 'folder': 'TRIX Log', 'inputs': [{'mql': 'inpTrixPeriod', 'py': 'inpTrixPeriod', 'param': 'inpTrixPeriod', 'type': 'int', 'default': 14, 'label': 'Trix period', 'sinput': False}, {'mql': 'inpTrixPrice', 'py': 'inpTrixPrice', 'param': 'inpTrixPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpTrixPeriod = _input('inpTrixPeriod', 14)  # Trix period
inpTrixPrice = _input('inpTrixPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workTrix = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TRIX log (' + _str(inpTrixPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(workTrix, 0) != rates_total:
        ArrayResize(workTrix, rates_total)
    alpha = _fdiv(2.0, 1.0 + inpTrixPeriod)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        price = MathLog(getPrice(inpTrixPrice, open, close, high, low, i, rates_total))
        workTrix[i][0] = ((workTrix[i - 1][0] + (alpha * (price - workTrix[i - 1][0]))) if (i > 0) else 0)
        workTrix[i][1] = ((workTrix[i - 1][1] + (alpha * (workTrix[i][0] - workTrix[i - 1][1]))) if (i > 0) else 0)
        workTrix[i][2] = ((workTrix[i - 1][2] + (alpha * (workTrix[i][1] - workTrix[i - 1][2]))) if (i > 0) else 0)
        val[i] = ((_fdiv(workTrix[i][2] - workTrix[i - 1][2], workTrix[i - 1][2]) if (workTrix[i - 1][2] != 0) else 0) if (i > 0) else 0)
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


class TRIXLog(_MQL5Indicator):
    name = 'TRIX log'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTrixPeriod': 14,  # Trix period
        'inpTrixPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

