"""colorrvi_htf — converted from MQL5: MQL5 Indicators/ColorRVI_HTF/colorrvi_htf.mq5

The RVI indicator with the option to select a fixed time frame
Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 12}, 'colors': {1: [25600, 128], 2: [8421504, 65280, 16711935]}, 'widths': {2: 5}, 'styles': {}, 'labels': {1: 'RVI HTF', 2: 'Signal line'}, 'levels': [0.0], 'description': ['The RVI indicator with the option to select a fixed time frame'], 'name': 'colorrvi_htf', 'source': 'MQL5 Indicators/ColorRVI_HTF/colorrvi_htf.mq5', 'folder': 'ColorRVI_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'RVIPeriod', 'py': 'RVIPeriod', 'param': 'RVIPeriod', 'type': 'uint', 'default': 5, 'label': 'RVI period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
RVIPeriod = _input('RVIPeriod', 5)  # RVI period
UpRVI = Arr(0, 0.0)
DnRVI = Arr(0, 0.0)
RVISignal = Arr(0, 0.0)
ColorRVISignal = Arr(0, 0.0)
Init = False
min_rates_total = 0
RVI_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Init, RVI_Handle, min_rates_total
    min_rates_total = 3
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('The RVI indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    RVI_Handle = iRVI(None, TimeFrame, RVIPeriod)
    if RVI_Handle == INVALID_HANDLE:
        Print(' Failed to get the RVI indicator handle')
        Init = False
        return INIT_FAILED
    SetIndexBuffer(0, UpRVI, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpRVI, True)
    SetIndexBuffer(1, DnRVI, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DnRVI, True)
    SetIndexBuffer(2, RVISignal, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(RVISignal, True)
    SetIndexBuffer(3, ColorRVISignal, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorRVISignal, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RVI(' + GetStringTimeframe(TimeFrame) + ', ' + _str(RVIPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 3)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    if BarsCalculated(RVI_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    RVI = Arr(2, 0.0, dyn=False)
    Signal = Arr(2, 0.0, dyn=False)
    RVITime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpRVI[bar] = EMPTY_VALUE
        DnRVI[bar] = EMPTY_VALUE
        RVISignal[bar] = EMPTY_VALUE
        ColorRVISignal[bar] = 0.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, RVITime) <= 0:
            return 0
        if time[bar] >= RVITime[0] and time[bar + 1] < RVITime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(RVI_Handle, MAIN_LINE, _DT(time[bar]), 2, RVI) <= 0:
                return 0
            if CopyBuffer(RVI_Handle, SIGNAL_LINE, _DT(time[bar]), 2, Signal) <= 0:
                return 0
            RVISignal[bar] = Signal[1]
            UpRVI[bar] = 0.0
            DnRVI[bar] = 0.0
            if RVI[1] > 0.0:
                UpRVI[bar] = RVI[1]
            if RVI[1] < 0.0:
                UpRVI[bar] = RVI[1]
            if RVI[1] > RVISignal[bar]:
                ColorRVISignal[bar] = 1.0
            if RVI[1] < RVISignal[bar]:
                ColorRVISignal[bar] = 2.0
        if UpRVI[bar + 1] != EMPTY_VALUE and UpRVI[bar] == EMPTY_VALUE:
            UpRVI[bar] = UpRVI[bar + 1]
            DnRVI[bar] = DnRVI[bar + 1]
            RVISignal[bar] = RVISignal[bar + 1]
            ColorRVISignal[bar] = ColorRVISignal[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorrviHtf(_MQL5Indicator):
    name = 'colorrvi_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'RVIPeriod': 5,  # RVI period
    }

