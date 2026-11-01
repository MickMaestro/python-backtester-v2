"""wd.Range_MACD — converted from MQL5: MQL5 Indicators/wd.Range_MACD/wd.Range_MACD.mq5

This Moving Average Convergence/Divergence is enhanced with additional range information.
It calculates the range difference between the MACD and Signal lines, as well as the range distance between the last MACD bar and the current one.
This range information helps in measuring price cross-points, resistance/support levels, and trend changes more efficiently.
Labels for reference:
Label 1: MACD
Label 2: Signal
Label 3: Range between Signal and MACD
Label 4: Range between the last two MACD bars
Copyright: Copyright © 2023, Karya Prima Rajasa Mediavestama.; Link: https://www.mql5.com/en/code/47143; Version: 2.23

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2023, Karya Prima Rajasa Mediavestama.', 'link': 'https://www.mql5.com/en/code/47143', 'version': '2.23', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 3, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {1: 'MACD', 2: 'Signal', 3: 'Range Signal to MACD', 4: 'Range Last two MACD Bar'}, 'levels': [], 'description': ['This Moving Average Convergence/Divergence is enhanced with additional range information.', 'It calculates the range difference between the MACD and Signal lines, as well as the range distance between the last MACD bar and the current one.', 'This range information helps in measuring price cross-points, resistance/support levels, and trend changes more efficiently.', '', 'Labels for reference:', 'Label 1: MACD', 'Label 2: Signal', 'Label 3: Range between Signal and MACD', 'Label 4: Range between the last two MACD bars'], 'name': 'wd.Range_MACD', 'source': 'MQL5 Indicators/wd.Range_MACD/wd.Range_MACD.mq5', 'folder': 'wd.Range_MACD', 'inputs': [{'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpSignalSMA', 'py': 'InpSignalSMA', 'param': 'InpSignalSMA', 'type': 'int', 'default': 9, 'label': 'Signal SMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpFastEMA = _input('InpFastEMA', 12)  # Fast EMA period
InpSlowEMA = _input('InpSlowEMA', 26)  # Slow EMA period
InpSignalSMA = _input('InpSignalSMA', 9)  # Signal SMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtMacdBuffer = Arr(0, 0.0)
ExtSignalBuffer = Arr(0, 0.0)
ExtFastMaBuffer = Arr(0, 0.0)
ExtSlowMaBuffer = Arr(0, 0.0)
RangeSignalMACDBuffer = Arr(0, 0.0)
Range2LastBarMACDBuffer = Arr(0, 0.0)
ExtFastMaHandle = 0
ExtSlowMaHandle = 0

def OnInit():
    global ExtFastMaHandle, ExtSlowMaHandle
    SetIndexBuffer(0, ExtMacdBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtSignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, RangeSignalMACDBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, Range2LastBarMACDBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtFastMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtSlowMaBuffer, INDICATOR_CALCULATIONS)
    short_name = StringFormat('MACD(%d,%d,%d)', InpFastEMA, InpSlowEMA, InpSignalSMA)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    ExtFastMaHandle = iMA(None, 0, InpFastEMA, 0, MODE_EMA, InpAppliedPrice)
    ExtSlowMaHandle = iMA(None, 0, InpSlowEMA, 0, MODE_EMA, InpAppliedPrice)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < InpSignalSMA:
        return 0
    ArraySetAsSeries(ExtMacdBuffer, True)
    ArraySetAsSeries(ExtSignalBuffer, True)
    ArraySetAsSeries(RangeSignalMACDBuffer, True)
    ArraySetAsSeries(Range2LastBarMACDBuffer, True)
    ArraySetAsSeries(ExtFastMaBuffer, True)
    ArraySetAsSeries(ExtSlowMaBuffer, True)
    if CopyBuffer(ExtFastMaHandle, 0, 0, rates_total, ExtFastMaBuffer) != rates_total:
        Print('Copying ExtFastMaBuffer failed! Error ', GetLastError())
        return 0
    if CopyBuffer(ExtSlowMaHandle, 0, 0, rates_total, ExtSlowMaBuffer) != rates_total:
        Print('Copying ExtSlowMaBuffer failed! Error ', GetLastError())
        return 0
    for i in range(0, rates_total):
        ExtMacdBuffer[i] = ExtFastMaBuffer[i] - ExtSlowMaBuffer[i]
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, InpSignalSMA, ExtMacdBuffer, ExtSignalBuffer)
    for i in range(0, rates_total):
        rangeValue = _setitem(RangeSignalMACDBuffer, i, _fdiv(ExtMacdBuffer[i] - ExtSignalBuffer[i], Point()))
        RangeSignalMACDBuffer[i] = _int(MathRound(rangeValue * 10))
    for i in range(0, rates_total):
        if i == 0:
            rangeValue = _setitem(Range2LastBarMACDBuffer, i, _fdiv(ExtMacdBuffer[i] - ExtMacdBuffer[i + 1], Point()))
            Range2LastBarMACDBuffer[i] = _int(MathRound(rangeValue * 10))
        elif i == (rates_total - 1):
            rangeValue = _setitem(Range2LastBarMACDBuffer, i, _fdiv(ExtMacdBuffer[i - 1] - ExtMacdBuffer[i], Point()))
            Range2LastBarMACDBuffer[i] = _int(MathRound(rangeValue * 10))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WdRangeMACD(_MQL5Indicator):
    name = 'wd.Range_MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpFastEMA': 12,  # Fast EMA period
        'InpSlowEMA': 26,  # Slow EMA period
        'InpSignalSMA': 9,  # Signal SMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

