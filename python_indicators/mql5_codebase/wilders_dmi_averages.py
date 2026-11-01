"""Wilders DMI - averages — converted from MQL5: MQL5 Indicators/Wilders DMI - averages/Wilders DMI - averages.mq5

Wilders DMI - averages
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 1}, 'colors': {1: [11861960, 14804223], 2: [3329330], 3: [55295], 4: [12632256]}, 'widths': {2: 2, 3: 2}, 'styles': {2: 0, 3: 0, 4: 2}, 'labels': {1: 'ADX trend', 2: 'ADX', 3: 'ADXR', 4: 'Level'}, 'levels': [], 'description': ['Wilders DMI - averages'], 'name': 'Wilders DMI - averages', 'source': 'MQL5 Indicators/Wilders DMI - averages/Wilders DMI - averages.mq5', 'folder': 'Wilders DMI - averages', 'inputs': [{'mql': 'AdxPeriod', 'py': 'AdxPeriod', 'param': 'AdxPeriod', 'type': 'int', 'default': 14, 'label': 'ADX (DMI) period', 'sinput': False}, {'mql': 'AdxLevel', 'py': 'AdxLevel', 'param': 'AdxLevel', 'type': 'double', 'default': 20.0, 'label': 'ADX level', 'sinput': False}, {'mql': 'ShowADX', 'py': 'ShowADX', 'param': 'ShowADX', 'type': 'bool', 'default': True, 'label': 'ADX visible', 'sinput': False}, {'mql': 'ShowADXR', 'py': 'ShowADXR', 'param': 'ShowADXR', 'type': 'bool', 'default': False, 'label': 'ADXR visible', 'sinput': False}, {'mql': 'AverageType', 'py': 'AverageType', 'param': 'AverageType', 'type': 'int', 'default': 2, 'label': 'Average type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
AdxPeriod = _input('AdxPeriod', 14)  # ADX (DMI) period
AdxLevel = _input('AdxLevel', 20.0)  # ADX level
ShowADX = _input('ShowADX', True)  # ADX visible
ShowADXR = _input('ShowADXR', False)  # ADXR visible
AverageType = _input('AverageType', ma_smma)  # Average type
DIp = Arr(0, 0.0)
DIm = Arr(0, 0.0)
ADX = Arr(0, 0.0)
ADXR = Arr(0, 0.0)
Level = Arr(0, 0.0)
_maNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
averages = Arr(0, 0.0, dims=(4,))
workSma = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(4,))
workSmma = Arr(0, 0.0, dims=(4,))
workLwma = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, DIp, INDICATOR_DATA)
    SetIndexBuffer(1, DIm, INDICATOR_DATA)
    SetIndexBuffer(2, ADX, INDICATOR_DATA)
    SetIndexBuffer(3, ADXR, INDICATOR_DATA)
    SetIndexBuffer(4, Level, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, _maNames[AverageType] + " Wilder''s DMI (" + _str(AdxPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArrayRange(averages, 0) != rates_total:
        ArrayResize(averages, rates_total)
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        currTR = MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])
        DeltaHi = high[i] - high[i - 1]
        DeltaLo = low[i - 1] - low[i]
        plusDM = 0.0
        minusDM = 0.0
        if DeltaHi > DeltaLo and DeltaHi > 0:
            plusDM = DeltaHi
        if DeltaLo > DeltaHi and DeltaLo > 0:
            minusDM = DeltaLo
        averages[i][0] = iCustomMa(AverageType, plusDM, AdxPeriod, i, rates_total, 0)
        averages[i][1] = iCustomMa(AverageType, minusDM, AdxPeriod, i, rates_total, 1)
        averages[i][2] = iCustomMa(AverageType, currTR, AdxPeriod, i, rates_total, 2)
        Level[i] = AdxLevel
        DIp[i] = 0.0
        DIm[i] = 0.0
        ADX[i] = EMPTY_VALUE
        ADXR[i] = EMPTY_VALUE
        if averages[i][2] > 0:
            DIp[i] = _fdiv(100.0 * averages[i][0], averages[i][2])
            DIm[i] = _fdiv(100.0 * averages[i][1], averages[i][2])
        if ShowADX:
            DX = 0.0
            if (DIp[i] + DIm[i]) > 0:
                DX = _fdiv(100 * MathAbs(DIp[i] - DIm[i]), DIp[i] + DIm[i])
            else:
                DX = 0.0
            averages[i][3] = iCustomMa(AverageType, DX, AdxPeriod, i, rates_total, 3)
            ADX[i] = averages[i][3]
            if ShowADXR and i >= AdxPeriod:
                ADXR[i] = 0.5 * (ADX[i] + ADX[i - AdxPeriod])
    return rates_total

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


class WildersDMIAverages(_MQL5Indicator):
    name = 'Wilders DMI - averages'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AdxPeriod': 14,  # ADX (DMI) period
        'AdxLevel': 20.0,  # ADX level
        'ShowADX': True,  # ADX visible
        'ShowADXR': False,  # ADXR visible
        'AverageType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=2),  # Average type
    }

