"""Directional_Volatility — converted from MQL5: MQL5 Indicators/Directional_Volatility/Directional_Volatility.mq5

Directional Volatility indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'VShort', 2: 'VLong'}, 'levels': [], 'description': ['Directional Volatility indicator'], 'name': 'Directional_Volatility', 'source': 'MQL5 Indicators/Directional_Volatility/Directional_Volatility.mq5', 'folder': 'Directional_Volatility', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'uint', 'default': 3, 'label': 'Deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpDeviation = _input('InpDeviation', 3)  # Deviation
BufferShort = Arr(0, 0.0)
BufferLong = Arr(0, 0.0)
BufferShortS = Arr(0, 0.0)
BufferLongS = Arr(0, 0.0)
BufferShortMA = Arr(0, 0.0)
BufferLongMA = Arr(0, 0.0)
BufferShortDev = Arr(0, 0.0)
BufferLongDev = Arr(0, 0.0)
BufferMADevTmp = Arr(0, 0.0)
deviation = 0.0
period_sm = 0

def OnInit():
    global deviation, period_sm
    period_sm = (2 if (InpPeriod < 2) else InpPeriod)
    deviation = InpDeviation
    SetIndexBuffer(0, BufferShort, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLong, INDICATOR_DATA)
    SetIndexBuffer(2, BufferShortS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferLongS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferShortMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferLongMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferShortDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferLongDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMADevTmp, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Directional Volatility (' + _str(period_sm) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferShort, True)
    ArraySetAsSeries(BufferLong, True)
    ArraySetAsSeries(BufferShortS, True)
    ArraySetAsSeries(BufferLongS, True)
    ArraySetAsSeries(BufferShortMA, True)
    ArraySetAsSeries(BufferLongMA, True)
    ArraySetAsSeries(BufferShortDev, True)
    ArraySetAsSeries(BufferLongDev, True)
    ArraySetAsSeries(BufferMADevTmp, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_sm, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferShort, EMPTY_VALUE)
        ArrayInitialize(BufferLong, 0)
        ArrayInitialize(BufferShortS, 0)
        ArrayInitialize(BufferLongS, 0)
        ArrayInitialize(BufferShortMA, 0)
        ArrayInitialize(BufferLongMA, 0)
        ArrayInitialize(BufferShortDev, 0)
        ArrayInitialize(BufferLongDev, 0)
        ArrayInitialize(BufferMADevTmp, 0)
    for i in range(limit, 0 - 1, -1):
        BufferShortS[i] = close[i + 1] - low[i]
        BufferLongS[i] = high[i] - close[i + 1]
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferShortS, BufferShortMA) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferLongS, BufferLongMA) == 0:
        return 0
    if StdDevOnArray(rates_total, prev_calculated, 0, period_sm, MODE_SMA, BufferMADevTmp, BufferShortMA, BufferShortDev) == 0:
        return 0
    if StdDevOnArray(rates_total, prev_calculated, 0, period_sm, MODE_SMA, BufferMADevTmp, BufferLongMA, BufferLongDev) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferShort[i] = _fdiv(BufferShortMA[i] + (deviation * BufferShortDev[i]), Point())
        BufferLong[i] = _fdiv(BufferLongMA[i] + (deviation * BufferLongDev[i]), Point())
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


class DirectionalVolatility(_MQL5Indicator):
    name = 'Directional_Volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpDeviation': 3,  # Deviation
    }

