"""Heiken_Ashi_Smoothed_Trend — converted from MQL5: MQL5 Indicators/Heiken_Ashi_Smoothed_Trend_HTF/Heiken_Ashi_Smoothed_Trend.mq5

Семафорный сигнальный индикатор, подающий торговые сигналы при изменении направления свечей Heiken Ashi Smoothed
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16776960], 2: [9639167]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Heiken_Ashi_Smoothed_Trend Buy', 2: 'Heiken_Ashi_Smoothed_Trend Sell'}, 'levels': [], 'description': ['Семафорный сигнальный индикатор, подающий торговые сигналы при изменении направления свечей Heiken Ashi Smoothed'], 'name': 'Heiken_Ashi_Smoothed_Trend', 'source': 'MQL5 Indicators/Heiken_Ashi_Smoothed_Trend_HTF/Heiken_Ashi_Smoothed_Trend.mq5', 'folder': 'Heiken_Ashi_Smoothed_Trend_HTF', 'inputs': [{'mql': 'HMA_Method', 'py': 'HMA_Method', 'param': 'HMA_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'HLength', 'py': 'HLength', 'param': 'HLength', 'type': 'int', 'default': 30, 'label': 'Глубина  усреднения', 'sinput': False}, {'mql': 'HPhase', 'py': 'HPhase', 'param': 'HPhase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения, влияет на качество переходного процесса,', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'BuySymb', 'py': 'BuySymb', 'param': 'BuySymb', 'type': 'uint', 'default': 174, 'label': 'Символ покупки', 'sinput': False}, {'mql': 'SellSymb', 'py': 'SellSymb', 'param': 'SellSymb', 'type': 'uint', 'default': 174, 'label': 'Символ продажи', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
HMA_Method = _input('HMA_Method', MODE_JJMA)  # Метод усреднения
HLength = _input('HLength', 30)  # Глубина  усреднения
HPhase = _input('HPhase', 100)  # Параметр усреднения, влияет на качество переходного процесса,
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
BuySymb = _input('BuySymb', 174)  # Символ покупки
SellSymb = _input('SellSymb', 174)  # Символ продажи
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_1, min_rates_total
    ATR_Period = 15
    min_rates_1 = ATR_Period
    min_rates_total = min_rates_1 + XMAO.GetStartBars(HMA_Method, HLength, HPhase) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    XMAO.XMAPhaseCheck('HPhase', HPhase, HMA_Method)
    IndInit(0, BuyBuffer, INDICATOR_DATA)
    IndInit(1, SellBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, min_rates_total, 0, BuySymb)
    PlotInit(1, 0.0, min_rates_total, 0, SellSymb)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Heiken Ashi Smoothed'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift, ArrSymb):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_ARROW, ArrSymb)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_C_prev, _s_OnCalculate_O_prev, _s_OnCalculate_trend_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    first = 0
    trend = 0
    ATR = Arr(0, 0.0)
    XmaOpen = 0.0
    XmaHigh = 0.0
    XmaLow = 0.0
    XmaClose = 0.0
    O = 0.0
    C = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
        _s_OnCalculate_O_prev = open[first]
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
        XmaOpen = XMAO.XMASeries(min_rates_1, prev_calculated, rates_total, HMA_Method, HPhase, HLength, open[bar], bar, False)
        XmaClose = XMAC.XMASeries(min_rates_1, prev_calculated, rates_total, HMA_Method, HPhase, HLength, close[bar], bar, False)
        XmaHigh = XMAH.XMASeries(min_rates_1, prev_calculated, rates_total, HMA_Method, HPhase, HLength, high[bar], bar, False)
        XmaLow = XMAL.XMASeries(min_rates_1, prev_calculated, rates_total, HMA_Method, HPhase, HLength, low[bar], bar, False)
        O = (_s_OnCalculate_O_prev + _s_OnCalculate_C_prev) / 2
        C = (XmaOpen + XmaHigh + XmaLow + XmaClose) / 4
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
XMAO = _alloc(CXMA)
XMAO.__init__()
XMAL = _alloc(CXMA)
XMAL.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAC = _alloc(CXMA)
XMAC.__init__()

# ---- static local variables
_s_OnCalculate_trend_prev = 0
_s_OnCalculate_O_prev = 0.0
_s_OnCalculate_C_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikenAshiSmoothedTrend(_MQL5Indicator):
    name = 'Heiken_Ashi_Smoothed_Trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'HLength': 30,  # Глубина  усреднения
        'HPhase': 100,  # Параметр усреднения, влияет на качество переходного процесса,
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'BuySymb': 174,  # Символ покупки
        'SellSymb': 174,  # Символ продажи
    }

