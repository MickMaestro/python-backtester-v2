"""waddahattarfibo — converted from MQL5: MQL5 Indicators/Waddah Attar Fibo/waddahattarfibo.mq5

Waddah Attar Fibo
Copyright: Copyright © 2007, Waddah Attar waddahattar@hotmail.com; Link: waddahattar@hotmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Waddah Attar waddahattar@hotmail.com', 'link': 'waddahattar@hotmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 12}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5}, 'colors': {1: [8519755], 2: [8519755], 3: [5197615], 4: [8388736], 5: [255], 6: [16711680], 7: [16711680], 8: [255], 9: [8388736], 10: [5197615], 11: [8519755], 12: [8519755]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1}, 'styles': {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 11: 4, 12: 4}, 'labels': {1: 'Fibo +0.764', 2: 'Fibo +0.618', 3: 'Fibo +0.50', 4: 'Fibo +0.382', 5: 'Fibo +0.236', 6: 'Fibo +0', 7: 'Fibo -0', 8: 'Fibo -0.236', 9: 'Fibo -0.382', 10: 'Fibo -0.50', 11: 'Fibo -0.618', 12: 'Fibo -0.764'}, 'levels': [], 'description': ['Waddah Attar Fibo'], 'name': 'waddahattarfibo', 'source': 'MQL5 Indicators/Waddah Attar Fibo/waddahattarfibo.mq5', 'folder': 'Waddah Attar Fibo', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16408, 'label': 'Chart period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_D1)  # Chart period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
ExtLineBuffer0 = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
ExtLineBuffer7 = Arr(0, 0.0)
ExtLineBuffer8 = Arr(0, 0.0)
ExtLineBuffer9 = Arr(0, 0.0)
ExtLineBuffer10 = Arr(0, 0.0)
ExtLineBuffer11 = Arr(0, 0.0)
Symbol_ = ""
dPriceShift = 0.0
min_rates_total = 0
Init = False

def OnInit():
    global Init, Symbol_, dPriceShift, min_rates_total
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Waddah Attar Fibo indicator timeframe cannot be less than the current chart period')
        Init = False
        return 1
    Symbol_ = Symbol()
    shortname = 'Waddah Attar Fibo' + ' indicator: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    min_rates_total = _idiv(2 * PeriodSeconds(TimeFrame), PeriodSeconds())
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer6, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer7, INDICATOR_DATA)
    SetIndexBuffer(8, ExtLineBuffer8, INDICATOR_DATA)
    SetIndexBuffer(9, ExtLineBuffer9, INDICATOR_DATA)
    SetIndexBuffer(10, ExtLineBuffer10, INDICATOR_DATA)
    SetIndexBuffer(11, ExtLineBuffer11, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(9, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(10, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(11, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(9, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(10, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(11, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(6, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(7, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(8, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(9, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(10, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(11, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtLineBuffer0, True)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    ArraySetAsSeries(ExtLineBuffer7, True)
    ArraySetAsSeries(ExtLineBuffer8, True)
    ArraySetAsSeries(ExtLineBuffer9, True)
    ArraySetAsSeries(ExtLineBuffer10, True)
    ArraySetAsSeries(ExtLineBuffer11, True)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or (not Init):
        return 0
    iHigh_ = Arr(2, 0.0, dyn=False)
    iLow_ = Arr(2, 0.0, dyn=False)
    Range = 0.0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(iHigh_, True)
    ArraySetAsSeries(iLow_, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if CopyHigh(Symbol_, TimeFrame, _DT(time[bar]), 2, iHigh_) <= 0:
            return 0
        if CopyLow(Symbol_, TimeFrame, _DT(time[bar]), 2, iLow_) <= 0:
            return 0
        Range = iHigh_[0] - iLow_[0]
        ExtLineBuffer0[bar] = iHigh_[0] + (Range * 0.764) + dPriceShift
        ExtLineBuffer1[bar] = iHigh_[0] + (Range * 0.618) + dPriceShift
        ExtLineBuffer2[bar] = iHigh_[0] + (Range * 0.5) + dPriceShift
        ExtLineBuffer3[bar] = iHigh_[0] + (Range * 0.382) + dPriceShift
        ExtLineBuffer4[bar] = iHigh_[0] + (Range * 0.236) + dPriceShift
        ExtLineBuffer5[bar] = iHigh_[0] + dPriceShift
        ExtLineBuffer6[bar] = iLow_[0] + dPriceShift
        ExtLineBuffer7[bar] = iLow_[0] - (Range * 0.236) + dPriceShift
        ExtLineBuffer8[bar] = iLow_[0] - (Range * 0.382) + dPriceShift
        ExtLineBuffer9[bar] = iLow_[0] - (Range * 0.5) + dPriceShift
        ExtLineBuffer10[bar] = iLow_[0] - (Range * 0.618) + dPriceShift
        ExtLineBuffer11[bar] = iLow_[0] - (Range * 0.764) + dPriceShift
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Waddahattarfibo(_MQL5Indicator):
    name = 'waddahattarfibo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Chart period
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

