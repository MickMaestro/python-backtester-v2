"""XVolume_HTF — converted from MQL5: MQL5 Indicators/XVolume_HTF/XVolume_HTF.mq5

Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [8421504, 16760576], 2: [255]}, 'widths': {1: 5, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Volume HTF', 2: 'XVolume HTF'}, 'levels': [], 'description': [], 'name': 'XVolume_HTF', 'source': 'MQL5 Indicators/XVolume_HTF/XVolume_HTF.mq5', 'folder': 'XVolume_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_JJMA = 4
MODE_JurX = 5
MODE_ParMA = 6
MODE_T3 = 7
MODE_VIDYA = 8
MODE_AMA = 9
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_JJMA', 5: 'MODE_JurX', 6: 'MODE_ParMA', 7: 'MODE_T3', 8: 'MODE_VIDYA', 9: 'MODE_AMA'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
XMA_Method = _input('XMA_Method', MODE_SMA)  # метод усреднения
XLength = _input('XLength', 12)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
ReDraw = _input('ReDraw', True)  # Повтор отображения инфомации на пустых барах
min_rates_total = 0
XVolume_Handle = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
IndBuffer1 = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global XVolume_Handle, min_rates_total
    min_rates_total = 3
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора XVolume не может быть меньше периода текущего графика')
        return INIT_FAILED
    XVolume_Handle = iCustom(Symbol(), TimeFrame, 'XVolume', VolumeType, XMA_Method, XLength, XPhase, 0)
    if XVolume_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XVolume')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    SetIndexBuffer(2, IndBuffer1, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer1, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'XVolume HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(XVolume_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    Volume = Arr(1, 0.0, dyn=False)
    XVolume = Arr(1, 0.0, dyn=False)
    Col = Arr(1, 0.0, dyn=False)
    XVolumeTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = EMPTY_VALUE
        ColorIndBuffer[bar] = 1.0
        IndBuffer1[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, XVolumeTime) <= 0:
            return 0
        if time[bar] >= XVolumeTime[0] and time[bar + 1] < XVolumeTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(XVolume_Handle, 0, _DT(time[bar]), 1, Volume) <= 0:
                return 0
            if CopyBuffer(XVolume_Handle, 1, _DT(time[bar]), 1, Col) <= 0:
                return 0
            if CopyBuffer(XVolume_Handle, 2, _DT(time[bar]), 1, XVolume) <= 0:
                return 0
            IndBuffer[bar] = Volume[0]
            ColorIndBuffer[bar] = Col[0]
            IndBuffer1[bar] = XVolume[0]
        if ReDraw:
            if IndBuffer[bar + 1] != EMPTY_VALUE and IndBuffer[bar] == EMPTY_VALUE:
                IndBuffer[bar] = IndBuffer[bar + 1]
                ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
                IndBuffer1[bar] = IndBuffer1[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XVolumeHTF(_MQL5Indicator):
    name = 'XVolume_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 12,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }

