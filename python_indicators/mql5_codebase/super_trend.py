"""Super trend — converted from MQL5: MQL5 Indicators/Super Trend/Super trend.mq5

Super trend - CCI based
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Super trend'}, 'levels': [], 'description': ['Super trend - CCI based'], 'name': 'Super trend', 'source': 'MQL5 Indicators/Super Trend/Super trend.mq5', 'folder': 'Super Trend', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'Cci Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Cci Price', 'sinput': False}, {'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 5, 'label': 'Atr period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # Cci Period
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Cci Price
inpAtrPeriod = _input('inpAtrPeriod', 5)  # Atr period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
trend = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, trend, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Super trend (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
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
    return rates_total

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


class SuperTrend(_MQL5Indicator):
    name = 'Super trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 50,  # Cci Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Cci Price
        'inpAtrPeriod': 5,  # Atr period
    }

