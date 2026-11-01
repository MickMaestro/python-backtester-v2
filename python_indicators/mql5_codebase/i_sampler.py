"""i_sampler — converted from MQL5: MQL5 Indicators/Sampler/i_sampler.mq5

Copyright: Copyright 2012, her.human; Link: her.human@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, her.human', 'link': 'her.human@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_minimum': -1.0, 'indicator_maximum': 1.0, 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 10}, 'colors': {1: [8388352], 2: [16760576, 5275647]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'analog', 2: 'discrete'}, 'levels': [], 'description': [], 'name': 'i_sampler', 'source': 'MQL5 Indicators/Sampler/i_sampler.mq5', 'folder': 'Sampler', 'inputs': [{'mql': 'bars_future', 'py': 'bars_future', 'param': 'bars_future', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'max_bars', 'py': 'max_bars', 'param': 'max_bars', 'type': 'int', 'default': 10000, 'label': '', 'sinput': False}, {'mql': 'discrete_metod', 'py': 'discrete_metod', 'param': 'discrete_metod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'porog', 'py': 'porog', 'param': 'porog', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'tp', 'py': 'tp', 'param': 'tp', 'type': 'int', 'default': 500, 'label': '', 'sinput': False}, {'mql': 'sl', 'py': 'sl', 'param': 'sl', 'type': 'int', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'show_arrow', 'py': 'show_arrow', 'param': 'show_arrow', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'save_file', 'py': 'save_file', 'param': 'save_file', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
bars_future = _input('bars_future', 10)
max_bars = _input('max_bars', 10000)
discrete_metod = _input('discrete_metod', 1)
porog = _input('porog', 0.5)
tp = _input('tp', 500)
sl = _input('sl', 200)
show_arrow = _input('show_arrow', True)
save_file = _input('save_file', False)
analogBuffer = Arr(0, 0.0)
discreteBuffer = Arr(0, 0.0)
discreteColors = Arr(0, 0.0)
point = 0.0
name = ""
timesignal = Arr(0, 0)

def OnInit():
    global name, point
    SetIndexBuffer(0, analogBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, discreteBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, discreteColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Bars(Symbol(), Period()) - max_bars)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Bars(Symbol(), Period()) - max_bars)
    point = SymbolInfoDouble(Symbol(), SYMBOL_POINT)
    name = MQL5InfoString(MQL5_PROGRAM_NAME)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    start = MathMax(rates_total - max_bars, prev_calculated)
    i = start
    for i in range(i, rates_total - bars_future):
        analogBuffer[i + bars_future] = EMPTY_VALUE
        discreteBuffer[i + bars_future] = EMPTY_VALUE
        price_high = high[ArrayMaximum(high, i, bars_future)]
        price_low = low[ArrayMinimum(low, i, bars_future)]
        deviation_plus = price_high - open[i]
        deviation_minus = open[i] - price_low
        value = _fdiv(2.0 * deviation_plus, deviation_plus + deviation_minus) - 1
        analogBuffer[i] = value
        _sw1 = discrete_metod
        if _sw1 == 1:
            if value > porog:
                discreteBuffer[i] = 1.0
                discreteColors[i] = 0.0
            elif value < (-porog):
                discreteBuffer[i] = -1.0
                discreteColors[i] = 1.0
            else:
                discreteBuffer[i] = 0.0
        elif _sw1 == 2:
            if deviation_plus > (tp * point) and deviation_minus < (sl * point):
                discreteBuffer[i] = 1.0
                discreteColors[i] = 0.0
            elif deviation_plus < (sl * point) and deviation_minus > (tp * point):
                discreteBuffer[i] = -1.0
                discreteColors[i] = 1.0
            else:
                discreteBuffer[i] = 0.0
        if show_arrow:
            SetArrow(discreteBuffer[i], time[i], open[i])
        if save_file and i == (rates_total - bars_future - 1):
            SaveBuffer(rates_total, time, discreteBuffer)
    else:
        i = _range_end(i, rates_total - bars_future, 1)
    return i

def OnDeinit(reason):
    NameObjectDelete(name)

def SetArrow(signal, timebar, price):
    if signal == 0:
        return
    name_arrow = Box("")
    if signal > 0:
        StringConcatenate(name_arrow, name, ' Buy ', ' ', timebar)
        ObjectCreate(0, name_arrow.v, OBJ_ARROW_BUY, 0, timebar, price)
    if signal < 0:
        StringConcatenate(name_arrow, name, ' Buy ', ' ', timebar)
        ObjectCreate(0, name_arrow.v, OBJ_ARROW_SELL, 0, timebar, price)

def NameObjectDelete(namedelet):
    totalobject = ObjectsTotal(0, 0, -1)
    for i in range(totalobject - 1, 0 - 1, -1):
        nameobj = ObjectName(0, i, 0, -1)
        if StringFind(nameobj, namedelet) >= 0:
            ObjectDelete(0, nameobj)

def SaveBuffer(rates_total, time, Buffer):
    n = 0
    ne = 0
    for i in range(0, rates_total):
        if Buffer[i] == 1 or Buffer[i] == -1:
            n += 1
    ArrayResize(timesignal, n)
    n = 0
    for i in range(0, rates_total):
        if Buffer[i] == 1 or Buffer[i] == -1:
            timesignal[n] = _int(time[i]) * _int(Buffer[i])
            n += 1
    ResetLastError()
    namefile = Box("")
    StringConcatenate(namefile, Symbol(), '_Sampler.BIN')
    filehandle = FileOpen(namefile.v, (FILE_WRITE | FILE_BIN) | FILE_COMMON)
    if filehandle != INVALID_HANDLE:
        ne = FileWriteArray(filehandle, timesignal, 0, WHOLE_ARRAY)
        FileClose(filehandle)
    else:
        Print(namefile.v, ' FileWrite failed, error ', GetLastError())


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ISampler(_MQL5Indicator):
    name = 'i_sampler'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'bars_future': 10,
        'max_bars': 10000,
        'discrete_metod': 1,
        'porog': 0.5,
        'tp': 500,
        'sl': 200,
        'show_arrow': True,
        'save_file': False,
    }
    y_range = (-1.0, 1.0)

