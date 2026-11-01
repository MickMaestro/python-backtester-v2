"""FVE — converted from MQL5: MQL5 Indicators/FVE/FVE.mq5

Finite Volume Elements indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'FVE', 2: 'Signal'}, 'levels': [], 'description': ['Finite Volume Elements indicator'], 'name': 'FVE', 'source': 'MQL5 Indicators/FVE/FVE.mq5', 'folder': 'FVE', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 22, 'label': 'FVE period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'FVE method', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 22, 'label': 'Signal line period', 'sinput': False}, {'mql': 'InpMethodSig', 'py': 'InpMethodSig', 'param': 'InpMethodSig', 'type': 'int', 'default': 0, 'label': 'Signal line method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 22)  # FVE period
InpMethod = _input('InpMethod', MODE_SMA)  # FVE method
InpPeriodSig = _input('InpPeriodSig', 22)  # Signal line period
InpMethodSig = _input('InpMethodSig', MODE_SMA)  # Signal line method
BufferFVE = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferIntra = Arr(0, 0.0)
BufferInter = Arr(0, 0.0)
BufferIntraDev = Arr(0, 0.0)
BufferInterDev = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferVE = Arr(0, 0.0)
BufferVolAVG = Arr(0, 0.0)
BufferVEAVG = Arr(0, 0.0)
BufferMADevTmp = Arr(0, 0.0)
period_ma = 0
period_sig = 0
weight_sum = 0

def OnInit():
    global period_ma, period_sig
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    SetIndexBuffer(0, BufferFVE, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferIntra, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferInter, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferIntraDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferInterDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferVE, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferVolAVG, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferVEAVG, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferMADevTmp, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Finite Volume Elements (' + _str(period_ma) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferFVE, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferIntra, True)
    ArraySetAsSeries(BufferInter, True)
    ArraySetAsSeries(BufferIntraDev, True)
    ArraySetAsSeries(BufferInterDev, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferVE, True)
    ArraySetAsSeries(BufferVolAVG, True)
    ArraySetAsSeries(BufferVEAVG, True)
    ArraySetAsSeries(BufferMADevTmp, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferFVE, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferIntra, 0)
        ArrayInitialize(BufferInter, 0)
        ArrayInitialize(BufferIntraDev, 0)
        ArrayInitialize(BufferInterDev, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferVE, 0)
        ArrayInitialize(BufferVolAVG, 0)
        ArrayInitialize(BufferVEAVG, 0)
        ArrayInitialize(BufferMADevTmp, 0)
    for i in range(limit, 0 - 1, -1):
        BufferIntra[i] = log(high[i]) - log(low[i])
        BufferInter[i] = log((high[i] + low[i] + close[i]) / 3.0) - log((high[i + 1] + low[i + 1] + close[i + 1]) / 3.0)
        BufferVol[i] = float(tick_volume[i])
    StdDevOnArray(rates_total, prev_calculated, 0, period_ma, MODE_SMA, BufferMADevTmp, BufferIntra, BufferIntraDev)
    StdDevOnArray(rates_total, prev_calculated, 0, period_ma, MODE_SMA, BufferMADevTmp, BufferInter, BufferInterDev)
    for i in range(limit, 0 - 1, -1):
        Vintra = BufferIntraDev[i]
        Vinter = BufferInterDev[i]
        Cutoff = 0.1 * (Vintra + Vinter) * close[i]
        MF = close[i] - ((high[i] + low[i]) / 2.0) + high[i] + low[i] + close[i] - high[i + 1] - low[i + 1] - close[i + 1]
        v = (1.0 if (MF > Cutoff) else -1 if (MF < (-Cutoff)) else 0)
        BufferVE[i] = v * float(tick_volume[i])
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferVE, BufferVEAVG)
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferVol, BufferVolAVG)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferVol, BufferVolAVG)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ma, BufferVol, BufferVolAVG, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferVol, BufferVolAVG)
    for i in range(limit, 0 - 1, -1):
        BufferFVE[i] = (_fdiv(100.0 * BufferVEAVG[i], BufferVolAVG[i] * Point()) if (BufferVolAVG[i] != 0) else 0)
    _sw2 = InpMethodSig
    if _sw2 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma, period_sig, BufferFVE, BufferSignal)
    elif _sw2 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma, period_sig, BufferFVE, BufferSignal)
    elif _sw2 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma, period_sig, BufferFVE, BufferSignal, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_ma, period_sig, BufferFVE, BufferSignal)
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
    _sw3 = method
    if _sw3 == MODE_EMA:
        for i in range(pos, rates_total):
            if i == (period - 1):
                buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            else:
                buffer_ma_tmp[i] = ExponentialMA(i, period, buffer_ma_tmp[i - 1], src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    elif _sw3 == MODE_SMMA:
        for i in range(pos, rates_total):
            if i == (period - 1):
                buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            else:
                buffer_ma_tmp[i] = SmoothedMA(i, period, buffer_ma_tmp[i - 1], src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    elif _sw3 == MODE_LWMA:
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


class FVE(_MQL5Indicator):
    name = 'FVE'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 22,  # FVE period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # FVE method
        'InpPeriodSig': 22,  # Signal line period
        'InpMethodSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal line method
    }

