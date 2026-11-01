"""xkricandle — converted from MQL5: MQL5 Indicators/XKRICandle/xkricandle.mq5

XKRICandle
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 8421504, 8421376]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XKRI Open;XKRI High;XKRI Low;XKRI Close'}, 'levels': [], 'description': ['XKRICandle'], 'name': 'xkricandle', 'source': 'MQL5 Indicators/XKRICandle/xkricandle.mq5', 'folder': 'XKRICandle', 'inputs': [{'mql': 'XKRIPeriod', 'py': 'XKRIPeriod', 'param': 'XKRIPeriod', 'type': 'int', 'default': 20, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'KRIPeriod', 'py': 'KRIPeriod', 'param': 'KRIPeriod', 'type': 'uint', 'default': 20, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'Ratio', 'py': 'Ratio', 'param': 'Ratio', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 7, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 1.0, 'label': 'Уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -1.0, 'label': 'Уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XKRIPeriod = _input('XKRIPeriod', 20)  # Период усреднения
KRIPeriod = _input('KRIPeriod', 20)  # Период усреднения
MA_Method_ = _input('MA_Method_', MODE_SMA)  # Метод усреднения
Ratio = _input('Ratio', 1.0)
XMA_Method = _input('XMA_Method', MODE_JJMA)  # Метод усреднения
XLength = _input('XLength', 7)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
HighLevel = _input('HighLevel', 1.0)  # Уровень перекупленности
LowLevel = _input('LowLevel', -1.0)  # Уровень перепроданности
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = XKRIPeriod + 1
    PRICE_CLOSE_ = 1
    PRICE_OPEN_ = 2
    PRICE_HIGH_ = 3
    PRICE_LOW_ = 4
    Ind_Handle[0] = iCustom(None, 0, 'XKRI', KRIPeriod, MA_Method_, Ratio, PRICE_OPEN_, XMA_Method, XLength, XPhase, 0, 0, 0)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iXKRI[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iCustom(None, 0, 'XKRI', XKRIPeriod, MA_Method_, Ratio, PRICE_HIGH_, XMA_Method, XLength, XPhase, 0, 0, 0)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iXKRI[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iCustom(None, 0, 'XKRI', XKRIPeriod, MA_Method_, Ratio, PRICE_LOW_, XMA_Method, XLength, XPhase, 0, 0, 0)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iXKRI[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iCustom(None, 0, 'XKRI', XKRIPeriod, MA_Method_, Ratio, PRICE_CLOSE_, XMA_Method, XLength, XPhase, 0, 0, 0)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iXKRI[' + _str(3) + ']!')
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
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'XKRICandle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
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


class Xkricandle(_MQL5Indicator):
    name = 'xkricandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XKRIPeriod': 20,  # Период усреднения
        'KRIPeriod': 20,  # Период усреднения
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Метод усреднения
        'Ratio': 1.0,
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'XLength': 7,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'HighLevel': 1.0,  # Уровень перекупленности
        'LowLevel': -1.0,  # Уровень перепроданности
    }

