"""PanPrizMA Sin leverage 72 — converted from MQL5: MQL5 Indicators/Pan PrizMA Sin leverage 72/PanPrizMA Sin leverage 72.mq5

Copyright: Copyright © 2018, Aleksei Panfilov. filpan1@yandex.ru; Link: filpan1@yandex.ru; Version: 1.2

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Aleksei Panfilov. filpan1@yandex.ru', 'link': 'filpan1@yandex.ru', 'version': '1.2', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711680], 2: [17919], 3: [12632256], 4: [17919]}, 'widths': {1: 2, 2: 6, 3: 2, 4: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Line1', 2: 'Line2', 3: 'Line3', 4: 'Line4'}, 'levels': [], 'description': [], 'name': 'PanPrizMA Sin leverage 72', 'source': 'MQL5 Indicators/Pan PrizMA Sin leverage 72/PanPrizMA Sin leverage 72.mq5', 'folder': 'Pan PrizMA Sin leverage 72', 'inputs': [{'mql': 'line_power', 'py': 'line_power', 'param': 'line_power', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'leverage', 'py': 'leverage', 'param': 'leverage', 'type': 'int', 'default': 132, 'label': '', 'sinput': False}, {'mql': 'multiplier', 'py': 'multiplier', 'param': 'multiplier', 'type': 'double', 'default': -2.0, 'label': '', 'sinput': False}, {'mql': 'line4_SHIFT', 'py': 'line4_SHIFT', 'param': 'line4_SHIFT', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'interval', 'py': 'interval', 'param': 'interval', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'StartPoint', 'py': 'StartPoint', 'param': 'StartPoint', 'type': 'int', 'default': 400, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
line_power = _input('line_power', 2)
leverage = _input('leverage', 132)
multiplier = _input('multiplier', -2.0)
line4_SHIFT = _input('line4_SHIFT', 0)
interval = _input('interval', 3)
StartPoint = _input('StartPoint', 400)
a1_Buffer = Arr(0, 0.0)
a2_Buffer = Arr(0, 0.0)
a3_Buffer = Arr(0, 0.0)
a4_Buffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, a1_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, a2_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, a3_Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, a4_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, 119 * interval)
    PlotIndexSetInteger(1, PLOT_SHIFT, -72 * interval)
    PlotIndexSetInteger(2, PLOT_SHIFT, 120 * interval)
    PlotIndexSetInteger(3, PLOT_SHIFT, line4_SHIFT * interval)
    ArraySetAsSeries(a4_Buffer, True)
    ArraySetAsSeries(a3_Buffer, True)
    ArraySetAsSeries(a2_Buffer, True)
    ArraySetAsSeries(a1_Buffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    z = 0
    limit = 0
    ArraySetAsSeries(open, True)
    if prev_calculated == 0:
        limit = rates_total - (StartPoint * interval)
        if limit < 1:
            return 0
        i = rates_total - 1
        for i in range(i, limit - 1, -1):
            a1_Buffer[i] = open[limit]
            a2_Buffer[i] = open[limit]
            a3_Buffer[i] = open[limit]
            a4_Buffer[i] = open[limit]
        else:
            i = _range_end(i, limit - 1, -1)
    else:
        limit = rates_total - prev_calculated
    i = limit
    for i in range(i, 0 - 1, -1):
        a2_Buffer[i] = (open[i] + (5061600 * a2_Buffer[i + (1 * interval)]) - (7489800 * a2_Buffer[i + (2 * interval)]) + (4926624 * a2_Buffer[i + (3 * interval)]) - (1215450 * a2_Buffer[i + (4 * interval)])) / 1282975
        if line_power == 2:
            a3_Buffer[i + (192 * interval)] = a2_Buffer[i]
            if i >= 0:
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a3_Buffer[i + 0 + (z * interval)] = (2.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) - (2.9980964433 * a3_Buffer[i + (2 * interval) + (z * interval)]) + (1 * a3_Buffer[i + (3 * interval) + (z * interval)])
                else:
                    z = _range_end(z, 0 - 1, -1)
            a1_Buffer[i + (192 * interval)] = (a3_Buffer[i + (193 * interval)] - (1.998096443 * a3_Buffer[i + (192 * interval)]) + a3_Buffer[i + (191 * interval)]) / 0.001903557
            if i >= 0:
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a1_Buffer[i + 0 + (z * interval)] = (a3_Buffer[i + (2 * interval) + (z * interval)] - (1.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) + a3_Buffer[i + (0 * interval) + (z * interval)]) / 0.001903557
                else:
                    z = _range_end(z, 0 - 1, -1)
        if line_power == 3:
            a3_Buffer[i + (192 * interval)] = a2_Buffer[i]
            if i >= 0:
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a3_Buffer[i + 0 + (z * interval)] = (3.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) - (5.996192886 * a3_Buffer[i + (2 * interval) + (z * interval)]) + (3.998096443 * a3_Buffer[i + (3 * interval) + (z * interval)]) - (1 * a3_Buffer[i + (4 * interval) + (z * interval)])
                else:
                    z = _range_end(z, 0 - 1, -1)
            a1_Buffer[i + (192 * interval)] = (a3_Buffer[i + (193 * interval)] - (1.998096443 * a3_Buffer[i + (192 * interval)]) + a3_Buffer[i + (191 * interval)]) / 0.001903557
            if i >= 0:
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a1_Buffer[i + 0 + (z * interval)] = (a3_Buffer[i + (2 * interval) + (z * interval)] - (1.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) + a3_Buffer[i + (0 * interval) + (z * interval)]) / 0.001903557
                else:
                    z = _range_end(z, 0 - 1, -1)
        if line_power == 4:
            a3_Buffer[i + (192 * interval)] = a2_Buffer[i]
            if i >= 0:
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a3_Buffer[i + 0 + (z * interval)] = (4.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) - (9.994289329 * a3_Buffer[i + (2 * interval) + (z * interval)]) + (9.994289329 * a3_Buffer[i + (3 * interval) + (z * interval)]) - (4.998096443 * a3_Buffer[i + (4 * interval) + (z * interval)]) + (1 * a3_Buffer[i + (5 * interval) + (z * interval)])
                else:
                    z = _range_end(z, 0 - 1, -1)
            a1_Buffer[i + (192 * interval)] = (a3_Buffer[i + (193 * interval)] - (1.998096443 * a3_Buffer[i + (192 * interval)]) + a3_Buffer[i + (191 * interval)]) / 0.001903557
            if i >= 0:
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a1_Buffer[i + 0 + (z * interval)] = (a3_Buffer[i + (2 * interval) + (z * interval)] - (1.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) + a3_Buffer[i + (0 * interval) + (z * interval)]) / 0.001903557
                else:
                    z = _range_end(z, 0 - 1, -1)
        a4_Buffer[i] = ((a3_Buffer[i + (192 * interval) - (leverage * interval)] - a1_Buffer[i + (192 * interval) - (leverage * interval)]) * multiplier) + a1_Buffer[i + (192 * interval) - (leverage * interval)]
    else:
        i = _range_end(i, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PanPrizMASinLeverage72(_MQL5Indicator):
    name = 'PanPrizMA Sin leverage 72'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'line_power': 2,
        'leverage': 132,
        'multiplier': -2.0,
        'line4_SHIFT': 0,
        'interval': 3,
        'StartPoint': 400,
    }

