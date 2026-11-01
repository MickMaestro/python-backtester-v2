"""WAAB — converted from MQL5: MQL5 Indicators/WAAB/WAAB.mq5

Waddah Attar ADXxBollinger indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'WAAB'}, 'levels': [], 'description': ['Waddah Attar ADXxBollinger indicator'], 'name': 'WAAB', 'source': 'MQL5 Indicators/WAAB/WAAB.mq5', 'folder': 'WAAB', 'inputs': [{'mql': 'InpPeriodADX', 'py': 'InpPeriodADX', 'param': 'InpPeriodADX', 'type': 'uint', 'default': 14, 'label': 'ADX Period', 'sinput': False}, {'mql': 'InpPeriodBB', 'py': 'InpPeriodBB', 'param': 'InpPeriodBB', 'type': 'uint', 'default': 20, 'label': 'BB Period', 'sinput': False}, {'mql': 'InpAppliedPriceBB', 'py': 'InpAppliedPriceBB', 'param': 'InpAppliedPriceBB', 'type': 'int', 'default': 1, 'label': 'BB Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodADX = _input('InpPeriodADX', 14)  # ADX Period
InpPeriodBB = _input('InpPeriodBB', 20)  # BB Period
InpAppliedPriceBB = _input('InpAppliedPriceBB', PRICE_CLOSE)  # BB Applied price
BufferWAAB = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferADX = Arr(0, 0.0)
BufferPDI = Arr(0, 0.0)
BufferMDI = Arr(0, 0.0)
BufferBBUP = Arr(0, 0.0)
BufferBBDN = Arr(0, 0.0)
period_adx = 0
period_bb = 0
handle_adx = 0
handle_bb = 0

def OnInit():
    global handle_adx, handle_bb, period_adx, period_bb
    period_adx = (1 if (InpPeriodADX < 1) else InpPeriodADX)
    period_bb = (2 if (InpPeriodBB < 2) else InpPeriodBB)
    SetIndexBuffer(0, BufferWAAB, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferADX, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferPDI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMDI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferBBUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferBBDN, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Waddah Attar ADXxBollinger (' + _str(period_adx) + ',' + _str(period_bb) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferWAAB, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferADX, True)
    ArraySetAsSeries(BufferPDI, True)
    ArraySetAsSeries(BufferMDI, True)
    ArraySetAsSeries(BufferBBUP, True)
    ArraySetAsSeries(BufferBBDN, True)
    ResetLastError()
    handle_adx = iADX(None, PERIOD_CURRENT, period_adx)
    if handle_adx == INVALID_HANDLE:
        Print('The iADX(', _str(period_adx), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_bb = iBands(None, PERIOD_CURRENT, period_bb, 0, 2.0, InpAppliedPriceBB)
    if handle_bb == INVALID_HANDLE:
        Print('The iBands(', _str(period_bb), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferWAAB, EMPTY_VALUE)
        ArrayInitialize(BufferADX, 0)
        ArrayInitialize(BufferPDI, 0)
        ArrayInitialize(BufferMDI, 0)
        ArrayInitialize(BufferBBUP, 0)
        ArrayInitialize(BufferBBDN, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_adx, MAIN_LINE, 0, count, BufferADX)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx, PLUSDI_LINE, 0, count, BufferPDI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx, MINUSDI_LINE, 0, count, BufferMDI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, UPPER_BAND, 0, count, BufferBBUP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, LOWER_BAND, 0, count, BufferBBDN)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        mdi = BufferMDI[i]
        pdi = BufferPDI[i]
        xxplo = BufferBBUP[i] - BufferBBDN[i]
        BufferWAAB[i] = xxplo * BufferADX[i]
        BufferColors[i] = (0 if (pdi > mdi) else 1 if (pdi < mdi) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WAAB(_MQL5Indicator):
    name = 'WAAB'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodADX': 14,  # ADX Period
        'InpPeriodBB': 20,  # BB Period
        'InpAppliedPriceBB': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # BB Applied price
    }

