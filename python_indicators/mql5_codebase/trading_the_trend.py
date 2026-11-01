"""Trading the trend — converted from MQL5: MQL5 Indicators/Trading the trend/Trading the trend.mq5

Trading the trend
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 3}, 'types': {1: 16, 2: 17, 3: 8}, 'colors': {1: [11119017, 16760576, 6333684], 2: [11119017, 16760576, 6333684], 3: [11119017, 16760576, 6333684]}, 'widths': {}, 'styles': {3: 2}, 'labels': {1: 'Trend bars', 2: 'Trend candles', 3: 'Trend line'}, 'levels': [], 'description': ['Trading the trend'], 'name': 'Trading the trend', 'source': 'MQL5 Indicators/Trading the trend/Trading the trend.mq5', 'folder': 'Trading the trend', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 21, 'label': 'Look back period', 'sinput': False}, {'mql': 'inpMultiplier', 'py': 'inpMultiplier', 'param': 'inpMultiplier', 'type': 'double', 'default': 3.0, 'label': 'Multiplier', 'sinput': False}, {'mql': 'inpChannelShift', 'py': 'inpChannelShift', 'param': 'inpChannelShift', 'type': 'int', 'default': 1, 'label': 'Channel shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 21)  # Look back period
inpMultiplier = _input('inpMultiplier', 3.0)  # Multiplier
inpChannelShift = _input('inpChannelShift', 1)  # Channel shift
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
workLwma = Arr(0, 0.0, dims=(1,))

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
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trading the trend (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prevDisplayType
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    limit = prev_calculated - 1
    currDisplayType = _int(ChartGetInteger(0, CHART_MODE))
    if currDisplayType != _s_OnCalculate_prevDisplayType:
        limit = 0
        _s_OnCalculate_prevDisplayType = currDisplayType
    i = MathMax(limit, 0)
    while i < rates_total:
        _start = MathMax(i - inpPeriod - inpChannelShift + 1, 0)
        hi = close[ArrayMaximum(close, _start, inpPeriod)]
        lo = close[ArrayMinimum(close, _start, inpPeriod)]
        tr = iLwma(((MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])) if (i > 0) else (high[i] - low[i])), inpPeriod, i, rates_total)
        hiLimit = hi - (tr * inpMultiplier)
        loLimit = lo + (tr * inpMultiplier)
        line[i] = (line[i - 1] if (i > 0) else close[i])
        linecl[i] = (linecl[i - 1] if (i > 0) else 0)
        if close[i] > loLimit and close[i] > hiLimit:
            line[i] = hiLimit
        if close[i] < loLimit and close[i] < hiLimit:
            line[i] = loLimit
        if close[i] > line[i]:
            linecl[i] = 1.0
        if close[i] < line[i]:
            linecl[i] = 2.0
        barc[i] = EMPTY_VALUE
        barl[i] = barc[i]
        barh[i] = barl[i]
        baro[i] = barh[i]
        canc[i] = EMPTY_VALUE
        canl[i] = canc[i]
        canh[i] = canl[i]
        cano[i] = canh[i]
        _sw1 = currDisplayType
        if _sw1 == CHART_BARS:
            barh[i] = high[i]
            barl[i] = low[i]
            barc[i] = close[i]
            baro[i] = open[i]
            barcl[i] = linecl[i]
        elif _sw1 == CHART_CANDLES:
            canh[i] = high[i]
            canl[i] = low[i]
            canc[i] = close[i]
            cano[i] = open[i]
            cancl[i] = linecl[i]
        i += 1
    return i

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

# ---- static local variables
_s_OnCalculate_prevDisplayType = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TradingTheTrend(_MQL5Indicator):
    name = 'Trading the trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 21,  # Look back period
        'inpMultiplier': 3.0,  # Multiplier
        'inpChannelShift': 1,  # Channel shift
    }

