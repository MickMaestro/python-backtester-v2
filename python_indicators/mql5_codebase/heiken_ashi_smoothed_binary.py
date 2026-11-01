"""Heiken Ashi Smoothed - binary — converted from MQL5: MQL5 Indicators/Heiken Ashi Smoothed - Binary/Heiken Ashi Smoothed - binary.mq5

ADXVMA moving average - binary
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1, 'indicator_minimum': -1.1, 'indicator_maximum': 1.1}, 'types': {1: 1}, 'colors': {1: [9639167]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'HeikenAshi'}, 'levels': [], 'description': ['ADXVMA moving average - binary'], 'name': 'Heiken Ashi Smoothed - binary', 'source': 'MQL5 Indicators/Heiken Ashi Smoothed - Binary/Heiken Ashi Smoothed - binary.mq5', 'folder': 'Heiken Ashi Smoothed - Binary', 'inputs': [{'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 7, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpMaMetod', 'py': 'inpMaMetod', 'param': 'inpMaMetod', 'type': 'int', 'default': 3, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'inpStep', 'py': 'inpStep', 'param': 'inpStep', 'type': 'int', 'default': 0, 'label': 'Step size', 'sinput': False}, {'mql': 'inpBetterFormula', 'py': 'inpBetterFormula', 'param': 'inpBetterFormula', 'type': 'bool', 'default': False, 'label': 'Use better formula', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpMaPeriod = _input('inpMaPeriod', 7)  # Smoothing period
inpMaMetod = _input('inpMaMetod', ma_lwma)  # Smoothing method
inpStep = _input('inpStep', 0)  # Step size
inpBetterFormula = _input('inpBetterFormula', False)  # Use better formula
hah = Arr(0, 0.0)
hal = Arr(0, 0.0)
hao = Arr(0, 0.0)
hac = Arr(0, 0.0)
val = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(4,))
workSmma = Arr(0, 0.0, dims=(4,))
workLwma = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, hao, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, hah, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, hal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, hac, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heiken ashi smoothed binary (' + _str(inpMaPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _pointModifier = MathPow(10, _imod(SymbolInfoInteger(Symbol(), SYMBOL_DIGITS), 2))
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        maOpen = iCustomMa(inpMaMetod, open[i], inpMaPeriod, i, rates_total, 0)
        maClose = iCustomMa(inpMaMetod, close[i], inpMaPeriod, i, rates_total, 1)
        maLow = iCustomMa(inpMaMetod, low[i], inpMaPeriod, i, rates_total, 2)
        maHigh = iCustomMa(inpMaMetod, high[i], inpMaPeriod, i, rates_total, 3)
        haClose = (((((maOpen + maClose) / 2) + (_fdiv(maClose - maOpen, maHigh - maLow) * MathAbs((maClose - maOpen) / 2))) if (maHigh != maLow) else ((maOpen + maClose) / 2)) if inpBetterFormula else ((maOpen + maHigh + maLow + maClose) / 4))
        haOpen = (((hao[i - 1] + hac[i - 1]) / 2) if (i > 0) else open[i])
        haHigh = MathMax(maHigh, MathMax(haOpen, haClose))
        haLow = MathMin(maLow, MathMin(haOpen, haClose))
        hal[i] = haLow
        hah[i] = haHigh
        hao[i] = haOpen
        hac[i] = haClose
        if i > 0 and inpStep > 0:
            if MathAbs(hah[i] - hah[i - 1]) < (inpStep * _pointModifier * Point()):
                hah[i] = hah[i - 1]
            if MathAbs(hal[i] - hal[i - 1]) < (inpStep * _pointModifier * Point()):
                hal[i] = hal[i - 1]
            if MathAbs(hao[i] - hao[i - 1]) < (inpStep * _pointModifier * Point()):
                hao[i] = hao[i - 1]
            if MathAbs(hac[i] - hac[i - 1]) < (inpStep * _pointModifier * Point()):
                hac[i] = hac[i - 1]
        val[i] = (-1 if (hao[i] > hac[i]) else 1 if (hao[i] < hac[i]) else val[i - 1] if (i > 0) else 0)
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
    avg = _fdiv(avg, float(k))
    return avg

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


class HeikenAshiSmoothedBinary(_MQL5Indicator):
    name = 'Heiken Ashi Smoothed - binary'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMaPeriod': 7,  # Smoothing period
        'inpMaMetod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=3),  # Smoothing method
        'inpStep': 0,  # Step size
        'inpBetterFormula': False,  # Use better formula
    }
    y_range = (-1.1, 1.1)

