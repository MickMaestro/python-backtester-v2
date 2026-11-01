"""2XMA_Ichimoku_Signal — converted from MQL5: MQL5 Indicators/2XMA_Ichimoku_Signal/2XMA_Ichimoku_Signal.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: '2XMA_Ichimoku Sell', 2: '2XMA_Ichimoku Buy'}, 'levels': [], 'description': [], 'name': '2XMA_Ichimoku_Signal', 'source': 'MQL5 Indicators/2XMA_Ichimoku_Signal/2XMA_Ichimoku_Signal.mq5', 'folder': '2XMA_Ichimoku_Signal', 'inputs': [{'mql': 'Up_period1', 'py': 'Up_period1', 'param': 'Up_period1', 'type': 'uint', 'default': 6, 'label': '1 период, используемый для вычисления наивысшего значения цены', 'sinput': False}, {'mql': 'Dn_period1', 'py': 'Dn_period1', 'param': 'Dn_period1', 'type': 'uint', 'default': 6, 'label': '1 период, используеммый для вычисления наинизшего значения цены', 'sinput': False}, {'mql': 'Up_period2', 'py': 'Up_period2', 'param': 'Up_period2', 'type': 'uint', 'default': 9, 'label': '2 период, используемый для вычисления наивысшего значения цены', 'sinput': False}, {'mql': 'Dn_period2', 'py': 'Dn_period2', 'param': 'Dn_period2', 'type': 'uint', 'default': 9, 'label': '2 период, используеммый для вычисления наинизшего значения цены', 'sinput': False}, {'mql': 'Up_mode1', 'py': 'Up_mode1', 'param': 'Up_mode1', 'type': 'int', 'default': 2, 'label': '1 таймсерия для поиска максимумов', 'sinput': False}, {'mql': 'Dn_mode1', 'py': 'Dn_mode1', 'param': 'Dn_mode1', 'type': 'int', 'default': 1, 'label': '1 таймсерия для поиска минимумов', 'sinput': False}, {'mql': 'Up_mode2', 'py': 'Up_mode2', 'param': 'Up_mode2', 'type': 'int', 'default': 2, 'label': '2 таймсерия для поиска максимумов', 'sinput': False}, {'mql': 'Dn_mode2', 'py': 'Dn_mode2', 'param': 'Dn_mode2', 'type': 'int', 'default': 1, 'label': '2 таймсерия для поиска минимумов', 'sinput': False}, {'mql': 'XMA1_Method', 'py': 'XMA1_Method', 'param': 'XMA1_Method', 'type': 'int', 'default': 0, 'label': '1 метод усреднения', 'sinput': False}, {'mql': 'XMA2_Method', 'py': 'XMA2_Method', 'param': 'XMA2_Method', 'type': 'int', 'default': 0, 'label': '2 метод усреднения', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'int', 'default': 25, 'label': '1 глубина сглаживания', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'int', 'default': 80, 'label': '2 глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum MODE_PRICE
OPEN = 0
LOW = 1
HIGH = 2
CLOSE = 3
_enum('MODE_PRICE', {0: 'OPEN', 1: 'LOW', 2: 'HIGH', 3: 'CLOSE'})

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
Up_period1 = _input('Up_period1', 6)  # 1 период, используемый для вычисления наивысшего значения цены
Dn_period1 = _input('Dn_period1', 6)  # 1 период, используеммый для вычисления наинизшего значения цены
Up_period2 = _input('Up_period2', 9)  # 2 период, используемый для вычисления наивысшего значения цены
Dn_period2 = _input('Dn_period2', 9)  # 2 период, используеммый для вычисления наинизшего значения цены
Up_mode1 = _input('Up_mode1', HIGH)  # 1 таймсерия для поиска максимумов
Dn_mode1 = _input('Dn_mode1', LOW)  # 1 таймсерия для поиска минимумов
Up_mode2 = _input('Up_mode2', HIGH)  # 2 таймсерия для поиска максимумов
Dn_mode2 = _input('Dn_mode2', LOW)  # 2 таймсерия для поиска минимумов
XMA1_Method = _input('XMA1_Method', MODE_SMA_)  # 1 метод усреднения
XMA2_Method = _input('XMA2_Method', MODE_SMA_)  # 2 метод усреднения
XLength1 = _input('XLength1', 25)  # 1 глубина сглаживания
XLength2 = _input('XLength2', 80)  # 2 глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр усреднения,
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates = 0
ATR_Handle = 0

def FindMaximum(Open, High, Low, Close, Mode, index, period):
    max_ = 0
    Mode_ = Mode
    _sw1 = Mode_
    if _sw1 == OPEN:
        max_ = ArrayMaximum(Open, index, period)
    elif _sw1 == LOW:
        max_ = ArrayMaximum(Low, index, period)
    elif _sw1 == HIGH:
        max_ = ArrayMaximum(High, index, period)
    elif _sw1 == CLOSE:
        max_ = ArrayMaximum(Close, index, period)
    return max_

def FindMinimum(Open, High, Low, Close, Mode, index, period):
    min_ = 0
    Mode_ = Mode
    _sw2 = Mode_
    if _sw2 == OPEN:
        min_ = ArrayMinimum(Open, index, period)
    elif _sw2 == LOW:
        min_ = ArrayMinimum(Low, index, period)
    elif _sw2 == HIGH:
        min_ = ArrayMinimum(High, index, period)
    elif _sw2 == CLOSE:
        min_ = ArrayMinimum(Close, index, period)
    return min_

def OnInit():
    global ATR_Handle, min_rates, min_rates_total
    min_rates_1 = _int(MathMax(Up_period1, Dn_period1))
    min_rates_1 += GetStartBars(XMA1_Method, XLength1, XPhase)
    min_rates = min_rates_1
    min_rates_2 = _int(MathMax(Up_period2, Dn_period2))
    min_rates_2 += GetStartBars(XMA2_Method, XLength2, XPhase)
    min_rates = MathMax(min_rates, min_rates_2)
    min_rates_total = MathMax(min_rates_1, min_rates_2)
    ATR_Period = 15
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    shortname = '2XMA_Ichimoku_Signal'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend_prev, _s_OnCalculate_xma_ichimoku_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ish_Up = 0.0
    ish_Dn = 0.0
    xma1 = 0.0
    xma2 = 0.0
    xma_ichimoku = 0.0
    ATR = Arr(0, 0.0)
    limit = 0
    to_copy = 0
    trend = 0
    maxbar = rates_total - min_rates - 1
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
        _s_OnCalculate_trend_prev = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    for bar in range(limit, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        ish_Up = high[FindMaximum(open, high, low, close, Up_mode1, bar, Up_period1)]
        ish_Dn = low[FindMinimum(open, high, low, close, Dn_mode1, bar, Dn_period1)]
        xma1 = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA1_Method, XPhase, XLength1, (ish_Up + ish_Dn) / 2, bar, True)
        ish_Up = high[FindMaximum(open, high, low, close, Up_mode2, bar, Up_period2)]
        ish_Dn = low[FindMinimum(open, high, low, close, Dn_mode2, bar, Dn_period2)]
        xma2 = XMA2.XMASeries(maxbar, prev_calculated, rates_total, XMA2_Method, XPhase, XLength2, (ish_Up + ish_Dn) / 2, bar, True)
        trend = _s_OnCalculate_trend_prev
        xma_ichimoku = xma1 - xma2
        if xma_ichimoku > _s_OnCalculate_xma_ichimoku_prev:
            trend = 1
        if xma_ichimoku < _s_OnCalculate_xma_ichimoku_prev:
            trend = -1
        if _s_OnCalculate_trend_prev < 0 and trend > 0:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_trend_prev > 0 and trend < 0:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_trend_prev = trend
            _s_OnCalculate_xma_ichimoku_prev = xma_ichimoku
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_OnCalculate_xma_ichimoku_prev = 0.0
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2XMAIchimokuSignal(_MQL5Indicator):
    name = '2XMA_Ichimoku_Signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Up_period1': 6,  # 1 период, используемый для вычисления наивысшего значения цены
        'Dn_period1': 6,  # 1 период, используеммый для вычисления наинизшего значения цены
        'Up_period2': 9,  # 2 период, используемый для вычисления наивысшего значения цены
        'Dn_period2': 9,  # 2 период, используеммый для вычисления наинизшего значения цены
        'Up_mode1': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=2),  # 1 таймсерия для поиска максимумов
        'Dn_mode1': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=1),  # 1 таймсерия для поиска минимумов
        'Up_mode2': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=2),  # 2 таймсерия для поиска максимумов
        'Dn_mode2': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=1),  # 2 таймсерия для поиска минимумов
        'XMA1_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # 1 метод усреднения
        'XMA2_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # 2 метод усреднения
        'XLength1': 25,  # 1 глубина сглаживания
        'XLength2': 80,  # 2 глубина сглаживания
        'XPhase': 15,  # параметр усреднения,
    }

