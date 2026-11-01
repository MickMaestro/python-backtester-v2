"""Root Mean Square — converted from MQL5: MQL5 Indicators/Root Mean Square/Root Mean Square.mq5

Copyright: © mladen, 2024; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2024', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 3329330, 36095]}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'pdfma'}, 'levels': [], 'description': [], 'name': 'Root Mean Square', 'source': 'MQL5 Indicators/Root Mean Square/Root Mean Square.mq5', 'folder': 'Root Mean Square', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 25, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 25)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valColor = Arr(0, 0.0)

class sWorkStruct(MqlObject):
    _q_fields = ('valueXvalue', 'valueXvalueSum')
    def __init__(self, *args):
        self.valueXvalue = 0.0
        self.valueXvalueSum = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valColor, INDICATOR_COLOR_INDEX)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(limit, rates_total):
        val[i] = iRootMeanSquare(iGetPrice(inpPrice, open[i], high[i], low[i], close[i]), inpPeriod, i, rates_total)
        valColor[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valColor[i - 1]) if (i > 0) else 0)
    return rates_total

def iRootMeanSquare(value, period, r, bars, instanceNo=0):
    global _s_iRootMeanSquare_m_workSize
    if _s_iRootMeanSquare_m_workSize <= bars:
        _s_iRootMeanSquare_m_workSize = ArrayResize(_s_iRootMeanSquare_m_work, bars + 500, 2000)
    if period < 1:
        period = 1
    _s_iRootMeanSquare_m_work[r].valueXvalue = value * value
    if r >= period:
        _s_iRootMeanSquare_m_work[r].valueXvalueSum = _s_iRootMeanSquare_m_work[r - 1].valueXvalueSum + _s_iRootMeanSquare_m_work[r].valueXvalue - _s_iRootMeanSquare_m_work[r - period].valueXvalue
    else:
        _s_iRootMeanSquare_m_work[r].valueXvalueSum = _s_iRootMeanSquare_m_work[r].valueXvalue
        k = 1
        while k < period and r >= k:
            _s_iRootMeanSquare_m_work[r].valueXvalueSum += _s_iRootMeanSquare_m_work[r - k].valueXvalue
            k += 1
    return MathSqrt(_fdiv(_s_iRootMeanSquare_m_work[r].valueXvalueSum, float(period)))

def iGetPrice(tprice, open, high, low, close):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close
    elif _sw1 == PRICE_OPEN:
        return open
    elif _sw1 == PRICE_HIGH:
        return high
    elif _sw1 == PRICE_LOW:
        return low
    elif _sw1 == PRICE_MEDIAN:
        return (high + low) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high + low + close) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high + low + close + close) / 4.0
    return 0.0

# ---- static local variables
_s_iRootMeanSquare_m_work = Arr(0, 0, factory=sWorkStruct)
_s_iRootMeanSquare_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RootMeanSquare(_MQL5Indicator):
    name = 'Root Mean Square'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 25,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

