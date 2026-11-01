"""Keltner_Cloud — converted from MQL5: MQL5 Indicators/Keltner Channel in the cloud form/Keltner_Cloud.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 4, 2: 4, 3: 1, 4: 1, 5: 1}, 'colors': {1: [255], 2: [32768], 3: [16711935], 4: [16776960], 5: [65535]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'UpperCloud', 2: 'LowerCloud', 3: 'Upper', 4: 'Middle', 5: 'Lower'}, 'levels': [], 'description': [], 'name': 'Keltner_Cloud', 'source': 'MQL5 Indicators/Keltner Channel in the cloud form/Keltner_Cloud.mq5', 'folder': 'Keltner Channel in the cloud form', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 50, 'label': 'Number of the periods to smooth the center line', 'sinput': False}, {'mql': 'InpPeriodDev', 'py': 'InpPeriodDev', 'param': 'InpPeriodDev', 'type': 'uint', 'default': 50, 'label': 'Number of periods to smooth deviation', 'sinput': False}, {'mql': 'InpF', 'py': 'InpF', 'param': 'InpF', 'type': 'double', 'default': 1.0, 'label': 'Factor which is used to apply the deviation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'The center line applied price:', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'The center line smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 50)  # Number of the periods to smooth the center line
InpPeriodDev = _input('InpPeriodDev', 50)  # Number of periods to smooth deviation
InpF = _input('InpF', 1.0)  # Factor which is used to apply the deviation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # The center line applied price:
InpMethod = _input('InpMethod', MODE_SMA)  # The center line smoothing method
BufferUpperCloud1 = Arr(0, 0.0)
BufferUpperCloud2 = Arr(0, 0.0)
BufferLowerCloud1 = Arr(0, 0.0)
BufferLowerCloud2 = Arr(0, 0.0)
BufferUpper = Arr(0, 0.0)
BufferMiddle = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
period_ma = 0
period_dev = 0
handle_ma = 0
handle_atr = 0

def OnInit():
    global handle_atr, handle_ma, period_dev, period_ma
    SetIndexBuffer(0, BufferUpperCloud1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUpperCloud2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLowerCloud1, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLowerCloud2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferUpper, INDICATOR_DATA)
    SetIndexBuffer(5, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(6, BufferLower, INDICATOR_DATA)
    SetIndexBuffer(7, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Keltner with color zones')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferLower, True)
    ArraySetAsSeries(BufferLowerCloud1, True)
    ArraySetAsSeries(BufferLowerCloud2, True)
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferUpper, True)
    ArraySetAsSeries(BufferUpperCloud1, True)
    ArraySetAsSeries(BufferUpperCloud2, True)
    ArraySetAsSeries(BufferATR, True)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_dev = (1 if (InpPeriodDev < 1) else InpPeriodDev)
    ResetLastError()
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, period_ma, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_atr = iATR(Symbol(), PERIOD_CURRENT, period_dev)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    copied_ma = 0
    copied_atr = 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferLower, EMPTY_VALUE)
        ArrayInitialize(BufferLowerCloud1, EMPTY_VALUE)
        ArrayInitialize(BufferLowerCloud2, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle, EMPTY_VALUE)
        ArrayInitialize(BufferUpper, EMPTY_VALUE)
        ArrayInitialize(BufferUpperCloud1, EMPTY_VALUE)
        ArrayInitialize(BufferUpperCloud2, EMPTY_VALUE)
        ArrayInitialize(BufferATR, EMPTY_VALUE)
        copied_ma = CopyBuffer(handle_ma, 0, 0, rates_total, BufferMiddle)
        if copied_ma != rates_total:
            return 0
        copied_atr = CopyBuffer(handle_atr, 0, 0, rates_total, BufferATR)
        if copied_atr != rates_total:
            return 0
    copied = (rates_total if (limit > 1) else 1)
    copied_ma = CopyBuffer(handle_ma, 0, 0, copied, BufferMiddle)
    if copied_ma != copied:
        return 0
    copied_atr = CopyBuffer(handle_atr, 0, 0, copied, BufferATR)
    if copied_atr != copied:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferUpper[i] = BufferMiddle[i] + (BufferATR[i] * InpF)
        BufferUpperCloud1[i] = BufferUpper[i]
        BufferLowerCloud1[i] = BufferMiddle[i]
        BufferUpperCloud2[i] = BufferLowerCloud1[i]
        BufferLower[i] = BufferMiddle[i] - (BufferATR[i] * InpF)
        BufferLowerCloud2[i] = BufferLower[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KeltnerCloud(_MQL5Indicator):
    name = 'Keltner_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 50,  # Number of the periods to smooth the center line
        'InpPeriodDev': 50,  # Number of periods to smooth deviation
        'InpF': 1.0,  # Factor which is used to apply the deviation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # The center line applied price:
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # The center line smoothing method
    }

