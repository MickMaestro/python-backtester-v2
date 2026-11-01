"""momcross — converted from MQL5: MQL5 Indicators/MomCross/momcross.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7}, 'colors': {1: [65280, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'MomCross'}, 'levels': [], 'description': [], 'name': 'momcross', 'source': 'MQL5 Indicators/MomCross/momcross.mq5', 'folder': 'MomCross', 'inputs': [{'mql': 'FastLength', 'py': 'FastLength', 'param': 'FastLength', 'type': 'uint', 'default': 5, 'label': 'Fast Momentum period', 'sinput': False}, {'mql': 'SlowLength', 'py': 'SlowLength', 'param': 'SlowLength', 'type': 'uint', 'default': 14, 'label': 'Slow Momentum period', 'sinput': False}, {'mql': 'SmoothLength', 'py': 'SmoothLength', 'param': 'SmoothLength', 'type': 'uint', 'default': 3, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
FastLength = _input('FastLength', 5)  # Fast Momentum period
SlowLength = _input('SlowLength', 14)  # Slow Momentum period
SmoothLength = _input('SmoothLength', 3)  # Smoothing period
IPC = _input('IPC', PRICE_CLOSE)  # Applied price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_ = 0
min_rates_total = 0

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = _int(MathMax(FastLength, SlowLength)) + 1
    min_rates_total = min_rates_ + 30
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'MomCross( ', FastLength, ', ', SlowLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    fmom = 0.0
    smom = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        fmom = _fdiv(_s_OnCalculate_FMom.MomentumSeries(0, prev_calculated, rates_total, FastLength, price, bar, False), Point())
        smom = _fdiv(_s_OnCalculate_SMom.MomentumSeries(0, prev_calculated, rates_total, SlowLength, price, bar, False), Point())
        UpBuffer[bar] = _s_OnCalculate_FJMA.JJMASeries(min_rates_, prev_calculated, rates_total, 0, 100.0, SmoothLength, fmom, bar, False)
        DnBuffer[bar] = _s_OnCalculate_SJMA.JJMASeries(min_rates_, prev_calculated, rates_total, 0, 100.0, SmoothLength, smom, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_FMom = CMomentum()
_s_OnCalculate_SMom = CMomentum()
_s_OnCalculate_FJMA = CJJMA()
_s_OnCalculate_SJMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Momcross(_MQL5Indicator):
    name = 'momcross'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastLength': 5,  # Fast Momentum period
        'SlowLength': 14,  # Slow Momentum period
        'SmoothLength': 3,  # Smoothing period
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Applied price
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

