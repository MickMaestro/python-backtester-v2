"""InOutBar — converted from MQL5: MQL5 Indicators/InOutBar/InOutBar.mq5

Copyright: Copyright © 2005, Kalenzo; Link: http://www.fxservice.eu; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Kalenzo', 'link': 'http://www.fxservice.eu', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [65280], 2: [65280], 3: [16748574], 4: [16748574]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {}, 'labels': {1: 'High Up', 2: 'Low Up', 3: 'High Down', 4: 'Low Down'}, 'levels': [], 'description': [], 'name': 'InOutBar', 'source': 'MQL5 Indicators/InOutBar/InOutBar.mq5', 'folder': 'InOutBar', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpHiBuffer = Arr(0, 0.0)
UpLoBuffer = Arr(0, 0.0)
DnHiBuffer = Arr(0, 0.0)
DnLoBuffer = Arr(0, 0.0)
min_rates_total = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global min_rates_total
    min_rates_total = _idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT))
    shortname = Box("")
    StringConcatenate(shortname, 'InOutBar(', GetStringTimeframe(TimeFrame), ', ', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, UpHiBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(0, PLOT_ARROW, 218)
    ArraySetAsSeries(UpHiBuffer, True)
    SetIndexBuffer(1, UpLoBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(1, PLOT_ARROW, 217)
    ArraySetAsSeries(UpLoBuffer, True)
    SetIndexBuffer(2, DnHiBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnHiBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(2, PLOT_ARROW, 217)
    SetIndexBuffer(3, DnLoBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnLoBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(3, PLOT_ARROW, 218)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    iHigh_ = Arr(2, 0.0, dyn=False)
    iLow_ = Arr(2, 0.0, dyn=False)
    iTime_ = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if CopyTime(None, TimeFrame, _DT(time[bar]), 1, iTime_) < 1:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            _s_OnCalculate_LastCountBar = bar
        UpHiBuffer[bar] = 0.0
        UpLoBuffer[bar] = 0.0
        DnHiBuffer[bar] = 0.0
        DnLoBuffer[bar] = 0.0
        if CopyHigh(None, TimeFrame, _DT(time[bar]), 2, iHigh_) < 2:
            return 0
        if CopyLow(None, TimeFrame, _DT(time[bar]), 2, iLow_) < 2:
            return 0
        if iHigh_[0] > iHigh_[1] and iLow_[0] < iLow_[1]:
            UpHiBuffer[bar] = high[bar]
            UpLoBuffer[bar] = low[bar]
        if iHigh_[0] < iHigh_[1] and iLow_[0] > iLow_[1]:
            DnHiBuffer[bar] = high[bar]
            DnLoBuffer[bar] = low[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class InOutBar(_MQL5Indicator):
    name = 'InOutBar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

