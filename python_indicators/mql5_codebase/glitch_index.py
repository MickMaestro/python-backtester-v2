"""Glitch index — converted from MQL5: MQL5 Indicators/Glitch Index/Glitch index.mq5

Glitch index
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [11119017, 3329330, 32768, 2237106, 17919], 2: [11119017, 3329330, 32768, 2237106, 17919]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Histogram', 2: 'Glitch index value'}, 'levels': [], 'description': ['Glitch index'], 'name': 'Glitch index', 'source': 'MQL5 Indicators/Glitch Index/Glitch index.mq5', 'folder': 'Glitch Index', 'inputs': [{'mql': 'inpSmaPeriod', 'py': 'inpSmaPeriod', 'param': 'inpSmaPeriod', 'type': 'int', 'default': 30, 'label': 'Average period', 'sinput': False}, {'mql': 'inpLevel1', 'py': 'inpLevel1', 'param': 'inpLevel1', 'type': 'double', 'default': 2.0, 'label': 'Level 1', 'sinput': False}, {'mql': 'inpLevel2', 'py': 'inpLevel2', 'param': 'inpLevel2', 'type': 'double', 'default': 5.0, 'label': 'Level 2', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpSmaPeriod = _input('inpSmaPeriod', 30)  # Average period
inpLevel1 = _input('inpLevel1', 2.0)  # Level 1
inpLevel2 = _input('inpLevel2', 5.0)  # Level 2
histo = Arr(0, 0.0)
histoc = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
sma = Arr(0, 0.0)
workSma = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, histo, INDICATOR_DATA)
    SetIndexBuffer(1, histoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, sma, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevel2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpLevel1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, -inpLevel1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, -inpLevel2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Glitch index (' + _str(inpSmaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        sma[i] = iSma(close[i], inpSmaPeriod, i, rates_total)
        rocSma = ((((sma[i] - sma[i - 1]) * 0.1) + 1.0) if (i > 0) else 0)
        smaMul = sma[i] * rocSma
        diff = close[i] - smaMul
        val[i] = _fdiv(diff, close[i]) * 100.0
        while True:
            if val[i] > inpLevel2:
                valc[i] = 1.0
                break
            if val[i] > inpLevel1:
                valc[i] = 2.0
                break
            if val[i] < (-inpLevel2):
                valc[i] = 4.0
                break
            if val[i] < (-inpLevel1):
                valc[i] = 3.0
                break
            valc[i] = 0.0
            break
        histo[i] = val[i]
        histoc[i] = valc[i]
        i += 1
    return i

def iSma(price, period, r, _bars, instanceNo=0):
    if ArrayRange(workSma, 0) != _bars:
        ArrayResize(workSma, _bars)
    workSma[r][instanceNo] = price
    avg = price
    k = 1
    while k < period and (r - k) >= 0:
        avg += workSma[r - k][instanceNo]
        k += 1
    return _fdiv(avg, float(k))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GlitchIndex(_MQL5Indicator):
    name = 'Glitch index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpSmaPeriod': 30,  # Average period
        'inpLevel1': 2.0,  # Level 1
        'inpLevel2': 5.0,  # Level 2
    }

