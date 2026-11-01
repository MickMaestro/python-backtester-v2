"""Hurst_Bands — converted from MQL5: MQL5 Indicators/Hurst_Bands/Hurst_Bands.mq5

Hurst Bands indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [255], 2: [15128749], 3: [15128749], 4: [11119017], 5: [11119017], 6: [3329434], 7: [3329434]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {1: 'Center', 2: 'Extreme High', 3: 'Extreme Low', 4: 'Outer High', 5: 'Outer Low', 6: 'Inner High', 7: 'Inner Low'}, 'levels': [], 'description': ['Hurst Bands indicator'], 'name': 'Hurst_Bands', 'source': 'MQL5 Indicators/Hurst_Bands/Hurst_Bands.mq5', 'folder': 'Hurst_Bands', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpInner', 'py': 'InpInner', 'param': 'InpInner', 'type': 'double', 'default': 1.6, 'label': 'Inner value', 'sinput': False}, {'mql': 'InpOuter', 'py': 'InpOuter', 'param': 'InpOuter', 'type': 'double', 'default': 2.6, 'label': 'Outer value', 'sinput': False}, {'mql': 'InpExtreme', 'py': 'InpExtreme', 'param': 'InpExtreme', 'type': 'double', 'default': 4.2, 'label': 'Extreme value', 'sinput': False}, {'mql': 'InpShowExtreme', 'py': 'InpShowExtreme', 'param': 'InpShowExtreme', 'type': 'int', 'default': 1, 'label': 'Show extreme lines', 'sinput': False}, {'mql': 'InpShowOuter', 'py': 'InpShowOuter', 'param': 'InpShowOuter', 'type': 'int', 'default': 1, 'label': 'Show outer lines', 'sinput': False}, {'mql': 'InpShowInner', 'py': 'InpShowInner', 'param': 'InpShowInner', 'type': 'int', 'default': 1, 'label': 'Show inner lines', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpInner = _input('InpInner', 1.6)  # Inner value
InpOuter = _input('InpOuter', 2.6)  # Outer value
InpExtreme = _input('InpExtreme', 4.2)  # Extreme value
InpShowExtreme = _input('InpShowExtreme', INPUT_YES)  # Show extreme lines
InpShowOuter = _input('InpShowOuter', INPUT_YES)  # Show outer lines
InpShowInner = _input('InpShowInner', INPUT_YES)  # Show inner lines
BufferCenter = Arr(0, 0.0)
BufferExtUP = Arr(0, 0.0)
BufferExtDN = Arr(0, 0.0)
BufferOutUP = Arr(0, 0.0)
BufferOutDN = Arr(0, 0.0)
BufferInnUP = Arr(0, 0.0)
BufferInnDN = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
inner = 0.0
outer = 0.0
extreme = 0.0
period = 0
displacement = 0
handle_ma = 0

def OnInit():
    global displacement, extreme, handle_ma, inner, outer, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    displacement = _int((period / 2.0) + 1.0)
    inner = fabs(InpInner)
    outer = fabs(InpOuter)
    extreme = fabs(InpExtreme)
    SetIndexBuffer(0, BufferCenter, INDICATOR_DATA)
    SetIndexBuffer(1, BufferExtUP, INDICATOR_DATA)
    SetIndexBuffer(2, BufferExtDN, INDICATOR_DATA)
    SetIndexBuffer(3, BufferOutUP, INDICATOR_DATA)
    SetIndexBuffer(4, BufferOutDN, INDICATOR_DATA)
    SetIndexBuffer(5, BufferInnUP, INDICATOR_DATA)
    SetIndexBuffer(6, BufferInnDN, INDICATOR_DATA)
    SetIndexBuffer(7, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hurst Bands (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferCenter, True)
    ArraySetAsSeries(BufferExtUP, True)
    ArraySetAsSeries(BufferExtDN, True)
    ArraySetAsSeries(BufferOutUP, True)
    ArraySetAsSeries(BufferOutDN, True)
    ArraySetAsSeries(BufferInnUP, True)
    ArraySetAsSeries(BufferInnDN, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, MODE_SMA, PRICE_MEDIAN)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(displacement + period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - displacement - period - 1
        ArrayInitialize(BufferCenter, EMPTY_VALUE)
        ArrayInitialize(BufferExtUP, EMPTY_VALUE)
        ArrayInitialize(BufferExtDN, EMPTY_VALUE)
        ArrayInitialize(BufferOutUP, EMPTY_VALUE)
        ArrayInitialize(BufferOutDN, EMPTY_VALUE)
        ArrayInitialize(BufferInnUP, EMPTY_VALUE)
        ArrayInitialize(BufferInnDN, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCenter[i] = BufferMA[i + displacement]
        extreme_band = (BufferCenter[i] * extreme) / 100.0
        outer_band = (BufferCenter[i] * outer) / 100.0
        inner_band = (BufferCenter[i] * inner) / 100.0
        BufferExtUP[i] = ((BufferCenter[i] + extreme_band) if InpShowExtreme else EMPTY_VALUE)
        BufferExtDN[i] = ((BufferCenter[i] - extreme_band) if InpShowExtreme else EMPTY_VALUE)
        BufferOutUP[i] = ((BufferCenter[i] + outer_band) if InpShowOuter else EMPTY_VALUE)
        BufferOutDN[i] = ((BufferCenter[i] - outer_band) if InpShowOuter else EMPTY_VALUE)
        BufferInnUP[i] = ((BufferCenter[i] + inner_band) if InpShowInner else EMPTY_VALUE)
        BufferInnDN[i] = ((BufferCenter[i] - inner_band) if InpShowInner else EMPTY_VALUE)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HurstBands(_MQL5Indicator):
    name = 'Hurst_Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpInner': 1.6,  # Inner value
        'InpOuter': 2.6,  # Outer value
        'InpExtreme': 4.2,  # Extreme value
        'InpShowExtreme': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show extreme lines
        'InpShowOuter': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show outer lines
        'InpShowInner': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show inner lines
    }

