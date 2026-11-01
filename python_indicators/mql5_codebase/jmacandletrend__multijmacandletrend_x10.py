"""JMACandleTrend — converted from MQL5: MQL5 Indicators/MultiJMACandleTrend_x10/JMACandleTrend.mq5

Семафорный сигнальный индикатор, подающий торговые сигналы при изменении направления свечей JMACandle
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16748574], 2: [16711935]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'JMACandleTrend Buy', 2: 'JMACandleTrend Sell'}, 'levels': [], 'description': ['Семафорный сигнальный индикатор, подающий торговые сигналы при изменении направления свечей JMACandle'], 'name': 'JMACandleTrend', 'source': 'MQL5 Indicators/MultiJMACandleTrend_x10/JMACandleTrend.mq5', 'folder': 'MultiJMACandleTrend_x10', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 30, 'label': 'глубина усреднения', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'BuySymb', 'py': 'BuySymb', 'param': 'BuySymb', 'type': 'uint', 'default': 171, 'label': 'Символ покупки', 'sinput': False}, {'mql': 'SellSymb', 'py': 'SellSymb', 'param': 'SellSymb', 'type': 'uint', 'default': 171, 'label': 'Символ продажи', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_JJMA)  # метод усреднения
Length1 = _input('Length1', 30)  # глубина усреднения
Phase1 = _input('Phase1', 15)  # параметр усреднения,
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
BuySymb = _input('BuySymb', 171)  # Символ покупки
SellSymb = _input('SellSymb', 171)  # Символ продажи
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = GetStartBars(MA_Method1, Length1, Phase1)
    ATR_Period = 15
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    IndInit(0, BuyBuffer, INDICATOR_DATA)
    IndInit(1, SellBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, min_rates_total, 0, BuySymb)
    PlotInit(1, 0.0, min_rates_total, 0, SellSymb)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    Smooth1 = XMAo.GetString_MA_Method(MA_Method1)
    StringConcatenate(shortname, 'JMACandleTrend(', Length1, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    return INIT_SUCCEEDED

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift, ArrSymb):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_ARROW, ArrSymb)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_C_prev, _s_OnCalculate_trend_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    O = 0.0
    C = 0.0
    ATR = Arr(0, 0.0)
    to_copy = 0
    first = 0
    trend = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_C_prev = close[first]
        _s_OnCalculate_trend_prev = 0
    else:
        first = prev_calculated - 1
    to_copy = rates_total - first
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    for bar in range(first, rates_total):
        trend = _s_OnCalculate_trend_prev
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = SellBuffer[bar]
        O = XMAo.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, open[bar], bar, False)
        C = XMAc.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, close[bar], bar, False)
        if MathAbs(open[bar] - close[bar]) <= Gap:
            O = _s_OnCalculate_C_prev
        if O < C:
            trend = 1
        elif O > C:
            trend = -1
        if _s_OnCalculate_trend_prev <= 0 and trend > 0:
            BuyBuffer[bar] = low[bar] - ((ATR[rates_total - bar - 1] * 3) / 8)
        if _s_OnCalculate_trend_prev >= 0 and trend < 0:
            SellBuffer[bar] = high[bar] + ((ATR[rates_total - bar - 1] * 3) / 8)
        if bar < (rates_total - 1):
            _s_OnCalculate_C_prev = C
            _s_OnCalculate_trend_prev = trend
    return rates_total

# ---- global variables initialised from expressions
XMAo = _alloc(CXMA)
XMAo.__init__()
XMAc = _alloc(CXMA)
XMAc.__init__()

# ---- static local variables
_s_OnCalculate_C_prev = 0.0
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JMACandleTrend(_MQL5Indicator):
    name = 'JMACandleTrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'Length1': 30,  # глубина усреднения
        'Phase1': 15,  # параметр усреднения,
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'BuySymb': 171,  # Символ покупки
        'SellSymb': 171,  # Символ продажи
    }

