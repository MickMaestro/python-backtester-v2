"""DivergenceBar — converted from MQL5: MQL5 Indicators/DivergenceBar/DivergenceBar.mq5

Copyright: Copyright © 2010, Dmitry Zhebrak aka Necron; Link: www.mqlcoder.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Dmitry Zhebrak aka Necron', 'link': 'www.mqlcoder.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 11}, 'colors': {1: [65280, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'DivergenceBar'}, 'levels': [], 'description': [], 'name': 'DivergenceBar', 'source': 'MQL5 Indicators/DivergenceBar/DivergenceBar.mq5', 'folder': 'DivergenceBar', 'inputs': [{'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 2, 'label': 'метод усреднения цены', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 5, 'label': 'ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SmoothMethod = _input('SmoothMethod', MODE_SMMA)  # метод усреднения цены
IPC = _input('IPC', PRICE_MEDIAN)  # ценовая константа
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_total = 0

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = MathMax(13 + 8, MathMax(8 + 5, 5 + 3)) + 1
    Ind_Handle = iAlligator(Symbol(), Period(), 13, 8, 8, 5, 5, 3, SmoothMethod, IPC)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iAlligator')
        return INIT_FAILED
    SetIndexBuffer(0, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'DivergenceBar'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    clr = 0
    Ind1 = Arr(0, 0.0)
    Ind2 = Arr(0, 0.0)
    Ind3 = Arr(0, 0.0)
    lips = 0.0
    teeth = 0.0
    jaw = 0.0
    up = 0.0
    dn = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, GATORLIPS_LINE, 0, to_copy, Ind1) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, GATORTEETH_LINE, 0, to_copy, Ind2) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, GATORJAW_LINE, 0, to_copy, Ind3) <= 0:
        return 0
    ArraySetAsSeries(Ind1, True)
    ArraySetAsSeries(Ind2, True)
    ArraySetAsSeries(Ind3, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        lips = Ind1[bar]
        teeth = Ind2[bar]
        jaw = Ind3[bar]
        up = MathMax(lips, MathMax(teeth, jaw))
        dn = MathMin(lips, MathMin(teeth, jaw))
        UpBuffer[bar] = low[bar] + ((high[bar] - low[bar]) / 2) + ((high[bar] - low[bar]) / 10)
        DnBuffer[bar] = low[bar] + ((high[bar] - low[bar]) / 2) - ((high[bar] - low[bar]) / 10)
        if (high[bar] > high[bar + 1] and close[bar] < (high[bar] - (0.5 * (high[bar] - low[bar])))) and low[bar] > up:
            clr = 0
        elif (low[bar] < low[bar + 1] and close[bar] > (low[bar] + (0.5 * (high[bar] - low[bar])))) and high[bar] < dn:
            clr = 1
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DivergenceBar(_MQL5Indicator):
    name = 'DivergenceBar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SmoothMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # метод усреднения цены
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # ценовая константа
    }

