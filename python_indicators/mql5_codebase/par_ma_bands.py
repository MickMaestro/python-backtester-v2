"""Par_MA_Bands — converted from MQL5: MQL5 Indicators/Par_MA_Bands/Par_MA_Bands.mq5

Parabolic Moving Average with Bands indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [255], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Parabolic MA', 2: 'Upper Band', 3: 'Lower Band'}, 'levels': [], 'description': ['Parabolic Moving Average with Bands indicator'], 'name': 'Par_MA_Bands', 'source': 'MQL5 Indicators/Par_MA_Bands/Par_MA_Bands.mq5', 'folder': 'Par_MA_Bands', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 1.0, 'label': 'Deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpDeviation = _input('InpDeviation', 1.0)  # Deviation
BufferPMA = Arr(0, 0.0)
BufferBandUP = Arr(0, 0.0)
BufferBandDN = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
BufferMADevTmp = Arr(0, 0.0)
sum_x = 0.0
sum_x2 = 0.0
sum_x3 = 0.0
sum_x4 = 0.0
deviation = 0.0
period_pma = 0
handle_ma = 0

def OnInit():
    global deviation, handle_ma, period_pma, sum_x, sum_x2, sum_x3, sum_x4
    deviation = InpDeviation
    period_pma = (3 if (InpPeriod < 3) else InpPeriod)
    sum_x = ((1.0 + period_pma) * period_pma) / 2.0
    sum_x2 = ((1.0 + period_pma) * ((2.0 * period_pma) + 1.0) * period_pma) / 6.0
    sum_x3 = sum_x * sum_x
    sum_x4 = ((1.0 + period_pma) * period_pma * ((2.0 * period_pma) + 1.0) * ((3.0 * period_pma * period_pma) + (3.0 * period_pma) - 1.0)) / 30.0
    SetIndexBuffer(0, BufferPMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBandUP, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBandDN, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMADevTmp, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PMAwB (' + _str(period_pma) + ',' + _str(deviation) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPMA, True)
    ArraySetAsSeries(BufferBandUP, True)
    ArraySetAsSeries(BufferBandDN, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferDev, True)
    ArraySetAsSeries(BufferMADevTmp, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_pma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_pma - 1
        ArrayInitialize(BufferPMA, EMPTY_VALUE)
        ArrayInitialize(BufferBandUP, EMPTY_VALUE)
        ArrayInitialize(BufferBandDN, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferDev, 0)
        ArrayInitialize(BufferMADevTmp, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        sum_y = 0.0
        sum_xy = 0.0
        sum_x2y = 0.0
        for j in range(1, period_pma + 1):
            tmp = BufferMA[i + period_pma - j]
            sum_y += tmp
            sum_xy += tmp * j
            sum_x2y += tmp * j * j
        F = sum_x3
        M = sum_x4
        P = sum_y
        R = sum_xy
        S = sum_x2y
        E = sum_x2
        L = sum_x3
        Q = _fdiv(sum_x, period_pma)
        E -= Q * sum_x
        F -= Q * sum_x2
        R -= Q * P
        Q = _fdiv(sum_x2, period_pma)
        L -= Q * sum_x
        M -= Q * sum_x2
        S -= Q * P
        Q = _fdiv(L, E)
        B2 = _fdiv(S - (R * Q), M - (F * Q))
        B1 = _fdiv(R - (F * B2), E)
        B0 = _fdiv(P - (sum_x * B1) - (sum_x2 * B2), period_pma)
        BufferPMA[i] = B0 + ((B1 + (B2 * period_pma)) * period_pma)
    if StdDevOnArray(rates_total, prev_calculated, 0, period_pma, MODE_SMA, BufferMADevTmp, BufferPMA, BufferDev) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferBandUP[i] = BufferPMA[i] + (BufferDev[i] * deviation)
        BufferBandDN[i] = BufferPMA[i] - (BufferDev[i] * deviation)
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


class ParMABands(_MQL5Indicator):
    name = 'Par_MA_Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpDeviation': 1.0,  # Deviation
    }

