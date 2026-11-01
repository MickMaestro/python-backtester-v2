"""r-squared_v1 — converted from MQL5: MQL5 Indicators/R-Squared_v1/r-squared_v1.mq5

Copyright: Copyright © 2006, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [8721863], 2: [15624315]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'R-Squared_v1', 2: 'Signal'}, 'levels': [50.0], 'description': [], 'name': 'r-squared_v1', 'source': 'MQL5 Indicators/R-Squared_v1/r-squared_v1.mq5', 'folder': 'R-Squared_v1', 'inputs': [{'mql': 'nLength', 'py': 'nLength', 'param': 'nLength', 'type': 'uint', 'default': 12, 'label': 'indicator period', 'sinput': False}, {'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'uint', 'default': 5, 'label': 'moving average period', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'moving average smoothing method', 'sinput': False}, {'mql': 'MA_Price', 'py': 'MA_Price', 'param': 'MA_Price', 'type': 'int', 'default': 7, 'label': 'price constant', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'uint', 'default': 14, 'label': 'moving period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
nLength = _input('nLength', 12)  # indicator period
MA_Period = _input('MA_Period', 5)  # moving average period
MA_Method = _input('MA_Method', MODE_SMA)  # moving average smoothing method
MA_Price = _input('MA_Price', PRICE_WEIGHTED)  # price constant
Smooth = _input('Smooth', 14)  # moving period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
MA_Handle = 0
min_rates_ = 0
min_rates_total = 0
Length = 0
SumX = 0.0
SumX2 = 0.0

def OnInit():
    global Length, MA_Handle, SumX, SumX2, min_rates_, min_rates_total
    min_rates_ = _int(MathMax(MathMax(MA_Period, nLength), Smooth))
    Length = _int(nLength)
    min_rates_total = _int(min_rates_ + Length + Smooth)
    SumX = 0.0
    for i in range(0, Length):
        SumX += i + 1
    SumX2 = 0.0
    for i in range(0, Length):
        SumX2 += MathPow(i + 1, 2)
    MA_Handle = iMA(None, 0, MA_Period, 0, MA_Method, MA_Price)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        return 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SignalBuffer, True)
    shortname = 'R-Squared_v1'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(MA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    SumY = 0.0
    SumY2 = 0.0
    SumXY = 0.0
    Q1 = 0.0
    Q2 = 0.0
    Q3 = 0.0
    res = 0.0
    SumR = 0.0
    MA = Arr(0, 0.0)
    ArraySetAsSeries(MA, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_
    else:
        limit = rates_total - prev_calculated
    to_copy = MathMin(limit + Length, rates_total)
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SumY = 0.0
        for i in range(0, Length):
            SumY += MA[bar + i]
        SumY2 = 0.0
        for i in range(0, Length):
            SumY2 += MathPow(MA[bar + i], 2)
        SumXY = 0.0
        for i in range(0, Length):
            SumXY += (i + 1) * MA[bar + i]
        Q1 = SumXY - _fdiv(SumX * SumY, Length)
        Q2 = SumX2 - _fdiv(SumX * SumX, Length)
        Q3 = SumY2 - _fdiv(SumY * SumY, Length)
        res = Q2 * Q3
        if res:
            IndBuffer[bar] = _fdiv(100 * Q1 * Q1, res)
        else:
            IndBuffer[bar] = 0.0
        SumR = 0.0
        for i in range(0, _int(Smooth)):
            SumR += IndBuffer[bar + i]
        SignalBuffer[bar] = SumR / Smooth
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSquaredV1(_MQL5Indicator):
    name = 'r-squared_v1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'nLength': 12,  # indicator period
        'MA_Period': 5,  # moving average period
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # moving average smoothing method
        'MA_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),  # price constant
        'Smooth': 14,  # moving period
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

