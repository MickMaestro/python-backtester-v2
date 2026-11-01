"""pricechanel_htf — converted from MQL5: MQL5 Indicators/PriceChanel_HTF/pricechanel_htf.mq5

Copyright: Copyright © 2009, MaxxMT; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, MaxxMT', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [13828244], 2: [36095]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper Price Chanel', 2: 'Lower Price Chanel'}, 'levels': [], 'description': [], 'name': 'pricechanel_htf', 'source': 'MQL5 Indicators/PriceChanel_HTF/pricechanel_htf.mq5', 'folder': 'PriceChanel_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'UpPeriod', 'py': 'UpPeriod', 'param': 'UpPeriod', 'type': 'uint', 'default': 12, 'label': 'Maximums searching period', 'sinput': False}, {'mql': 'DnPeriod', 'py': 'DnPeriod', 'param': 'DnPeriod', 'type': 'uint', 'default': 12, 'label': 'Minimums searching period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
UpPeriod = _input('UpPeriod', 12)  # Maximums searching period
DnPeriod = _input('DnPeriod', 12)  # Minimums searching period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
min_rates_total = 0
Init = False
iHigh_v = Arr(0, 0.0)
iLow_v = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Init, min_rates_total
    min_rates_ = _int(MathMax(UpPeriod, DnPeriod))
    min_rates_total = _idiv(min_rates_ * PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT))
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Price Chanel HTF indicator chart period cannot be less than the current chart period')
        Init = False
        return
    ArrayResize(iHigh_v, UpPeriod)
    ArrayResize(iLow_v, DnPeriod)
    ArraySetAsSeries(iHigh_v, True)
    ArraySetAsSeries(iLow_v, True)
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(1, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowerBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Price Chanel HTF(', GetStringTimeframe(TimeFrame), ',', UpPeriod, ',', DnPeriod, ',', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    limit = 0
    bar = 0
    iTime_ = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        LowerBuffer[bar] = EMPTY_VALUE
        UpperBuffer[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyLow(Symbol(), TimeFrame, _DT(time[bar]), DnPeriod, iLow_v) <= 0:
                return 0
            if CopyHigh(Symbol(), TimeFrame, _DT(time[bar]), UpPeriod, iHigh_v) <= 0:
                return 0
            LowerBuffer[bar] = iLow_v[ArrayMinimum(iLow_v, 0, DnPeriod)]
            UpperBuffer[bar] = iHigh_v[ArrayMaximum(iHigh_v, 0, UpPeriod)]
        if LowerBuffer[bar + 1] != EMPTY_VALUE and LowerBuffer[bar] == EMPTY_VALUE:
            LowerBuffer[bar] = LowerBuffer[bar + 1]
            UpperBuffer[bar] = UpperBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PricechanelHtf(_MQL5Indicator):
    name = 'pricechanel_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'UpPeriod': 12,  # Maximums searching period
        'DnPeriod': 12,  # Minimums searching period
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

