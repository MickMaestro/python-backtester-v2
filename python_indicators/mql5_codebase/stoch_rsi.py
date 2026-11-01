"""Stoch RSI — converted from MQL5: MQL5 Indicators/Stoch RSI MT5/Stoch RSI.mq5

Fully Coded By Hossein Nouri
Email : hsn.nouri@gmail.com
Skype : hsn.nouri
Telegram : @hypernova1990
Website : http://www.metatraderprogrammer.ir
MQL5 Profile : https://www.mql5.com/en/users/hsnnouri
 
Feel free to contact me for MQL4/MQL5 coding.
Copyright: Copyright 2020, Hossein Nouri; Link: https://www.mql5.com/en/users/hsnnouri; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Hossein Nouri', 'link': 'https://www.mql5.com/en/users/hsnnouri', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'K', 2: 'D'}, 'levels': [20.0, 80.0], 'description': ['Fully Coded By Hossein Nouri', 'Email : hsn.nouri@gmail.com', 'Skype : hsn.nouri', 'Telegram : @hypernova1990', 'Website : http://www.metatraderprogrammer.ir', 'MQL5 Profile : https://www.mql5.com/en/users/hsnnouri', ' ', 'Feel free to contact me for MQL4/MQL5 coding.'], 'name': 'Stoch RSI', 'source': 'MQL5 Indicators/Stoch RSI MT5/Stoch RSI.mq5', 'folder': 'Stoch RSI MT5', 'inputs': [{'mql': 'InpStockKPeriod', 'py': 'InpStockKPeriod', 'param': 'InpStockKPeriod', 'type': 'int', 'default': 3, 'label': 'K', 'sinput': False}, {'mql': 'InpStockDPeriod', 'py': 'InpStockDPeriod', 'param': 'InpStockDPeriod', 'type': 'int', 'default': 3, 'label': 'D', 'sinput': False}, {'mql': 'InpRSIPeriod', 'py': 'InpRSIPeriod', 'param': 'InpRSIPeriod', 'type': 'int', 'default': 14, 'label': 'RSI Period', 'sinput': False}, {'mql': 'InpStochastikPeriod', 'py': 'InpStochastikPeriod', 'param': 'InpStochastikPeriod', 'type': 'int', 'default': 14, 'label': 'Stochastic Period', 'sinput': False}, {'mql': 'InpRSIAppliedPrice', 'py': 'InpRSIAppliedPrice', 'param': 'InpRSIAppliedPrice', 'type': 'int', 'default': 1, 'label': 'RSI Applied Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpStockKPeriod = _input('InpStockKPeriod', 3)  # K
InpStockDPeriod = _input('InpStockDPeriod', 3)  # D
InpRSIPeriod = _input('InpRSIPeriod', 14)  # RSI Period
InpStochastikPeriod = _input('InpStochastikPeriod', 14)  # Stochastic Period
InpRSIAppliedPrice = _input('InpRSIAppliedPrice', PRICE_CLOSE)  # RSI Applied Price
KBuffer = Arr(0, 0.0)
DBuffer = Arr(0, 0.0)
RSIBuffer = Arr(0, 0.0)
StochBuffer = Arr(0, 0.0)
RSIHandle = 0

def OnInit():
    global RSIHandle
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, KBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, RSIBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, StochBuffer, INDICATOR_CALCULATIONS)
    RSIHandle = iRSI(Symbol(), Period(), InpRSIPeriod, InpRSIAppliedPrice)
    ArraySetAsSeries(KBuffer, True)
    ArraySetAsSeries(DBuffer, True)
    ArraySetAsSeries(RSIBuffer, True)
    ArraySetAsSeries(StochBuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    calculated = BarsCalculated(RSIHandle)
    if calculated < rates_total:
        Print('Not all data of RSIHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(RSIHandle, 0, 0, to_copy, RSIBuffer) <= 0:
        Print('Getting RSIBuffer is failed! Error', GetLastError())
        return 0
    limit = ((rates_total - (InpRSIPeriod + 1)) if (prev_calculated == 0) else (rates_total - prev_calculated + 1))
    for i in range(limit, 0 - 1, -1):
        if i < (rates_total - (InpRSIPeriod + 2)):
            StochBuffer[i] = Stoch(RSIBuffer, RSIBuffer, RSIBuffer, InpStochastikPeriod, i, rates_total)
        if StochBuffer[i + InpStockKPeriod - 1] != EMPTY_VALUE:
            KBuffer[i] = SimpleMA(i, InpStockKPeriod, StochBuffer, rates_total)
        if KBuffer[i + InpStockDPeriod - 1] != EMPTY_VALUE:
            DBuffer[i] = SimpleMA(i, InpStockDPeriod, KBuffer, rates_total)
    return rates_total

def Stoch(source, high, low, length, shift, rates_total):
    if (shift + length) > rates_total:
        return EMPTY_VALUE
    Highest_ = Highest(high, length, shift)
    Lowest_ = Lowest(low, length, shift)
    if (Highest_ - Lowest_) == 0:
        return EMPTY_VALUE
    return _fdiv(100 * (source[shift] - Lowest_), Highest_ - Lowest_)

def Lowest(low, length, shift):
    Result = 0.0
    for i in range(shift, shift + length + 1):
        if Result == 0 or (low[i] < Result and low[i] != EMPTY_VALUE):
            Result = low[i]
    return Result

def Highest(high, length, shift):
    Result = 0.0
    for i in range(shift, shift + length + 1):
        if Result == 0 or (high[i] > Result and high[i] != EMPTY_VALUE):
            Result = high[i]
    return Result

def SimpleMA(position, period, price, rates_total):
    result = 0.0
    if position <= (rates_total - period) and period > 0:
        for i in range(0, period):
            if price[position + i] != EMPTY_VALUE:
                result += price[position + i]
        result = _fdiv(result, period)
    return result


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochRSI(_MQL5Indicator):
    name = 'Stoch RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStockKPeriod': 3,  # K
        'InpStockDPeriod': 3,  # D
        'InpRSIPeriod': 14,  # RSI Period
        'InpStochastikPeriod': 14,  # Stochastic Period
        'InpRSIAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI Applied Price
    }
    y_range = (0.0, 100.0)

