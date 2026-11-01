"""Volume pressure — converted from MQL5: MQL5 Indicators/Accumulated volume pressure/Volume pressure.mq5

Volume pressure
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [14478300, 14474475], 2: [7451452], 3: [17919]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Zone', 2: 'Volume pressure', 3: 'Volume pressure back'}, 'levels': [], 'description': ['Volume pressure'], 'name': 'Volume pressure', 'source': 'MQL5 Indicators/Accumulated volume pressure/Volume pressure.mq5', 'folder': 'Accumulated volume pressure', 'inputs': [{'mql': 'inpVolType', 'py': 'inpVolType', 'param': 'inpVolType', 'type': 'int', 'default': 0, 'label': 'Volume type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enVolType
vol_ticks = 0
vol_real = 1
_enum('enVolType', {0: 'vol_ticks', 1: 'vol_real'})

# ---- inputs and global variables
inpVolType = _input('inpVolType', vol_ticks)  # Volume type
vala = Arr(0, 0.0)
valp = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, vala, INDICATOR_DATA)
    SetIndexBuffer(3, valp, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volume pressure (' + StringSubstr(EnumToString(inpVolType, 'enVolType'), 5) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _diff = _fdiv(close[i] - open[i], Point() * 100)
        _volume = (float(tick_volume[i]) if (inpVolType == vol_ticks) else float(volume[i]))
        filld[i] = (vala[i - 1] if (i > 0) else 0)
        valp[i] = filld[i]
        fillu[i] = valp[i] + (_fdiv(_volume, _diff) if (_diff != 0) else 0)
        vala[i] = fillu[i]
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumePressure(_MQL5Indicator):
    name = 'Volume pressure'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpVolType': _Choice({0: 'Use tick volume', 1: 'Use real volume (if available)'}, default=0),  # Volume type
    }

