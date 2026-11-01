"""Super trend - extended — converted from MQL5: MQL5 Indicators/Super Trend - Extended/Super trend - extended.mq5

Super trend - CCI based
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 16, 'indicator_plots': 3}, 'types': {1: 16, 2: 17, 3: 8}, 'colors': {1: [11119017, 9639167, 3329330], 2: [11119017, 9639167, 3329330], 3: [11119017, 9639167, 3329330]}, 'widths': {3: 2}, 'styles': {}, 'labels': {1: 'Super trend bars', 2: 'Super trend candles', 3: 'Super trend line'}, 'levels': [], 'description': ['Super trend - CCI based'], 'name': 'Super trend - extended', 'source': 'MQL5 Indicators/Super Trend - Extended/Super trend - extended.mq5', 'folder': 'Super Trend - Extended', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'Cci Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Cci Price', 'sinput': False}, {'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 5, 'label': 'Atr period', 'sinput': False}, {'mql': 'inpDisplayStyle', 'py': 'inpDisplayStyle', 'param': 'inpDisplayStyle', 'type': 'int', 'default': 0, 'label': 'Display style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDisplayStyle
dis_automatic = 0
dis_line = 1
dis_bars = 2
dis_candles = 3
_enum('enDisplayStyle', {0: 'dis_automatic', 1: 'dis_line', 2: 'dis_bars', 3: 'dis_candles'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # Cci Period
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Cci Price
inpAtrPeriod = _input('inpAtrPeriod', 5)  # Atr period
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
prices = Arr(0, 0.0)
trend = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

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
    SetIndexBuffer(12, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, val, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, valc, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Super trend (' + _str(inpPeriod) + ')')
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
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        avg = 0.0
        k = 0
        while k < inpPeriod and (i - k) >= 0:
            avg += prices[i - k]
            k += 1
        avg = avg / inpPeriod
        dev = 0.0
        k = 0
        while k < inpPeriod and (i - k) >= 0:
            dev += MathAbs(prices[i - k] - avg)
            k += 1
        dev = dev / inpPeriod
        atr = 0.0
        k = 0
        while k < inpAtrPeriod and (i - k - 1) >= 0:
            atr += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
            k += 1
        atr = atr / inpAtrPeriod
        cci = (_fdiv(prices[i] - avg, 0.015 * dev) if (dev != 0) else 0)
        trend[i] = (1 if (cci > 0) else -1 if (cci < 0) else trend[i - 1] if (i > 0) else 0)
        val[i] = ((MathMax(low[i] - atr, val[i - 1]) if (trend[i] == 1) else MathMin(high[i] + atr, val[i - 1])) if (i > 0) else close[i])
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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
            barcl[i] = valc[i]
        elif _sw2 == CHART_CANDLES:
            canh[i] = high[i]
            canl[i] = low[i]
            canc[i] = close[i]
            cano[i] = open[i]
            cancl[i] = valc[i]
        elif _sw2 == CHART_LINE:
            line[i] = val[i]
            linecl[i] = valc[i]
        i += 1
    return rates_total

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
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


class SuperTrendExtended(_MQL5Indicator):
    name = 'Super trend - extended'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 50,  # Cci Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Cci Price
        'inpAtrPeriod': 5,  # Atr period
        'inpDisplayStyle': _Choice({0: 'Automatic display style', 1: 'Display line', 2: 'Display bars', 3: 'Display candles'}, default=0),  # Display style
    }

