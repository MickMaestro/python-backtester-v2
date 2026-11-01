"""donchian_channel_mtf — converted from MQL5: MQL5 Indicators/Donchian Channel MTF/donchian_channel_mtf.mq5

Copyright: mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329330], 2: [42495]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'High', 2: 'Low'}, 'levels': [], 'description': [], 'name': 'donchian_channel_mtf', 'source': 'MQL5 Indicators/Donchian Channel MTF/donchian_channel_mtf.mq5', 'folder': 'Donchian Channel MTF', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 0, 'label': 'Time frame for highs/lows', 'sinput': False}, {'mql': 'inpPeriodsBack', 'py': 'inpPeriodsBack', 'param': 'inpPeriodsBack', 'type': 'int', 'default': 20, 'label': 'Look back period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', PERIOD_CURRENT)  # Time frame for highs/lows
inpPeriodsBack = _input('inpPeriodsBack', 20)  # Look back period
HiBuffer = Arr(0, 0.0)
LoBuffer = Arr(0, 0.0)
iPeriod = 0

def OnInit():
    global iPeriod
    SetIndexBuffer(0, HiBuffer, INDICATOR_DATA)
    ArraySetAsSeries(HiBuffer, True)
    SetIndexBuffer(1, LoBuffer, INDICATOR_DATA)
    ArraySetAsSeries(LoBuffer, True)
    iPeriod = (inpPeriod if (inpPeriod >= Period()) else Period())
    timeFrameName = periodToString(iPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameName + ' highs/lows')
    PlotIndexSetString(0, PLOT_LABEL, timeFrameName + ' high')
    PlotIndexSetString(1, PLOT_LABEL, timeFrameName + ' low')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not ArrayGetAsSeries(time):
        ArraySetAsSeries(time, True)
    ratesArray = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(ratesArray, True)
    copiedRates = 0
    for i in range(0, 5):
        if (copiedRates := CopyRates(Symbol(), iPeriod, _DT(time[rates_total - 1]), _DT(time[0]), ratesArray)) > 0:
            break
    if copiedRates <= 0:
        Print('not all rates copied. Will try on next tick')
        return prev_calculated
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    if prev_calculated == 0:
        limit -= 1
    minutesPeriod = periodToMinutes(Period())
    minutesChosen = periodToMinutes(iPeriod)
    limit = (limit if (limit > _idiv(3 * minutesChosen, minutesPeriod)) else _idiv(3 * minutesChosen, minutesPeriod))
    for i in range(MathMin(limit, rates_total - 2), 0 - 1, -1):
        d = dateArrayBsearch(ratesArray, time[i] - (minutesChosen * 60), copiedRates)
        if d >= 0:
            HiBuffer[i] = ratesArray[d].high
            LoBuffer[i] = ratesArray[d].low
            k = 1
            while k < inpPeriodsBack and (d + k) < copiedRates:
                HiBuffer[i] = MathMax(HiBuffer[i], ratesArray[d + k].high)
                LoBuffer[i] = MathMin(LoBuffer[i], ratesArray[d + k].low)
                k += 1
        else:
            HiBuffer[i] = EMPTY_VALUE
            LoBuffer[i] = EMPTY_VALUE
    return rates_total

def dateArrayBsearch(rates, toFind, total):
    mid = 0
    first = 0
    last = total - 1
    while last >= first:
        mid = (first + last) >> 1
        if toFind == rates[mid].time or ((mid > 0 and toFind > rates[mid].time) and toFind < rates[mid - 1].time):
            break
        if toFind > rates[mid].time:
            last = mid - 1
        else:
            first = mid + 1
    return mid

def periodToMinutes(period):
    i = 0
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    for i in range(i, 20):
        if period == _s_periodToMinutes__per[i]:
            break
    else:
        i = _range_end(i, 20, 1)
    return _s_periodToMinutes__min[i]

def periodToString(period):
    i = 0
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    for i in range(i, 20):
        if period == _s_periodToString__per[i]:
            break
    else:
        i = _range_end(i, 20, 1)
    return _s_periodToString__tfs[i]

# ---- static local variables
_s_periodToMinutes__per = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 0x4001, 0x4002, 0x4003, 0x4004, 0x4006, 0x4008, 0x400c, 0x4018, 0x8001, 0xc001], fill=0)
_s_periodToMinutes__min = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60, 120, 180, 240, 360, 480, 720, 1440, 10080, 43200], fill=0)
_s_periodToString__per = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 0x4001, 0x4002, 0x4003, 0x4004, 0x4006, 0x4008, 0x400c, 0x4018, 0x8001, 0xc001], fill=0)
_s_periodToString__tfs = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianChannelMtf(_MQL5Indicator):
    name = 'donchian_channel_mtf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame for highs/lows
        'inpPeriodsBack': 20,  # Look back period
    }

