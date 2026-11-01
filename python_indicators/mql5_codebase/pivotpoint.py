"""pivotpoint — converted from MQL5: MQL5 Indicators/Pivot Point/pivotpoint.mq5

Copyright: Copyright 2012, niuniu; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, niuniu', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5}, 'colors': {1: [255], 2: [255], 3: [255], 4: [65535], 5: [16748574], 6: [16748574], 7: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'R3', 2: 'R2', 3: 'R1', 4: 'Pivot Point', 5: 'S1', 6: 'S2', 7: 'S3'}, 'levels': [], 'description': [], 'name': 'pivotpoint', 'source': 'MQL5 Indicators/Pivot Point/pivotpoint.mq5', 'folder': 'Pivot Point', 'inputs': [{'mql': 'ppPeriod', 'py': 'ppPeriod', 'param': 'ppPeriod', 'type': 'int', 'default': 0, 'label': 'PivotPoint Calculation Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PP_PERIOD
ppDay = 0
ppWeek = 1
ppMonth = 2
_enum('ENUM_PP_PERIOD', {0: 'ppDay', 1: 'ppWeek', 2: 'ppMonth'})

# ---- inputs and global variables
ppPeriod = _input('ppPeriod', ppDay)  # PivotPoint Calculation Period
PPBuffer = Arr(0, 0.0)
S1Buffer = Arr(0, 0.0)
R1Buffer = Arr(0, 0.0)
S2Buffer = Arr(0, 0.0)
R2Buffer = Arr(0, 0.0)
S3Buffer = Arr(0, 0.0)
R3Buffer = Arr(0, 0.0)
fontsize = 10
P = 0.0
S1 = 0.0
R1 = 0.0
S2 = 0.0
R2 = 0.0
S3 = 0.0
R3 = 0.0
LastHigh = 0.0
LastLow = 0.0
x = 0.0
drawBegin = False
dayOfWeek = 0

def OnInit():
    SetIndexBuffer(0, R3Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, R2Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, R1Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, PPBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, S1Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, S2Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, S3Buffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0.0)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LastHigh, LastLow, P, R1, R2, R3, S1, S2, S3, drawBegin
    limit = 0
    if ((ppPeriod == ppDay and Period() > PERIOD_D1) or (ppPeriod == ppWeek and Period() > PERIOD_W1)) or (ppPeriod == ppMonth and Period() > PERIOD_MN1):
        return 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    dWeek = 0
    for i in range(limit, rates_total - 1):
        if LastHigh == 0.0:
            LastHigh = high[i]
        else:
            if high[i] > LastHigh:
                LastHigh = high[i]
        if LastLow == 0.0:
            LastLow = low[i]
        else:
            if low[i] < LastLow:
                LastLow = low[i]
        TimeToStruct(time[i], dateStr1)
        TimeToStruct(time[i + 1], dateStr2)
        if dWeek == 0:
            dWeek = dateStr1.day_of_week
        if ((ppPeriod == ppDay and dateStr1.day != dateStr2.day) or (ppPeriod == ppWeek and dWeek == dateStr2.day_of_week)) or (ppPeriod == ppMonth and dateStr1.mon != dateStr2.mon):
            P = (LastHigh + LastLow + close[i]) / 3
            R1 = (2 * P) - LastLow
            S1 = (2 * P) - LastHigh
            R2 = P + (LastHigh - LastLow)
            S2 = P - (LastHigh - LastLow)
            R3 = (2 * P) + (LastHigh - (2 * LastLow))
            S3 = (2 * P) - ((2 * LastHigh) - LastLow)
            if drawBegin:
                PlotIndexSetInteger(0, PLOT_ARROW, 159)
                PlotIndexSetInteger(1, PLOT_ARROW, 159)
                PlotIndexSetInteger(2, PLOT_ARROW, 159)
                PlotIndexSetInteger(3, PLOT_ARROW, 159)
                PlotIndexSetInteger(4, PLOT_ARROW, 159)
                PlotIndexSetInteger(5, PLOT_ARROW, 159)
                PlotIndexSetInteger(6, PLOT_ARROW, 159)
                drawBegin = True
            if ppPeriod == ppWeek:
                dWeek = dateStr1.day_of_week
            LastLow = open[i + 1]
            LastHigh = open[i + 1]
        PPBuffer[i + 1] = P
        S1Buffer[i + 1] = S1
        R1Buffer[i + 1] = R1
        S2Buffer[i + 1] = S2
        R2Buffer[i + 1] = R2
        S3Buffer[i + 1] = S3
        R3Buffer[i + 1] = R3
    return rates_total

# ---- global variables initialised from expressions
dateStr1 = MqlDateTime()
dateStr2 = MqlDateTime()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pivotpoint(_MQL5Indicator):
    name = 'pivotpoint'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ppPeriod': _Choice({0: 'Day', 1: 'Week', 2: 'Month'}, default=0),  # PivotPoint Calculation Period
    }

