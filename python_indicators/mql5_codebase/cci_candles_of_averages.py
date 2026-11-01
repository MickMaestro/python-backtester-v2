"""CCI candles - of averages — converted from MQL5: MQL5 Indicators/CCI Candles of Averages/CCI candles - of averages.mq5

CCI candles (of smoothed prices)
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421504, 16748574, 6333684]}, 'widths': {}, 'styles': {}, 'labels': {1: 'cci'}, 'levels': [], 'description': ['CCI candles (of smoothed prices)'], 'name': 'CCI candles - of averages', 'source': 'MQL5 Indicators/CCI Candles of Averages/CCI candles - of averages.mq5', 'folder': 'CCI Candles of Averages', 'inputs': [{'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 32, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpSmtPeriod', 'py': 'inpSmtPeriod', 'param': 'inpSmtPeriod', 'type': 'int', 'default': 14, 'label': 'Smoothing period (<=1 for no smoothing)', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpCciPeriod = _input('inpCciPeriod', 32)  # CCI period
inpSmtPeriod = _input('inpSmtPeriod', 14)  # Smoothing period (<=1 for no smoothing)
inpMaMethod = _input('inpMaMethod', ma_sma)  # Smoothing method
ccio = Arr(0, 0.0)
ccih = Arr(0, 0.0)
ccil = Arr(0, 0.0)
ccic = Arr(0, 0.0)
ccicl = Arr(0, 0.0)
savgh = Arr(0, 0.0)
savgl = Arr(0, 0.0)
savgo = Arr(0, 0.0)
savgc = Arr(0, 0.0)
_avgNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
workSma = Arr(0, 0.0, dims=(4,))
workEma = Arr(0, 0.0, dims=(4,))
workSmma = Arr(0, 0.0, dims=(4,))
workLwma = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, ccio, INDICATOR_DATA)
    SetIndexBuffer(1, ccih, INDICATOR_DATA)
    SetIndexBuffer(2, ccil, INDICATOR_DATA)
    SetIndexBuffer(3, ccic, INDICATOR_DATA)
    SetIndexBuffer(4, ccicl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, savgo, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, savgh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, savgl, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, savgc, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI candles (' + _str(inpCciPeriod) + ')(' + _str(inpSmtPeriod) + ' ' + _avgNames[inpMaMethod] + ' smoothed)')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    _cci = Arr(4, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        savgh[i] = iCustomMa(inpMaMethod, high[i], inpSmtPeriod, i, rates_total, 0)
        savgl[i] = iCustomMa(inpMaMethod, low[i], inpSmtPeriod, i, rates_total, 1)
        savgo[i] = iCustomMa(inpMaMethod, open[i], inpSmtPeriod, i, rates_total, 2)
        savgc[i] = iCustomMa(inpMaMethod, close[i], inpSmtPeriod, i, rates_total, 3)
        avgh = 0.0
        avgl = 0.0
        avgo = 0.0
        avgc = 0.0
        k = 0
        while k < inpCciPeriod and (i - k) >= 0:
            avgh += savgh[i - k]
            avgl += savgl[i - k]
            avgo += savgo[i - k]
            avgc += savgc[i - k]
            k += 1
        avgh = avgh / inpCciPeriod
        avgl = avgl / inpCciPeriod
        avgo = avgo / inpCciPeriod
        avgc = avgc / inpCciPeriod
        devh = 0.0
        devl = 0.0
        devo = 0.0
        devc = 0.0
        k = 0
        while k < inpCciPeriod and (i - k) >= 0:
            devh += MathAbs(savgh[i - k] - avgh)
            devl += MathAbs(savgl[i - k] - avgl)
            devo += MathAbs(savgo[i - k] - avgo)
            devc += MathAbs(savgc[i - k] - avgc)
            k += 1
        devh = devh / inpCciPeriod
        devl = devl / inpCciPeriod
        devo = devo / inpCciPeriod
        devc = devc / inpCciPeriod
        _cci[0] = (_fdiv(savgh[i] - avgh, 0.015 * devh) if (devh != 0) else 0)
        _cci[1] = (_fdiv(savgl[i] - avgl, 0.015 * devl) if (devl != 0) else 0)
        _cci[2] = (_fdiv(savgo[i] - avgo, 0.015 * devo) if (devo != 0) else 0)
        _cci[3] = (_fdiv(savgc[i] - avgc, 0.015 * devc) if (devc != 0) else 0)
        ccio[i] = _cci[2]
        ccic[i] = _cci[3]
        ccih[i] = _cci[ArrayMaximum(_cci, 0, 4)]
        ccil[i] = _cci[ArrayMinimum(_cci, 0, 4)]
        ccicl[i] = (1 if (ccic[i] > ccio[i]) else 2 if (ccic[i] < ccio[i]) else 0)
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


class CCICandlesOfAverages(_MQL5Indicator):
    name = 'CCI candles - of averages'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCciPeriod': 32,  # CCI period
        'inpSmtPeriod': 14,  # Smoothing period (<=1 for no smoothing)
        'inpMaMethod': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Smoothing method
    }

