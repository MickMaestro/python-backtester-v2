"""Double smoothed EMA (fl) — converted from MQL5: MQL5 Indicators/Double smoothed EMA - floating levels/Double smoothed EMA (fl).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [15132390], 2: [8421504], 3: [11119017, 3329330, 9639167]}, 'widths': {3: 2}, 'styles': {2: 2}, 'labels': {1: 'Zone', 2: 'Middle', 3: 'Double smoothed EMA'}, 'levels': [], 'description': [], 'name': 'Double smoothed EMA (fl)', 'source': 'MQL5 Indicators/Double smoothed EMA - floating levels/Double smoothed EMA (fl).mq5', 'folder': 'Double smoothed EMA - floating levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 14.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Period for finding floating levels', 'sinput': False}, {'mql': 'inpFlUp', 'py': 'inpFlUp', 'param': 'inpFlUp', 'type': 'double', 'default': 90.0, 'label': 'Upper level %', 'sinput': False}, {'mql': 'inpFlDown', 'py': 'inpFlDown', 'param': 'inpFlDown', 'type': 'double', 'default': 10.0, 'label': 'Lower level %', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum chgColor
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
_enum('chgColor', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14.0)  # Period
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
inpFlPeriod = _input('inpFlPeriod', 25)  # Period for finding floating levels
inpFlUp = _input('inpFlUp', 90.0)  # Upper level %
inpFlDown = _input('inpFlDown', 10.0)  # Lower level %
inpColorOn = _input('inpColorOn', chg_onLevel)  # Color change on :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
work = Arr(0, 0.0)
mid = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
_alpha = 0.0

def OnInit():
    global _alpha
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, mid, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, work, INDICATOR_CALCULATIONS)
    _alpha = _fdiv(2.0, 1.0 + MathSqrt(MathMax(inpPeriod, 1)))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Double smoothed EMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        price = getPrice(inpPrice, open, close, high, low, i)
        work[i] = ((work[i - 1] + (_alpha * (price - work[i - 1]))) if (i > 0) else price)
        val[i] = ((val[i - 1] + (_alpha * (work[i] - val[i - 1]))) if (i > 0) else work[i])
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpFlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = val[ArrayMaximum(val, start, inpFlPeriod - 1)]
            _s_OnCalculate_prev_min = val[ArrayMinimum(val, start, inpFlPeriod - 1)]
        max_ = (val[i] if (val[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (val[i] if (val[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        range_ = (max_ - min_) / 100.0
        fup[i] = min_ + (inpFlUp * range_)
        fdn[i] = min_ + (inpFlDown * range_)
        mid[i] = min_ + (50.0 * range_)
        _sw1 = inpColorOn
        if _sw1 == chg_onLevel:
            valc[i] = (1 if (val[i] > fup[i]) else 2 if (val[i] < fdn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        elif _sw1 == chg_onMiddle:
            valc[i] = (1 if (val[i] > mid[i]) else 2 if (val[i] < mid[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def getPrice(tprice, open, close, high, low, i):
    _sw2 = tprice
    if _sw2 == PRICE_CLOSE:
        return close[i]
    elif _sw2 == PRICE_OPEN:
        return open[i]
    elif _sw2 == PRICE_HIGH:
        return high[i]
    elif _sw2 == PRICE_LOW:
        return low[i]
    elif _sw2 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DoubleSmoothedEMAFl(_MQL5Indicator):
    name = 'Double smoothed EMA (fl)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14.0,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
        'inpFlPeriod': 25,  # Period for finding floating levels
        'inpFlUp': 90.0,  # Upper level %
        'inpFlDown': 10.0,  # Lower level %
        'inpColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=1),  # Color change on :
    }

