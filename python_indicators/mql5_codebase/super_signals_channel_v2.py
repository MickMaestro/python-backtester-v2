"""Super_Signals_Channel_V2 — converted from MQL5: MQL5 Indicators/Super_Signals_Channel_V2/Super_Signals_Channel_V2.mq5

Copyright: Copyright © 2006, Nick Bilak, beluck[AT]gmail.com; Link: http://www.forex-tsd.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Nick Bilak, beluck[AT]gmail.com', 'link': 'http://www.forex-tsd.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [16443110], 2: [8421376], 3: [16711935], 4: [65280], 5: [255]}, 'widths': {2: 2, 3: 2, 4: 1, 5: 1}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'Super_Signals_Channel Cloud', 2: 'Upper Super_Signals_Channel', 3: 'Lower Super_Signals_Channel', 4: 'Buy Super_Signals_Channel', 5: 'Sell Super_Signals_Channel'}, 'levels': [], 'description': [], 'name': 'Super_Signals_Channel_V2', 'source': 'MQL5 Indicators/Super_Signals_Channel_V2/Super_Signals_Channel_V2.mq5', 'folder': 'Super_Signals_Channel_V2', 'inputs': [{'mql': 'SignalGap', 'py': 'SignalGap', 'param': 'SignalGap', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'dist', 'py': 'dist', 'param': 'dist', 'type': 'uint', 'default': 24, 'label': 'величина заскока в будущее', 'sinput': False}, {'mql': 'repaint', 'py': 'repaint', 'param': 'repaint', 'type': 'bool', 'default': False, 'label': 'перерисовка', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SignalGap = _input('SignalGap', 4)
dist = _input('dist', 24)  # величина заскока в будущее
repaint = _input('repaint', False)  # перерисовка
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ExtMapBufferUp1 = Arr(0, 0.0)
ExtMapBufferDown1 = Arr(0, 0.0)
dSignalGap = 0.0
min_rates_total = 0
dist2 = 0

def OnInit():
    global dSignalGap, dist2, min_rates_total
    min_rates_total = _int(dist + 1)
    dSignalGap = SignalGap * Point()
    dist2 = _int(_idiv(dist, 2))
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, ExtMapBufferUp1, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp1, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    SetIndexBuffer(5, ExtMapBufferDown1, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown1, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_ARROW, 108)
    shortname = Box("")
    StringConcatenate(shortname, 'Super_Signals_Channel(', SignalGap, ', ', dist, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    hhb = 0
    llb = 0
    limit = 0
    bar = 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated + dist2
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtMapBufferUp1[bar] = EMPTY_VALUE
        ExtMapBufferDown1[bar] = EMPTY_VALUE
        barx = 0
        if repaint:
            barx = MathMax(bar - dist2, 0)
        else:
            barx = bar
        hhb = ArrayMaximum(high, barx, dist)
        llb = ArrayMinimum(low, barx, dist)
        if bar == hhb:
            ExtMapBufferDown1[bar] = high[hhb] + dSignalGap
        if bar == llb:
            ExtMapBufferUp1[bar] = low[llb] - dSignalGap
        UpBuffer[bar] = high[hhb]
        ExtMapBufferDown[bar] = UpBuffer[bar]
        DnBuffer[bar] = low[llb]
        ExtMapBufferUp[bar] = DnBuffer[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperSignalsChannelV2(_MQL5Indicator):
    name = 'Super_Signals_Channel_V2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SignalGap': 4,
        'dist': 24,  # величина заскока в будущее
        'repaint': False,  # перерисовка
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

