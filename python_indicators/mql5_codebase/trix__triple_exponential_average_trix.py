"""trix — converted from MQL5: MQL5 Indicators/Triple Exponential Average (TRIX)/trix.mq5

Triple Exponential Average
Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'TRIX'}, 'levels': [], 'description': ['Triple Exponential Average'], 'name': 'trix', 'source': 'MQL5 Indicators/Triple Exponential Average (TRIX)/trix.mq5', 'folder': 'Triple Exponential Average (TRIX)', 'inputs': [{'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'int', 'default': 14, 'label': 'EMA period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodEMA = _input('InpPeriodEMA', 14)  # EMA period
TRIX_Buffer = Arr(0, 0.0)
EMA = Arr(0, 0.0)
SecondEMA = Arr(0, 0.0)
ThirdEMA = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, TRIX_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, EMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, SecondEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ThirdEMA, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (3 * InpPeriodEMA) - 3)
    PlotIndexSetString(0, PLOT_LABEL, 'TRIX(' + _str(InpPeriodEMA) + ')')
    IndicatorSetString(INDICATOR_SHORTNAME, 'TRIX(' + _str(InpPeriodEMA) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 5)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < ((3 * InpPeriodEMA) - 3):
        return 0
    limit = 0
    if prev_calculated == 0:
        limit = 3 * (InpPeriodEMA - 1)
        for i in range(0, limit):
            TRIX_Buffer[0] = EMPTY_VALUE
    else:
        limit = prev_calculated - 1
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpPeriodEMA, price, EMA)
    ExponentialMAOnBuffer(rates_total, prev_calculated, InpPeriodEMA - 1, InpPeriodEMA, EMA, SecondEMA)
    ExponentialMAOnBuffer(rates_total, prev_calculated, (2 * InpPeriodEMA) - 2, InpPeriodEMA, SecondEMA, ThirdEMA)
    for i in range(limit, rates_total):
        if ThirdEMA[i - 1] != 0.0:
            TRIX_Buffer[i] = _fdiv(ThirdEMA[i] - ThirdEMA[i - 1], ThirdEMA[i - 1])
        else:
            TRIX_Buffer[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trix(_MQL5Indicator):
    name = 'trix'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodEMA': 14,  # EMA period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

