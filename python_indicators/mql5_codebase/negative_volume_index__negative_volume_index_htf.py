"""negative_volume_index — converted from MQL5: MQL5 Indicators/Negative_Volume_Index_HTF/negative_volume_index.mq5

Индекс отрицательного объема (Negative Volume Index - NVI)
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Negative Volume Index'}, 'levels': [], 'description': ['Индекс отрицательного объема (Negative Volume Index - NVI)'], 'name': 'negative_volume_index', 'source': 'MQL5 Indicators/Negative_Volume_Index_HTF/negative_volume_index.mq5', 'folder': 'Negative_Volume_Index_HTF', 'inputs': [{'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объем', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
VolumeType = _input('VolumeType', VOLUME_TICK)  # объем
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
NVIBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, NVIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Negative Volume Index')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 2:
        return 0
    first = 0
    bar = 0
    Vol0 = 0
    Vol1 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        NVIBuffer[0] = 1.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if VolumeType == VOLUME_TICK:
            Vol0 = tick_volume[bar]
            Vol1 = tick_volume[bar - 1]
        else:
            Vol0 = volume[bar]
            Vol1 = volume[bar - 1]
        if Vol0 < Vol1:
            NVIBuffer[bar] = NVIBuffer[bar - 1] * (1 + _fdiv(close[bar] - close[bar - 1], close[bar - 1]))
        else:
            NVIBuffer[bar] = NVIBuffer[bar - 1]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NegativeVolumeIndex(_MQL5Indicator):
    name = 'negative_volume_index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объем
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

