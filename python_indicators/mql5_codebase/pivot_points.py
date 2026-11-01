"""pivot_points — converted from MQL5: MQL5 Indicators/Pivot Points/pivot_points.mq5

Copyright: mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'pivot_points', 'source': 'MQL5 Indicators/Pivot Points/pivot_points.mq5', 'folder': 'Pivot Points', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 16408, 'label': 'Time frame for pivots', 'sinput': False}, {'mql': 'inpPivotType', 'py': 'inpPivotType', 'param': 'inpPivotType', 'type': 'int', 'default': 0, 'label': 'Pivot calculated as', 'sinput': False}, {'mql': 'inpPivotCalculate', 'py': 'inpPivotCalculate', 'param': 'inpPivotCalculate', 'type': 'int', 'default': 0, 'label': 'Calculation method', 'sinput': False}, {'mql': 'inpColorPivot', 'py': 'inpColorPivot', 'param': None, 'type': 'color', 'default': 0, 'label': 'Pivot line color', 'sinput': False}, {'mql': 'inpColorFrom', 'py': 'inpColorFrom', 'param': None, 'type': 'color', 'default': 0, 'label': 'Starting color for pivots', 'sinput': False}, {'mql': 'inpColorTo', 'py': 'inpColorTo', 'param': None, 'type': 'color', 'default': 0, 'label': 'Ending color for pivots', 'sinput': False}, {'mql': 'inpLineStyle', 'py': 'inpLineStyle', 'param': 'inpLineStyle', 'type': 'int', 'default': 0, 'label': 'Drawing style for lines', 'sinput': False}, {'mql': 'inpHideConnections', 'py': 'inpHideConnections', 'param': 'inpHideConnections', 'type': 'bool', 'default': False, 'label': 'Hide conecting lines between periods', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DeepSkyBlue = 0xFFBF00  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# enum eStyles
stDash = 1
stDashDot = 3
stDashDotDot = 4
stDot = 2
stSolid = 0
_enum('eStyles', {1: 'stDash', 3: 'stDashDot', 4: 'stDashDotDot', 2: 'stDot', 0: 'stSolid'})

# enum ePivotTypes
ptHLC = 0
ptHLCC = 1
ptHLOC = 2
ptHLOO = 3
_enum('ePivotTypes', {0: 'ptHLC', 1: 'ptHLCC', 2: 'ptHLOC', 3: 'ptHLOO'})

# enum eCalculation
ecOriginal = 0
ecAlternate = 1
_enum('eCalculation', {0: 'ecOriginal', 1: 'ecAlternate'})

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', PERIOD_D1)  # Time frame for pivots
inpPivotType = _input('inpPivotType', ptHLC)  # Pivot calculated as
inpPivotCalculate = _input('inpPivotCalculate', ecOriginal)  # Calculation method
inpLineStyle = _input('inpLineStyle', stSolid)  # Drawing style for lines
inpHideConnections = _input('inpHideConnections', False)  # Hide conecting lines between periods
pivBuffer01 = Arr(0, 0.0)
pivBuffer02 = Arr(0, 0.0)
pivBuffer03 = Arr(0, 0.0)
pivBuffer04 = Arr(0, 0.0)
pivBuffer05 = Arr(0, 0.0)
pivBuffer06 = Arr(0, 0.0)
pivBuffer07 = Arr(0, 0.0)
labels = Arr.of(['R3', 'R2', 'R1', 'pivot', 'S1', 'S2', 'S3'], fill="", dyn=False, size=7)
iTimeFrame = 0

def OnInit():
    global iTimeFrame
    SetIndexBuffer(0, pivBuffer01, INDICATOR_DATA)
    ArraySetAsSeries(pivBuffer01, True)
    SetIndexBuffer(1, pivBuffer02, INDICATOR_DATA)
    ArraySetAsSeries(pivBuffer02, True)
    SetIndexBuffer(2, pivBuffer03, INDICATOR_DATA)
    ArraySetAsSeries(pivBuffer03, True)
    SetIndexBuffer(3, pivBuffer04, INDICATOR_DATA)
    ArraySetAsSeries(pivBuffer04, True)
    SetIndexBuffer(4, pivBuffer05, INDICATOR_DATA)
    ArraySetAsSeries(pivBuffer05, True)
    SetIndexBuffer(5, pivBuffer06, INDICATOR_DATA)
    ArraySetAsSeries(pivBuffer06, True)
    SetIndexBuffer(6, pivBuffer07, INDICATOR_DATA)
    ArraySetAsSeries(pivBuffer07, True)
    steps = ArraySize(labels)
    for i in range(0, steps):
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, gradientColor(i, steps, inpColorFrom, inpColorTo))
        PlotIndexSetInteger(i, PLOT_LINE_STYLE, inpLineStyle)
        PlotIndexSetString(i, PLOT_LABEL, labels[i])
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, inpColorPivot)
    iTimeFrame = (inpTimeFrame if (inpTimeFrame >= Period()) else Period())
    timeFrameName = periodToString(iTimeFrame)
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameName + ' pivot points')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not ArrayGetAsSeries(time):
        ArraySetAsSeries(time, True)
    ratesArray = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(ratesArray, True)
    copiedRates = 0
    for i in range(0, 5):
        if (copiedRates := CopyRates(Symbol(), iTimeFrame, _DT(time[rates_total - 1]), _DT(time[0]), ratesArray)) > 0:
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
    minutesChosen = periodToMinutes(iTimeFrame)
    limit = (limit if (limit > _idiv(minutesChosen, minutesPeriod)) else _idiv(minutesChosen, minutesPeriod))
    for i in range(limit, 0 - 1, -1):
        d = dateArrayBsearch(ratesArray, time[i], copiedRates)
        if d >= 0 and d < (copiedRates - 1):
            d += 1
            LastHigh = ratesArray[d].high
            LastLow = ratesArray[d].low
            P = 0.0
            _sw1 = inpPivotType
            if _sw1 == ptHLC:
                P = (LastHigh + LastLow + ratesArray[d].close) / 3.0
            elif _sw1 == ptHLCC:
                P = (LastHigh + LastLow + ratesArray[d].close + ratesArray[d].close) / 4.0
            elif _sw1 == ptHLOC:
                P = (LastHigh + LastLow + ratesArray[d].close + ratesArray[d - 1].open) / 4.0
            elif _sw1 == ptHLOO:
                P = (LastHigh + LastLow + ratesArray[d - 1].open + ratesArray[d - 1].open) / 4.0
            pivBuffer04[i] = P
            if inpPivotCalculate == ecOriginal:
                pivBuffer03[i] = P + (P - LastLow)
                pivBuffer05[i] = P - (LastHigh - P)
                pivBuffer02[i] = P + (LastHigh - LastLow)
                pivBuffer06[i] = P - (LastHigh - LastLow)
                pivBuffer01[i] = P + ((LastHigh - LastLow) * 2.0)
                pivBuffer07[i] = P - ((LastHigh - LastLow) * 2.0)
            else:
                pivBuffer03[i] = (P * 2.0) - LastLow
                pivBuffer05[i] = (P * 2.0) - LastHigh
                pivBuffer02[i] = P + (LastHigh - LastLow)
                pivBuffer06[i] = P - (LastHigh - LastLow)
                pivBuffer01[i] = (P * 2.0) + (LastHigh - (2.0 * LastLow))
                pivBuffer07[i] = (P * 2.0) - ((2.0 * LastHigh) - LastLow)
            if inpHideConnections:
                cd = dateArrayBsearch(ratesArray, time[i + 1], copiedRates) + 1
                if cd != d:
                    pivBuffer01[i + 1] = EMPTY_VALUE
                    pivBuffer02[i + 1] = EMPTY_VALUE
                    pivBuffer03[i + 1] = EMPTY_VALUE
                    pivBuffer04[i + 1] = EMPTY_VALUE
                    pivBuffer05[i + 1] = EMPTY_VALUE
                    pivBuffer06[i + 1] = EMPTY_VALUE
                    pivBuffer07[i + 1] = EMPTY_VALUE
        else:
            pivBuffer01[i] = EMPTY_VALUE
            pivBuffer02[i] = EMPTY_VALUE
            pivBuffer03[i] = EMPTY_VALUE
            pivBuffer04[i] = EMPTY_VALUE
            pivBuffer05[i] = EMPTY_VALUE
            pivBuffer06[i] = EMPTY_VALUE
            pivBuffer07[i] = EMPTY_VALUE
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

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed

def getColor(stepNo, totalSteps, from_, to):
    step = _fdiv(from_ - to, totalSteps - 1.0)
    return _uint(round(from_ - (step * stepNo)))

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

# ---- global variables initialised from expressions
inpColorPivot = _input('inpColorPivot', _uint(Yellow))  # Pivot line color
inpColorFrom = _input('inpColorFrom', _uint(Lime))  # Starting color for pivots
inpColorTo = _input('inpColorTo', _uint(DeepSkyBlue))  # Ending color for pivots

# ---- static local variables
_s_periodToMinutes__per = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 0x4001, 0x4002, 0x4003, 0x4004, 0x4006, 0x4008, 0x400c, 0x4018, 0x8001, 0xc001], fill=0)
_s_periodToMinutes__min = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60, 120, 180, 240, 360, 480, 720, 1440, 10080, 43200], fill=0)
_s_periodToString__per = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 0x4001, 0x4002, 0x4003, 0x4004, 0x4006, 0x4008, 0x400c, 0x4018, 0x8001, 0xc001], fill=0)
_s_periodToString__tfs = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PivotPoints(_MQL5Indicator):
    name = 'pivot_points'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Time frame for pivots
        'inpPivotType': _Choice({0: '(high+low+close)/3', 1: '(high+low+close+close)/4', 2: '(high+low+close+open)/4', 3: ')high+low+open+open)/4'}, default=0),  # Pivot calculated as
        'inpPivotCalculate': _Choice({0: 'Calculate pivot the original way', 1: 'Calculate pivot the "alternate" way'}, default=0),  # Calculation method
        'inpLineStyle': _Choice({1: 'Draw dash', 3: 'Draw dash-dot', 4: 'Draw dash-dot-dot', 2: 'Draw dot', 0: 'Draw solid line'}, default=0),  # Drawing style for lines
        'inpHideConnections': False,  # Hide conecting lines between periods
    }

