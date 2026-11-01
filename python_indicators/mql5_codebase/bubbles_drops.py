"""bubbles_drops — converted from MQL5: MQL5 Indicators/BubblesAndDrops/bubbles_drops.mq5

Bubbles&Drops
Copyright: Maxaxa Angry Hunter; Link: mg@dsr.ru

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Maxaxa Angry Hunter', 'link': 'mg@dsr.ru', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bubbles', 2: 'Drops'}, 'levels': [], 'description': ['Bubbles&Drops'], 'name': 'bubbles_drops', 'source': 'MQL5 Indicators/BubblesAndDrops/bubbles_drops.mq5', 'folder': 'BubblesAndDrops', 'inputs': [{'mql': 'historyDeep', 'py': 'historyDeep', 'param': 'historyDeep', 'type': 'uint', 'default': 100, 'label': 'Number of bars in history', 'sinput': False}, {'mql': 'future', 'py': 'future', 'param': 'future', 'type': 'uint', 'default': 10, 'label': 'How many bars are shown after the chart', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
historyDeep = _input('historyDeep', 100)  # Number of bars in history
future = _input('future', 10)  # How many bars are shown after the chart
Buffer = Arr(0, 0.0)
FutBuffer = Arr(0, 0.0)
min_rates_total = 0
temp = Arr(0, 0.0)
divider = 10000.0

def OnInit():
    global divider, min_rates_total
    min_rates_total = _int(historyDeep + future + 1)
    divider = MathPow(10, Digits())
    ArrayResize(temp, min_rates_total)
    SetIndexBuffer(0, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(Buffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, 0)
    SetIndexBuffer(1, FutBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(FutBuffer, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, future)
    shortname = Box("")
    StringConcatenate(shortname, 'Bubbles&Drops(', historyDeep, ', ', future, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def splash(length, Open, Close):
    ArrayInitialize(temp, 0.0)
    ampl = MathRound((Open[length] - Close[length]) * divider)
    if not ampl:
        for i in range(0, length + _int(future) + 1):
            temp[i] = _fdiv(attenuation(ampl, i + 1), divider)

def attenuation(a, x):
    if not a:
        if a < 0:
            return MathAbs(a) - (_fdiv(100, x) * MathSin((x / 100) * MathAbs(a)))
        if a > 0:
            return -(MathAbs(a) - (_fdiv(100, x) * MathSin((x / 100) * MathAbs(a))))
    return 0.0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    for bar in range(limit, _int(historyDeep) - 1, -1):
        Buffer[bar] = 0.0
        FutBuffer[bar] = 0.0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    for j in range(0, _int(historyDeep)):
        Buffer[j] = open[j]
        FutBuffer[j] = open[j]
    for j in range(0, _int(historyDeep)):
        splash(historyDeep - j, open, close)
        for i in range(0, _int(historyDeep) - j + 1):
            Buffer[historyDeep - j - i] += temp[i]
        for i in range(0, _int(future) + 1):
            FutBuffer[future - i] += temp[historyDeep - j + i]
        for i in range(_int(future), _int(historyDeep + future)):
            FutBuffer[i] = Buffer[i - future]
    FutBuffer[0] = FutBuffer[1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BubblesDrops(_MQL5Indicator):
    name = 'bubbles_drops'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'historyDeep': 100,  # Number of bars in history
        'future': 10,  # How many bars are shown after the chart
    }

