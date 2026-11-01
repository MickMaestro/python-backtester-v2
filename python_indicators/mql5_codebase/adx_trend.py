"""ADX_Trend — converted from MQL5: MQL5 Indicators/ADX_Trend/ADX_Trend.mq5

ADX Trend indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bearish ADXTrend', 2: 'Bullish ADXTrend'}, 'levels': [], 'description': ['ADX Trend indicator'], 'name': 'ADX_Trend', 'source': 'MQL5 Indicators/ADX_Trend/ADX_Trend.mq5', 'folder': 'ADX_Trend', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 10, 'label': 'First ADX period', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 14, 'label': 'Second ADX period', 'sinput': False}, {'mql': 'InpPeriod3', 'py': 'InpPeriod3', 'param': 'InpPeriod3', 'type': 'uint', 'default': 20, 'label': 'Third ADX period', 'sinput': False}, {'mql': 'InpLev1', 'py': 'InpLev1', 'param': 'InpLev1', 'type': 'double', 'default': 35.0, 'label': 'Lelel 1', 'sinput': False}, {'mql': 'InpLev2', 'py': 'InpLev2', 'param': 'InpLev2', 'type': 'double', 'default': 30.0, 'label': 'Level 2', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpAnchorBuffer', 'py': 'InpAnchorBuffer', 'param': 'InpAnchorBuffer', 'type': 'int', 'default': 0, 'label': 'Signal point anchor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_ANCHOR_BUFFER
ANCHOR_HL = 0
ANCHOR_OPEN = 1
_enum('ENUM_ANCHOR_BUFFER', {0: 'ANCHOR_HL', 1: 'ANCHOR_OPEN'})

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 10)  # First ADX period
InpPeriod2 = _input('InpPeriod2', 14)  # Second ADX period
InpPeriod3 = _input('InpPeriod3', 20)  # Third ADX period
InpLev1 = _input('InpLev1', 35.0)  # Lelel 1
InpLev2 = _input('InpLev2', 30.0)  # Level 2
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpAnchorBuffer = _input('InpAnchorBuffer', ANCHOR_HL)  # Signal point anchor
BufferBear = Arr(0, 0.0)
BufferBull = Arr(0, 0.0)
BufferADX1 = Arr(0, 0.0)
BufferADX2 = Arr(0, 0.0)
BufferADX3 = Arr(0, 0.0)
BufferPDI = Arr(0, 0.0)
BufferMDI = Arr(0, 0.0)
lev1 = 0.0
lev2 = 0.0
period1 = 0
period2 = 0
period3 = 0
handle_adx1 = 0
handle_adx2 = 0
handle_adx3 = 0

def OnInit():
    global handle_adx1, handle_adx2, handle_adx3, lev1, lev2, period1, period2, period3
    period1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    period3 = (1 if (InpPeriod3 < 1) else InpPeriod3)
    lev1 = InpLev1
    lev2 = InpLev2
    SetIndexBuffer(0, BufferBear, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBull, INDICATOR_DATA)
    SetIndexBuffer(2, BufferADX1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferADX2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferADX3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferPDI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMDI, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ADX Trend indicator (' + _str(period1) + ',' + _str(period2) + ',' + _str(period3) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBear, True)
    ArraySetAsSeries(BufferBull, True)
    ArraySetAsSeries(BufferADX1, True)
    ArraySetAsSeries(BufferADX2, True)
    ArraySetAsSeries(BufferADX3, True)
    ArraySetAsSeries(BufferPDI, True)
    ArraySetAsSeries(BufferMDI, True)
    ResetLastError()
    handle_adx1 = iADX(None, PERIOD_CURRENT, period1)
    if handle_adx1 == INVALID_HANDLE:
        Print('The iADX(', _str(period1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_adx2 = iADX(None, PERIOD_CURRENT, period2)
    if handle_adx2 == INVALID_HANDLE:
        Print('The iADX(', _str(period2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_adx3 = iADX(None, PERIOD_CURRENT, period3)
    if handle_adx3 == INVALID_HANDLE:
        Print('The iADX(', _str(period3), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferBear, EMPTY_VALUE)
        ArrayInitialize(BufferBull, EMPTY_VALUE)
        ArrayInitialize(BufferADX1, 0)
        ArrayInitialize(BufferADX2, 0)
        ArrayInitialize(BufferADX3, 0)
        ArrayInitialize(BufferPDI, 0)
        ArrayInitialize(BufferMDI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_adx1, 0, 0, count, BufferADX1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx2, 0, 0, count, BufferADX2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx3, 0, 0, count, BufferADX3)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx1, PLUSDI_LINE, 0, count, BufferPDI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx1, MINUSDI_LINE, 0, count, BufferMDI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        ADX1_0 = BufferADX1[i]
        ADX2_0 = BufferADX2[i]
        ADX3_0 = BufferADX3[i]
        ADX1_1 = BufferADX1[i + 1]
        ADX2_1 = BufferADX2[i + 1]
        ADX3_1 = BufferADX3[i + 1]
        DMI = BufferPDI[i] - BufferMDI[i]
        BufferBull[i] = EMPTY_VALUE
        BufferBear[i] = BufferBull[i]
        if (((ADX1_1 < ADX1_0 and ADX2_1 < ADX2_0) and ADX3_1 < ADX3_0) and ADX1_0 > lev1) and ADX2_0 > lev2:
            if DMI > 0:
                BufferBear[i] = (high[i] if (InpAnchorBuffer == ANCHOR_HL) else open[i])
            else:
                BufferBull[i] = (low[i] if (InpAnchorBuffer == ANCHOR_HL) else open[i])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADXTrend(_MQL5Indicator):
    name = 'ADX_Trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 10,  # First ADX period
        'InpPeriod2': 14,  # Second ADX period
        'InpPeriod3': 20,  # Third ADX period
        'InpLev1': 35.0,  # Lelel 1
        'InpLev2': 30.0,  # Level 2
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpAnchorBuffer': _Choice({0: 'High/Low', 1: 'Open'}, default=0),  # Signal point anchor
    }

