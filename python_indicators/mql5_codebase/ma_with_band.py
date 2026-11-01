"""MA_With_Band — converted from MQL5: MQL5 Indicators/MA with Band/MA_With_Band.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 4, 2: 4, 3: 1, 4: 1, 5: 1}, 'colors': {1: [7451452], 2: [255], 3: [16711935], 4: [16776960], 5: [65535]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Cloud Upper', 2: 'Cloud Lower', 3: 'Upper', 4: 'Middle', 5: 'Lower'}, 'levels': [], 'description': [], 'name': 'MA_With_Band', 'source': 'MQL5 Indicators/MA with Band/MA_With_Band.mq5', 'folder': 'MA with Band', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 10, 'label': 'Period of MA calculation', 'sinput': False}, {'mql': 'InpMethodMA', 'py': 'InpMethodMA', 'param': 'InpMethodMA', 'type': 'int', 'default': 0, 'label': 'Method of MA calculation', 'sinput': False}, {'mql': 'InpAppliedPriceMA', 'py': 'InpAppliedPriceMA', 'param': 'InpAppliedPriceMA', 'type': 'int', 'default': 1, 'label': 'Applied price of MA', 'sinput': False}, {'mql': 'InpPeriodBand', 'py': 'InpPeriodBand', 'param': 'InpPeriodBand', 'type': 'uint', 'default': 15, 'label': 'Period of BB calculation', 'sinput': False}, {'mql': 'InpDeviationBand', 'py': 'InpDeviationBand', 'param': 'InpDeviationBand', 'type': 'double', 'default': 2.0, 'label': 'Deviation of BB', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 10)  # Period of MA calculation
InpMethodMA = _input('InpMethodMA', MODE_SMA)  # Method of MA calculation
InpAppliedPriceMA = _input('InpAppliedPriceMA', PRICE_CLOSE)  # Applied price of MA
InpPeriodBand = _input('InpPeriodBand', 15)  # Period of BB calculation
InpDeviationBand = _input('InpDeviationBand', 2.0)  # Deviation of BB
BufferCloudUpper1 = Arr(0, 0.0)
BufferCloudUpper2 = Arr(0, 0.0)
BufferCloudLower1 = Arr(0, 0.0)
BufferCloudLower2 = Arr(0, 0.0)
BufferLower = Arr(0, 0.0)
BufferMiddle = Arr(0, 0.0)
BufferUpper = Arr(0, 0.0)
handle_ma = 0
handle_bb = 0
period_ma = 0
period_bb = 0
deviation = 0.0

def OnInit():
    global deviation, handle_bb, handle_ma, period_bb, period_ma
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_bb = (1 if (InpPeriodBand < 1) else InpPeriodBand)
    deviation = (0.1 if (InpDeviationBand < 0.1) else InpDeviationBand)
    SetIndexBuffer(0, BufferCloudUpper1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCloudUpper2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCloudLower1, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCloudLower2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferUpper, INDICATOR_DATA)
    SetIndexBuffer(5, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(6, BufferLower, INDICATOR_DATA)
    ArraySetAsSeries(BufferCloudUpper1, True)
    ArraySetAsSeries(BufferCloudUpper2, True)
    ArraySetAsSeries(BufferCloudLower1, True)
    ArraySetAsSeries(BufferCloudLower2, True)
    ArraySetAsSeries(BufferUpper, True)
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferLower, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA with Band')
    handle_ma = iMA(Symbol(), PERIOD_CURRENT, period_ma, 0, InpMethodMA, InpAppliedPriceMA)
    if handle_ma == INVALID_HANDLE:
        Print("Error creating MA's handle: ", GetLastError())
        return INIT_FAILED
    handle_bb = iBands(Symbol(), PERIOD_CURRENT, period_bb, 0, deviation, handle_ma)
    if handle_bb == INVALID_HANDLE:
        Print("Error creating BB's handle: ", GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMiddle, EMPTY_VALUE)
        ArrayInitialize(BufferUpper, EMPTY_VALUE)
        ArrayInitialize(BufferLower, EMPTY_VALUE)
        ArrayInitialize(BufferCloudUpper1, EMPTY_VALUE)
        ArrayInitialize(BufferCloudUpper2, EMPTY_VALUE)
        ArrayInitialize(BufferCloudLower1, EMPTY_VALUE)
        ArrayInitialize(BufferCloudLower2, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMiddle)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, 1, 0, count, BufferUpper)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, 2, 0, count, BufferLower)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCloudUpper2[i] = BufferMiddle[i]
        BufferCloudLower1[i] = BufferCloudUpper2[i]
        BufferCloudUpper1[i] = BufferUpper[i]
        BufferCloudLower2[i] = BufferLower[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAWithBand(_MQL5Indicator):
    name = 'MA_With_Band'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 10,  # Period of MA calculation
        'InpMethodMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method of MA calculation
        'InpAppliedPriceMA': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price of MA
        'InpPeriodBand': 15,  # Period of BB calculation
        'InpDeviationBand': 2.0,  # Deviation of BB
    }

