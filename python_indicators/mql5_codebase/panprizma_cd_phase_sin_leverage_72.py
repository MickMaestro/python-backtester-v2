"""PanPrizMA CD Phase Sin leverage 72 — converted from MQL5: MQL5 Indicators/Pan PrizMA CD Phase Sin leverage 72/PanPrizMA CD Phase Sin leverage 72.mq5

Copyright: Copyright © 2020, Aleksei Panfilov. filpan1@yandex.ru; Link: https://www.mql5.com/ru/market/product/18845; Version: 1.3

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2020, Aleksei Panfilov. filpan1@yandex.ru', 'link': 'https://www.mql5.com/ru/market/product/18845', 'version': '1.3', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 9}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 8: 3, 5: 1, 6: 1, 7: 1, 9: 1}, 'colors': {1: [16711680], 2: [17919], 3: [12632256], 4: [17919], 8: [12632256], 5: [25600], 6: [255], 7: [25600], 9: [42495]}, 'widths': {1: 2, 2: 6, 3: 2, 4: 3, 8: 1, 5: 2, 6: 2, 7: 1, 9: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 8: 0, 5: 0, 6: 0, 7: 2, 9: 0}, 'labels': {1: 'Line1', 2: 'Line2', 3: 'Line3', 4: 'Line4', 8: 'Line8', 5: 'Line5', 6: 'Line6', 7: 'Line7', 9: 'Line9_Amplitude'}, 'levels': [], 'description': [], 'name': 'PanPrizMA CD Phase Sin leverage 72', 'source': 'MQL5 Indicators/Pan PrizMA CD Phase Sin leverage 72/PanPrizMA CD Phase Sin leverage 72.mq5', 'folder': 'Pan PrizMA CD Phase Sin leverage 72', 'inputs': [{'mql': 'line_power', 'py': 'line_power', 'param': 'line_power', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'leverage', 'py': 'leverage', 'param': 'leverage', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'multiplier', 'py': 'multiplier', 'param': 'multiplier', 'type': 'double', 'default': -2.0, 'label': '', 'sinput': False}, {'mql': 'line4_SHIFT', 'py': 'line4_SHIFT', 'param': 'line4_SHIFT', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'interval', 'py': 'interval', 'param': 'interval', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'StartPoint', 'py': 'StartPoint', 'param': 'StartPoint', 'type': 'int', 'default': 400, 'label': '', 'sinput': False}, {'mql': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 'py': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 'param': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Multiplikator_HISTOGRAM', 'py': 'Multiplikator_HISTOGRAM', 'param': 'Multiplikator_HISTOGRAM', 'type': 'int', 'default': 1000000, 'label': '', 'sinput': False}, {'mql': 'Multiplikator_PRICE', 'py': 'Multiplikator_PRICE', 'param': 'Multiplikator_PRICE', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Multiplikator_Amplitude', 'py': 'Multiplikator_Amplitude', 'param': 'Multiplikator_Amplitude', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Discount_PRICE', 'py': 'Discount_PRICE', 'param': 'Discount_PRICE', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'InpSignalSMA', 'py': 'InpSignalSMA', 'param': 'InpSignalSMA', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
line_power = _input('line_power', 2)
leverage = _input('leverage', 1)
multiplier = _input('multiplier', -2.0)
line4_SHIFT = _input('line4_SHIFT', 0)
interval = _input('interval', 1)
StartPoint = _input('StartPoint', 400)
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX = _input('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 1)
Multiplikator_HISTOGRAM = _input('Multiplikator_HISTOGRAM', 1000000)
Multiplikator_PRICE = _input('Multiplikator_PRICE', 1)
Multiplikator_Amplitude = _input('Multiplikator_Amplitude', 1.0)
Discount_PRICE = _input('Discount_PRICE', 0)
InpSignalSMA = _input('InpSignalSMA', 9)
a1_Buffer = Arr(0, 0.0)
a2_Buffer = Arr(0, 0.0)
a3_Buffer = Arr(0, 0.0)
a4_Buffer = Arr(0, 0.0)
a5_Buffer = Arr(0, 0.0)
a6_Buffer = Arr(0, 0.0)
a7_Buffer = Arr(0, 0.0)
a8_Buffer = Arr(0, 0.0)
a9_Buffer = Arr(0, 0.0)
P = 0.0
O = 0.0
M = 0.0
C = 0.0
H_kv = 0.0
H = 0.0
A = 0.0
K = 0.0
S_ZN = 0.0
S = 0.0
AK = 0.0
AS = 0.0
AK_S = 0.0
AS_S = 0.0

def OnInit():
    SetIndexBuffer(0, a1_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, a2_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, a3_Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, a4_Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, a5_Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, a6_Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, a7_Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, a8_Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, a9_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, 119 * interval)
    PlotIndexSetInteger(1, PLOT_SHIFT, -72 * interval)
    PlotIndexSetInteger(2, PLOT_SHIFT, 120 * interval)
    PlotIndexSetInteger(3, PLOT_SHIFT, line4_SHIFT * interval)
    PlotIndexSetInteger(4, PLOT_SHIFT, 0)
    PlotIndexSetInteger(5, PLOT_SHIFT, 0)
    PlotIndexSetInteger(6, PLOT_SHIFT, 0)
    PlotIndexSetInteger(7, PLOT_SHIFT, 0)
    PlotIndexSetInteger(8, PLOT_SHIFT, 0)
    ArraySetAsSeries(a1_Buffer, True)
    ArraySetAsSeries(a2_Buffer, True)
    ArraySetAsSeries(a3_Buffer, True)
    ArraySetAsSeries(a4_Buffer, True)
    ArraySetAsSeries(a5_Buffer, True)
    ArraySetAsSeries(a6_Buffer, True)
    ArraySetAsSeries(a7_Buffer, True)
    ArraySetAsSeries(a8_Buffer, True)
    ArraySetAsSeries(a9_Buffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global A, AK, AK_S, AS, AS_S, C, H, H_kv, K, M, O, P, S, S_ZN
    i = 0
    z = 0
    limit = 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(time, True)
    if prev_calculated == 0:
        limit = rates_total - (StartPoint * interval)
        if limit < 1:
            return 0
        i = rates_total - 1
        for i in range(i, limit - 1, -1):
            a1_Buffer[i] = open[limit] * Multiplikator_PRICE
            a2_Buffer[i] = open[limit] * Multiplikator_PRICE
            a3_Buffer[i] = open[limit] * Multiplikator_PRICE
            a4_Buffer[i] = open[limit] * Multiplikator_PRICE
            a5_Buffer[i] = open[limit] * Multiplikator_PRICE
            a6_Buffer[i] = open[limit] * Multiplikator_PRICE
            a7_Buffer[i] = open[limit] * Multiplikator_PRICE
            a8_Buffer[i] = open[limit] * Multiplikator_PRICE
            a9_Buffer[i] = open[limit] * Multiplikator_PRICE
        else:
            i = _range_end(i, limit - 1, -1)
    else:
        limit = rates_total - prev_calculated
    i = limit
    for i in range(i, 0 - 1, -1):
        a2_Buffer[i] = ((open[i] * Multiplikator_PRICE) - Discount_PRICE + (5061600 * a2_Buffer[i + (1 * interval)]) - (7489800 * a2_Buffer[i + (2 * interval)]) + (4926624 * a2_Buffer[i + (3 * interval)]) - (1215450 * a2_Buffer[i + (4 * interval)])) / 1282975
        if line_power == 2:
            a3_Buffer[i + (192 * interval)] = a2_Buffer[i]
            if i <= (5000 * interval):
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a3_Buffer[i + 0 + (z * interval)] = (2.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) - (2.9980964433 * a3_Buffer[i + (2 * interval) + (z * interval)]) + (1 * a3_Buffer[i + (3 * interval) + (z * interval)])
                else:
                    z = _range_end(z, 0 - 1, -1)
            a1_Buffer[i + (192 * interval)] = (a3_Buffer[i + (193 * interval)] - (1.998096443 * a3_Buffer[i + (192 * interval)]) + a3_Buffer[i + (191 * interval)]) / 0.001903557
            if i <= (5000 * interval):
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a1_Buffer[i + 0 + (z * interval)] = (a3_Buffer[i + (2 * interval) + (z * interval)] - (1.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) + a3_Buffer[i + (0 * interval) + (z * interval)]) / 0.001903557
                else:
                    z = _range_end(z, 0 - 1, -1)
        if line_power == 3:
            a3_Buffer[i + (192 * interval)] = a2_Buffer[i]
            if i <= (5000 * interval):
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a3_Buffer[i + 0 + (z * interval)] = (3.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) - (5.996192886 * a3_Buffer[i + (2 * interval) + (z * interval)]) + (3.998096443 * a3_Buffer[i + (3 * interval) + (z * interval)]) - (1 * a3_Buffer[i + (4 * interval) + (z * interval)])
                else:
                    z = _range_end(z, 0 - 1, -1)
            a1_Buffer[i + (192 * interval)] = (a3_Buffer[i + (193 * interval)] - (1.998096443 * a3_Buffer[i + (192 * interval)]) + a3_Buffer[i + (191 * interval)]) / 0.001903557
            if i <= (5000 * interval):
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a1_Buffer[i + 0 + (z * interval)] = (a3_Buffer[i + (2 * interval) + (z * interval)] - (1.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) + a3_Buffer[i + (0 * interval) + (z * interval)]) / 0.001903557
                else:
                    z = _range_end(z, 0 - 1, -1)
        if line_power == 4:
            a3_Buffer[i + (192 * interval)] = a2_Buffer[i]
            if i <= (5000 * interval):
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a3_Buffer[i + 0 + (z * interval)] = (4.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) - (9.994289329 * a3_Buffer[i + (2 * interval) + (z * interval)]) + (9.994289329 * a3_Buffer[i + (3 * interval) + (z * interval)]) - (4.998096443 * a3_Buffer[i + (4 * interval) + (z * interval)]) + (1 * a3_Buffer[i + (5 * interval) + (z * interval)])
                else:
                    z = _range_end(z, 0 - 1, -1)
            a1_Buffer[i + (192 * interval)] = (a3_Buffer[i + (193 * interval)] - (1.998096443 * a3_Buffer[i + (192 * interval)]) + a3_Buffer[i + (191 * interval)]) / 0.001903557
            if i <= (5000 * interval):
                z = 192 - 1
                for z in range(z, 0 - 1, -1):
                    a1_Buffer[i + 0 + (z * interval)] = (a3_Buffer[i + (2 * interval) + (z * interval)] - (1.998096443 * a3_Buffer[i + (1 * interval) + (z * interval)]) + a3_Buffer[i + (0 * interval) + (z * interval)]) / 0.001903557
                else:
                    z = _range_end(z, 0 - 1, -1)
        a4_Buffer[i] = ((a3_Buffer[i + (192 * interval) - (leverage * interval)] - a1_Buffer[i + (192 * interval) - (leverage * interval)]) * multiplier) + a1_Buffer[i + (192 * interval) - (leverage * interval)]
        M = a3_Buffer[i + (192 * interval) - (leverage * interval)]
        O = a3_Buffer[i + (191 * interval) - (leverage * interval)]
        P = a3_Buffer[i + (190 * interval) - (leverage * interval)]
        C = a1_Buffer[i + (191 * interval) - (leverage * interval)]
        H_kv = ((O - C) * (O - C)) - ((M - C) * (P - C))
        H = MathPow(H_kv, 0.5)
        A = _fdiv(H / 0.043318753, Point())
        if H_kv > 0 and (P - M) != 0:
            K = _fdiv(P - M, MathPow(H_kv, 0.5) * 2)
        if MathAbs(O - C) > 0:
            S_ZN = _fdiv(O - C, MathAbs(O - C))
        S = MathPow(1 - MathPow(K, 2), 0.5) * S_ZN
        AK = (MathArccos(K) / 3.14159265358979) * 180
        AS = (MathArcsin(K) / 3.14159265358979) * 180
        AK_S = (MathArccos(S) / 3.14159265358979) * 180
        AS_S = (MathArcsin(S) / 3.14159265358979) * 180
        if K > 0 and S < 0:
            a5_Buffer[i] = AS
        if K > 0 and S > 0:
            a5_Buffer[i] = (AS * -1) + 180
        if K < 0 and S > 0:
            a5_Buffer[i] = (AS * -1) + 180
        if K < 0 and S < 0:
            a5_Buffer[i] = AS + 360
        if K > 0 and S < 0:
            a6_Buffer[i] = AS + 180 - 360
        if K > 0 and S > 0:
            a6_Buffer[i] = (AS * -1) + 360 - 360
        if K < 0 and S > 0:
            a6_Buffer[i] = (AS * -1) - 360
        if K < 0 and S < 0:
            a6_Buffer[i] = AS + 180 - 360
        a7_Buffer[i] = AS * 2
        a8_Buffer[i] = (P - M) * Multiplikator_HISTOGRAM
        a9_Buffer[i] = A * Multiplikator_Amplitude
    else:
        i = _range_end(i, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PanPrizMACDPhaseSinLeverage72(_MQL5Indicator):
    name = 'PanPrizMA CD Phase Sin leverage 72'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'line_power': 2,
        'leverage': 1,
        'multiplier': -2.0,
        'line4_SHIFT': 0,
        'interval': 1,
        'StartPoint': 400,
        'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX': 1,
        'Multiplikator_HISTOGRAM': 1000000,
        'Multiplikator_PRICE': 1,
        'Multiplikator_Amplitude': 1.0,
        'Discount_PRICE': 0,
        'InpSignalSMA': 9,
    }

