"""xdidi_index_cloud_htf — converted from MQL5: MQL5 Indicators/XDidi_Index_HTF/xdidi_index_cloud_htf.mq5

XDidi_Index с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16748574, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XDidi_Index_HTF'}, 'levels': [1.0], 'description': ['XDidi_Index с возможностью изменения таймфрейма во входных параметрах'], 'name': 'xdidi_index_cloud_htf', 'source': 'MQL5 Indicators/XDidi_Index_HTF/xdidi_index_cloud_htf.mq5', 'folder': 'XDidi_Index_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Curta_Method', 'py': 'Curta_Method', 'param': 'Curta_Method', 'type': 'int', 'default': 0, 'label': 'Curta метод усреднения', 'sinput': False}, {'mql': 'Curta', 'py': 'Curta', 'param': 'Curta', 'type': 'uint', 'default': 3, 'label': 'Curta глубина сглаживания', 'sinput': False}, {'mql': 'CPhase', 'py': 'CPhase', 'param': 'CPhase', 'type': 'int', 'default': 15, 'label': 'Curta параметр сглаживания', 'sinput': False}, {'mql': 'Media_Method', 'py': 'Media_Method', 'param': 'Media_Method', 'type': 'int', 'default': 0, 'label': 'Media метод усреднения', 'sinput': False}, {'mql': 'Media', 'py': 'Media', 'param': 'Media', 'type': 'uint', 'default': 8, 'label': 'Media глубина сглаживания', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'int', 'default': 15, 'label': 'Media параметр сглаживания', 'sinput': False}, {'mql': 'Longa_Method', 'py': 'Longa_Method', 'param': 'Longa_Method', 'type': 'int', 'default': 0, 'label': 'Longa метод усреднения', 'sinput': False}, {'mql': 'Longa', 'py': 'Longa', 'param': 'Longa', 'type': 'uint', 'default': 20, 'label': 'Longa глубина сглаживания', 'sinput': False}, {'mql': 'LPhase', 'py': 'LPhase', 'param': 'LPhase', 'type': 'int', 'default': 15, 'label': 'Longa параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Revers', 'py': 'Revers', 'param': 'Revers', 'type': 'bool', 'default': False, 'label': 'Переворот графика относительно оси времени', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
Curta_Method = _input('Curta_Method', MODE_SMA)  # Curta метод усреднения
Curta = _input('Curta', 3)  # Curta глубина сглаживания
CPhase = _input('CPhase', 15)  # Curta параметр сглаживания
Media_Method = _input('Media_Method', MODE_SMA)  # Media метод усреднения
Media = _input('Media', 8)  # Media глубина сглаживания
MPhase = _input('MPhase', 15)  # Media параметр сглаживания
Longa_Method = _input('Longa_Method', MODE_SMA)  # Longa метод усреднения
Longa = _input('Longa', 20)  # Longa глубина сглаживания
LPhase = _input('LPhase', 15)  # Longa параметр сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # ценовая константа
Revers = _input('Revers', False)  # Переворот графика относительно оси времени
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('XDidi_Index', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'XDidi_Index', Curta_Method, Curta, CPhase, Media_Method, Media, MPhase, Longa_Method, Longa, LPhase, IPC, Revers)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XDidi_Index')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, DnIndBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'XDidi_Index', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, UpIndBuffer, 1, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, UpBuffNumb, UpIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            UpArr = Arr(1, 0.0, dyn=False)
            DnArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, UpBuffNumb, _DT(iTime_[bar]), 1, UpArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, DnBuffNumb, _DT(iTime_[bar]), 1, DnArr) <= 0:
                return (0 != 0)
            UpIndBuf[bar] = UpArr[0]
            DnIndBuf[bar] = DnArr[0]
        else:
            UpIndBuf[bar] = UpIndBuf[bar + 1]
            DnIndBuf[bar] = DnIndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XdidiIndexCloudHtf(_MQL5Indicator):
    name = 'xdidi_index_cloud_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'Curta_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Curta метод усреднения
        'Curta': 3,  # Curta глубина сглаживания
        'CPhase': 15,  # Curta параметр сглаживания
        'Media_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Media метод усреднения
        'Media': 8,  # Media глубина сглаживания
        'MPhase': 15,  # Media параметр сглаживания
        'Longa_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Longa метод усреднения
        'Longa': 20,  # Longa глубина сглаживания
        'LPhase': 15,  # Longa параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Revers': False,  # Переворот графика относительно оси времени
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

