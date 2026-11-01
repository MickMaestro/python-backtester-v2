"""volatilityqualitysign — converted from MQL5: MQL5 Indicators/VolatilityQualitySign/volatilityqualitysign.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16748574]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'VolatilityQuality Sell', 2: 'VolatilityQuality Buy'}, 'levels': [], 'description': [], 'name': 'volatilityqualitysign', 'source': 'MQL5 Indicators/VolatilityQualitySign/volatilityqualitysign.mq5', 'folder': 'VolatilityQualitySign', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 5, 'label': 'Глубина  сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Smoothing', 'py': 'Smoothing', 'param': 'Smoothing', 'type': 'uint', 'default': 1, 'label': 'Глубина  пересчета', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'uint', 'default': 5, 'label': 'Фильтрация в пунктах ценового графика', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 5, 'label': 'Цена', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum App_price
PRICE_CLOSE_ = 1
PRICE_MEDIAN_ = 5
_enum('App_price', {1: 'PRICE_CLOSE_', 5: 'PRICE_MEDIAN_'})

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_LWMA)  # Метод усреднения
XLength = _input('XLength', 5)  # Глубина  сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
Smoothing = _input('Smoothing', 1)  # Глубина  пересчета
Filter = _input('Filter', 5)  # Фильтрация в пунктах ценового графика
Price = _input('Price', PRICE_MEDIAN)  # Цена
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
dFilter = 0.0
min_rates_total = 0
min_rates = 0
Len = 0
Count = Arr(0, 0)
Mc = Arr(0, 0.0)

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
    global ATR_Handle, Len, dFilter, min_rates, min_rates_total
    min_rates = GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_total = _int(min_rates + Smoothing + 1)
    ATR_Period = 10
    min_rates_total = MathMax(min_rates_total + 1, ATR_Period)
    Len = _int(Smoothing + 1)
    dFilter = Point() * Filter
    ArrayResize(Count, Len)
    ArrayResize(Mc, Len)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Mc, 0.0)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 175)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 175)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    shortname = Box("")
    Smooth = XmaMC.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'VolatilityQualitySign(', XLength, ', ', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_SumVQ_prev, _s_OnCalculate_trend_prev
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    MH = 0.0
    ML = 0.0
    MC = 0.0
    MC1 = 0.0
    MO = 0.0
    VQ = 0.0
    SumVQ = 0.0
    res1 = 0.0
    res2 = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    first = 0
    bar = 0
    trend = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_SumVQ_prev = PriceSeries(Price, 0, open, low, high, close)
        ArrayInitialize(Count, 0)
        ArrayInitialize(Mc, _s_OnCalculate_SumVQ_prev)
        _s_OnCalculate_trend_prev = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(Price, bar, open, low, high, close)
        Mc[Count[0]] = XmaMC.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, False)
        MC = Mc[Count[0]]
        MC1 = Mc[Count[Smoothing]]
        if bar == min_rates_total:
            _s_OnCalculate_SumVQ_prev = PriceSeries(Price, bar - 1, open, low, high, close)
        MH = XmaMH.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, high[bar], bar, False)
        ML = XmaML.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, low[bar], bar, False)
        MO = XmaMO.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, open[bar], bar, False)
        res1 = MathMax(MH - ML, MathMax(MH - MC1, MC1 - ML))
        res2 = MH - ML
        if res1 and res2:
            VQ = MathAbs((_fdiv(MC - MC1, res1) + _fdiv(MC - MO, res2)) * 0.5) * ((MC - MC1 + (MC - MO)) * 0.5)
        else:
            VQ = price
        SumVQ = _s_OnCalculate_SumVQ_prev + VQ
        if Filter and MathAbs(SumVQ - _s_OnCalculate_SumVQ_prev) < dFilter:
            SumVQ = _s_OnCalculate_SumVQ_prev
        if _s_OnCalculate_SumVQ_prev < SumVQ:
            trend = 1
        elif _s_OnCalculate_SumVQ_prev > SumVQ:
            trend = -1
        else:
            trend = _s_OnCalculate_trend_prev
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_trend_prev <= 0 and trend > 0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_trend_prev >= 0 and trend < 0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, Len)
            _s_OnCalculate_SumVQ_prev = SumVQ
            if trend:
                _s_OnCalculate_trend_prev = trend
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XmaMH = _alloc(CXMA)
XmaMH.__init__()
XmaML = _alloc(CXMA)
XmaML.__init__()
XmaMO = _alloc(CXMA)
XmaMO.__init__()
XmaMC = _alloc(CXMA)
XmaMC.__init__()
XmaMC1 = _alloc(CXMA)
XmaMC1.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_SumVQ_prev = 0.0
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Volatilityqualitysign(_MQL5Indicator):
    name = 'volatilityqualitysign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения
        'XLength': 5,  # Глубина  сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'Smoothing': 1,  # Глубина  пересчета
        'Filter': 5,  # Фильтрация в пунктах ценового графика
        'Price': _Choice({1: 'Close', 5: 'Median Price (HL/2)'}, default=5),  # Цена
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

