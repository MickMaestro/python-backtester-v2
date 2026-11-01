"""squize_ma — converted from MQL5: MQL5 Indicators/Squize_MA_HTF/squize_ma.mq5

Новая и очень удачная версия MA - на график добавлены условные границы флета.
Выход за них сигнализирует о возникновении условий для устойчивого тренда.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [1993170], 2: [8421376], 3: [255], 4: [14822282]}, 'widths': {1: 2, 2: 5, 3: 5, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Squize_MA1', 2: '+Squize_MA Env', 3: '-Squize_MA Env', 4: 'Squize_MA2'}, 'levels': [], 'description': ['Новая и очень удачная версия MA - на график добавлены условные границы флета.', 'Выход за них сигнализирует о возникновении условий для устойчивого тренда.'], 'name': 'squize_ma', 'source': 'MQL5 Indicators/Squize_MA_HTF/squize_ma.mq5', 'folder': 'Squize_MA_HTF', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 1, 'label': 'Метод первого усреднения', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 5, 'label': 'Глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр первого среднения', 'sinput': False}, {'mql': 'IPC1', 'py': 'IPC1', 'param': 'IPC1', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 1, 'label': 'Метод второго усреднения', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 21, 'label': 'Глубина  второго усреднения', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Параметр второго сглаживания', 'sinput': False}, {'mql': 'IPC2', 'py': 'IPC2', 'param': 'IPC2', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'MAsThreSHoldPips', 'py': 'MAsThreSHoldPips', 'param': 'MAsThreSHoldPips', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'ATRmode', 'py': 'ATRmode', 'param': 'ATRmode', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'ATRperiod', 'py': 'ATRperiod', 'param': 'ATRperiod', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'ATRmultipl', 'py': 'ATRmultipl', 'param': 'ATRmultipl', 'type': 'double', 'default': 0.4, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_EMA)  # Метод первого усреднения
Length1 = _input('Length1', 5)  # Глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # Параметр первого среднения
IPC1 = _input('IPC1', PRICE_CLOSE)  # Ценовая константа
MA_Method2 = _input('MA_Method2', MODE_EMA)  # Метод второго усреднения
Length2 = _input('Length2', 21)  # Глубина  второго усреднения
Phase2 = _input('Phase2', 100)  # Параметр второго сглаживания
IPC2 = _input('IPC2', PRICE_CLOSE)  # Ценовая константа
MAsThreSHoldPips = _input('MAsThreSHoldPips', 15)
ATRmode = _input('ATRmode', True)
ATRperiod = _input('ATRperiod', 50)
ATRmultipl = _input('ATRmultipl', 0.4)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
XMA1Buffer = Arr(0, 0.0)
XMA2Buffer = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ATR_Handle = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = XMA2.GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total = MathMax(min_rates_1, min_rates_2)
    if ATRmode:
        min_rates_total += ATRperiod
    XMA1.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA2.XMALengthCheck('BandsPeriod', ATRperiod)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    if ATRmode:
        ATR_Handle = iATR(None, PERIOD_CURRENT, ATRperiod)
        if ATR_Handle == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора ATR')
    SetIndexBuffer(0, XMA1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(XMA1Buffer, True)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    SetIndexBuffer(3, XMA2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(XMA2Buffer, True)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method1)
    Smooth2 = XMA1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'X2MA_Bollinger Bands(', Length1, ', ', Length2, ', ', ATRperiod, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (ATRmode and BarsCalculated(ATR_Handle) < rates_total) or rates_total < _int(min_rates_total):
        return 0
    price_1 = 0.0
    price_2 = 0.0
    x1xma = 0.0
    x2xma = 0.0
    madif = 0.0
    delta = 0.0
    Range = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    if ATRmode:
        if CopyBuffer(ATR_Handle, 0, 0, to_copy, Range) <= 0:
            return 0
    ArraySetAsSeries(Range, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        price_1 = PriceSeries(IPC1, bar, open, low, high, close)
        price_2 = PriceSeries(IPC2, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(maxbar, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price_1, bar, True)
        x2xma = XMA2.XMASeries(maxbar, prev_calculated, rates_total, MA_Method2, Phase2, Length2, price_2, bar, True)
        madif = MathAbs(x1xma - x2xma)
        XMA1Buffer[bar] = x1xma
        XMA2Buffer[bar] = x2xma
        if ATRmode:
            delta = _fdiv(Range[bar] * ATRmultipl, Point())
        else:
            delta = MAsThreSHoldPips
        if _fdiv(madif, Point()) < delta:
            dPoint = delta * Point()
            ExtLineBuffer1[bar] = x2xma + dPoint
            ExtLineBuffer2[bar] = x2xma - dPoint
        else:
            ExtLineBuffer1[bar] = EMPTY_VALUE
            ExtLineBuffer2[bar] = EMPTY_VALUE
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


class SquizeMa(_MQL5Indicator):
    name = 'squize_ma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод первого усреднения
        'Length1': 5,  # Глубина  первого сглаживания
        'Phase1': 15,  # Параметр первого среднения
        'IPC1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Ценовая константа
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод второго усреднения
        'Length2': 21,  # Глубина  второго усреднения
        'Phase2': 100,  # Параметр второго сглаживания
        'IPC2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Ценовая константа
        'MAsThreSHoldPips': 15,
        'ATRmode': True,
        'ATRperiod': 50,
        'ATRmultipl': 0.4,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

