"""ama_slope — converted from MQL5: MQL5 Indicators/AMA_SLOPE_HTF/ama_slope.mq5

Copyright: Copyright © 2007, Kalenzo; Link: bartlomiej.gorski@gmail.combartlomiej.gorski@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Kalenzo', 'link': 'bartlomiej.gorski@gmail.combartlomiej.gorski@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'AMA_SLOPE'}, 'levels': [], 'description': [], 'name': 'ama_slope', 'source': 'MQL5 Indicators/AMA_SLOPE_HTF/ama_slope.mq5', 'folder': 'AMA_SLOPE_HTF', 'inputs': [{'mql': 'ama_period', 'py': 'ama_period', 'param': 'ama_period', 'type': 'uint', 'default': 9, 'label': 'Период AMA', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'uint', 'default': 2, 'label': 'Период быстрой скользящей', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'uint', 'default': 30, 'label': 'Период медленной скользящей', 'sinput': False}, {'mql': 'G', 'py': 'G', 'param': 'G', 'type': 'double', 'default': 2.0, 'label': 'Степень, в которую возводится сглаживающая константа', 'sinput': False}, {'mql': 'AMAShift', 'py': 'AMAShift', 'param': 'AMAShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'dK', 'py': 'dK', 'param': 'dK', 'type': 'double', 'default': 1.0, 'label': 'Коэффициент для фильтра', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ama_period = _input('ama_period', 9)  # Период AMA
fast_ma_period = _input('fast_ma_period', 2)  # Период быстрой скользящей
slow_ma_period = _input('slow_ma_period', 30)  # Период медленной скользящей
G = _input('G', 2.0)  # Степень, в которую возводится сглаживающая константа
AMAShift = _input('AMAShift', 0)  # Сдвиг индикатора по горизонтали в барах
dK = _input('dK', 1.0)  # Коэффициент для фильтра
AMABuffer = Arr(0, 0.0)
dSC = 0.0
slowSC = 0.0
fastSC = 0.0
AMA_Handle = 0
dAMA_Handle = 0
min_rates_total = 0

def OnInit():
    global dSC, fastSC, min_rates_total, slowSC
    min_rates_total = _int(ama_period + 1)
    SetIndexBuffer(0, AMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, AMAShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'AMA_SLOPE( ', ama_period, ', ', fast_ma_period, ', ', slow_ma_period, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    slowSC = 2.0 / (slow_ma_period + 1)
    fastSC = 2.0 / (fast_ma_period + 1)
    dSC = fastSC - slowSC

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_AMA_
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    noise = 0.0
    AMA = 0.0
    signal = 0.0
    ER = 0.0
    ERSC = 0.0
    SSC = 0.0
    price0 = 0.0
    price1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total + begin + 1
        _s_OnCalculate_AMA_ = price[first - 1]
        AMA = _s_OnCalculate_AMA_
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        first = prev_calculated - 1
        AMA = _s_OnCalculate_AMA_
    bar = first
    for bar in range(bar, rates_total):
        noise = Point() / 10000
        for iii in range(0, _int(ama_period)):
            price0 = price[bar - iii - 0]
            price1 = price[bar - iii - 1]
            noise += MathAbs(price0 - price1)
        price0 = price[bar]
        price1 = price[bar - ama_period]
        signal = MathAbs(price0 - price1)
        ER = _fdiv(signal, noise)
        ERSC = ER * dSC
        SSC = ERSC + slowSC
        AMA = AMA + (MathPow(SSC, G) * (price0 - AMA))
        AMABuffer[bar] = _fdiv(AMA - _s_OnCalculate_AMA_, Point())
        if bar < (rates_total - 1):
            _s_OnCalculate_AMA_ = AMA
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_AMA_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AmaSlope(_MQL5Indicator):
    name = 'ama_slope'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ama_period': 9,  # Период AMA
        'fast_ma_period': 2,  # Период быстрой скользящей
        'slow_ma_period': 30,  # Период медленной скользящей
        'G': 2.0,  # Степень, в которую возводится сглаживающая константа
        'AMAShift': 0,  # Сдвиг индикатора по горизонтали в барах
        'dK': 1.0,  # Коэффициент для фильтра
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

