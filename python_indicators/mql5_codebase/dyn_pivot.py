"""dyn_pivot — converted from MQL5: MQL5 Indicators/Dyn_Pivot/dyn_pivot.mq5

An indicator of pivot points
Copyright: Copyright © 2006, Modest; Link: http://forexsystems.ru/phpBB/index.php; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Modest', 'link': 'http://forexsystems.ru/phpBB/index.php', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [36095]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Dyn_Pivot'}, 'levels': [], 'description': ['An indicator of pivot points'], 'name': 'dyn_pivot', 'source': 'MQL5 Indicators/Dyn_Pivot/dyn_pivot.mq5', 'folder': 'Dyn_Pivot', 'inputs': [{'mql': 'Formula', 'py': 'Formula', 'param': 'Formula', 'type': 'bool', 'default': False, 'label': 'Calculation algorithm', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Formula = _input('Formula', False)  # Calculation algorithm
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
LineBuffer = Arr(0, 0.0)
FP = 0.0
FH = 0.0
FL = 0.0
min_rates_total = 0
ret = 0

def isNewDay(Time, shift):
    tm = MqlDateTime()
    TimeToStruct(Time[shift], tm)
    if (not tm.hour) and (not tm.min):
        return True
    return False

def GetFPofDay(Rates_Total, Time, High, Low, Close, shift):
    global FH, FL, FP
    tm = MqlDateTime()
    TimeToStruct(Time[shift + 1], tm)
    prevDay = tm.day
    iii = 1
    while tm.day == prevDay:
        iii += 1
        if (shift + iii) == Rates_Total:
            break
        TimeToStruct(Time[shift + iii], tm)
    iii -= 1
    FH = High[ArrayMaximum(High, shift + 1, iii)]
    FL = Low[ArrayMinimum(Low, shift + 1, iii)]
    if not Formula:
        FP = NormalizeDouble((FH + FL + Close[shift + 1]) / 3.0, Digits())
    else:
        FP = NormalizeDouble((FH + FL + (2 * Close[shift + 1])) / 4.0, Digits())
    return FP

def SetNullBarValue(Rates_Total, Time, High, Low, Close, shift):
    global FH, FL, FP
    tm = MqlDateTime()
    TimeToStruct(Time[shift], tm)
    currDay = tm.day
    iii = 1
    TimeToStruct(Time[shift + 1], tm)
    while tm.day == currDay:
        iii += 1
        if (shift + iii) == Rates_Total:
            break
        TimeToStruct(Time[shift + iii], tm)
    if iii >= 2:
        iii -= 2
        for cnt in range(iii, 0, -1):
            LineBuffer[shift + cnt] = 0.0
        FH = High[ArrayMaximum(High, shift, iii + 1)]
        FL = Low[ArrayMinimum(Low, shift, iii + 1)]
        if not Formula:
            FP = NormalizeDouble((FH + FL + Close[shift + 1]) / 3.0, Digits())
        else:
            FP = NormalizeDouble((FH + FL + (2 * Close[shift + 1])) / 4.0, Digits())
        LineBuffer[shift] = FP
    return

def OnInit():
    global FH, FL, FP, min_rates_total, ret
    if Period() > PERIOD_H6:
        Print('Indicator period cannot be greater than H6')
        return INIT_FAILED
    ret = _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
    min_rates_total = ret + 1
    FP = 0.0
    FH = 0.0
    FL = 0.0
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(LineBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dyn_Pivot')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2 - min_rates_total
        limit = rates_total - 1
        iii = 1
        tm = MqlDateTime()
        TimeToStruct(time[limit], tm)
        firstDay = tm.day
        TimeToStruct(time[limit - iii], tm)
        while tm.day == firstDay:
            iii += 1
            if (limit - iii) == 0:
                break
            TimeToStruct(time[limit - iii], tm)
        limit -= iii + ret
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if isNewDay(time, bar):
            LineBuffer[bar] = GetFPofDay(rates_total, time, high, low, close, bar)
        else:
            LineBuffer[bar] = 0.0
        if not bar:
            SetNullBarValue(rates_total, time, high, low, close, bar)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynPivot(_MQL5Indicator):
    name = 'dyn_pivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Formula': False,  # Calculation algorithm
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

