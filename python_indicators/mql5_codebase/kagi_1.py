"""kagi-1 — converted from MQL5: MQL5 Indicators/KAGI-1_HTF/kagi-1.mq5

Copyright: Copyright © 2005, Инструменты трейдера; Link: http://www.traderstools.h15.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Инструменты трейдера', 'link': 'http://www.traderstools.h15.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16711935, 8421376]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'KAGI-1'}, 'levels': [], 'description': [], 'name': 'kagi-1', 'source': 'MQL5 Indicators/KAGI-1_HTF/kagi-1.mq5', 'folder': 'KAGI-1_HTF', 'inputs': [{'mql': 'Percent', 'py': 'Percent', 'param': 'Percent', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Threshold', 'py': 'Threshold', 'param': 'Threshold', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Size', 'py': 'Size', 'param': 'Size', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Percent = _input('Percent', True)
Threshold = _input('Threshold', 1)
Size = _input('Size', 12)
KagiBuffer = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
dThreshold = 0.0
min_rates_total = 0

def OnInit():
    global dThreshold, min_rates_total
    min_rates_total = 2
    dThreshold = _fdiv(Threshold, Point())
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    SetIndexBuffer(2, KagiBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(KagiBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    shortname = 'KAGI-1'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    i = 0
    j = 0
    Ind = 0
    size1 = 0
    Threshold1 = 0
    KagiBuffShift = 0
    ArraySetAsSeries(close, True)
    KagiBuffer[KagiBuffShift] = close[rates_total - 1]
    for bar in range(rates_total - 2, 0 - 1, -1):
        if Percent:
            Threshold1 = _int((close[bar] / 100) * dThreshold)
        else:
            Threshold1 = _int(Threshold)
        if not KagiBuffShift:
            if close[bar] >= (KagiBuffer[KagiBuffShift] + (Threshold1 * Point())):
                KagiBuffShift += 1
                KagiBuffer[KagiBuffShift] = close[bar]
            if close[bar] <= (KagiBuffer[KagiBuffShift] - (Threshold1 * Point())):
                KagiBuffShift += 1
                KagiBuffer[KagiBuffShift] = close[bar]
        if KagiBuffShift > 0:
            if KagiBuffer[KagiBuffShift] > KagiBuffer[KagiBuffShift - 1]:
                if close[bar] > KagiBuffer[KagiBuffShift]:
                    KagiBuffer[KagiBuffShift] = close[bar]
                if close[bar] <= (KagiBuffer[KagiBuffShift] - (Threshold1 * Point())):
                    KagiBuffShift += 1
                    KagiBuffer[KagiBuffShift] = close[bar]
            if KagiBuffer[KagiBuffShift] < KagiBuffer[KagiBuffShift - 1]:
                if close[bar] < KagiBuffer[KagiBuffShift]:
                    KagiBuffer[KagiBuffShift] = close[bar]
                if close[bar] >= (KagiBuffer[KagiBuffShift] + (Threshold1 * Point())):
                    KagiBuffShift += 1
                    KagiBuffer[KagiBuffShift] = close[bar]
    size1 = _int(MathMin(MathMax(3, Size), 50))
    i = rates_total - 1
    for i in range(i, 0 - 1, -1):
        IndBuffer[i] = 0.0
    else:
        i = _range_end(i, 0 - 1, -1)
    i = 0
    for i in range(i, KagiBuffShift + 1):
        j = 0
        for j in range(j, size1):
            barX = MathMin(MathMax(((KagiBuffShift - i) * size1) - j, 0), rates_total - 1)
            IndBuffer[barX] = KagiBuffer[i]
            ColorIndBuffer[barX] = 0.0
        else:
            j = _range_end(j, size1, 1)
    else:
        i = _range_end(i, KagiBuffShift + 1, 1)
    if KagiBuffer[0] < KagiBuffer[1]:
        Ind = 1
    else:
        Ind = 2
    i = 0
    for i in range(i, 2):
        j = 0
        for j in range(j, size1):
            if Ind == 1 or Ind == 2:
                ColorIndBuffer[MathMin(MathMax(((KagiBuffShift - i) * size1) - j, 0), rates_total - 1)] = 1.0
        else:
            j = _range_end(j, size1, 1)
    else:
        i = _range_end(i, 2, 1)
    i = 2
    for i in range(i, KagiBuffShift + 1):
        if (Ind == 2 and KagiBuffer[i] > KagiBuffer[i - 1]) and KagiBuffer[i] > KagiBuffer[i - 2]:
            ColorIndBuffer[MathMin(MathMax(((KagiBuffShift - i) * size1) + 1, 0), rates_total - 1)] = 1.0
            Ind = 1
        if (Ind == 1 and KagiBuffer[i] < KagiBuffer[i - 1]) and KagiBuffer[i] < KagiBuffer[i - 2]:
            ColorIndBuffer[MathMin(MathMax((KagiBuffShift - i) * size1, 0), rates_total - 1)] = 1.0
            Ind = 2
        if Ind == 1:
            j = 0
            for j in range(j, size1):
                ColorIndBuffer[MathMin(MathMax(((KagiBuffShift - i) * size1) - j, 0), rates_total - 1)] = 1.0
            else:
                j = _range_end(j, size1, 1)
    else:
        i = _range_end(i, KagiBuffShift + 1, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Kagi1(_MQL5Indicator):
    name = 'kagi-1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Percent': True,
        'Threshold': 1,
        'Size': 12,
    }

