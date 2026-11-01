"""ADXm — converted from MQL5: MQL5 Indicators/ADXm/ADXm.mq5

original mt4 version was made by ANG3110
this version made by Mladen
Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [8421504, 16748574, 6333684], 2: [8421504]}, 'widths': {1: 3}, 'styles': {2: 2}, 'labels': {1: 'ADXm', 2: 'ADXm DI'}, 'levels': [], 'description': ['original mt4 version was made by ANG3110', 'this version made by Mladen'], 'name': 'ADXm', 'source': 'MQL5 Indicators/ADXm/ADXm.mq5', 'folder': 'ADXm', 'inputs': [{'mql': 'AdxmPeriod', 'py': 'AdxmPeriod', 'param': 'AdxmPeriod', 'type': 'int', 'default': 14, 'label': 'ADXm period', 'sinput': False}, {'mql': 'AdxmPriceC', 'py': 'AdxmPriceC', 'param': 'AdxmPriceC', 'type': 'int', 'default': 0, 'label': 'Price to use for close', 'sinput': False}, {'mql': 'AdxmPriceH', 'py': 'AdxmPriceH', 'param': 'AdxmPriceH', 'type': 'int', 'default': 2, 'label': 'Price to use for high', 'sinput': False}, {'mql': 'AdxmPriceL', 'py': 'AdxmPriceL', 'param': 'AdxmPriceL', 'type': 'int', 'default': 3, 'label': 'Price to use for low', 'sinput': False}, {'mql': 'AdxmLevels', 'py': 'AdxmLevels', 'param': 'AdxmLevels', 'type': 'double', 'default': 25.0, 'label': 'Levels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
pr_medianb = 8
pr_tbiased = 9
pr_tbiased2 = 10
pr_haclose = 11
pr_haopen = 12
pr_hahigh = 13
pr_halow = 14
pr_hamedian = 15
pr_hatypical = 16
pr_haweighted = 17
pr_haaverage = 18
pr_hamedianb = 19
pr_hatbiased = 20
pr_hatbiased2 = 21
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_medianb', 9: 'pr_tbiased', 10: 'pr_tbiased2', 11: 'pr_haclose', 12: 'pr_haopen', 13: 'pr_hahigh', 14: 'pr_halow', 15: 'pr_hamedian', 16: 'pr_hatypical', 17: 'pr_haweighted', 18: 'pr_haaverage', 19: 'pr_hamedianb', 20: 'pr_hatbiased', 21: 'pr_hatbiased2'})

# ---- inputs and global variables
AdxmPeriod = _input('AdxmPeriod', 14)  # ADXm period
AdxmPriceC = _input('AdxmPriceC', pr_close)  # Price to use for close
AdxmPriceH = _input('AdxmPriceH', pr_high)  # Price to use for high
AdxmPriceL = _input('AdxmPriceL', pr_low)  # Price to use for low
AdxmLevels = _input('AdxmLevels', 25.0)  # Levels
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
di = Arr(0, 0.0)
_adxmWork = Arr(0, 0.0, dims=(8,))
workHa = Arr(0, 0.0, dims=(12,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, di, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, -AdxmLevels)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, AdxmLevels)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ADXm (' + _str(AdxmPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return 0
    i = 0
    i = MathMax(prev_calculated - 1, 0)
    for i in range(i, rates_total):
        _prices = Arr(3, 0.0, dyn=False)
        _di = Box(0.0)
        _adx = Box(0.0)
        _prices[0] = getPrice(AdxmPriceC, open, close, high, low, i, rates_total, 0)
        _prices[1] = getPrice(AdxmPriceH, open, close, high, low, i, rates_total, 1)
        _prices[2] = getPrice(AdxmPriceL, open, close, high, low, i, rates_total, 2)
        ArraySort(_prices)
        iAdxm(_prices[1], _prices[2], _prices[0], AdxmPeriod, _adx, _di, i, rates_total)
        di[i] = _di.v
        val[i] = _adx.v
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    else:
        i = _range_end(i, rates_total, 1)
    return i

def iAdxm(_close, _high, _low, _period, _adx, _di, i, bars, instanceNo=0):
    if ArrayRange(_adxmWork, 0) != bars:
        ArrayResize(_adxmWork, bars)
    instanceNo *= 8
    _adxmWork[i][instanceNo + 3] = _close
    _adxmWork[i][instanceNo + 4] = _high
    _adxmWork[i][instanceNo + 5] = _low
    hc = _adxmWork[i][instanceNo + 4]
    lc = _adxmWork[i][instanceNo + 5]
    cp = (_adxmWork[i - 1][instanceNo + 3] if (i > 0) else _adxmWork[i][instanceNo + 3])
    hp = (_adxmWork[i - 1][instanceNo + 4] if (i > 0) else _adxmWork[i][instanceNo + 4])
    lp = (_adxmWork[i - 1][instanceNo + 5] if (i > 0) else _adxmWork[i][instanceNo + 5])
    dh = MathMax(hc - hp, 0)
    dl = MathMax(lp - lc, 0)
    if dh == dl:
        dh = 0.0
        dl = 0.0
    elif dh < dl:
        dh = 0.0
    elif dl < dh:
        dl = 0.0
    tr = MathMax(hc, cp) - MathMin(lc, cp)
    dhk = (_fdiv(100.0 * dh, tr) if (tr != 0) else 0)
    dlk = (_fdiv(100.0 * dl, tr) if (tr != 0) else 0)
    alpha = _fdiv(2.0, _period + 1.0)
    _adxmWork[i][instanceNo + 0] = ((_adxmWork[i - 1][instanceNo + 0] + (alpha * (dhk - _adxmWork[i - 1][instanceNo + 0]))) if (i > 0) else dhk)
    _adxmWork[i][instanceNo + 1] = ((_adxmWork[i - 1][instanceNo + 1] + (alpha * (dlk - _adxmWork[i - 1][instanceNo + 1]))) if (i > 0) else dlk)
    _adxmWork[i][instanceNo + 6] = _adxmWork[i][instanceNo + 0] - _adxmWork[i][instanceNo + 1]
    div = MathAbs(_adxmWork[i][instanceNo + 0] + _adxmWork[i][instanceNo + 1])
    temp = (_fdiv(100 * _adxmWork[i][instanceNo + 6], div) if (div != 0.0) else 0)
    _adxmWork[i][instanceNo + 7] = ((_adxmWork[i - 1][instanceNo + 7] + (alpha * (temp - _adxmWork[i - 1][instanceNo + 7]))) if (i > 0) else 0)
    _adx.v = _adxmWork[i][instanceNo + 7]
    _di.v = _adxmWork[i][instanceNo + 6]
    return

def getPrice(tprice, open, close, high, low, i, _bars, instanceNo=0):
    if tprice >= pr_haclose:
        if ArrayRange(workHa, 0) != _bars:
            ArrayResize(workHa, _bars)
        instanceNo *= 4
        haOpen = 0.0
        if i > 0:
            haOpen = (workHa[i - 1][instanceNo + 2] + workHa[i - 1][instanceNo + 3]) / 2.0
        else:
            haOpen = (open[i] + close[i]) / 2
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][instanceNo + 0] = haLow
            workHa[i][instanceNo + 1] = haHigh
        else:
            workHa[i][instanceNo + 0] = haHigh
            workHa[i][instanceNo + 1] = haLow
        workHa[i][instanceNo + 2] = haOpen
        workHa[i][instanceNo + 3] = haClose
        _sw1 = tprice
        if _sw1 == pr_haclose:
            return haClose
        elif _sw1 == pr_haopen:
            return haOpen
        elif _sw1 == pr_hahigh:
            return haHigh
        elif _sw1 == pr_halow:
            return haLow
        elif _sw1 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw1 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw1 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw1 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw1 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw1 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw1 == pr_hatbiased2:
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw2 = tprice
    if _sw2 == pr_close:
        return close[i]
    elif _sw2 == pr_open:
        return open[i]
    elif _sw2 == pr_high:
        return high[i]
    elif _sw2 == pr_low:
        return low[i]
    elif _sw2 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw2 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw2 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw2 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADXm(_MQL5Indicator):
    name = 'ADXm'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AdxmPeriod': 14,  # ADXm period
        'AdxmPriceC': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=0),  # Price to use for close
        'AdxmPriceH': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=2),  # Price to use for high
        'AdxmPriceL': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Heiken ashi close', 12: 'Heiken ashi open', 13: 'Heiken ashi high', 14: 'Heiken ashi low', 15: 'Heiken ashi median', 16: 'Heiken ashi typical', 17: 'Heiken ashi weighted', 18: 'Heiken ashi average', 19: 'Heiken ashi median body', 20: 'Heiken ashi trend biased price', 21: 'Heiken ashi trend biased (extreme) price'}, default=3),  # Price to use for low
        'AdxmLevels': 25.0,  # Levels
    }

