"""VolMA — converted from MQL5: MQL5 Indicators/Dynamic Moving Average/VolMA.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14772545]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VolMA'}, 'levels': [], 'description': [], 'name': 'VolMA', 'source': 'MQL5 Indicators/Dynamic Moving Average/VolMA.mq5', 'folder': 'Dynamic Moving Average', 'inputs': [{'mql': 'InpRSIVolPeriod', 'py': 'InpRSIVolPeriod', 'param': 'InpRSIVolPeriod', 'type': 'int', 'default': 20, 'label': 'RSI Vol Period', 'sinput': False}, {'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'int', 'default': 50, 'label': 'MA Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Calculated method', 'sinput': False}, {'mql': 'InpPrice', 'py': 'InpPrice', 'param': 'InpPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpRSIVolPeriod = _input('InpRSIVolPeriod', 20)  # RSI Vol Period
InpMAPeriod = _input('InpMAPeriod', 50)  # MA Period
InpMethod = _input('InpMethod', MODE_EMA)  # Calculated method
InpPrice = _input('InpPrice', PRICE_CLOSE)  # Applied price
BufferVolMA = Arr(0, 0.0)
BufferRSIOnArray = Arr(0, 0.0)
BufferRSIPositive = Arr(0, 0.0)
BufferRSINegative = Arr(0, 0.0)
rsi_vol_period = 0
ma_period = 0

def OnInit():
    global ma_period, rsi_vol_period
    SetIndexBuffer(0, BufferVolMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRSIOnArray, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferRSIPositive, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferRSINegative, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VolMA')
    rsi_vol_period = (1 if (InpRSIVolPeriod < 1) else InpRSIVolPeriod)
    ma_period = (1 if (InpMAPeriod < 1) else InpMAPeriod)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(rsi_vol_period, ma_period):
        return 0
    ArraySetAsSeries(BufferVolMA, True)
    ArraySetAsSeries(BufferRSIOnArray, True)
    ArraySetAsSeries(BufferRSIPositive, True)
    ArraySetAsSeries(BufferRSINegative, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - fmax(rsi_vol_period, ma_period) - 1
        ArrayInitialize(BufferVolMA, EMPTY_VALUE)
        ArrayInitialize(BufferRSIOnArray, EMPTY_VALUE)
        ArrayInitialize(BufferRSIPositive, EMPTY_VALUE)
        ArrayInitialize(BufferRSINegative, EMPTY_VALUE)
    RSIOnArray(rates_total, prev_calculated, 0, rsi_vol_period, tick_volume, BufferRSIPositive, BufferRSINegative, BufferRSIOnArray)
    for i in range(limit, 0 - 1, -1):
        PeriodMA = (BufferRSIOnArray[i] * ma_period) / 100
        PeriodMA = fmax(PeriodMA, 1)
        ma = GetMA(_int(PeriodMA), InpMethod, InpPrice, i)
        if ma == WRONG_VALUE:
            return 0
        BufferVolMA[i] = ma
    return rates_total

def RSIOnArray(rates_total, prev_calculated, begin, period, price, buffer_pos, buffer_neg, buffer_rsi):
    i = 0
    diff = 0
    if period < 1 or (rates_total - begin) < period:
        return 0
    as_series_price = ArrayGetAsSeries(price)
    as_series_rsi = ArrayGetAsSeries(buffer_rsi)
    if as_series_price:
        ArraySetAsSeries(price, False)
    if as_series_rsi:
        ArraySetAsSeries(buffer_rsi, False)
        ArraySetAsSeries(buffer_pos, False)
        ArraySetAsSeries(buffer_neg, False)
    pos = prev_calculated - 1
    if pos <= period:
        buffer_rsi[0] = 0.0
        buffer_pos[0] = 0.0
        buffer_neg[0] = 0.0
        SumP = 0.0
        SumN = 0.0
        i = 1
        for i in range(i, period + 1):
            buffer_rsi[i] = 0.0
            buffer_pos[i] = 0.0
            buffer_neg[i] = 0.0
            diff = price[i] - price[i - 1]
            SumP += (diff if (diff > 0) else 0)
            SumN += ((-diff) if (diff < 0) else 0)
        else:
            i = _range_end(i, period + 1, 1)
        buffer_pos[period] = _fdiv(SumP, period)
        buffer_neg[period] = _fdiv(SumN, period)
        buffer_rsi[period] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(buffer_pos[period], (buffer_neg[period] if (buffer_neg[period] > 0) else DBL_MIN)))
        pos = period + 1
    i = pos
    for i in range(i, rates_total):
        diff = price[i] - price[i - 1]
        buffer_pos[i] = _fdiv((buffer_pos[i - 1] * (period - 1)) + (diff if (diff > 0.0) else 0.0), period)
        buffer_neg[i] = _fdiv((buffer_neg[i - 1] * (period - 1)) + ((-diff) if (diff < 0.0) else 0.0), period)
        buffer_rsi[i] = 100.0 - _fdiv(100.0, 1 + _fdiv(buffer_pos[i], (buffer_neg[i] if (buffer_neg[i] > 0) else DBL_MIN)))
    else:
        i = _range_end(i, rates_total, 1)
    if as_series_price:
        ArraySetAsSeries(price, True)
    if as_series_rsi:
        ArraySetAsSeries(buffer_rsi, True)
        ArraySetAsSeries(buffer_pos, True)
        ArraySetAsSeries(buffer_neg, True)
    return rates_total

def GetMA(period, method, price, shift):
    array = Arr(0, 0.0)
    handle = iMA(None, PERIOD_CURRENT, period, 0, method, price)
    ResetLastError()
    if handle == INVALID_HANDLE:
        Print('Error creating MA handle ', GetLastError())
        return WRONG_VALUE
    if CopyBuffer(handle, 0, shift, 1, array) == 1:
        return array[0]
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolMA(_MQL5Indicator):
    name = 'VolMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpRSIVolPeriod': 20,  # RSI Vol Period
        'InpMAPeriod': 50,  # MA Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Calculated method
        'InpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

