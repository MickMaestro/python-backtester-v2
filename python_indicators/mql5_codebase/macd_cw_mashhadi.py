"""MACD_CW_Mashhadi — converted from MQL5: MQL5 Indicators/Chart Window MACD/MACD_CW_Mashhadi.mq5

The indicator is an equivalent \\"Chart Window\\" version of MACD.
Link: Author: saeed.h.mashhadi@gmail.com; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'Author: saeed.h.mashhadi@gmail.com', 'version': '1.1', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fast-Slow EMA', 2: 'MACD SMA'}, 'levels': [], 'description': ['The indicator is an equivalent \\"Chart Window\\" version of MACD.'], 'name': 'MACD_CW_Mashhadi', 'source': 'MQL5 Indicators/Chart Window MACD/MACD_CW_Mashhadi.mq5', 'folder': 'Chart Window MACD', 'inputs': [{'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA Period = 12', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA Period = 26', 'sinput': False}, {'mql': 'InpSignalSMA', 'py': 'InpSignalSMA', 'param': 'InpSignalSMA', 'type': 'int', 'default': 9, 'label': 'Signal SMA Period = 9', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFastEMA = _input('InpFastEMA', 12)  # Fast EMA Period = 12
InpSlowEMA = _input('InpSlowEMA', 26)  # Slow EMA Period = 26
InpSignalSMA = _input('InpSignalSMA', 9)  # Signal SMA Period = 9
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied Price
Fast_Slow_Buffer = Arr(0, 0.0)
MACD_Buffer = Arr(0, 0.0)
ExtMacdBuffer = Arr(0, 0.0)
ExtSignalBuffer = Arr(0, 0.0)
ExtFastMaBuffer = Arr(0, 0.0)
ExtSlowMaBuffer = Arr(0, 0.0)
ExtFastMaHandle = 0
ExtSlowMaHandle = 0

def OnInit():
    global ExtFastMaHandle, ExtSlowMaHandle
    SetIndexBuffer(0, Fast_Slow_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, MACD_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtMacdBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtSignalBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtFastMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtSlowMaBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpSignalSMA - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD(' + _str(InpFastEMA) + ',' + _str(InpSlowEMA) + ',' + _str(InpSignalSMA) + ')')
    ExtFastMaHandle = iMA(None, 0, InpFastEMA, 0, MODE_EMA, InpAppliedPrice)
    ExtSlowMaHandle = iMA(None, 0, InpSlowEMA, 0, MODE_EMA, InpAppliedPrice)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    CopyBuffer(ExtFastMaHandle, 0, 0, rates_total, ExtFastMaBuffer)
    CopyBuffer(ExtSlowMaHandle, 0, 0, rates_total, ExtSlowMaBuffer)
    ii = 0
    ii = 0
    for ii in range(ii, rates_total):
        ExtMacdBuffer[ii] = ExtFastMaBuffer[ii] - ExtSlowMaBuffer[ii]
        Fast_Slow_Buffer[ii] = EMPTY_VALUE
        MACD_Buffer[ii] = EMPTY_VALUE
    else:
        ii = _range_end(ii, rates_total, 1)
    ii = 1
    for ii in range(ii, rates_total):
        Fast_Slow_Buffer[ii] = _fdiv(((1 - _fdiv(2, float(InpFastEMA) + 1)) * ExtFastMaBuffer[ii - 1]) - ((1 - _fdiv(2, float(InpSlowEMA) + 1)) * ExtSlowMaBuffer[ii - 1]), _fdiv(2, float(InpSlowEMA) + 1) - _fdiv(2, float(InpFastEMA) + 1))
    else:
        ii = _range_end(ii, rates_total, 1)
    ii = 0
    for ii in range(ii, InpSignalSMA - 1):
        ExtSignalBuffer[ii] = 0.0
    else:
        ii = _range_end(ii, InpSignalSMA - 1, 1)
    firstValue = 0.0
    ii = 0
    for ii in range(ii, InpSignalSMA):
        firstValue += ExtMacdBuffer[ii]
    else:
        ii = _range_end(ii, InpSignalSMA, 1)
    firstValue = firstValue / InpSignalSMA
    ExtSignalBuffer[InpSignalSMA - 1] = firstValue
    ii = InpSignalSMA
    for ii in range(ii, rates_total):
        ExtSignalBuffer[ii] = ExtSignalBuffer[ii - 1] + ((ExtMacdBuffer[ii] - ExtMacdBuffer[ii - InpSignalSMA]) / InpSignalSMA)
    else:
        ii = _range_end(ii, rates_total, 1)
    ii = InpSignalSMA
    for ii in range(ii, rates_total):
        MACD_Buffer[ii] = Fast_Slow_Buffer[ii] - (_fdiv((InpSignalSMA * ExtSignalBuffer[ii - 1]) - ExtMacdBuffer[ii - InpSignalSMA], _fdiv(2, float(InpSlowEMA) + 1) - _fdiv(2, float(InpFastEMA) + 1)) / (InpSignalSMA - 1))
    else:
        ii = _range_end(ii, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDCWMashhadi(_MQL5Indicator):
    name = 'MACD_CW_Mashhadi'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastEMA': 12,  # Fast EMA Period = 12
        'InpSlowEMA': 26,  # Slow EMA Period = 26
        'InpSignalSMA': 9,  # Signal SMA Period = 9
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied Price
    }

