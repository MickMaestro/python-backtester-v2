"""dc_signals — converted from MQL5: MQL5 Indicators/The _DC signals_ signals generator/dc_signals.mq5

Генератор сигналов DC signals
Copyright: Copyright © 2008-2016, DC2008; Link: http://www.mql5.com/ru/users/dc2008; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008-2016, DC2008', 'link': 'http://www.mql5.com/ru/users/dc2008', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [65535], 2: [16776960], 3: [255], 4: [4678655], 5: [255], 6: [16711680]}, 'widths': {1: 3, 2: 3, 3: 1, 4: 0, 5: 3, 6: 3}, 'styles': {}, 'labels': {1: 'Upper Bound', 2: 'Lower Bound', 3: 'Center line', 4: 'Settlement price', 5: 'Reference line', 6: 'Upper breakborder'}, 'levels': [], 'description': ['Генератор сигналов DC signals'], 'name': 'dc_signals', 'source': 'MQL5 Indicators/The _DC signals_ signals generator/dc_signals.mq5', 'folder': 'The _DC signals_ signals generator', 'inputs': [{'mql': 'history', 'py': 'history', 'param': 'history', 'type': 'int', 'default': 500, 'label': 'Количество баров для анализа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
history = _input('history', 500)  # Количество баров для анализа
DCOS = Arr(0, 0.0)
BULLSBEARS = Arr(0, 0.0)
BufferUPDown = Arr(0, 0.0)
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
Buffer3 = Arr(0, 0.0)
h_Bulls = 0
h_Bears = 0
Bulls = Arr(0, 0.0)
Bears = Arr(0, 0.0)

def OnInit():
    global h_Bears, h_Bulls
    ObjectsDeleteAll(0, -1, -1)
    ArraySetAsSeries(DCOS, True)
    ArraySetAsSeries(BULLSBEARS, True)
    ArraySetAsSeries(BufferUPDown, True)
    ArraySetAsSeries(Buffer1, True)
    ArraySetAsSeries(Buffer2, True)
    ArraySetAsSeries(Buffer3, True)
    SetIndexBuffer(0, DCOS, INDICATOR_DATA)
    SetIndexBuffer(1, BULLSBEARS, INDICATOR_DATA)
    SetIndexBuffer(2, BufferUPDown, INDICATOR_DATA)
    SetIndexBuffer(3, Buffer1, INDICATOR_DATA)
    SetIndexBuffer(4, Buffer2, INDICATOR_DATA)
    SetIndexBuffer(5, Buffer3, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetInteger(3, PLOT_ARROW, 250)
    PlotIndexSetInteger(4, PLOT_ARROW, 178)
    PlotIndexSetInteger(5, PLOT_ARROW, 178)
    h_Bulls = iBullsPower(None, 0, 21)
    h_Bears = iBearsPower(None, 0, 21)
    ArraySetAsSeries(Bulls, True)
    ArraySetAsSeries(Bears, True)
    ChartRedraw()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    rt = rates_total - history
    for i in range(0, 6):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, rt)
    for i in range(history, 0 - 1, -1):
        CopyBuffer(h_Bulls, 0, i, 1, Bulls)
        CopyBuffer(h_Bears, 0, i, 1, Bears)
        BULLSBEARS[i] = Bulls[0] + Bears[0]
        if close[i] > open[i]:
            DCOS[i] = DCOS[i + 1] + tick_volume[i]
        if close[i] == open[i]:
            DCOS[i] = DCOS[i + 1]
        if close[i] < open[i]:
            DCOS[i] = DCOS[i + 1] - tick_volume[i]
        if close[i] > ((high[i] + low[i]) / 2):
            DCOS[i] += float(tick_volume[i])
        if close[i] < ((high[i] + low[i]) / 2):
            DCOS[i] -= float(tick_volume[i])
        if close[i] > ((high[i] + low[i] + open[i]) / 3):
            DCOS[i] += float(tick_volume[i])
        if close[i] < ((high[i] + low[i] + open[i]) / 3):
            DCOS[i] -= float(tick_volume[i])
        if close[i] > ((((high[i] + low[i]) / 2) + open[i]) / 2):
            DCOS[i] += float(tick_volume[i])
        if close[i] < ((((high[i] + low[i]) / 2) + open[i]) / 2):
            DCOS[i] -= float(tick_volume[i])
    for i in range(history, 1 - 1, -1):
        if DCOS[i] < DCOS[i + 1] and BULLSBEARS[i] > BULLSBEARS[i + 1]:
            BufferUPDown[i] = high[i]
        if DCOS[i] > DCOS[i + 1] and BULLSBEARS[i] < BULLSBEARS[i + 1]:
            BufferUPDown[i] = low[i]
        if DCOS[i] < DCOS[i + 1] and DCOS[i + 2] < DCOS[i + 1]:
            Buffer1[i] = high[i]
        if DCOS[i] > DCOS[i + 1] and DCOS[i + 2] > DCOS[i + 1]:
            Buffer1[i] = low[i]
        if ((DCOS[i] < DCOS[i + 1] and BULLSBEARS[i] > BULLSBEARS[i + 1]) and DCOS[i] > DCOS[i - 1]) and BULLSBEARS[i] > BULLSBEARS[i - 1]:
            Buffer2[i] = low[i]
        if ((DCOS[i] > DCOS[i + 1] and BULLSBEARS[i] < BULLSBEARS[i + 1]) and DCOS[i] < DCOS[i - 1]) and BULLSBEARS[i] < BULLSBEARS[i - 1]:
            Buffer3[i] = high[i]
    for i in range(history, 0 - 1, -1):
        DCOS[i] = 0.0
        BULLSBEARS[i] = 0.0
    for i in range(history, 1 - 1, -1):
        DCOS[i] = Buffer2[i]
        BULLSBEARS[i] = Buffer3[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DcSignals(_MQL5Indicator):
    name = 'dc_signals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'history': 500,  # Количество баров для анализа
    }

