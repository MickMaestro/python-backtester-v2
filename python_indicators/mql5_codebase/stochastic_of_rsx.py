"""stochastic_of_rsx — converted from MQL5: MQL5 Indicators/Stochastic of RSX/stochastic_of_rsx.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Stochastic of RSX'}, 'levels': [10.0, 90.0, 100.0], 'description': [], 'name': 'stochastic_of_rsx', 'source': 'MQL5 Indicators/Stochastic of RSX/stochastic_of_rsx.mq5', 'folder': 'Stochastic of RSX', 'inputs': [{'mql': 'StochasticPeriod', 'py': 'StochasticPeriod', 'param': 'StochasticPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'StochasticSlowing', 'py': 'StochasticSlowing', 'param': 'StochasticSlowing', 'type': 'int', 'default': 9, 'label': 'Stochastic slowing period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'RsxPeriod', 'py': 'RsxPeriod', 'param': 'RsxPeriod', 'type': 'double', 'default': 32.0, 'label': 'Rsx period', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 17919, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Color Up', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average'})

# ---- inputs and global variables
StochasticPeriod = _input('StochasticPeriod', 32)  # Stochastic period
StochasticSlowing = _input('StochasticSlowing', 9)  # Stochastic slowing period
Price = _input('Price', pr_close)  # Price to use
RsxPeriod = _input('RsxPeriod', 32.0)  # Rsx period
ColorFrom = _input('ColorFrom', clrOrangeRed)  # Color down
ColorTo = _input('ColorTo', clrLimeGreen)  # Color Up
sto = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
cSteps = 0
wrkBuffer = Arr(0, 0.0, dims=(13,))
workSto = Arr(0, 0.0, dims=(5,))

def OnInit():
    global cSteps
    SetIndexBuffer(0, sto, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    cSteps = (StochasticPeriod if (StochasticPeriod > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if ArrayRange(wrkBuffer, 0) != rates_total:
        ArrayResize(wrkBuffer, rates_total)
    Kg = _fdiv(3.0, 2.0 + RsxPeriod)
    Hg = 1.0 - Kg
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        for c in range(0, 12):
            wrkBuffer[i][c] = 0.0
        wrkBuffer[i][12] = getPrice(Price, open, close, high, low, rates_total, i)
        roc = ((wrkBuffer[i][12] - wrkBuffer[i - 1][12]) if (i > 0) else 0)
        roa = MathAbs(roc)
        if i > 0:
            for k in range(0, 3):
                kk = k * 2
                wrkBuffer[i][kk + 0] = (Kg * roc) + (Hg * wrkBuffer[i - 1][kk + 0])
                wrkBuffer[i][kk + 1] = (Kg * wrkBuffer[i][kk + 0]) + (Hg * wrkBuffer[i - 1][kk + 1])
                roc = (1.5 * wrkBuffer[i][kk + 0]) - (0.5 * wrkBuffer[i][kk + 1])
                wrkBuffer[i][kk + 6] = (Kg * roa) + (Hg * wrkBuffer[i - 1][kk + 6])
                wrkBuffer[i][kk + 7] = (Kg * wrkBuffer[i][kk + 6]) + (Hg * wrkBuffer[i - 1][kk + 7])
                roa = (1.5 * wrkBuffer[i][kk + 6]) - (0.5 * wrkBuffer[i][kk + 7])
        rsi = (MathMax(MathMin((_fdiv(roc, roa) + 1.0) * 50.0, 100.0), 0.0) if (roa != 0) else 0)
        sto[i] = iStoch(rsi, rsi, rsi, StochasticPeriod, StochasticSlowing, rates_total, i)
        colorBuffer[i] = MathFloor((sto[i] * cSteps) / 100.0)
    return rates_total

def iStoch(priceR, priceH, priceL, period, slowing, bars, i, instanceNo=0):
    if ArrayRange(workSto, 0) != bars:
        ArrayResize(workSto, bars)
    instanceNo *= 5
    workSto[i][0 + instanceNo] = priceH
    workSto[i][1 + instanceNo] = priceL
    workSto[i][2 + instanceNo] = priceR
    workSto[i][3 + instanceNo] = priceH
    workSto[i][4 + instanceNo] = priceL
    k = 1
    while k < period and (i - k) >= 0:
        workSto[i][4 + instanceNo] = MathMin(workSto[i][4 + instanceNo], workSto[i - k][instanceNo + 1])
        workSto[i][3 + instanceNo] = MathMax(workSto[i][3 + instanceNo], workSto[i - k][instanceNo + 0])
        k += 1
    sumlow = 0.0
    sumhigh = 0.0
    k = 0
    while k < slowing and (i - k) >= 0:
        sumlow += workSto[i - k][2 + instanceNo] - workSto[i - k][4 + instanceNo]
        sumhigh += workSto[i - k][3 + instanceNo] - workSto[i - k][4 + instanceNo]
        k += 1
    if sumhigh != 0.0:
        return _fdiv(100.0 * sumlow, sumhigh)
    else:
        return 0.0

def getPrice(price, open, close, high, low, bars, i):
    _sw1 = price
    if _sw1 == pr_close:
        return close[i]
    elif _sw1 == pr_open:
        return open[i]
    elif _sw1 == pr_high:
        return high[i]
    elif _sw1 == pr_low:
        return low[i]
    elif _sw1 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw1 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    return 0.0

def getColor(stepNo, totalSteps, from_, to):
    stes = float(totalSteps) - 1.0
    step = _fdiv(from_ - to, stes)
    return _uint(round(from_ - (step * stepNo)))

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticOfRsx(_MQL5Indicator):
    name = 'stochastic_of_rsx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StochasticPeriod': 32,  # Stochastic period
        'StochasticSlowing': 9,  # Stochastic slowing period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=0),  # Price to use
        'RsxPeriod': 32.0,  # Rsx period
    }

