"""Volume zone oscillator - fl — converted from MQL5: MQL5 Indicators/Volume Zone Oscillator - Floating Levels/Volume zone oscillator - fl.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [14474460, 14474460], 2: [11119017, 3329330, 3937500]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Volume zone oscillator'}, 'levels': [], 'description': [], 'name': 'Volume zone oscillator - fl', 'source': 'MQL5 Indicators/Volume Zone Oscillator - Floating Levels/Volume zone oscillator - fl.mq5', 'folder': 'Volume Zone Oscillator - Floating Levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpFlLookBack', 'py': 'inpFlLookBack', 'param': 'inpFlLookBack', 'type': 'int', 'default': 25, 'label': 'Floating levels look back period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up level %', 'sinput': False}, {'mql': 'inpFlLevelDown', 'py': 'inpFlLevelDown', 'param': 'inpFlLevelDown', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpFlLookBack = _input('inpFlLookBack', 25)  # Floating levels look back period
inpFlLevelUp = _input('inpFlLevelUp', 90.0)  # Floating levels up level %
inpFlLevelDown = _input('inpFlLevelDown', 10.0)  # Floating levels down level %
vzo = Arr(0, 0.0)
vzoc = Arr(0, 0.0)
levup = Arr(0, 0.0)
levdn = Arr(0, 0.0)
work = Arr(0, 0.0, dims=(2,))

def OnInit():
    SetIndexBuffer(0, levup, INDICATOR_DATA)
    SetIndexBuffer(1, levdn, INDICATOR_DATA)
    SetIndexBuffer(2, vzo, INDICATOR_DATA)
    SetIndexBuffer(3, vzoc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volume zone oscillator - fl (' + _str(inpPeriod) + ',' + _str(inpFlLookBack) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if ArrayRange(work, 0) != rates_total:
        ArrayResize(work, rates_total)
    alpha = _fdiv(2.0, 1.0 + inpPeriod)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        sign = ((1 if (close[i] > close[i - 1]) else -1 if (close[i] < close[i - 1]) else 0) if (i > 0) else 0)
        R = sign * tick_volume[i]
        work[i][0] = (R if (i == 0) else (work[i - 1][0] + (alpha * (R - work[i - 1][0]))))
        work[i][1] = (float(tick_volume[i]) if (i == 0) else (work[i - 1][1] + (alpha * (tick_volume[i] - work[i - 1][1]))))
        vzo[i] = (_fdiv(100.0 * work[i][0], work[i][1]) if (work[i][1] != 0) else 0)
        _start = MathMax(i - inpFlLookBack, 0)
        min_ = vzo[ArrayMinimum(vzo, _start, inpFlLookBack)]
        max_ = vzo[ArrayMaximum(vzo, _start, inpFlLookBack)]
        range_ = max_ - min_
        levup[i] = min_ + ((inpFlLevelUp * range_) / 100.0)
        levdn[i] = min_ + ((inpFlLevelDown * range_) / 100.0)
        vzoc[i] = (1 if (vzo[i] > levup[i]) else 2 if (vzo[i] < levdn[i]) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeZoneOscillatorFl(_MQL5Indicator):
    name = 'Volume zone oscillator - fl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpFlLookBack': 25,  # Floating levels look back period
        'inpFlLevelUp': 90.0,  # Floating levels up level %
        'inpFlLevelDown': 10.0,  # Floating levels down level %
    }

