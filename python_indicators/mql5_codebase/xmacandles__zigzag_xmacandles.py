"""XMACandles — converted from MQL5: MQL5 Indicators/ZigZag_XMACandles/XMACandles.mq5

XMA Candles
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [13850042, 13458026, 32768]}, 'widths': {}, 'styles': {}, 'labels': {1: 'X2MA Open; High; Low; Close'}, 'levels': [], 'description': ['XMA Candles'], 'name': 'XMACandles', 'source': 'MQL5 Indicators/ZigZag_XMACandles/XMACandles.mq5', 'folder': 'ZigZag_XMACandles', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 7, 'label': 'Метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 12, 'label': 'Глубина первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр первого сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_T3)  # Метод усреднения первого сглаживания
Length1 = _input('Length1', 12)  # Глубина первого сглаживания
Phase1 = _input('Phase1', 15)  # Параметр первого сглаживания,
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(MA_Method1, Length1, Phase1)
    OpXMA.XMALengthCheck('Length1', Length1)
    OpXMA.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    Smooth1 = OpXMA.GetString_MA_Method(MA_Method1)
    StringConcatenate(shortname, 'XMA Candles(', Smooth1, ', ', Length1, ', ', Phase1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

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
        ExtOpenBuffer[bar] = OpXMA.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, open[bar], bar, False)
        ExtHighBuffer[bar] = HiXMA.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, high[bar], bar, False)
        ExtLowBuffer[bar] = LoXMA.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, low[bar], bar, False)
        ExtCloseBuffer[bar] = ClXMA.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, close[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
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
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
OpXMA = _alloc(CXMA)
OpXMA.__init__()
HiXMA = _alloc(CXMA)
HiXMA.__init__()
LoXMA = _alloc(CXMA)
LoXMA.__init__()
ClXMA = _alloc(CXMA)
ClXMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XMACandles(_MQL5Indicator):
    name = 'XMACandles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения первого сглаживания
        'Length1': 12,  # Глубина первого сглаживания
        'Phase1': 15,  # Параметр первого сглаживания,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

