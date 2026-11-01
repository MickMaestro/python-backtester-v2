"""AsymmetricStochNR_Cloud_HTF — converted from MQL5: MQL5 Indicators/AsymmetricStochNR_Cloud_HTF/AsymmetricStochNR_Cloud_HTF.mq5

AsymmetricStochNR_Cloud с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16760576, 14524637]}, 'widths': {}, 'styles': {}, 'labels': {1: 'AsymmetricStochNR_Cloud'}, 'levels': [], 'description': ['AsymmetricStochNR_Cloud с возможностью изменения таймфрейма во входных параметрах'], 'name': 'AsymmetricStochNR_Cloud_HTF', 'source': 'MQL5 Indicators/AsymmetricStochNR_Cloud_HTF/AsymmetricStochNR_Cloud_HTF.mq5', 'folder': 'AsymmetricStochNR_Cloud_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'KperiodShort', 'py': 'KperiodShort', 'param': 'KperiodShort', 'type': 'uint', 'default': 5, 'label': 'Период %K', 'sinput': False}, {'mql': 'KperiodLong', 'py': 'KperiodLong', 'param': 'KperiodLong', 'type': 'uint', 'default': 12, 'label': 'Период %K', 'sinput': False}, {'mql': 'DMethod', 'py': 'DMethod', 'param': 'DMethod', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания сигнальной линии', 'sinput': False}, {'mql': 'Dperiod', 'py': 'Dperiod', 'param': 'Dperiod', 'type': 'uint', 'default': 7, 'label': 'Период сигнальной линии %D', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания сигнальной линии', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': 'Замедление', 'sinput': False}, {'mql': 'PriceField', 'py': 'PriceField', 'param': 'PriceField', 'type': 'int', 'default': 0, 'label': 'Параметр выбора цен для расчета', 'sinput': False}, {'mql': 'Sens', 'py': 'Sens', 'param': 'Sens', 'type': 'uint', 'default': 7, 'label': 'Чувствительность в пунктах', 'sinput': False}, {'mql': 'OverBought', 'py': 'OverBought', 'param': 'OverBought', 'type': 'uint', 'default': 80, 'label': 'Уровень перекупленности в %%', 'sinput': False}, {'mql': 'OverSold', 'py': 'OverSold', 'param': 'OverSold', 'type': 'uint', 'default': 20, 'label': 'Уровень перепроданности в %%', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет уровня перекупленности', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет уровня перепроданности', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'Стиль уровней', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'Толщина уровней', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
KperiodShort = _input('KperiodShort', 5)  # Период %K
KperiodLong = _input('KperiodLong', 12)  # Период %K
DMethod = _input('DMethod', MODE_SMA_)  # Метод сглаживания сигнальной линии
Dperiod = _input('Dperiod', 7)  # Период сигнальной линии %D
DPhase = _input('DPhase', 15)  # Параметр сглаживания сигнальной линии
Slowing = _input('Slowing', 3)  # Замедление
PriceField = _input('PriceField', STO_LOWHIGH)  # Параметр выбора цен для расчета
Sens = _input('Sens', 7)  # Чувствительность в пунктах
OverBought = _input('OverBought', 80)  # Уровень перекупленности в %%
OverSold = _input('OverSold', 20)  # Уровень перепроданности в %%
UpLevelsColor = _input('UpLevelsColor', clrBlue)  # Цвет уровня перекупленности
DnLevelsColor = _input('DnLevelsColor', clrMagenta)  # Цвет уровня перепроданности
Levelstyle = _input('Levelstyle', DASH_)  # Стиль уровней
LevelsWidth = _input('LevelsWidth', Width_1)  # Толщина уровней
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('AsymmetricStochNR_Cloud', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'AsymmetricStochNR_Cloud', KperiodShort, KperiodLong, DMethod, Dperiod, DPhase, Slowing, PriceField, Sens, OverBought, OverSold, 0, 0, 0, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора AsymmetricStochNR_Cloud')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, DnIndBuffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'AsymmetricStochNR_Cloud', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, OverSold)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, DnLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, OverBought)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, UpLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
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


class AsymmetricStochNRCloudHTF(_MQL5Indicator):
    name = 'AsymmetricStochNR_Cloud_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'KperiodShort': 5,  # Период %K
        'KperiodLong': 12,  # Период %K
        'DMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания сигнальной линии
        'Dperiod': 7,  # Период сигнальной линии %D
        'DPhase': 15,  # Параметр сглаживания сигнальной линии
        'Slowing': 3,  # Замедление
        'PriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Параметр выбора цен для расчета
        'Sens': 7,  # Чувствительность в пунктах
        'OverBought': 80,  # Уровень перекупленности в %%
        'OverSold': 20,  # Уровень перепроданности в %%
        'Levelstyle': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=1),  # Стиль уровней
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Толщина уровней
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

