"""OsHMA — converted from MQL5: MQL5 Indicators/OsHMA_HTF/OsHMA.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 16711680, 16748574, 36095, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'OsHMA'}, 'levels': [], 'description': [], 'name': 'OsHMA', 'source': 'MQL5 Indicators/OsHMA_HTF/OsHMA.mq5', 'folder': 'OsHMA_HTF', 'inputs': [{'mql': 'FastHMA', 'py': 'FastHMA', 'param': 'FastHMA', 'type': 'int', 'default': 13, 'label': 'Период быстрой HMA', 'sinput': False}, {'mql': 'SlowHMA', 'py': 'SlowHMA', 'param': 'SlowHMA', 'type': 'int', 'default': 26, 'label': 'Период медленной HMA', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
FastHMA = _input('FastHMA', 13)  # Период быстрой HMA
SlowHMA = _input('SlowHMA', 26)  # Период медленной HMA
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
fHma2_Period = 0
fSqrt_Period = 0
sHma2_Period = 0
sSqrt_Period = 0

def OnInit():
    global fHma2_Period, fSqrt_Period, min_rates_total, sHma2_Period, sSqrt_Period
    fHma2_Period = _int(MathFloor(_idiv(FastHMA, 2)))
    sHma2_Period = _int(MathFloor(_idiv(SlowHMA, 2)))
    fSqrt_Period = _int(MathFloor(MathSqrt(FastHMA)))
    sSqrt_Period = _int(MathFloor(MathSqrt(SlowHMA)))
    min_rates_total = MathMax(fHma2_Period + fSqrt_Period, sHma2_Period + sSqrt_Period)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'Ind')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    short_name = 'OsHMA'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + '(' + _str(FastHMA) + ',' + _str(SlowHMA) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_fbegin, _s_OnCalculate_sbegin
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    lwma1 = 0.0
    lwma2 = 0.0
    fhma = 0.0
    shma = 0.0
    series = 0.0
    if prev_calculated == 0:
        first = begin
        minbar = min_rates_total + begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, minbar)
        bar = 0
        for bar in range(bar, minbar + 1):
            IndBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, minbar + 1, 1)
        _s_OnCalculate_fbegin = FastHMA + 1 + begin
        _s_OnCalculate_sbegin = SlowHMA + 1 + begin
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        series = price[bar]
        lwma1 = _s_OnCalculate_MA1.LWMASeries(begin, prev_calculated, rates_total, fHma2_Period, series, bar, False)
        lwma2 = _s_OnCalculate_MA2.LWMASeries(begin, prev_calculated, rates_total, FastHMA, series, bar, False)
        fhma = _s_OnCalculate_MA3.LWMASeries(_s_OnCalculate_fbegin, prev_calculated, rates_total, fSqrt_Period, (2 * lwma1) - lwma2, bar, False)
        lwma1 = _s_OnCalculate_MA4.LWMASeries(begin, prev_calculated, rates_total, sHma2_Period, series, bar, False)
        lwma2 = _s_OnCalculate_MA5.LWMASeries(begin, prev_calculated, rates_total, SlowHMA, series, bar, False)
        shma = _s_OnCalculate_MA6.LWMASeries(_s_OnCalculate_sbegin, prev_calculated, rates_total, sSqrt_Period, (2 * lwma1) - lwma2, bar, False)
        IndBuffer[bar] = fhma - shma
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        ColorIndBuffer[bar] = 0.0
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 1.0
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 2.0
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 3.0
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_fbegin = 0
_s_OnCalculate_sbegin = 0
_s_OnCalculate_MA1 = CMoving_Average()
_s_OnCalculate_MA2 = CMoving_Average()
_s_OnCalculate_MA3 = CMoving_Average()
_s_OnCalculate_MA4 = CMoving_Average()
_s_OnCalculate_MA5 = CMoving_Average()
_s_OnCalculate_MA6 = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OsHMA(_MQL5Indicator):
    name = 'OsHMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastHMA': 13,  # Период быстрой HMA
        'SlowHMA': 26,  # Период медленной HMA
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

