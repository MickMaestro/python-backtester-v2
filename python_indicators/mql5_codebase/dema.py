"""dema — converted from MQL5: MQL5 Indicators/Double Exponential Moving Average (DEMA)/dema.mq5

Double Exponential Moving Average
Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9109504]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'DEMA'}, 'levels': [], 'description': ['Double Exponential Moving Average'], 'name': 'dema', 'source': 'MQL5 Indicators/Double Exponential Moving Average (DEMA)/dema.mq5', 'folder': 'Double Exponential Moving Average (DEMA)', 'inputs': [{'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'int', 'default': 14, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 0, 'label': "Indicator's shift", 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodEMA = _input('InpPeriodEMA', 14)  # EMA period
InpShift = _input('InpShift', 0)  # Indicator's shift
DemaBuffer = Arr(0, 0.0)
Ema = Arr(0, 0.0)
EmaOfEma = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, DemaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Ema, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, EmaOfEma, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (2 * InpPeriodEMA) - 2)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DEMA(' + _str(InpPeriodEMA) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'DEMA(' + _str(InpPeriodEMA) + ')')

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < ((2 * InpPeriodEMA) - 2):
        return 0
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpPeriodEMA, price, Ema)
    ExponentialMAOnBuffer(rates_total, prev_calculated, InpPeriodEMA - 1, InpPeriodEMA, Ema, EmaOfEma)
    for i in range(limit, rates_total):
        DemaBuffer[i] = (2 * Ema[i]) - EmaOfEma[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dema(_MQL5Indicator):
    name = 'dema'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodEMA': 14,  # EMA period
        'InpShift': 0,  # Indicator's shift
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

