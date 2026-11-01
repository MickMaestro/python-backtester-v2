"""gmma — converted from MQL5: MQL5 Indicators/GMMA_HTF/gmma.mq5

LINES_SIRNAME
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {1: [255], 2: [255], 3: [255], 4: [255], 5: [255], 6: [255], 7: [16711680], 8: [16711680], 9: [16711680], 10: [16711680], 11: [16711680], 12: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['LINES_SIRNAME'], 'name': 'gmma', 'source': 'MQL5 Indicators/GMMA_HTF/gmma.mq5', 'folder': 'GMMA_HTF', 'inputs': [{'mql': 'xMA_Method', 'py': 'xMA_Method', 'param': 'xMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'TrLength1', 'py': 'TrLength1', 'param': 'TrLength1', 'type': 'int', 'default': 3, 'label': 'Период усреднения 1 трейдерский', 'sinput': False}, {'mql': 'TrLength2', 'py': 'TrLength2', 'param': 'TrLength2', 'type': 'int', 'default': 5, 'label': 'Период усреднения 2 трейдерский', 'sinput': False}, {'mql': 'TrLength3', 'py': 'TrLength3', 'param': 'TrLength3', 'type': 'int', 'default': 8, 'label': 'Период усреднения 3 трейдерский', 'sinput': False}, {'mql': 'TrLength4', 'py': 'TrLength4', 'param': 'TrLength4', 'type': 'int', 'default': 10, 'label': 'Период усреднения 4 трейдерский', 'sinput': False}, {'mql': 'TrLength5', 'py': 'TrLength5', 'param': 'TrLength5', 'type': 'int', 'default': 12, 'label': 'Период усреднения 5 трейдерский', 'sinput': False}, {'mql': 'TrLength6', 'py': 'TrLength6', 'param': 'TrLength6', 'type': 'int', 'default': 15, 'label': 'Период усреднения 6 трейдерский', 'sinput': False}, {'mql': 'InvLength1', 'py': 'InvLength1', 'param': 'InvLength1', 'type': 'int', 'default': 30, 'label': 'Период усреднения 1 инвесторский', 'sinput': False}, {'mql': 'InvLength2', 'py': 'InvLength2', 'param': 'InvLength2', 'type': 'int', 'default': 35, 'label': 'Период усреднения 2 инвесторский', 'sinput': False}, {'mql': 'InvLength3', 'py': 'InvLength3', 'param': 'InvLength3', 'type': 'int', 'default': 40, 'label': 'Период усреднения 3 инвесторский', 'sinput': False}, {'mql': 'InvLength4', 'py': 'InvLength4', 'param': 'InvLength4', 'type': 'int', 'default': 45, 'label': 'Период усреднения 4 инвесторский', 'sinput': False}, {'mql': 'InvLength5', 'py': 'InvLength5', 'param': 'InvLength5', 'type': 'int', 'default': 50, 'label': 'Период усреднения 5 инвесторский', 'sinput': False}, {'mql': 'InvLength6', 'py': 'InvLength6', 'param': 'InvLength6', 'type': 'int', 'default': 60, 'label': 'Период усреднения 6 инвесторский', 'sinput': False}, {'mql': 'xPhase', 'py': 'xPhase', 'param': 'xPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
xMA_Method = _input('xMA_Method', MODE_EMA)  # Метод усреднения
TrLength1 = _input('TrLength1', 3)  # Период усреднения 1 трейдерский
TrLength2 = _input('TrLength2', 5)  # Период усреднения 2 трейдерский
TrLength3 = _input('TrLength3', 8)  # Период усреднения 3 трейдерский
TrLength4 = _input('TrLength4', 10)  # Период усреднения 4 трейдерский
TrLength5 = _input('TrLength5', 12)  # Период усреднения 5 трейдерский
TrLength6 = _input('TrLength6', 15)  # Период усреднения 6 трейдерский
InvLength1 = _input('InvLength1', 30)  # Период усреднения 1 инвесторский
InvLength2 = _input('InvLength2', 35)  # Период усреднения 2 инвесторский
InvLength3 = _input('InvLength3', 40)  # Период усреднения 3 инвесторский
InvLength4 = _input('InvLength4', 45)  # Период усреднения 4 инвесторский
InvLength5 = _input('InvLength5', 50)  # Период усреднения 5 инвесторский
InvLength6 = _input('InvLength6', 60)  # Период усреднения 6 инвесторский
xPhase = _input('xPhase', 100)  # Параметр сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
period = Arr(12, 0, dyn=False)
dPriceShift = 0.0
min_rates_total = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    period[0] = TrLength1
    period[1] = TrLength2
    period[2] = TrLength3
    period[3] = TrLength4
    period[4] = TrLength5
    period[5] = TrLength6
    period[6] = InvLength1
    period[7] = InvLength2
    period[8] = InvLength3
    period[9] = InvLength4
    period[10] = InvLength5
    period[11] = InvLength6
    MaxPeriod = period[ArrayMaximum(period)]
    min_rates_total = XMA[0].GetStartBars(xMA_Method, MaxPeriod, xPhase)
    for numb in range(0, 12):
        shortname = Box('')
        StringConcatenate(shortname, 'GMMA', numb, '(', period[numb], ')')
        PlotIndexSetString(numb, PLOT_LABEL, shortname.v)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb, PLOT_DRAW_BEGIN, min_rates_total)
        SetIndexBuffer(numb, Ind[numb].IndBuffer, INDICATOR_DATA)
        ArraySetAsSeries(Ind[numb].IndBuffer, True)
        PlotIndexSetInteger(numb, PLOT_DRAW_TYPE, PlotIndexGetInteger(0, PLOT_DRAW_TYPE))
        PlotIndexSetInteger(numb, PLOT_LINE_STYLE, PlotIndexGetInteger(0, PLOT_LINE_STYLE))
        PlotIndexSetInteger(numb, PLOT_LINE_WIDTH, PlotIndexGetInteger(0, PLOT_LINE_WIDTH))
    shortname = Box("")
    Smooth1 = XMA[0].GetString_MA_Method(xMA_Method)
    StringConcatenate(shortname, 'GMMA', 12, '(', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    bar = 0
    limit = 0
    maxbar = 0
    price_ = 0.0
    maxbar = rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        for numb in range(0, 12):
            Ind[numb].IndBuffer[bar] = XMA[numb].XMASeries(maxbar, prev_calculated, rates_total, xMA_Method, xPhase, period[numb], price_, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = Arr(12, 0, dyn=False, factory=CXMA)
Ind = Arr(12, 0, dyn=False, factory=CIndicatorsBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Gmma(_MQL5Indicator):
    name = 'gmma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'xMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения
        'TrLength1': 3,  # Период усреднения 1 трейдерский
        'TrLength2': 5,  # Период усреднения 2 трейдерский
        'TrLength3': 8,  # Период усреднения 3 трейдерский
        'TrLength4': 10,  # Период усреднения 4 трейдерский
        'TrLength5': 12,  # Период усреднения 5 трейдерский
        'TrLength6': 15,  # Период усреднения 6 трейдерский
        'InvLength1': 30,  # Период усреднения 1 инвесторский
        'InvLength2': 35,  # Период усреднения 2 инвесторский
        'InvLength3': 40,  # Период усреднения 3 инвесторский
        'InvLength4': 45,  # Период усреднения 4 инвесторский
        'InvLength5': 50,  # Период усреднения 5 инвесторский
        'InvLength6': 60,  # Период усреднения 6 инвесторский
        'xPhase': 100,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

