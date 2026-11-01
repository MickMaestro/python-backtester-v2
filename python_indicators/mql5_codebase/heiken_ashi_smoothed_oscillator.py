"""Heiken ashi smoothed oscillator — converted from MQL5: MQL5 Indicators/Heiken Ashi Smoothed Oscillator/Heiken ashi smoothed oscillator.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 10, 2: 8, 3: 8}, 'colors': {1: [16436871, 6333684], 2: [16436871, 6333684], 3: [16748574, 5275647]}, 'widths': {1: 2, 3: 2}, 'styles': {}, 'labels': {1: 'HA oscillator histogram', 2: 'HA oscillator line', 3: 'HA oscillator average'}, 'levels': [], 'description': [], 'name': 'Heiken ashi smoothed oscillator', 'source': 'MQL5 Indicators/Heiken Ashi Smoothed Oscillator/Heiken ashi smoothed oscillator.mq5', 'folder': 'Heiken Ashi Smoothed Oscillator', 'inputs': [{'mql': 'inpMaPreSmoothPeriod', 'py': 'inpMaPreSmoothPeriod', 'param': 'inpMaPreSmoothPeriod', 'type': 'int', 'default': 7, 'label': 'Pre smoothing average period', 'sinput': False}, {'mql': 'inpMaPreSmoothMethod', 'py': 'inpMaPreSmoothMethod', 'param': 'inpMaPreSmoothMethod', 'type': 'int', 'default': 3, 'label': 'Pre smoothing average method', 'sinput': False}, {'mql': 'inpMaPosSmoothPeriod', 'py': 'inpMaPosSmoothPeriod', 'param': 'inpMaPosSmoothPeriod', 'type': 'int', 'default': 7, 'label': 'Pos smoothing average period', 'sinput': False}, {'mql': 'inpMaPosSmoothMethod', 'py': 'inpMaPosSmoothMethod', 'param': 'inpMaPosSmoothMethod', 'type': 'int', 'default': 3, 'label': 'Pos smoothing average method', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 2, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 2, 'label': 'Signal method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpMaPreSmoothPeriod = _input('inpMaPreSmoothPeriod', 7)  # Pre smoothing average period
inpMaPreSmoothMethod = _input('inpMaPreSmoothMethod', ma_lwma)  # Pre smoothing average method
inpMaPosSmoothPeriod = _input('inpMaPosSmoothPeriod', 7)  # Pos smoothing average period
inpMaPosSmoothMethod = _input('inpMaPosSmoothMethod', ma_lwma)  # Pos smoothing average method
inpMaPeriod = _input('inpMaPeriod', 2)  # Signal period
inpMaMethod = _input('inpMaMethod', ma_smma)  # Signal method
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
lin = Arr(0, 0.0)
linc = Arr(0, 0.0)
signal = Arr(0, 0.0)
signalc = Arr(0, 0.0)
workHa = Arr(0, 0.0, dims=(5,))
workSma = Arr(0, 0.0, dims=(6,))
workEma = Arr(0, 0.0, dims=(6,))
workSmma = Arr(0, 0.0, dims=(6,))
workLwma = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, lin, INDICATOR_DATA)
    SetIndexBuffer(3, linc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, signal, INDICATOR_DATA)
    SetIndexBuffer(5, signalc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heiken ashi smoothed oscillator (' + _str(inpMaPeriod) + ',' + _str(inpMaPreSmoothPeriod) + ',' + _str(inpMaPosSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if ArrayRange(workHa, 0) != rates_total:
        ArrayResize(workHa, rates_total)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        maOpen = iCustomMa(inpMaPreSmoothMethod, open[i], inpMaPreSmoothPeriod, i, rates_total, 0)
        maClose = iCustomMa(inpMaPreSmoothMethod, close[i], inpMaPreSmoothPeriod, i, rates_total, 1)
        maLow = iCustomMa(inpMaPreSmoothMethod, low[i], inpMaPreSmoothPeriod, i, rates_total, 2)
        maHigh = iCustomMa(inpMaPreSmoothMethod, high[i], inpMaPreSmoothPeriod, i, rates_total, 3)
        haOpen = (((workHa[i - 1][2] + workHa[i - 1][3]) / 2.0) if (i > 0) else ((open[i] + close[i]) / 2))
        haClose = (maOpen + maHigh + maLow + maClose) / 4.0
        haHigh = MathMax(maHigh, MathMax(haOpen, haClose))
        haLow = MathMin(maLow, MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][0] = haLow
            workHa[i][1] = haHigh
        else:
            workHa[i][0] = haHigh
            workHa[i][1] = haLow
        workHa[i][2] = haOpen
        workHa[i][3] = haClose
        workHa[i][4] = iCustomMa(inpMaPosSmoothMethod, (haOpen + haClose) / 2, inpMaPosSmoothPeriod, i, rates_total, 4)
        val[i] = ((workHa[i][4] - workHa[i - 1][4]) if (i > 0) else 0)
        lin[i] = val[i]
        valc[i] = (1 if (val[i] < 0) else 0)
        linc[i] = valc[i]
        signal[i] = iCustomMa(inpMaMethod, val[i], inpMaPeriod, i, rates_total, 5)
        signalc[i] = (0 if (val[i] > signal[i]) else 1 if (val[i] < signal[i]) else signalc[i - 1] if (i > 0) else 0)
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


class HeikenAshiSmoothedOscillator(_MQL5Indicator):
    name = 'Heiken ashi smoothed oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMaPreSmoothPeriod': 7,  # Pre smoothing average period
        'inpMaPreSmoothMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=3),  # Pre smoothing average method
        'inpMaPosSmoothPeriod': 7,  # Pos smoothing average period
        'inpMaPosSmoothMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=3),  # Pos smoothing average method
        'inpMaPeriod': 2,  # Signal period
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=2),  # Signal method
    }

