"""Directional volatility & volume_0 — converted from MQL5: MQL5 Indicators/Directional volatility & volume oscillator/Directional volatility & volume_0.mq5

Copyright: Copyright 2021, PuguForex; Link: https://www.mql5.com/en/users/puguforex; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2021, PuguForex', 'link': 'https://www.mql5.com/en/users/puguforex', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 15, 'indicator_plots': 5}, 'types': {1: 10, 2: 8, 3: 11, 4: 1, 5: 1}, 'colors': {1: [8388608, 3937500], 2: [3329330, 9639167], 3: [16776960, 65535], 4: [12632256], 5: [12632256]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Volatility', 2: 'Volatility slope', 3: 'Volume', 4: 'Zone up', 5: 'Zone down'}, 'levels': [], 'description': [], 'name': 'Directional volatility & volume_0', 'source': 'MQL5 Indicators/Directional volatility & volume oscillator/Directional volatility & volume_0.mq5', 'folder': 'Directional volatility & volume oscillator', 'inputs': [{'mql': 'inpVolatilityPeriod', 'py': 'inpVolatilityPeriod', 'param': 'inpVolatilityPeriod', 'type': 'int', 'default': 5, 'label': 'Volatility period', 'sinput': False}, {'mql': 'inpVolatilityMethod', 'py': 'inpVolatilityMethod', 'param': 'inpVolatilityMethod', 'type': 'int', 'default': 0, 'label': 'Volatility method', 'sinput': False}, {'mql': 'inpVolumePeriod', 'py': 'inpVolumePeriod', 'param': 'inpVolumePeriod', 'type': 'int', 'default': 14, 'label': 'Volume period', 'sinput': False}, {'mql': 'inpVolumeMethod', 'py': 'inpVolumeMethod', 'param': 'inpVolumeMethod', 'type': 'int', 'default': 0, 'label': 'Volume method', 'sinput': False}, {'mql': 'inpZonePeriod', 'py': 'inpZonePeriod', 'param': 'inpZonePeriod', 'type': 'int', 'default': 14, 'label': 'Zone period', 'sinput': False}, {'mql': 'inpZoneMethod', 'py': 'inpZoneMethod', 'param': 'inpZoneMethod', 'type': 'int', 'default': 0, 'label': 'Zone method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
inpVolatilityPeriod = _input('inpVolatilityPeriod', 5)  # Volatility period
inpVolatilityMethod = _input('inpVolatilityMethod', MODE_SMA)  # Volatility method
inpVolumePeriod = _input('inpVolumePeriod', 14)  # Volume period
inpVolumeMethod = _input('inpVolumeMethod', MODE_SMA)  # Volume method
inpZonePeriod = _input('inpZonePeriod', 14)  # Zone period
inpZoneMethod = _input('inpZoneMethod', MODE_SMA)  # Zone method
vola = Arr(0, 0.0)
volacl = Arr(0, 0.0)
vlsl = Arr(0, 0.0)
vlslcl = Arr(0, 0.0)
volu = Arr(0, 0.0)
vold = Arr(0, 0.0)
volucl = Arr(0, 0.0)
znup = Arr(0, 0.0)
zndn = Arr(0, 0.0)
zl = Arr(0, 0.0)
cl = Arr(0, 0.0)
hi = Arr(0, 0.0)
lo = Arr(0, 0.0)
vl = Arr(0, 0.0)
vlsm = Arr(0, 0.0)
mdHandle = 0
clHandle = 0
hiHandle = 0
loHandle = 0

def OnInit():
    global clHandle, hiHandle, loHandle, mdHandle
    SetIndexBuffer(0, vola, INDICATOR_DATA)
    SetIndexBuffer(1, volacl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vlsl, INDICATOR_DATA)
    SetIndexBuffer(3, vlslcl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, volu, INDICATOR_DATA)
    SetIndexBuffer(5, vold, INDICATOR_DATA)
    SetIndexBuffer(6, volucl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, znup, INDICATOR_DATA)
    SetIndexBuffer(8, zndn, INDICATOR_DATA)
    SetIndexBuffer(9, zl, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, cl, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, hi, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, lo, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, vl, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, vlsm, INDICATOR_CALCULATIONS)
    mdHandle = iMA(Symbol(), Period(), inpZonePeriod, 0, inpZoneMethod, PRICE_MEDIAN)
    clHandle = iMA(Symbol(), Period(), inpVolatilityPeriod, 0, inpVolatilityMethod, PRICE_CLOSE)
    hiHandle = iMA(Symbol(), Period(), inpZonePeriod, 0, inpZoneMethod, PRICE_HIGH)
    loHandle = iMA(Symbol(), Period(), inpZonePeriod, 0, inpZoneMethod, PRICE_LOW)
    if ((mdHandle == INVALID_HANDLE or clHandle == INVALID_HANDLE) or hiHandle == INVALID_HANDLE) or loHandle == INVALID_HANDLE:
        Print('Failed to create all handles, Try again')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if mdHandle != INVALID_HANDLE:
        IndicatorRelease(mdHandle)
    if clHandle != INVALID_HANDLE:
        IndicatorRelease(clHandle)
    if hiHandle != INVALID_HANDLE:
        IndicatorRelease(hiHandle)
    if loHandle != INVALID_HANDLE:
        IndicatorRelease(loHandle)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    tocopy = ((rates_total - prev_calculated + 1) if prev_calculated else rates_total)
    if ((CopyBuffer(mdHandle, MAIN_LINE, 0, tocopy, zl) != tocopy or CopyBuffer(clHandle, MAIN_LINE, 0, tocopy, cl) != tocopy) or CopyBuffer(hiHandle, MAIN_LINE, 0, tocopy, hi) != tocopy) or CopyBuffer(loHandle, MAIN_LINE, 0, tocopy, lo) != tocopy:
        return prev_calculated
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(limit, rates_total):
        vola[i] = cl[i] - zl[i]
        volacl[i] = (0 if (vola[i] > 0) else 1 if (vola[i] < 0) else volacl[i - 1] if (i > 0) else 0)
        vlsl[i] = vola[i]
        vlslcl[i] = ((0 if (vlsl[i] > vlsl[i - 1]) else 1 if (vlsl[i] < vlsl[i - 1]) else vlslcl[i - 1]) if (i > 0) else 0)
        znup[i] = hi[i] - zl[i]
        zndn[i] = lo[i] - zl[i]
        volu[i] = znup[i]
        vold[i] = zndn[i]
        vl[i] = (float(tick_volume[i]) if (close[i] > open[i]) else (-float(tick_volume[i])) if (close[i] < open[i]) else 0)
        _sw1 = inpVolumeMethod
        if _sw1 == MODE_SMA:
            vlsm[i] = SimpleMA(i, inpVolumePeriod, vl)
        elif _sw1 == MODE_EMA:
            vlsm[i] = ExponentialMA(i, inpVolumePeriod, (vlsm[i - 1] if (i > 0) else vl[i]), vl)
        elif _sw1 == MODE_SMMA:
            vlsm[i] = SmoothedMA(i, inpVolumePeriod, (vlsm[i - 1] if (i > 0) else vl[i]), vl)
        elif _sw1 == MODE_LWMA:
            vlsm[i] = LinearWeightedMA(i, inpVolumePeriod, vl)
        else:
            vlsm[i] = vl[i]
        volucl[i] = (0 if (vlsm[i] > 0) else 1 if (vlsm[i] < 0) else volucl[i - 1] if (i > 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DirectionalVolatilityVolume0(_MQL5Indicator):
    name = 'Directional volatility & volume_0'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpVolatilityPeriod': 5,  # Volatility period
        'inpVolatilityMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Volatility method
        'inpVolumePeriod': 14,  # Volume period
        'inpVolumeMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Volume method
        'inpZonePeriod': 14,  # Zone period
        'inpZoneMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Zone method
    }

