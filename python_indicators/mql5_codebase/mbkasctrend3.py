"""mbkasctrend3 — converted from MQL5: MQL5 Indicators/MBKAsctrend3/mbkasctrend3.mq5

MBKAsctrend3
Copyright: Copyright © 2007, Matt Kennel; Link: http://www.metatrader.org/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Matt Kennel', 'link': 'http://www.metatrader.org/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16748574]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'MBKAsctrend3 Sell', 2: 'MBKAsctrend3 Buy'}, 'levels': [], 'description': ['MBKAsctrend3'], 'name': 'mbkasctrend3', 'source': 'MQL5 Indicators/MBKAsctrend3/mbkasctrend3.mq5', 'folder': 'MBKAsctrend3', 'inputs': [{'mql': 'WPRLength1', 'py': 'WPRLength1', 'param': 'WPRLength1', 'type': 'uint', 'default': 9, 'label': 'WPR1 period', 'sinput': False}, {'mql': 'WPRLength2', 'py': 'WPRLength2', 'param': 'WPRLength2', 'type': 'uint', 'default': 33, 'label': 'WPR2 period', 'sinput': False}, {'mql': 'WPRLength3', 'py': 'WPRLength3', 'param': 'WPRLength3', 'type': 'uint', 'default': 77, 'label': 'WPR3 period', 'sinput': False}, {'mql': 'Swing', 'py': 'Swing', 'param': 'Swing', 'type': 'int', 'default': 3, 'label': 'Swing', 'sinput': False}, {'mql': 'AverSwing', 'py': 'AverSwing', 'param': 'AverSwing', 'type': 'int', 'default': -5, 'label': 'Average swing', 'sinput': False}, {'mql': 'W1', 'py': 'W1', 'param': 'W1', 'type': 'double', 'default': 1.0, 'label': 'WPR1 indicator weight', 'sinput': False}, {'mql': 'W2', 'py': 'W2', 'param': 'W2', 'type': 'double', 'default': 3.0, 'label': 'WPR2 indicator weight', 'sinput': False}, {'mql': 'W3', 'py': 'W3', 'param': 'W3', 'type': 'double', 'default': 1.0, 'label': 'WPR3 indicator weight', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
WPRLength1 = _input('WPRLength1', 9)  # WPR1 period
WPRLength2 = _input('WPRLength2', 33)  # WPR2 period
WPRLength3 = _input('WPRLength3', 77)  # WPR3 period
Swing = _input('Swing', 3)  # Swing
AverSwing = _input('AverSwing', -5)  # Average swing
W1 = _input('W1', 1.0)  # WPR1 indicator weight
W2 = _input('W2', 3.0)  # WPR2 indicator weight
W3 = _input('W3', 1.0)  # WPR3 indicator weight
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
w1 = 0.0
w2 = 0.0
w3 = 0.0
WPR1_Handle = 0
WPR2_Handle = 0
WPR3_Handle = 0
min_rates_total = 0
SSP = 0
UpLevel = 0
DnLevel = 0
Up1Level = 0
Dn1Level = 0

def OnInit():
    global Dn1Level, DnLevel, SSP, Up1Level, UpLevel, WPR1_Handle, WPR2_Handle, WPR3_Handle, min_rates_total, w1, w2, w3
    sumweights = W1 + W2 + W3
    w1 = _fdiv(W1, sumweights)
    w2 = _fdiv(W2, sumweights)
    w3 = _fdiv(W3, sumweights)
    SSP = 10
    UpLevel = 67 + Swing
    DnLevel = 33 - Swing
    Up1Level = 50 - AverSwing
    Dn1Level = 50 + AverSwing
    min_rates_total = _int(MathMax(MathMax(MathMax(WPRLength1, WPRLength2), WPRLength3), SSP))
    WPR1_Handle = iWPR(None, 0, WPRLength1)
    if WPR1_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iWPR 1 indicator')
    WPR2_Handle = iWPR(None, 0, WPRLength2)
    if WPR2_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iWPR 2 indicator')
    WPR3_Handle = iWPR(None, 0, WPRLength3)
    if WPR3_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iWPR 3 indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'MBKAsctrend3 Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'MBKAsctrend3 Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'MBKAsctrend3'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_oldtrend
    if ((BarsCalculated(WPR1_Handle) < rates_total or BarsCalculated(WPR2_Handle) < rates_total) or BarsCalculated(WPR3_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    trend = 0
    WPR1 = Arr(0, 0.0)
    WPR2 = Arr(0, 0.0)
    WPR3 = Arr(0, 0.0)
    wprvalue = 0.0
    wprlong = 0.0
    Range = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_oldtrend = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(WPR1, True)
    ArraySetAsSeries(WPR2, True)
    ArraySetAsSeries(WPR3, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if CopyBuffer(WPR1_Handle, 0, 0, to_copy, WPR1) <= 0:
        return 0
    if CopyBuffer(WPR2_Handle, 0, 0, to_copy, WPR2) <= 0:
        return 0
    if CopyBuffer(WPR3_Handle, 0, 0, to_copy, WPR3) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        WPR1[bar] = 100 + WPR1[bar]
        WPR2[bar] = 100 + WPR2[bar]
        WPR3[bar] = 100 + WPR3[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        trend = 0
        wprvalue = (w1 * WPR1[bar]) + (w2 * WPR2[bar]) + (w3 * WPR3[bar])
        wprlong = WPR3[bar]
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if wprvalue < DnLevel and wprlong <= Dn1Level:
            trend = -1
        if wprvalue > UpLevel and wprlong >= Up1Level:
            trend = 1
        if (_s_OnCalculate_oldtrend and trend != _s_OnCalculate_oldtrend) and trend > 0:
            Range = 0.0
            for iii in range(bar, bar + SSP + 1):
                Range += MathAbs(high[iii] - low[iii])
            Range = _fdiv(Range, SSP + 1)
            BuyBuffer[bar] = low[bar] - (Range * 0.8)
        if (_s_OnCalculate_oldtrend and trend != _s_OnCalculate_oldtrend) and trend < 0:
            Range = 0.0
            for iii in range(bar, bar + SSP + 1):
                Range += MathAbs(high[iii] - low[iii])
            Range = _fdiv(Range, SSP + 1)
            SellBuffer[bar] = high[bar] + (Range * 0.8)
        if bar and trend:
            _s_OnCalculate_oldtrend = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_oldtrend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Mbkasctrend3(_MQL5Indicator):
    name = 'mbkasctrend3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WPRLength1': 9,  # WPR1 period
        'WPRLength2': 33,  # WPR2 period
        'WPRLength3': 77,  # WPR3 period
        'Swing': 3,  # Swing
        'AverSwing': -5,  # Average swing
        'W1': 1.0,  # WPR1 indicator weight
        'W2': 3.0,  # WPR2 indicator weight
        'W3': 1.0,  # WPR3 indicator weight
    }

