"""linearregressionchannel — converted from MQL5: MQL5 Indicators/LinearRegressionChannel/linearregressionchannel.mq5

LinearRegression Channel
Copyright: Copyright © 2008, dimicr; Link: http://www.signalsbg.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, dimicr', 'link': 'http://www.signalsbg.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [14822282], 2: [65280], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 4, 2: 4, 3: 4}, 'labels': {1: 'LinearRegression Line', 2: 'LinearRegression Resistance', 3: 'LinearRegression Support'}, 'levels': [], 'description': ['LinearRegression Channel'], 'name': 'linearregressionchannel', 'source': 'MQL5 Indicators/LinearRegressionChannel/linearregressionchannel.mq5', 'folder': 'LinearRegressionChannel', 'inputs': [{'mql': 'UserPrice', 'py': 'UserPrice', 'param': 'UserPrice', 'type': 'int', 'default': 0, 'label': 'price mode', 'sinput': False}, {'mql': 'barsToCount', 'py': 'barsToCount', 'param': 'barsToCount', 'type': 'uint', 'default': 50, 'label': 'Number of bars for calculation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_USER_PRICE
MODE_CLOSE = 0
MODE_HIGH_LOW = 1
_enum('ENUM_USER_PRICE', {0: 'MODE_CLOSE', 1: 'MODE_HIGH_LOW'})

# ---- inputs and global variables
UserPrice = _input('UserPrice', MODE_CLOSE)  # price mode
barsToCount = _input('barsToCount', 50)  # Number of bars for calculation
LineBuffer = Arr(0, 0.0)
ResBuffer = Arr(0, 0.0)
SupBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(barsToCount)
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(LineBuffer, True)
    SetIndexBuffer(1, ResBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, SupBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(ResBuffer, True)
    ArraySetAsSeries(SupBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'LinearRegression(', EnumToString(UserPrice, 'ENUM_USER_PRICE'), ', ', barsToCount, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    DRAW_BEGIN = rates_total - min_rates_total - 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, DRAW_BEGIN)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, DRAW_BEGIN)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, DRAW_BEGIN)
    a = 0.0
    b = 0.0
    c = 0.0
    res = 0.0
    sumy = 0.0
    sumx = 0.0
    sumxy = 0.0
    sumx2 = 0.0
    h = 0.0
    l = 0.0
    bar = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit + min_rates_total
    for bar in range(bar, min_rates_total, -1):
        LineBuffer[bar] = 0.0
        SupBuffer[bar] = 0.0
        ResBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, min_rates_total, -1)
    bar = 0
    for bar in range(bar, min_rates_total):
        sumy += close[bar]
        sumxy += close[bar] * bar
        sumx += bar
        sumx2 += bar * bar
    else:
        bar = _range_end(bar, min_rates_total, 1)
    c = (sumx2 * barsToCount) - (sumx * sumx)
    if not c:
        Alert('Error in linear regression!')
        return 0
    b = _fdiv((sumxy * barsToCount) - (sumx * sumy), c)
    a = (sumy - (sumx * b)) / barsToCount
    bar = 0
    for bar in range(bar, min_rates_total):
        LineBuffer[bar] = a + (b * bar)
    else:
        bar = _range_end(bar, min_rates_total, 1)
    if UserPrice == MODE_CLOSE:
        bar = 0
        for bar in range(bar, min_rates_total):
            h = MathMax(h, close[bar] - LineBuffer[bar])
            l = MathMax(l, LineBuffer[bar] - close[bar])
        else:
            bar = _range_end(bar, min_rates_total, 1)
    else:
        bar = 0
        for bar in range(bar, min_rates_total):
            h = MathMax(h, high[bar] - LineBuffer[bar])
            l = MathMax(l, LineBuffer[bar] - low[bar])
        else:
            bar = _range_end(bar, min_rates_total, 1)
    if h > l:
        res = h
    else:
        res = l
    bar = 0
    for bar in range(bar, min_rates_total):
        SupBuffer[bar] = a - res + (b * bar)
        ResBuffer[bar] = a + res + (b * bar)
    else:
        bar = _range_end(bar, min_rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Linearregressionchannel(_MQL5Indicator):
    name = 'linearregressionchannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'UserPrice': _Choice({0: 'Используем close', 1: 'Используем high и low'}, default=0),  # price mode
        'barsToCount': 50,  # Number of bars for calculation
    }

