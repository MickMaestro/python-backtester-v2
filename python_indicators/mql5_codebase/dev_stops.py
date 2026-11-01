"""Dev-stops — converted from MQL5: MQL5 Indicators/DevStops/Dev-stops.mq5

Dev-stops
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 8, 2: 8, 3: 8, 4: 8}, 'colors': {1: [11119017, 15453831, 6333684], 2: [11119017, 15453831, 6333684], 3: [11119017, 15453831, 6333684], 4: [11119017, 15453831, 6333684]}, 'widths': {1: 2, 4: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'Dev-stop 1', 2: 'Dev-stop 2', 3: 'Dev-stop 3', 4: 'Dev-stop 4'}, 'levels': [], 'description': ['Dev-stops'], 'name': 'Dev-stops', 'source': 'MQL5 Indicators/DevStops/Dev-stops.mq5', 'folder': 'DevStops', 'inputs': [{'mql': 'inpDesPeriod', 'py': 'inpDesPeriod', 'param': 'inpDesPeriod', 'type': 'int', 'default': 20, 'label': 'Dev-stop period', 'sinput': False}, {'mql': 'inpHilPeriod', 'py': 'inpHilPeriod', 'param': 'inpHilPeriod', 'type': 'int', 'default': 2, 'label': 'Dev-stop high/low period', 'sinput': False}, {'mql': 'inpStdDev2', 'py': 'inpStdDev2', 'param': 'inpStdDev2', 'type': 'double', 'default': 2.2, 'label': 'Deviation 2', 'sinput': False}, {'mql': 'inpStdDev3', 'py': 'inpStdDev3', 'param': 'inpStdDev3', 'type': 'double', 'default': 3.6, 'label': 'Deviation 3', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpDesPeriod = _input('inpDesPeriod', 20)  # Dev-stop period
inpHilPeriod = _input('inpHilPeriod', 2)  # Dev-stop high/low period
inpStdDev2 = _input('inpStdDev2', 2.2)  # Deviation 2
inpStdDev3 = _input('inpStdDev3', 3.6)  # Deviation 3
val1 = Arr(0, 0.0)
val1c = Arr(0, 0.0)
val2 = Arr(0, 0.0)
val2c = Arr(0, 0.0)
val3 = Arr(0, 0.0)
val3c = Arr(0, 0.0)
val4 = Arr(0, 0.0)
val4c = Arr(0, 0.0)
range_ = Arr(0, 0.0)
values = Arr(0, 0.0, dims=(4,))

def OnInit():
    SetIndexBuffer(0, val1, INDICATOR_DATA)
    SetIndexBuffer(1, val1c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val2, INDICATOR_DATA)
    SetIndexBuffer(3, val2c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, val3, INDICATOR_DATA)
    SetIndexBuffer(5, val3c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, val4, INDICATOR_DATA)
    SetIndexBuffer(7, val4c, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, range_, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Kase dev-stop (' + _str(inpDesPeriod) + ',' + _str(inpHilPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(values, 0) != rates_total:
        ArrayResize(values, rates_total)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _start = MathMax(0, i - inpHilPeriod)
        range_[i] = high[ArrayMaximum(high, _start, inpHilPeriod)] - low[ArrayMinimum(low, _start, inpHilPeriod)]
        avg = range_[i]
        n = 1
        while n < inpDesPeriod and (i - n) >= 0:
            avg += range_[i - n]
            n += 1
        avg = _fdiv(avg, n)
        dev = MathPow(range_[i] - avg, 2)
        n = 1
        while n < inpDesPeriod and (i - n) >= 0:
            dev += (range_[i - n] - avg) * (range_[i - n] - avg)
            n += 1
        dev = MathSqrt(_fdiv(dev, n))
        values[i][0] = high[i] - avg - (dev * inpStdDev3)
        values[i][1] = high[i] - avg - (dev * inpStdDev2)
        values[i][2] = high[i] - avg - dev
        values[i][3] = high[i] - avg
        val1[i] = values[i][0]
        val2[i] = values[i][1]
        val3[i] = values[i][2]
        val4[i] = values[i][3]
        n = 1
        while n < inpDesPeriod and (i - n) >= 0:
            val1[i] = MathMax(val1[i], values[i - n][0])
            val2[i] = MathMax(val2[i], values[i - n][1])
            val3[i] = MathMax(val3[i], values[i - n][2])
            val4[i] = MathMax(val4[i], values[i - n][3])
            n += 1
        val1c[i] = ((1 if (val1[i] > val1[i - 1]) else 2 if (val1[i] < val1[i - 1]) else val1c[i - 1]) if (i > 0) else 0)
        val2c[i] = ((1 if (val2[i] > val2[i - 1]) else 2 if (val2[i] < val2[i - 1]) else val2c[i - 1]) if (i > 0) else 0)
        val3c[i] = ((1 if (val3[i] > val3[i - 1]) else 2 if (val3[i] < val3[i - 1]) else val3c[i - 1]) if (i > 0) else 0)
        val4c[i] = ((1 if (val4[i] > val4[i - 1]) else 2 if (val4[i] < val4[i - 1]) else val4c[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DevStops(_MQL5Indicator):
    name = 'Dev-stops'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDesPeriod': 20,  # Dev-stop period
        'inpHilPeriod': 2,  # Dev-stop high/low period
        'inpStdDev2': 2.2,  # Deviation 2
        'inpStdDev3': 3.6,  # Deviation 3
    }

