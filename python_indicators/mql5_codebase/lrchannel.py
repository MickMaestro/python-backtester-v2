"""lrchannel — converted from MQL5: MQL5 Indicators/Linear Regression Channel/lrchannel.mq5

Linear Regression Channel
Copyright: Vladimir M.; Link: mikh.vl@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Vladimir M.', 'link': 'mikh.vl@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16711680], 2: [65535], 3: [65535], 4: [255], 5: [255]}, 'widths': {}, 'styles': {1: 0, 2: 2, 3: 2, 4: 2, 5: 2}, 'labels': {}, 'levels': [], 'description': ['Linear Regression Channel'], 'name': 'lrchannel', 'source': 'MQL5 Indicators/Linear Regression Channel/lrchannel.mq5', 'folder': 'Linear Regression Channel', 'inputs': [{'mql': 'InChPeriod', 'py': 'InChPeriod', 'param': 'InChPeriod', 'type': 'int', 'default': 150, 'label': 'Channel Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InChPeriod = _input('InChPeriod', 150)  # Channel Period
ExChPeriod = 0
rCount = 0
rlBuffer = Arr(0, 0.0)
upBuffer = Arr(0, 0.0)
downBuffer = Arr(0, 0.0)
highBuffer = Arr(0, 0.0)
lowBuffer = Arr(0, 0.0)

def OnInit():
    global ExChPeriod
    BarsTotal = 0
    BarsTotal = Bars(Symbol(), PERIOD_CURRENT)
    if InChPeriod < 2:
        ExChPeriod = 2
        printf('Incorrect input value InChPeriod=%d. Indicator will use InChPeriod=%d.', InChPeriod, ExChPeriod)
    elif InChPeriod >= BarsTotal:
        ExChPeriod = BarsTotal - 1
        printf('Total Bars=%d. Incorrect input value InChPeriod=%d. Indicator will use InChPeriod=%d.', BarsTotal, InChPeriod, ExChPeriod)
    else:
        ExChPeriod = InChPeriod
    SetIndexBuffer(0, rlBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, upBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, downBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, highBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, lowBuffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Main Line(' + _str(ExChPeriod) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Up Line(' + _str(ExChPeriod) + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'Down Line(' + _str(ExChPeriod) + ')')
    PlotIndexSetString(3, PLOT_LABEL, 'High Line(' + _str(ExChPeriod) + ')')
    PlotIndexSetString(4, PLOT_LABEL, 'Low Line(' + _str(ExChPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, begin, price):
    global rCount
    sumX = 0.0
    sumY = 0.0
    sumXY = 0.0
    sumX2 = 0.0
    a = 0.0
    b = 0.0
    F = 0.0
    S = 0.0
    X = 0
    if rates_total < (ExChPeriod + 1):
        return 0
    if rCount != rates_total:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - ExChPeriod - 1)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - ExChPeriod - 1)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, rates_total - ExChPeriod - 1)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, rates_total - ExChPeriod - 1)
        PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, rates_total - ExChPeriod - 1)
        F = 0.0
        S = 0.0
        sumX = 0.0
        sumY = 0.0
        sumXY = 0.0
        sumX2 = 0.0
        X = 0
        for i in range(rates_total - 1 - ExChPeriod, rates_total - 1):
            sumX += X
            sumY += price[i]
            sumXY += X * price[i]
            sumX2 += MathPow(X, 2)
            X += 1
        a = _fdiv((sumX * sumY) - (ExChPeriod * sumXY), MathPow(sumX, 2) - (ExChPeriod * sumX2))
        b = _fdiv(sumY - (a * sumX), ExChPeriod)
        X = 0
        for i in range(rates_total - 1 - ExChPeriod, rates_total):
            rlBuffer[i] = b + (a * X)
            F += MathPow(price[i] - rlBuffer[i], 2)
            X += 1
        S = NormalizeDouble(_fdiv(MathSqrt(_fdiv(F, ExChPeriod + 1)), MathCos((MathArctan((a * M_PI) / 180) * M_PI) / 180)), Digits())
        for i in range(rates_total - 1 - ExChPeriod, rates_total):
            upBuffer[i] = rlBuffer[i] + S
            downBuffer[i] = rlBuffer[i] - S
            highBuffer[i] = rlBuffer[i] + (2 * S)
            lowBuffer[i] = rlBuffer[i] - (2 * S)
        rCount = rates_total
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Lrchannel(_MQL5Indicator):
    name = 'lrchannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InChPeriod': 150,  # Channel Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

