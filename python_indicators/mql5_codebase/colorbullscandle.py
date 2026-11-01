"""colorbullscandle — converted from MQL5: MQL5 Indicators/ColorBullsCandle/colorbullscandle.mq5

ColorBullsCandle
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [5737262, 8421504, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['ColorBullsCandle'], 'name': 'colorbullscandle', 'source': 'MQL5 Indicators/ColorBullsCandle/colorbullscandle.mq5', 'folder': 'ColorBullsCandle', 'inputs': [{'mql': 'CandelesColorMode', 'py': 'CandelesColorMode', 'param': 'CandelesColorMode', 'type': 'int', 'default': 4, 'label': 'Алгоритм окраски свеч', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения индикатора', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 12, 'label': 'Глубина усреднения индикатора', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения индикатора', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания итогового индикатора', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания итогового индикатора', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания итогового индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ColorMode
MODE_Candeles = 0
MODE_ColorBullsOpen = 1
MODE_ColorBullsHigh = 2
MODE_ColorBullsLow = 3
MODE_ColorBullsClose = 4
_enum('ColorMode', {0: 'MODE_Candeles', 1: 'MODE_ColorBullsOpen', 2: 'MODE_ColorBullsHigh', 3: 'MODE_ColorBullsLow', 4: 'MODE_ColorBullsClose'})

# ---- inputs and global variables
CandelesColorMode = _input('CandelesColorMode', MODE_ColorBullsClose)  # Алгоритм окраски свеч
MA_Method1 = _input('MA_Method1', MODE_SMA)  # Метод усреднения индикатора
Length1 = _input('Length1', 12)  # Глубина усреднения индикатора
Phase1 = _input('Phase1', 15)  # Параметр усреднения индикатора
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # Метод сглаживания итогового индикатора
Length2 = _input('Length2', 5)  # Глубина сглаживания итогового индикатора
Phase2 = _input('Phase2', 15)  # Параметр сглаживания итогового индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_total += GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total += 1
    Ind_Handle[0] = iCustom(None, 0, 'ColorBulls', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, PRICE_OPEN, 0)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorBulls[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iCustom(None, 0, 'ColorBulls', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, PRICE_HIGH, 0)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorBulls[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iCustom(None, 0, 'ColorBulls', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, PRICE_LOW, 0)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorBulls[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iCustom(None, 0, 'ColorBulls', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, PRICE_CLOSE, 0)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorBulls[' + _str(3) + ']!')
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
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    short_name = 'ColorBullsCandle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
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
    if CopyBuffer(Ind_Handle[3], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[0], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    _sw1 = CandelesColorMode
    if _sw1 == MODE_ColorBullsOpen:
        if CopyBuffer(Ind_Handle[0], 1, 0, to_copy, ExtColorBuffer) <= 0:
            return 0
    elif _sw1 == MODE_ColorBullsHigh:
        if CopyBuffer(Ind_Handle[1], 1, 0, to_copy, ExtColorBuffer) <= 0:
            return 0
    elif _sw1 == MODE_ColorBullsLow:
        if CopyBuffer(Ind_Handle[2], 1, 0, to_copy, ExtColorBuffer) <= 0:
            return 0
    elif _sw1 == MODE_ColorBullsClose:
        if CopyBuffer(Ind_Handle[3], 1, 0, to_copy, ExtColorBuffer) <= 0:
            return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if CandelesColorMode == MODE_Candeles:
            if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
                ExtColorBuffer[bar] = 0.0
            elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
                ExtColorBuffer[bar] = 2.0
            else:
                ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorbullscandle(_MQL5Indicator):
    name = 'colorbullscandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CandelesColorMode': _Choice({0: 'Окраска свеч по Open и Close', 1: 'Окраска свеч по графику индикатора ColorBulls[Open]', 2: 'Окраска свеч по графику индикатора ColorBulls[High]', 3: 'Окраска свеч по графику индикатора ColorBulls[Low]', 4: 'Окраска свеч по графику индикатора ColorBulls[Close]'}, default=4),  # Алгоритм окраски свеч
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения индикатора
        'Length1': 12,  # Глубина усреднения индикатора
        'Phase1': 15,  # Параметр усреднения индикатора
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания итогового индикатора
        'Length2': 5,  # Глубина сглаживания итогового индикатора
        'Phase2': 15,  # Параметр сглаживания итогового индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

