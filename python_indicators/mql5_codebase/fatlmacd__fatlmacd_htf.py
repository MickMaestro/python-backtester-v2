"""fatlmacd — converted from MQL5: MQL5 Indicators/FatlMacd_HTF/fatlmacd.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [16711935, 9639167, 8421504, 16748574, 2330219]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'FatlMacd'}, 'levels': [0.0], 'description': [], 'name': 'fatlmacd', 'source': 'MQL5 Indicators/FatlMacd_HTF/fatlmacd.mq5', 'folder': 'FatlMacd_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'Метод усреднения гистограммы', 'sinput': False}, {'mql': 'XMA_Lengh', 'py': 'XMA_Lengh', 'param': 'XMA_Lengh', 'type': 'int', 'default': 20, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'XMA_Phase', 'py': 'XMA_Phase', 'param': 'XMA_Phase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения скользящих средний', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_T3)  # Метод усреднения гистограммы
XMA_Lengh = _input('XMA_Lengh', 20)  # Период усреднения
XMA_Phase = _input('XMA_Phase', 100)  # Параметр усреднения скользящих средний
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Ценовая константа
min_rates_total = 0
min_rates_1 = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = 39
    min_rates_total = min_rates_1 + XMA1.GetStartBars(XMA_Method, XMA_Lengh, XMA_Phase)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    XMA1.XMALengthCheck('Fast_XMA', XMA_Phase)
    XMA1.XMAPhaseCheck('Phase', XMA_Phase, XMA_Method)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FatlMacd')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    fatl = 0.0
    macd = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fatl = FATL1.FATLSeries(0, prev_calculated, rates_total, price, bar, False)
        macd = price - fatl
        IndBuffer[bar] = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XMA_Phase, XMA_Lengh, macd, bar, False)
        IndBuffer[bar] = _fdiv(IndBuffer[bar], Point())
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
FATL1 = _alloc(CFATL)
FATL1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fatlmacd(_MQL5Indicator):
    name = 'fatlmacd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения гистограммы
        'XMA_Lengh': 20,  # Период усреднения
        'XMA_Phase': 100,  # Параметр усреднения скользящих средний
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
    }

