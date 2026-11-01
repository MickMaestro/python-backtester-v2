"""centerofgravityosma — converted from MQL5: MQL5 Indicators/CenterOfGravityOSMA/centerofgravityosma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 15631086, 8421504, 16748574, 16776960]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'CenterOfGravityOSMA'}, 'levels': [], 'description': [], 'name': 'centerofgravityosma', 'source': 'MQL5 Indicators/CenterOfGravityOSMA/centerofgravityosma.mq5', 'folder': 'CenterOfGravityOSMA', 'inputs': [{'mql': 'Period_', 'py': 'Period_', 'param': 'Period_', 'type': 'uint', 'default': 10, 'label': 'Период усреднения индикатора', 'sinput': False}, {'mql': 'SmoothPeriod1', 'py': 'SmoothPeriod1', 'param': 'SmoothPeriod1', 'type': 'uint', 'default': 3, 'label': 'Период сглаживания сигнальной линии', 'sinput': False}, {'mql': 'MA_Method_1', 'py': 'MA_Method_1', 'param': 'MA_Method_1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'SmoothPeriod2', 'py': 'SmoothPeriod2', 'param': 'SmoothPeriod2', 'type': 'uint', 'default': 3, 'label': 'Период сглаживания сигнальной линии', 'sinput': False}, {'mql': 'MA_Method_2', 'py': 'MA_Method_2', 'param': 'MA_Method_2', 'type': 'int', 'default': 0, 'label': 'Метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
Period_ = _input('Period_', 10)  # Период усреднения индикатора
SmoothPeriod1 = _input('SmoothPeriod1', 3)  # Период сглаживания сигнальной линии
MA_Method_1 = _input('MA_Method_1', MODE_SMA)  # Метод усреднения сигнальной линии
SmoothPeriod2 = _input('SmoothPeriod2', 3)  # Период сглаживания сигнальной линии
MA_Method_2 = _input('MA_Method_2', MODE_SMA)  # Метод усреднения сигнальной линии
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Ценовая константа
ExtBuffer = Arr(0, 0.0)
ColorExtBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(Period_ + 1 + SmoothPeriod1 + SmoothPeriod2 + 2)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, ColorExtBuffer, INDICATOR_COLOR_INDEX)
    shortname = Box("")
    StringConcatenate(shortname, 'Center of Gravity OSMA(', Period_, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_startbar1, _s_OnCalculate_startbar2
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    sma = 0.0
    lwma = 0.0
    res1 = 0.0
    res2 = 0.0
    res3 = 0.0
    diff = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_startbar1 = _int(Period_ + 1)
        _s_OnCalculate_startbar2 = _s_OnCalculate_startbar1 + _int(SmoothPeriod1)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(AppliedPrice, bar, open, low, high, close)
        sma = _s_OnCalculate_MA.MASeries(0, prev_calculated, rates_total, Period_, MODE_SMA, price, bar, False)
        lwma = _s_OnCalculate_LWMA.MASeries(0, prev_calculated, rates_total, Period_, MODE_LWMA, price, bar, False)
        res1 = _fdiv(sma * lwma, Point())
        res2 = _s_OnCalculate_SIGN.MASeries(_s_OnCalculate_startbar1, prev_calculated, rates_total, SmoothPeriod1, MA_Method_1, res1, bar, False)
        res3 = res1 - res2
        ExtBuffer[bar] = _s_OnCalculate_SMOOTH.MASeries(_s_OnCalculate_startbar2, prev_calculated, rates_total, SmoothPeriod2, MA_Method_2, res3, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        diff = ExtBuffer[bar] - ExtBuffer[bar - 1]
        if ExtBuffer[bar] > 0:
            if diff > 0:
                clr = 4
            if diff < 0:
                clr = 3
        if ExtBuffer[bar] < 0:
            if diff < 0:
                clr = 0
            if diff > 0:
                clr = 1
        ColorExtBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_startbar1 = 0
_s_OnCalculate_startbar2 = 0
_s_OnCalculate_MA = CMoving_Average()
_s_OnCalculate_LWMA = CMoving_Average()
_s_OnCalculate_SIGN = CMoving_Average()
_s_OnCalculate_SMOOTH = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Centerofgravityosma(_MQL5Indicator):
    name = 'centerofgravityosma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_': 10,  # Период усреднения индикатора
        'SmoothPeriod1': 3,  # Период сглаживания сигнальной линии
        'MA_Method_1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Метод усреднения сигнальной линии
        'SmoothPeriod2': 3,  # Период сглаживания сигнальной линии
        'MA_Method_2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Метод усреднения сигнальной линии
        'AppliedPrice': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
    }

