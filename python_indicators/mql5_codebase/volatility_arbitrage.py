"""Volatility_Arbitrage — converted from MQL5: MQL5 Indicators/Volatility_Arbitrage/Volatility_Arbitrage.mq5

Volatility Arbitrage indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'ROC', 2: 'Top', 3: 'Bottom'}, 'levels': [], 'description': ['Volatility Arbitrage indicator'], 'name': 'Volatility_Arbitrage', 'source': 'MQL5 Indicators/Volatility_Arbitrage/Volatility_Arbitrage.mq5', 'folder': 'Volatility_Arbitrage', 'inputs': [{'mql': 'InpPeriodROC', 'py': 'InpPeriodROC', 'param': 'InpPeriodROC', 'type': 'uint', 'default': 1, 'label': 'ROC period', 'sinput': False}, {'mql': 'InpPeriodDev', 'py': 'InpPeriodDev', 'param': 'InpPeriodDev', 'type': 'uint', 'default': 20, 'label': 'Deviation period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 2.0, 'label': 'Deviation multiplier', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodROC = _input('InpPeriodROC', 1)  # ROC period
InpPeriodDev = _input('InpPeriodDev', 20)  # Deviation period
InpMultiplier = _input('InpMultiplier', 2.0)  # Deviation multiplier
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferROC = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
BufferMADevTmp = Arr(0, 0.0)
multiplier = 0.0
period_roc = 0
period_dev = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global handle_ma1, multiplier, period_dev, period_roc
    period_dev = (1 if (InpPeriodDev < 1) else InpPeriodDev)
    period_roc = (1 if (InpPeriodROC < 1) else InpPeriodROC)
    multiplier = InpMultiplier
    SetIndexBuffer(0, BufferROC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMADevTmp, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility Arbitrage (' + _str(period_roc) + ',' + _str(period_dev) + ',' + DoubleToString(multiplier, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferROC, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferDev, True)
    ArraySetAsSeries(BufferMADevTmp, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_dev, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_roc - 1
        ArrayInitialize(BufferROC, EMPTY_VALUE)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferDev, 0)
        ArrayInitialize(BufferMADevTmp, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        Pr1 = BufferMA1[i + period_roc]
        BufferROC[i] = ((100.0 * (_fdiv(BufferMA1[i], Pr1) - 1.0)) if (Pr1 != 0) else 0)
    if StdDevOnArray(rates_total, prev_calculated, 0, period_dev, MODE_SMA, BufferMADevTmp, BufferROC, BufferDev) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferTop[i] = BufferDev[i] * multiplier
        BufferBottom[i] = -1.0 * BufferTop[i]
    return rates_total

def StdDevOnArray(rates_total, prev_calculated, begin, period, method, buffer_ma_tmp, src_array, dest_buffer):
    pos = 0
    if rates_total < period:
        return 0
    as_series_arr = ArrayGetAsSeries(src_array)
    as_series_dev = ArrayGetAsSeries(dest_buffer)
    as_series_ma = ArrayGetAsSeries(buffer_ma_tmp)
    if as_series_arr:
        ArraySetAsSeries(src_array, False)
    if as_series_dev:
        ArraySetAsSeries(dest_buffer, False)
    if as_series_ma:
        ArraySetAsSeries(buffer_ma_tmp, False)
    pos = prev_calculated - 1
    if pos < period:
        pos = period - 1
        ArrayInitialize(dest_buffer, 0.0)
        ArrayInitialize(buffer_ma_tmp, 0.0)
    _sw1 = method
    if _sw1 == MODE_EMA:
        for i in range(pos, rates_total):
            if i == (period - 1):
                buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            else:
                buffer_ma_tmp[i] = ExponentialMA(i, period, buffer_ma_tmp[i - 1], src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    elif _sw1 == MODE_SMMA:
        for i in range(pos, rates_total):
            if i == (period - 1):
                buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            else:
                buffer_ma_tmp[i] = SmoothedMA(i, period, buffer_ma_tmp[i - 1], src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    elif _sw1 == MODE_LWMA:
        for i in range(pos, rates_total):
            buffer_ma_tmp[i] = LinearWeightedMA(i, period, src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    else:
        for i in range(pos, rates_total):
            buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    if as_series_arr:
        ArraySetAsSeries(src_array, True)
    if as_series_dev:
        ArraySetAsSeries(dest_buffer, True)
    if as_series_ma:
        ArraySetAsSeries(buffer_ma_tmp, True)
    return rates_total

def StdDevFunc(price, price_ma, period, position):
    dev = 0.0
    for i in range(0, period):
        dev += pow(price[position - i] - price_ma[position], 2)
    dev = sqrt(_fdiv(dev, period))
    return dev


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityArbitrage(_MQL5Indicator):
    name = 'Volatility_Arbitrage'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodROC': 1,  # ROC period
        'InpPeriodDev': 20,  # Deviation period
        'InpMultiplier': 2.0,  # Deviation multiplier
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

