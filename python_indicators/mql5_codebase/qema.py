"""qema — converted from MQL5: MQL5 Indicators/QEMA/qema.mq5

Quadruple Exponential Moving Average
Copyright: Bruno Pio

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Bruno Pio', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [65535]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'QEMA'}, 'levels': [], 'description': ['Quadruple Exponential Moving Average'], 'name': 'qema', 'source': 'MQL5 Indicators/QEMA/qema.mq5', 'folder': 'QEMA', 'inputs': [{'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'int', 'default': 14, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 0, 'label': "Indicator's shift", 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodEMA = _input('InpPeriodEMA', 14)  # EMA period
InpShift = _input('InpShift', 0)  # Indicator's shift
QemaBuffer = Arr(0, 0.0)
Ema = Arr(0, 0.0)
EmaOfEma = Arr(0, 0.0)
EmaOfEmaOfEma = Arr(0, 0.0)
EmaOfEmaOfEmaOfEma = Arr(0, 0.0)
EmaOfEmaOfEmaOfEmaOfEma = Arr(0, 0.0)
Close = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, QemaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Ema, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, EmaOfEma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, EmaOfEmaOfEma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, EmaOfEmaOfEmaOfEma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, EmaOfEmaOfEmaOfEmaOfEma, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (5 * InpPeriodEMA) - 5)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'QEMA(' + _str(InpPeriodEMA) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'QEMA(' + _str(InpPeriodEMA) + ')')
    ArraySetAsSeries(Close, True)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < ((5 * InpPeriodEMA) - 5):
        return 0
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpPeriodEMA, price, Ema)
    ExponentialMAOnBuffer(rates_total, prev_calculated, InpPeriodEMA - 1, InpPeriodEMA, Ema, EmaOfEma)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (2 * InpPeriodEMA) - 2, InpPeriodEMA, EmaOfEma, EmaOfEmaOfEma)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (3 * InpPeriodEMA) - 3, InpPeriodEMA, EmaOfEmaOfEma, EmaOfEmaOfEmaOfEma)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (4 * InpPeriodEMA) - 4, InpPeriodEMA, EmaOfEmaOfEmaOfEma, EmaOfEmaOfEmaOfEmaOfEma)
    for i in range(limit, rates_total):
        QemaBuffer[i] = (5 * Ema[i]) - (10 * EmaOfEma[i]) + (10 * EmaOfEmaOfEma[i]) - (5 * EmaOfEmaOfEmaOfEma[i]) + EmaOfEmaOfEmaOfEmaOfEma[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Qema(_MQL5Indicator):
    name = 'qema'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodEMA': 14,  # EMA period
        'InpShift': 0,  # Indicator's shift
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

