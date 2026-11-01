"""parabolic_htf_ — converted from MQL5: MQL5 Indicators/Parabolic_HTF/parabolic_htf_.mq5

3Parabolic System
Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [255], 2: [16711680], 3: [16711935], 4: [65280]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: 'Lower Parabolic', 2: 'Upper Parabolic', 3: 'Parabolic Sell', 4: 'Parabolic Buy'}, 'levels': [], 'description': ['3Parabolic System'], 'name': 'parabolic_htf_', 'source': 'MQL5 Indicators/Parabolic_HTF/parabolic_htf_.mq5', 'folder': 'Parabolic_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16390, 'label': 'iSAR indicator chart period', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'double', 'default': 0.02, 'label': 'iSAR step', 'sinput': False}, {'mql': 'Maximum', 'py': 'Maximum', 'param': 'Maximum', 'type': 'double', 'default': 0.2, 'label': 'iSAR maximum', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H6)  # iSAR indicator chart period
Step = _input('Step', 0.02)  # iSAR step
Maximum = _input('Maximum', 0.2)  # iSAR maximum
UpSarBuffer = Arr(0, 0.0)
DnSarBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
Init = False
Symbol_ = ""
SAR_Handle = 0
min_rates_total = 0

def OnInit():
    global Init, SAR_Handle, Symbol_, min_rates_total
    Init = True
    if TimeFrame < Period():
        Print('iSAR chart period cannot be less than the current chart period')
        Init = False
        return
    min_rates_total = 3
    Symbol_ = Symbol()
    SAR_Handle = iCustom(Symbol_, TimeFrame, 'ExamplesParabolicSAR', Step, Maximum)
    if SAR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iSAR indicator')
        Init = False
        return
    SetIndexBuffer(0, UpSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpSarBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, DnSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnSarBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Parabolic HTF'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if (BarsCalculated(SAR_Handle) < min_rates_total or rates_total < min_rates_total) or (not Init):
        return 0
    if BarsCalculated(SAR_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    iSar = Arr(1, 0.0, dyn=False)
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
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpSarBuffer[bar] = EMPTY_VALUE
        DnSarBuffer[bar] = EMPTY_VALUE
        BuyBuffer[bar] = EMPTY_VALUE
        SellBuffer[bar] = EMPTY_VALUE
        iSar[0] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            if CopyBuffer(SAR_Handle, 0, _DT(time[bar]), 1, iSar) <= 0:
                return 0
            if CopyClose(Symbol_, TimeFrame, _DT(time[bar]), 1, iClose_) <= 0:
                return 0
            if iClose_[0] < iSar[0]:
                SellBuffer[bar] = iSar[0]
                UpSarBuffer[bar] = iSar[0]
            else:
                BuyBuffer[bar] = iSar[0]
                DnSarBuffer[bar] = iSar[0]
            _s_OnCalculate_LastCountBar = bar
        if not iSar[0]:
            UpSarBuffer[bar] = UpSarBuffer[bar + 1]
            DnSarBuffer[bar] = DnSarBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ParabolicHtf(_MQL5Indicator):
    name = 'parabolic_htf_'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # iSAR indicator chart period
        'Step': 0.02,  # iSAR step
        'Maximum': 0.2,  # iSAR maximum
    }

