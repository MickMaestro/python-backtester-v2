"""vema_wilders_dmi — converted from MQL5: MQL5 Indicators/Volume Weighted Wilder's DMI/vema_wilders_dmi.mq5

Copyright: mladen; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 1}, 'colors': {1: [11861960, 14804223], 2: [3329330], 3: [55295], 4: [12632256]}, 'widths': {2: 2, 3: 2}, 'styles': {2: 0, 3: 0, 4: 2}, 'labels': {1: 'ADX trend', 2: 'ADX', 3: 'ADXR', 4: 'Level'}, 'levels': [], 'description': [], 'name': 'vema_wilders_dmi', 'source': "MQL5 Indicators/Volume Weighted Wilder's DMI/vema_wilders_dmi.mq5", 'folder': "Volume Weighted Wilder's DMI", 'inputs': [{'mql': 'AdxPeriod', 'py': 'AdxPeriod', 'param': 'AdxPeriod', 'type': 'int', 'default': 14, 'label': 'ADX (DMI) period', 'sinput': False}, {'mql': 'AdxLevel', 'py': 'AdxLevel', 'param': 'AdxLevel', 'type': 'double', 'default': 20.0, 'label': 'ADX level', 'sinput': False}, {'mql': 'ShowADX', 'py': 'ShowADX', 'param': 'ShowADX', 'type': 'bool', 'default': True, 'label': 'ADX visible', 'sinput': False}, {'mql': 'ShowADXR', 'py': 'ShowADXR', 'param': 'ShowADXR', 'type': 'bool', 'default': False, 'label': 'ADXR visible', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 1, 'label': 'Volume to use', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enVolume
vol_noVolume = 0
vol_ticks = 1
vol_real = 2
_enum('enVolume', {0: 'vol_noVolume', 1: 'vol_ticks', 2: 'vol_real'})

# ---- inputs and global variables
AdxPeriod = _input('AdxPeriod', 14)  # ADX (DMI) period
AdxLevel = _input('AdxLevel', 20.0)  # ADX level
ShowADX = _input('ShowADX', True)  # ADX visible
ShowADXR = _input('ShowADXR', False)  # ADXR visible
VolumeType = _input('VolumeType', vol_ticks)  # Volume to use
DIp = Arr(0, 0.0)
DIm = Arr(0, 0.0)
ADX = Arr(0, 0.0)
ADXR = Arr(0, 0.0)
Level = Arr(0, 0.0)
averages = Arr(0, 0.0, dims=(9,))

def OnInit():
    SetIndexBuffer(0, DIp, INDICATOR_DATA)
    SetIndexBuffer(1, DIm, INDICATOR_DATA)
    SetIndexBuffer(2, ADX, INDICATOR_DATA)
    SetIndexBuffer(3, ADXR, INDICATOR_DATA)
    SetIndexBuffer(4, Level, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, " VEMA Wilder''s DMI (" + _str(AdxPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ArrayRange(averages, 0) != rates_total:
        ArrayResize(averages, rates_total)
    sf = 1.0 / float(AdxPeriod)
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        currTR = MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])
        DeltaHi = high[i] - high[i - 1]
        DeltaLo = low[i - 1] - low[i]
        plusDM = 0.0
        minusDM = 0.0
        vol = 0.0
        _sw1 = VolumeType
        if _sw1 == vol_ticks:
            vol = float(tick_volume[i])
        elif _sw1 == vol_real:
            vol = float(volume[i])
        else:
            vol = 1.0
        if DeltaHi > DeltaLo and DeltaHi > 0:
            plusDM = DeltaHi
        if DeltaLo > DeltaHi and DeltaLo > 0:
            minusDM = DeltaLo
        averages[i][0] = averages[i - 1][0] + (sf * (vol - averages[i - 1][0]))
        averages[i][1] = averages[i - 1][1] + (sf * ((vol * plusDM) - averages[i - 1][1]))
        averages[i][2] = averages[i - 1][2] + (sf * ((vol * minusDM) - averages[i - 1][2]))
        averages[i][3] = averages[i - 1][3] + (sf * ((vol * currTR) - averages[i - 1][3]))
        averages[i][5] = _fdiv(averages[i][1], MathMax(averages[i][0], 1))
        averages[i][6] = _fdiv(averages[i][2], MathMax(averages[i][0], 1))
        averages[i][7] = _fdiv(averages[i][3], MathMax(averages[i][0], 1))
        Level[i] = AdxLevel
        DIp[i] = 0.0
        DIm[i] = 0.0
        ADX[i] = EMPTY_VALUE
        ADXR[i] = EMPTY_VALUE
        if averages[i][7] > 0:
            DIp[i] = _fdiv(100.0 * averages[i][5], averages[i][7])
            DIm[i] = _fdiv(100.0 * averages[i][6], averages[i][7])
        if ShowADX:
            DX = 0.0
            if (DIp[i] + DIm[i]) > 0:
                DX = _fdiv(100 * MathAbs(DIp[i] - DIm[i]), DIp[i] + DIm[i])
            else:
                DX = 0.0
            averages[i][4] = averages[i - 1][4] + (sf * ((vol * DX) - averages[i - 1][4]))
            averages[i][8] = _fdiv(averages[i][4], MathMax(averages[i][0], 1))
            ADX[i] = averages[i][8]
            if ShowADXR and i >= AdxPeriod:
                ADXR[i] = 0.5 * (ADX[i] + ADX[i - AdxPeriod])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VemaWildersDmi(_MQL5Indicator):
    name = 'vema_wilders_dmi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AdxPeriod': 14,  # ADX (DMI) period
        'AdxLevel': 20.0,  # ADX level
        'ShowADX': True,  # ADX visible
        'ShowADXR': False,  # ADXR visible
        'VolumeType': _Choice({0: 'do not use volume', 1: 'use ticks', 2: 'use real volume'}, default=1),  # Volume to use
    }

