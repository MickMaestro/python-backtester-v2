"""super_trend_hull — converted from MQL5: MQL5 Indicators/Super Trend Hull Indicator/super_trend_hull.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Super trend hull'}, 'levels': [], 'description': [], 'name': 'super_trend_hull', 'source': 'MQL5 Indicators/Super Trend Hull Indicator/super_trend_hull.mq5', 'folder': 'Super Trend Hull Indicator', 'inputs': [{'mql': 'hullPeriod', 'py': 'hullPeriod', 'param': 'hullPeriod', 'type': 'int', 'default': 12, 'label': 'Hull period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 4, 'label': 'Price', 'sinput': False}, {'mql': 'atrPeriod', 'py': 'atrPeriod', 'param': 'atrPeriod', 'type': 'int', 'default': 12, 'label': 'ATR period', 'sinput': False}, {'mql': 'atrMultiplier', 'py': 'atrMultiplier', 'param': 'atrMultiplier', 'type': 'double', 'default': 0.66, 'label': 'ATR multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
hullPeriod = _input('hullPeriod', 12)  # Hull period
Price = _input('Price', pr_median)  # Price
atrPeriod = _input('atrPeriod', 12)  # ATR period
atrMultiplier = _input('atrMultiplier', 0.66)  # ATR multiplier
st = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
Up = Arr(0, 0.0)
Dn = Arr(0, 0.0)
Direction = Arr(0, 0.0)
workHull = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, st, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArraySize(Direction) != rates_total:
        ArrayResize(Up, rates_total)
        ArrayResize(Dn, rates_total)
        ArrayResize(Direction, rates_total)
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        atr = 0.0
        k = 0
        while k < atrPeriod and (i - k - 1) >= 0:
            atr += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
            k += 1
        atr = atr / atrPeriod
        cprice = close[i]
        mprice = iHull(getPrice(Price, open, close, high, low, i, rates_total), hullPeriod, i, rates_total)
        Up[i] = mprice + (atrMultiplier * atr)
        Dn[i] = mprice - (atrMultiplier * atr)
        colorBuffer[i] = colorBuffer[i - 1]
        Direction[i] = Direction[i - 1]
        if cprice > Up[i - 1]:
            Direction[i] = 1.0
        if cprice < Dn[i - 1]:
            Direction[i] = -1.0
        if Direction[i] > 0:
            Dn[i] = MathMax(Dn[i], Dn[i - 1])
            st[i] = Dn[i]
        else:
            Up[i] = MathMin(Up[i], Up[i - 1])
            st[i] = Up[i]
        if Direction[i] == 1:
            colorBuffer[i] = 0.0
        if Direction[i] == -1:
            colorBuffer[i] = 1.0
    return rates_total

def iHull(price, period, r, bars, instanceNo=0):
    if ArrayRange(workHull, 0) != bars:
        ArrayResize(workHull, bars)
    HmaPeriod = _int(MathMax(period, 2))
    HalfPeriod = _int(MathFloor(_idiv(HmaPeriod, 2)))
    HullPeriod = _int(MathFloor(MathSqrt(HmaPeriod)))
    hma = 0.0
    hmw = 0.0
    weight = 0.0
    instanceNo *= 2
    workHull[r][instanceNo] = price
    hmw = HalfPeriod
    hma = hmw * price
    k = 1
    while k < HalfPeriod and (r - k) >= 0:
        weight = HalfPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][instanceNo]
        k += 1
    workHull[r][instanceNo + 1] = _fdiv(2.0 * hma, hmw)
    hmw = HmaPeriod
    hma = hmw * price
    k = 1
    while k < period and (r - k) >= 0:
        weight = HmaPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][instanceNo]
        k += 1
    workHull[r][instanceNo + 1] -= _fdiv(hma, hmw)
    hmw = HullPeriod
    hma = hmw * workHull[r][instanceNo + 1]
    k = 1
    while k < HullPeriod and (r - k) >= 0:
        weight = HullPeriod - k
        hmw += weight
        hma += weight * workHull[r - k][1 + instanceNo]
        k += 1
    return _fdiv(hma, hmw)

def getPrice(price, open, close, high, low, i, bars):
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperTrendHull(_MQL5Indicator):
    name = 'super_trend_hull'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'hullPeriod': 12,  # Hull period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4'}, default=4),  # Price
        'atrPeriod': 12,  # ATR period
        'atrMultiplier': 0.66,  # ATR multiplier
    }

