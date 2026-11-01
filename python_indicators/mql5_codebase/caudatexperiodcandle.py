"""CaudateXPeriodCandle — converted from MQL5: MQL5 Indicators/CaudateXPeriodCandle/CaudateXPeriodCandle.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16748574, 16711680, 15658671, 8421504, 12695295, 128, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'CaudateXPeriodOpen;CaudateXPeriodHigh;CaudateXPeriodLow;CaudateXPeriodClose'}, 'levels': [], 'description': [], 'name': 'CaudateXPeriodCandle', 'source': 'MQL5 Indicators/CaudateXPeriodCandle/CaudateXPeriodCandle.mq5', 'folder': 'CaudateXPeriodCandle', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 5, 'label': 'Период расчёта свечей', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'int', 'default': 3, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
period = _input('period', 5)  # Период расчёта свечей
MA_SMethod = _input('MA_SMethod', MODE_JJMA)  # Метод усреднения
MA_Length = _input('MA_Length', 3)  # глубина сглаживания
MA_Phase = _input('MA_Phase', 100)  # параметр сглаживания,
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
Count = Arr(0, 0)
iopen = Arr(0, 0.0)
ihigh = Arr(0, 0.0)
ilow = Arr(0, 0.0)

def GetCandleType(index, Open, High, Low, Close):
    candleHalf = (High[index] + Low[index]) / 2
    if Open[index] < candleHalf and Close[index] < candleHalf:
        return 1
    if Open[index] > candleHalf and Close[index] > candleHalf:
        return 2
    return 0

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
    global min_rates_1, min_rates_total
    min_rates_1 = GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    min_rates_total = min_rates_1 + _int(period) + 1
    ArrayResize(Count, period)
    ArrayResize(iopen, period)
    ArrayResize(ihigh, period)
    ArrayResize(ilow, period)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'CaudateXPeriodCandle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    bar = 0
    limit = 0
    maxbar = rates_total - 1
    HH = 0.0
    LL = 0.0
    iclose = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
        ArrayInitialize(Count, 0)
        ArrayInitialize(iopen, open[maxbar])
        ArrayInitialize(ihigh, high[maxbar])
        ArrayInitialize(ilow, low[maxbar])
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        iopen[Count[0]] = XMAO.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, open[bar], bar, True)
        ihigh[Count[0]] = XMAH.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, high[bar], bar, True)
        ilow[Count[0]] = XMAL.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, low[bar], bar, True)
        iclose = XMAC.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, close[bar], bar, True)
        HH = ihigh[ArrayMaximum(ihigh, 0, period)]
        LL = ilow[ArrayMinimum(ilow, 0, period)]
        ExtOpenBuffer[bar] = iopen[Count[period - 1]]
        ExtHighBuffer[bar] = HH
        ExtLowBuffer[bar] = LL
        ExtCloseBuffer[bar] = iclose
        ExtColorsBuffer[bar] = 1.0
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] <= ExtCloseBuffer[bar]:
            ExtColorsBuffer[bar] = 2.0
        else:
            ExtColorsBuffer[bar] = 4.0
        _sw1 = GetCandleType(bar, ExtOpenBuffer, ExtHighBuffer, ExtLowBuffer, ExtCloseBuffer)
        if _sw1 == 0:
            pass
        elif _sw1 == 2:
            if ExtOpenBuffer[bar] <= ExtCloseBuffer[bar]:
                ExtColorsBuffer[bar] = 0.0
            else:
                ExtColorsBuffer[bar] = 1.0
        elif _sw1 == 1:
            if ExtOpenBuffer[bar] >= ExtCloseBuffer[bar]:
                ExtColorsBuffer[bar] = 6.0
            else:
                ExtColorsBuffer[bar] = 5.0
        if bar:
            Recount_ArrayZeroPos(Count, period)
    else:
        bar = _range_end(bar, 0 - 1, -1)
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
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CaudateXPeriodCandle(_MQL5Indicator):
    name = 'CaudateXPeriodCandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 5,  # Период расчёта свечей
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'MA_Length': 3,  # глубина сглаживания
        'MA_Phase': 100,  # параметр сглаживания,
    }

