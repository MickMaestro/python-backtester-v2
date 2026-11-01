"""Vervoort Crossover tape — converted from MQL5: MQL5 Indicators/Vervoort's crossover - tape/Vervoort Crossover tape.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [7451452, 17919], 2: [12632256], 3: [6908265]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Tape', 2: 'High', 3: 'Low'}, 'levels': [], 'description': [], 'name': 'Vervoort Crossover tape', 'source': "MQL5 Indicators/Vervoort's crossover - tape/Vervoort Crossover tape.mq5", 'folder': "Vervoort's crossover - tape", 'inputs': [{'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'double', 'default': 55.0, 'label': 'Fast tema period', 'sinput': False}, {'mql': 'inpPrice1', 'py': 'inpPrice1', 'param': 'inpPrice1', 'type': 'int', 'default': 5, 'label': 'Fast tema price', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'double', 'default': 55.0, 'label': 'Slow tema period', 'sinput': False}, {'mql': 'inpPrice2', 'py': 'inpPrice2', 'param': 'inpPrice2', 'type': 'int', 'default': 17, 'label': 'Slow tema price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
pr_haclose = 10
pr_haopen = 11
pr_hahigh = 12
pr_halow = 13
pr_hamedian = 14
pr_hatypical = 15
pr_haweighted = 16
pr_haaverage = 17
pr_hamedianb = 18
pr_hatbiased = 19
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_medianb', 9: 'pr_tbiased', 10: 'pr_haclose', 11: 'pr_haopen', 12: 'pr_hahigh', 13: 'pr_halow', 14: 'pr_hamedian', 15: 'pr_hatypical', 16: 'pr_haweighted', 17: 'pr_haaverage', 18: 'pr_hamedianb', 19: 'pr_hatbiased'})

# ---- inputs and global variables
inpPeriod1 = _input('inpPeriod1', 55.0)  # Fast tema period
inpPrice1 = _input('inpPrice1', pr_typical)  # Fast tema price
inpPeriod2 = _input('inpPeriod2', 55.0)  # Slow tema period
inpPrice2 = _input('inpPrice2', pr_haaverage)  # Slow tema price
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
valf = Arr(0, 0.0)
vals = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, valu, INDICATOR_DATA)
    SetIndexBuffer(1, vald, INDICATOR_DATA)
    SetIndexBuffer(2, valf, INDICATOR_DATA)
    SetIndexBuffer(3, vals, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Vervoort crossover (' + _str(inpPeriod1) + ',' + _str(inpPeriod2) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        fast = iZlTema(getPrice(inpPrice1, open, close, high, low, i, rates_total), inpPeriod1, i, rates_total, 0)
        slow = iZlTema(getPrice(inpPrice2, open, close, high, low, i, rates_total), inpPeriod2, i, rates_total, 1)
        _median = (fast + slow) / 2.0
        valf[i] = fast - _median
        valu[i] = valf[i]
        vald[i] = slow - _median
        vald[i] = vald[i]
        i += 1
    return i

def iZlTema(price, period, i, bars, instanceNo=0):
    global _s_iZlTema_m_arraySize
    if _s_iZlTema_m_arraySize < bars:
        _s_iZlTema_m_arraySize = ArrayResize(_s_iZlTema_m_array, bars + 500)
        if _s_iZlTema_m_arraySize < bars:
            return 0.0
    instanceNo *= 6
    if i > 0 and period > 1:
        alpha = _fdiv(2.0, 1.0 + period)
        _s_iZlTema_m_array[i][0 + instanceNo] = _s_iZlTema_m_array[i - 1][0 + instanceNo] + (alpha * (price - _s_iZlTema_m_array[i - 1][0 + instanceNo]))
        _s_iZlTema_m_array[i][1 + instanceNo] = _s_iZlTema_m_array[i - 1][1 + instanceNo] + (alpha * (_s_iZlTema_m_array[i][0 + instanceNo] - _s_iZlTema_m_array[i - 1][1 + instanceNo]))
        _s_iZlTema_m_array[i][2 + instanceNo] = _s_iZlTema_m_array[i - 1][2 + instanceNo] + (alpha * (_s_iZlTema_m_array[i][1 + instanceNo] - _s_iZlTema_m_array[i - 1][2 + instanceNo]))
        tema1 = _s_iZlTema_m_array[i][2 + instanceNo] + (3.0 * (_s_iZlTema_m_array[i][0 + instanceNo] - _s_iZlTema_m_array[i][1 + instanceNo]))
        _s_iZlTema_m_array[i][3 + instanceNo] = _s_iZlTema_m_array[i - 1][3 + instanceNo] + (alpha * (tema1 - _s_iZlTema_m_array[i - 1][3 + instanceNo]))
        _s_iZlTema_m_array[i][4 + instanceNo] = _s_iZlTema_m_array[i - 1][4 + instanceNo] + (alpha * (_s_iZlTema_m_array[i][3 + instanceNo] - _s_iZlTema_m_array[i - 1][4 + instanceNo]))
        _s_iZlTema_m_array[i][5 + instanceNo] = _s_iZlTema_m_array[i - 1][5 + instanceNo] + (alpha * (_s_iZlTema_m_array[i][4 + instanceNo] - _s_iZlTema_m_array[i - 1][5 + instanceNo]))
        tema2 = _s_iZlTema_m_array[i][5 + instanceNo] + (3.0 * (_s_iZlTema_m_array[i][3 + instanceNo] - _s_iZlTema_m_array[i][4 + instanceNo]))
        return (2.0 * tema1) - tema2
    else:
        _s_iZlTema_m_array[i][0 + instanceNo] = price
        _s_iZlTema_m_array[i][1 + instanceNo] = price
        _s_iZlTema_m_array[i][2 + instanceNo] = price
        _s_iZlTema_m_array[i][3 + instanceNo] = price
        _s_iZlTema_m_array[i][4 + instanceNo] = price
        _s_iZlTema_m_array[i][5 + instanceNo] = price
    return price

def getPrice(tprice, open, close, high, low, i, _bars):
    global _s_getPrice_m_arraySize
    if tprice >= pr_haclose:
        if _s_getPrice_m_arraySize < _bars:
            _s_getPrice_m_arraySize = ArrayResize(_s_getPrice_workHa, _bars + 500)
            if _s_getPrice_m_arraySize < _bars:
                return 0.0
        haOpen = (((_s_getPrice_workHa[i - 1][2] + _s_getPrice_workHa[i - 1][3]) / 2.0) if (i > 0) else ((open[i] + close[i]) / 2))
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = (high[i] if (high[i] > (haOpen if (haOpen > haClose) else haClose)) else haOpen if (haOpen > haClose) else haClose)
        haLow = (low[i] if (low[i] < (haOpen if (haOpen < haClose) else haClose)) else haOpen if (haOpen < haClose) else haClose)
        if haOpen < haClose:
            _s_getPrice_workHa[i][0] = haLow
            _s_getPrice_workHa[i][1] = haHigh
        else:
            _s_getPrice_workHa[i][0] = haHigh
            _s_getPrice_workHa[i][1] = haLow
        _s_getPrice_workHa[i][2] = haOpen
        _s_getPrice_workHa[i][3] = haClose
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
    return 0.0

# ---- static local variables
_s_iZlTema_m_array = Arr(0, 0.0, dims=(12,))
_s_iZlTema_m_arraySize = -1
_s_getPrice_workHa = Arr(0, 0.0, dims=(4,))
_s_getPrice_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VervoortCrossoverTape(_MQL5Indicator):
    name = 'Vervoort Crossover tape'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod1': 55.0,  # Fast tema period
        'inpPrice1': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=5),  # Fast tema price
        'inpPeriod2': 55.0,  # Slow tema period
        'inpPrice2': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=17),  # Slow tema price
    }

