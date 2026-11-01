"""Delta_RSI — converted from MQL5: MQL5 Indicators/Delta_RSI/Delta_RSI.mq5

Copyright: Copyright 2016, Tor; Link: http://einvestor.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, Tor', 'link': 'http://einvestor.ru/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 8421504, 16711935]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'Delta_RSI'}, 'levels': [], 'description': [], 'name': 'Delta_RSI', 'source': 'MQL5 Indicators/Delta_RSI/Delta_RSI.mq5', 'folder': 'Delta_RSI', 'inputs': [{'mql': 'TypeGr', 'py': 'TypeGr', 'param': 'TypeGr', 'type': 'int', 'default': 0, 'label': 'Type graph', 'sinput': False}, {'mql': 'RSIPeriod1', 'py': 'RSIPeriod1', 'param': 'RSIPeriod1', 'type': 'uint', 'default': 14, 'label': 'Fast RSI Period', 'sinput': False}, {'mql': 'RSIPrice1', 'py': 'RSIPrice1', 'param': 'RSIPrice1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSIPeriod2', 'py': 'RSIPeriod2', 'param': 'RSIPeriod2', 'type': 'uint', 'default': 50, 'label': 'Slow RSI Period', 'sinput': False}, {'mql': 'RSIPrice2', 'py': 'RSIPrice2', 'param': 'RSIPrice2', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Level', 'py': 'Level', 'param': 'Level', 'type': 'uint', 'default': 50, 'label': 'Signal Level', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum TypeGraph
Histogram = 0
Cute = 1
_enum('TypeGraph', {0: 'Histogram', 1: 'Cute'})

# ---- inputs and global variables
TypeGr = _input('TypeGr', Histogram)  # Type graph
RSIPeriod1 = _input('RSIPeriod1', 14)  # Fast RSI Period
RSIPrice1 = _input('RSIPrice1', PRICE_CLOSE)
RSIPeriod2 = _input('RSIPeriod2', 50)  # Slow RSI Period
RSIPrice2 = _input('RSIPrice2', PRICE_CLOSE)
Level = _input('Level', 50)  # Signal Level
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
rsi1 = Arr(0, 0.0)
rsi2 = Arr(0, 0.0)
delta = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Ind1_Handle = 0
Ind2_Handle = 0
min_rates_total = 0
maxLevel = 0
minLevel = 0

def OnInit():
    global Ind1_Handle, Ind2_Handle, maxLevel, minLevel, min_rates_total
    Ind1_Handle = iRSI(Symbol(), PERIOD_CURRENT, RSIPeriod1, RSIPrice1)
    if Ind1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора RSI 1')
        return INIT_FAILED
    Ind2_Handle = iRSI(Symbol(), PERIOD_CURRENT, RSIPeriod2, RSIPrice2)
    if Ind2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора RSI 2')
        return INIT_FAILED
    min_rates_total = _int(MathMax(RSIPeriod1, RSIPeriod2))
    maxLevel = _int(100 - (100 - Level))
    minLevel = _int(100 - Level)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, rsi1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, rsi2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, delta, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(IndBuffer, True)
    ArraySetAsSeries(ColorIndBuffer, True)
    ArraySetAsSeries(rsi1, True)
    ArraySetAsSeries(rsi2, True)
    ArraySetAsSeries(delta, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Delta_RSI(', RSIPeriod1, ',', RSIPeriod2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Ind1_Handle) < rates_total or BarsCalculated(Ind2_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind1_Handle, 0, 0, to_copy, rsi1) <= 0:
        return 0
    if CopyBuffer(Ind2_Handle, 0, 0, to_copy, rsi2) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        delta[bar] = rsi1[bar] - rsi2[bar]
        if TypeGr == Cute:
            IndBuffer[bar] = 1.0
        else:
            IndBuffer[bar] = delta[bar]
        clr = 1
        if rsi2[bar] > maxLevel and rsi1[bar] > rsi2[bar]:
            clr = 0
        if rsi2[bar] < minLevel and rsi1[bar] < rsi2[bar]:
            clr = 2
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DeltaRSI(_MQL5Indicator):
    name = 'Delta_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TypeGr': _Choice({0: 'Full Histogram', 1: 'Cute Histogram'}, default=0),  # Type graph
        'RSIPeriod1': 14,  # Fast RSI Period
        'RSIPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSIPeriod2': 50,  # Slow RSI Period
        'RSIPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Level': 50,  # Signal Level
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

