"""Hull trend — converted from MQL5: MQL5 Indicators/Hull trend/Hull trend.mq5

Hull trend
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'chart', 'indicator_buffers': 14, 'indicator_plots': 3}, 'types': {1: 16, 2: 17, 3: 8}, 'colors': {1: [11119017, 16760576, 6333684], 2: [11119017, 16760576, 6333684], 3: [11119017, 16760576, 6333684]}, 'widths': {3: 2}, 'styles': {}, 'labels': {1: 'Hull trend bars', 2: 'Hull trend candles', 3: 'Hull trend line'}, 'levels': [], 'description': ['Hull trend'], 'name': 'Hull trend', 'source': 'MQL5 Indicators/Hull trend/Hull trend.mq5', 'folder': 'Hull trend', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Hull period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDisplayStyle', 'py': 'inpDisplayStyle', 'param': 'inpDisplayStyle', 'type': 'int', 'default': 0, 'label': 'Display style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDisplayStyle
dis_automatic = 0
dis_line = 1
dis_bars = 2
dis_candles = 3
_enum('enDisplayStyle', {0: 'dis_automatic', 1: 'dis_line', 2: 'dis_bars', 3: 'dis_candles'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Hull period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDisplayStyle = _input('inpDisplayStyle', dis_automatic)  # Display style
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
cano = Arr(0, 0.0)
canc = Arr(0, 0.0)
cancl = Arr(0, 0.0)
baro = Arr(0, 0.0)
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
barc = Arr(0, 0.0)
barcl = Arr(0, 0.0)
line = Arr(0, 0.0)
linecl = Arr(0, 0.0)
hull = Arr(0, 0.0)
hullcl = Arr(0, 0.0)
workHull = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, baro, INDICATOR_DATA)
    SetIndexBuffer(1, barh, INDICATOR_DATA)
    SetIndexBuffer(2, barl, INDICATOR_DATA)
    SetIndexBuffer(3, barc, INDICATOR_DATA)
    SetIndexBuffer(4, barcl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, cano, INDICATOR_DATA)
    SetIndexBuffer(6, canh, INDICATOR_DATA)
    SetIndexBuffer(7, canl, INDICATOR_DATA)
    SetIndexBuffer(8, canc, INDICATOR_DATA)
    SetIndexBuffer(9, cancl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(10, line, INDICATOR_DATA)
    SetIndexBuffer(11, linecl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(12, hull, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, hullcl, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hull trend (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prevDisplayType
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    limit = prev_calculated - 1
    currDisplayType = -1
    _sw1 = inpDisplayStyle
    if _sw1 == dis_line:
        currDisplayType = CHART_LINE
    elif _sw1 == dis_bars:
        currDisplayType = CHART_BARS
    elif _sw1 == dis_candles:
        currDisplayType = CHART_CANDLES
    elif _sw1 == dis_automatic:
        currDisplayType = _int(ChartGetInteger(0, CHART_MODE))
    if currDisplayType != _s_OnCalculate_prevDisplayType:
        limit = 0
        _s_OnCalculate_prevDisplayType = currDisplayType
    i = MathMax(limit, 0)
    while i < rates_total:
        hull[i] = iHull(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i, rates_total)
        hullcl[i] = ((1 if (hull[i] > hull[i - 1]) else 2 if (hull[i] < hull[i - 1]) else hullcl[i - 1]) if (i > 0) else 0)
        barc[i] = EMPTY_VALUE
        barl[i] = barc[i]
        barh[i] = barl[i]
        baro[i] = barh[i]
        canc[i] = EMPTY_VALUE
        canl[i] = canc[i]
        canh[i] = canl[i]
        cano[i] = canh[i]
        line[i] = EMPTY_VALUE
        _sw2 = currDisplayType
        if _sw2 == CHART_BARS:
            barh[i] = high[i]
            barl[i] = low[i]
            barc[i] = close[i]
            baro[i] = open[i]
            barcl[i] = hullcl[i]
        elif _sw2 == CHART_CANDLES:
            canh[i] = high[i]
            canl[i] = low[i]
            canc[i] = close[i]
            cano[i] = open[i]
            cancl[i] = hullcl[i]
        elif _sw2 == CHART_LINE:
            line[i] = hull[i]
            linecl[i] = hullcl[i]
        i += 1
    return i

def iHull(price, period, r, bars, instanceNo=0):
    if ArrayRange(workHull, 0) != bars:
        ArrayResize(workHull, bars)
    instanceNo *= 2
    workHull[r][instanceNo] = price
    if period <= 1:
        return price
    HmaPeriod = _int(MathMax(period, 2))
    HalfPeriod = _int(MathFloor(_idiv(HmaPeriod, 2)))
    HullPeriod = _int(MathFloor(MathSqrt(HmaPeriod)))
    hma = 0.0
    hmw = 0.0
    weight = 0.0
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

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw3 = tprice
    if _sw3 == PRICE_CLOSE:
        return close[i]
    elif _sw3 == PRICE_OPEN:
        return open[i]
    elif _sw3 == PRICE_HIGH:
        return high[i]
    elif _sw3 == PRICE_LOW:
        return low[i]
    elif _sw3 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw3 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw3 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

# ---- static local variables
_s_OnCalculate_prevDisplayType = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HullTrend(_MQL5Indicator):
    name = 'Hull trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Hull period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDisplayStyle': _Choice({0: 'Automatic display style', 1: 'Display line', 2: 'Display bars', 3: 'Display candles'}, default=0),  # Display style
    }

