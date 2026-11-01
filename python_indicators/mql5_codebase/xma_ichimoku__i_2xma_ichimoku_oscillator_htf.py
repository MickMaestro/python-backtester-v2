"""XMA_Ichimoku — converted from MQL5: MQL5 Indicators/2XMA_Ichimoku_Oscillator_HTF/XMA_Ichimoku.mq5

Ichimoku XMA
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Ichimoku XMA'}, 'levels': [], 'description': ['Ichimoku XMA'], 'name': 'XMA_Ichimoku', 'source': 'MQL5 Indicators/2XMA_Ichimoku_Oscillator_HTF/XMA_Ichimoku.mq5', 'folder': '2XMA_Ichimoku_Oscillator_HTF', 'inputs': [{'mql': 'Up_period', 'py': 'Up_period', 'param': 'Up_period', 'type': 'uint', 'default': 3, 'label': 'период, используемый для вычисления наивысшего значения цены', 'sinput': False}, {'mql': 'Dn_period', 'py': 'Dn_period', 'param': 'Dn_period', 'type': 'uint', 'default': 3, 'label': 'период, используеммый для вычисления наинизшего значения цены', 'sinput': False}, {'mql': 'Up_mode', 'py': 'Up_mode', 'param': 'Up_mode', 'type': 'int', 'default': 2, 'label': 'таймсерия для поиска максимумов', 'sinput': False}, {'mql': 'Dn_mode', 'py': 'Dn_mode', 'param': 'Dn_mode', 'type': 'int', 'default': 1, 'label': 'таймсерия для поиска минимумов', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 8, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Up_period = _input('Up_period', 3)  # период, используемый для вычисления наивысшего значения цены
Dn_period = _input('Dn_period', 3)  # период, используеммый для вычисления наинизшего значения цены
Up_mode = _input('Up_mode', HIGH)  # таймсерия для поиска максимумов
Dn_mode = _input('Dn_mode', LOW)  # таймсерия для поиска минимумов
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 8)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр усреднения,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
XMA = Arr(0, 0.0)
dPriceShift = 0.0
StartBars = 0
StartBars1 = 0

def OnInit():
    global StartBars, StartBars1, dPriceShift
    StartBars1 = _int(MathMax(Up_period, Dn_period))
    StartBars = StartBars1 + XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, XMA, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(XMA, True)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'Ichimoku XMA(', XLength, ', ', XPhase, ', ', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

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

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    ish_Up = 0.0
    ish_Dn = 0.0
    limit = 0
    maxbar = 0
    maxbar = rates_total - 1 - StartBars1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    for bar in range(limit, 0 - 1, -1):
        ish_Up = high[FindMaximum(open, high, low, close, Up_mode, bar, Up_period)]
        ish_Dn = low[FindMinimum(open, high, low, close, Dn_mode, bar, Dn_period)]
        XMA[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, (ish_Up + ish_Dn) / 2, bar, True) + PriceShift
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XMAIchimoku(_MQL5Indicator):
    name = 'XMA_Ichimoku'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Up_period': 3,  # период, используемый для вычисления наивысшего значения цены
        'Dn_period': 3,  # период, используеммый для вычисления наинизшего значения цены
        'Up_mode': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=2),  # таймсерия для поиска максимумов
        'Dn_mode': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=1),  # таймсерия для поиска минимумов
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 8,  # глубина сглаживания
        'XPhase': 15,  # параметр усреднения,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
    }

