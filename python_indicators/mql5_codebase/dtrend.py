"""dTrend — converted from MQL5: MQL5 Indicators/dTrend_HTF/dTrend.mq5

Copyright: Yuriy Tokman; Link: yuriytokman@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Yuriy Tokman', 'link': 'yuriytokman@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [32768, 65280], 2: [8388736, 16711935]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'dTrend Upper', 2: 'dTrend Lower'}, 'levels': [], 'description': [], 'name': 'dTrend', 'source': 'MQL5 Indicators/dTrend_HTF/dTrend.mq5', 'folder': 'dTrend_HTF', 'inputs': [{'mql': 'Rasrad', 'py': 'Rasrad', 'param': 'Rasrad', 'type': 'uint', 'default': 16, 'label': '', 'sinput': False}, {'mql': 'Level', 'py': 'Level', 'param': 'Level', 'type': 'uint', 'default': 15, 'label': 'уровень срабатывания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Rasrad = _input('Rasrad', 16)
Level = _input('Level', 15)  # уровень срабатывания
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpColorsBuffer = Arr(0, 0.0)
LoColorsBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(Rasrad) + 1
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, UpColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, LowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, LoColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'dTrend(Rasrad=', Rasrad, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Level)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -Level)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    first = 0
    bar = 0
    count = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = high[bar]
        if price > high[bar - 1]:
            count = 1
            while price > high[bar - count]:
                count += 1
                if count > _int(Rasrad):
                    break
            UpperBuffer[bar] = count - 1
        else:
            UpperBuffer[bar] = 0.0
        price = low[bar]
        if price < low[bar - 1]:
            count = 1
            while price < low[bar - count]:
                count += 1
                if count > _int(Rasrad):
                    break
            LowerBuffer[bar] = 1 - count
        else:
            LowerBuffer[bar] = 0.0
        if UpperBuffer[bar] >= Level:
            UpColorsBuffer[bar] = 1.0
        else:
            UpColorsBuffer[bar] = 0.0
        if LowerBuffer[bar] <= (-Level):
            LoColorsBuffer[bar] = 1.0
        else:
            LoColorsBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DTrend(_MQL5Indicator):
    name = 'dTrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Rasrad': 16,
        'Level': 15,  # уровень срабатывания
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

