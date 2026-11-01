"""nonlagdot — converted from MQL5: MQL5 Indicators/NonLagDot/nonlagdot.mq5

Copyright: Copyright © 2006, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [8421504, 16711935, 32768]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'NonLagDot'}, 'levels': [], 'description': [], 'name': 'nonlagdot', 'source': 'MQL5 Indicators/NonLagDot/nonlagdot.mq5', 'folder': 'NonLagDot', 'inputs': [{'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Type', 'py': 'Type', 'param': 'Type', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Indicator calculation period', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 0.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Price = _input('Price', PRICE_CLOSE)  # Applied price
Type = _input('Type', MODE_SMA)  # Smoothing method
Length = _input('Length', 10)  # Indicator calculation period
Filter = _input('Filter', 0)
Deviation = _input('Deviation', 0.0)  # Deviation
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
MABuffer = Arr(0, 0.0)
ColorMABuffer = Arr(0, 0.0)
min_rates_total = 0
MA_Handle = 0
Phase = 0
Coeff = 0.0
Len = 0.0
Cycle = 0.0
dT1 = 0.0
dT2 = 0.0
Kd = 0.0
Fi = 0.0

def OnInit():
    global Coeff, Cycle, Fi, Kd, Len, MA_Handle, Phase, dT1, dT2, min_rates_total
    Coeff = 3 * 3.1415926535
    Phase = Length - 1
    Cycle = 4.0
    Len = (Length * Cycle) + Phase
    dT1 = _fdiv((2 * Cycle) - 1, (Cycle * Length) - 1)
    dT2 = _fdiv(1.0, Phase - 1)
    Kd = 1.0 + (Deviation / 100)
    Fi = Filter * Point()
    min_rates_total = _int(Length + Len + 1)
    MA_Handle = iMA(None, 0, Length, 0, Type, Price)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    SetIndexBuffer(0, MABuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MABuffer, True)
    SetIndexBuffer(1, ColorMABuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorMABuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'NonLagDot( Length = ', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend1
    if BarsCalculated(MA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    trend0 = 0
    MA = Arr(0, 0.0)
    alfa = 0.0
    beta = 0.0
    t = 0.0
    Sum = 0.0
    Weight = 0.0
    g = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - min_rates_total - 1
    else:
        to_copy = rates_total - prev_calculated + _int(Len)
        limit = rates_total - prev_calculated
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    ArraySetAsSeries(MA, True)
    trend0 = _s_OnCalculate_trend1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Weight = 0.0
        Sum = 0.0
        t = 0.0
        iii = 0
        while iii <= (Len - 1):
            g = _fdiv(1.0, (Coeff * t) + 1)
            if t <= 0.5:
                g = 1.0
            beta = MathCos(3.1415926535 * t)
            alfa = g * beta
            Sum += alfa * MA[bar + iii]
            Weight += alfa
            if t < 1:
                t += dT2
            elif t < (Len - 1):
                t += dT1
            iii += 1
        if Weight > 0:
            MABuffer[bar] = _fdiv(Kd * Sum, Weight)
        if Filter > 0:
            if MathAbs(MABuffer[bar] - MABuffer[bar - 1]) < Fi:
                MABuffer[bar] = MABuffer[bar - 1]
        if (MABuffer[bar] - MABuffer[bar + 1]) > Fi:
            trend0 = 1
        if (MABuffer[bar + 1] - MABuffer[bar]) > Fi:
            trend0 = -1
        ColorMABuffer[bar] = 0.0
        if trend0 > 0:
            ColorMABuffer[bar] = 2.0
        if trend0 < 0:
            ColorMABuffer[bar] = 1.0
        if bar:
            _s_OnCalculate_trend1 = trend0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Nonlagdot(_MQL5Indicator):
    name = 'nonlagdot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'Type': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
        'Length': 10,  # Indicator calculation period
        'Filter': 0,
        'Deviation': 0.0,  # Deviation
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

