"""ColorJSatl_Digit — converted from MQL5: MQL5 Indicators/ColorJSatl_Digit/ColorJSatl_Digit.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [9639167, 16748574]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'JSatl'}, 'levels': [], 'description': [], 'name': 'ColorJSatl_Digit', 'source': 'MQL5 Indicators/ColorJSatl_Digit/ColorJSatl_Digit.mq5', 'folder': 'ColorJSatl_Digit', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ColorJSatl_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'iLength', 'py': 'iLength', 'param': 'iLength', 'type': 'uint', 'default': 5, 'label': 'глубина JMA сглаживания', 'sinput': False}, {'mql': 'iPhase', 'py': 'iPhase', 'param': 'iPhase', 'type': 'int', 'default': 100, 'label': 'параметр JMA сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'SATLShift', 'py': 'SATLShift', 'param': 'SATLShift', 'type': 'int', 'default': 0, 'label': 'сдвиг Фатла по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг Фатла по вертикали в пунктах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовую метку', 'sinput': False}, {'mql': 'Price_color', 'py': 'Price_color', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет ценовой метки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
SirName = _input('SirName', 'ColorJSatl_Digit')  # Первая часть имени графических объектов
iLength = _input('iLength', 5)  # глубина JMA сглаживания
iPhase = _input('iPhase', 100)  # параметр JMA сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
SATLShift = _input('SATLShift', 0)  # сдвиг Фатла по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг Фатла по вертикали в пунктах
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовую метку
Price_color = _input('Price_color', clrGray)  # цвет ценовой метки
SATLPeriod = 65
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0
fstart = 0
SATLSize = 0
dPriceShift = 0.0
PointPow10 = 0.0
Price_name = ""

def OnInit():
    global PointPow10, Price_name, dPriceShift, min_rates_total
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, SATLShift)
    min_rates_total = SATLSize + 30
    PointPow10 = Point() * MathPow(10, Digit)
    Price_name = SirName + 'Price'
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'JSatl(', iLength, ' ,', iPhase, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    dPriceShift = Point() * PriceShift
    JMA.JJMALengthCheck('iLength', iLength)
    JMA.JJMAPhaseCheck('iPhase', iPhase)

def OnDeinit(reason):
    ObjectDelete(0, Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global fstart
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    satl = 0.0
    jsatl = 0.0
    trend = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = SATLPeriod - 1
        fstart = first
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        satl = STL.SATLSeries(0, prev_calculated, rates_total, price, bar, False)
        jsatl = JMA.JJMASeries(fstart, prev_calculated, rates_total, 0, iPhase, iLength, satl, bar, False)
        ExtLineBuffer[bar] = (PointPow10 * MathRound(_fdiv(jsatl, PointPow10))) + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (1 * PeriodSeconds())
        SetRightPrice(0, Price_name, 0, time0, ExtLineBuffer[bar0], Price_color)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = ColorExtLineBuffer[bar - 1]
        trend = ExtLineBuffer[bar] - ExtLineBuffer[bar - 1]
        if trend > 0:
            clr = 1.0
        if trend < 0:
            clr = 0.0
        ColorExtLineBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
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
JMA = _alloc(CJJMA)
JMA.__init__()
STL = _alloc(CSATL)
STL.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorJSatlDigit(_MQL5Indicator):
    name = 'ColorJSatl_Digit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iLength': 5,  # глубина JMA сглаживания
        'iPhase': 100,  # параметр JMA сглаживания,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'SATLShift': 0,  # сдвиг Фатла по горизонтали в барах
        'PriceShift': 0,  # cдвиг Фатла по вертикали в пунктах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовую метку
    }

