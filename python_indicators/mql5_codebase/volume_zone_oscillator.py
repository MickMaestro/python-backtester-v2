"""Volume zone oscillator — converted from MQL5: MQL5 Indicators/Volume Zone Oscillator/Volume zone oscillator.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [14474460, 14474460], 2: [11119017, 3329330, 3937500]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Volume zone oscillator'}, 'levels': [], 'description': [], 'name': 'Volume zone oscillator', 'source': 'MQL5 Indicators/Volume Zone Oscillator/Volume zone oscillator.mq5', 'folder': 'Volume Zone Oscillator', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
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
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volume zone oscillator (' + _str(inpPeriod) + ')')
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
        vzoc[i] = (1 if (vzo[i] > 0) else 2 if (vzo[i] < 0) else 0)
        levup[i] = MathMax(vzo[i], 0)
        levdn[i] = MathMin(vzo[i], 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeZoneOscillator(_MQL5Indicator):
    name = 'Volume zone oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
    }

