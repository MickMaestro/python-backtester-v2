"""jbraintrend1sig — converted from MQL5: MQL5 Indicators/JBrainTrendSig1/jbraintrend1sig.mq5

Copyright: Copyright © 2005, BrainTrading Inc.; Link: http://www.braintrading.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, BrainTrading Inc.', 'link': 'http://www.braintrading.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [36095], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'JBrain1 Sell', 2: 'JBrain1 Buy'}, 'levels': [], 'description': [], 'name': 'jbraintrend1sig', 'source': 'MQL5 Indicators/JBrainTrendSig1/jbraintrend1sig.mq5', 'folder': 'JBrainTrendSig1', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 7, 'label': 'ATR period', 'sinput': False}, {'mql': 'STO_Period', 'py': 'STO_Period', 'param': 'STO_Period', 'type': 'int', 'default': 9, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'STO_Price', 'py': 'STO_Price', 'param': 'STO_Price', 'type': 'int', 'default': 0, 'label': 'Prices calculation method', 'sinput': False}, {'mql': 'Length_', 'py': 'Length_', 'param': 'Length_', 'type': 'int', 'default': 7, 'label': 'JMA smoothing depth', 'sinput': False}, {'mql': 'Phase_', 'py': 'Phase_', 'param': 'Phase_', 'type': 'int', 'default': 100, 'label': 'JMA smoothing parameter', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 7)  # ATR period
STO_Period = _input('STO_Period', 9)  # Stochastic period
MA_Method = _input('MA_Method', MODE_SMA)  # Smoothing method
STO_Price = _input('STO_Price', STO_LOWHIGH)  # Prices calculation method
Length_ = _input('Length_', 7)  # JMA smoothing depth
Phase_ = _input('Phase_', 100)  # JMA smoothing parameter
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
d = 0.0
s = 0.0
p = 0
x1 = 0
x2 = 0
P_ = 0
min_rates_total = 0
OldTrend = 0
ATR_Handle = 0
STO_Handle = 0
JO_Handle = 0
JH_Handle = 0
JL_Handle = 0
JC_Handle = 0

def OnInit():
    global ATR_Handle, JC_Handle, JH_Handle, JL_Handle, STO_Handle, d, min_rates_total, s, x1, x2
    d = 2.3
    s = 1.5
    x1 = 53
    x2 = 47
    min_rates_total = MathMax(MathMax(ATR_Period, STO_Period), 30) + 2
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    STO_Handle = iStochastic(None, 0, STO_Period, STO_Period, 1, MA_Method, STO_Price)
    if STO_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Stochastic indicator')
    JL_Handle = iCustom(None, 0, 'JMA', Length_, Phase_, 4, 0, 0)
    if JL_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the indicator JMA')
        return 1
    JC_Handle = iCustom(None, 0, 'JMA', Length_, Phase_, 1, 0, 0)
    if JC_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the indicator JMA')
        return 1
    JH_Handle = iCustom(None, 0, 'JMA', Length_, Phase_, 3, 0, 0)
    if JH_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the indicator JMA')
        return 1
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'JBrainTrend1Sig'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global OldTrend, P_, p
    if ((((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(STO_Handle) < rates_total) or BarsCalculated(JH_Handle) < rates_total) or BarsCalculated(JL_Handle) < rates_total) or BarsCalculated(JC_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    value2 = Arr(0, 0.0)
    Range = Arr(0, 0.0)
    JH = Arr(0, 0.0)
    JL = Arr(0, 0.0)
    JC = Arr(0, 0.0)
    range_ = 0.0
    range2 = 0.0
    val1 = 0.0
    val2 = 0.0
    val3 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, Range) <= 0:
        return 0
    if CopyBuffer(STO_Handle, 0, 0, to_copy, value2) <= 0:
        return 0
    if CopyBuffer(JH_Handle, 0, 0, to_copy, JH) <= 0:
        return 0
    if CopyBuffer(JL_Handle, 0, 0, to_copy, JL) <= 0:
        return 0
    if CopyBuffer(JC_Handle, 0, 0, to_copy + 2, JC) <= 0:
        return 0
    ArraySetAsSeries(Range, True)
    ArraySetAsSeries(value2, True)
    ArraySetAsSeries(JH, True)
    ArraySetAsSeries(JL, True)
    ArraySetAsSeries(JC, True)
    p = P_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            P_ = p
        range_ = _fdiv(Range[bar], d)
        range2 = (Range[bar] * s) / 4
        val1 = 0.0
        val2 = 0.0
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        val3 = MathAbs(NormalizeDouble(JC[bar], Digits()) - NormalizeDouble(JC[bar + 2], Digits()))
        if value2[bar] < x2 and val3 > range_:
            p = 1
        if value2[bar] > x1 and val3 > range_:
            p = 2
        if val3 <= range_:
            continue
        if value2[bar] < x2 and (p == 1 or p == 0):
            if OldTrend > 0:
                SellBuffer[bar] = JH[bar] + range2
            if bar:
                OldTrend = -1
        if value2[bar] > x1 and (p == 2 or p == 0):
            if OldTrend < 0:
                BuyBuffer[bar] = JL[bar] - range2
            if bar:
                OldTrend = 1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jbraintrend1sig(_MQL5Indicator):
    name = 'jbraintrend1sig'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 7,  # ATR period
        'STO_Period': 9,  # Stochastic period
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
        'STO_Price': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Prices calculation method
        'Length_': 7,  # JMA smoothing depth
        'Phase_': 100,  # JMA smoothing parameter
    }

