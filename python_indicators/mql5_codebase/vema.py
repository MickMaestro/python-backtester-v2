"""vema — converted from MQL5: MQL5 Indicators/Volume Weighted EMA/vema.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Volume veighted EMA'}, 'levels': [], 'description': [], 'name': 'vema', 'source': 'MQL5 Indicators/Volume Weighted EMA/vema.mq5', 'folder': 'Volume Weighted EMA', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 25, 'label': 'Vema period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'RealV', 'py': 'RealV', 'param': 'RealV', 'type': 'bool', 'default': False, 'label': 'Use real volume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
pr_haclose = 8
pr_haopen = 9
pr_hahigh = 10
pr_halow = 11
pr_hamedian = 12
pr_hatypical = 13
pr_haweighted = 14
pr_haaverage = 15
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_haclose', 9: 'pr_haopen', 10: 'pr_hahigh', 11: 'pr_halow', 12: 'pr_hamedian', 13: 'pr_hatypical', 14: 'pr_haweighted', 15: 'pr_haaverage'})

# ---- inputs and global variables
Length = _input('Length', 25)  # Vema period
Price = _input('Price', pr_close)  # Price to use
RealV = _input('RealV', False)  # Use real volume
vma = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
vemas = Arr(0, 0.0, dims=(2,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, vma, INDICATOR_DATA)
    SetIndexBuffer(1, colorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, ' VEMA (' + _str(Length) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArrayRange(vemas, 0) != rates_total:
        ArrayResize(vemas, rates_total)
    alpha = _fdiv(2.0, 1.0 + Length)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = getPrice(Price, open, close, high, low, i, rates_total)
        vol = 0.0
        if RealV:
            vol = float(volume[i])
        else:
            vol = float(tick_volume[i])
        if i < 2:
            vemas[i][0] = vol * price
            vemas[i][1] = vol
            continue
        vemas[i][0] = vemas[i - 1][0] + (alpha * ((vol * price) - vemas[i - 1][0]))
        vemas[i][1] = vemas[i - 1][1] + (alpha * (vol - vemas[i - 1][1]))
        vma[i] = _fdiv(vemas[i][0], vemas[i][1])
        colorBuffer[i] = colorBuffer[i - 1]
        if vma[i] > vma[i - 1]:
            colorBuffer[i] = 0.0
        if vma[i] < vma[i - 1]:
            colorBuffer[i] = 1.0
    return rates_total

def getPrice(price, open, close, high, low, i, bars):
    if price >= pr_haclose and price <= pr_haaverage:
        if ArrayRange(workHa, 0) != bars:
            ArrayResize(workHa, bars)
        haOpen = 0.0
        if i > 0:
            haOpen = (workHa[i - 1][2] + workHa[i - 1][3]) / 2.0
        else:
            haOpen = open[i] + close[i]
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][0] = haLow
            workHa[i][1] = haHigh
        else:
            workHa[i][0] = haHigh
            workHa[i][1] = haLow
        workHa[i][2] = haOpen
        workHa[i][3] = haClose
        _sw1 = price
        if _sw1 == pr_haclose:
            return haClose
        elif _sw1 == pr_haopen:
            return haOpen
        elif _sw1 == pr_hahigh:
            return haHigh
        elif _sw1 == pr_halow:
            return haLow
        elif _sw1 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw1 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw1 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw1 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
    _sw2 = price
    if _sw2 == pr_close:
        return close[i]
    elif _sw2 == pr_open:
        return open[i]
    elif _sw2 == pr_high:
        return high[i]
    elif _sw2 == pr_low:
        return low[i]
    elif _sw2 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw2 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vema(_MQL5Indicator):
    name = 'vema'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 25,  # Vema period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4', 8: 'Heiken ashi close', 9: 'Heiken ashi open', 10: 'Heiken ashi high', 11: 'Heiken ashi low', 12: 'Heiken ashi median', 13: 'Heiken ashi typical', 14: 'Heiken ashi weighted', 15: 'Heiken ashi average'}, default=0),  # Price to use
        'RealV': False,  # Use real volume
    }

