"""Bollinger Bands with pre Band Smoothing — converted from MQL5: MQL5 Indicators/Bollinger Bands with pre outer band smoothing/Bollinger Bands with pre Band Smoothing.mq5

Bollinger Bands with optional outer band smoothing
Copyright: phade; Link: fxcalculator.io; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'phade', 'link': 'fxcalculator.io', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [12632256], 2: [12632256], 3: [12903679]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Bands upper', 2: 'Bands lower', 3: 'Bands middle'}, 'levels': [], 'description': ['Bollinger Bands with optional outer band smoothing'], 'name': 'Bollinger Bands with pre Band Smoothing', 'source': 'MQL5 Indicators/Bollinger Bands with pre outer band smoothing/Bollinger Bands with pre Band Smoothing.mq5', 'folder': 'Bollinger Bands with pre outer band smoothing', 'inputs': [{'mql': 'BB_Period', 'py': 'BB_Period', 'param': 'BB_Period', 'type': 'int', 'default': 20, 'label': 'BB Period', 'sinput': False}, {'mql': 'BB_Deviation', 'py': 'BB_Deviation', 'param': 'BB_Deviation', 'type': 'double', 'default': 2.0, 'label': 'Standard deviation multiplier', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'MA type', 'sinput': False}, {'mql': 'additive_smoothing', 'py': 'additive_smoothing', 'param': 'additive_smoothing', 'type': 'bool', 'default': True, 'label': 'Additive outer band smoothing', 'sinput': False}, {'mql': 'MA_Period_1', 'py': 'MA_Period_1', 'param': 'MA_Period_1', 'type': 'int', 'default': 14, 'label': 'Upper band MA smoothing period', 'sinput': False}, {'mql': 'MA_Period_2', 'py': 'MA_Period_2', 'param': 'MA_Period_2', 'type': 'int', 'default': 14, 'label': 'Lower band MA smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BB_Period = _input('BB_Period', 20)  # BB Period
BB_Deviation = _input('BB_Deviation', 2.0)  # Standard deviation multiplier
ma_method = _input('ma_method', MODE_SMA)  # MA type
additive_smoothing = _input('additive_smoothing', True)  # Additive outer band smoothing
MA_Period_1 = _input('MA_Period_1', 14)  # Upper band MA smoothing period
MA_Period_2 = _input('MA_Period_2', 14)  # Lower band MA smoothing period
BBUpperBuffer = Arr(0, 0.0)
BBLowerBuffer = Arr(0, 0.0)
BBMainBuffer = Arr(0, 0.0)
BBCalcBuffer = Arr(0, 0.0)
ma_buf_a = Arr(0, 0.0)
ma_buf_b = Arr(0, 0.0)
handle = 0
handle_2 = 0
upper = 0
lower = 0

def OnInit():
    global handle, handle_2, lower, upper
    SetIndexBuffer(0, BBUpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BBLowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, BBMainBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, BBCalcBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ma_buf_a, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ma_buf_b, INDICATOR_CALCULATIONS)
    handle = iMA(None, 0, BB_Period, 0, ma_method, PRICE_CLOSE)
    handle_2 = iMA(None, 0, BB_Period, 0, ma_method, PRICE_CLOSE)
    upper = iMA(None, 0, ((BB_Period + MA_Period_1) if additive_smoothing else MA_Period_1), 0, ma_method, PRICE_CLOSE)
    lower = iMA(None, 0, ((BB_Period + MA_Period_2) if additive_smoothing else MA_Period_2), 0, ma_method, PRICE_CLOSE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Bands with outer band smoothing')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    IndicatorRelease(handle)
    IndicatorRelease(handle_2)
    IndicatorRelease(upper)
    IndicatorRelease(lower)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < BB_Period:
        return 0
    calculated = BarsCalculated(handle)
    if calculated < rates_total:
        Print('Not all data of handle is calculated (', calculated, ' bars). Error ', GetLastError())
        return prev_calculated
    calculated = BarsCalculated(handle_2)
    if calculated < rates_total:
        Print('Not all data of handle_2 is calculated (', calculated, ' bars). Error ', GetLastError())
        return prev_calculated
    calculated = BarsCalculated(upper)
    if calculated < rates_total:
        Print('Not all data of upper is calculated (', calculated, ' bars). Error ', GetLastError())
        return prev_calculated
    calculated = BarsCalculated(lower)
    if calculated < rates_total:
        Print('Not all data of lower is calculated (', calculated, ' bars). Error ', GetLastError())
        return prev_calculated
    to_copy = (rates_total if (prev_calculated > rates_total or prev_calculated < 0) else (rates_total - prev_calculated))
    if prev_calculated > 0:
        to_copy += 1
    if False:
        return 0
    if CopyBuffer(handle, 0, 0, to_copy, BBMainBuffer) <= 0:
        Print('Getting main MA failed! Error ', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(handle_2, 0, 0, to_copy, BBCalcBuffer) <= 0:
        Print('Getting calculation MA failed! Error ', GetLastError())
        return prev_calculated
    if False:
        return 0
    if CopyBuffer(upper, 0, 0, to_copy, ma_buf_a) <= 0:
        Print('Getting upper smoothing MA failed! Error ', GetLastError())
        return prev_calculated
    if False:
        return 0
    if CopyBuffer(lower, 0, 0, to_copy, ma_buf_b) <= 0:
        Print('Getting lower smoothing MA failed! Error ', GetLastError())
        return prev_calculated
    limit = (0 if (prev_calculated == 0) else (prev_calculated - 1))
    for i in range(limit, rates_total):
        stdDev = iDeviation(close, BBCalcBuffer, BB_Period, i)
        BBUpperBuffer[i] = ma_buf_a[i] + (BB_Deviation * stdDev)
        BBLowerBuffer[i] = ma_buf_b[i] - (BB_Deviation * stdDev)
    return rates_total

def iDeviation(price, ma_price, period, pos):
    dSum = 0.0
    i = 0
    while i < period and pos >= 0:
        index = pos - i
        if (index >= 0 and index < ArraySize(price)) and index < ArraySize(ma_price):
            dSum += MathPow(price[index] - ma_price[pos], 2)
        i += 1
    return MathSqrt(_fdiv(dSum, period))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerBandsWithPreBandSmoothing(_MQL5Indicator):
    name = 'Bollinger Bands with pre Band Smoothing'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BB_Period': 20,  # BB Period
        'BB_Deviation': 2.0,  # Standard deviation multiplier
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA type
        'additive_smoothing': True,  # Additive outer band smoothing
        'MA_Period_1': 14,  # Upper band MA smoothing period
        'MA_Period_2': 14,  # Lower band MA smoothing period
    }

