"""pema — converted from MQL5: MQL5 Indicators/PEMA/pema.mq5

Pentuple Exponential Moving Average
Copyright: Bruno Pio

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Bruno Pio', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [65535]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'PEMA'}, 'levels': [], 'description': ['Pentuple Exponential Moving Average'], 'name': 'pema', 'source': 'MQL5 Indicators/PEMA/pema.mq5', 'folder': 'PEMA', 'inputs': [{'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'int', 'default': 14, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 0, 'label': "Indicator's shift", 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodEMA = _input('InpPeriodEMA', 14)  # EMA period
InpShift = _input('InpShift', 0)  # Indicator's shift
PemaBuffer = Arr(0, 0.0)
Ema1 = Arr(0, 0.0)
Ema2 = Arr(0, 0.0)
Ema3 = Arr(0, 0.0)
Ema4 = Arr(0, 0.0)
Ema5 = Arr(0, 0.0)
Ema6 = Arr(0, 0.0)
Ema7 = Arr(0, 0.0)
Ema8 = Arr(0, 0.0)
Close = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, PemaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Ema1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, Ema2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, Ema3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, Ema4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, Ema5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, Ema6, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, Ema7, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, Ema8, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (8 * InpPeriodEMA) - 8)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PEMA(' + _str(InpPeriodEMA) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'PEMA(' + _str(InpPeriodEMA) + ')')
    ArraySetAsSeries(Close, True)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < ((8 * InpPeriodEMA) - 8):
        return 0
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpPeriodEMA, price, Ema1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, InpPeriodEMA - 1, InpPeriodEMA, Ema1, Ema2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (2 * InpPeriodEMA) - 2, InpPeriodEMA, Ema2, Ema3)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (3 * InpPeriodEMA) - 3, InpPeriodEMA, Ema3, Ema4)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (4 * InpPeriodEMA) - 4, InpPeriodEMA, Ema4, Ema5)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (5 * InpPeriodEMA) - 5, InpPeriodEMA, Ema5, Ema6)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (6 * InpPeriodEMA) - 6, InpPeriodEMA, Ema6, Ema7)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (7 * InpPeriodEMA) - 7, InpPeriodEMA, Ema7, Ema8)
    for i in range(limit, rates_total):
        PemaBuffer[i] = (8 * Ema1[i]) - (28 * Ema2[i]) + (56 * Ema3[i]) - (70 * Ema4[i]) + (56 * Ema5[i]) - (28 * Ema6[i]) + (8 * Ema7[i]) - Ema8[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pema(_MQL5Indicator):
    name = 'pema'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodEMA': 14,  # EMA period
        'InpShift': 0,  # Indicator's shift
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

