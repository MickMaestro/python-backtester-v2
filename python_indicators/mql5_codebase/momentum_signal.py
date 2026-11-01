"""Momentum_Signal — converted from MQL5: MQL5 Indicators/Momentum_Signal/Momentum_Signal.mq5

Momentum Signal oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Momentum', 2: 'Signal'}, 'levels': [], 'description': ['Momentum Signal oscillator'], 'name': 'Momentum_Signal', 'source': 'MQL5 Indicators/Momentum_Signal/Momentum_Signal.mq5', 'folder': 'Momentum_Signal', 'inputs': [{'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 6, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 12, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpPeriodMom', 'py': 'InpPeriodMom', 'param': 'InpPeriodMom', 'type': 'uint', 'default': 7, 'label': 'Momentum period', 'sinput': False}, {'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 7, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpPeriodADX', 'py': 'InpPeriodADX', 'param': 'InpPeriodADX', 'type': 'uint', 'default': 7, 'label': 'ADX period', 'sinput': False}, {'mql': 'InpSubstrSig', 'py': 'InpSubstrSig', 'param': 'InpSubstrSig', 'type': 'double', 'default': -5.0, 'label': 'Signal line offset', 'sinput': False}, {'mql': 'InpSubstrInd', 'py': 'InpSubstrInd', 'param': 'InpSubstrInd', 'type': 'double', 'default': -1.0, 'label': 'Momentum line offset', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodCCI = _input('InpPeriodCCI', 6)  # CCI period
InpPeriodATR = _input('InpPeriodATR', 12)  # ATR period
InpPeriodMom = _input('InpPeriodMom', 7)  # Momentum period
InpPeriodRSI = _input('InpPeriodRSI', 7)  # RSI period
InpPeriodADX = _input('InpPeriodADX', 7)  # ADX period
InpSubstrSig = _input('InpSubstrSig', -5.0)  # Signal line offset
InpSubstrInd = _input('InpSubstrInd', -1.0)  # Momentum line offset
BufferMomentum = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferMom = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferADX = Arr(0, 0.0)
offset_mom = 0.0
offset_sig = 0.0
period_cci = 0
period_atr = 0
period_mom = 0
period_rsi = 0
period_adx = 0
period_max = 0
handle_cci = 0
handle_atr = 0
handle_mom = 0
handle_rsi = 0
handle_adx = 0

def OnInit():
    global handle_adx, handle_atr, handle_cci, handle_mom, handle_rsi, offset_mom, offset_sig, period_adx, period_atr, period_cci, period_max, period_mom, period_rsi
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    period_mom = (1 if (InpPeriodMom < 1) else InpPeriodMom)
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    period_adx = (1 if (InpPeriodADX < 1) else InpPeriodADX)
    period_max = fmax(period_adx, fmax(period_cci, fmax(period_atr, fmax(period_mom, period_rsi))))
    offset_mom = InpSubstrInd
    offset_sig = InpSubstrSig
    SetIndexBuffer(0, BufferMomentum, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCCI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMom, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferADX, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Momentum Signal (CCI:' + _str(period_cci) + ', ATR:' + _str(period_atr) + ', Mom:' + _str(period_mom) + ', RSI:' + _str(period_rsi) + ', ADX:' + _str(period_adx) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferMomentum, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferCCI, True)
    ArraySetAsSeries(BufferATR, True)
    ArraySetAsSeries(BufferMom, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferADX, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_adx = iADX(None, PERIOD_CURRENT, period_adx)
    if handle_adx == INVALID_HANDLE:
        Print('The iADX(', _str(period_adx), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, PRICE_TYPICAL)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') by PRICE_TYPICAL object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mom = iMomentum(None, PERIOD_CURRENT, period_mom, PRICE_TYPICAL)
    if handle_mom == INVALID_HANDLE:
        Print('The iMomentum(', _str(period_mom), ') by PRICE_TYPICAL object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, PRICE_TYPICAL)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi), ') by PRICE_TYPICAL object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferMomentum, 0)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferCCI, 0)
        ArrayInitialize(BufferATR, 0)
        ArrayInitialize(BufferMom, 0)
        ArrayInitialize(BufferRSI, 0)
        ArrayInitialize(BufferADX, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mom, 0, 0, count, BufferMom)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx, MAIN_LINE, 0, count, BufferADX)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        ATR = BufferATR[i]
        ADX = BufferADX[i]
        BufferSignal[i] = ((_fdiv(BufferMom[i], ATR + ADX) - offset_sig) if ((ATR + ADX) != 0) else 0)
        BufferMomentum[i] = ((_fdiv(ATR + BufferCCI[i] + BufferRSI[i], ADX) - offset_mom) if (ADX != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MomentumSignal(_MQL5Indicator):
    name = 'Momentum_Signal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodCCI': 6,  # CCI period
        'InpPeriodATR': 12,  # ATR period
        'InpPeriodMom': 7,  # Momentum period
        'InpPeriodRSI': 7,  # RSI period
        'InpPeriodADX': 7,  # ADX period
        'InpSubstrSig': -5.0,  # Signal line offset
        'InpSubstrInd': -1.0,  # Momentum line offset
    }

