"""RJTX_Matches_Smoothed_main — converted from MQL5: MQL5 Indicators/RJTX_Matches_Smoothed_main/RJTX_Matches_Smoothed_main.mq5

We recommend adjust the body and head size of the matches for better visualization.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [13828244], 2: [13828244], 3: [13828244], 4: [9639167], 5: [16748574]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'match 1', 2: 'match 2', 3: 'match 3', 4: 'RJTX_Matches_Smoothed Sell', 5: 'RJTX_Matches_Smoothed Buy'}, 'levels': [], 'description': ['We recommend adjust the body and head size of the matches for better visualization.'], 'name': 'RJTX_Matches_Smoothed_main', 'source': 'MQL5 Indicators/RJTX_Matches_Smoothed_main/RJTX_Matches_Smoothed_main.mq5', 'folder': 'RJTX_Matches_Smoothed_main', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 10, 'label': 'Период индикатора свечек', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 10)  # Период индикатора свечек
XMA_Method = _input('XMA_Method', MODE_SMA_)  # Метод усреднения
XLength = _input('XLength', 12)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
LineBuffer0 = Arr(0, 0.0)
LineBuffer1 = Arr(0, 0.0)
LineBuffer2 = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
xOpen = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_total = _int(MathMax(iPeriod, min_rates_total))
    ArrayResize(Count, iPeriod + 1)
    ArrayResize(xOpen, iPeriod + 1)
    IndInit(0, LineBuffer0, 0.0, min_rates_total, 0)
    IndInit(1, LineBuffer1, 0.0, min_rates_total, 0)
    IndInit(2, LineBuffer2, 0.0, min_rates_total, 0)
    IndInit(3, SellBuffer, 0.0, min_rates_total, 0)
    IndInit(4, BuyBuffer, 0.0, min_rates_total, 0)
    PlotIndexSetInteger(3, PLOT_ARROW, 174)
    PlotIndexSetInteger(4, PLOT_ARROW, 174)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'RJTX_Matches_Smoothed'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_SHOW_DATA, False)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_p
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    xclose = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        ArrayInitialize(Count, 0)
        ArrayInitialize(xOpen, open[first])
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        xOpen[Count[0]] = XMAO.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, open[bar], bar, False)
        xclose = XMAC.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, close[bar], bar, False)
        if xclose > xOpen[Count[iPeriod]]:
            SellBuffer[bar] = 0.0
            BuyBuffer[bar] = xclose
        else:
            SellBuffer[bar] = xclose
            BuyBuffer[bar] = 0.0
        _sw1 = _s_OnCalculate_p
        if _sw1 == 0:
            LineBuffer0[bar] = xOpen[Count[iPeriod - 1]]
            LineBuffer1[bar] = 0.0
            LineBuffer2[bar] = xclose
        elif _sw1 == 1:
            LineBuffer0[bar] = xclose
            LineBuffer1[bar] = xOpen[Count[iPeriod - 1]]
            LineBuffer2[bar] = 0.0
        elif _sw1 == 2:
            LineBuffer0[bar] = 0.0
            LineBuffer1[bar] = xclose
            LineBuffer2[bar] = xOpen[Count[iPeriod - 1]]
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, iPeriod + 1)
            _s_OnCalculate_p += 1
        if _s_OnCalculate_p > 2:
            _s_OnCalculate_p = 0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMAO = _alloc(CXMA)
XMAO.__init__()
XMAC = _alloc(CXMA)
XMAC.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_p = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RJTXMatchesSmoothedMain(_MQL5Indicator):
    name = 'RJTX_Matches_Smoothed_main'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 10,  # Период индикатора свечек
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 12,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
    }

