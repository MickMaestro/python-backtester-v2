"""Correlation trend indicator (opt) — converted from MQL5: MQL5 Indicators/Correlation trend indicator/Correlation trend indicator (opt).mq5

Copyright: copyright© mladen 2020; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'copyright© mladen 2020', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Short', 2: 'Long'}, 'levels': [], 'description': [], 'name': 'Correlation trend indicator (opt)', 'source': 'MQL5 Indicators/Correlation trend indicator/Correlation trend indicator (opt).mq5', 'folder': 'Correlation trend indicator', 'inputs': [{'mql': 'inpPeriodShort', 'py': 'inpPeriodShort', 'param': 'inpPeriodShort', 'type': 'int', 'default': 20, 'label': 'Short period', 'sinput': False}, {'mql': 'inpPeriodLong', 'py': 'inpPeriodLong', 'param': 'inpPeriodLong', 'type': 'int', 'default': 40, 'label': 'Long period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriodShort = _input('inpPeriodShort', 20)  # Short period
inpPeriodLong = _input('inpPeriodLong', 40)  # Long period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
vals = Arr(0, 0.0)
vall = Arr(0, 0.0)
_longPeriod = 0
_shortPeriod = 0
SSyy = 0.0
SSy = 0.0
LSyy = 0.0
LSy = 0.0
_ts2 = 0.0
_tl2 = 0.0

class sWorkStruc(MqlObject):
    _q_fields = ('price', 'sums')
    def __init__(self, *args):
        self.price = 0.0
        self.sums = Arr(2, 0, dyn=False, factory=sCalcStruct)

class sCalcStruct(MqlObject):
    _q_fields = ('Sx', 'Sxx', 'Sxy')
    def __init__(self, *args):
        self.Sx = 0.0
        self.Sxx = 0.0
        self.Sxy = 0.0

def OnInit():
    global LSy, LSyy, SSy, SSyy, _longPeriod, _shortPeriod, _tl2, _ts2
    SetIndexBuffer(0, vals, INDICATOR_DATA)
    SetIndexBuffer(1, vall, INDICATOR_DATA)
    _longPeriod = MathMax(inpPeriodShort, inpPeriodLong)
    _shortPeriod = MathMin(inpPeriodShort, inpPeriodLong)
    k = 0
    y = 0
    while k < _longPeriod:
        if k < _shortPeriod:
            SSy += y
            SSyy += y * y
        LSy += y
        LSyy += y * y
        k += 1
        y -= 1
    _ts2 = (_shortPeriod * SSyy) - (SSy * SSy)
    _tl2 = (_longPeriod * LSyy) - (LSy * LSy)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Correlation trend (%i,%i)', _shortPeriod, _longPeriod))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        _s_OnCalculate_m_work[i].price = getPrice(inpPrice, open, high, low, close, i)
        if i > _shortPeriod:
            _s_OnCalculate_m_work[i].sums[0].Sx = _s_OnCalculate_m_work[i - 1].sums[0].Sx + _s_OnCalculate_m_work[i].price - _s_OnCalculate_m_work[i - _shortPeriod].price
            _s_OnCalculate_m_work[i].sums[0].Sxx = _s_OnCalculate_m_work[i - 1].sums[0].Sxx + (_s_OnCalculate_m_work[i].price * _s_OnCalculate_m_work[i].price) - (_s_OnCalculate_m_work[i - _shortPeriod].price * _s_OnCalculate_m_work[i - _shortPeriod].price)
            _s_OnCalculate_m_work[i].sums[0].Sxy = _s_OnCalculate_m_work[i - 1].sums[0].Sxy - _s_OnCalculate_m_work[i].sums[0].Sx + _s_OnCalculate_m_work[i].price + ((_shortPeriod - 1) * _s_OnCalculate_m_work[i - _shortPeriod].price)
        else:
            _s_OnCalculate_m_work[i].sums[0].Sx = _s_OnCalculate_m_work[i].price
            _s_OnCalculate_m_work[i].sums[0].Sxx = _s_OnCalculate_m_work[i].price * _s_OnCalculate_m_work[i].price
            _s_OnCalculate_m_work[i].sums[0].Sxy = 0.0
            k = 1
            y = -1
            while k < _shortPeriod and i >= k:
                _s_OnCalculate_m_work[i].sums[0].Sx += _s_OnCalculate_m_work[i - k].price
                _s_OnCalculate_m_work[i].sums[0].Sxx += _s_OnCalculate_m_work[i - k].price * _s_OnCalculate_m_work[i - k].price
                _s_OnCalculate_m_work[i].sums[0].Sxy += _s_OnCalculate_m_work[i - k].price * y
                k += 1
                y -= 1
        if i > _longPeriod:
            _s_OnCalculate_m_work[i].sums[1].Sx = _s_OnCalculate_m_work[i - 1].sums[1].Sx + _s_OnCalculate_m_work[i].price - _s_OnCalculate_m_work[i - _longPeriod].price
            _s_OnCalculate_m_work[i].sums[1].Sxx = _s_OnCalculate_m_work[i - 1].sums[1].Sxx + (_s_OnCalculate_m_work[i].price * _s_OnCalculate_m_work[i].price) - (_s_OnCalculate_m_work[i - _longPeriod].price * _s_OnCalculate_m_work[i - _longPeriod].price)
            _s_OnCalculate_m_work[i].sums[1].Sxy = _s_OnCalculate_m_work[i - 1].sums[1].Sxy - _s_OnCalculate_m_work[i].sums[1].Sx + _s_OnCalculate_m_work[i].price + ((_longPeriod - 1) * _s_OnCalculate_m_work[i - _longPeriod].price)
        else:
            _s_OnCalculate_m_work[i].sums[1].Sx = _s_OnCalculate_m_work[i].price
            _s_OnCalculate_m_work[i].sums[1].Sxx = _s_OnCalculate_m_work[i].price * _s_OnCalculate_m_work[i].price
            _s_OnCalculate_m_work[i].sums[1].Sxy = 0.0
            k = 1
            y = -1
            while k < _longPeriod and i >= k:
                _s_OnCalculate_m_work[i].sums[1].Sx += _s_OnCalculate_m_work[i - k].price
                _s_OnCalculate_m_work[i].sums[1].Sxx += _s_OnCalculate_m_work[i - k].price * _s_OnCalculate_m_work[i - k].price
                _s_OnCalculate_m_work[i].sums[1].Sxy += _s_OnCalculate_m_work[i - k].price * y
                k += 1
                y -= 1
        _ts1 = (_shortPeriod * _s_OnCalculate_m_work[i].sums[0].Sxx) - (_s_OnCalculate_m_work[i].sums[0].Sx * _s_OnCalculate_m_work[i].sums[0].Sx)
        _tl1 = (_longPeriod * _s_OnCalculate_m_work[i].sums[1].Sxx) - (_s_OnCalculate_m_work[i].sums[1].Sx * _s_OnCalculate_m_work[i].sums[1].Sx)
        vals[i] = (_fdiv((_shortPeriod * _s_OnCalculate_m_work[i].sums[0].Sxy) - (_s_OnCalculate_m_work[i].sums[0].Sx * SSy), MathSqrt(_ts1 * _ts2)) if (_ts1 > 0 and _ts2 > 0) else 0)
        vall[i] = (_fdiv((_longPeriod * _s_OnCalculate_m_work[i].sums[1].Sxy) - (_s_OnCalculate_m_work[i].sums[1].Sx * LSy), MathSqrt(_tl1 * _tl2)) if (_tl1 > 0 and _tl2 > 0) else 0)
    return rates_total

def getPrice(price, open, high, low, close, i):
    _sw1 = price
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruc)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrelationTrendIndicatorOpt(_MQL5Indicator):
    name = 'Correlation trend indicator (opt)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriodShort': 20,  # Short period
        'inpPeriodLong': 40,  # Long period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

