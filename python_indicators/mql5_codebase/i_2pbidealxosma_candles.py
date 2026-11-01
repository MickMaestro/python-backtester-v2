"""2pbidealxosma_candles — converted from MQL5: MQL5 Indicators/2pbIdealXOSMA_Candles/2pbidealxosma_candles.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [255, 42495, 8388736, 15631086, 16711680, 16760576, 8421376, 65280]}, 'widths': {}, 'styles': {}, 'labels': {1: '2pbIdealXOSMA Open'}, 'levels': [], 'description': [], 'name': '2pbidealxosma_candles', 'source': 'MQL5 Indicators/2pbIdealXOSMA_Candles/2pbidealxosma_candles.mq5', 'folder': '2pbIdealXOSMA_Candles', 'inputs': [{'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'int', 'default': 10, 'label': 'rough smoothing', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'int', 'default': 10, 'label': 'adjusting smoothing', 'sinput': False}, {'mql': 'PeriodX1', 'py': 'PeriodX1', 'param': 'PeriodX1', 'type': 'int', 'default': 10, 'label': 'first rough smoothing', 'sinput': False}, {'mql': 'PeriodX2', 'py': 'PeriodX2', 'param': 'PeriodX2', 'type': 'int', 'default': 10, 'label': 'first adjusting smoothing', 'sinput': False}, {'mql': 'PeriodY1', 'py': 'PeriodY1', 'param': 'PeriodY1', 'type': 'int', 'default': 10, 'label': 'second rough smoothing', 'sinput': False}, {'mql': 'PeriodY2', 'py': 'PeriodY2', 'param': 'PeriodY2', 'type': 'int', 'default': 10, 'label': 'second adjusting smoothing', 'sinput': False}, {'mql': 'PeriodZ1', 'py': 'PeriodZ1', 'param': 'PeriodZ1', 'type': 'int', 'default': 10, 'label': 'third rough smoothing', 'sinput': False}, {'mql': 'PeriodZ2', 'py': 'PeriodZ2', 'param': 'PeriodZ2', 'type': 'int', 'default': 10, 'label': 'third adjusting smoothing', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'smoothing method', 'sinput': False}, {'mql': 'Smooth_XMA', 'py': 'Smooth_XMA', 'param': 'Smooth_XMA', 'type': 'int', 'default': 9, 'label': 'smoothing period', 'sinput': False}, {'mql': 'Smooth_Phase', 'py': 'Smooth_Phase', 'param': 'Smooth_Phase', 'type': 'int', 'default': 100, 'label': 'moving averages smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Period1 = _input('Period1', 10)  # rough smoothing
Period2 = _input('Period2', 10)  # adjusting smoothing
PeriodX1 = _input('PeriodX1', 10)  # first rough smoothing
PeriodX2 = _input('PeriodX2', 10)  # first adjusting smoothing
PeriodY1 = _input('PeriodY1', 10)  # second rough smoothing
PeriodY2 = _input('PeriodY2', 10)  # second adjusting smoothing
PeriodZ1 = _input('PeriodZ1', 10)  # third rough smoothing
PeriodZ2 = _input('PeriodZ2', 10)  # third adjusting smoothing
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # smoothing method
Smooth_XMA = _input('Smooth_XMA', 9)  # smoothing period
Smooth_Phase = _input('Smooth_Phase', 100)  # moving averages smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE)  # price constant
min_rates_total = 0
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
OsmaBuffer = Arr(0, 0.0)
w1 = 0.0
w2 = 0.0
wX1 = 0.0
wX2 = 0.0
wY1 = 0.0
wY2 = 0.0
wZ1 = 0.0
wZ2 = 0.0
Moving0_ = 0.0
Moving01_ = 0.0
Moving11_ = 0.0
Moving21_ = 0.0

def GetIdealMASmooth(W1_, W2_, Series1, Series0, Resalt1):
    Resalt0 = 0.0
    dSeries = 0.0
    dSeries2 = 0.0
    dSeries = Series0 - Series1
    dSeries2 = (dSeries * dSeries) - 1.0
    Resalt0 = _fdiv((W1_ * (Series0 - Resalt1)) + Resalt1 + (W2_ * Resalt1 * dSeries2), 1.0 + (W2_ * dSeries2))
    return Resalt0

def OnInit():
    global min_rates_total, w1, w2, wX1, wX2, wY1, wY2, wZ1, wZ2
    min_rates_total = 2 + XMA1.GetStartBars(SmoothMethod, Smooth_XMA, Smooth_Phase)
    w1 = 1.0 / Period1
    w2 = 1.0 / Period2
    wX1 = 1.0 / PeriodX1
    wX2 = 1.0 / PeriodX2
    wY1 = 1.0 / PeriodY1
    wY2 = 1.0 / PeriodY2
    wZ1 = 1.0 / PeriodZ1
    wZ2 = 1.0 / PeriodZ2
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, OsmaBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    XMA1.XMALengthCheck('Smooth_XMA', Smooth_XMA)
    XMA1.XMAPhaseCheck('Smooth_Phase', Smooth_Phase, SmoothMethod)
    IndicatorSetString(INDICATOR_SHORTNAME, '2pbIdealXOSMA Candles')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Moving01_, Moving0_, Moving11_, Moving21_
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Osma0 = 0.0
    Osma1 = 0.0
    price0 = 0.0
    price1 = 0.0
    Moving0 = 0.0
    SlowMA = 0.0
    FastMA = 0.0
    macd = 0.0
    Moving00 = 0.0
    Moving10 = 0.0
    Moving20 = 0.0
    Moving01 = 0.0
    Moving11 = 0.0
    Moving21 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        price0 = PriceSeries(IPC, 0, open, low, high, close)
        Moving0_ = price0
        Moving01_ = Moving0_
        Moving11_ = Moving0_
        Moving21_ = Moving0_
    else:
        first = prev_calculated - 1
    Moving0 = Moving0_
    Moving01 = Moving01_
    Moving11 = Moving11_
    Moving21 = Moving21_
    bar = first
    for bar in range(bar, rates_total):
        price0 = PriceSeries(IPC, bar, open, low, high, close)
        price1 = PriceSeries(IPC, bar - 1, open, low, high, close)
        Moving0 = GetIdealMASmooth(w1, w2, price1, price0, Moving0)
        Moving00 = GetIdealMASmooth(wX1, wX2, price1, price0, Moving01)
        Moving10 = GetIdealMASmooth(wY1, wY2, Moving01, Moving00, Moving11)
        Moving20 = GetIdealMASmooth(wZ1, wZ2, Moving11, Moving10, Moving21)
        Moving01 = Moving00
        Moving11 = Moving10
        Moving21 = Moving20
        SlowMA = Moving20
        FastMA = Moving0
        macd = FastMA - SlowMA
        OsmaBuffer[bar] = XMA1.XMASeries(1, prev_calculated, rates_total, SmoothMethod, Smooth_Phase, Smooth_XMA, macd, bar, False)
        if bar == (rates_total - 2):
            Moving0_ = Moving0
            Moving01_ = Moving01
            Moving11_ = Moving11
            Moving21_ = Moving21
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        ExtOpenBuffer[bar] = open[bar]
        ExtCloseBuffer[bar] = close[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        Osma0 = OsmaBuffer[bar]
        Osma1 = OsmaBuffer[bar - 1]
        if Osma0 >= 0:
            if Osma1 > Osma0:
                if close[bar] >= open[bar]:
                    ExtColorBuffer[bar] = 5.0
                else:
                    ExtColorBuffer[bar] = 4.0
            if Osma1 <= Osma0:
                if close[bar] >= open[bar]:
                    ExtColorBuffer[bar] = 7.0
                else:
                    ExtColorBuffer[bar] = 6.0
        if Osma0 < 0:
            if Osma1 <= Osma0:
                if close[bar] >= open[bar]:
                    ExtColorBuffer[bar] = 3.0
                else:
                    ExtColorBuffer[bar] = 2.0
            if Osma1 > Osma0:
                if close[bar] >= open[bar]:
                    ExtColorBuffer[bar] = 1.0
                else:
                    ExtColorBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2pbidealxosmaCandles(_MQL5Indicator):
    name = '2pbidealxosma_candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period1': 10,  # rough smoothing
        'Period2': 10,  # adjusting smoothing
        'PeriodX1': 10,  # first rough smoothing
        'PeriodX2': 10,  # first adjusting smoothing
        'PeriodY1': 10,  # second rough smoothing
        'PeriodY2': 10,  # second adjusting smoothing
        'PeriodZ1': 10,  # third rough smoothing
        'PeriodZ2': 10,  # third adjusting smoothing
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # smoothing method
        'Smooth_XMA': 9,  # smoothing period
        'Smooth_Phase': 100,  # moving averages smoothing parameter,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
    }

