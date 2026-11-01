"""Super_Signals_Channel_V3 — converted from MQL5: MQL5 Indicators/Super_Signals_Channel_V3/Super_Signals_Channel_V3.mq5

Copyright: Copyright © 2006, Nick Bilak, beluck[AT]gmail.com; Link: http://www.forex-tsd.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Nick Bilak, beluck[AT]gmail.com', 'link': 'http://www.forex-tsd.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 7}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 5, 7: 5}, 'colors': {1: [15007673], 2: [16766975], 3: [8421376], 4: [16711680], 5: [16711935], 6: [65280], 7: [255]}, 'widths': {3: 3, 4: 2, 5: 3, 6: 1, 7: 1}, 'styles': {3: 0, 4: 0, 5: 0}, 'labels': {1: 'Upper Super_Signals_Channel Cloud', 2: 'Lower Super_Signals_Channel Cloud', 3: 'Upper Super_Signals_Channel', 4: 'Middle Super_Signals_Channel', 5: 'Lower Super_Signals_Channel', 6: 'Buy Super_Signals_Channel', 7: 'Sell Super_Signals_Channel'}, 'levels': [], 'description': [], 'name': 'Super_Signals_Channel_V3', 'source': 'MQL5 Indicators/Super_Signals_Channel_V3/Super_Signals_Channel_V3.mq5', 'folder': 'Super_Signals_Channel_V3', 'inputs': [{'mql': 'SignalGap', 'py': 'SignalGap', 'param': 'SignalGap', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'dist', 'py': 'dist', 'param': 'dist', 'type': 'uint', 'default': 24, 'label': 'величина заскока в будущее', 'sinput': False}, {'mql': 'repaint', 'py': 'repaint', 'param': 'repaint', 'type': 'bool', 'default': False, 'label': 'перерисовка', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SignalGap = _input('SignalGap', 4)
dist = _input('dist', 24)  # величина заскока в будущее
repaint = _input('repaint', False)  # перерисовка
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ExtMapBufferMiddle = Arr(0, 0.0)
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
    SetIndexBuffer(0, UpUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, UpDnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpUpBuffer, True)
    ArraySetAsSeries(UpDnBuffer, True)
    SetIndexBuffer(2, DnUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DnDnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(DnUpBuffer, True)
    ArraySetAsSeries(DnDnBuffer, True)
    SetIndexBuffer(4, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, ExtMapBufferMiddle, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferMiddle, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(6, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(7, ExtMapBufferUp1, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp1, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(5, PLOT_ARROW, 108)
    SetIndexBuffer(8, ExtMapBufferDown1, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown1, True)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(6, PLOT_ARROW, 108)
    shortname = Box("")
    StringConcatenate(shortname, 'Super_Signals_Channel_V3(', SignalGap, ', ', dist, ', ', Shift, ')')
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
            ExtMapBufferUp1[bar] = high[hhb] + dSignalGap
        if bar == llb:
            ExtMapBufferDown1[bar] = low[llb] - dSignalGap
        UpUpBuffer[bar] = high[hhb]
        ExtMapBufferUp[bar] = UpUpBuffer[bar]
        DnUpBuffer[bar] = (high[hhb] + low[llb]) / 2
        UpDnBuffer[bar] = DnUpBuffer[bar]
        ExtMapBufferMiddle[bar] = UpDnBuffer[bar]
        DnDnBuffer[bar] = low[llb]
        ExtMapBufferDown[bar] = DnDnBuffer[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperSignalsChannelV3(_MQL5Indicator):
    name = 'Super_Signals_Channel_V3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SignalGap': 4,
        'dist': 24,  # величина заскока в будущее
        'repaint': False,  # перерисовка
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

