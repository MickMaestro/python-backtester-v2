"""Normalized_Volume_Oscillator — converted from MQL5: MQL5 Indicators/Normalized_Volume_Oscillator_HTF/Normalized_Volume_Oscillator.mq5

Copyright: Copyright © 2008, Vadim Shumiloff; Link: shumiloff@mail.ru; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Vadim Shumiloff', 'link': 'shumiloff@mail.ru', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 16711680, 8388736, 255, 65535]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Normalized_Volume_Oscillator'}, 'levels': [], 'description': [], 'name': 'Normalized_Volume_Oscillator', 'source': 'MQL5 Indicators/Normalized_Volume_Oscillator_HTF/Normalized_Volume_Oscillator.mq5', 'folder': 'Normalized_Volume_Oscillator_HTF', 'inputs': [{'mql': 'VolumePeriod', 'py': 'VolumePeriod', 'param': 'VolumePeriod', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
VolumePeriod = _input('VolumePeriod', 10)
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(VolumePeriod)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Normalized_Volume_Oscillator(', VolumePeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 38.2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 61.8)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, 100.0)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrTeal)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrOrange)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    nvo = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        IndBuffer[bar] = (NormalizedVolume(VolumeType, tick_volume, volume, bar) * 100) - 100
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        nvo = IndBuffer[bar]
        if nvo < 0:
            clr = 0
        else:
            if nvo < 38.2:
                clr = 1
            else:
                if nvo < 61.8:
                    clr = 2
                else:
                    if nvo < 100:
                        clr = 3
                    else:
                        clr = 4
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def NormalizedVolume(type_, Tick_Volume, Volume, index):
    nv = 0.0
    vol = 0.0
    if type_ == VOLUME_TICK:
        for kkk in range(0, _int(VolumePeriod)):
            nv += float(Tick_Volume[index - kkk])
        nv = nv / VolumePeriod
        vol = _fdiv(Tick_Volume[index], nv)
    else:
        for kkk in range(0, _int(VolumePeriod)):
            nv += float(Volume[index - kkk])
        nv = nv / VolumePeriod
        vol = _fdiv(Volume[index], nv)
    return vol


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NormalizedVolumeOscillator(_MQL5Indicator):
    name = 'Normalized_Volume_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'VolumePeriod': 10,
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

