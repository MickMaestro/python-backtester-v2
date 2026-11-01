"""dailypivotpoints_full — converted from MQL5: MQL5 Indicators/DailyPivotPoints_Full/dailypivotpoints_full.mq5

Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 15, 'indicator_plots': 15}, 'types': {1: 1, 2: 1, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5, 15: 5}, 'colors': {1: [16711680], 2: [16711935], 3: [7451452], 4: [7451452], 5: [65280], 6: [7451452], 7: [7451452], 8: [7451452], 9: [13382297], 10: [255], 11: [255], 12: [255], 13: [16711935], 14: [255], 15: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 1, 7: 3, 8: 1, 9: 1, 10: 1, 11: 1, 12: 2, 13: 1, 14: 3, 15: 1}, 'styles': {1: 4, 2: 4}, 'labels': {3: 'Pivot R3.0', 4: 'Pivot R2.5', 5: 'Pivot R2.0', 6: 'Pivot R1.5', 7: 'Pivot R1.0', 8: 'Pivot R0.5', 9: 'Pivot P', 10: 'Pivot S0.5', 11: 'Pivot S1.0', 12: 'Pivot S1.5', 13: 'Pivot S2.0', 14: 'Pivot S2.5', 15: 'Pivot S3.0'}, 'levels': [], 'description': [], 'name': 'dailypivotpoints_full', 'source': 'MQL5 Indicators/DailyPivotPoints_Full/dailypivotpoints_full.mq5', 'folder': 'DailyPivotPoints_Full', 'inputs': [{'mql': 'ExtFormula', 'py': 'ExtFormula', 'param': 'ExtFormula', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ExtHowManyDays', 'py': 'ExtHowManyDays', 'param': 'ExtHowManyDays', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'ExtDraw', 'py': 'ExtDraw', 'param': 'ExtDraw', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Symbol_R30', 'py': 'Symbol_R30', 'param': 'Symbol_R30', 'type': 'int', 'default': 119, 'label': 'R30 level label', 'sinput': False}, {'mql': 'Symbol_R25', 'py': 'Symbol_R25', 'param': 'Symbol_R25', 'type': 'int', 'default': 158, 'label': 'R25 level label', 'sinput': False}, {'mql': 'Symbol_R20', 'py': 'Symbol_R20', 'param': 'Symbol_R20', 'type': 'int', 'default': 167, 'label': 'R20 level label', 'sinput': False}, {'mql': 'Symbol_R15', 'py': 'Symbol_R15', 'param': 'Symbol_R15', 'type': 'int', 'default': 158, 'label': 'R15 level label', 'sinput': False}, {'mql': 'Symbol_R10', 'py': 'Symbol_R10', 'param': 'Symbol_R10', 'type': 'int', 'default': 108, 'label': 'R10 level label', 'sinput': False}, {'mql': 'Symbol_R05', 'py': 'Symbol_R05', 'param': 'Symbol_R05', 'type': 'int', 'default': 158, 'label': 'R05 level label', 'sinput': False}, {'mql': 'Symbol_P', 'py': 'Symbol_P', 'param': 'Symbol_P', 'type': 'int', 'default': 167, 'label': 'P level label', 'sinput': False}, {'mql': 'Symbol_S05', 'py': 'Symbol_S05', 'param': 'Symbol_S05', 'type': 'int', 'default': 158, 'label': 'S05 level label', 'sinput': False}, {'mql': 'Symbol_S10', 'py': 'Symbol_S10', 'param': 'Symbol_S10', 'type': 'int', 'default': 108, 'label': 'S10 level label', 'sinput': False}, {'mql': 'Symbol_S15', 'py': 'Symbol_S15', 'param': 'Symbol_S15', 'type': 'int', 'default': 158, 'label': 'S15 level label', 'sinput': False}, {'mql': 'Symbol_S20', 'py': 'Symbol_S20', 'param': 'Symbol_S20', 'type': 'int', 'default': 167, 'label': 'S20 level label', 'sinput': False}, {'mql': 'Symbol_S25', 'py': 'Symbol_S25', 'param': 'Symbol_S25', 'type': 'int', 'default': 158, 'label': 'S25 level label', 'sinput': False}, {'mql': 'Symbol_S30', 'py': 'Symbol_S30', 'param': 'Symbol_S30', 'type': 'int', 'default': 119, 'label': 'S30 level label', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Number
Number_0 = 0
Number_1 = 1
Number_2 = 2
Number_3 = 3
_enum('Number', {0: 'Number_0', 1: 'Number_1', 2: 'Number_2', 3: 'Number_3'})

# ---- inputs and global variables
ExtFormula = _input('ExtFormula', Number_0)
ExtHowManyDays = _input('ExtHowManyDays', 30)
ExtDraw = _input('ExtDraw', True)
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
    draw_begin = 0
    if ExtHowManyDays < 1:
        draw_begin = 0
    else:
        draw_begin = ExtHowManyDays
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, draw_begin)
    ArraySetAsSeries(ExtMapBuffer1, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, ExtMapBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, 0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, draw_begin)
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
    if ExtDraw:
        if ExtFormula == Number_0:
            IndicatorSetString(INDICATOR_SHORTNAME, 'Pivot')
            PlotIndexSetString(0, PLOT_LABEL, 'Pivot')
            PlotIndexSetString(1, PLOT_LABEL, None)
        else:
            IndicatorSetString(INDICATOR_SHORTNAME, 'Support&Resistance')
            PlotIndexSetString(0, PLOT_LABEL, 'Resistance')
            PlotIndexSetString(1, PLOT_LABEL, 'Support')
    else:
        PlotIndexSetString(0, PLOT_LABEL, None)
        PlotIndexSetString(1, PLOT_LABEL, None)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Period() >= PERIOD_D1:
        return 0
    begin_bar = 0
    first_bar = 0
    last_bar = 0
    cnt = 0
    copy = 0
    yesterday_high = 0.0
    yesterday_low = 0.0
    yesterday_close = 0.0
    today_open = 0.0
    P = 0.0
    p_ = 0.0
    S = 0.0
    R = 0.0
    S05 = 0.0
    R05 = 0.0
    S10 = 0.0
    R10 = 0.0
    S15 = 0.0
    R15 = 0.0
    S20 = 0.0
    R20 = 0.0
    S25 = 0.0
    R25 = 0.0
    S30 = 0.0
    R30 = 0.0
    iClose_ = Arr(0, 0.0)
    iOpen_ = Arr(0, 0.0)
    iHigh_ = Arr(0, 0.0)
    iLow_ = Arr(0, 0.0)
    iTime_ = Arr(0, 0)
    if ExtHowManyDays < 1:
        begin_bar = Bars(None, PERIOD_D1) - 2
    else:
        begin_bar = ExtHowManyDays - 1
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(iTime_, True)
    ArraySetAsSeries(iClose_, True)
    ArraySetAsSeries(iOpen_, True)
    ArraySetAsSeries(iHigh_, True)
    ArraySetAsSeries(iLow_, True)
    copy = begin_bar + 2
    if CopyTime(None, PERIOD_D1, 0, copy, iTime_) < copy:
        return 0
    if CopyClose(None, PERIOD_D1, 0, copy, iClose_) < copy:
        return 0
    if CopyOpen(None, PERIOD_D1, 0, copy, iOpen_) < copy:
        return 0
    if CopyHigh(None, PERIOD_D1, 0, copy, iHigh_) < copy:
        return 0
    if CopyLow(None, PERIOD_D1, 0, copy, iLow_) < copy:
        return 0
    cnt = 0
    while True:
        if iTime_[0] >= (time[0] - (PERIOD_D1 * 60)):
            break
        cnt += 1
        if cnt > 5:
            return 0
        Sleep(1000)
    if ExtDraw == False or prev_calculated != 0:
        begin_bar = 0
    cnt = begin_bar
    for cnt in range(cnt, 0 - 1, -1):
        if cnt < rates_total:
            ExtMapBuffer1[cnt] = 0.0
            ExtMapBuffer2[cnt] = 0.0
        yesterday_close = iClose_[cnt + 1]
        today_open = iOpen_[cnt]
        yesterday_high = iHigh_[cnt + 1]
        yesterday_low = iLow_[cnt + 1]
        P = (yesterday_high + yesterday_low + yesterday_close + today_open) / 4
        _sw1 = ExtFormula
        if _sw1 == 1:
            R = P + P - yesterday_low
            S = P + P - yesterday_high
        elif _sw1 == 2:
            R = P + yesterday_high - yesterday_low
            S = P - yesterday_high + yesterday_low
        elif _sw1 == 3:
            R = P + P - yesterday_low - yesterday_low + yesterday_high
            S = P + P - yesterday_high - yesterday_high + yesterday_low
        if ExtDraw == True:
            first_bar = iBarShift_u("", 0, iTime_[cnt]) - 1
            if cnt > 0:
                last_bar = iBarShift_u("", 0, iTime_[cnt - 1]) - 1
            else:
                last_bar = 0
            while first_bar >= last_bar:
                if (first_bar == last_bar and last_bar > 0) or first_bar < 0:
                    break
                if ExtFormula == 0:
                    ExtMapBuffer1[first_bar] = P
                else:
                    ExtMapBuffer1[first_bar] = R
                    ExtMapBuffer2[first_bar] = S
                p_ = NormalizeDouble((yesterday_high + yesterday_low + yesterday_close) / 3, Digits())
                R10 = NormalizeDouble((2 * p_) - yesterday_low, Digits())
                S10 = NormalizeDouble((2 * p_) - yesterday_high, Digits())
                R05 = NormalizeDouble((p_ + R10) / 2, Digits())
                S05 = NormalizeDouble((p_ + S10) / 2, Digits())
                R20 = NormalizeDouble(p_ + (yesterday_high - yesterday_low), Digits())
                S20 = NormalizeDouble(p_ - (yesterday_high - yesterday_low), Digits())
                R15 = NormalizeDouble((R10 + R20) / 2, Digits())
                S15 = NormalizeDouble((S10 + S20) / 2, Digits())
                R30 = NormalizeDouble((2 * p_) + (yesterday_high - (2 * yesterday_low)), Digits())
                S30 = NormalizeDouble((2 * p_) - ((2 * yesterday_high) - yesterday_low), Digits())
                R25 = NormalizeDouble((R20 + R30) / 2, Digits())
                S25 = NormalizeDouble((S20 + S30) / 2, Digits())
                R30_Buffer[first_bar] = R30
                R25_Buffer[first_bar] = R25
                R20_Buffer[first_bar] = R20
                R15_Buffer[first_bar] = R15
                R10_Buffer[first_bar] = R10
                R05_Buffer[first_bar] = R05
                P_Buffer[first_bar] = p_
                S05_Buffer[first_bar] = S05
                S10_Buffer[first_bar] = S10
                S15_Buffer[first_bar] = S15
                S20_Buffer[first_bar] = S20
                S25_Buffer[first_bar] = S25
                S30_Buffer[first_bar] = S30
                first_bar -= 1
    else:
        cnt = _range_end(cnt, 0 - 1, -1)
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailypivotpointsFull(_MQL5Indicator):
    name = 'dailypivotpoints_full'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtFormula': _Choice({0: 'Number_0', 1: 'Number_1', 2: 'Number_2', 3: 'Number_3'}, default=0),
        'ExtHowManyDays': 30,
        'ExtDraw': True,
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

