"""VWAP_Close — converted from MQL5: MQL5 Indicators/VWAP_Close_HTF/VWAP_Close.mq5

Copyright: Copyright © 2016, STS; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, STS', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13382297]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'VWAP_Close'}, 'levels': [], 'description': [], 'name': 'VWAP_Close', 'source': 'MQL5 Indicators/VWAP_Close_HTF/VWAP_Close.mq5', 'folder': 'VWAP_Close_HTF', 'inputs': [{'mql': 'n', 'py': 'n', 'param': 'n', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
n = _input('n', 2)
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
size = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(n) + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VWAP_Close')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    vol = 0
    sum2 = 0
    limit = 0
    bar = 0
    sum1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    if VolumeType == VOLUME_TICK:
        ArraySetAsSeries(tick_volume, True)
    else:
        ArraySetAsSeries(volume, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        sum1 = 0.0
        sum2 = 0
        for ntmp in range(0, _int(n)):
            if VolumeType == VOLUME_TICK:
                vol = tick_volume[bar + ntmp]
            else:
                vol = volume[bar + ntmp]
            sum1 += close[bar + ntmp] * vol
            sum2 += vol
        if sum2:
            IndBuffer[bar] = _fdiv(sum1, sum2)
        else:
            IndBuffer[bar] = IndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VWAPClose(_MQL5Indicator):
    name = 'VWAP_Close'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'n': 2,
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

