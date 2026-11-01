"""SVSI — converted from MQL5: MQL5 Indicators/SVSI/SVSI.mq5

Slow Volume Strength Index oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SVSI'}, 'levels': [], 'description': ['Slow Volume Strength Index oscillator'], 'name': 'SVSI', 'source': 'MQL5 Indicators/SVSI/SVSI.mq5', 'folder': 'SVSI', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 6, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 14, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpMiddle', 'py': 'InpMiddle', 'param': 'InpMiddle', 'type': 'double', 'default': 50.0, 'label': 'Middle', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 6)  # EMA period
InpPeriodSm = _input('InpPeriodSm', 14)  # Smoothing
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpMiddle = _input('InpMiddle', 50.0)  # Middle
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferSVSI = Arr(0, 0.0)
BufferPos = Arr(0, 0.0)
BufferNeg = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
overbought = 0.0
middle = 0.0
oversold = 0.0
period_ma = 0
period_sm = 0
handle_ma = 0

def OnInit():
    global handle_ma, middle, overbought, oversold, period_ma, period_sm
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_sm = (1 if (InpPeriodSm < 1) else InpPeriodSm)
    middle = (99.9 if (InpMiddle > 99.9) else 0.1 if (InpMiddle < 0.1) else InpMiddle)
    overbought = (100 if (InpOverbought > 100) else (middle + 0.1) if (InpOverbought <= middle) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (middle - 0.1) if (InpOversold >= middle) else InpOversold)
    SetIndexBuffer(0, BufferSVSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPos, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferNeg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Slow Volume Strength Index (' + _str(period_ma) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, middle)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    ArraySetAsSeries(BufferSVSI, True)
    ArraySetAsSeries(BufferPos, True)
    ArraySetAsSeries(BufferNeg, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_sm, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_sm - 1
        ArrayInitialize(BufferSVSI, EMPTY_VALUE)
        ArrayInitialize(BufferPos, 0)
        ArrayInitialize(BufferNeg, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if close[i] > BufferMA[i]:
            BufferPos[i] = tick_volume[i] / 1000000.0
            BufferNeg[i] = 0.0
        elif close[i] < BufferMA[i]:
            BufferNeg[i] = tick_volume[i] / 1000000.0
            BufferPos[i] = 0.0
        else:
            BufferNeg[i] = 0.0
            BufferPos[i] = BufferNeg[i]
    for i in range(limit, 0 - 1, -1):
        AvgPosVol = GetSMA(rates_total, i, period_sm, BufferPos)
        AvgNegVol = GetSMA(rates_total, i, period_sm, BufferNeg)
        svs = (_fdiv(AvgPosVol, AvgNegVol) if (AvgNegVol != 0) else 100.0)
        BufferSVSI[i] = 100.0 - _fdiv(100.0, 1.0 + svs)
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SVSI(_MQL5Indicator):
    name = 'SVSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 6,  # EMA period
        'InpPeriodSm': 14,  # Smoothing
        'InpOverbought': 80.0,  # Overbought
        'InpMiddle': 50.0,  # Middle
        'InpOversold': 20.0,  # Oversold
    }

