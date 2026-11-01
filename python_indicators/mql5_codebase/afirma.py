"""afirma — converted from MQL5: MQL5 Indicators/AFIRMA/afirma.mq5

Copyright: Copyright © 2006, gpwr.; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, gpwr.', 'link': '', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [14822282], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'FIRMA', 2: 'ARMA'}, 'levels': [], 'description': [], 'name': 'afirma', 'source': 'MQL5 Indicators/AFIRMA/afirma.mq5', 'folder': 'AFIRMA', 'inputs': [{'mql': 'Periods', 'py': 'Periods', 'param': 'Periods', 'type': 'int', 'default': 4, 'label': 'LF transmission width 1/(2*Periods)', 'sinput': False}, {'mql': 'Taps', 'py': 'Taps', 'param': 'Taps', 'type': 'int', 'default': 21, 'label': 'Number of delay units in the filter', 'sinput': False}, {'mql': 'Window', 'py': 'Window', 'param': 'Window', 'type': 'int', 'default': 4, 'label': 'Window index', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_WINDOWS
Rectangular = 1
Hanning1 = 2
Hanning2 = 3
Blackman = 4
Blackman_Harris = 5
_enum('ENUM_WINDOWS', {1: 'Rectangular', 2: 'Hanning1', 3: 'Hanning2', 4: 'Blackman', 5: 'Blackman_Harris'})

# ---- inputs and global variables
Periods = _input('Periods', 4)  # LF transmission width 1/(2*Periods)
Taps = _input('Taps', 21)  # Number of delay units in the filter
Window = _input('Window', Blackman)  # Window index
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
min_rates_total = 0
n = 0
w = Arr(0, 0.0)
wsum = 0.0
sx2 = 0.0
sx3 = 0.0
sx4 = 0.0
sx5 = 0.0
sx6 = 0.0
den = 0.0
FIRMABuffer = Arr(0, 0.0)
ARMABuffer = Arr(0, 0.0)

def OnInit():
    global den, min_rates_total, n, sx2, sx3, sx4, sx5, sx6, wsum
    ArrayResize(w, Taps)
    wsum = 0.0
    for k in range(0, Taps):
        _sw1 = Window
        if _sw1 == Rectangular:
            w[k] = 1.0
        elif _sw1 == Hanning1:
            w[k] = 0.5 - (0.5 * MathCos((2.0 * 3.141592653589793 * k) / Taps))
        elif _sw1 == Hanning2:
            w[k] = 0.54 - (0.46 * MathCos((2.0 * 3.141592653589793 * k) / Taps))
        elif _sw1 == Blackman:
            w[k] = 0.42 - (0.5 * MathCos((2.0 * 3.141592653589793 * k) / Taps)) + (0.08 * MathCos((4.0 * 3.141592653589793 * k) / Taps))
        elif _sw1 == Blackman_Harris:
            w[k] = 0.35875 - (0.48829 * MathCos((2.0 * 3.141592653589793 * k) / Taps)) + (0.14128 * MathCos((4.0 * 3.141592653589793 * k) / Taps)) - (0.01168 * MathCos((6.0 * 3.141592653589793 * k) / Taps))
        if k != (Taps / 2.0):
            w[k] = _fdiv((w[k] * MathSin((3.141592653589793 * (k - (Taps / 2.0))) / Periods)) / 3.141592653589793, k - (Taps / 2.0))
        wsum += w[k]
    n = _idiv(Taps - 1, 2)
    sx2 = ((2 * n) + 1) / 3.0
    sx3 = (n * (n + 1)) / 2.0
    sx4 = (sx2 * ((3 * n * n) + (3 * n) - 1)) / 5.0
    sx5 = (sx3 * ((2 * n * n) + (2 * n) - 1)) / 3.0
    sx6 = (sx2 * ((3 * n * n * n * (n + 2)) - (3 * n) + 1)) / 7.0
    den = _fdiv(sx6 * sx4, sx5) - sx5
    min_rates_total = Taps
    SetIndexBuffer(0, FIRMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(FIRMABuffer, True)
    SetIndexBuffer(1, ARMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ARMABuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'AFIRMA(', Periods, ', ', Taps, ', ', EnumToString(Window, 'ENUM_WINDOWS'), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    limit = 0
    bar = 0
    a0 = 0.0
    a1 = 0.0
    a2 = 0.0
    a3 = 0.0
    sx2y = 0.0
    sx3y = 0.0
    p = 0.0
    q = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total - begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - n - 1)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(price, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        FIRMABuffer[bar + n] = 0.0
        for k in range(0, Taps):
            FIRMABuffer[bar + n] += _fdiv(price[bar + k] * w[k], wsum)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if bar < n:
            FIRMABuffer[bar] = EMPTY_VALUE
        ARMABuffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, 0 - 1, -1)
    a0 = FIRMABuffer[n]
    a1 = FIRMABuffer[n] - FIRMABuffer[n + 1]
    sx2y = 0.0
    sx3y = 0.0
    for i in range(0, n + 1):
        sx2y += i * i * price[n - i]
        sx3y += i * i * i * price[n - i]
    sx2y = _fdiv(_fdiv(2.0 * sx2y, n), n + 1)
    sx3y = _fdiv(_fdiv(2.0 * sx3y, n), n + 1)
    p = sx2y - (a0 * sx2) - (a1 * sx3)
    q = sx3y - (a0 * sx3) - (a1 * sx4)
    a2 = _fdiv(_fdiv(p * sx6, sx5) - q, den)
    a3 = _fdiv(_fdiv(q * sx4, sx5) - p, den)
    for k in range(0, n + 1):
        ARMABuffer[n - k] = a0 + (k * a1) + (k * k * a2) + (k * k * k * a3)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Afirma(_MQL5Indicator):
    name = 'afirma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Periods': 4,  # LF transmission width 1/(2*Periods)
        'Taps': 21,  # Number of delay units in the filter
        'Window': _Choice({1: 'Rectangular window', 2: 'Hanning window 1', 3: 'Hanning window 2', 4: 'Blackman window', 5: 'Blackman-Harris window'}, default=4),  # Window index
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

