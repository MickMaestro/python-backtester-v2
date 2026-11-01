"""temab — converted from MQL5: MQL5 Indicators/TEMA Band/temab.mq5

Triple Exponential Moving Average Band
Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [11186720], 3: [11186720]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Bands middle', 2: 'Bands upper', 3: 'Bands lower'}, 'levels': [], 'description': ['Triple Exponential Moving Average Band'], 'name': 'temab', 'source': 'MQL5 Indicators/TEMA Band/temab.mq5', 'folder': 'TEMA Band', 'inputs': [{'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'int', 'default': 14, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 0, 'label': "Indicator's shift", 'sinput': False}, {'mql': 'ExtBandsDeviations', 'py': 'ExtBandsDeviations', 'param': 'ExtBandsDeviations', 'type': 'double', 'default': 1.5, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodEMA = _input('InpPeriodEMA', 14)  # EMA period
InpShift = _input('InpShift', 0)  # Indicator's shift
ExtBandsDeviations = _input('ExtBandsDeviations', 1.5)
TemaBuffer = Arr(0, 0.0)
Ema = Arr(0, 0.0)
EmaOfEma = Arr(0, 0.0)
EmaOfEmaOfEma = Arr(0, 0.0)
ExtStdDevBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, TemaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, Ema, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, EmaOfEma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, EmaOfEmaOfEma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtStdDevBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (3 * InpPeriodEMA) - 3)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShift)
    PlotIndexSetString(0, PLOT_LABEL, 'Bands(' + _str(InpPeriodEMA) + ') Middle')
    PlotIndexSetString(1, PLOT_LABEL, 'Bands(' + _str(InpPeriodEMA) + ') Upper')
    PlotIndexSetString(2, PLOT_LABEL, 'Bands(' + _str(InpPeriodEMA) + ') Lower')

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < ((3 * InpPeriodEMA) - 3):
        return 0
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpPeriodEMA, price, Ema)
    ExponentialMAOnBuffer(rates_total, prev_calculated, InpPeriodEMA - 1, InpPeriodEMA, Ema, EmaOfEma)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (2 * InpPeriodEMA) - 2, InpPeriodEMA, EmaOfEma, EmaOfEmaOfEma)
    for i in range(limit, rates_total):
        TemaBuffer[i] = (3 * Ema[i]) - (3 * EmaOfEma[i]) + EmaOfEmaOfEma[i]
        ExtStdDevBuffer[i] = StdDev_Func(i, price, TemaBuffer, InpPeriodEMA)
        UpBuffer[i] = TemaBuffer[i] + (ExtBandsDeviations * ExtStdDevBuffer[i])
        DnBuffer[i] = TemaBuffer[i] - (ExtBandsDeviations * ExtStdDevBuffer[i])
    return rates_total

def StdDev_Func(position, price, MAprice, period):
    StdDev_dTmp = 0.0
    if position < period:
        return StdDev_dTmp
    for i in range(0, period):
        StdDev_dTmp += MathPow(price[position - i] - MAprice[position], 2)
    StdDev_dTmp = MathSqrt(_fdiv(StdDev_dTmp, period))
    return StdDev_dTmp


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Temab(_MQL5Indicator):
    name = 'temab'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodEMA': 14,  # EMA period
        'InpShift': 0,  # Indicator's shift
        'ExtBandsDeviations': 1.5,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

