"""colormacd — converted from MQL5: MQL5 Indicators/ColorMACD_HTF/colormacd.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [8421504, 8421376, 13828244, 6053069, 16711935], 2: [8421504, 65280, 255]}, 'widths': {1: 2, 2: 3}, 'styles': {1: 0, 2: 4}, 'labels': {1: 'MACD', 2: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'colormacd', 'source': 'MQL5 Indicators/ColorMACD_HTF/colormacd.mq5', 'folder': 'ColorMACD_HTF', 'inputs': [{'mql': 'Fast_MA', 'py': 'Fast_MA', 'param': 'Fast_MA', 'type': 'int', 'default': 12, 'label': 'Период быстрой скользящей средней', 'sinput': False}, {'mql': 'Slow_MA', 'py': 'Slow_MA', 'param': 'Slow_MA', 'type': 'int', 'default': 26, 'label': 'Глубина SMMA сглаживания', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 1, 'label': 'Метод усреднения индикатора', 'sinput': False}, {'mql': 'Signal_MA', 'py': 'Signal_MA', 'param': 'Signal_MA', 'type': 'int', 'default': 9, 'label': 'Период сигнальной линии', 'sinput': False}, {'mql': 'Signal_Method_', 'py': 'Signal_Method_', 'param': 'Signal_Method_', 'type': 'int', 'default': 1, 'label': 'Метод усреднения индикатора', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
Fast_MA = _input('Fast_MA', 12)  # Период быстрой скользящей средней
Slow_MA = _input('Slow_MA', 26)  # Глубина SMMA сглаживания
MA_Method_ = _input('MA_Method_', MODE_EMA)  # Метод усреднения индикатора
Signal_MA = _input('Signal_MA', 9)  # Период сигнальной линии
Signal_Method_ = _input('Signal_Method_', MODE_EMA)  # Метод усреднения индикатора
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Ценовая константа
start = 0
macd_start = 0
MACDBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
ColorMACDBuffer = Arr(0, 0.0)
ColorSignBuffer = Arr(0, 0.0)

def OnInit():
    global macd_start, start
    if MA_Method_ != MODE_EMA:
        macd_start = MathMax(Fast_MA, Slow_MA)
    start = macd_start + Signal_MA + 1
    SetIndexBuffer(0, MACDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, macd_start)
    PlotIndexSetString(0, PLOT_LABEL, 'MACD')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorMACDBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, macd_start + 1)
    SetIndexBuffer(2, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(2, PLOT_LABEL, 'Signal SMA')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ColorSignBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, start + 1)
    shortname = Box("")
    StringConcatenate(shortname, 'MACD( ', Fast_MA, ', ', Slow_MA, ', ', Signal_MA, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < start:
        return 0
    first1 = 0
    first2 = 0
    first3 = 0
    bar = 0
    price = 0.0
    fast_ma = 0.0
    slow_ma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = macd_start + 1
        first3 = start + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
        first3 = first1
    bar = first1
    for bar in range(bar, rates_total):
        price = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fast_ma = _s_OnCalculate_MA1.MASeries(0, prev_calculated, rates_total, Fast_MA, MA_Method_, price, bar, False)
        slow_ma = _s_OnCalculate_MA2.MASeries(0, prev_calculated, rates_total, Slow_MA, MA_Method_, price, bar, False)
        MACDBuffer[bar] = fast_ma - slow_ma
        SignBuffer[bar] = _s_OnCalculate_MA3.MASeries(macd_start, prev_calculated, rates_total, Signal_MA, Signal_Method_, MACDBuffer[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        clr = 0
        if MACDBuffer[bar] > 0:
            if MACDBuffer[bar] > MACDBuffer[bar - 1]:
                clr = 1
            if MACDBuffer[bar] < MACDBuffer[bar - 1]:
                clr = 2
        if MACDBuffer[bar] < 0:
            if MACDBuffer[bar] < MACDBuffer[bar - 1]:
                clr = 3
            if MACDBuffer[bar] > MACDBuffer[bar - 1]:
                clr = 4
        ColorMACDBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        clr = 0
        if MACDBuffer[bar] > SignBuffer[bar - 1]:
            clr = 1
        if MACDBuffer[bar] < SignBuffer[bar - 1]:
            clr = 2
        ColorSignBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_MA1 = CMoving_Average()
_s_OnCalculate_MA2 = CMoving_Average()
_s_OnCalculate_MA3 = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colormacd(_MQL5Indicator):
    name = 'colormacd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast_MA': 12,  # Период быстрой скользящей средней
        'Slow_MA': 26,  # Глубина SMMA сглаживания
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Метод усреднения индикатора
        'Signal_MA': 9,  # Период сигнальной линии
        'Signal_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Метод усреднения индикатора
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
    }

