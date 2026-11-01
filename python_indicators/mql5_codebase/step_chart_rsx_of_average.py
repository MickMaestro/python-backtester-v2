"""Step chart - rsx of average — converted from MQL5: MQL5 Indicators/Step chart of RSX of average/Step chart - rsx of average.mq5

Step chart of RSX of averages
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 11}, 'colors': {1: [11119017], 2: [11119017, 16748574, 6333684]}, 'widths': {2: 2}, 'styles': {1: 2}, 'labels': {1: 'RSX of average', 2: 'Step chart'}, 'levels': [], 'description': ['Step chart of RSX of averages'], 'name': 'Step chart - rsx of average', 'source': 'MQL5 Indicators/Step chart of RSX of average/Step chart - rsx of average.mq5', 'folder': 'Step chart of RSX of average', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSX period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpAvgPeriod', 'py': 'inpAvgPeriod', 'param': 'inpAvgPeriod', 'type': 'int', 'default': 14, 'label': 'Average period (<=1 for no average)', 'sinput': False}, {'mql': 'inpMaType', 'py': 'inpMaType', 'param': 'inpMaType', 'type': 'int', 'default': 0, 'label': 'Average type', 'sinput': False}, {'mql': 'inpStepSize', 'py': 'inpStepSize', 'param': 'inpStepSize', 'type': 'double', 'default': 5.0, 'label': 'Step size (in RSX %)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMaTypes
ma_sma = 0
ma_ema = 1
ma_smma = 2
ma_lwma = 3
_enum('enMaTypes', {0: 'ma_sma', 1: 'ma_ema', 2: 'ma_smma', 3: 'ma_lwma'})

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSX period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpAvgPeriod = _input('inpAvgPeriod', 14)  # Average period (<=1 for no average)
inpMaType = _input('inpMaType', ma_sma)  # Average type
inpStepSize = _input('inpStepSize', 5.0)  # Step size (in RSX %)
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
barc = Arr(0, 0.0)
val = Arr(0, 0.0)
_avgName = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
workSma = Arr(0, 0.0, dims=(1,))
workEma = Arr(0, 0.0, dims=(1,))
workSmma = Arr(0, 0.0, dims=(1,))
workLwma = Arr(0, 0.0, dims=(1,))
workRsi = Arr(5, 0.0, dyn=False, dims=(13,))
_stepChartWork = Arr(5, 0.0, dyn=False, dims=(2,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, barh, INDICATOR_DATA)
    SetIndexBuffer(2, barl, INDICATOR_DATA)
    SetIndexBuffer(3, barc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Step chart (' + _str(inpRsiPeriod) + ') RSX' + ((' of (' + _str(inpAvgPeriod) + ' ' + _avgName[inpMaType]) if (inpAvgPeriod > 1) else '') + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        val[i] = iRsx(iCustomMa(inpMaType, getPrice(inpPrice, open, close, high, low, i, rates_total), inpAvgPeriod, i, rates_total), inpRsiPeriod, i)
        rbarh = Box(0.0)
        rbarl = Box(0.0)
        rtrend = Box(0.0)
        iStepChart(val[i], inpStepSize, rbarh, rbarl, rtrend, i)
        barh[i] = rbarh.v
        barl[i] = ((rbarh.v - 1) if (rbarh.v == rbarl.v) else rbarl.v)
        barc[i] = (1 if (rtrend.v == 1) else 2)
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
    k = 1
    workSma[r][instanceNo + 0] = price
    avg = price
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
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

def iRsx(price, period, i, instance=0):
    _indP = _int(MathMod(i - 1, 5))
    _indC = _int(MathMod(i, 5))
    _inst = instance * 13
    workRsi[_indC][_inst] = price
    if i < period:
        for k in range(1, 13):
            workRsi[_indC][_inst + k] = 0.0
        return 50.0
    Kg = _fdiv(3.0, 2.0 + period)
    Hg = 1.0 - Kg
    mom = workRsi[_indC][_inst] - workRsi[_indP][_inst]
    moa = MathAbs(mom)
    for k in range(0, 3):
        kk = _inst + (k * 2)
        workRsi[_indC][kk + 1] = (Kg * mom) + (Hg * workRsi[_indP][kk + 1])
        workRsi[_indC][kk + 2] = (Kg * workRsi[_indC][kk + 1]) + (Hg * workRsi[_indP][kk + 2])
        mom = (1.5 * workRsi[_indC][kk + 1]) - (0.5 * workRsi[_indC][kk + 2])
        workRsi[_indC][kk + 7] = (Kg * moa) + (Hg * workRsi[_indP][kk + 7])
        workRsi[_indC][kk + 8] = (Kg * workRsi[_indC][kk + 7]) + (Hg * workRsi[_indP][kk + 8])
        moa = (1.5 * workRsi[_indC][kk + 7]) - (0.5 * workRsi[_indC][kk + 8])
    return MathMax(MathMin((_fdiv(mom, MathMax(moa, DBL_MIN)) + 1.0) * 50.0, 100.0), 0.0)

def iStepChart(value, stepSize, rbarh, rbarl, rtrend, i, instance=0):
    _indP = _int(MathMod(i - 1, 5))
    _indC = _int(MathMod(i, 5))
    _inst = instance * 2
    if i == 0:
        rbarl.v = ((MathRound(_fdiv(value, stepSize)) * stepSize) if (stepSize > 0) else value)
        rbarh.v = rbarl.v
        _stepChartWork[_indC][_inst + 0] = rbarh.v
        rtrend.v = 0.0
        _stepChartWork[_indC][_inst + 1] = rtrend.v
    else:
        if MathAbs(value - _stepChartWork[_indP][_inst + 0]) < stepSize:
            _stepChartWork[_indC][_inst + 0] = _stepChartWork[_indP][_inst + 0]
        else:
            _stepChartWork[_indC][_inst + 0] = _stepChartWork[_indP][_inst + 0]
            while MathAbs(value - _stepChartWork[_indC][_inst + 0]) > stepSize:
                if value > _stepChartWork[_indC][_inst + 0]:
                    _stepChartWork[_indC][_inst + 0] += stepSize
                if value < _stepChartWork[_indC][_inst + 0]:
                    _stepChartWork[_indC][_inst + 0] -= stepSize
        _stepChartWork[_indC][_inst + 1] = (1 if (_stepChartWork[_indC][_inst + 0] > _stepChartWork[_indP][_inst + 0]) else -1 if (_stepChartWork[_indC][_inst + 0] < _stepChartWork[_indP][_inst + 0]) else _stepChartWork[_indP][_inst + 1])
        rbarh.v = _stepChartWork[_indC][_inst + 0]
        rbarl.v = _stepChartWork[_indP][_inst + 0]
        rtrend.v = _stepChartWork[_indC][_inst + 1]

def getPrice(tprice, open, close, high, low, i, _bars):
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


class StepChartRsxOfAverage(_MQL5Indicator):
    name = 'Step chart - rsx of average'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSX period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpAvgPeriod': 14,  # Average period (<=1 for no average)
        'inpMaType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed MA', 3: 'Linear weighted MA'}, default=0),  # Average type
        'inpStepSize': 5.0,  # Step size (in RSX %)
    }

