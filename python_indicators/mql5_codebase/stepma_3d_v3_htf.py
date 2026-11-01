"""StepMA_3D_v3_HTF — converted from MQL5: MQL5 Indicators/StepMA_3D_v3_HTF/StepMA_3D_v3_HTF.mq5

StepMA_3D_v3 с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3329330], 2: [16711680], 3: [255]}, 'widths': {1: 4, 2: 4, 3: 4}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper StepMA_3D_v3', 2: 'Middle StepMA_3D_v3', 3: 'Lower StepMA_3D_v3'}, 'levels': [], 'description': ['StepMA_3D_v3 с возможностью изменения таймфрейма во входных параметрах'], 'name': 'StepMA_3D_v3_HTF', 'source': 'MQL5 Indicators/StepMA_3D_v3_HTF/StepMA_3D_v3_HTF.mq5', 'folder': 'StepMA_3D_v3_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 10, 'label': 'Период ATR', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 1.000001, 'label': 'Фактор чувствительности на изменения цены', 'sinput': False}, {'mql': 'MA_Mode', 'py': 'MA_Mode', 'param': 'MA_Mode', 'type': 'int', 'default': 0, 'label': 'Метод усреднения ATR', 'sinput': False}, {'mql': 'ShiftMIN', 'py': 'ShiftMIN', 'param': 'ShiftMIN', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора быстрого тренда по горизонтали в барах', 'sinput': False}, {'mql': 'ShiftMID', 'py': 'ShiftMID', 'param': 'ShiftMID', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора среднего тренда по горизонтали в барах', 'sinput': False}, {'mql': 'ShiftMAX', 'py': 'ShiftMAX', 'param': 'ShiftMAX', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора медленного тренда по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MA_MODE
MODE_SMA_ = 0
MODE_LWMA_ = 1
_enum('ENUM_MA_MODE', {0: 'MODE_SMA_', 1: 'MODE_LWMA_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
Length = _input('Length', 10)  # Период ATR
Kv = _input('Kv', 1.000001)  # Фактор чувствительности на изменения цены
MA_Mode = _input('MA_Mode', MODE_SMA_)  # Метод усреднения ATR
ShiftMIN = _input('ShiftMIN', 0)  # сдвиг индикатора быстрого тренда по горизонтали в барах
ShiftMID = _input('ShiftMID', 0)  # сдвиг индикатора среднего тренда по горизонтали в барах
ShiftMAX = _input('ShiftMAX', 0)  # сдвиг индикатора медленного тренда по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
MdIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('StepMA_3D_v3', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'StepMA_3D_v3', Length, Kv, MA_Mode, 0, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора StepMA_3D_v3')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, MdIndBuffer, INDICATOR_DATA)
    IndInit(2, DnIndBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, 0, ShiftMIN)
    PlotInit(1, 0.0, 0, ShiftMID)
    PlotInit(2, 0.0, 0, ShiftMAX)
    shortname = Box("")
    StringConcatenate(shortname, 'StepMA_3D_v3', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, UpIndBuffer, 1, MdIndBuffer, 2, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, UpBuffNumb, UpIndBuf, MdBuffNumb, MdIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
            MdArr = Arr(1, 0.0, dyn=False)
            DnArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, UpBuffNumb, _DT(iTime_[bar]), 1, UpArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, MdBuffNumb, _DT(iTime_[bar]), 1, MdArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, DnBuffNumb, _DT(iTime_[bar]), 1, DnArr) <= 0:
                return (0 != 0)
            UpIndBuf[bar] = UpArr[0]
            MdIndBuf[bar] = MdArr[0]
            DnIndBuf[bar] = DnArr[0]
        else:
            UpIndBuf[bar] = UpIndBuf[bar + 1]
            MdIndBuf[bar] = MdIndBuf[bar + 1]
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


class StepMA3DV3HTF(_MQL5Indicator):
    name = 'StepMA_3D_v3_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'Length': 10,  # Период ATR
        'Kv': 1.000001,  # Фактор чувствительности на изменения цены
        'MA_Mode': _Choice({0: 'SMA', 1: 'LWMA'}, default=0),  # Метод усреднения ATR
        'ShiftMIN': 0,  # сдвиг индикатора быстрого тренда по горизонтали в барах
        'ShiftMID': 0,  # сдвиг индикатора среднего тренда по горизонтали в барах
        'ShiftMAX': 0,  # сдвиг индикатора медленного тренда по горизонтали в барах
    }

