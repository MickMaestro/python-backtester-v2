"""Open_Oscillator_Cloud — converted from MQL5: MQL5 Indicators/Open_Oscillator_Cloud_HTF/Open_Oscillator_Cloud.mq5

Open oscillator
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [13688896, 55295], 2: [16711680], 3: [16711935]}, 'widths': {2: 2, 3: 2}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'Cloud', 2: 'Signal High', 3: 'Signal Low'}, 'levels': [0.0], 'description': ['Open oscillator'], 'name': 'Open_Oscillator_Cloud', 'source': 'MQL5 Indicators/Open_Oscillator_Cloud_HTF/Open_Oscillator_Cloud.mq5', 'folder': 'Open_Oscillator_Cloud_HTF', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'XMethod', 'py': 'XMethod', 'param': 'XMethod', 'type': 'int', 'default': 0, 'label': 'метод усреднения сглаживания', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 10, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг канала по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
XMethod = _input('XMethod', MODE_SMA_)  # метод усреднения сглаживания
XLength = _input('XLength', 10)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Shift = _input('Shift', 0)  # сдвиг канала по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
UpClIndBuffer = Arr(0, 0.0)
DnClIndBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = _int(InpPeriod)
    min_rates_total = min_rates_1 + GetStartBars(XMethod, XLength, XPhase)
    SetIndexBuffer(0, UpClIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnClIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DnIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpClIndBuffer, True)
    ArraySetAsSeries(DnClIndBuffer, True)
    ArraySetAsSeries(UpIndBuffer, True)
    ArraySetAsSeries(DnIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    short_name = 'Open_Oscillator_Cloud'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar = rates_total - min_rates_1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        bh = ArrayMaximum(high, bar, InpPeriod)
        bl = ArrayMinimum(low, bar, InpPeriod)
        UpClIndBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMethod, XPhase, XLength, open[bar] - open[bh], bar, True)
        UpIndBuffer[bar] = UpClIndBuffer[bar]
        DnClIndBuffer[bar] = XMA2.XMASeries(maxbar, prev_calculated, rates_total, XMethod, XPhase, XLength, open[bl] - open[bar], bar, True)
        DnIndBuffer[bar] = DnClIndBuffer[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OpenOscillatorCloud(_MQL5Indicator):
    name = 'Open_Oscillator_Cloud'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'XMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения сглаживания
        'XLength': 10,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'Shift': 0,  # сдвиг канала по горизонтали в барах
    }

