"""ytg_Price_Peak — converted from MQL5: MQL5 Indicators/ytg_Price_Peak_HTF/ytg_Price_Peak.mq5

Индикатор пиковых значений цен
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [14822282, 8421504, 16711935]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'ytg_Price_Peak'}, 'levels': [], 'description': ['Индикатор пиковых значений цен'], 'name': 'ytg_Price_Peak', 'source': 'MQL5 Indicators/ytg_Price_Peak_HTF/ytg_Price_Peak.mq5', 'folder': 'ytg_Price_Peak_HTF', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 1, 'label': 'метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 5, 'label': 'глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 1, 'label': 'метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 12, 'label': 'глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'параметр второго сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 2, 'label': 'объём', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# enum VolumeMode
VOLUME_TICK_ = 0
VOLUME_REAL_ = 1
NO_VOLUME = 2
_enum('VolumeMode', {0: 'VOLUME_TICK_', 1: 'VOLUME_REAL_', 2: 'NO_VOLUME'})

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_EMA_)  # метод усреднения первого сглаживания
Length1 = _input('Length1', 5)  # глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # параметр первого сглаживания,
MA_Method2 = _input('MA_Method2', MODE_EMA_)  # метод усреднения второго сглаживания
Length2 = _input('Length2', 12)  # глубина  второго сглаживания
Phase2 = _input('Phase2', 15)  # параметр второго сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
VolumeType = _input('VolumeType', NO_VOLUME)  # объём
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = XMA2.GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total = MathMax(min_rates_1, min_rates_2) + 1
    XMA1.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method1)
    Smooth2 = XMA1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'ytg_Price_Peak(', Length1, ', ', Length2, ', ', Smooth1, ', ', Smooth2, ', ', EnumToString(IPC, 'Applied_price_'), ', ', EnumToString(VolumeType, 'VolumeMode'), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price_ = 0.0
    xma1 = 0.0
    xma2 = 0.0
    macd = 0.0
    XL = 0.0
    XH = 0.0
    first = 0
    bar = 0
    Volume = 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        xma1 = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price_, bar, False)
        xma2 = XMA2.XMASeries(0, prev_calculated, rates_total, MA_Method2, Phase2, Length2, price_, bar, False)
        _sw1 = VolumeType
        if _sw1 == VOLUME_TICK:
            Volume = tick_volume[bar]
        elif _sw1 == VOLUME_REAL:
            Volume = volume[bar]
        elif _sw1 == NO_VOLUME:
            Volume = 1
        macd = xma1 - xma2
        XL = low[bar] - xma1
        XH = high[bar] - xma1
        ColorIndBuffer[bar] = 1.0
        IndBuffer[bar] = 0.0
        if macd > 0 and XL > 0:
            IndBuffer[bar] = _fdiv(XL * Volume, Point())
            ColorIndBuffer[bar] = 0.0
        if macd < 0 and XH < 0:
            IndBuffer[bar] = _fdiv(XH * Volume, Point())
            ColorIndBuffer[bar] = 2.0
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


class YtgPricePeak(_MQL5Indicator):
    name = 'ytg_Price_Peak'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод усреднения первого сглаживания
        'Length1': 5,  # глубина  первого сглаживания
        'Phase1': 15,  # параметр первого сглаживания,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод усреднения второго сглаживания
        'Length2': 12,  # глубина  второго сглаживания
        'Phase2': 15,  # параметр второго сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # ценовая константа
        'VolumeType': _Choice({0: 'Тиковый объем', 1: 'Торговый объем', 2: 'Объём не использовать'}, default=2),  # объём
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

