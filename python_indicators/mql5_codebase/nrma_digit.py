"""NRMA_Digit — converted from MQL5: MQL5 Indicators/NRMA_Digit/NRMA_Digit.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'NRMA_Digit'}, 'levels': [], 'description': [], 'name': 'NRMA_Digit', 'source': 'MQL5 Indicators/NRMA_Digit/NRMA_Digit.mq5', 'folder': 'NRMA_Digit', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'NRMA_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 3, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Kf', 'py': 'Kf', 'param': 'Kf', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Fast', 'py': 'Fast', 'param': 'Fast', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'Sharp', 'py': 'Sharp', 'param': 'Sharp', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Price_color', 'py': 'Price_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
SirName = _input('SirName', 'NRMA_Digit')  # Первая часть имени графических объектов
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 3)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Kf = _input('Kf', 1.0)
Fast = _input('Fast', 2.0)
Sharp = _input('Sharp', 2.0)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Price_color = _input('Price_color', clrBlue)
IndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
dF = 0.0
PointPow10 = 0.0
min_rates_total = 0
Price_name = ""

def OnInit():
    global PointPow10, Price_name, dF, dPriceShift, min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase) + 1
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    dF = _fdiv(2.0, 1.0 + Fast)
    PointPow10 = Point() * MathPow(10, Digit)
    Price_name = SirName + 'Price'
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'NRMA(', XLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjectDelete(0, Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Trend1, _s_OnCalculate_nrtr1
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    LPrice = 0.0
    HPrice = 0.0
    Oscil = 0.0
    NRatio = 0.0
    xOscil = 0.0
    nrtr = 0.0
    first = 0
    bar = 0
    Trend0 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        bar = first - 1
        price = PriceSeries(IPC, bar, open, low, high, close)
        IndBuffer[bar] = price
        if close[first] > open[first]:
            _s_OnCalculate_Trend1 = 1
            _s_OnCalculate_nrtr1 = NormalizeDouble(price * (1.0 - (Kf * 0.01)), Digits())
        else:
            _s_OnCalculate_Trend1 = -1
            _s_OnCalculate_nrtr1 = NormalizeDouble(price * (1.0 + (Kf * 0.01)), Digits())
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        nrtr = _s_OnCalculate_nrtr1
        Trend0 = _s_OnCalculate_Trend1
        if _s_OnCalculate_Trend1 >= 0:
            if price < _s_OnCalculate_nrtr1:
                Trend0 = -1
                nrtr = NormalizeDouble(price * (1.0 + (Kf * 0.01)), Digits())
            else:
                Trend0 = 1
                LPrice = NormalizeDouble(price * (1.0 - (Kf * 0.01)), Digits())
                if LPrice > _s_OnCalculate_nrtr1:
                    nrtr = LPrice
                else:
                    nrtr = _s_OnCalculate_nrtr1
        if _s_OnCalculate_Trend1 <= 0:
            if price > _s_OnCalculate_nrtr1:
                Trend0 = 1
                nrtr = NormalizeDouble(price * (1.0 - (Kf * 0.01)), Digits())
            else:
                Trend0 = -1
                HPrice = NormalizeDouble(price * (1.0 + (Kf * 0.01)), Digits())
                if HPrice < _s_OnCalculate_nrtr1:
                    nrtr = HPrice
                else:
                    nrtr = _s_OnCalculate_nrtr1
        Oscil = _fdiv(100.0 * MathAbs(price - nrtr), price) / Kf
        xOscil = XMA1.XMASeries(1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, Oscil, bar, False)
        if bar < (min_rates_total - 1):
            IndBuffer[bar] = price
            if bar < (rates_total - 1):
                _s_OnCalculate_Trend1 = Trend0
                _s_OnCalculate_nrtr1 = nrtr
            continue
        NRatio = MathPow(xOscil, Sharp)
        IndBuffer[bar] = IndBuffer[bar - 1] + (NRatio * dF * (price - IndBuffer[bar - 1])) + dPriceShift
        IndBuffer[bar] = PointPow10 * MathRound(_fdiv(IndBuffer[bar], PointPow10))
        if bar < (rates_total - 1):
            _s_OnCalculate_Trend1 = Trend0
            _s_OnCalculate_nrtr1 = nrtr
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (1 * PeriodSeconds())
        SetRightPrice(0, Price_name, 0, time0, IndBuffer[bar0], Price_color)
    ChartRedraw(0)
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color)
    else:
        ObjectMove(chart_id, name, 0, time, price)

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_OnCalculate_Trend1 = 0
_s_OnCalculate_nrtr1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NRMADigit(_MQL5Indicator):
    name = 'NRMA_Digit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 3,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Kf': 1.0,
        'Fast': 2.0,
        'Sharp': 2.0,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовые метки
    }

