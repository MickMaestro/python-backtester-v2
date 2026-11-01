"""rainbow_hma — converted from MQL5: MQL5 Indicators/Rainbow_HMA/rainbow_hma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {1: [4163021], 2: [4163021], 3: [4163021], 4: [4163021], 5: [4163021], 6: [4163021], 7: [4163021], 8: [4163021], 9: [4163021], 10: [4163021], 11: [16711680], 12: [16711680], 13: [16711680], 14: [16711680], 15: [16711680], 16: [16711680], 17: [16711680], 18: [16711680], 19: [16711680], 20: [16711680], 21: [16711680], 22: [16776960], 23: [16776960], 24: [16776960], 25: [16776960], 26: [16776960], 27: [16776960], 28: [16776960], 29: [16776960], 30: [16776960], 31: [16776960], 32: [16776960], 33: [16776960], 34: [9639167], 35: [9639167], 36: [9639167], 37: [9639167], 38: [9639167], 39: [9639167], 40: [9639167], 41: [9639167], 42: [9639167], 43: [9639167], 44: [9639167], 45: [9639167], 46: [9639167], 47: [8388736], 48: [8388736], 49: [8388736], 50: [8388736], 51: [8388736], 52: [8388736], 53: [8388736], 54: [8388736], 55: [8388736], 56: [8388736], 57: [8388736], 58: [8388736], 59: [8388736], 60: [8388736]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'rainbow_hma', 'source': 'MQL5 Indicators/Rainbow_HMA/rainbow_hma.mq5', 'folder': 'Rainbow_HMA', 'inputs': [{'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'uint', 'default': 2, 'label': 'Первая глубина усреднения', 'sinput': False}, {'mql': 'StartStep', 'py': 'StartStep', 'param': 'StartStep', 'type': 'uint', 'default': 2, 'label': 'Стартовый шаг изменения усреднения', 'sinput': False}, {'mql': 'EndStep', 'py': 'EndStep', 'param': 'EndStep', 'type': 'uint', 'default': 6, 'label': 'Финишный шаг изменения усреднения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 9, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
StartLength = _input('StartLength', 2)  # Первая глубина усреднения
StartStep = _input('StartStep', 2)  # Стартовый шаг изменения усреднения
EndStep = _input('EndStep', 6)  # Финишный шаг изменения усреднения
IPC = _input('IPC', PRICE_QUARTER_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
dPriceShift = 0.0
min_rates_total = 0
hma_period = Arr(60, 0, dyn=False)
hma2_period = Arr(60, 0, dyn=False)
sqrt_period = Arr(60, 0, dyn=False)

class CIndBuffers(MqlObject):
    _q_fields = ('m_LineBuffer',)
    def __init__(self, *args):
        self.m_LineBuffer = Arr(0, 0.0)

def OnInit():
    global dPriceShift, min_rates_total
    ratio = _idiv(EndStep - StartStep, 60 - 1)
    hma_period[0] = _int(StartLength)
    for count in range(1, 60):
        hma_period[count] += hma_period[count - 1] + _int(StartStep + (count * ratio))
    for count in range(0, 60):
        hma2_period[count] = _int(MathFloor(_idiv(hma_period[count], 2)))
    for count in range(0, 60):
        sqrt_period[count] = _int(MathFloor(MathSqrt(hma_period[count])))
    min_rates_total = hma_period[60 - 1] + sqrt_period[60 - 1]
    dPriceShift = Point() * PriceShift
    for count in range(0, 60):
        SetIndexBuffer(count, Ind[count].m_LineBuffer, INDICATOR_DATA)
    for count in range(0, 60):
        PlotIndexSetInteger(count, PLOT_DRAW_TYPE, DRAW_LINE)
    for count in range(0, 60):
        PlotIndexSetInteger(count, PLOT_SHIFT, Shift)
    for count in range(0, 60):
        PlotIndexSetInteger(count, PLOT_DRAW_BEGIN, hma_period[count] + sqrt_period[count])
    for count in range(0, 60):
        PlotIndexSetDouble(count, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    for count in range(0, 60):
        PlotIndexSetString(count, PLOT_LABEL, 'Line ' + _str(count + 1))
    shortname = Box("")
    StringConcatenate(shortname, 'Rainbow_HMA(', StartLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    lwma1 = 0.0
    lwma2 = 0.0
    dma = 0.0
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
            lwma1 = MA[0][count].LWMASeries(0, prev_calculated, rates_total, hma2_period[count], price, bar, False)
            lwma2 = MA[1][count].LWMASeries(0, prev_calculated, rates_total, hma_period[count], price, bar, False)
            dma = (2 * lwma1) - lwma2
            Ind[count].m_LineBuffer[bar] = MA[2][count].LWMASeries(hma_period[count], prev_calculated, rates_total, sqrt_period[count], dma, bar, False) + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
MA = Arr(3, 0, dyn=False, factory=CMoving_Average, dims=(60,))
Ind = Arr(60, 0, dyn=False, factory=CIndBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RainbowHma(_MQL5Indicator):
    name = 'rainbow_hma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartLength': 2,  # Первая глубина усреднения
        'StartStep': 2,  # Стартовый шаг изменения усреднения
        'EndStep': 6,  # Финишный шаг изменения усреднения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=9),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

