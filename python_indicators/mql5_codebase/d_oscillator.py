"""D_Oscillator — converted from MQL5: MQL5 Indicators/D_Oscillator/D_Oscillator.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'D1', 2: 'D2'}, 'levels': [], 'description': [], 'name': 'D_Oscillator', 'source': 'MQL5 Indicators/D_Oscillator/D_Oscillator.mq5', 'folder': 'D_Oscillator', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 13, 'label': 'Period RSI', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 8, 'label': 'D-period', 'sinput': False}, {'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 8, 'label': 'Period CCI', 'sinput': False}, {'mql': 'InpCoeffCCI', 'py': 'InpCoeffCCI', 'param': 'InpCoeffCCI', 'type': 'double', 'default': 0.4, 'label': 'CCI coefficient', 'sinput': False}, {'mql': 'InpSmooth', 'py': 'InpSmooth', 'param': 'InpSmooth', 'type': 'double', 'default': 4.0, 'label': 'Smooth', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 13)  # Period RSI
InpPeriodD = _input('InpPeriodD', 8)  # D-period
InpPeriodCCI = _input('InpPeriodCCI', 8)  # Period CCI
InpCoeffCCI = _input('InpCoeffCCI', 0.4)  # CCI coefficient
InpSmooth = _input('InpSmooth', 4.0)  # Smooth
BufferD1 = Arr(0, 0.0)
BufferD2 = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
period_rsi = 0
period_cci = 0
period_d = 0
coeff_cci = 0.0
smooth = 0.0
sk = 0.0
sk2 = 0.0
handle_rsi = 0
handle_cci = 0

def OnInit():
    global coeff_cci, handle_cci, handle_rsi, period_cci, period_d, period_rsi, sk, sk2, smooth
    period_rsi = (2 if (InpPeriodRSI < 2) else InpPeriodRSI)
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    period_d = (2 if (InpPeriodD < 2) else InpPeriodD)
    coeff_cci = InpCoeffCCI
    smooth = InpSmooth
    sk = _fdiv(2, smooth + 1)
    sk2 = _fdiv(2, (smooth * 0.8) + 1)
    SetIndexBuffer(0, BufferD1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferCCI, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'D Oscillator')
    ArraySetAsSeries(BufferD1, True)
    ArraySetAsSeries(BufferD2, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferCCI, True)
    ResetLastError()
    handle_rsi = iRSI(Symbol(), PERIOD_CURRENT, period_rsi, PRICE_CLOSE)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_cci = iCCI(Symbol(), PERIOD_CURRENT, period_cci, PRICE_TYPICAL)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 5:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferD1, 0)
        ArrayInitialize(BufferD2, 0)
        ArrayInitialize(BufferRSI, 0)
        ArrayInitialize(BufferCCI, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    MaxRSI = 0.0
    MinRSI = 0.0
    StRSI = 0.0
    StCCI = 0.0
    for i in range(limit, 0 - 1, -1):
        if i != limit:
            max_ = ArrayMaximum(BufferRSI, i, period_d)
            min_ = ArrayMinimum(BufferRSI, i, period_d)
            if max_ == WRONG_VALUE or min_ == WRONG_VALUE:
                continue
            MaxRSI = BufferRSI[max_]
            MinRSI = BufferRSI[min_]
            if MaxRSI != MinRSI:
                StRSI = _fdiv((BufferRSI[i] - MinRSI) * 200, MaxRSI - MinRSI) - 100
                StCCI = (coeff_cci * BufferCCI[i]) + ((1 - coeff_cci) * StRSI)
                BufferD1[i] = (sk * StCCI) + ((1 - sk) * BufferD1[i + 1])
                BufferD2[i] = (sk2 * BufferD1[i + 1]) + ((1 - sk2) * BufferD2[i + 1])
            else:
                BufferD1[i] = 0.0
                BufferD2[i] = BufferD1[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DOscillator(_MQL5Indicator):
    name = 'D_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 13,  # Period RSI
        'InpPeriodD': 8,  # D-period
        'InpPeriodCCI': 8,  # Period CCI
        'InpCoeffCCI': 0.4,  # CCI coefficient
        'InpSmooth': 4.0,  # Smooth
    }

