"""WAVE_PM — converted from MQL5: MQL5 Indicators/WAVE_PM/WAVE_PM.mq5

Whistler's Active Volatility Energy - Price Mass indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: tanh
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fast Osc', 2: 'Slow Osc'}, 'levels': [], 'description': ["Whistler's Active Volatility Energy - Price Mass indicator"], 'name': 'WAVE_PM', 'source': 'MQL5 Indicators/WAVE_PM/WAVE_PM.mq5', 'folder': 'WAVE_PM', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 14, 'label': 'Fast bands period', 'sinput': False}, {'mql': 'InpShiftFast', 'py': 'InpShiftFast', 'param': 'InpShiftFast', 'type': 'uint', 'default': 0, 'label': 'Fast bands shift', 'sinput': False}, {'mql': 'InpDevFast', 'py': 'InpDevFast', 'param': 'InpDevFast', 'type': 'double', 'default': 2.2, 'label': 'Fast bands deviation', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 55, 'label': 'Slow bands period', 'sinput': False}, {'mql': 'InpShiftSlow', 'py': 'InpShiftSlow', 'param': 'InpShiftSlow', 'type': 'uint', 'default': 0, 'label': 'Slow bands shift', 'sinput': False}, {'mql': 'InpDevSlow', 'py': 'InpDevSlow', 'param': 'InpDevSlow', 'type': 'double', 'default': 2.2, 'label': 'Slow bands deviation', 'sinput': False}, {'mql': 'InpChars', 'py': 'InpChars', 'param': 'InpChars', 'type': 'uint', 'default': 100, 'label': 'Chars', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 0.8, 'label': 'Extreme top level', 'sinput': False}, {'mql': 'InpLevelTop', 'py': 'InpLevelTop', 'param': 'InpLevelTop', 'type': 'double', 'default': 0.7, 'label': 'Top level', 'sinput': False}, {'mql': 'InpCentral', 'py': 'InpCentral', 'param': 'InpCentral', 'type': 'double', 'default': 0.5, 'label': 'Central level', 'sinput': False}, {'mql': 'InpLevelBottom', 'py': 'InpLevelBottom', 'param': 'InpLevelBottom', 'type': 'double', 'default': 0.3, 'label': 'Bottom level', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 0.2, 'label': 'Extreme bottom level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 14)  # Fast bands period
InpShiftFast = _input('InpShiftFast', 0)  # Fast bands shift
InpDevFast = _input('InpDevFast', 2.2)  # Fast bands deviation
InpPeriodSlow = _input('InpPeriodSlow', 55)  # Slow bands period
InpShiftSlow = _input('InpShiftSlow', 0)  # Slow bands shift
InpDevSlow = _input('InpDevSlow', 2.2)  # Slow bands deviation
InpChars = _input('InpChars', 100)  # Chars
InpOverbought = _input('InpOverbought', 0.8)  # Extreme top level
InpLevelTop = _input('InpLevelTop', 0.7)  # Top level
InpCentral = _input('InpCentral', 0.5)  # Central level
InpLevelBottom = _input('InpLevelBottom', 0.3)  # Bottom level
InpOversold = _input('InpOversold', 0.2)  # Extreme bottom level
BufferFastOsc = Arr(0, 0.0)
BufferSlowOsc = Arr(0, 0.0)
BufferFastDev = Arr(0, 0.0)
BufferFastDev1 = Arr(0, 0.0)
BufferSlowDev = Arr(0, 0.0)
BufferSlowDev1 = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
lev_highest = 0.0
lev_top = 0.0
central = 0.0
lev_bottom = 0.0
lev_lowest = 0.0
dev_fast = 0.0
dev_slow = 0.0
period_fast = 0
shift_fast = 0
period_slow = 0
shift_slow = 0
chars = 0
period_max = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global central, chars, dev_fast, dev_slow, handle_fma, handle_sma, lev_bottom, lev_highest, lev_lowest, lev_top, period_fast, period_max, period_slow, shift_fast, shift_slow
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = (1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    shift_fast = _int(InpShiftFast)
    shift_slow = _int(InpShiftSlow)
    dev_fast = InpDevFast
    dev_slow = InpDevSlow
    chars = (2 if (InpChars < 2) else InpChars)
    period_max = fmax(chars, fmax(period_fast, fmax(period_slow, fmax(shift_fast, shift_slow))))
    lev_highest = (1 if (InpOverbought > 1) else 0.04 if (InpOverbought < 0.04) else InpOverbought)
    lev_top = ((lev_highest - 0.01) if (InpLevelTop >= lev_highest) else 0.03 if (InpLevelTop < 0.03) else InpLevelTop)
    central = ((lev_top - 0.01) if (InpCentral >= lev_top) else 0.02 if (InpCentral < 0.02) else InpCentral)
    lev_bottom = ((central - 0.01) if (InpLevelBottom >= central) else 0.01 if (InpLevelBottom < 0.01) else InpLevelBottom)
    lev_lowest = (0 if (InpOversold < 0) else (lev_bottom - 0.01) if (InpOversold >= lev_bottom) else InpOversold)
    SetIndexBuffer(0, BufferFastOsc, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSlowOsc, INDICATOR_DATA)
    SetIndexBuffer(2, BufferFastDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferFastDev1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSlowDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSlowDev1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WAVE-PM')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, lev_highest)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, lev_top)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, central)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, lev_bottom)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, lev_lowest)
    ArraySetAsSeries(BufferFastOsc, True)
    ArraySetAsSeries(BufferSlowOsc, True)
    ArraySetAsSeries(BufferFastDev, True)
    ArraySetAsSeries(BufferFastDev1, True)
    ArraySetAsSeries(BufferSlowDev, True)
    ArraySetAsSeries(BufferSlowDev1, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fast, 0, MODE_SMA, PRICE_CLOSE)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fast), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_slow, 0, MODE_SMA, PRICE_CLOSE)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_slow), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferFastOsc, EMPTY_VALUE)
        ArrayInitialize(BufferSlowOsc, EMPTY_VALUE)
        ArrayInitialize(BufferFastDev, 0)
        ArrayInitialize(BufferFastDev1, 0)
        ArrayInitialize(BufferSlowDev, 0)
        ArrayInitialize(BufferSlowDev1, 0)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        avg = BufferFMA[i + shift_fast]
        sum_ = 0.0
        temp = 0.0
        for j in range(period_fast - 1, 0 - 1, -1):
            temp = close[i + j] - avg
            sum_ += temp * temp
        BufferFastDev[i] = dev_fast * sqrt(_fdiv(sum_, period_fast))
        BufferFastDev1[i] = pow(_fdiv(BufferFastDev[i], Point()), 2)
        temp = 0.0
        for j in range(chars - 1, 0 - 1, -1):
            temp += BufferFastDev1[i + j]
        temp = sqrt(_fdiv(temp, chars)) * Point()
        if temp != 0:
            temp = _fdiv(BufferFastDev[i], temp)
        BufferFastOsc[i] = _missing('tanh')(temp)
    for i in range(limit, 0 - 1, -1):
        avg = BufferSMA[i + shift_slow]
        sum_ = 0.0
        temp = 0.0
        for j in range(period_slow - 1, 0 - 1, -1):
            temp = close[i + j] - avg
            sum_ += temp * temp
        BufferSlowDev[i] = dev_slow * sqrt(_fdiv(sum_, period_slow))
        BufferSlowDev1[i] = pow(_fdiv(BufferSlowDev[i], Point()), 2)
        temp = 0.0
        for j in range(chars - 1, 0 - 1, -1):
            temp += BufferSlowDev1[i + j]
        temp = sqrt(_fdiv(temp, chars)) * Point()
        if temp != 0:
            temp = _fdiv(BufferSlowDev[i], temp)
        BufferSlowOsc[i] = _missing('tanh')(temp)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WAVEPM(_MQL5Indicator):
    name = 'WAVE_PM'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 14,  # Fast bands period
        'InpShiftFast': 0,  # Fast bands shift
        'InpDevFast': 2.2,  # Fast bands deviation
        'InpPeriodSlow': 55,  # Slow bands period
        'InpShiftSlow': 0,  # Slow bands shift
        'InpDevSlow': 2.2,  # Slow bands deviation
        'InpChars': 100,  # Chars
        'InpOverbought': 0.8,  # Extreme top level
        'InpLevelTop': 0.7,  # Top level
        'InpCentral': 0.5,  # Central level
        'InpLevelBottom': 0.3,  # Bottom level
        'InpOversold': 0.2,  # Extreme bottom level
    }

