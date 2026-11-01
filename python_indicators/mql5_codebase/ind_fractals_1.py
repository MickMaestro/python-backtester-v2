"""ind-fractals-1 — converted from MQL5: MQL5 Indicators/Ind-Fractals-1/ind-fractals-1.mq5

Fractals of different time periods on one chart
Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [65280], 2: [65280], 3: [255], 4: [255], 5: [16711680], 6: [16711680], 7: [16711935], 8: [16711935]}, 'widths': {1: 5, 2: 5, 3: 3, 4: 3, 5: 2, 6: 2, 7: 1, 8: 1}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Fractals of different time periods on one chart'], 'name': 'ind-fractals-1', 'source': 'MQL5 Indicators/Ind-Fractals-1/ind-fractals-1.mq5', 'folder': 'Ind-Fractals-1', 'inputs': [{'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16388, 'label': '4 indicator chart period', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16385, 'label': '3 indicator chart period', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 30, 'label': '2 indicator chart period', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 15, 'label': '1 indicator chart period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame4 = _input('TimeFrame4', PERIOD_H4)  # 4 indicator chart period
TimeFrame3 = _input('TimeFrame3', PERIOD_H1)  # 3 indicator chart period
TimeFrame2 = _input('TimeFrame2', PERIOD_M30)  # 2 indicator chart period
TimeFrame1 = _input('TimeFrame1', PERIOD_M15)  # 1 indicator chart period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
ExtLineBuffer7 = Arr(0, 0.0)
ExtLineBuffer8 = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0
min_rates_ = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global ATR_Handle, min_rates_, min_rates_total
    MaxTimeFrame = MathMax(MathMax(MathMax(TimeFrame1, TimeFrame2), TimeFrame3), TimeFrame4)
    res = _idiv(PeriodSeconds(MaxTimeFrame), PeriodSeconds(PERIOD_CURRENT))
    min_rates_ = _int((res * 2) + MathCeil(_idiv(res, 2)))
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, min_rates_)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer6, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer7, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer8, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'Up Fractals(' + GetStringTimeframe(TimeFrame4) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Dn Fractals(' + GetStringTimeframe(TimeFrame4) + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'Up Fractals(' + GetStringTimeframe(TimeFrame3) + ')')
    PlotIndexSetString(3, PLOT_LABEL, 'Dn Fractals(' + GetStringTimeframe(TimeFrame3) + ')')
    PlotIndexSetString(4, PLOT_LABEL, 'Up Fractals(' + GetStringTimeframe(TimeFrame2) + ')')
    PlotIndexSetString(5, PLOT_LABEL, 'Dn Fractals(' + GetStringTimeframe(TimeFrame2) + ')')
    PlotIndexSetString(6, PLOT_LABEL, 'Up Fractals(' + GetStringTimeframe(TimeFrame1) + ')')
    PlotIndexSetString(7, PLOT_LABEL, 'Dn Fractals(' + GetStringTimeframe(TimeFrame1) + ')')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    PlotIndexSetInteger(5, PLOT_ARROW, 159)
    PlotIndexSetInteger(6, PLOT_ARROW, 159)
    PlotIndexSetInteger(7, PLOT_ARROW, 159)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    ArraySetAsSeries(ExtLineBuffer7, True)
    ArraySetAsSeries(ExtLineBuffer8, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ind-Fractals-1')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated + min_rates_
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtLineBuffer1[bar] = EMPTY_VALUE
        ExtLineBuffer2[bar] = EMPTY_VALUE
        ExtLineBuffer3[bar] = EMPTY_VALUE
        ExtLineBuffer4[bar] = EMPTY_VALUE
        ExtLineBuffer5[bar] = EMPTY_VALUE
        ExtLineBuffer6[bar] = EMPTY_VALUE
        ExtLineBuffer7[bar] = EMPTY_VALUE
        ExtLineBuffer8[bar] = EMPTY_VALUE
        if FindUpFractal(rates_total, TimeFrame1, high, bar):
            ExtLineBuffer1[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if FindDnFractal(rates_total, TimeFrame1, low, bar):
            ExtLineBuffer2[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if FindUpFractal(rates_total, TimeFrame2, high, bar):
            ExtLineBuffer3[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if FindDnFractal(rates_total, TimeFrame2, low, bar):
            ExtLineBuffer4[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if FindUpFractal(rates_total, TimeFrame3, high, bar):
            ExtLineBuffer5[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if FindDnFractal(rates_total, TimeFrame3, low, bar):
            ExtLineBuffer6[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if FindUpFractal(rates_total, TimeFrame4, high, bar):
            ExtLineBuffer7[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if FindDnFractal(rates_total, TimeFrame4, low, bar):
            ExtLineBuffer8[bar] = low[bar] - ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def FindUpFractal(Bars_, period, High, index):
    res = _idiv(PeriodSeconds(period), PeriodSeconds(PERIOD_CURRENT))
    Per = _int((res * 2) + MathCeil(_idiv(res, 2)))
    if index < Per or index > (Bars_ - Per):
        return False
    for iii in range(1, Per + 1):
        if (index + iii) >= Bars_ or (index - iii) < 0:
            return False
        if High[index + iii] > High[index]:
            return False
        if High[index - iii] >= High[index]:
            return False
    return True

def FindDnFractal(Bars_, period, Low, index):
    res = _idiv(PeriodSeconds(period), PeriodSeconds(PERIOD_CURRENT))
    Per = _int((res * 2) + MathCeil(_idiv(res, 2)))
    if index < Per or index > (Bars_ - Per):
        return False
    for iii in range(1, Per + 1):
        if (index + iii) >= Bars_ or (index - iii) < 0:
            return False
        if Low[index + iii] < Low[index]:
            return False
        if Low[index - iii] <= Low[index]:
            return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IndFractals1(_MQL5Indicator):
    name = 'ind-fractals-1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # 4 indicator chart period
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # 3 indicator chart period
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # 2 indicator chart period
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=15),  # 1 indicator chart period
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

