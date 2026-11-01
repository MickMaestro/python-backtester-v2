"""Ehlers Quotient Transform — converted from MQL5: MQL5 Indicators/Ehlers Quotient Transform/Ehlers Quotient Transform.mq5

Copyright: © mladen, 2021; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16760576], 2: [6333684]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Ehlers Quotient Transform', 'source': 'MQL5 Indicators/Ehlers Quotient Transform/Ehlers Quotient Transform.mq5', 'folder': 'Ehlers Quotient Transform', 'inputs': [{'mql': 'CalcPeriod', 'py': 'CalcPeriod', 'param': 'CalcPeriod', 'type': 'int', 'default': 20, 'label': 'Calculation period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'Q1', 'py': 'Q1', 'param': 'Q1', 'type': 'double', 'default': 0.8, 'label': 'K for entries', 'sinput': False}, {'mql': 'Q2', 'py': 'Q2', 'param': 'Q2', 'type': 'double', 'default': 0.4, 'label': 'K for exits', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
CalcPeriod = _input('CalcPeriod', 20)  # Calculation period
Price = _input('Price', pr_close)  # Price
Q1 = _input('Q1', 0.8)  # K for entries
Q2 = _input('Q2', 0.4)  # K for exits
quot1 = Arr(0, 0.0)
quot2 = Arr(0, 0.0)
hp = Arr(0, 0.0)
peak = Arr(0, 0.0)
prices = Arr(0, 0.0)

class sCoeffsStruct(MqlObject):
    _q_fields = ('_speriod', '_sc1', '_sc2', '_sc3')
    def __init__(self):
        self._speriod = 0.0
        self._sc1 = 0.0
        self._sc2 = 0.0
        self._sc3 = 0.0
        self._speriod = EMPTY_VALUE

class sDataStruct(MqlObject):
    _q_fields = ('_tprice', '_ssm')
    def __init__(self, *args):
        self._tprice = 0.0
        self._ssm = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('data',)
    def __init__(self, *args):
        self.data = Arr(1, 0, dyn=False, factory=sDataStruct)

def OnInit():
    SetIndexBuffer(0, quot1, INDICATOR_DATA)
    SetIndexBuffer(1, quot2, INDICATOR_DATA)
    SetIndexBuffer(2, hp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, peak, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = (0 if (prev_calculated == 0) else (prev_calculated - 1))
    for i in range(limit, rates_total):
        prices[i] = getPrice(Price, open, close, high, low, i, rates_total)
        if i < 2:
            hp[i] = prices[i]
            peak[i] = prices[i]
            iSsm(hp[i], CalcPeriod, i, rates_total)
            continue
        hp[i] = ((1 - (alpha / 2.0)) * (1 - (alpha / 2.0)) * (prices[i] - (2.0 * prices[i - 1]) + prices[i - 2])) + (2.0 * (1 - alpha) * hp[i - 1]) - ((1 - alpha) * (1 - alpha) * hp[i - 2])
        peak[i] = 0.991 * peak[i - 1]
        hps = iSsm(hp[i], CalcPeriod, i, rates_total)
        if MathAbs(hps) > peak[i]:
            peak[i] = MathAbs(hps)
        x = 0.0
        if peak[i] != 0:
            x = _fdiv(hps, peak[i])
        quot1[i] = _fdiv(x + Q1, (Q1 * x) + 1.0)
        quot2[i] = _fdiv(x + Q2, (Q2 * x) + 1.0)
    return rates_total

def iSsm(price, period, i, bars, instanceNo=0):
    global _s_iSsm_m_workSize
    if _s_iSsm_m_workSize < bars:
        _s_iSsm_m_workSize = ArrayResize(_s_iSsm_m_work, bars + 500, 2000)
    if _s_iSsm_m_coeffs[instanceNo]._speriod != period:
        _s_iSsm_m_coeffs[instanceNo]._speriod = period
        a1 = MathExp(_fdiv(-1.414 * M_PI, period))
        b1 = 2.0 * a1 * MathCos(_fdiv(1.414 * M_PI, period))
        _s_iSsm_m_coeffs[instanceNo]._sc2 = b1
        _s_iSsm_m_coeffs[instanceNo]._sc3 = (-a1) * a1
        _s_iSsm_m_coeffs[instanceNo]._sc1 = 1.0 - _s_iSsm_m_coeffs[instanceNo]._sc2 - _s_iSsm_m_coeffs[instanceNo]._sc3
    _s_iSsm_m_work[i].data[instanceNo]._tprice = price
    _s_iSsm_m_work[i].data[instanceNo]._ssm = _s_iSsm_m_work[i].data[instanceNo]._tprice
    if i > 1:
        _s_iSsm_m_work[i].data[instanceNo]._ssm = ((_s_iSsm_m_coeffs[instanceNo]._sc1 * (_s_iSsm_m_work[i].data[instanceNo]._tprice + _s_iSsm_m_work[i - 1].data[instanceNo]._tprice)) / 2.0) + (_s_iSsm_m_coeffs[instanceNo]._sc2 * _s_iSsm_m_work[i - 1].data[instanceNo]._ssm) + (_s_iSsm_m_coeffs[instanceNo]._sc3 * _s_iSsm_m_work[i - 1].data[instanceNo]._ssm)
    return _s_iSsm_m_work[i].data[instanceNo]._ssm

def getPrice(tprice, open, close, high, low, i, bars):
    global _s_getPrice_workHaSize
    if tprice >= pr_haclose:
        if _s_getPrice_workHaSize < bars:
            _s_getPrice_workHaSize = ArrayResize(_s_getPrice_workHa, bars + 500, 2000)
        r = i
        haOpen = 0.0
        if r > 0:
            haOpen = (_s_getPrice_workHa[r - 1][2] + _s_getPrice_workHa[r - 1][3]) / 2.0
        else:
            haOpen = (open[i] + close[i]) / 2
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            _s_getPrice_workHa[r][0] = haLow
            _s_getPrice_workHa[r][1] = haHigh
        else:
            _s_getPrice_workHa[r][0] = haHigh
            _s_getPrice_workHa[r][1] = haLow
        _s_getPrice_workHa[r][2] = haOpen
        _s_getPrice_workHa[r][3] = haClose
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

# ---- global variables initialised from expressions
angle = (0.707 * 2.0 * M_PI) / 100
alpha = _fdiv(cos(angle) + sin(angle) - 1.0, cos(angle))

# ---- static local variables
_s_iSsm_m_coeffs = Arr(1, 0, dyn=False, factory=sCoeffsStruct)
_s_iSsm_m_work = Arr(0, 0, factory=sWorkStruct)
_s_iSsm_m_workSize = -1
_s_getPrice_workHa = Arr(0, 0.0, dims=(4,))
_s_getPrice_workHaSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersQuotientTransform(_MQL5Indicator):
    name = 'Ehlers Quotient Transform'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CalcPeriod': 20,  # Calculation period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=0),  # Price
        'Q1': 0.8,  # K for entries
        'Q2': 0.4,  # K for exits
    }

