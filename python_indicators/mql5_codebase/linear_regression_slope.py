"""linear_regression_slope — converted from MQL5: MQL5 Indicators/Linear Regression Slope/linear_regression_slope.mq5

Copyright: gpwr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'gpwr', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'LRS'}, 'levels': [], 'description': [], 'name': 'linear_regression_slope', 'source': 'MQL5 Indicators/Linear Regression Slope/linear_regression_slope.mq5', 'folder': 'Linear Regression Slope', 'inputs': [{'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 40, 'label': 'Linear regression period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 5, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Per = _input('Per', 40)  # Linear regression period
Price = _input('Price', PRICE_MEDIAN)  # Applied price
x = Arr(0, 0.0)
lrs = Arr(0, 0.0)

def OnInit():
    ArrayResize(x, Per + 1)
    SetIndexBuffer(0, lrs)
    IndicatorSetInteger(INDICATOR_DIGITS, 5)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LRS(' + _str(Per) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Per + 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    if rates_total < (Per + 1):
        Print('Error: not enough bars in history!')
        return 0
    i = prev_calculated - 1
    if i < Per:
        i = Per
    while i < rates_total:
        for j in range(1, Per + 1):
            if Price == PRICE_CLOSE:
                x[j] = Close[i - j]
            if Price == PRICE_OPEN:
                x[j] = Open[i - j]
            if Price == PRICE_HIGH:
                x[j] = High[i - j]
            if Price == PRICE_LOW:
                x[j] = Low[i - j]
            if Price == PRICE_MEDIAN:
                x[j] = (Low[i - j] + High[i - j]) / 2.0
            if Price == PRICE_TYPICAL:
                x[j] = (Low[i - j] + High[i - j] + Close[i - j]) / 3.0
            if Price == PRICE_WEIGHTED:
                x[j] = (Low[i - j] + High[i - j] + Close[i - j] + Open[i - j]) / 4.0
        lrs[i] = LinRegrSlope(Per)
        i += 1
    return rates_total

def LinRegrSlope(per):
    sum_ = 0.0
    wsum = 0.0
    for i in range(per, 0, -1):
        sum_ += x[i]
        wsum += x[i] * (per + 1 - i)
    lrs1 = 0.0
    lrs1 = _fdiv(6.0 * (_fdiv(_fdiv(2.0 * wsum, per + 1), sum_) - 1.0), per - 1)
    return lrs1 * 100000.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LinearRegressionSlope(_MQL5Indicator):
    name = 'linear_regression_slope'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Per': 40,  # Linear regression period
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Applied price
    }

