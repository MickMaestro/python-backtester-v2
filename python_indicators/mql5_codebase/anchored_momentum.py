"""Anchored_Momentum — converted from MQL5: MQL5 Indicators/Anchored_Momentum/Anchored_Momentum.mq5

Anchored Momentum oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'AMomentum'}, 'levels': [], 'description': ['Anchored Momentum oscillator'], 'name': 'Anchored_Momentum', 'source': 'MQL5 Indicators/Anchored_Momentum/Anchored_Momentum.mq5', 'folder': 'Anchored_Momentum', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 2, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 2, 'label': 'First MA method', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 42, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 0, 'label': 'Second MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpBuffZoneUp', 'py': 'InpBuffZoneUp', 'param': 'InpBuffZoneUp', 'type': 'double', 'default': 0.2, 'label': 'Upper limit of the buffered zone', 'sinput': False}, {'mql': 'InpBuffZoneDn', 'py': 'InpBuffZoneDn', 'param': 'InpBuffZoneDn', 'type': 'double', 'default': -0.2, 'label': 'Lower limit of the buffered zone', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 2)  # First MA period
InpMethod1 = _input('InpMethod1', 2)  # First MA method
InpPeriod2 = _input('InpPeriod2', 42)  # Second MA period
InpMethod2 = _input('InpMethod2', 0)  # Second MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpBuffZoneUp = _input('InpBuffZoneUp', 0.2)  # Upper limit of the buffered zone
InpBuffZoneDn = _input('InpBuffZoneDn', -0.2)  # Lower limit of the buffered zone
BufferAMOM = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
zone_up = 0.0
zone_dn = 0.0
period1 = 0
period2 = 0
period_max = 0
handle_ma1 = 0
handle_ma2 = 0

def OnInit():
    global handle_ma1, handle_ma2, period1, period2, period_max, zone_dn, zone_up
    period1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period2 = ((period1 + 1) if (InpPeriod2 == period1) else 1 if (InpPeriod2 < 1) else InpPeriod2)
    period_max = fmax(period1, period2)
    zone_up = (0 if (InpBuffZoneUp < 0) else InpBuffZoneUp)
    zone_dn = (0 if (InpBuffZoneDn > 0) else InpBuffZoneDn)
    SetIndexBuffer(0, BufferAMOM, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Anchored Momentum (' + _str(period1) + ',' + _str(period2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, zone_up)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, zone_dn)
    ArraySetAsSeries(BufferAMOM, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, period1, 0, InpMethod1, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(', _str(period1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, PERIOD_CURRENT, period2, 0, InpMethod2, InpAppliedPrice)
    if handle_ma2 == INVALID_HANDLE:
        Print('The iMA(', _str(period2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferAMOM, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferMA2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        MA1 = BufferMA1[i]
        MA2 = BufferMA2[i]
        BufferAMOM[i] = ((100.0 * (_fdiv(MA1, MA2) - 1.0)) if (MA2 != 0) else 0)
        BufferColors[i] = (0 if (BufferAMOM[i] > BufferAMOM[i + 1]) else 1 if (BufferAMOM[i] < BufferAMOM[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AnchoredMomentum(_MQL5Indicator):
    name = 'Anchored_Momentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 2,  # First MA period
        'InpMethod1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # First MA method
        'InpPeriod2': 42,  # Second MA period
        'InpMethod2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Second MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpBuffZoneUp': 0.2,  # Upper limit of the buffered zone
        'InpBuffZoneDn': -0.2,  # Lower limit of the buffered zone
    }

