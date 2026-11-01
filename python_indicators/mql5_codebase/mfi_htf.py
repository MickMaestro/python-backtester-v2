"""mfi_htf — converted from MQL5: MQL5 Indicators/MFI_HTF/mfi_htf.mq5

Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 8388736, 8421504, 8421376, 65280]}, 'widths': {1: 5}, 'styles': {1: 0}, 'labels': {1: 'MFI HTF'}, 'levels': [20.0, 0.0, -20.0], 'description': [], 'name': 'mfi_htf', 'source': 'MQL5 Indicators/MFI_HTF/mfi_htf.mq5', 'folder': 'MFI_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 8, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объём', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
Length = _input('Length', 8)  # Период индикатора
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объём
ReDraw = _input('ReDraw', True)  # Повтор отображения инфомации на пустых барах
Init = False
min_rates_total = 0
MFI_Handle = 0
MFIBuffer = Arr(0, 0.0)
ColorMFIBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Init, MFI_Handle, min_rates_total
    min_rates_total = 3
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора iMFI не может быть меньше периода текущего графика')
        Init = False
        return
    MFI_Handle = iMFI(Symbol(), TimeFrame, Length, VolumeType)
    if MFI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора  iMFI')
        Init = False
        return
    SetIndexBuffer(0, MFIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, ' MFI HTF')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MFIBuffer, True)
    SetIndexBuffer(1, ColorMFIBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorMFIBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, ' MFI HTF(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    if BarsCalculated(MFI_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    MFI = Arr(2, 0.0, dyn=False)
    MFITime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        MFIBuffer[bar] = EMPTY_VALUE
        ColorMFIBuffer[bar] = 0.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, MFITime) <= 0:
            return 0
        if time[bar] >= MFITime[0] and time[bar + 1] < MFITime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(MFI_Handle, 0, _DT(time[bar]), 2, MFI) <= 0:
                return 0
            MFIBuffer[bar] = MFI[1] - 50.0
            if MFIBuffer[bar] > 0:
                if MFI[1] > MFI[0]:
                    ColorMFIBuffer[bar] = 4.0
                if MFI[1] < MFI[0]:
                    ColorMFIBuffer[bar] = 3.0
            if MFIBuffer[bar] < 0:
                if MFI[1] < MFI[0]:
                    ColorMFIBuffer[bar] = 0.0
                if MFI[1] > MFI[0]:
                    ColorMFIBuffer[bar] = 1.0
        if ReDraw:
            if MFIBuffer[bar + 1] != EMPTY_VALUE and MFIBuffer[bar] == EMPTY_VALUE:
                MFIBuffer[bar] = MFIBuffer[bar + 1]
                ColorMFIBuffer[bar] = ColorMFIBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MfiHtf(_MQL5Indicator):
    name = 'mfi_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'Length': 8,  # Период индикатора
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объём
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }

