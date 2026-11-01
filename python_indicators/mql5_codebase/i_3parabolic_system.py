"""3parabolic_system — converted from MQL5: MQL5 Indicators/3Parabolic System/3parabolic_system.mq5

3Parabolic System
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [255], 2: [16711680], 3: [16711935], 4: [65280]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: 'Lower Parabolic', 2: 'Upper Parabolic', 3: '3Parabolic System Sell', 4: '3Parabolic System Buy'}, 'levels': [], 'description': ['3Parabolic System'], 'name': '3parabolic_system', 'source': 'MQL5 Indicators/3Parabolic System/3parabolic_system.mq5', 'folder': '3Parabolic System', 'inputs': [{'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Number of submitted alerts', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'Signal bar index, 0 is a current bar', 'sinput': False}, {'mql': 'Junior_Step', 'py': 'Junior_Step', 'param': 'Junior_Step', 'type': 'double', 'default': 0.02, 'label': 'Junior iSAR step', 'sinput': False}, {'mql': 'Junior_Maximum', 'py': 'Junior_Maximum', 'param': 'Junior_Maximum', 'type': 'double', 'default': 0.2, 'label': 'Junior iSAR maximum', 'sinput': False}, {'mql': 'Middle_TimeFrame', 'py': 'Middle_TimeFrame', 'param': 'Middle_TimeFrame', 'type': 'int', 'default': 16385, 'label': 'Middle iSAR chart period', 'sinput': False}, {'mql': 'Middle_Step', 'py': 'Middle_Step', 'param': 'Middle_Step', 'type': 'double', 'default': 0.02, 'label': 'Middle iSAR step', 'sinput': False}, {'mql': 'Middle_Maximum', 'py': 'Middle_Maximum', 'param': 'Middle_Maximum', 'type': 'double', 'default': 0.2, 'label': 'Middle iSAR maximum', 'sinput': False}, {'mql': 'Senior_TimeFrame', 'py': 'Senior_TimeFrame', 'param': 'Senior_TimeFrame', 'type': 'int', 'default': 16396, 'label': 'Senior iSAR chart period', 'sinput': False}, {'mql': 'Senior_Step', 'py': 'Senior_Step', 'param': 'Senior_Step', 'type': 'double', 'default': 0.02, 'label': 'Senior iSAR step', 'sinput': False}, {'mql': 'Senior_Maximum', 'py': 'Senior_Maximum', 'param': 'Senior_Maximum', 'type': 'double', 'default': 0.2, 'label': 'Senior iSAR maximum', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AlertCount = _input('AlertCount', 0)  # Number of submitted alerts
SignalBar = _input('SignalBar', 1)  # Signal bar index, 0 is a current bar
Junior_Step = _input('Junior_Step', 0.02)  # Junior iSAR step
Junior_Maximum = _input('Junior_Maximum', 0.2)  # Junior iSAR maximum
Middle_TimeFrame = _input('Middle_TimeFrame', PERIOD_H1)  # Middle iSAR chart period
Middle_Step = _input('Middle_Step', 0.02)  # Middle iSAR step
Middle_Maximum = _input('Middle_Maximum', 0.2)  # Middle iSAR maximum
Senior_TimeFrame = _input('Senior_TimeFrame', PERIOD_H12)  # Senior iSAR chart period
Senior_Step = _input('Senior_Step', 0.02)  # Senior iSAR step
Senior_Maximum = _input('Senior_Maximum', 0.2)  # Senior iSAR maximum
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
UpSarBuffer = Arr(0, 0.0)
DnSarBuffer = Arr(0, 0.0)
Init = False
JSAR_Handle = 0
MSAR_Handle = 0
SSAR_Handle = 0
min_rates_total = 0

def OnInit():
    global Init, JSAR_Handle, MSAR_Handle, SSAR_Handle, min_rates_total
    Init = True
    if Middle_TimeFrame < Period():
        Print('Middle iSAR chart period cannot be less than the current chart period')
        Init = False
        return
    if Senior_TimeFrame < Middle_TimeFrame:
        Print('Senior iSAR chart period cannot be less than the middle iSAR chart period')
        Init = False
        return
    min_rates_total = 3
    JSAR_Handle = iSAR(None, PERIOD_CURRENT, Junior_Step, Junior_Maximum)
    if JSAR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of iSAR Junior indicator')
    MSAR_Handle = iSAR(None, Middle_TimeFrame, Middle_Step, Middle_Maximum)
    if MSAR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of iSAR Middle indicator')
    SSAR_Handle = iSAR(None, Senior_TimeFrame, Senior_Step, Senior_Maximum)
    if SSAR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of iSAR Senior indicator')
    SetIndexBuffer(0, UpSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    ArraySetAsSeries(UpSarBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, DnSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    ArraySetAsSeries(DnSarBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = '3Parabolic System'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    Comment('3Parabolic System')

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DnCount, _s_OnCalculate_UpCount
    if BarsCalculated(JSAR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    JSAR = Arr(0, 0.0)
    MSAR = Arr(0, 0.0)
    SSAR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total + 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(JSAR_Handle, 0, 0, to_copy, JSAR) <= 0:
        return 0
    ArraySetAsSeries(JSAR, True)
    ArraySetAsSeries(MSAR, True)
    ArraySetAsSeries(SSAR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        DnSarBuffer[bar] = 0.0
        UpSarBuffer[bar] = 0.0
        if open[bar] < JSAR[bar]:
            UpSarBuffer[bar] = JSAR[bar]
        else:
            DnSarBuffer[bar] = JSAR[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if CopyBuffer(MSAR_Handle, 0, _DT(time[bar]), 1, MSAR) <= 0:
            return 0
        if CopyBuffer(SSAR_Handle, 0, _DT(time[bar]), 1, SSAR) <= 0:
            return 0
        if ((UpSarBuffer[bar + 1] > 0.0 and DnSarBuffer[bar] > 0.0) and close[bar] > MSAR[0]) and close[bar] > SSAR[0]:
            BuyBuffer[bar] = JSAR[bar]
        if ((DnSarBuffer[bar + 1] > 0.0 and UpSarBuffer[bar] > 0.0) and close[bar] < MSAR[0]) and close[bar] < SSAR[0]:
            SellBuffer[bar] = JSAR[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if rates_total != prev_calculated:
        _s_OnCalculate_UpCount = 0
        _s_OnCalculate_DnCount = 0
    if _s_OnCalculate_UpCount < AlertCount and BuyBuffer[SignalBar]:
        _s_OnCalculate_UpCount += 1
        Alert('3Parabolic System indicator: ' + Symbol() + EnumToString(PERIOD_CURRENT, 'ENUM_TIMEFRAMES') + ': Buy signal ' + Symbol())
    if _s_OnCalculate_DnCount < AlertCount and SellBuffer[SignalBar]:
        _s_OnCalculate_DnCount += 1
        Alert('3Parabolic System indicator: ' + Symbol() + EnumToString(PERIOD_CURRENT, 'ENUM_TIMEFRAMES') + ': Sell signal ' + Symbol())
    return rates_total

# ---- static local variables
_s_OnCalculate_UpCount = 0
_s_OnCalculate_DnCount = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind3parabolicSystem(_MQL5Indicator):
    name = '3parabolic_system'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AlertCount': 0,  # Number of submitted alerts
        'SignalBar': 1,  # Signal bar index, 0 is a current bar
        'Junior_Step': 0.02,  # Junior iSAR step
        'Junior_Maximum': 0.2,  # Junior iSAR maximum
        'Middle_TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Middle iSAR chart period
        'Middle_Step': 0.02,  # Middle iSAR step
        'Middle_Maximum': 0.2,  # Middle iSAR maximum
        'Senior_TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # Senior iSAR chart period
        'Senior_Step': 0.02,  # Senior iSAR step
        'Senior_Maximum': 0.2,  # Senior iSAR maximum
    }

