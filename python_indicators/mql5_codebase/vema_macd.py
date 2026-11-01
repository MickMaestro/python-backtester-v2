"""vema_macd — converted from MQL5: MQL5 Indicators/Volume weighted MACD/vema_macd.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [15986136, 14804223], 2: [3329330], 3: [55295]}, 'widths': {2: 2, 3: 2}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'Volume veighted MACD OSMA', 2: 'Volume veighted MACD', 3: 'Volume veighted MACD Signal'}, 'levels': [], 'description': [], 'name': 'vema_macd', 'source': 'MQL5 Indicators/Volume weighted MACD/vema_macd.mq5', 'folder': 'Volume weighted MACD', 'inputs': [{'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'int', 'default': 12, 'label': 'Fast period', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'int', 'default': 26, 'label': 'Slow period', 'sinput': False}, {'mql': 'SignalPeriod', 'py': 'SignalPeriod', 'param': 'SignalPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'RealV', 'py': 'RealV', 'param': 'RealV', 'type': 'bool', 'default': False, 'label': 'Use real volume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
FastPeriod = _input('FastPeriod', 12)  # Fast period
SlowPeriod = _input('SlowPeriod', 26)  # Slow period
SignalPeriod = _input('SignalPeriod', 9)  # Signal period
Price = _input('Price', pr_close)  # Price to use
RealV = _input('RealV', False)  # Use real volume
osmau = Arr(0, 0.0)
osmad = Arr(0, 0.0)
macd = Arr(0, 0.0)
signal = Arr(0, 0.0)
vemas = Arr(0, 0.0, dims=(6,))
workHa = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, osmau, INDICATOR_DATA)
    SetIndexBuffer(1, osmad, INDICATOR_DATA)
    SetIndexBuffer(2, macd, INDICATOR_DATA)
    SetIndexBuffer(3, signal, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, ' VEMA MACD (' + _str(FastPeriod) + ',' + _str(SlowPeriod) + ',' + _str(SignalPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArrayRange(vemas, 0) != rates_total:
        ArrayResize(vemas, rates_total)
    alphaf = _fdiv(2.0, 1.0 + FastPeriod)
    alphas = _fdiv(2.0, 1.0 + SlowPeriod)
    alphag = _fdiv(2.0, 1.0 + SignalPeriod)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        vol = 0.0
        price = getPrice(Price, open, close, high, low, i, rates_total)
        if RealV:
            vol = float(volume[i])
        else:
            vol = float(tick_volume[i])
        if i < 2:
            vemas[i][0] = vol * price
            vemas[i][1] = vol
            vemas[i][3] = vol * price
            vemas[i][4] = vol
            continue
        vemas[i][0] = vemas[i - 1][0] + (alphaf * ((vol * price) - vemas[i - 1][0]))
        vemas[i][1] = vemas[i - 1][1] + (alphaf * (vol - vemas[i - 1][1]))
        vemas[i][2] = _fdiv(vemas[i][0], vemas[i][1])
        vemas[i][3] = vemas[i - 1][3] + (alphas * ((vol * price) - vemas[i - 1][3]))
        vemas[i][4] = vemas[i - 1][4] + (alphas * (vol - vemas[i - 1][4]))
        vemas[i][5] = _fdiv(vemas[i][3], vemas[i][4])
        macd[i] = vemas[i][2] - vemas[i][5]
        signal[i] = signal[i - 1] + (alphag * (macd[i] - signal[i - 1]))
        osmau[i] = macd[i] - signal[i]
        osmad[i] = 0.0
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


class VemaMacd(_MQL5Indicator):
    name = 'vema_macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastPeriod': 12,  # Fast period
        'SlowPeriod': 26,  # Slow period
        'SignalPeriod': 9,  # Signal period
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+oprn+close)/4', 8: 'Heiken ashi close', 9: 'Heiken ashi open', 10: 'Heiken ashi high', 11: 'Heiken ashi low', 12: 'Heiken ashi median', 13: 'Heiken ashi typical', 14: 'Heiken ashi weighted', 15: 'Heiken ashi average'}, default=0),  # Price to use
        'RealV': False,  # Use real volume
    }

