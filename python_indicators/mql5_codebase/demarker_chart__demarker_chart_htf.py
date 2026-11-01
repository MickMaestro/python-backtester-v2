"""demarker_chart — converted from MQL5: MQL5 Indicators/DeMarker_Chart_HTF/demarker_chart.mq5

Индикатор DeMarker на ценовом графике
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16443110], 2: [11823615], 3: [14822282]}, 'widths': {2: 2, 3: 2}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'DeMarker Cloud', 2: 'XMA', 3: 'DeMarker'}, 'levels': [], 'description': ['Индикатор DeMarker на ценовом графике'], 'name': 'demarker_chart', 'source': 'MQL5 Indicators/DeMarker_Chart_HTF/demarker_chart.mq5', 'folder': 'DeMarker_Chart_HTF', 'inputs': [{'mql': 'PeriodDeMarker', 'py': 'PeriodDeMarker', 'param': 'PeriodDeMarker', 'type': 'uint', 'default': 14, 'label': 'Период индикатора DeMarker', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 2, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'Глубина  усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Dev', 'py': 'Dev', 'param': 'Dev', 'type': 'double', 'default': 10.0, 'label': 'Девиация ширины канала', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены или handle', 'sinput': False}, {'mql': 'Level_DeMarker_UP', 'py': 'Level_DeMarker_UP', 'param': 'Level_DeMarker_UP', 'type': 'int', 'default': 70, 'label': 'Уровень перекупленности', 'sinput': False}, {'mql': 'Level_DeMarker_DN', 'py': 'Level_DeMarker_DN', 'param': 'Level_DeMarker_DN', 'type': 'int', 'default': 30, 'label': 'Уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PeriodDeMarker = _input('PeriodDeMarker', 14)  # Период индикатора DeMarker
XMA_Method = _input('XMA_Method', MODE_SMMA)  # Метод усреднения
XLength = _input('XLength', 12)  # Глубина  усреднения
XPhase = _input('XPhase', 15)  # Параметр сглаживания
Dev = _input('Dev', 10.0)  # Девиация ширины канала
Applied_price = _input('Applied_price', PRICE_CLOSE)  # Тип цены или handle
Level_DeMarker_UP = _input('Level_DeMarker_UP', 70)  # Уровень перекупленности
Level_DeMarker_DN = _input('Level_DeMarker_DN', 30)  # Уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Line1Buffer = Arr(0, 0.0)
Line2Buffer = Arr(0, 0.0)
Line3Buffer = Arr(0, 0.0)
Line4Buffer = Arr(0, 0.0)
dLevel_DeMarker_UP = 0.0
dLevel_DeMarker_DN = 0.0
min_rates_total = 0
min_rates_1 = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, dLevel_DeMarker_DN, dLevel_DeMarker_UP, min_rates_1, min_rates_total
    min_rates_1 = _int(PeriodDeMarker)
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method, XLength, XPhase)
    dLevel_DeMarker_UP = (Level_DeMarker_UP - 50) * Point() * Dev
    dLevel_DeMarker_DN = (Level_DeMarker_DN - 50) * Point() * Dev
    Ind_Handle = iDeMarker(Symbol(), None, PeriodDeMarker)
    if Ind_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора DeMarker')
        return INIT_FAILED
    SetIndexBuffer(0, Line1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Line2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(2, Line3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(3, Line4Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line1Buffer, True)
    ArraySetAsSeries(Line2Buffer, True)
    ArraySetAsSeries(Line3Buffer, True)
    ArraySetAsSeries(Line4Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'F_DeMarker(', PeriodDeMarker, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    price = 0.0
    xma = 0.0
    DeMarker = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = rates_total - 1 - min_rates_1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, MAIN_LINE, 0, to_copy, DeMarker) <= 0:
        return 0
    ArraySetAsSeries(DeMarker, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        price = PriceSeries(Applied_price, bar, open, low, high, close)
        xma = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, True)
        Line3Buffer[bar] = xma
        Line4Buffer[bar] = xma + (Dev * ((100 * DeMarker[bar]) - 50) * Point())
        Line1Buffer[bar] = xma + dLevel_DeMarker_UP
        Line2Buffer[bar] = xma + dLevel_DeMarker_DN
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DemarkerChart(_MQL5Indicator):
    name = 'demarker_chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodDeMarker': 14,  # Период индикатора DeMarker
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=2),  # Метод усреднения
        'XLength': 12,  # Глубина  усреднения
        'XPhase': 15,  # Параметр сглаживания
        'Dev': 10.0,  # Девиация ширины канала
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены или handle
        'Level_DeMarker_UP': 70,  # Уровень перекупленности
        'Level_DeMarker_DN': 30,  # Уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

