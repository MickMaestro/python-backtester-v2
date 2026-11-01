"""RSI_Rendiment — converted from MQL5: MQL5 Indicators/RSI_Rendiment/RSI_Rendiment.mq5

RSI Rendiment oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RRSI'}, 'levels': [], 'description': ['RSI Rendiment oscillator'], 'name': 'RSI_Rendiment', 'source': 'MQL5 Indicators/RSI_Rendiment/RSI_Rendiment.mq5', 'folder': 'RSI_Rendiment', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpNormalized', 'py': 'InpNormalized', 'param': 'InpNormalized', 'type': 'int', 'default': 1, 'label': 'Normalized', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 5, 'label': 'Normalization range', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'uint', 'default': 1, 'label': 'Rendiment X', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 14)  # RSI period
InpNormalized = _input('InpNormalized', INPUT_YES)  # Normalized
InpPeriod = _input('InpPeriod', 5)  # Normalization range
InpMultiplier = _input('InpMultiplier', 1)  # Rendiment X
InpOverbought = _input('InpOverbought', 70.0)  # Overbought
InpOversold = _input('InpOversold', 30.0)  # Oversold
BufferRRSI = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
multiplier = 0
period_rsi = 0
range_ = 0
handle_rsi = 0

def OnInit():
    global handle_rsi, multiplier, overbought, oversold, period_rsi, range_
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    range_ = (2 if (InpPeriod < 2) else InpPeriod)
    multiplier = (1 if (InpMultiplier < 1) else InpMultiplier)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferRRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI Rendiment (' + _str(period_rsi) + ',' + _str(range_) + ',' + _str(multiplier) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, ('Overbought' if InpNormalized else ''))
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, ('Oversold' if InpNormalized else ''))
    ArraySetAsSeries(BufferRRSI, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferRAW, True)
    ResetLastError()
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, PRICE_CLOSE)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI (', _str(period_rsi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(range_, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - range_ - 1
        ArrayInitialize(BufferRRSI, EMPTY_VALUE)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferRSI, 0)
    count = (rates_total if (limit > 0) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRAW[i] = ((multiplier * log(_fdiv(close[i], close[i + range_ - 1]))) if (close[i + range_ - 1] != 0) else 0)
        Rendiment = 0.0
        if InpNormalized:
            min_idx = ArrayMinimum(BufferRAW, i, range_)
            max_idx = ArrayMaximum(BufferRAW, i, range_)
            if min_idx == WRONG_VALUE or max_idx == WRONG_VALUE:
                continue
            min_ = BufferRAW[min_idx]
            max_ = BufferRAW[max_idx]
            if (max_ - min_) != 0:
                Rendiment = _fdiv(BufferRAW[i] - min_, max_ - min_) * 100
            else:
                Rendiment = 0.0
        else:
            Rendiment = BufferRAW[i]
        BufferRRSI[i] = (BufferRSI[i] + Rendiment) / 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIRendiment(_MQL5Indicator):
    name = 'RSI_Rendiment'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 14,  # RSI period
        'InpNormalized': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Normalized
        'InpPeriod': 5,  # Normalization range
        'InpMultiplier': 1,  # Rendiment X
        'InpOverbought': 70.0,  # Overbought
        'InpOversold': 30.0,  # Oversold
    }

