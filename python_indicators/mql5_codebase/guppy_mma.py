"""guppy_mma — converted from MQL5: MQL5 Indicators/Guppy MMA/guppy_mma.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 12}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'guppy_mma', 'source': 'MQL5 Indicators/Guppy MMA/guppy_mma.mq5', 'folder': 'Guppy MMA', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Guppy MMAs price', 'sinput': False}, {'mql': 'Method', 'py': 'Method', 'param': 'Method', 'type': 'int', 'default': 1, 'label': 'Guppy MMAs method', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 0, 'label': 'Starting color for MAs', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 0, 'label': 'Ending color for MAs', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate when in multi time frame mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Lime = 0x00FF00  # MQL4 colour name
MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter
MediumVioletRed = 0x8515C7  # MQL4 colour name

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
Price = _input('Price', PRICE_CLOSE)  # Guppy MMAs price
Method = _input('Method', MODE_EMA)  # Guppy MMAs method
Interpolate = _input('Interpolate', True)  # Interpolate when in multi time frame mode?
count = Arr(0, 0.0)
timeFrame = 0
steps = 0
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

class simpleMa(MqlObject):
    _q_fields = ('handle', 'buffer')
    def __init__(self, *args):
        self.handle = 0
        self.buffer = Arr(0, 0.0)

def OnInit():
    global steps, timeFrame
    periods = Arr.of([3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60], fill=0)
    steps = ArraySize(periods)
    timeFrame = MathMax(Period(), TimeFrame)
    i = 0
    while i < steps:
        if timeFrame == Period():
            handle = iMA(None, 0, periods[i], 0, Method, Price)
            aBuffers[i].handle = handle
        SetIndexBuffer(i, aBuffers[i].buffer, INDICATOR_DATA)
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(i, PLOT_COLOR_INDEXES, 1)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, gradientColor(i, steps, ColorFrom, ColorTo))
        PlotIndexSetString(i, PLOT_LABEL, 'Guppy MA ' + IntegerToString(periods[i]))
        i += 1
    SetIndexBuffer(12, count, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(timeFrame) + ' Guppy MMA')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_indHandle
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if timeFrame != Period():
        result = Arr(0, 0.0)
        currTime = Arr(0, 0)
        nextTime = Arr(0, 0)
        if _s_OnCalculate_indHandle == -1:
            _s_OnCalculate_indHandle = iCustom(Symbol(), timeFrame, getIndicatorName(), PERIOD_CURRENT, Price, Method)
        if _s_OnCalculate_indHandle == -1:
            return 0
        if CopyBuffer(_s_OnCalculate_indHandle, 12, 0, 1, result) == -1:
            return 0
        i = 0
        limit = rates_total - _int(MathMin(_fdiv(result[0] * PeriodSeconds(timeFrame), PeriodSeconds(Period())), rates_total))
        limit = MathMax(limit, 0)
        for limit in range(limit, 0, -1):
            if count[limit] == (EMPTY_VALUE - 1):
                break
        else:
            limit = _range_end(limit, 0, -1)
        i = MathMin(limit, MathMax(prev_calculated - 1, 0))
        for i in range(i, rates_total):
            OK = True
            for b in range(0, steps):
                if CopyBuffer(_s_OnCalculate_indHandle, b, _DT(time[i]), 1, result) == -1:
                    OK = False
                    break
                aBuffers[b].buffer[i] = result[0]
            if not OK:
                break
            count[i] = EMPTY_VALUE - 1
            if not Interpolate:
                continue
            CopyTime(Symbol(), TimeFrame, _DT(time[i]), 1, currTime)
            if i < (rates_total - 1):
                CopyTime(Symbol(), TimeFrame, _DT(time[i + 1]), 1, nextTime)
                if currTime[0] == nextTime[0]:
                    continue
            n = 0
            k = 0
            n = 1
            while (i - n) > 0 and time[i - n] >= currTime[0]:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                for b in range(0, steps):
                    aBuffers[b].buffer[i - k] = aBuffers[b].buffer[i] + _fdiv((aBuffers[b].buffer[i - n] - aBuffers[b].buffer[i]) * k, n)
                k += 1
        else:
            i = _range_end(i, rates_total, 1)
        if i != rates_total:
            return 0
        return rates_total
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    for i in range(0, steps):
        CopyBuffer(aBuffers[i].handle, 0, 0, limit, aBuffers[i].buffer)
    count[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
    return rates_total

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed

def getColor(stepNo, totalSteps, from_, to):
    step = _fdiv(from_ - to, totalSteps - 1.0)
    return _uint(round(from_ - (step * stepNo)))

def getIndicatorName():
    progPath = MQL5InfoString(MQL5_PROGRAM_PATH)
    start = -1
    while True:
        foundAt = StringFind(progPath, '\\', start + 1)
        if foundAt >= 0:
            start = foundAt
        else:
            break
    indicatorName = StringSubstr(progPath, start + 1)
    indicatorName = StringSubstr(indicatorName, 0, StringLen(indicatorName) - 4)
    return indicatorName

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = ArraySize(_tfsPer) - 1
    for i in range(i, 0 - 1, -1):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, 0 - 1, -1)
    return _tfsStr[i]

# ---- global variables initialised from expressions
ColorFrom = _input('ColorFrom', _uint(Lime))  # Starting color for MAs
ColorTo = _input('ColorTo', _uint(MediumVioletRed))  # Ending color for MAs
aBuffers = Arr(12, 0, dyn=False, factory=simpleMa)

# ---- static local variables
_s_OnCalculate_indHandle = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GuppyMma(_MQL5Indicator):
    name = 'guppy_mma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Guppy MMAs price
        'Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Guppy MMAs method
        'Interpolate': True,  # Interpolate when in multi time frame mode?
    }

