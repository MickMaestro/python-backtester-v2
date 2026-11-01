"""ergodic_ticks_volume_osma — converted from MQL5: MQL5 Indicators/Ergodic_Ticks_Volume_OSMA_HTF/ergodic_ticks_volume_osma.mq5

Ergodic Ticks Volume Indicator
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 10}, 'colors': {1: [16711935, 14524637, 8421504, 16748574, 16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Ergodic_Ticks_Volume_OSMA'}, 'levels': [], 'description': ['Ergodic Ticks Volume Indicator'], 'name': 'ergodic_ticks_volume_osma', 'source': 'MQL5 Indicators/Ergodic_Ticks_Volume_OSMA_HTF/ergodic_ticks_volume_osma.mq5', 'folder': 'Ergodic_Ticks_Volume_OSMA_HTF', 'inputs': [{'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объем', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 12, 'label': 'Глубина первого усреднения', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 12, 'label': 'Глубина второго усреднения', 'sinput': False}, {'mql': 'XLength3', 'py': 'XLength3', 'param': 'XLength3', 'type': 'uint', 'default': 1, 'label': 'Глубина третьего усреднения', 'sinput': False}, {'mql': 'XLength4', 'py': 'XLength4', 'param': 'XLength4', 'type': 'uint', 'default': 5, 'label': 'Глубина четвертого усреднения', 'sinput': False}, {'mql': 'XLength5', 'py': 'XLength5', 'param': 'XLength5', 'type': 'uint', 'default': 5, 'label': 'Глубина пятого усреднения', 'sinput': False}, {'mql': 'XLength6', 'py': 'XLength6', 'param': 'XLength6', 'type': 'uint', 'default': 5, 'label': 'Глубина шестого усреднения', 'sinput': False}, {'mql': 'XLength7', 'py': 'XLength7', 'param': 'XLength7', 'type': 'uint', 'default': 3, 'label': 'Глубина седьмого усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объем
XMA_Method = _input('XMA_Method', MODE_EMA)  # Метод усреднения
XLength1 = _input('XLength1', 12)  # Глубина первого усреднения
XLength2 = _input('XLength2', 12)  # Глубина второго усреднения
XLength3 = _input('XLength3', 1)  # Глубина третьего усреднения
XLength4 = _input('XLength4', 5)  # Глубина четвертого усреднения
XLength5 = _input('XLength5', 5)  # Глубина пятого усреднения
XLength6 = _input('XLength6', 5)  # Глубина шестого усреднения
XLength7 = _input('XLength7', 3)  # Глубина седьмого усреднения
XPhase = _input('XPhase', 15)  # Параметр сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
min_rates_4 = 0
min_rates_5 = 0
min_rates_6 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_4, min_rates_5, min_rates_6, min_rates_total
    min_rates_1 = XMA1.GetStartBars(XMA_Method, XLength1, XPhase)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(XMA_Method, XLength2, XPhase)
    min_rates_3 = min_rates_2 + XMA1.GetStartBars(XMA_Method, XLength3, XPhase)
    min_rates_4 = min_rates_3 + XMA1.GetStartBars(XMA_Method, XLength4, XPhase)
    min_rates_5 = min_rates_4 + XMA1.GetStartBars(XMA_Method, XLength5, XPhase)
    min_rates_6 = min_rates_5 + XMA1.GetStartBars(XMA_Method, XLength6, XPhase)
    min_rates_total = min_rates_6 + XMA1.GetStartBars(XMA_Method, XLength7, XPhase)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ergodic_Ticks_Volume_OSMA')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    UpTicks = 0.0
    DownTicks = 0.0
    EMA_UpTicks = 0.0
    EMA_DownTicks = 0.0
    DEMA_UpTicks = 0.0
    DEMA_DownTicks = 0.0
    res = 0.0
    TVI_calculate = 0.0
    TVI = 0.0
    EMA_TVI = 0.0
    Ergodic_TVI = 0.0
    Ergodic_Signal = 0.0
    MACD = 0.0
    Ergodic_OSMA = 0.0
    first = 0
    bar = 0
    Vol = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if VolumeType == VOLUME_TICK:
            Vol = tick_volume[bar]
        else:
            Vol = volume[bar]
        UpTicks = (Vol + _fdiv(close[bar] - open[bar], Point())) / 2
        DownTicks = Vol - UpTicks
        EMA_UpTicks = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, UpTicks, bar, False)
        EMA_DownTicks = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, DownTicks, bar, False)
        DEMA_UpTicks = XMA3.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, EMA_UpTicks, bar, False)
        DEMA_DownTicks = XMA4.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, EMA_DownTicks, bar, False)
        res = DEMA_UpTicks + DEMA_DownTicks
        if res:
            TVI_calculate = _fdiv(100.0 * (DEMA_UpTicks - DEMA_DownTicks), res)
        else:
            TVI_calculate = 0.0
        TVI = XMA5.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, TVI_calculate, bar, False)
        EMA_TVI = XMA6.XMASeries(min_rates_3, prev_calculated, rates_total, XMA_Method, XPhase, XLength4, TVI, bar, False)
        Ergodic_TVI = XMA7.XMASeries(min_rates_4, prev_calculated, rates_total, XMA_Method, XPhase, XLength5, EMA_TVI, bar, False)
        Ergodic_Signal = XMA8.XMASeries(min_rates_5, prev_calculated, rates_total, XMA_Method, XPhase, XLength6, Ergodic_TVI, bar, False)
        MACD = Ergodic_TVI - Ergodic_Signal
        Ergodic_OSMA = XMA9.XMASeries(min_rates_6, prev_calculated, rates_total, XMA_Method, XPhase, XLength7, MACD, bar, False)
        IndBuffer[bar] = Ergodic_OSMA
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
XMA7 = _alloc(CXMA)
XMA7.__init__()
XMA8 = _alloc(CXMA)
XMA8.__init__()
XMA9 = _alloc(CXMA)
XMA9.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ErgodicTicksVolumeOsma(_MQL5Indicator):
    name = 'ergodic_ticks_volume_osma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объем
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения
        'XLength1': 12,  # Глубина первого усреднения
        'XLength2': 12,  # Глубина второго усреднения
        'XLength3': 1,  # Глубина третьего усреднения
        'XLength4': 5,  # Глубина четвертого усреднения
        'XLength5': 5,  # Глубина пятого усреднения
        'XLength6': 5,  # Глубина шестого усреднения
        'XLength7': 3,  # Глубина седьмого усреднения
        'XPhase': 15,  # Параметр сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

