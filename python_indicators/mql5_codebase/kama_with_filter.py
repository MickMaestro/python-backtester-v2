"""KAMA with filter — converted from MQL5: MQL5 Indicators/Kaufman AMA with filter/KAMA with filter.mq5

KAMA with filter
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'KAMA with filter'}, 'levels': [], 'description': ['KAMA with filter'], 'name': 'KAMA with filter', 'source': 'MQL5 Indicators/Kaufman AMA with filter/KAMA with filter.mq5', 'folder': 'Kaufman AMA with filter', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 2, 'label': 'Fast end period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 30, 'label': 'Slow end period', 'sinput': False}, {'mql': 'inpPower', 'py': 'inpPower', 'param': 'inpPower', 'type': 'double', 'default': 2.0, 'label': 'Smooth power', 'sinput': False}, {'mql': 'inpFilter', 'py': 'inpFilter', 'param': 'inpFilter', 'type': 'int', 'default': 50, 'label': 'Filter', 'sinput': False}, {'mql': 'inpFilterPeriod', 'py': 'inpFilterPeriod', 'param': 'inpFilterPeriod', 'type': 'int', 'default': 4, 'label': 'Filter period', 'sinput': False}, {'mql': 'inpFilterDifference', 'py': 'inpFilterDifference', 'param': 'inpFilterDifference', 'type': 'double', 'default': 50.0, 'label': 'Filter difference', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpFastPeriod = _input('inpFastPeriod', 2)  # Fast end period
inpSlowPeriod = _input('inpSlowPeriod', 30)  # Slow end period
inpPower = _input('inpPower', 2.0)  # Smooth power
inpFilter = _input('inpFilter', 50)  # Filter
inpFilterPeriod = _input('inpFilterPeriod', 4)  # Filter period
inpFilterDifference = _input('inpFilterDifference', 50.0)  # Filter difference
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ama = Arr(0, 0.0)
workAma = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ama, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KAMA with filter (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        ama[i] = iKama(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, inpFastPeriod, inpSlowPeriod, inpPower, i, open, close, high, low, rates_total)
        val[i] = ama[i]
        if inpFilter > 0:
            sAmaDiff = 0.0
            k = 0
            while k < inpSlowPeriod and (i - k - 1) >= 0:
                sAmaDiff += MathAbs(ama[i - k] - ama[i - k - 1])
                k += 1
            cAmaDiff = ((ama[i] - ama[i - 1]) if (i > 0) else 0)
            aAmaDiff = MathAbs(cAmaDiff)
            filterValue = NormalizeDouble(_fdiv(inpFilter * sAmaDiff, 100.0 * inpSlowPeriod), Digits())
            _start = MathMax(i - inpFilterPeriod, 0)
            if cAmaDiff > 0:
                if cAmaDiff < filterValue and high[i] <= (high[ArrayMaximum(high, _start, inpFilterPeriod)] + (inpFilterDifference * Point())):
                    val[i] = (val[i - 1] if (i > 0) else ama[i])
            if cAmaDiff < 0:
                if aAmaDiff < filterValue and low[i] >= (low[ArrayMinimum(low, _start, inpFilterPeriod)] - (inpFilterDifference * Point())):
                    val[i] = (val[i - 1] if (i > 0) else ama[i])
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iKama(price, period, fast, slow, power, i, open, close, high, low, bars, instanceNo=0):
    if ArrayRange(workAma, 0) != bars:
        ArrayResize(workAma, bars)
    r = i
    instanceNo *= 3
    fastend = _fdiv(2.0, fast + 1)
    slowend = _fdiv(2.0, slow + 1)
    efratio = 1.0
    workAma[r][instanceNo + 2] = price
    signal = (MathAbs(price - workAma[r - period][instanceNo + 2]) if (r >= period) else 0)
    noise = 0.0
    workAma[r][instanceNo + 0] = (MathAbs(price - workAma[r - 1][instanceNo + 2]) if (r > 0) else 0)
    k = 0
    while k < period and (r - k) >= 0:
        noise += workAma[r - k][instanceNo + 0]
        k += 1
    if noise != 0:
        efratio = _fdiv(signal, noise)
    else:
        efratio = 1.0
    smooth = MathPow((efratio * (fastend - slowend)) + slowend, power)
    workAma[r][instanceNo + 1] = ((workAma[r - 1][instanceNo + 1] + (smooth * (price - workAma[r - 1][instanceNo + 1]))) if (r > 0) else price)
    return workAma[r][instanceNo + 1]

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
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


class KAMAWithFilter(_MQL5Indicator):
    name = 'KAMA with filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpFastPeriod': 2,  # Fast end period
        'inpSlowPeriod': 30,  # Slow end period
        'inpPower': 2.0,  # Smooth power
        'inpFilter': 50,  # Filter
        'inpFilterPeriod': 4,  # Filter period
        'inpFilterDifference': 50.0,  # Filter difference
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

