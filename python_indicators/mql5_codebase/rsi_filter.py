"""rsi_filter — converted from MQL5: MQL5 Indicators/RSI Filter/rsi_filter.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': -1.1, 'indicator_maximum': 1.1}, 'types': {1: 10}, 'colors': {1: [16760576, 9662683, 6908265]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'rsi filter'}, 'levels': [], 'description': [], 'name': 'rsi_filter', 'source': 'MQL5 Indicators/RSI Filter/rsi_filter.mq5', 'folder': 'RSI Filter', 'inputs': [{'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 14, 'label': 'Rsi period :', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RsiPeriod = _input('RsiPeriod', 14)  # Rsi period :
FltBuffer = Arr(0, 0.0)
ClrBuffer = Arr(0, 0.0)
RsiBuffer = Arr(0, 0.0)
ChgBuffer = Arr(0, 0.0)
TotBuffer = Arr(0, 0.0)
TrnBuffer = Arr(0, 0.0)
PrcBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, FltBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    SetIndexBuffer(1, ClrBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rsi filter (' + _str(RsiPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    if ArraySize(RsiBuffer) != rates_total:
        ArrayResize(RsiBuffer, rates_total)
        ArrayResize(ChgBuffer, rates_total)
        ArrayResize(TotBuffer, rates_total)
        ArrayResize(TrnBuffer, rates_total)
        ArrayResize(PrcBuffer, rates_total)
    alpha = 1.0 / float(RsiPeriod)
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        PrcBuffer[i] = price[i]
        if price[i] == EMPTY_VALUE:
            PrcBuffer[i] = 0.0
        if i < RsiPeriod:
            k = 0
            sum_ = 0.0
            k = 0
            while k < RsiPeriod and (i - k - 1) >= 0:
                sum_ += MathAbs(PrcBuffer[i - k] - PrcBuffer[i - k - 1])
                k += 1
            if k > 0:
                ChgBuffer[i] = _fdiv(PrcBuffer[i] - PrcBuffer[0], k)
                TotBuffer[i] = _fdiv(sum_, k)
        else:
            change = PrcBuffer[i] - PrcBuffer[i - 1]
            ChgBuffer[i] = ChgBuffer[i - 1] + (alpha * (change - ChgBuffer[i - 1]))
            TotBuffer[i] = TotBuffer[i - 1] + (alpha * (MathAbs(change) - TotBuffer[i - 1]))
        if TotBuffer[i] != 0:
            RsiBuffer[i] = 50.0 * (_fdiv(ChgBuffer[i], TotBuffer[i]) + 1)
        else:
            RsiBuffer[i] = 0.0
        FltBuffer[i] = EMPTY_VALUE
        TrnBuffer[i] = TrnBuffer[i - 1]
        if RsiBuffer[i] > 70:
            TrnBuffer[i] = 1.0
        if RsiBuffer[i] < 30:
            TrnBuffer[i] = -1.0
        if TrnBuffer[i] == 1 and RsiBuffer[i] > 40:
            FltBuffer[i] = 1.0
            ClrBuffer[i] = 0.0
        if TrnBuffer[i] == -1 and RsiBuffer[i] < 60:
            FltBuffer[i] = -1.0
            ClrBuffer[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiFilter(_MQL5Indicator):
    name = 'rsi_filter'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RsiPeriod': 14,  # Rsi period :
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (-1.1, 1.1)

