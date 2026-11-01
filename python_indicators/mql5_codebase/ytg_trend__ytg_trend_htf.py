"""ytg_Trend — converted from MQL5: MQL5 Indicators/ytg_Trend_HTF/ytg_Trend.mq5

Индикатор тренда
Copyright: Copyright © 2009, Yuriy Tokman; Link: yuriytokman@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Yuriy Tokman', 'link': 'yuriytokman@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 8721863, 8421504, 8421376, 65280]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'ytg_Trend'}, 'levels': [], 'description': ['Индикатор тренда'], 'name': 'ytg_Trend', 'source': 'MQL5 Indicators/ytg_Trend_HTF/ytg_Trend.mq5', 'folder': 'ytg_Trend_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 16, 'label': 'период расчёта индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 16)  # период расчёта индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Level = 0

def OnInit():
    global Level, min_rates_total
    min_rates_total = _int(Length)
    Level = min_rates_total - 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ytg_Trend(', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Level)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -Level)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    limit = 0
    k = 0
    bar = 0
    rasr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        rasr = _int(Length)
        price = high[bar]
        IndBuffer[bar] = 0.0
        if price > high[bar + 1]:
            k = 1
            while price > high[bar + k]:
                k += 1
                if k > rasr:
                    break
            IndBuffer[bar] = k - 1
        rasr = _int(Length)
        price = low[bar]
        if price < low[bar + 1]:
            k = 1
            while price < low[bar + k]:
                k += 1
                if k > rasr:
                    break
            IndBuffer[bar] = -(k - 1)
        ColorIndBuffer[bar] = 2.0
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > Level:
                ColorIndBuffer[bar] = 4.0
            else:
                ColorIndBuffer[bar] = 3.0
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < (-Level):
                ColorIndBuffer[bar] = 0.0
            else:
                ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YtgTrend(_MQL5Indicator):
    name = 'ytg_Trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 16,  # период расчёта индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

