"""OBV (extended) — converted from MQL5: MQL5 Indicators/OBV (extended)/OBV (extended).mq5

Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 8}, 'colors': {1: [13165000], 2: [12903679], 3: [12632256, 7451452, 3329330, 36095, 42495]}, 'widths': {3: 2}, 'styles': {}, 'labels': {1: 'Uper DC', 2: 'Lower DC', 3: 'OBV'}, 'levels': [], 'description': [], 'name': 'OBV (extended)', 'source': 'MQL5 Indicators/OBV (extended)/OBV (extended).mq5', 'folder': 'OBV (extended)', 'inputs': [{'mql': 'inpVolumeType', 'py': 'inpVolumeType', 'param': 'inpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}, {'mql': 'inpDcPeriod', 'py': 'inpDcPeriod', 'param': 'inpDcPeriod', 'type': 'uint', 'default': 50, 'label': 'Donchian channel period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVolumeType = _input('inpVolumeType', VOLUME_TICK)  # Volumes
inpDcPeriod = _input('inpDcPeriod', 50)  # Donchian channel period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
dcuph = Arr(0, 0.0)
dcupl = Arr(0, 0.0)
dcdnh = Arr(0, 0.0)
dcdnl = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, dcuph, INDICATOR_DATA)
    SetIndexBuffer(1, dcupl, INDICATOR_DATA)
    SetIndexBuffer(2, dcdnh, INDICATOR_DATA)
    SetIndexBuffer(3, dcdnl, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('OBV (%i)', inpDcPeriod))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(_limit, rates_total):
        _volume = (float(tick_volume[i]) if (inpVolumeType == VOLUME_TICK) else volume[i])
        val[i] = (((val[i - 1] + _volume) if (close[i] > close[i - 1]) else (val[i - 1] - _volume) if (close[i] < close[i - 1]) else val[i - 1]) if (i > 0) else 0)
        if inpDcPeriod > 0:
            _start = _int(i - inpDcPeriod)
            if _start < 0:
                _start = 0
            _max = val[ArrayMaximum(val, _start, inpDcPeriod)]
            _min = val[ArrayMinimum(val, _start, inpDcPeriod)]
            dcuph[i] = _max
            dcupl[i] = _max - ((_max - _min) / 5.0)
            dcdnl[i] = _min
            dcdnh[i] = _min + ((_max - _min) / 5.0)
            valc[i] = (2 if (val[i] > dcuph[i]) else 1 if (val[i] > dcupl[i]) else 4 if (val[i] < dcdnl[i]) else 3 if (val[i] < dcdnh[i]) else 0)
        else:
            dcdnl[i] = EMPTY_VALUE
            dcdnh[i] = dcdnl[i]
            dcupl[i] = dcdnh[i]
            dcuph[i] = dcupl[i]
            valc[i] = (1 if (val[i] > 0) else 3 if (val[i] < 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OBVExtended(_MQL5Indicator):
    name = 'OBV (extended)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
        'inpDcPeriod': 50,  # Donchian channel period
    }

