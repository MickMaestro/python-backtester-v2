"""MFI_normalized — converted from MQL5: MQL5 Indicators/MFI_normalized/MFI_normalized.mq5

John Bollinger's MFI normalized indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Normalized MFI'}, 'levels': [], 'description': ["John Bollinger's MFI normalized indicator"], 'name': 'MFI_normalized', 'source': 'MQL5 Indicators/MFI_normalized/MFI_normalized.mq5', 'folder': 'MFI_normalized', 'inputs': [{'mql': 'InpPeriodMFI', 'py': 'InpPeriodMFI', 'param': 'InpPeriodMFI', 'type': 'uint', 'default': 10, 'label': 'MFI period', 'sinput': False}, {'mql': 'InpAppliedVolume', 'py': 'InpAppliedVolume', 'param': 'InpAppliedVolume', 'type': 'int', 'default': 0, 'label': 'MFI applied volume', 'sinput': False}, {'mql': 'InpPeriodBB', 'py': 'InpPeriodBB', 'param': 'InpPeriodBB', 'type': 'uint', 'default': 40, 'label': 'BB period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'BB deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodMFI = _input('InpPeriodMFI', 10)  # MFI period
InpAppliedVolume = _input('InpAppliedVolume', VOLUME_TICK)  # MFI applied volume
InpPeriodBB = _input('InpPeriodBB', 40)  # BB period
InpDeviation = _input('InpDeviation', 2.0)  # BB deviation
BufferNormMFI = Arr(0, 0.0)
BufferMFI = Arr(0, 0.0)
deviation = 0.0
period_mfi = 0
period_bb = 0
handle_mfi = 0

def OnInit():
    global deviation, handle_mfi, period_bb, period_mfi
    period_mfi = (1 if (InpPeriodMFI < 1) else InpPeriodMFI)
    period_bb = (1 if (InpPeriodBB < 1) else InpPeriodBB)
    deviation = InpDeviation
    SetIndexBuffer(0, BufferNormMFI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMFI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MFI normalized (' + _str(period_mfi) + ',' + _str(period_bb) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 1.0)
    ArraySetAsSeries(BufferNormMFI, True)
    ArraySetAsSeries(BufferMFI, True)
    ResetLastError()
    handle_mfi = iMFI(None, PERIOD_CURRENT, period_mfi, InpAppliedVolume)
    if handle_mfi == INVALID_HANDLE:
        Print(57, ': The iMFI(', _str(period_mfi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_bb, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_bb - period_mfi - 1
        ArrayInitialize(BufferNormMFI, 0)
        ArrayInitialize(BufferMFI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_mfi, 0, 0, count, BufferMFI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        TL = BandsOnArray(rates_total, i, period_bb, deviation, BufferMFI, UPPER_BAND)
        BL = BandsOnArray(rates_total, i, period_bb, deviation, BufferMFI, LOWER_BAND)
        BufferNormMFI[i] = (_fdiv(BufferMFI[i] - BL, TL - BL) if ((TL - BL) != 0) else 0)
    return rates_total

def BandsOnArray(rates_total, index, period, deviation_bb, array, line, as_series=True):
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    dev = StdDevOnArray(rates_total, index, period, array)
    mid = 0.0
    for i in range(0, period):
        mid += array[index + i]
    mid = _fdiv(mid, period)
    top = mid + (dev * deviation_bb)
    btm = mid - (dev * deviation_bb)
    return (top if (line == UPPER_BAND) else btm if (line == LOWER_BAND) else mid)

def StdDevOnArray(rates_total, index, period, array, as_series=True):
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    avg = 0.0
    for i in range(0, period):
        avg += array[index + i]
    avg = _fdiv(avg, period)
    sd = 0.0
    for i in range(0, period):
        sd += (avg - array[index + i]) * (avg - array[index + i])
    return sqrt(_fdiv(sd, period))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MFINormalized(_MQL5Indicator):
    name = 'MFI_normalized'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMFI': 10,  # MFI period
        'InpAppliedVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # MFI applied volume
        'InpPeriodBB': 40,  # BB period
        'InpDeviation': 2.0,  # BB deviation
    }

