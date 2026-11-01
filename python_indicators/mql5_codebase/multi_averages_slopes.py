"""Multi averages slopes — converted from MQL5: MQL5 Indicators/Multi Averages Slopes/Multi averages slopes.mq5

Multi averages slopes
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [3329330], 2: [3937500]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Multi averages slopes up', 2: 'Multi averages slopes down'}, 'levels': [], 'description': ['Multi averages slopes'], 'name': 'Multi averages slopes', 'source': 'MQL5 Indicators/Multi Averages Slopes/Multi averages slopes.mq5', 'folder': 'Multi Averages Slopes', 'inputs': [{'mql': 'inpMaType', 'py': 'inpMaType', 'param': 'inpMaType', 'type': 'int', 'default': 1, 'label': 'Averages types', 'sinput': False}, {'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'int', 'default': 8, 'label': 'Period 1', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 11, 'label': 'Period 2', 'sinput': False}, {'mql': 'inpPeriod3', 'py': 'inpPeriod3', 'param': 'inpPeriod3', 'type': 'int', 'default': 14, 'label': 'Period 3', 'sinput': False}, {'mql': 'inpPeriod4', 'py': 'inpPeriod4', 'param': 'inpPeriod4', 'type': 'int', 'default': 17, 'label': 'Period 4', 'sinput': False}, {'mql': 'inpPeriod5', 'py': 'inpPeriod5', 'param': 'inpPeriod5', 'type': 'int', 'default': 20, 'label': 'Period 5', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpMaType = _input('inpMaType', ma_ema)  # Averages types
inpPeriod1 = _input('inpPeriod1', 8)  # Period 1
inpPeriod2 = _input('inpPeriod2', 11)  # Period 2
inpPeriod3 = _input('inpPeriod3', 14)  # Period 3
inpPeriod4 = _input('inpPeriod4', 17)  # Period 4
inpPeriod5 = _input('inpPeriod5', 20)  # Period 5
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
histou = Arr(0, 0.0)
histod = Arr(0, 0.0)
averages = Arr(0, 0.0, dims=(5,))
_averageNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
workSma = Arr(0, 0.0, dims=(5,))
workEma = Arr(0, 0.0, dims=(5,))
workSmma = Arr(0, 0.0, dims=(5,))
workLwma = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, histou, INDICATOR_DATA)
    SetIndexBuffer(1, histod, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Multi ' + _averageNames[inpMaType] + ' slopes (' + _str(inpPeriod1) + ',' + _str(inpPeriod2) + ',' + _str(inpPeriod3) + ',' + _str(inpPeriod4) + ',' + _str(inpPeriod5) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if ArrayRange(averages, 0) != rates_total:
        ArrayResize(averages, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        averages[i][0] = iCustomMa(inpMaType, _price, inpPeriod1, i, rates_total, 0)
        averages[i][1] = iCustomMa(inpMaType, _price, inpPeriod2, i, rates_total, 1)
        averages[i][2] = iCustomMa(inpMaType, _price, inpPeriod3, i, rates_total, 2)
        averages[i][3] = iCustomMa(inpMaType, _price, inpPeriod4, i, rates_total, 3)
        averages[i][4] = iCustomMa(inpMaType, _price, inpPeriod5, i, rates_total, 4)
        histod[i] = 0.0
        histou[i] = histod[i]
        if i > 0:
            if averages[i][0] > averages[i - 1][0]:
                histou[i] += 1
            if averages[i][0] < averages[i - 1][0]:
                histod[i] -= 1
            if averages[i][1] > averages[i - 1][1]:
                histou[i] += 1
            if averages[i][1] < averages[i - 1][1]:
                histod[i] -= 1
            if averages[i][2] > averages[i - 1][2]:
                histou[i] += 1
            if averages[i][2] < averages[i - 1][2]:
                histod[i] -= 1
            if averages[i][3] > averages[i - 1][3]:
                histou[i] += 1
            if averages[i][3] < averages[i - 1][3]:
                histod[i] -= 1
            if averages[i][4] > averages[i - 1][4]:
                histou[i] += 1
            if averages[i][4] < averages[i - 1][4]:
                histod[i] -= 1
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
    k = 0
    workSma[r][instanceNo + 0] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    return _fdiv(avg, k)

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
    if period <= 1:
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

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiAveragesSlopes(_MQL5Indicator):
    name = 'Multi averages slopes'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMaType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=1),  # Averages types
        'inpPeriod1': 8,  # Period 1
        'inpPeriod2': 11,  # Period 2
        'inpPeriod3': 14,  # Period 3
        'inpPeriod4': 17,  # Period 4
        'inpPeriod5': 20,  # Period 5
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

