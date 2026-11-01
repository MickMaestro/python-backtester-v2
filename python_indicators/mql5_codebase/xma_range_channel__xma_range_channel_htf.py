"""xma_range_channel — converted from MQL5: MQL5 Indicators/XMA_Range_Channel_HTF/xma_range_channel.mq5

XMA Ichimoku Channel
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 17}, 'colors': {1: [16443110], 2: [7451452], 3: [255], 4: [16711935, 8388736, 32768, 65280]}, 'widths': {2: 1, 3: 1}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'XMA Range Channel', 2: 'Up Line', 3: 'Down Line', 4: 'Open;High;Low;Close'}, 'levels': [], 'description': ['XMA Ichimoku Channel'], 'name': 'xma_range_channel', 'source': 'MQL5 Indicators/XMA_Range_Channel_HTF/xma_range_channel.mq5', 'folder': 'XMA_Range_Channel_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 7, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XLength = _input('XLength', 7)  # Глубина сглаживания
XPhase = _input('XPhase', 100)  # Параметр усреднения
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
UpLineBuffer = Arr(0, 0.0)
DnLineBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, UpLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DnLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    SetIndexBuffer(4, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'XMA_Range_Channel', XLength, ', ', XPhase, ', ', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        UpIndBuffer[bar] = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, high[bar], bar, False) + dPriceShift
        UpLineBuffer[bar] = UpIndBuffer[bar]
        DnIndBuffer[bar] = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, low[bar], bar, False) + dPriceShift
        DnLineBuffer[bar] = DnIndBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        ExtColorBuffer[bar] = EMPTY_VALUE
        ExtLowBuffer[bar] = ExtColorBuffer[bar]
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtCloseBuffer[bar] = ExtHighBuffer[bar]
        ExtOpenBuffer[bar] = ExtCloseBuffer[bar]
        if close[bar] > UpLineBuffer[bar]:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if close[bar] < DnLineBuffer[bar]:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] <= open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
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


class XmaRangeChannel(_MQL5Indicator):
    name = 'xma_range_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 7,  # Глубина сглаживания
        'XPhase': 100,  # Параметр усреднения
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

