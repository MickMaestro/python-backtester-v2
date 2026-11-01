"""iTrend ADXVMA — converted from MQL5: MQL5 Indicators/iTrend ADXVMA/iTrend ADXVMA.mq5

iTrendd ADXVMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 8}, 'colors': {1: [3329330, 3329330], 2: [9639167, 9639167], 3: [11119017], 4: [11119017], 5: [11119017, 65280, 11823615]}, 'widths': {3: 2, 4: 2, 5: 2}, 'styles': {5: 0}, 'labels': {1: 'iTrend up', 2: 'iTrend down', 3: 'iTrend line up', 4: 'iTrend line down', 5: 'iTrend'}, 'levels': [], 'description': ['iTrendd ADXVMA'], 'name': 'iTrend ADXVMA', 'source': 'MQL5 Indicators/iTrend ADXVMA/iTrend ADXVMA.mq5', 'folder': 'iTrend ADXVMA', 'inputs': [{'mql': 'ItPeriod', 'py': 'ItPeriod', 'param': 'ItPeriod', 'type': 'int', 'default': 14, 'label': 'iTrend period', 'sinput': False}, {'mql': 'ItPrice', 'py': 'ItPrice', 'param': 'ItPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'LevelBars', 'py': 'LevelBars', 'param': 'LevelBars', 'type': 'int', 'default': 300, 'label': 'Look back period for levels', 'sinput': False}, {'mql': 'LevelFactor', 'py': 'LevelFactor', 'param': 'LevelFactor', 'type': 'double', 'default': 0.283, 'label': 'Levels factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ItPeriod = _input('ItPeriod', 14)  # iTrend period
ItPrice = _input('ItPrice', PRICE_CLOSE)  # Price
LevelBars = _input('LevelBars', 300)  # Look back period for levels
LevelFactor = _input('LevelFactor', 0.283)  # Levels factor
itrend = Arr(0, 0.0)
itrendc = Arr(0, 0.0)
lup = Arr(0, 0.0)
ldn = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filluz = Arr(0, 0.0)
filld = Arr(0, 0.0)
filldz = Arr(0, 0.0)
adxvmaWork = Arr(0, 0.0, dims=(7,))

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filluz, INDICATOR_DATA)
    SetIndexBuffer(2, filld, INDICATOR_DATA)
    SetIndexBuffer(3, filldz, INDICATOR_DATA)
    SetIndexBuffer(4, lup, INDICATOR_DATA)
    SetIndexBuffer(5, ldn, INDICATOR_DATA)
    SetIndexBuffer(6, itrend, INDICATOR_DATA)
    SetIndexBuffer(7, itrendc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'iTrend ADXVMA (' + _str(ItPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        ma = getPrice(ItPrice, open, close, high, low, i, rates_total)
        mv = iAdxvma(ma, ItPeriod, i, rates_total, 0)
        fillu[i] = ma - mv
        lup[i] = fillu[i]
        filluz[i] = 0.0
        filld[i] = -(low[i] + high[i] - (2 * mv))
        ldn[i] = filld[i]
        filldz[i] = 0.0
        hi = MathMax(fillu[i], filld[i])
        k = 1
        while k < LevelBars and (i - k) >= 0:
            hi = MathMax(hi, MathMax(fillu[i - k], filld[i - k]))
            k += 1
        itrend[i] = hi * LevelFactor
        itrendc[i] = (1 if (fillu[i] > itrend[i]) else 2 if (filld[i] > itrend[i]) else itrendc[i - 1] if (i > 0) else 0)
    return rates_total

def iAdxvma(price, period, r, bars, instanceNo=0):
    if ArrayRange(adxvmaWork, 0) != bars:
        ArrayResize(adxvmaWork, bars)
    instanceNo *= 7
    adxvmaWork[r][instanceNo + 0] = price
    if r < 1:
        adxvmaWork[r][instanceNo + 6] = adxvmaWork[r][instanceNo + 0]
        return adxvmaWork[r][6]
    tpdm = 0.0
    tmdm = 0.0
    diff = adxvmaWork[r][instanceNo + 0] - adxvmaWork[r - 1][instanceNo + 0]
    if diff > 0:
        tpdm = diff
    else:
        tmdm = -diff
    adxvmaWork[r][instanceNo + 1] = _fdiv(((period - 1.0) * adxvmaWork[r - 1][instanceNo + 1]) + tpdm, period)
    adxvmaWork[r][instanceNo + 2] = _fdiv(((period - 1.0) * adxvmaWork[r - 1][instanceNo + 2]) + tmdm, period)
    trueRange = adxvmaWork[r][instanceNo + 1] + adxvmaWork[r][instanceNo + 2]
    tpdi = 0.0
    tmdi = 0.0
    if trueRange > 0:
        tpdi = _fdiv(adxvmaWork[r][instanceNo + 1], trueRange)
        tmdi = _fdiv(adxvmaWork[r][instanceNo + 2], trueRange)
    adxvmaWork[r][instanceNo + 3] = _fdiv(((period - 1.0) * adxvmaWork[r - 1][instanceNo + 3]) + tpdi, period)
    adxvmaWork[r][instanceNo + 4] = _fdiv(((period - 1.0) * adxvmaWork[r - 1][instanceNo + 4]) + tmdi, period)
    tout = 0.0
    if (adxvmaWork[r][instanceNo + 3] + adxvmaWork[r][instanceNo + 4]) > 0:
        tout = _fdiv(MathAbs(adxvmaWork[r][instanceNo + 3] - adxvmaWork[r][instanceNo + 4]), adxvmaWork[r][instanceNo + 3] + adxvmaWork[r][instanceNo + 4])
    adxvmaWork[r][instanceNo + 5] = _fdiv(((period - 1.0) * adxvmaWork[r - 1][instanceNo + 5]) + tout, period)
    thi = MathMax(adxvmaWork[r][instanceNo + 5], adxvmaWork[r - 1][instanceNo + 5])
    tlo = MathMin(adxvmaWork[r][instanceNo + 5], adxvmaWork[r - 1][instanceNo + 5])
    j = 2
    while j < _int(period) and (r - j) >= 0:
        thi = MathMax(adxvmaWork[r - j][instanceNo + 5], thi)
        tlo = MathMin(adxvmaWork[r - j][instanceNo + 5], tlo)
        j += 1
    vi = 0.0
    if (thi - tlo) > 0:
        vi = _fdiv(adxvmaWork[r][instanceNo + 5] - tlo, thi - tlo)
    adxvmaWork[r][instanceNo + 6] = _fdiv(((period - vi) * adxvmaWork[r - 1][instanceNo + 6]) + (vi * adxvmaWork[r][instanceNo + 0]), period)
    return adxvmaWork[r][instanceNo + 6]

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw1 = tprice
        if _sw1 == PRICE_CLOSE:
            return close[i]
        elif _sw1 == PRICE_OPEN:
            return open[i]
        elif _sw1 == PRICE_HIGH:
            return high[i]
        elif _sw1 == PRICE_LOW:
            return low[i]
        elif _sw1 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ITrendADXVMA(_MQL5Indicator):
    name = 'iTrend ADXVMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ItPeriod': 14,  # iTrend period
        'ItPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'LevelBars': 300,  # Look back period for levels
        'LevelFactor': 0.283,  # Levels factor
    }

