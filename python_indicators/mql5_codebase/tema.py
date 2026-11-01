"""tema — converted from MQL5: MQL5 Indicators/Triple Exponential Moving Average (TEMA)/tema.mq5

Triple Exponential Moving Average
Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9109504]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'TEMA'}, 'levels': [], 'description': ['Triple Exponential Moving Average'], 'name': 'tema', 'source': 'MQL5 Indicators/Triple Exponential Moving Average (TEMA)/tema.mq5', 'folder': 'Triple Exponential Moving Average (TEMA)', 'inputs': [{'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'int', 'default': 14, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 0, 'label': "Indicator's shift", 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodEMA = _input('InpPeriodEMA', 14)  # EMA period
InpShift = _input('InpShift', 0)  # Indicator's shift
TemaBuffer = Arr(0, 0.0)
Ema = Arr(0, 0.0)
EmaOfEma = Arr(0, 0.0)
EmaOfEmaOfEma = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, TemaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Ema, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, EmaOfEma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, EmaOfEmaOfEma, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (3 * InpPeriodEMA) - 3)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TEMA(' + _str(InpPeriodEMA) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'TEMA(' + _str(InpPeriodEMA) + ')')

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
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tema(_MQL5Indicator):
    name = 'tema'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodEMA': 14,  # EMA period
        'InpShift': 0,  # Indicator's shift
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

