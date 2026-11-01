"""RSI adaptive ds EMA — converted from MQL5: MQL5 Indicators/RSI adaptive double smoothed EMA/RSI adaptive ds EMA.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 3937500, 2263842]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'RSI adaptive DS EMA'}, 'levels': [], 'description': [], 'name': 'RSI adaptive ds EMA', 'source': 'MQL5 Indicators/RSI adaptive double smoothed EMA/RSI adaptive ds EMA.mq5', 'folder': 'RSI adaptive double smoothed EMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 32.0, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32.0)  # RSI period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valw = Arr(0, 0.0)

class sRsiStruct(MqlObject):
    _q_fields = ('price', 'change', 'changa')
    def __init__(self, *args):
        self.price = 0.0
        self.change = 0.0
        self.changa = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valw, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI adaptive ds EMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i)
        _alpha = (iRsi(_price, inpPeriod, i, rates_total) - 0.5) * 2.0
        if _alpha < 0:
            _alpha *= -1.0
        _alpha = MathSqrt(_alpha)
        if i > 0:
            valw[i] = valw[i - 1] + (_alpha * (_price - valw[i - 1]))
            val[i] = val[i - 1] + (_alpha * (valw[i] - val[i - 1]))
            valc[i] = (2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1])
        else:
            valw[i] = _price
            val[i] = valw[i]
            valc[i] = 0.0
        i += 1
    return i

def iRsi(price, period, i, bars, _instanceNo=0):
    global _s_iRsi_m_arraySize
    if _s_iRsi_m_arraySize < bars:
        _s_iRsi_m_arraySize = ArrayResize(_s_iRsi_m_array, bars + 500)
        if _s_iRsi_m_arraySize < bars:
            return 0.0
    alpha = _fdiv(1.0, period)
    _s_iRsi_m_array[i][_instanceNo].price = price
    if i < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and i > k:
            sum_ += MathAbs(_s_iRsi_m_array[i - k][_instanceNo].price - _s_iRsi_m_array[i - k - 1][_instanceNo].price)
            k += 1
        _s_iRsi_m_array[i][_instanceNo].change = _fdiv(_s_iRsi_m_array[i][_instanceNo].price - _s_iRsi_m_array[0][_instanceNo].price, MathMax(k, 1))
        _s_iRsi_m_array[i][_instanceNo].changa = _fdiv(sum_, MathMax(k, 1))
    else:
        change = _s_iRsi_m_array[i][_instanceNo].price - _s_iRsi_m_array[i - 1][_instanceNo].price
        _s_iRsi_m_array[i][_instanceNo].change = _s_iRsi_m_array[i - 1][_instanceNo].change + (alpha * (change - _s_iRsi_m_array[i - 1][_instanceNo].change))
        if change > 0:
            _s_iRsi_m_array[i][_instanceNo].changa = _s_iRsi_m_array[i - 1][_instanceNo].changa + (alpha * (change - _s_iRsi_m_array[i - 1][_instanceNo].changa))
        else:
            _s_iRsi_m_array[i][_instanceNo].changa = _s_iRsi_m_array[i - 1][_instanceNo].changa + (alpha * ((-change) - _s_iRsi_m_array[i - 1][_instanceNo].changa))
    if _s_iRsi_m_array[i][_instanceNo].changa != 0:
        return 0.5 * (_fdiv(_s_iRsi_m_array[i][_instanceNo].change, _s_iRsi_m_array[i][_instanceNo].changa) + 1.0)
    else:
        return 0.0

def getPrice(tprice, open, close, high, low, i):
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

# ---- static local variables
_s_iRsi_m_array = Arr(0, 0, factory=sRsiStruct, dims=(2,))
_s_iRsi_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIAdaptiveDsEMA(_MQL5Indicator):
    name = 'RSI adaptive ds EMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32.0,  # RSI period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

