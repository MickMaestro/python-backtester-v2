"""Smoother momentum stops — converted from MQL5: MQL5 Indicators/Smoother Momentum Stops/Smoother momentum stops.mq5

Smoother momentum stops
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 5, 3: 1, 4: 5}, 'colors': {1: [15453831], 2: [15453831], 3: [17919], 4: [17919]}, 'widths': {1: 2, 2: 1, 3: 2, 4: 1}, 'styles': {}, 'labels': {1: 'Smoother momentum support', 2: 'Smoother momentum support signal', 3: 'Smoother momentum resistance', 4: 'Smoother momentum resistance signal'}, 'levels': [], 'description': ['Smoother momentum stops'], 'name': 'Smoother momentum stops', 'source': 'MQL5 Indicators/Smoother Momentum Stops/Smoother momentum stops.mq5', 'folder': 'Smoother Momentum Stops', 'inputs': [{'mql': 'inpMomPeriod', 'py': 'inpMomPeriod', 'param': 'inpMomPeriod', 'type': 'int', 'default': 20, 'label': 'Momentum period', 'sinput': False}, {'mql': 'inpAvgPeriod', 'py': 'inpAvgPeriod', 'param': 'inpAvgPeriod', 'type': 'int', 'default': 20, 'label': 'Average period', 'sinput': False}, {'mql': 'inpAvgMethod', 'py': 'inpAvgMethod', 'param': 'inpAvgMethod', 'type': 'int', 'default': 0, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpMultiplier', 'py': 'inpMultiplier', 'param': 'inpMultiplier', 'type': 'double', 'default': 1.5, 'label': 'Stops distance', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMomPeriod = _input('inpMomPeriod', 20)  # Momentum period
inpAvgPeriod = _input('inpAvgPeriod', 20)  # Average period
inpAvgMethod = _input('inpAvgMethod', MODE_SMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpMultiplier = _input('inpMultiplier', 1.5)  # Stops distance
stopu = Arr(0, 0.0)
stopua = Arr(0, 0.0)
stopd = Arr(0, 0.0)
stopda = Arr(0, 0.0)
_maHandle = 0
_avgVal = Arr(1, 0.0, dyn=False)
workSmom = Arr(0, 0.0, dims=(3,))

def OnInit():
    global _maHandle
    SetIndexBuffer(0, stopu, INDICATOR_DATA)
    SetIndexBuffer(1, stopua, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    SetIndexBuffer(2, stopd, INDICATOR_DATA)
    SetIndexBuffer(3, stopda, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    _maHandle = iMA(Symbol(), 0, inpAvgPeriod, 0, inpAvgMethod, inpPrice)
    if _maHandle == INVALID_HANDLE:
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoother momentum stops(' + _str(inpMomPeriod) + ',' + _str(inpMomPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_maHandle) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _avgCopied = CopyBuffer(_maHandle, 0, _DT(time[i]), 1, _avgVal)
        _avg = (_avgVal[0] if (_avgCopied == 1) else 0)
        _mom = inpMultiplier * iSmoothMomentum(getPrice(inpPrice, open, close, high, low, i, rates_total), inpMomPeriod, i, rates_total)
        if _mom > 0:
            stopu[i] = (((_avg - _mom) if (stopu[i - 1] == EMPTY_VALUE) else MathMax(stopu[i - 1], _avg - _mom)) if (i > 0) else (_avg - _mom))
            stopd[i] = EMPTY_VALUE
            stopda[i] = EMPTY_VALUE
            stopua[i] = ((stopu[i] if (stopu[i - 1] == EMPTY_VALUE) else EMPTY_VALUE) if (i > 0) else EMPTY_VALUE)
        if _mom < 0:
            stopd[i] = (((_avg - _mom) if (stopd[i - 1] == EMPTY_VALUE) else MathMin(stopd[i - 1], _avg - _mom)) if (i > 0) else (_avg - _mom))
            stopu[i] = EMPTY_VALUE
            stopua[i] = EMPTY_VALUE
            stopda[i] = ((stopd[i] if (stopd[i - 1] == EMPTY_VALUE) else EMPTY_VALUE) if (i > 0) else EMPTY_VALUE)
        i += 1
    return i

def iSmoothMomentum(price, period, r, bars, instanceNo=0):
    if ArrayRange(workSmom, 0) != bars:
        ArrayResize(workSmom, bars)
    instanceNo *= 3
    workSmom[r][0 + instanceNo] = price
    workSmom[r][1 + instanceNo] = price
    workSmom[r][2 + instanceNo] = price
    if r > 0:
        alphar = _fdiv(2.0, 1.0 + period)
        alphad = _fdiv(2.0, 1.0 + MathSqrt(period))
        workSmom[r][0 + instanceNo] = workSmom[r - 1][0 + instanceNo] + (alphar * (price - workSmom[r - 1][0 + instanceNo]))
        workSmom[r][1 + instanceNo] = workSmom[r - 1][1 + instanceNo] + (alphad * (price - workSmom[r - 1][1 + instanceNo]))
        workSmom[r][2 + instanceNo] = workSmom[r - 1][2 + instanceNo] + (alphad * (workSmom[r][1 + instanceNo] - workSmom[r - 1][2 + instanceNo]))
    return workSmom[r][2 + instanceNo] - workSmom[r][0 + instanceNo]

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


class SmootherMomentumStops(_MQL5Indicator):
    name = 'Smoother momentum stops'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMomPeriod': 20,  # Momentum period
        'inpAvgPeriod': 20,  # Average period
        'inpAvgMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpMultiplier': 1.5,  # Stops distance
    }

