"""i-ama-optimum — converted from MQL5: MQL5 Indicators/i-AMA-Optimum/i-ama-optimum.mq5

Copyright: Copyright © 2007, RickD; Link: www.e2e-fx.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, RickD', 'link': 'www.e2e-fx.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13850042]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'i-AMA-Optimum'}, 'levels': [], 'description': [], 'name': 'i-ama-optimum', 'source': 'MQL5 Indicators/i-AMA-Optimum/i-ama-optimum.mq5', 'folder': 'i-AMA-Optimum', 'inputs': [{'mql': 'P', 'py': 'P', 'param': 'P', 'type': 'uint', 'default': 1000, 'label': 'Depth of smoothing', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'double', 'default': 2.0, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'double', 'default': 10.0, 'label': 'period of slow MA', 'sinput': False}, {'mql': 'G', 'py': 'G', 'param': 'G', 'type': 'double', 'default': 2.0, 'label': 'A power the smoothing constant is raised to', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
P = _input('P', 1000)  # Depth of smoothing
fast_ma_period = _input('fast_ma_period', 2.0)  # Fast MA period
slow_ma_period = _input('slow_ma_period', 10.0)  # period of slow MA
G = _input('G', 2.0)  # A power the smoothing constant is raised to
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
IndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
SlowSC = 0.0
FastSC = 0.0
min_rates_total = 0

def OnInit():
    global FastSC, SlowSC, dPriceShift, min_rates_total
    min_rates_total = _int(P + 1)
    dPriceShift = Point() * PriceShift
    SlowSC = 2 / (1 + slow_ma_period)
    FastSC = 2 / (1 + fast_ma_period)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'i-AMA-Optimum(', P, ', ', fast_ma_period, ', ', slow_ma_period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_Noise_
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    Noise = 0.0
    Signal = 0.0
    ER = 0.0
    SSC = 0.0
    AMA = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total + begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
        _s_OnCalculate_Noise_ = 0.0
        bar = 1 + begin
        for bar in range(bar, first):
            _s_OnCalculate_Noise_ += MathAbs(price[bar] - price[bar - 1])
            IndBuffer[bar] = price[bar]
        else:
            bar = _range_end(bar, first, 1)
    else:
        first = prev_calculated - 1
    Noise = _s_OnCalculate_Noise_
    bar = first
    for bar in range(bar, rates_total):
        Signal = MathAbs(price[bar] - price[bar - P])
        Noise += MathAbs(price[bar] - price[bar - 1])
        Noise -= MathAbs(price[bar - P] - price[bar - 1 - P])
        ER = 1.0
        if Noise:
            ER = _fdiv(Signal, Noise)
        SSC = MathPow(SlowSC + (ER * (FastSC - SlowSC)), G)
        AMA = (SSC * price[bar]) + ((1 - SSC) * (IndBuffer[bar - 1] - dPriceShift))
        IndBuffer[bar] = AMA + dPriceShift
        if bar == (rates_total - 2):
            _s_OnCalculate_Noise_ = Noise
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Noise_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IAmaOptimum(_MQL5Indicator):
    name = 'i-ama-optimum'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'P': 1000,  # Depth of smoothing
        'fast_ma_period': 2.0,  # Fast MA period
        'slow_ma_period': 10.0,  # period of slow MA
        'G': 2.0,  # A power the smoothing constant is raised to
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

