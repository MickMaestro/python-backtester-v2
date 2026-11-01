"""WCCI — converted from MQL5: MQL5 Indicators/WCCI/WCCI.mq5

Weighted CCI
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'WCCI Fast', 2: 'WCCI Slow'}, 'levels': [], 'description': ['Weighted CCI'], 'name': 'WCCI', 'source': 'MQL5 Indicators/WCCI/WCCI.mq5', 'folder': 'WCCI', 'inputs': [{'mql': 'InpPeriodFastCCI', 'py': 'InpPeriodFastCCI', 'param': 'InpPeriodFastCCI', 'type': 'uint', 'default': 7, 'label': 'CCI Fast period', 'sinput': False}, {'mql': 'InpPeriodSlowCCI', 'py': 'InpPeriodSlowCCI', 'param': 'InpPeriodSlowCCI', 'type': 'uint', 'default': 14, 'label': 'CCI Slow period', 'sinput': False}, {'mql': 'InpWeight', 'py': 'InpWeight', 'param': 'InpWeight', 'type': 'int', 'default': 1, 'label': 'Weight', 'sinput': False}, {'mql': 'InpPeriodFastATR', 'py': 'InpPeriodFastATR', 'param': 'InpPeriodFastATR', 'type': 'uint', 'default': 7, 'label': 'ATR Fast period', 'sinput': False}, {'mql': 'InpPeriodSlowATR', 'py': 'InpPeriodSlowATR', 'param': 'InpPeriodSlowATR', 'type': 'uint', 'default': 50, 'label': 'ATR Slow period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverboughtMajor', 'py': 'InpOverboughtMajor', 'param': 'InpOverboughtMajor', 'type': 'int', 'default': 200, 'label': 'Overbought max', 'sinput': False}, {'mql': 'InpOverboughtMinor', 'py': 'InpOverboughtMinor', 'param': 'InpOverboughtMinor', 'type': 'int', 'default': 50, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversoldMinor', 'py': 'InpOversoldMinor', 'param': 'InpOversoldMinor', 'type': 'int', 'default': -50, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpOversoldMajor', 'py': 'InpOversoldMajor', 'param': 'InpOversoldMajor', 'type': 'int', 'default': -200, 'label': 'Oversold min', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFastCCI = _input('InpPeriodFastCCI', 7)  # CCI Fast period
InpPeriodSlowCCI = _input('InpPeriodSlowCCI', 14)  # CCI Slow period
InpWeight = _input('InpWeight', 1)  # Weight
InpPeriodFastATR = _input('InpPeriodFastATR', 7)  # ATR Fast period
InpPeriodSlowATR = _input('InpPeriodSlowATR', 50)  # ATR Slow period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverboughtMajor = _input('InpOverboughtMajor', 200)  # Overbought max
InpOverboughtMinor = _input('InpOverboughtMinor', 50)  # Overbought
InpOversoldMinor = _input('InpOversoldMinor', -50)  # Oversold
InpOversoldMajor = _input('InpOversoldMajor', -200)  # Oversold min
BufferFast = Arr(0, 0.0)
BufferSlow = Arr(0, 0.0)
BufferCCIF = Arr(0, 0.0)
BufferCCIS = Arr(0, 0.0)
BufferATRF = Arr(0, 0.0)
BufferATRS = Arr(0, 0.0)
period_ccif = 0
period_ccis = 0
period_atrf = 0
period_atrs = 0
overbought_major = 0
overbought_minor = 0
oversold_major = 0
oversold_minor = 0
handle_ccif = 0
handle_ccis = 0
handle_atrf = 0
handle_atrs = 0

def OnInit():
    global handle_atrf, handle_atrs, handle_ccif, handle_ccis, overbought_major, overbought_minor, oversold_major, oversold_minor, period_atrf, period_atrs, period_ccif, period_ccis
    period_atrf = (1 if (InpPeriodFastATR < 1) else InpPeriodFastATR)
    period_atrs = (1 if (InpPeriodSlowATR < 1) else InpPeriodSlowATR)
    period_ccif = (1 if (InpPeriodFastCCI < 1) else InpPeriodFastCCI)
    period_ccis = (1 if (InpPeriodSlowCCI < 1) else InpPeriodSlowCCI)
    overbought_major = InpOverboughtMajor
    oversold_major = InpOversoldMajor
    overbought_minor = ((overbought_major - 1) if (InpOverboughtMinor >= overbought_major) else InpOverboughtMinor)
    oversold_minor = ((oversold_major + 1) if (InpOversoldMinor <= oversold_major) else InpOversoldMinor)
    SetIndexBuffer(0, BufferFast, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSlow, INDICATOR_DATA)
    SetIndexBuffer(2, BufferATRF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferATRS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferCCIF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferCCIS, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Weighted CCI')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought_major)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, overbought_minor)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold_major)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, oversold_minor)
    ArraySetAsSeries(BufferFast, True)
    ArraySetAsSeries(BufferSlow, True)
    ArraySetAsSeries(BufferATRF, True)
    ArraySetAsSeries(BufferATRS, True)
    ArraySetAsSeries(BufferCCIF, True)
    ArraySetAsSeries(BufferCCIS, True)
    ResetLastError()
    handle_atrf = iATR(None, PERIOD_CURRENT, period_atrf)
    if handle_atrf == INVALID_HANDLE:
        Print('The iATR(', _str(period_atrf), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_atrs = iATR(None, PERIOD_CURRENT, period_atrs)
    if handle_atrs == INVALID_HANDLE:
        Print('The iATR(', _str(period_atrs), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ccif = iCCI(None, PERIOD_CURRENT, period_ccif, InpAppliedPrice)
    if handle_ccif == INVALID_HANDLE:
        Print('The iCCI(', _str(period_ccif), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ccis = iCCI(None, PERIOD_CURRENT, period_ccis, InpAppliedPrice)
    if handle_ccis == INVALID_HANDLE:
        Print('The iCCI(', _str(period_ccis), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferFast, EMPTY_VALUE)
        ArrayInitialize(BufferSlow, EMPTY_VALUE)
        ArrayInitialize(BufferATRF, 0)
        ArrayInitialize(BufferATRS, 0)
        ArrayInitialize(BufferCCIF, 0)
        ArrayInitialize(BufferCCIS, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_atrf, 0, 0, count, BufferATRF)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atrs, 0, 0, count, BufferATRS)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ccif, 0, 0, count, BufferCCIF)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ccis, 0, 0, count, BufferCCIS)
    if copied != count:
        return 0
    Kw = 0.0
    F = 0.0
    S = 0.0
    for i in range(limit, 0 - 1, -1):
        if InpWeight != 0:
            ATR1 = BufferATRF[i]
            ATR2 = BufferATRS[i]
            if ATR2 != 0:
                Kw = _fdiv(InpWeight * ATR1, ATR2)
                F = Kw * BufferCCIF[i]
                S = Kw * BufferCCIS[i]
            else:
                F = 0.0
                S = 0.0
        else:
            F = BufferCCIF[i]
            S = BufferCCIS[i]
        BufferFast[i] = fmax(fmin(F, overbought_major + 50), oversold_major - 50)
        BufferSlow[i] = fmax(fmin(S, overbought_major + 50), oversold_major - 50)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WCCI(_MQL5Indicator):
    name = 'WCCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastCCI': 7,  # CCI Fast period
        'InpPeriodSlowCCI': 14,  # CCI Slow period
        'InpWeight': 1,  # Weight
        'InpPeriodFastATR': 7,  # ATR Fast period
        'InpPeriodSlowATR': 50,  # ATR Slow period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverboughtMajor': 200,  # Overbought max
        'InpOverboughtMinor': 50,  # Overbought
        'InpOversoldMinor': -50,  # Oversold
        'InpOversoldMajor': -200,  # Oversold min
    }

