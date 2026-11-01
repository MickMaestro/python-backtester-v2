"""WPR_Chart — converted from MQL5: MQL5 Indicators/WPR_Chart_HTF/WPR_Chart.mq5

Индикатор WPR на ценовом графике
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16443110], 2: [11823615], 3: [14822282]}, 'widths': {2: 2, 3: 2}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'WPR Cloud', 2: 'XMA', 3: 'WPR'}, 'levels': [], 'description': ['Индикатор WPR на ценовом графике'], 'name': 'WPR_Chart', 'source': 'MQL5 Indicators/WPR_Chart_HTF/WPR_Chart.mq5', 'folder': 'WPR_Chart_HTF', 'inputs': [{'mql': 'PeriodWPR', 'py': 'PeriodWPR', 'param': 'PeriodWPR', 'type': 'uint', 'default': 14, 'label': 'Период индикатора WPR', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 2, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'глубина  усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Dev', 'py': 'Dev', 'param': 'Dev', 'type': 'double', 'default': 10.0, 'label': 'Девиация ширины канала', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'тип цены или handle', 'sinput': False}, {'mql': 'Level_WPR_UP', 'py': 'Level_WPR_UP', 'param': 'Level_WPR_UP', 'type': 'int', 'default': -40, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'Level_WPR_DN', 'py': 'Level_WPR_DN', 'param': 'Level_WPR_DN', 'type': 'int', 'default': -60, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PeriodWPR = _input('PeriodWPR', 14)  # Период индикатора WPR
XMA_Method = _input('XMA_Method', MODE_SMMA_)  # метод усреднения
XLength = _input('XLength', 12)  # глубина  усреднения
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Dev = _input('Dev', 10.0)  # Девиация ширины канала
Applied_price = _input('Applied_price', PRICE_CLOSE_)  # тип цены или handle
Level_WPR_UP = _input('Level_WPR_UP', -40)  # уровень перекупленности
Level_WPR_DN = _input('Level_WPR_DN', -60)  # уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Line1Buffer = Arr(0, 0.0)
Line2Buffer = Arr(0, 0.0)
Line3Buffer = Arr(0, 0.0)
Line4Buffer = Arr(0, 0.0)
dLevel_WPR_UP = 0.0
dLevel_WPR_DN = 0.0
min_rates_total = 0
min_rates_1 = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, dLevel_WPR_DN, dLevel_WPR_UP, min_rates_1, min_rates_total
    min_rates_1 = _int(PeriodWPR)
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method, XLength, XPhase)
    dLevel_WPR_UP = (Level_WPR_UP + 50) * Point() * Dev
    dLevel_WPR_DN = (Level_WPR_DN + 50) * Point() * Dev
    Ind_Handle = iWPR(Symbol(), None, PeriodWPR)
    if Ind_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора WPR')
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
    StringConcatenate(shortname, 'F_WPR(', PeriodWPR, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    price = 0.0
    xma = 0.0
    WPR = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = rates_total - 1 - min_rates_1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, MAIN_LINE, 0, to_copy, WPR) <= 0:
        return 0
    ArraySetAsSeries(WPR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        price = PriceSeries(Applied_price, bar, open, low, high, close)
        xma = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, True)
        Line3Buffer[bar] = xma
        Line4Buffer[bar] = xma + (Dev * (WPR[bar] + 50) * Point())
        Line1Buffer[bar] = xma + dLevel_WPR_UP
        Line2Buffer[bar] = xma + dLevel_WPR_DN
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WPRChart(_MQL5Indicator):
    name = 'WPR_Chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodWPR': 14,  # Период индикатора WPR
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=2),  # метод усреднения
        'XLength': 12,  # глубина  усреднения
        'XPhase': 15,  # параметр сглаживания,
        'Dev': 10.0,  # Девиация ширины канала
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # тип цены или handle
        'Level_WPR_UP': -40,  # уровень перекупленности
        'Level_WPR_DN': -60,  # уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

