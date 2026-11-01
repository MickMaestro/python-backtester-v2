"""AverageChangeCandle — converted from MQL5: MQL5 Indicators/AverageChangeCandle/AverageChangeCandle.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [255, 8421504, 16760576]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Average Change'}, 'levels': [1.0], 'description': [], 'name': 'AverageChangeCandle', 'source': 'MQL5 Indicators/AverageChangeCandle/AverageChangeCandle.mq5', 'folder': 'AverageChangeCandle', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 3, 'label': 'метод усреднения мувинга', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 12, 'label': 'глубина усреднения мувинга', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр усреднения мувинга,', 'sinput': False}, {'mql': 'IPC1', 'py': 'IPC1', 'param': 'IPC1', 'type': 'int', 'default': 5, 'label': 'ценовая константа для  мувинга', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'метод сглаживания индикатора', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания индикатора', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания индикатора,', 'sinput': False}, {'mql': 'Pow', 'py': 'Pow', 'param': 'Pow', 'type': 'double', 'default': 5.0, 'label': 'степень', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MA_Method1 = _input('MA_Method1', MODE_LWMA_)  # метод усреднения мувинга
Length1 = _input('Length1', 12)  # глубина усреднения мувинга
Phase1 = _input('Phase1', 15)  # параметр усреднения мувинга,
IPC1 = _input('IPC1', PRICE_MEDIAN_)  # ценовая константа для  мувинга
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # метод сглаживания индикатора
Length2 = _input('Length2', 5)  # глубина сглаживания индикатора
Phase2 = _input('Phase2', 100)  # параметр сглаживания индикатора,
Pow = _input('Pow', 5.0)  # степень
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_ = 0
min_rates_total = 0

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_total = min_rates_ + XMA1.GetStartBars(MA_Method2, Length2, Phase2)
    XMA1.XMALengthCheck('Length1', Length1)
    XMA1.XMALengthCheck('Length2', Length2)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA1.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method1)
    Smooth2 = XMA1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'AverageChangeCandle(', Smooth1, ', ', Smooth2, ', ', Length1, ', ', Length2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price_1 = 0.0
    xma = 0.0
    res = 0.0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    maxbar1 = rates_total - 1
    maxbar2 = rates_total - min_rates_
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        price_1 = PriceSeries(IPC1, bar, open, low, high, close)
        xma = XMA1.XMASeries(maxbar1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price_1, bar, True)
        res = MathPow(_fdiv(open[bar], xma), Pow)
        ExtOpenBuffer[bar] = XMA2O.XMASeries(maxbar2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, res, bar, True)
        res = MathPow(_fdiv(high[bar], xma), Pow)
        ExtHighBuffer[bar] = XMA2H.XMASeries(maxbar2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, res, bar, True)
        res = MathPow(_fdiv(low[bar], xma), Pow)
        ExtLowBuffer[bar] = XMA2L.XMASeries(maxbar2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, res, bar, True)
        res = MathPow(_fdiv(close[bar], xma), Pow)
        ExtCloseBuffer[bar] = XMA2C.XMASeries(maxbar2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, res, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2O = _alloc(CXMA)
XMA2O.__init__()
XMA2H = _alloc(CXMA)
XMA2H.__init__()
XMA2L = _alloc(CXMA)
XMA2L.__init__()
XMA2C = _alloc(CXMA)
XMA2C.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AverageChangeCandle(_MQL5Indicator):
    name = 'AverageChangeCandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # метод усреднения мувинга
        'Length1': 12,  # глубина усреднения мувинга
        'Phase1': 15,  # параметр усреднения мувинга,
        'IPC1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=5),  # ценовая константа для  мувинга
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод сглаживания индикатора
        'Length2': 5,  # глубина сглаживания индикатора
        'Phase2': 100,  # параметр сглаживания индикатора,
        'Pow': 5.0,  # степень
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

