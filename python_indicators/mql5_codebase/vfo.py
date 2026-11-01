"""VFO — converted from MQL5: MQL5 Indicators/VFO/VFO.mq5

Volume Flow oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [10526303]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VFO'}, 'levels': [], 'description': ['Volume Flow oscillator'], 'name': 'VFO', 'source': 'MQL5 Indicators/VFO/VFO.mq5', 'folder': 'VFO', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 130, 'label': 'Period', 'sinput': False}, {'mql': 'InpCoeff', 'py': 'InpCoeff', 'param': 'InpCoeff', 'type': 'double', 'default': 0.2, 'label': 'Dev Coefficient', 'sinput': False}, {'mql': 'InpCoeffV', 'py': 'InpCoeffV', 'param': 'InpCoeffV', 'type': 'double', 'default': 2.5, 'label': 'Vol Coefficient', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 3, 'label': 'Smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 130)  # Period
InpCoeff = _input('InpCoeff', 0.2)  # Dev Coefficient
InpCoeffV = _input('InpCoeffV', 2.5)  # Vol Coefficient
InpPeriodSm = _input('InpPeriodSm', 3)  # Smoothing period
BufferVFI = Arr(0, 0.0)
BufferVFIRaw = Arr(0, 0.0)
BufferVFIRawAvg = Arr(0, 0.0)
BufferInter = Arr(0, 0.0)
BufferInterDev = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferVolAvg = Arr(0, 0.0)
BufferDirVol = Arr(0, 0.0)
BufferDirVolAvg = Arr(0, 0.0)
BufferMADevTmp = Arr(0, 0.0)
period_ind = 0
period_sm = 0
coeff_v = 0.0

def OnInit():
    global coeff_v, period_ind, period_sm
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    period_sm = (1 if (InpPeriodSm < 1) else InpPeriodSm)
    coeff_v = (0.01 if (InpCoeffV == 0) else InpCoeffV)
    SetIndexBuffer(0, BufferVFI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferVFIRaw, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferVFIRawAvg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferInter, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferInterDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferVolAvg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferDirVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferDirVolAvg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMADevTmp, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VFO (' + _str(period_ind) + ',' + DoubleToString(InpCoeff, 2) + ',' + DoubleToString(coeff_v, 2) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferVFI, True)
    ArraySetAsSeries(BufferVFIRaw, True)
    ArraySetAsSeries(BufferVFIRawAvg, True)
    ArraySetAsSeries(BufferInter, True)
    ArraySetAsSeries(BufferInterDev, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferVolAvg, True)
    ArraySetAsSeries(BufferDirVol, True)
    ArraySetAsSeries(BufferDirVolAvg, True)
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
        ArrayInitialize(BufferVFI, EMPTY_VALUE)
        ArrayInitialize(BufferVFIRaw, 0)
        ArrayInitialize(BufferVFIRawAvg, 0)
        ArrayInitialize(BufferInter, 0)
        ArrayInitialize(BufferInterDev, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferVolAvg, 0)
        ArrayInitialize(BufferDirVol, 0)
        ArrayInitialize(BufferDirVolAvg, 0)
        ArrayInitialize(BufferMADevTmp, 0)
    for i in range(limit, 0 - 1, -1):
        t0 = (high[i] + low[i] + close[i]) / 3.0
        t1 = (high[i + 1] + low[i + 1] + close[i + 1]) / 3.0
        BufferInter[i] = log(t0) - log(t1)
        BufferVol[i] = float(tick_volume[i])
    if StdDevOnArray(rates_total, prev_calculated, 0, 30, MODE_SMA, BufferMADevTmp, BufferInter, BufferInterDev) == 0:
        return 0
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVol, BufferVolAvg) == 0:
        return 0
    VAve = 0.0
    for i in range(limit, 0 - 1, -1):
        VAve = BufferVolAvg[i + 1]
        vmax = VAve * coeff_v
        vinter = BufferInterDev[i]
        cutoff = InpCoeff * vinter * close[i]
        vc = (BufferVol[i] if (BufferVol[i] < vmax) else vmax)
        t0 = (high[i] + low[i] + close[i]) / 3.0
        t1 = (high[i + 1] + low[i + 1] + close[i + 1]) / 3.0
        mf = t0 - t1
        BufferDirVol[i] = (vc if (mf > cutoff) else (-vc) if (mf < (-cutoff)) else 0)
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferDirVol, BufferDirVolAvg) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferVFIRaw[i] = (_fdiv(period_ind * BufferDirVolAvg[i], VAve * Point()) if (VAve != 0) else 0)
    if period_sm > 1:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferVFIRaw, BufferVFIRawAvg) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferVFI[i] = (BufferVFIRawAvg[i] if (period_sm > 1) else BufferVFIRaw[i])
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


class VFO(_MQL5Indicator):
    name = 'VFO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 130,  # Period
        'InpCoeff': 0.2,  # Dev Coefficient
        'InpCoeffV': 2.5,  # Vol Coefficient
        'InpPeriodSm': 3,  # Smoothing period
    }

