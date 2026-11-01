"""Volatility adjusted RSI — converted from MQL5: MQL5 Indicators/Volatility adjusted RSI/Volatility adjusted RSI.mq5

RSI
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 32768]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Rsi'}, 'levels': [], 'description': ['RSI'], 'name': 'Volatility adjusted RSI', 'source': 'MQL5 Indicators/Volatility adjusted RSI/Volatility adjusted RSI.mq5', 'folder': 'Volatility adjusted RSI', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpVolPeriod', 'py': 'inpVolPeriod', 'param': 'inpVolPeriod', 'type': 'int', 'default': 0, 'label': 'Volatilty period (<=0 for same as RSI period)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # RSI period
inpVolPeriod = _input('inpVolPeriod', 0)  # Volatilty period (<=0 for same as RSI period)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ª_volPeriod = 0
_workRsi = Arr(0, 0.0, dims=(3,))
_volArray = Arr(0, 0.0, dims=(4,))

def OnInit():
    global ª_volPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    ª_volPeriod = (inpVolPeriod if (inpVolPeriod > 1) else inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility adjusted RSI (' + _str(inpPeriod) + ',' + _str(ª_volPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
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
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        val[i] = iRsi(_price, _fdiv(float(inpPeriod), iVolatility(_price, ª_volPeriod, i, rates_total)), i, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iRsi(price, period, i, bars, _inst=0):
    global _s_iRsi__arrayError, _s_iRsi__arrayResizedTo
    if _s_iRsi__arrayResizedTo < bars:
        _res = bars + 500
        _res -= ArrayResize(_workRsi, _res)
        if _res:
            _s_iRsi__arrayError = True
        else:
            _s_iRsi__arrayResizedTo = bars + 500
    if _s_iRsi__arrayError:
        return 0.0
    _workRsi[i][_inst + 2] = price
    if i < period:
        sum_ = 0.0
        change = 0.0
        for k in range(0, i):
            change = _workRsi[i - k][_inst + 2] - _workRsi[i - k - 1][_inst + 2]
            sum_ += (change if (change > 0) else (-change))
        _workRsi[i][_inst + 1] = _fdiv(_workRsi[i][_inst + 2] - _workRsi[0][_inst + 2], i + 1.0)
        _workRsi[i][_inst] = _fdiv(sum_, i + 1.0)
    else:
        alpha = _fdiv(1.0, period)
        change = _workRsi[i][_inst + 2] - _workRsi[i - 1][_inst + 2]
        changa = (change if (change > 0) else (-change))
        _workRsi[i][_inst + 1] = _workRsi[i - 1][_inst + 1] + (alpha * (change - _workRsi[i - 1][_inst + 1]))
        _workRsi[i][_inst] = _workRsi[i - 1][_inst] + (alpha * (changa - _workRsi[i - 1][_inst]))
    return ((50.0 * (_fdiv(_workRsi[i][_inst + 1], _workRsi[i][_inst]) + 1.0)) if (_workRsi[i][_inst] > 0) else 50.0)

def iVolatility(price, period, i, _bars, instance=0):
    global _s_iVolatility__arrayError, _s_iVolatility__arrayResizedTo
    if _s_iVolatility__arrayResizedTo < _bars:
        _res = _bars + 500
        _res -= ArrayResize(_volArray, _res)
        if _res:
            _s_iVolatility__arrayError = True
        else:
            _s_iVolatility__arrayResizedTo = _bars + 500
    if _s_iVolatility__arrayError:
        return 1.0
    _volArray[i][instance] = price
    diff = ((_volArray[i][instance] - _volArray[i - 1][instance]) if (i > 0) else 0)
    _volArray[i][instance + 1] = (diff if (diff > 0) else (-diff))
    if i <= period:
        _volArray[i][instance + 2] = _volArray[i][instance + 1]
        k = 1
        while k < period and i >= k:
            _volArray[i][instance + 2] += _volArray[i - k][instance + 1]
            k += 1
        _volArray[i][instance + 3] = _volArray[i][instance + 2]
        k = 1
        while k < period and i >= k:
            _volArray[i][instance + 3] += _volArray[i - k][instance + 2]
            k += 1
    else:
        _volArray[i][instance + 2] = _volArray[i - 1][instance + 2] - _volArray[i - period][instance + 1] + _volArray[i][instance + 1]
        _volArray[i][instance + 3] = _volArray[i - 1][instance + 3] - _volArray[i - period][instance + 2] + _volArray[i][instance + 2]
    return (_fdiv(float(period) * _volArray[i][instance + 2], _volArray[i][instance + 3]) if (_volArray[i][instance + 3] != 0 and _volArray[i][instance + 2] != 0) else 1)

# ---- static local variables
_s_iRsi__arrayError = False
_s_iRsi__arrayResizedTo = 0
_s_iVolatility__arrayError = False
_s_iVolatility__arrayResizedTo = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityAdjustedRSI(_MQL5Indicator):
    name = 'Volatility adjusted RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # RSI period
        'inpVolPeriod': 0,  # Volatilty period (<=0 for same as RSI period)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

