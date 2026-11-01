"""dailypivotshift_full — converted from MQL5: MQL5 Indicators/DailyPivotShift_Full/dailypivotshift_full.mq5

Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 15, 'indicator_plots': 15}, 'types': {1: 1, 2: 1, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5, 15: 5}, 'colors': {1: [16711680], 2: [16711935], 3: [7451452], 4: [7451452], 5: [65280], 6: [7451452], 7: [7451452], 8: [7451452], 9: [13382297], 10: [255], 11: [255], 12: [255], 13: [16711935], 14: [255], 15: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 1, 7: 3, 8: 1, 9: 1, 10: 1, 11: 1, 12: 2, 13: 1, 14: 3, 15: 1}, 'styles': {1: 4, 2: 4}, 'labels': {3: 'Pivot R3.0', 4: 'Pivot R2.5', 5: 'Pivot R2.0', 6: 'Pivot R1.5', 7: 'Pivot R1.0', 8: 'Pivot R0.5', 9: 'Pivot P', 10: 'Pivot S0.5', 11: 'Pivot S1.0', 12: 'Pivot S1.5', 13: 'Pivot S2.0', 14: 'Pivot S2.5', 15: 'Pivot S3.0'}, 'levels': [], 'description': [], 'name': 'dailypivotshift_full', 'source': 'MQL5 Indicators/DailyPivotShift_Full/dailypivotshift_full.mq5', 'folder': 'DailyPivotShift_Full', 'inputs': [{'mql': 'ShiftTime_', 'py': 'ShiftTime_', 'param': 'ShiftTime_', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ExtFormula', 'py': 'ExtFormula', 'param': 'ExtFormula', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Symbol_R30', 'py': 'Symbol_R30', 'param': 'Symbol_R30', 'type': 'int', 'default': 119, 'label': 'R30 level label', 'sinput': False}, {'mql': 'Symbol_R25', 'py': 'Symbol_R25', 'param': 'Symbol_R25', 'type': 'int', 'default': 158, 'label': 'R25 level label', 'sinput': False}, {'mql': 'Symbol_R20', 'py': 'Symbol_R20', 'param': 'Symbol_R20', 'type': 'int', 'default': 167, 'label': 'R20 level label', 'sinput': False}, {'mql': 'Symbol_R15', 'py': 'Symbol_R15', 'param': 'Symbol_R15', 'type': 'int', 'default': 158, 'label': 'R15 level label', 'sinput': False}, {'mql': 'Symbol_R10', 'py': 'Symbol_R10', 'param': 'Symbol_R10', 'type': 'int', 'default': 108, 'label': 'R10 level label', 'sinput': False}, {'mql': 'Symbol_R05', 'py': 'Symbol_R05', 'param': 'Symbol_R05', 'type': 'int', 'default': 158, 'label': 'R05 level label', 'sinput': False}, {'mql': 'Symbol_P', 'py': 'Symbol_P', 'param': 'Symbol_P', 'type': 'int', 'default': 167, 'label': 'P level label', 'sinput': False}, {'mql': 'Symbol_S05', 'py': 'Symbol_S05', 'param': 'Symbol_S05', 'type': 'int', 'default': 158, 'label': 'S05 level label', 'sinput': False}, {'mql': 'Symbol_S10', 'py': 'Symbol_S10', 'param': 'Symbol_S10', 'type': 'int', 'default': 108, 'label': 'S10 level label', 'sinput': False}, {'mql': 'Symbol_S15', 'py': 'Symbol_S15', 'param': 'Symbol_S15', 'type': 'int', 'default': 158, 'label': 'S15 level label', 'sinput': False}, {'mql': 'Symbol_S20', 'py': 'Symbol_S20', 'param': 'Symbol_S20', 'type': 'int', 'default': 167, 'label': 'S20 level label', 'sinput': False}, {'mql': 'Symbol_S25', 'py': 'Symbol_S25', 'param': 'Symbol_S25', 'type': 'int', 'default': 158, 'label': 'S25 level label', 'sinput': False}, {'mql': 'Symbol_S30', 'py': 'Symbol_S30', 'param': 'Symbol_S30', 'type': 'int', 'default': 119, 'label': 'S30 level label', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Number
Number_0 = 0
Number_1 = 1
Number_2 = 2
Number_3 = 3
_enum('Number', {0: 'Number_0', 1: 'Number_1', 2: 'Number_2', 3: 'Number_3'})

# ---- inputs and global variables
ShiftTime_ = _input('ShiftTime_', 1)
ExtFormula = _input('ExtFormula', Number_0)
Symbol_R30 = _input('Symbol_R30', 119)  # R30 level label
Symbol_R25 = _input('Symbol_R25', 158)  # R25 level label
Symbol_R20 = _input('Symbol_R20', 167)  # R20 level label
Symbol_R15 = _input('Symbol_R15', 158)  # R15 level label
Symbol_R10 = _input('Symbol_R10', 108)  # R10 level label
Symbol_R05 = _input('Symbol_R05', 158)  # R05 level label
Symbol_P = _input('Symbol_P', 167)  # P level label
Symbol_S05 = _input('Symbol_S05', 158)  # S05 level label
Symbol_S10 = _input('Symbol_S10', 108)  # S10 level label
Symbol_S15 = _input('Symbol_S15', 158)  # S15 level label
Symbol_S20 = _input('Symbol_S20', 167)  # S20 level label
Symbol_S25 = _input('Symbol_S25', 158)  # S25 level label
Symbol_S30 = _input('Symbol_S30', 119)  # S30 level label
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
P_Buffer = Arr(0, 0.0)
R05_Buffer = Arr(0, 0.0)
R10_Buffer = Arr(0, 0.0)
R15_Buffer = Arr(0, 0.0)
R20_Buffer = Arr(0, 0.0)
R25_Buffer = Arr(0, 0.0)
R30_Buffer = Arr(0, 0.0)
S05_Buffer = Arr(0, 0.0)
S10_Buffer = Arr(0, 0.0)
S15_Buffer = Arr(0, 0.0)
S20_Buffer = Arr(0, 0.0)
S25_Buffer = Arr(0, 0.0)
S30_Buffer = Arr(0, 0.0)
ShiftTime = 0
minbar = 0

def iBarShift_u(symbol, timeframe, time):
    if time < 0:
        return -1
    Arr_ = Arr(0, 0)
    time1 = 0
    time1 = SeriesInfoInteger(symbol, timeframe, SERIES_LASTBAR_DATE)
    if CopyTime(symbol, timeframe, _DT(time), _DT(time1), Arr_) > 0:
        size = ArraySize(Arr_)
        return size - 1
    else:
        return -1

def OnInit():
    global ShiftTime, minbar
    minbar = _idiv(1440 * 60, PeriodSeconds())
    ShiftTime = ShiftTime_
    if MathAbs(ShiftTime) > 23:
        ShiftTime = 0
    Comment('Shift Hours = ', ShiftTime)
    if ShiftTime < 0:
        ShiftTime = 0
    ShiftTime *= 3600
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, 0)
    ArraySetAsSeries(ExtMapBuffer1, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, ExtMapBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, 0)
    ArraySetAsSeries(ExtMapBuffer2, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, R30_Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, R25_Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, R20_Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, R15_Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, R10_Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, R05_Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, P_Buffer, INDICATOR_DATA)
    SetIndexBuffer(9, S05_Buffer, INDICATOR_DATA)
    SetIndexBuffer(10, S10_Buffer, INDICATOR_DATA)
    SetIndexBuffer(11, S15_Buffer, INDICATOR_DATA)
    SetIndexBuffer(12, S20_Buffer, INDICATOR_DATA)
    SetIndexBuffer(13, S25_Buffer, INDICATOR_DATA)
    SetIndexBuffer(14, S30_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, Symbol_R30)
    PlotIndexSetInteger(3, PLOT_ARROW, Symbol_R25)
    PlotIndexSetInteger(4, PLOT_ARROW, Symbol_R20)
    PlotIndexSetInteger(5, PLOT_ARROW, Symbol_R15)
    PlotIndexSetInteger(6, PLOT_ARROW, Symbol_R10)
    PlotIndexSetInteger(7, PLOT_ARROW, Symbol_R05)
    PlotIndexSetInteger(8, PLOT_ARROW, Symbol_P)
    PlotIndexSetInteger(9, PLOT_ARROW, Symbol_S05)
    PlotIndexSetInteger(10, PLOT_ARROW, Symbol_S10)
    PlotIndexSetInteger(11, PLOT_ARROW, Symbol_S15)
    PlotIndexSetInteger(12, PLOT_ARROW, Symbol_S20)
    PlotIndexSetInteger(13, PLOT_ARROW, Symbol_S25)
    PlotIndexSetInteger(14, PLOT_ARROW, Symbol_S30)
    PlotIndexSetString(2, PLOT_LABEL, 'Pivot R3.0')
    PlotIndexSetString(3, PLOT_LABEL, 'Pivot R2.5')
    PlotIndexSetString(4, PLOT_LABEL, 'Pivot R2.0')
    PlotIndexSetString(5, PLOT_LABEL, 'Pivot R1.5')
    PlotIndexSetString(6, PLOT_LABEL, 'Pivot R1.0')
    PlotIndexSetString(7, PLOT_LABEL, 'Pivot R0.5')
    PlotIndexSetString(8, PLOT_LABEL, 'Pivot P')
    PlotIndexSetString(9, PLOT_LABEL, 'Pivot S0.5')
    PlotIndexSetString(10, PLOT_LABEL, 'Pivot S1.0')
    PlotIndexSetString(11, PLOT_LABEL, 'Pivot S1.5')
    PlotIndexSetString(12, PLOT_LABEL, 'Pivot S2.0')
    PlotIndexSetString(13, PLOT_LABEL, 'Pivot S2.5')
    PlotIndexSetString(14, PLOT_LABEL, 'Pivot S3.0')
    ArraySetAsSeries(R30_Buffer, True)
    ArraySetAsSeries(R25_Buffer, True)
    ArraySetAsSeries(R20_Buffer, True)
    ArraySetAsSeries(R15_Buffer, True)
    ArraySetAsSeries(R10_Buffer, True)
    ArraySetAsSeries(R05_Buffer, True)
    ArraySetAsSeries(P_Buffer, True)
    ArraySetAsSeries(S05_Buffer, True)
    ArraySetAsSeries(S10_Buffer, True)
    ArraySetAsSeries(S15_Buffer, True)
    ArraySetAsSeries(S20_Buffer, True)
    ArraySetAsSeries(S25_Buffer, True)
    ArraySetAsSeries(S30_Buffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if ExtFormula == Number_0:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Pivot')
        PlotIndexSetString(0, PLOT_LABEL, 'Pivot')
        PlotIndexSetString(1, PLOT_LABEL, None)
    else:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Support&Resistance')
        PlotIndexSetString(0, PLOT_LABEL, 'Resistance')
        PlotIndexSetString(1, PLOT_LABEL, 'Support')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_P, _s_OnCalculate_R05, _s_OnCalculate_R10, _s_OnCalculate_R15, _s_OnCalculate_R20, _s_OnCalculate_R25, _s_OnCalculate_R30, _s_OnCalculate_S05, _s_OnCalculate_S10, _s_OnCalculate_S15, _s_OnCalculate_S20, _s_OnCalculate_S25, _s_OnCalculate_S30, _s_OnCalculate_hi, _s_OnCalculate_lo, _s_OnCalculate_yesterday_close, _s_OnCalculate_yesterday_high, _s_OnCalculate_yesterday_low
    if Period() >= PERIOD_D1:
        return 0
    if prev_calculated == rates_total:
        return rates_total
    begin_bar = 0
    cnt = 0
    day = 0
    new_day = 0
    minbar_ = 0
    cl = 0.0
    S = 0.0
    R = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        begin_bar = rates_total - 1
    else:
        begin_bar = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    tm = MqlDateTime()
    TimeToStruct(time[begin_bar] - ShiftTime, tm)
    new_day = tm.day_of_week
    minbar_ = minbar
    if minbar_ >= rates_total:
        minbar_ = rates_total - 1
    cnt = MathMax(begin_bar, minbar_)
    for cnt in range(cnt, 0 - 1, -1):
        TimeToStruct(time[cnt] - ShiftTime, tm)
        day = tm.day_of_week
        if day == new_day:
            if high[cnt] > _s_OnCalculate_hi:
                _s_OnCalculate_hi = high[cnt]
            if low[cnt] < _s_OnCalculate_lo or _s_OnCalculate_lo == 0:
                _s_OnCalculate_lo = low[cnt]
            cl = close[cnt]
        else:
            new_day = day
            if new_day > 0 and new_day < 6:
                _s_OnCalculate_yesterday_close = cl
                _s_OnCalculate_yesterday_high = _s_OnCalculate_hi
                _s_OnCalculate_yesterday_low = _s_OnCalculate_lo
                _s_OnCalculate_hi = 0.0
                _s_OnCalculate_lo = 0.0
                _s_OnCalculate_P = (_s_OnCalculate_yesterday_high + _s_OnCalculate_yesterday_low + _s_OnCalculate_yesterday_close) / 3
            _sw1 = ExtFormula
            if _sw1 == 1:
                R = _s_OnCalculate_P + _s_OnCalculate_P - _s_OnCalculate_yesterday_low
                S = _s_OnCalculate_P + _s_OnCalculate_P - _s_OnCalculate_yesterday_high
            elif _sw1 == 2:
                R = _s_OnCalculate_P + _s_OnCalculate_yesterday_high - _s_OnCalculate_yesterday_low
                S = _s_OnCalculate_P - _s_OnCalculate_yesterday_high + _s_OnCalculate_yesterday_low
            elif _sw1 == 3:
                R = _s_OnCalculate_P + _s_OnCalculate_P - _s_OnCalculate_yesterday_low - _s_OnCalculate_yesterday_low + _s_OnCalculate_yesterday_high
                S = _s_OnCalculate_P + _s_OnCalculate_P - _s_OnCalculate_yesterday_high - _s_OnCalculate_yesterday_high + _s_OnCalculate_yesterday_low
        if ExtFormula == 0:
            ExtMapBuffer1[cnt] = _s_OnCalculate_P
            ExtMapBuffer2[cnt] = 0.0
        else:
            ExtMapBuffer1[cnt] = R
            ExtMapBuffer2[cnt] = S
        _s_OnCalculate_R10 = NormalizeDouble((2 * _s_OnCalculate_P) - _s_OnCalculate_yesterday_low, Digits())
        _s_OnCalculate_S10 = NormalizeDouble((2 * _s_OnCalculate_P) - _s_OnCalculate_yesterday_high, Digits())
        _s_OnCalculate_R05 = NormalizeDouble((_s_OnCalculate_P + _s_OnCalculate_R10) / 2, Digits())
        _s_OnCalculate_S05 = NormalizeDouble((_s_OnCalculate_P + _s_OnCalculate_S10) / 2, Digits())
        _s_OnCalculate_R20 = NormalizeDouble(_s_OnCalculate_P + (_s_OnCalculate_yesterday_high - _s_OnCalculate_yesterday_low), Digits())
        _s_OnCalculate_S20 = NormalizeDouble(_s_OnCalculate_P - (_s_OnCalculate_yesterday_high - _s_OnCalculate_yesterday_low), Digits())
        _s_OnCalculate_R15 = NormalizeDouble((_s_OnCalculate_R10 + _s_OnCalculate_R20) / 2, Digits())
        _s_OnCalculate_S15 = NormalizeDouble((_s_OnCalculate_S10 + _s_OnCalculate_S20) / 2, Digits())
        _s_OnCalculate_R30 = NormalizeDouble((2 * _s_OnCalculate_P) + (_s_OnCalculate_yesterday_high - (2 * _s_OnCalculate_yesterday_low)), Digits())
        _s_OnCalculate_S30 = NormalizeDouble((2 * _s_OnCalculate_P) - ((2 * _s_OnCalculate_yesterday_high) - _s_OnCalculate_yesterday_low), Digits())
        _s_OnCalculate_R25 = NormalizeDouble((_s_OnCalculate_R20 + _s_OnCalculate_R30) / 2, Digits())
        _s_OnCalculate_S25 = NormalizeDouble((_s_OnCalculate_S20 + _s_OnCalculate_S30) / 2, Digits())
        R30_Buffer[cnt] = _s_OnCalculate_R30
        R25_Buffer[cnt] = _s_OnCalculate_R25
        R20_Buffer[cnt] = _s_OnCalculate_R20
        R15_Buffer[cnt] = _s_OnCalculate_R15
        R10_Buffer[cnt] = _s_OnCalculate_R10
        R05_Buffer[cnt] = _s_OnCalculate_R05
        P_Buffer[cnt] = _s_OnCalculate_P
        S05_Buffer[cnt] = _s_OnCalculate_S05
        S10_Buffer[cnt] = _s_OnCalculate_S10
        S15_Buffer[cnt] = _s_OnCalculate_S15
        S20_Buffer[cnt] = _s_OnCalculate_S20
        S25_Buffer[cnt] = _s_OnCalculate_S25
        S30_Buffer[cnt] = _s_OnCalculate_S30
    else:
        cnt = _range_end(cnt, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_yesterday_high = 0.0
_s_OnCalculate_yesterday_low = 0.0
_s_OnCalculate_yesterday_close = 0.0
_s_OnCalculate_P = 0.0
_s_OnCalculate_S05 = 0.0
_s_OnCalculate_R05 = 0.0
_s_OnCalculate_S10 = 0.0
_s_OnCalculate_R10 = 0.0
_s_OnCalculate_S15 = 0.0
_s_OnCalculate_R15 = 0.0
_s_OnCalculate_S20 = 0.0
_s_OnCalculate_R20 = 0.0
_s_OnCalculate_S25 = 0.0
_s_OnCalculate_R25 = 0.0
_s_OnCalculate_S30 = 0.0
_s_OnCalculate_R30 = 0.0
_s_OnCalculate_hi = 0.0
_s_OnCalculate_lo = 100000000.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailypivotshiftFull(_MQL5Indicator):
    name = 'dailypivotshift_full'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ShiftTime_': 1,
        'ExtFormula': _Choice({0: 'Number_0', 1: 'Number_1', 2: 'Number_2', 3: 'Number_3'}, default=0),
        'Symbol_R30': 119,  # R30 level label
        'Symbol_R25': 158,  # R25 level label
        'Symbol_R20': 167,  # R20 level label
        'Symbol_R15': 158,  # R15 level label
        'Symbol_R10': 108,  # R10 level label
        'Symbol_R05': 158,  # R05 level label
        'Symbol_P': 167,  # P level label
        'Symbol_S05': 158,  # S05 level label
        'Symbol_S10': 108,  # S10 level label
        'Symbol_S15': 158,  # S15 level label
        'Symbol_S20': 167,  # S20 level label
        'Symbol_S25': 158,  # S25 level label
        'Symbol_S30': 119,  # S30 level label
    }

