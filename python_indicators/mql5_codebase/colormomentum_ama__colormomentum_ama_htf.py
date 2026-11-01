"""colormomentum_ama — converted from MQL5: MQL5 Indicators/ColorMomentum_AMA_HTF/colormomentum_ama.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [16711680, 32768], 2: [16711935, 255]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Momentum_AMA Upper', 2: 'Momentum_AMA Lower'}, 'levels': [], 'description': [], 'name': 'colormomentum_ama', 'source': 'MQL5 Indicators/ColorMomentum_AMA_HTF/colormomentum_ama.mq5', 'folder': 'ColorMomentum_AMA_HTF', 'inputs': [{'mql': 'ALength', 'py': 'ALength', 'param': 'ALength', 'type': 'uint', 'default': 8, 'label': 'Период Моментума', 'sinput': False}, {'mql': 'ama_period', 'py': 'ama_period', 'param': 'ama_period', 'type': 'uint', 'default': 9, 'label': 'Период AMA', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'uint', 'default': 2, 'label': 'Период быстрой скользящей', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'uint', 'default': 30, 'label': 'Период медленной скользящей', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'G', 'py': 'G', 'param': 'G', 'type': 'double', 'default': 2.0, 'label': 'Степень, в которую возводится сглаживающая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
ALength = _input('ALength', 8)  # Период Моментума
ama_period = _input('ama_period', 9)  # Период AMA
fast_ma_period = _input('fast_ma_period', 2)  # Период быстрой скользящей
slow_ma_period = _input('slow_ma_period', 30)  # Период медленной скользящей
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
G = _input('G', 2.0)  # Степень, в которую возводится сглаживающая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndMomentum = Arr(0, 0.0)
UpColorsBuffer = Arr(0, 0.0)
LoColorsBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(ALength + ama_period) + 2
    SetIndexBuffer(4, IndMomentum, INDICATOR_CALCULATIONS)
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, UpColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, LowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, LoColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'Momentum_AMA( ALength = ', ALength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    Mom = CMomentum()
    Mom.MALengthCheck_1('Length', ALength)
    Mom.MALengthCheck_1('ama_period', ama_period)
    Mom.MALengthCheck_1('fast_ma_period', fast_ma_period)
    Mom.MALengthCheck_1('slow_ma_period', slow_ma_period)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    momentum = 0.0
    amomentum = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        momentum = _s_OnCalculate_Mom.MomentumSeries(0, prev_calculated, rates_total, ALength, price, bar, False)
        amomentum = _s_OnCalculate_AMA.AMASeries(ALength + 1, prev_calculated, rates_total, ama_period, fast_ma_period, slow_ma_period, G, momentum, bar, False)
        amomentum = _fdiv(amomentum, Point())
        IndMomentum[bar] = amomentum
        UpperBuffer[bar] = 0.0
        UpColorsBuffer[bar] = 0.0
        LowerBuffer[bar] = 0.0
        LoColorsBuffer[bar] = 0.0
        if bar <= min_rates_total:
            continue
        if amomentum > 0:
            UpperBuffer[bar] = amomentum
            if amomentum > IndMomentum[bar - 1]:
                UpColorsBuffer[bar] = 1.0
        else:
            LowerBuffer[bar] = amomentum
            if amomentum < IndMomentum[bar - 1]:
                LoColorsBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Mom = CMomentum()
_s_OnCalculate_AMA = CAMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColormomentumAma(_MQL5Indicator):
    name = 'colormomentum_ama'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ALength': 8,  # Период Моментума
        'ama_period': 9,  # Период AMA
        'fast_ma_period': 2,  # Период быстрой скользящей
        'slow_ma_period': 30,  # Период медленной скользящей
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'G': 2.0,  # Степень, в которую возводится сглаживающая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

