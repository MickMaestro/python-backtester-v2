"""WSI — converted from MQL5: MQL5 Indicators/WSI/WSI.mq5

Wave Segregation Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 9419919, 255, 8894686, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'WSI'}, 'levels': [], 'description': ['Wave Segregation Index indicator'], 'name': 'WSI', 'source': 'MQL5 Indicators/WSI/WSI.mq5', 'folder': 'WSI', 'inputs': [{'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 100, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpPeriodADX', 'py': 'InpPeriodADX', 'param': 'InpPeriodADX', 'type': 'uint', 'default': 100, 'label': 'ADX period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodCCI = _input('InpPeriodCCI', 100)  # CCI period
InpPeriodADX = _input('InpPeriodADX', 100)  # ADX period
BufferWSI = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
BufferADX = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_cci = 0
period_adx = 0
handle_cci = 0
handle_adx = 0
handle_ma = 0

def OnInit():
    global handle_adx, handle_cci, handle_ma, period_adx, period_cci
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    period_adx = (1 if (InpPeriodADX < 1) else InpPeriodADX)
    SetIndexBuffer(0, BufferWSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferCCI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferADX, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WSI (' + _str(period_cci) + ',' + _str(period_adx) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferWSI, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferCCI, True)
    ArraySetAsSeries(BufferADX, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, PRICE_TYPICAL)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_adx = iADX(None, PERIOD_CURRENT, period_adx)
    if handle_adx == INVALID_HANDLE:
        Print('The iADX(', _str(period_adx), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_TYPICAL)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferWSI, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 4)
        ArrayInitialize(BufferCCI, 0)
        ArrayInitialize(BufferADX, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx, MAIN_LINE, 0, count, BufferADX)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferWSI[i] = (BufferCCI[i] * BufferMA[i] * BufferADX[i]) / 1000.0
        BufferColors[i] = ((0 if (BufferWSI[i] > BufferWSI[i + 1]) else 1 if (BufferWSI[i] < BufferWSI[i + 1]) else 4) if (BufferWSI[i] > 0) else (2 if (BufferWSI[i] < BufferWSI[i + 1]) else 3 if (BufferWSI[i] > BufferWSI[i + 1]) else 4) if (BufferWSI[i] < 0) else 4)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WSI(_MQL5Indicator):
    name = 'WSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodCCI': 100,  # CCI period
        'InpPeriodADX': 100,  # ADX period
    }

