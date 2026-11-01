"""Yaanna — converted from MQL5: MQL5 Indicators/Yaanna_HTF/Yaanna.mq5

Copyright: 2010,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh
from backtester.mql5.lib.indicatorsalgorithms import *  # #include indicatorsalgorithms.mqh

MQL5_META = {'props': {'copyright': '2010,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13382297]}, 'widths': {1: 1}, 'styles': {1: 4}, 'labels': {1: 'Yaanna'}, 'levels': [100.0, 0.0], 'description': [], 'name': 'Yaanna', 'source': 'MQL5 Indicators/Yaanna_HTF/Yaanna.mq5', 'folder': 'Yaanna_HTF', 'inputs': [{'mql': 'BandsPeriod', 'py': 'BandsPeriod', 'param': 'BandsPeriod', 'type': 'int', 'default': 200, 'label': 'период усреднения', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 2.0, 'label': 'девиация', 'sinput': False}, {'mql': 'Ma_Method', 'py': 'Ma_Method', 'param': 'Ma_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh', 'indicatorsalgorithms.mqh']}

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
BandsPeriod = _input('BandsPeriod', 200)  # период усреднения
BandsDeviation = _input('BandsDeviation', 2.0)  # девиация
Ma_Method = _input('Ma_Method', MODE_SMA)  # метод усреднения
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Buffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, BandsPeriod - 1)
    PlotIndexSetString(0, PLOT_LABEL, 'Yaanna')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Yaanna( BandsPeriod = ', BandsPeriod, ', BandsDeviation = ', BandsDeviation, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < BandsPeriod:
        return 0
    price_ = 0.0
    Lower = 0.0
    Middle = 0.0
    Upper = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        _s_OnCalculate_BBands.BBandsSeries(0, prev_calculated, rates_total, BandsPeriod, BandsDeviation, Ma_Method, price_, bar, False, _ValRef(Lower), _ValRef(Middle), _ValRef(Upper))
        Buffer[bar] = _fdiv(100 * (close[bar] - Lower), Upper - Lower)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_BBands = CBBands()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Yaanna(_MQL5Indicator):
    name = 'Yaanna'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BandsPeriod': 200,  # период усреднения
        'BandsDeviation': 2.0,  # девиация
        'Ma_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # метод усреднения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

