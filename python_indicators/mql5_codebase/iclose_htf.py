"""iclose_htf — converted from MQL5: MQL5 Indicators/iClose_HTF/iclose_htf.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [16711935]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [], 'description': [], 'name': 'iclose_htf', 'source': 'MQL5 Indicators/iClose_HTF/iclose_htf.mq5', 'folder': 'iClose_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in points
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Init = False
dPriceShift = 0.0
Symbol_ = ""
Word = ""
min_rates_total = 0

def OnInit():
    global Init, Symbol_, Word, dPriceShift, min_rates_total
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('The iClose indicator chart period cannot be less than the current chart period')
        Init = False
        return
    min_rates_total = _idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT)) * 3
    Symbol_ = Symbol()
    Word = 'iClose' + ' indicator: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'iClose')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    iClose_ = Arr(1, 0.0, dyn=False)
    limit = 0
    bar = 0
    iTime_ = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 2
        _s_OnCalculate_LastCountBar = limit
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar + 1] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            _s_OnCalculate_LastCountBar = bar
            IndBuffer[bar + 1] = close[bar + 1] + dPriceShift
    else:
        bar = _range_end(bar, 0 - 1, -1)
    IndBuffer[0] = close[0] + dPriceShift
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IcloseHtf(_MQL5Indicator):
    name = 'iclose_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in points
    }

