"""dpo — converted from MQL5: MQL5 Indicators/Detrended Price Oscillator (DPO)/dpo.mq5

Detrended Price Oscillator
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Detrended Price Oscillator'], 'name': 'dpo', 'source': 'MQL5 Indicators/Detrended Price Oscillator (DPO)/dpo.mq5', 'folder': 'Detrended Price Oscillator (DPO)', 'inputs': [{'mql': 'InpDetrendPeriod', 'py': 'InpDetrendPeriod', 'param': 'InpDetrendPeriod', 'type': 'int', 'default': 12, 'label': 'Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpDetrendPeriod = _input('InpDetrendPeriod', 12)  # Period
ExtDPOBuffer = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
ExtMAPeriod = 0

def OnInit():
    global ExtMAPeriod
    ExtMAPeriod = _idiv(InpDetrendPeriod, 2) + 1
    SetIndexBuffer(0, ExtDPOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMABuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtMAPeriod - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DPO(' + _str(InpDetrendPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, begin, price):
    limit = 0
    firstInd = begin + ExtMAPeriod - 1
    if begin > 0:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, firstInd)
    if prev_calculated < firstInd:
        ArrayInitialize(ExtDPOBuffer, 0.0)
        limit = firstInd
    else:
        limit = prev_calculated - 1
    SimpleMAOnBuffer(rates_total, prev_calculated, begin, ExtMAPeriod, price, ExtMABuffer)
    for i in range(limit, rates_total):
        ExtDPOBuffer[i] = price[i] - ExtMABuffer[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dpo(_MQL5Indicator):
    name = 'dpo'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDetrendPeriod': 12,  # Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

