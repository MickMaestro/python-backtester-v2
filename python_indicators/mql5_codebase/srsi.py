"""SRSI — converted from MQL5: MQL5 Indicators/SRSI/SRSI.mq5

Slow Relative Strength Index oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2237106]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SRSI'}, 'levels': [], 'description': ['Slow Relative Strength Index oscillator'], 'name': 'SRSI', 'source': 'MQL5 Indicators/SRSI/SRSI.mq5', 'folder': 'SRSI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 8, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 5, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpMiddle', 'py': 'InpMiddle', 'param': 'InpMiddle', 'type': 'double', 'default': 50.0, 'label': 'Middle level', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 8)  # Period
InpPeriodSm = _input('InpPeriodSm', 5)  # Smoothing
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpMiddle = _input('InpMiddle', 50.0)  # Middle level
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferSRSI = Arr(0, 0.0)
BufferNetChgAvg = Arr(0, 0.0)
BufferTotChgAvg = Arr(0, 0.0)
BufferEMA = Arr(0, 0.0)
overbought = 0.0
middle = 0.0
oversold = 0.0
sf = 0.0
period = 0
period_ema = 0
handle_ma = 0

def OnInit():
    global handle_ma, middle, overbought, oversold, period, period_ema, sf
    period = (1 if (InpPeriod < 1) else InpPeriod)
    period_ema = (1 if (InpPeriodSm < 1) else InpPeriodSm)
    sf = _fdiv(1.0, float(period))
    overbought = (100 if (InpOverbought > 100) else 0.2 if (InpOverbought < 0.2) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.2) if (InpOversold >= overbought) else InpOversold)
    middle = ((oversold + 0.1) if (InpMiddle <= oversold) else (overbought - 0.1) if (InpOversold >= overbought) else InpMiddle)
    SetIndexBuffer(0, BufferSRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferNetChgAvg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferTotChgAvg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferEMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SRSI (' + _str(period) + ',' + _str(period_ema) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, middle)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    ArraySetAsSeries(BufferSRSI, True)
    ArraySetAsSeries(BufferNetChgAvg, True)
    ArraySetAsSeries(BufferTotChgAvg, True)
    ArraySetAsSeries(BufferEMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ema, 0, MODE_EMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferSRSI, EMPTY_VALUE)
        ArrayInitialize(BufferNetChgAvg, 0)
        ArrayInitialize(BufferTotChgAvg, 0)
        ArrayInitialize(BufferEMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferEMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferNetChgAvg[i] = (BufferEMA[i] - BufferEMA[i + 1]) * sf
            BufferTotChgAvg[i] = fabs(BufferEMA[i] - BufferEMA[i + 1])
        else:
            Change = BufferEMA[i] - BufferEMA[i + 1]
            BufferNetChgAvg[i] = BufferNetChgAvg[i + 1] + (sf * (Change - BufferNetChgAvg[i + 1]))
            BufferTotChgAvg[i] = BufferTotChgAvg[i + 1] + (sf * (fabs(Change) - BufferTotChgAvg[i + 1]))
            ChgRatio = (_fdiv(BufferNetChgAvg[i], BufferTotChgAvg[i]) if (BufferTotChgAvg[i] != 0) else 0)
            BufferSRSI[i] = 50.0 * (1.0 + ChgRatio)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SRSI(_MQL5Indicator):
    name = 'SRSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 8,  # Period
        'InpPeriodSm': 5,  # Smoothing
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 80.0,  # Overbought
        'InpMiddle': 50.0,  # Middle level
        'InpOversold': 20.0,  # Oversold
    }

