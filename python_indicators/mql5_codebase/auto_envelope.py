"""Auto_Envelope — converted from MQL5: MQL5 Indicators/Auto_Envelope/Auto_Envelope.mq5

Auto Envelope indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [16711680], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'AEnv Top', 2: 'AEnv Central', 3: 'AEnv Bottom'}, 'levels': [], 'description': ['Auto Envelope indicator'], 'name': 'Auto_Envelope', 'source': 'MQL5 Indicators/Auto_Envelope/Auto_Envelope.mq5', 'folder': 'Auto_Envelope', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 22, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpFactor', 'py': 'InpFactor', 'param': 'InpFactor', 'type': 'uint', 'default': 27, 'label': 'Deviation factor', 'sinput': False}, {'mql': 'InpPeriodDev', 'py': 'InpPeriodDev', 'param': 'InpPeriodDev', 'type': 'uint', 'default': 100, 'label': 'Deviation period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 22)  # MA period
InpMethod = _input('InpMethod', MODE_SMA)  # MA method
InpFactor = _input('InpFactor', 27)  # Deviation factor
InpPeriodDev = _input('InpPeriodDev', 100)  # Deviation period
BufferTop = Arr(0, 0.0)
BufferCentral = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferMADevTmp = Arr(0, 0.0)
period_ma = 0
period_dev = 0
factor = 0
handle_ma = 0

def OnInit():
    global factor, handle_ma, period_dev, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    period_dev = (2 if (InpPeriodDev < 2) else InpPeriodDev)
    factor = _int(InpFactor)
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCentral, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMADevTmp, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Auto Envelope (' + _str(period_ma) + ',' + _str(period_dev) + ',' + _str(factor) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferCentral, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferDev, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferMADevTmp, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period_dev, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferCentral, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferDev, 0)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferMADevTmp, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferCentral)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRAW[i] = (_fdiv(2.0 * fmax(fabs(high[i] - BufferCentral[i]), fabs(low[i] - BufferCentral[i])), BufferCentral[i]) if (BufferCentral[i] != 0) else 0)
    if StdDevOnArray(rates_total, prev_calculated, 0, period_dev, MODE_SMA, BufferMADevTmp, BufferRAW, BufferDev) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        StdDev = BufferDev[i]
        Csize = (StdDev * factor) / 10.0
        Channel = Csize * BufferCentral[i]
        BufferTop[i] = BufferCentral[i] + (Channel / 2.0)
        BufferBottom[i] = BufferCentral[i] - (Channel / 2.0)
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


class AutoEnvelope(_MQL5Indicator):
    name = 'Auto_Envelope'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 22,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
        'InpFactor': 27,  # Deviation factor
        'InpPeriodDev': 100,  # Deviation period
    }

