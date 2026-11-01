"""xdidi_index — converted from MQL5: MQL5 Indicators/XDidi_Index_HTF/xdidi_index.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [16711935]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Curta', 2: 'Longa'}, 'levels': [1.0], 'description': [], 'name': 'xdidi_index', 'source': 'MQL5 Indicators/XDidi_Index_HTF/xdidi_index.mq5', 'folder': 'XDidi_Index_HTF', 'inputs': [{'mql': 'Curta_Method', 'py': 'Curta_Method', 'param': 'Curta_Method', 'type': 'int', 'default': 0, 'label': 'Curta метод усреднения', 'sinput': False}, {'mql': 'Curta', 'py': 'Curta', 'param': 'Curta', 'type': 'uint', 'default': 3, 'label': 'Curta глубина сглаживания', 'sinput': False}, {'mql': 'CPhase', 'py': 'CPhase', 'param': 'CPhase', 'type': 'int', 'default': 15, 'label': 'Curta параметр сглаживания', 'sinput': False}, {'mql': 'Media_Method', 'py': 'Media_Method', 'param': 'Media_Method', 'type': 'int', 'default': 0, 'label': 'Media метод усреднения', 'sinput': False}, {'mql': 'Media', 'py': 'Media', 'param': 'Media', 'type': 'uint', 'default': 8, 'label': 'Media глубина сглаживания', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'int', 'default': 15, 'label': 'Media параметр сглаживания', 'sinput': False}, {'mql': 'Longa_Method', 'py': 'Longa_Method', 'param': 'Longa_Method', 'type': 'int', 'default': 0, 'label': 'Longa метод усреднения', 'sinput': False}, {'mql': 'Longa', 'py': 'Longa', 'param': 'Longa', 'type': 'uint', 'default': 20, 'label': 'Longa глубина сглаживания', 'sinput': False}, {'mql': 'LPhase', 'py': 'LPhase', 'param': 'LPhase', 'type': 'int', 'default': 15, 'label': 'Longa параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Revers', 'py': 'Revers', 'param': 'Revers', 'type': 'bool', 'default': False, 'label': 'Переворот графика относительно оси времени', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
Curta_Method = _input('Curta_Method', MODE_SMA)  # Curta метод усреднения
Curta = _input('Curta', 3)  # Curta глубина сглаживания
CPhase = _input('CPhase', 15)  # Curta параметр сглаживания
Media_Method = _input('Media_Method', MODE_SMA)  # Media метод усреднения
Media = _input('Media', 8)  # Media глубина сглаживания
MPhase = _input('MPhase', 15)  # Media параметр сглаживания
Longa_Method = _input('Longa_Method', MODE_SMA)  # Longa метод усреднения
Longa = _input('Longa', 20)  # Longa глубина сглаживания
LPhase = _input('LPhase', 15)  # Longa параметр сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Revers = _input('Revers', False)  # Переворот графика относительно оси времени
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = MathMax(MathMax(GetStartBars(Curta_Method, Curta, CPhase), GetStartBars(Media_Method, Media, MPhase)), GetStartBars(Longa_Method, Longa, LPhase))
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'XDidi_Index'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    Cur = 0.0
    Med = 0.0
    Lon = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        Cur = XMA1.XMASeries(0, prev_calculated, rates_total, Curta_Method, CPhase, Curta, price, bar, False)
        Med = XMA2.XMASeries(0, prev_calculated, rates_total, Media_Method, MPhase, Media, price, bar, False)
        Lon = XMA3.XMASeries(0, prev_calculated, rates_total, Longa_Method, LPhase, Longa, price, bar, False)
        if Revers:
            DnBuffer[bar] = _fdiv(-Cur, Med)
            UpBuffer[bar] = _fdiv(-Lon, Med)
        else:
            UpBuffer[bar] = _fdiv(Cur, Med)
            DnBuffer[bar] = _fdiv(Lon, Med)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XdidiIndex(_MQL5Indicator):
    name = 'xdidi_index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Curta_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Curta метод усреднения
        'Curta': 3,  # Curta глубина сглаживания
        'CPhase': 15,  # Curta параметр сглаживания
        'Media_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Media метод усреднения
        'Media': 8,  # Media глубина сглаживания
        'MPhase': 15,  # Media параметр сглаживания
        'Longa_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Longa метод усреднения
        'Longa': 20,  # Longa глубина сглаживания
        'LPhase': 15,  # Longa параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Revers': False,  # Переворот графика относительно оси времени
    }

