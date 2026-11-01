"""blautvi — converted from MQL5: MQL5 Indicators/BlauTVI/blautvi.mq5

Tick Volume Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 42495, 8421504, 16760576, 16711680]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Tick Volume Index'}, 'levels': [], 'description': ['Tick Volume Index'], 'name': 'blautvi', 'source': 'MQL5 Indicators/BlauTVI/blautvi.mq5', 'folder': 'BlauTVI', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 12, 'label': 'Глубина первого усреднения', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 12, 'label': 'Глубина второго усреднения', 'sinput': False}, {'mql': 'XLength3', 'py': 'XLength3', 'param': 'XLength3', 'type': 'uint', 'default': 5, 'label': 'Глубина третьего усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объём', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_EMA)  # Метод усреднения
XLength1 = _input('XLength1', 12)  # Глубина первого усреднения
XLength2 = _input('XLength2', 12)  # Глубина второго усреднения
XLength3 = _input('XLength3', 5)  # Глубина третьего усреднения
XPhase = _input('XPhase', 15)  # Параметр сглаживания
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объём
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = XMA1.GetStartBars(XMA_Method, XLength1, XPhase)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(XMA_Method, XLength2, XPhase)
    min_rates_total = min_rates_2 + XMA1.GetStartBars(XMA_Method, XLength3, XPhase)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 4)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Tick Volume Index')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    UpTicks = 0.0
    XUpTicks = 0.0
    XXUpTicks = 0.0
    DnTicks = 0.0
    XDnTicks = 0.0
    XXDnTicks = 0.0
    TVI_Raw = 0.0
    XTVI_Raw = 0.0
    first = 0
    bar = 0
    Vol = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if VolumeType == VOLUME_TICK:
            Vol = tick_volume[bar]
        else:
            Vol = volume[bar]
        UpTicks = (Vol + _fdiv(close[bar] - open[bar], Point())) / 2
        DnTicks = Vol - UpTicks
        XUpTicks = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, UpTicks, bar, False)
        XDnTicks = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, DnTicks, bar, False)
        XXUpTicks = XMA3.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, XUpTicks, bar, False)
        XXDnTicks = XMA4.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, XDnTicks, bar, False)
        TVI_Raw = _fdiv(100.0 * (XXUpTicks - XXDnTicks), XXUpTicks + XXDnTicks)
        XTVI_Raw = XMA5.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, TVI_Raw, bar, False)
        IndBuffer[bar] = XTVI_Raw
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
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
XMA4 = _alloc(CXMA)
XMA4.__init__()
XMA5 = _alloc(CXMA)
XMA5.__init__()
XMA6 = _alloc(CXMA)
XMA6.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Blautvi(_MQL5Indicator):
    name = 'blautvi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения
        'XLength1': 12,  # Глубина первого усреднения
        'XLength2': 12,  # Глубина второго усреднения
        'XLength3': 5,  # Глубина третьего усреднения
        'XPhase': 15,  # Параметр сглаживания
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объём
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

