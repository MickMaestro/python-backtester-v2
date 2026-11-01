"""colorschafftrixtrendcyclecandle — converted from MQL5: MQL5 Indicators/ColorSchaffTriXTrendCycleCandle/colorschafftrixtrendcyclecandle.mq5

ColorSchaffTriXTrendCycleCandle
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1, 'indicator_minimum': -110.0, 'indicator_maximum': 110.0}, 'types': {1: 17}, 'colors': {1: [42495, 8421504, 16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ColorSchaffTriXTrendCycleCandle Open;High;Low;Close'}, 'levels': [], 'description': ['ColorSchaffTriXTrendCycleCandle'], 'name': 'colorschafftrixtrendcyclecandle', 'source': 'MQL5 Indicators/ColorSchaffTriXTrendCycleCandle/colorschafftrixtrendcyclecandle.mq5', 'folder': 'ColorSchaffTriXTrendCycleCandle', 'inputs': [{'mql': 'Fast_TriX', 'py': 'Fast_TriX', 'param': 'Fast_TriX', 'type': 'uint', 'default': 23, 'label': 'Период быстрого TriX', 'sinput': False}, {'mql': 'Slow_TriX', 'py': 'Slow_TriX', 'param': 'Slow_TriX', 'type': 'uint', 'default': 50, 'label': 'Период медленного TriX', 'sinput': False}, {'mql': 'Cycle', 'py': 'Cycle', 'param': 'Cycle', 'type': 'uint', 'default': 10, 'label': 'Период стохастического осциллятора', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 60, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -60, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Fast_TriX = _input('Fast_TriX', 23)  # Период быстрого TriX
Slow_TriX = _input('Slow_TriX', 50)  # Период медленного TriX
Cycle = _input('Cycle', 10)  # Период стохастического осциллятора
HighLevel = _input('HighLevel', 60)
MiddleLevel = _input('MiddleLevel', 0)
LowLevel = _input('LowLevel', -60)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_1 = _int(Fast_TriX)
    min_rates_2 = _int(Slow_TriX)
    min_rates_total = MathMax(min_rates_1, min_rates_2) + _int(Cycle) + 1 + 1
    Ind_Handle[0] = iCustom(None, 0, 'ColorSchaffTriXTrendCycle', Fast_TriX, Slow_TriX, PRICE_OPEN, Cycle, 0, 0, 0)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorSchaffTriXTrendCycle[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iCustom(None, 0, 'ColorSchaffTriXTrendCycle', Fast_TriX, Slow_TriX, PRICE_HIGH, Cycle, 0, 0, 0)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorSchaffTriXTrendCycle[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iCustom(None, 0, 'ColorSchaffTriXTrendCycle', Fast_TriX, Slow_TriX, PRICE_LOW, Cycle, 0, 0, 0)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorSchaffTriXTrendCycle[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iCustom(None, 0, 'ColorSchaffTriXTrendCycle', Fast_TriX, Slow_TriX, PRICE_CLOSE, Cycle, 0, 0, 0)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorSchaffTriXTrendCycle[' + _str(3) + ']!')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    short_name = 'ColorSchaffTriXTrendCycleCandl'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMediumSeaGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(Ind_Handle[0]) < rates_total or BarsCalculated(Ind_Handle[1]) < rates_total) or BarsCalculated(Ind_Handle[2]) < rates_total) or BarsCalculated(Ind_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorschafftrixtrendcyclecandle(_MQL5Indicator):
    name = 'colorschafftrixtrendcyclecandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast_TriX': 23,  # Период быстрого TriX
        'Slow_TriX': 50,  # Период медленного TriX
        'Cycle': 10,  # Период стохастического осциллятора
        'HighLevel': 60,
        'MiddleLevel': 0,
        'LowLevel': -60,
    }
    y_range = (-110.0, 110.0)

