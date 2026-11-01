"""emv_histogram — converted from MQL5: MQL5 Indicators/EMV_Histogram_HTF/emv_histogram.mq5

Ease of Movement Value
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [16711680, 8388736], 2: [9639167, 42495, 8421504, 3329434, 8421376]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'EMV Signal', 2: 'Ease of Movement Value'}, 'levels': [], 'description': ['Ease of Movement Value'], 'name': 'emv_histogram', 'source': 'MQL5 Indicators/EMV_Histogram_HTF/emv_histogram.mq5', 'folder': 'EMV_Histogram_HTF', 'inputs': [{'mql': 'XMA_Method1', 'py': 'XMA_Method1', 'param': 'XMA_Method1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения основной линии', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'int', 'default': 14, 'label': 'Глубина сглаживания основной линии', 'sinput': False}, {'mql': 'XPhase1', 'py': 'XPhase1', 'param': 'XPhase1', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания основной линии', 'sinput': False}, {'mql': 'XMA_Method2', 'py': 'XMA_Method2', 'param': 'XMA_Method2', 'type': 'int', 'default': 4, 'label': 'Метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'int', 'default': 5, 'label': 'Глубина сглаживания сигнальной линии', 'sinput': False}, {'mql': 'XPhase2', 'py': 'XPhase2', 'param': 'XPhase2', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания сигнальной линии', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 9, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объем', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method1 = _input('XMA_Method1', MODE_SMA)  # Метод усреднения основной линии
XLength1 = _input('XLength1', 14)  # Глубина сглаживания основной линии
XPhase1 = _input('XPhase1', 15)  # Параметр сглаживания основной линии
XMA_Method2 = _input('XMA_Method2', MODE_JJMA)  # Метод усреднения сигнальной линии
XLength2 = _input('XLength2', 5)  # Глубина сглаживания сигнальной линии
XPhase2 = _input('XPhase2', 100)  # Параметр сглаживания сигнальной линии
IPC = _input('IPC', PRICE_QUARTER_)  # Ценовая константа
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объем
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = GetStartBars(XMA_Method1, XLength1, XPhase1) + 1
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method2, XLength2, XPhase2)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ease of Movement Value')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price0 = 0.0
    price1 = 0.0
    EMV = 0.0
    XEMV = 0.0
    Volume = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price0 = PriceSeries(PRICE_MEDIAN, bar, open, low, high, close)
        price1 = PriceSeries(PRICE_MEDIAN, bar - 1, open, low, high, close)
        if VolumeType == VOLUME_TICK:
            Volume = tick_volume[bar]
        else:
            Volume = volume[bar]
        if Volume != 0:
            EMV = _fdiv((price0 - price1) * price0, 2 * Volume)
        else:
            EMV = 0.0
        XEMV = XMA1.XMASeries(1, prev_calculated, rates_total, XMA_Method1, XPhase1, XLength1, EMV, bar, False)
        UpBuffer[bar] = XEMV
        IndBuffer[bar] = UpBuffer[bar]
        DnBuffer[bar] = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method2, XPhase2, XLength2, XEMV, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EmvHistogram(_MQL5Indicator):
    name = 'emv_histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения основной линии
        'XLength1': 14,  # Глубина сглаживания основной линии
        'XPhase1': 15,  # Параметр сглаживания основной линии
        'XMA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения сигнальной линии
        'XLength2': 5,  # Глубина сглаживания сигнальной линии
        'XPhase2': 100,  # Параметр сглаживания сигнальной линии
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=9),  # Ценовая константа
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объем
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

