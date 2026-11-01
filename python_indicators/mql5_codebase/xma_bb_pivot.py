"""XMA_BB_Pivot — converted from MQL5: MQL5 Indicators/XMA_BB_Pivot/XMA_BB_Pivot.mq5

XMA Bollinger Bands Pivot
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['XMA Bollinger Bands Pivot'], 'name': 'XMA_BB_Pivot', 'source': 'MQL5 Indicators/XMA_BB_Pivot/XMA_BB_Pivot.mq5', 'folder': 'XMA_BB_Pivot', 'inputs': [{'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'XMA_BB_Pivot_', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 100, 'label': 'глубина  усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр первого усреднения,', 'sinput': False}, {'mql': 'BandsDeviation1', 'py': 'BandsDeviation1', 'param': 'BandsDeviation1', 'type': 'double', 'default': 2.0, 'label': 'девиация 1', 'sinput': False}, {'mql': 'BandsDeviation2', 'py': 'BandsDeviation2', 'param': 'BandsDeviation2', 'type': 'double', 'default': 4.0, 'label': 'девиация 2', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Up_Color', 'py': 'Up_Color', 'param': None, 'type': 'color', 'default': 13959039, 'label': 'Цвет верхней полосы индикатора', 'sinput': False}, {'mql': 'Dn_Color', 'py': 'Dn_Color', 'param': None, 'type': 'color', 'default': 14524637, 'label': 'Цвет нижней полосы индикатора', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'номер бара для получения значений индикатора', 'sinput': False}, {'mql': 'SignalLen', 'py': 'SignalLen', 'param': 'SignalLen', 'type': 'uint', 'default': 40, 'label': 'Длина полос индикатора', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
Symbols_Sirname = _input('Symbols_Sirname', 'XMA_BB_Pivot_')  # Название для меток индикатора
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 100)  # глубина  усреднения
XPhase = _input('XPhase', 15)  # параметр первого усреднения,
BandsDeviation1 = _input('BandsDeviation1', 2.0)  # девиация 1
BandsDeviation2 = _input('BandsDeviation2', 4.0)  # девиация 2
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Up_Color = _input('Up_Color', clrAquamarine)  # Цвет верхней полосы индикатора
Dn_Color = _input('Dn_Color', clrPlum)  # Цвет нижней полосы индикатора
SignalBar = _input('SignalBar', 0)  # номер бара для получения значений индикатора
SignalLen = _input('SignalLen', 40)  # Длина полос индикатора
min_rates_total = 0
min_rates_1 = 0
UpName = ""
DnName = ""
PerSignalLen = 0

def CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_RECTANGLE, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)

def SetRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnInit():
    global DnName, PerSignalLen, UpName, min_rates_1, min_rates_total
    min_rates_1 = GetStartBars(XMA_Method, XLength, XPhase) + 1
    min_rates_total = min_rates_1 + _int(XLength)
    UpName = Symbols_Sirname + 'Upper Band'
    DnName = Symbols_Sirname + 'Lower Band'
    PerSignalLen = _int(SignalLen) * PeriodSeconds()
    IndicatorSetString(INDICATOR_SHORTNAME, 'XMA_BB_Pivot')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjectsDeleteAll(0, Symbols_Sirname, -1, -1)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Dn1, _s_OnCalculate_Dn2, _s_OnCalculate_Up1, _s_OnCalculate_Up2
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    line = 0.0
    stdev = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total - _int(SignalBar)):
        price = PriceSeries(IPC, bar, open, low, high, close)
        line = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, False)
        stdev = STD1.StdDevSeries(min_rates_1, prev_calculated, rates_total, XLength, BandsDeviation1, price, line, bar, False)
        _s_OnCalculate_Up1 = line + stdev
        _s_OnCalculate_Dn1 = line - stdev
        stdev = STD2.StdDevSeries(min_rates_1, prev_calculated, rates_total, XLength, BandsDeviation2, price, line, bar, False)
        _s_OnCalculate_Up2 = line + stdev
        _s_OnCalculate_Dn2 = line - stdev
    else:
        bar = _range_end(bar, rates_total - _int(SignalBar), 1)
    bar0 = rates_total - 1
    bar1 = rates_total - _int(MathMax(SignalLen - 1, 0))
    time0 = time[bar0] + (2 * PeriodSeconds())
    time1 = time0 - PerSignalLen
    SetRectangle(0, UpName, 0, time1, _s_OnCalculate_Up1, time0, _s_OnCalculate_Up2, Up_Color, STYLE_SOLID, 1, UpName)
    SetRectangle(0, DnName, 0, time1, _s_OnCalculate_Dn1, time0, _s_OnCalculate_Dn2, Dn_Color, STYLE_SOLID, 1, DnName)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
STD1 = _alloc(CStdDeviation)
STD1.__init__()
STD2 = _alloc(CStdDeviation)
STD2.__init__()

# ---- static local variables
_s_OnCalculate_Up1 = 0.0
_s_OnCalculate_Up2 = 0.0
_s_OnCalculate_Dn1 = 0.0
_s_OnCalculate_Dn2 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XMABBPivot(_MQL5Indicator):
    name = 'XMA_BB_Pivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 100,  # глубина  усреднения
        'XPhase': 15,  # параметр первого усреднения,
        'BandsDeviation1': 2.0,  # девиация 1
        'BandsDeviation2': 4.0,  # девиация 2
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'SignalBar': 0,  # номер бара для получения значений индикатора
        'SignalLen': 40,  # Длина полос индикатора
    }

