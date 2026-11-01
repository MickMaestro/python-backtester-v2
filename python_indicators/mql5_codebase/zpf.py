"""ZPF — converted from MQL5: MQL5 Indicators/ZPF/ZPF.mq5

Zero Point Force indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [3329434, 42495]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: '+ZP Force;-ZP Force'}, 'levels': [], 'description': ['Zero Point Force indicator'], 'name': 'ZPF', 'source': 'MQL5 Indicators/ZPF/ZPF.mq5', 'folder': 'ZPF', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 12, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpMethodFast', 'py': 'InpMethodFast', 'param': 'InpMethodFast', 'type': 'int', 'default': 0, 'label': 'Fast MA method', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 24, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpMethodSlow', 'py': 'InpMethodSlow', 'param': 'InpMethodSlow', 'type': 'int', 'default': 0, 'label': 'Slow MA method', 'sinput': False}, {'mql': 'InpPeriodVol', 'py': 'InpPeriodVol', 'param': 'InpPeriodVol', 'type': 'uint', 'default': 12, 'label': 'Volume smoothing period', 'sinput': False}, {'mql': 'InpMethodVol', 'py': 'InpMethodVol', 'param': 'InpMethodVol', 'type': 'int', 'default': 0, 'label': 'Volume smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 12)  # Fast MA period
InpMethodFast = _input('InpMethodFast', MODE_SMA)  # Fast MA method
InpPeriodSlow = _input('InpPeriodSlow', 24)  # Slow MA period
InpMethodSlow = _input('InpMethodSlow', MODE_SMA)  # Slow MA method
InpPeriodVol = _input('InpPeriodVol', 12)  # Volume smoothing period
InpMethodVol = _input('InpMethodVol', MODE_SMA)  # Volume smoothing method
BufferZPF1 = Arr(0, 0.0)
BufferZPF2 = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferVolAvg = Arr(0, 0.0)
period_fma = 0
period_sma = 0
period_vol = 0
weight_sum = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global handle_fma, handle_sma, period_fma, period_sma, period_vol
    period_fma = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_sma = ((period_fma + 1) if (InpPeriodSlow == period_fma) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_vol = (2 if (InpPeriodVol < 2) else InpPeriodVol)
    SetIndexBuffer(0, BufferZPF1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferZPF2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferVolAvg, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Zero Point Force (' + _str(period_fma) + ',' + _str(period_sma) + ',' + _str(period_vol) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferZPF1, True)
    ArraySetAsSeries(BufferZPF2, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferVolAvg, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fma, 0, InpMethodFast, PRICE_CLOSE)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_sma, 0, InpMethodFast, PRICE_CLOSE)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_sma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferZPF1, EMPTY_VALUE)
        ArrayInitialize(BufferZPF2, EMPTY_VALUE)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferVolAvg, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferVol[i] = float(tick_volume[i])
    _sw1 = InpMethodVol
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_vol, BufferVol, BufferVolAvg) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_vol, BufferVol, BufferVolAvg) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_vol, BufferVol, BufferVolAvg, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_vol, BufferVol, BufferVolAvg) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        zpf = _fdiv(BufferVolAvg[i] * (BufferFMA[i] - BufferSMA[i]), 2.0 * Point())
        BufferZPF1[i] = zpf
        BufferZPF2[i] = -zpf
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZPF(_MQL5Indicator):
    name = 'ZPF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 12,  # Fast MA period
        'InpMethodFast': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Fast MA method
        'InpPeriodSlow': 24,  # Slow MA period
        'InpMethodSlow': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Slow MA method
        'InpPeriodVol': 12,  # Volume smoothing period
        'InpMethodVol': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Volume smoothing method
    }

