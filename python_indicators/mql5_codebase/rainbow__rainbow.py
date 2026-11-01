"""rainbow — converted from MQL5: MQL5 Indicators/Rainbow/rainbow.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {1: [55295], 2: [55295], 3: [55295], 4: [55295], 5: [55295], 6: [55295], 7: [55295], 8: [55295], 9: [55295], 10: [55295], 11: [16748574], 12: [16748574], 13: [16748574], 14: [16748574], 15: [16748574], 16: [16748574], 17: [16748574], 18: [16748574], 19: [16748574], 20: [16748574], 21: [16748574], 22: [3329330], 23: [3329330], 24: [3329330], 25: [3329330], 26: [3329330], 27: [3329330], 28: [3329330], 29: [3329330], 30: [3329330], 31: [3329330], 32: [3329330], 33: [3329330], 34: [255], 35: [255], 36: [255], 37: [255], 38: [255], 39: [255], 40: [255], 41: [255], 42: [255], 43: [255], 44: [255], 45: [255], 46: [255], 47: [13382297], 48: [13382297], 49: [13382297], 50: [13382297], 51: [13382297], 52: [13382297], 53: [13382297], 54: [13382297], 55: [13382297], 56: [13382297], 57: [13382297], 58: [13382297], 59: [13382297], 60: [13382297]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'rainbow', 'source': 'MQL5 Indicators/Rainbow/rainbow.mq5', 'folder': 'Rainbow', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'uint', 'default': 2, 'label': 'Первая глубина усреднения', 'sinput': False}, {'mql': 'StartStep', 'py': 'StartStep', 'param': 'StartStep', 'type': 'uint', 'default': 2, 'label': 'Стартовый шаг изменения усреднения', 'sinput': False}, {'mql': 'EndStep', 'py': 'EndStep', 'param': 'EndStep', 'type': 'uint', 'default': 6, 'label': 'Финишный шаг изменения усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 9, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_EMA)  # Метод усреднения
StartLength = _input('StartLength', 2)  # Первая глубина усреднения
StartStep = _input('StartStep', 2)  # Стартовый шаг изменения усреднения
EndStep = _input('EndStep', 6)  # Финишный шаг изменения усреднения
XPhase = _input('XPhase', 15)  # Параметр усреднения
IPC = _input('IPC', PRICE_QUARTER_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
dPriceShift = 0.0
min_rates_total = 0
period = Arr(60, 0, dyn=False)

class CIndBuffers(MqlObject):
    _q_fields = ('m_LineBuffer',)
    def __init__(self, *args):
        self.m_LineBuffer = Arr(0, 0.0)

def OnInit():
    global dPriceShift, min_rates_total
    ratio = _idiv(EndStep - StartStep, 60 - 1)
    period[0] = _int(StartLength)
    for count in range(1, 60):
        period[count] = period[count - 1] + _int(StartStep + (count * ratio))
    min_rates_total = XMA1[0].GetStartBars(XMA_Method, period[60 - 1], XPhase)
    dPriceShift = Point() * PriceShift
    for count in range(0, 60):
        SetIndexBuffer(count, Ind[count].m_LineBuffer, INDICATOR_DATA)
    for count in range(0, 60):
        PlotIndexSetInteger(count, PLOT_DRAW_TYPE, DRAW_LINE)
    for count in range(0, 60):
        PlotIndexSetInteger(count, PLOT_SHIFT, Shift)
    for count in range(0, 60):
        PlotIndexSetInteger(count, PLOT_DRAW_BEGIN, min_rates_total)
    for count in range(0, 60):
        PlotIndexSetDouble(count, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    for count in range(0, 60):
        PlotIndexSetString(count, PLOT_LABEL, 'Line ' + _str(count + 1))
    shortname = Box("")
    Smooth1 = XMA1[0].GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'Rainbow(', StartLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        for count in range(0, 60):
            Ind[count].m_LineBuffer[bar] = XMA1[count].XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, period[count], price, bar, False) + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = Arr(60, 0, dyn=False, factory=CXMA)
Ind = Arr(60, 0, dyn=False, factory=CIndBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rainbow(_MQL5Indicator):
    name = 'rainbow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения
        'StartLength': 2,  # Первая глубина усреднения
        'StartStep': 2,  # Стартовый шаг изменения усреднения
        'EndStep': 6,  # Финишный шаг изменения усреднения
        'XPhase': 15,  # Параметр усреднения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=9),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

