"""RSI with RSI — converted from MQL5: MQL5 Indicators/RSI with RSI/RSI with RSI.mq5

RSI with RSI
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16760576], 2: [16760576], 3: [6333684], 4: [6333684]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {}, 'labels': {1: 'Signal up', 2: 'Signal up 2', 3: 'Signal down', 4: 'Signal down 2'}, 'levels': [], 'description': ['RSI with RSI'], 'name': 'RSI with RSI', 'source': 'MQL5 Indicators/RSI with RSI/RSI with RSI.mq5', 'folder': 'RSI with RSI', 'inputs': [{'mql': 'inpRsiPeriodShort', 'py': 'inpRsiPeriodShort', 'param': 'inpRsiPeriodShort', 'type': 'int', 'default': 5, 'label': 'RSI short period', 'sinput': False}, {'mql': 'inpRsiPeriodLong', 'py': 'inpRsiPeriodLong', 'param': 'inpRsiPeriodLong', 'type': 'int', 'default': 17, 'label': 'RSI long period', 'sinput': False}, {'mql': 'inpRsiLevelUp', 'py': 'inpRsiLevelUp', 'param': 'inpRsiLevelUp', 'type': 'double', 'default': 60.0, 'label': 'RSI level up', 'sinput': False}, {'mql': 'inpRsiLevelDown', 'py': 'inpRsiLevelDown', 'param': 'inpRsiLevelDown', 'type': 'double', 'default': 40.0, 'label': 'RSI level down', 'sinput': False}, {'mql': 'inpMaPeriodShort', 'py': 'inpMaPeriodShort', 'param': 'inpMaPeriodShort', 'type': 'int', 'default': 10, 'label': 'Short MA period', 'sinput': False}, {'mql': 'inpMaPeriodLong', 'py': 'inpMaPeriodLong', 'param': 'inpMaPeriodLong', 'type': 'int', 'default': 40, 'label': 'Long MA period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriodShort = _input('inpRsiPeriodShort', 5)  # RSI short period
inpRsiPeriodLong = _input('inpRsiPeriodLong', 17)  # RSI long period
inpRsiLevelUp = _input('inpRsiLevelUp', 60.0)  # RSI level up
inpRsiLevelDown = _input('inpRsiLevelDown', 40.0)  # RSI level down
inpMaPeriodShort = _input('inpMaPeriodShort', 10)  # Short MA period
inpMaPeriodLong = _input('inpMaPeriodLong', 40)  # Long MA period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
arru1 = Arr(0, 0.0)
arru2 = Arr(0, 0.0)
arrd1 = Arr(0, 0.0)
arrd2 = Arr(0, 0.0)
trend1 = Arr(0, 0.0)
trend2 = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(6,))
workSma = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, arru1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    SetIndexBuffer(1, arru2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 251)
    SetIndexBuffer(2, arrd1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    SetIndexBuffer(3, arrd2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_ARROW, 251)
    SetIndexBuffer(4, trend1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, trend2, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        range_ = 0.0
        k = 0
        while k < 10 and (i - k - 1) >= 0:
            range_ += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
            k += 1
        range_ = range_ / 10
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        rsiShort = iRsi(price, inpRsiPeriodShort, i, rates_total, 0)
        rsiLong = iRsi(price, inpRsiPeriodLong, i, rates_total, 1)
        maShort = iSma(price, inpMaPeriodShort, i, rates_total, 0)
        maLong = iSma(price, inpMaPeriodLong, i, rates_total, 1)
        trend1[i] = (1 if (rsiShort > inpRsiLevelUp) else -1 if (rsiShort < inpRsiLevelDown) else trend1[i - 1] if (i > 0) else 0)
        trend2[i] = (1 if (rsiLong > inpRsiLevelUp) else -1 if (rsiLong < inpRsiLevelDown) else trend2[i - 1] if (i > 0) else 0)
        arru1[i] = (((low[i] - range_) if (((trend1[i] != trend1[i - 1] and trend1[i] == 1) and price > maShort) and trend2[i] == -1) else EMPTY_VALUE) if (i > 0) else EMPTY_VALUE)
        arru2[i] = (((low[i] - (range_ * 2.0)) if ((trend2[i] != trend2[i - 1] and trend2[i] == 1) and price > maLong) else EMPTY_VALUE) if (i > 0) else EMPTY_VALUE)
        arrd1[i] = (((high[i] + range_) if (((trend1[i] != trend1[i - 1] and trend1[i] == -1) and price < maShort) and trend2[i] == 1) else EMPTY_VALUE) if (i > 0) else EMPTY_VALUE)
        arrd2[i] = (((high[i] + (range_ * 2.0)) if ((trend2[i] != trend2[i - 1] and trend2[i] == -1) and price < maLong) else EMPTY_VALUE) if (i > 0) else EMPTY_VALUE)
        i += 1
    return i

def iRsi(price, period, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 3
    workRsi[r][z + 0] = price
    alpha = _fdiv(1.0, MathMax(period, 1))
    if r < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and (r - k - 1) >= 0:
            sum_ += MathAbs(workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0])
            k += 1
        workRsi[r][z + 1] = _fdiv(workRsi[r][z + 0] - workRsi[0][z + 0], MathMax(k, 1))
        workRsi[r][z + 2] = _fdiv(sum_, MathMax(k, 1))
    else:
        change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
        workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
        workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
    return 50.0 * (_fdiv(workRsi[r][z + 1], MathMax(workRsi[r][z + 2], DBL_MIN)) + 1)

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo + 0] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo + 0]
        k += 1
    return _fdiv(avg, float(k))

def getPrice(tprice, open, close, high, low, i, _bars):
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


class RSIWithRSI(_MQL5Indicator):
    name = 'RSI with RSI'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriodShort': 5,  # RSI short period
        'inpRsiPeriodLong': 17,  # RSI long period
        'inpRsiLevelUp': 60.0,  # RSI level up
        'inpRsiLevelDown': 40.0,  # RSI level down
        'inpMaPeriodShort': 10,  # Short MA period
        'inpMaPeriodLong': 40,  # Long MA period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

