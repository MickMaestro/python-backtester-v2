"""Dsl - Balance of Market Power — converted from MQL5: MQL5 Indicators/Dsl - Balance of Market Power/Dsl - Balance of Market Power.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [3329330], 2: [42495], 3: [12632256, 3329330, 42495]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'up level', 2: 'down level', 3: 'Balance of Market Power'}, 'levels': [], 'description': [], 'name': 'Dsl - Balance of Market Power', 'source': 'MQL5 Indicators/Dsl - Balance of Market Power/Dsl - Balance of Market Power.mq5', 'folder': 'Dsl - Balance of Market Power', 'inputs': [{'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 14, 'label': 'Result smoothing period', 'sinput': False}, {'mql': 'inpSmoothMethod', 'py': 'inpSmoothMethod', 'param': 'inpSmoothMethod', 'type': 'int', 'default': 0, 'label': 'Result smoothing type', 'sinput': False}, {'mql': 'inpSigPeriod', 'py': 'inpSigPeriod', 'param': 'inpSigPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpDisplayType', 'py': 'inpDisplayType', 'param': 'inpDisplayType', 'type': 'int', 'default': 0, 'label': 'Display type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# enum enDisplayType
dis_line = 0
dis_histo = 1
_enum('enDisplayType', {0: 'dis_line', 1: 'dis_histo'})

# ---- inputs and global variables
inpSmoothPeriod = _input('inpSmoothPeriod', 14)  # Result smoothing period
inpSmoothMethod = _input('inpSmoothMethod', ma_sma)  # Result smoothing type
inpSigPeriod = _input('inpSigPeriod', 9)  # Signal period
inpDisplayType = _input('inpDisplayType', dis_line)  # Display type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, levelUp, INDICATOR_DATA)
    SetIndexBuffer(1, levelDn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, (DRAW_COLOR_LINE if (inpDisplayType == dis_line) else DRAW_COLOR_HISTOGRAM))
    _avgNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
    IndicatorSetString(INDICATOR_SHORTNAME, '(dsl) Balance of Market Power (' + _avgNames[inpSmoothMethod] + ')(' + _str(inpSmoothPeriod) + ',' + _str(inpSigPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    alpha = _fdiv(2.0, 1.0 + inpSigPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        HighLowRange = high[i] - low[i]
        BullsRewardBasedOnOpen = (_fdiv(high[i] - open[i], HighLowRange) if (HighLowRange != 0) else 0)
        BearsRewardBasedOnOpen = (_fdiv(open[i] - low[i], HighLowRange) if (HighLowRange != 0) else 0)
        BullsRewardBasedOnClose = (_fdiv(close[i] - low[i], HighLowRange) if (HighLowRange != 0) else 0)
        BearsRewardBasedOnClose = (_fdiv(high[i] - close[i], HighLowRange) if (HighLowRange != 0) else 0)
        BullsRewardBasedOnOpenClose = ((_fdiv(close[i] - open[i], HighLowRange) if (close[i] > open[i]) else 0) if (HighLowRange != 0) else 0)
        BearsRewardBasedOnOpenClose = ((_fdiv(open[i] - close[i], HighLowRange) if (close[i] < open[i]) else 0) if (HighLowRange != 0) else 0)
        BullsRewardDaily = (BullsRewardBasedOnOpen + BullsRewardBasedOnClose + BullsRewardBasedOnOpenClose) / 3
        BearsRewardDaily = (BearsRewardBasedOnOpen + BearsRewardBasedOnClose + BearsRewardBasedOnOpenClose) / 3
        val[i] = iCustomMa(inpSmoothMethod, BullsRewardDaily - BearsRewardDaily, inpSmoothPeriod, i, rates_total)
        levelUp[i] = (((levelUp[i - 1] + (alpha * (val[i] - levelUp[i - 1]))) if (val[i] > 0) else levelUp[i - 1]) if (i > 0) else 0)
        levelDn[i] = (((levelDn[i - 1] + (alpha * (val[i] - levelDn[i - 1]))) if (val[i] < 0) else levelDn[i - 1]) if (i > 0) else 0)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return i

def iCustomMa(mode, price, length, r, bars, instanceNo=0):
    _sw1 = mode
    if _sw1 == ma_sma:
        return iSma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_ema:
        return iEma(price, length, r, bars, instanceNo)
    elif _sw1 == ma_smma:
        return iSmma(price, _int(length), r, bars, instanceNo)
    elif _sw1 == ma_lwma:
        return iLwma(price, _int(length), r, bars, instanceNo)
    else:
        return price

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))

def iEma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workEma, 0) != _bars:
        ArrayResize(workEma, _bars)
    workEma[r][instanceNo] = price
    if r > 0 and period > 1:
        workEma[r][instanceNo] = workEma[r - 1][instanceNo] + (_fdiv(2.0, 1.0 + period) * (price - workEma[r - 1][instanceNo]))
    return workEma[r][instanceNo]

def iSmma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != _bars:
        ArrayResize(workSmma, _bars)
    workSmma[r][instanceNo] = price
    if r > 1 and period > 1:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iLwma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workLwma, 0) != _bars:
        ArrayResize(workLwma, _bars)
    workLwma[r][instanceNo] = price
    if period < 1:
        return price
    sumw = period
    sum_ = period * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = period - k
        sumw += weight
        sum_ += weight * workLwma[r - k][instanceNo]
        k += 1
    return _fdiv(sum_, sumw)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DslBalanceOfMarketPower(_MQL5Indicator):
    name = 'Dsl - Balance of Market Power'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpSmoothPeriod': 14,  # Result smoothing period
        'inpSmoothMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Result smoothing type
        'inpSigPeriod': 9,  # Signal period
        'inpDisplayType': _Choice({0: 'Display Balance of Market Power as line', 1: 'Display Balance of Market Power as histogram'}, default=0),  # Display type
    }

