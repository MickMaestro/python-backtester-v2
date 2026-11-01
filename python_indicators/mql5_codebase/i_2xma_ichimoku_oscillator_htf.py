"""2XMA_Ichimoku_Oscillator_HTF — converted from MQL5: MQL5 Indicators/2XMA_Ichimoku_Oscillator_HTF/2XMA_Ichimoku_Oscillator_HTF.mq5

2XMA_Ichimoku_Oscillator с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421376, 14822282, 8421504, 6053069, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: '2XMA_Ichimoku_Oscillator'}, 'levels': [], 'description': ['2XMA_Ichimoku_Oscillator с возможностью изменения таймфрейма во входных параметрах'], 'name': '2XMA_Ichimoku_Oscillator_HTF', 'source': 'MQL5 Indicators/2XMA_Ichimoku_Oscillator_HTF/2XMA_Ichimoku_Oscillator_HTF.mq5', 'folder': '2XMA_Ichimoku_Oscillator_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Up_period1', 'py': 'Up_period1', 'param': 'Up_period1', 'type': 'uint', 'default': 6, 'label': '1 период, используемый для вычисления наивысшего значения цены', 'sinput': False}, {'mql': 'Dn_period1', 'py': 'Dn_period1', 'param': 'Dn_period1', 'type': 'uint', 'default': 6, 'label': '1 период, используеммый для вычисления наинизшего значения цены', 'sinput': False}, {'mql': 'Up_period2', 'py': 'Up_period2', 'param': 'Up_period2', 'type': 'uint', 'default': 9, 'label': '2 период, используемый для вычисления наивысшего значения цены', 'sinput': False}, {'mql': 'Dn_period2', 'py': 'Dn_period2', 'param': 'Dn_period2', 'type': 'uint', 'default': 9, 'label': '2 период, используеммый для вычисления наинизшего значения цены', 'sinput': False}, {'mql': 'Up_mode1', 'py': 'Up_mode1', 'param': 'Up_mode1', 'type': 'int', 'default': 2, 'label': '1 таймсерия для поиска максимумов', 'sinput': False}, {'mql': 'Dn_mode1', 'py': 'Dn_mode1', 'param': 'Dn_mode1', 'type': 'int', 'default': 1, 'label': '1 таймсерия для поиска минимумов', 'sinput': False}, {'mql': 'Up_mode2', 'py': 'Up_mode2', 'param': 'Up_mode2', 'type': 'int', 'default': 2, 'label': '2 таймсерия для поиска максимумов', 'sinput': False}, {'mql': 'Dn_mode2', 'py': 'Dn_mode2', 'param': 'Dn_mode2', 'type': 'int', 'default': 1, 'label': '2 таймсерия для поиска минимумов', 'sinput': False}, {'mql': 'XMA1_Method', 'py': 'XMA1_Method', 'param': 'XMA1_Method', 'type': 'int', 'default': 0, 'label': '1 метод усреднения', 'sinput': False}, {'mql': 'XMA2_Method', 'py': 'XMA2_Method', 'param': 'XMA2_Method', 'type': 'int', 'default': 0, 'label': '2 метод усреднения', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'int', 'default': 25, 'label': '1 глубина сглаживания', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'int', 'default': 80, 'label': '2 глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора  по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MODE_PRICE
OPEN = 0
LOW = 1
HIGH = 2
CLOSE = 3
_enum('MODE_PRICE', {0: 'OPEN', 1: 'LOW', 2: 'HIGH', 3: 'CLOSE'})

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

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
Up_period1 = _input('Up_period1', 6)  # 1 период, используемый для вычисления наивысшего значения цены
Dn_period1 = _input('Dn_period1', 6)  # 1 период, используеммый для вычисления наинизшего значения цены
Up_period2 = _input('Up_period2', 9)  # 2 период, используемый для вычисления наивысшего значения цены
Dn_period2 = _input('Dn_period2', 9)  # 2 период, используеммый для вычисления наинизшего значения цены
Up_mode1 = _input('Up_mode1', HIGH)  # 1 таймсерия для поиска максимумов
Dn_mode1 = _input('Dn_mode1', LOW)  # 1 таймсерия для поиска минимумов
Up_mode2 = _input('Up_mode2', HIGH)  # 2 таймсерия для поиска максимумов
Dn_mode2 = _input('Dn_mode2', LOW)  # 2 таймсерия для поиска минимумов
XMA1_Method = _input('XMA1_Method', MODE_SMA_)  # 1 метод усреднения
XMA2_Method = _input('XMA2_Method', MODE_SMA_)  # 2 метод усреднения
XLength1 = _input('XLength1', 25)  # 1 глубина сглаживания
XLength2 = _input('XLength2', 80)  # 2 глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр усреднения,
Shift = _input('Shift', 0)  # сдвиг индикатора  по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('2XMA_Ichimoku_Oscillator', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, '2XMA_Ichimoku_Oscillator', Up_period1, Dn_period1, Up_period2, Dn_period2, Up_mode1, Dn_mode1, Up_mode2, Dn_mode2, XMA1_Method, XMA2_Method, XLength1, XLength2, XPhase, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора 2XMA_Ichimoku_Oscillator')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, '2XMA_Ichimoku_Oscillator', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    Ind = Arr(1, 0.0, dyn=False)
    Col = Arr(1, 0.0, dyn=False)
    limit = 0
    bar = 0
    IndTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, IndTime) <= 0:
            return 0
        if time[bar] >= IndTime[0] and time[bar + 1] < IndTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 1, Ind) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 1, _DT(time[bar]), 1, Col) <= 0:
                return 0
            IndBuffer[bar] = Ind[0]
            ColorIndBuffer[bar] = Col[0]
        else:
            IndBuffer[bar] = IndBuffer[bar + 1]
            ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_OnCalculate_LastInd = 0.0
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2XMAIchimokuOscillatorHTF(_MQL5Indicator):
    name = '2XMA_Ichimoku_Oscillator_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'Up_period1': 6,  # 1 период, используемый для вычисления наивысшего значения цены
        'Dn_period1': 6,  # 1 период, используеммый для вычисления наинизшего значения цены
        'Up_period2': 9,  # 2 период, используемый для вычисления наивысшего значения цены
        'Dn_period2': 9,  # 2 период, используеммый для вычисления наинизшего значения цены
        'Up_mode1': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=2),  # 1 таймсерия для поиска максимумов
        'Dn_mode1': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=1),  # 1 таймсерия для поиска минимумов
        'Up_mode2': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=2),  # 2 таймсерия для поиска максимумов
        'Dn_mode2': _Choice({0: 'По ценам открытия', 1: 'По минимумам', 2: 'По максимумам', 3: 'По ценам закрытия'}, default=1),  # 2 таймсерия для поиска минимумов
        'XMA1_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # 1 метод усреднения
        'XMA2_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # 2 метод усреднения
        'XLength1': 25,  # 1 глубина сглаживания
        'XLength2': 80,  # 2 глубина сглаживания
        'XPhase': 15,  # параметр усреднения,
        'Shift': 0,  # сдвиг индикатора  по горизонтали в барах
    }

