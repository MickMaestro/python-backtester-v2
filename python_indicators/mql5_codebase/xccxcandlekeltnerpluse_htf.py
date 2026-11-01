"""XCCXCandleKeltnerPluse_HTF — converted from MQL5: MQL5 Indicators/XCCXCandleKeltnerPluse_HTF/XCCXCandleKeltnerPluse_HTF.mq5

Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 17, 2: 7}, 'colors': {1: [255, 11823615, 8421504, 8421376, 65280], 2: [16443110]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XCCXCandle Open;XCCXCandle High;XCCXCandle Low;XCCXCandle Close', 2: 'Channels'}, 'levels': [], 'description': [], 'name': 'XCCXCandleKeltnerPluse_HTF', 'source': 'MQL5 Indicators/XCCXCandleKeltnerPluse_HTF/XCCXCandleKeltnerPluse_HTF.mq5', 'folder': 'XCCXCandleKeltnerPluse_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'метод усреднения цены', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 15, 'label': 'период мувинга', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения мувинга,', 'sinput': False}, {'mql': 'MSmoothMethod', 'py': 'MSmoothMethod', 'param': 'MSmoothMethod', 'type': 'int', 'default': 7, 'label': 'метод усреднения отклонения', 'sinput': False}, {'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'int', 'default': 15, 'label': 'период среднего отклонения', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'int', 'default': 15, 'label': 'среднего отклонения,', 'sinput': False}, {'mql': 'KeltnerPeriod', 'py': 'KeltnerPeriod', 'param': 'KeltnerPeriod', 'type': 'uint', 'default': 100, 'label': 'период усреднения Келтнера', 'sinput': False}, {'mql': 'Ratio', 'py': 'Ratio', 'param': 'Ratio', 'type': 'double', 'default': 4.01, 'label': 'девиация канала', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг канала по горизонтали в барах', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 1, 'label': 'метод индикации пробоя', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -50, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_COLOR_MODE
ENUM_LEVELES = 1
ENUM__CHANELS = 2
_enum('ENUM_COLOR_MODE', {1: 'ENUM_LEVELES', 2: 'ENUM__CHANELS'})

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
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # метод усреднения цены
DPeriod = _input('DPeriod', 15)  # период мувинга
DPhase = _input('DPhase', 15)  # параметр усреднения мувинга,
MSmoothMethod = _input('MSmoothMethod', MODE_T3)  # метод усреднения отклонения
MPeriod = _input('MPeriod', 15)  # период среднего отклонения
MPhase = _input('MPhase', 15)  # среднего отклонения,
KeltnerPeriod = _input('KeltnerPeriod', 100)  # период усреднения Келтнера
Ratio = _input('Ratio', 4.01)  # девиация канала
Shift = _input('Shift', 0)  # сдвиг канала по горизонтали в барах
Mode = _input('Mode', ENUM_LEVELES)  # метод индикации пробоя
HighLevel = _input('HighLevel', 50)
MiddleLevel = _input('MiddleLevel', 0)
LowLevel = _input('LowLevel', -50)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
ExtLineBuffer7 = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора XCCXCandleKeltnerPluse не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'XCCXCandleKeltnerPluse' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol_, TimeFrame, 'XCCXCandleKeltnerPluse', DSmoothMethod, DPeriod, DPhase, MSmoothMethod, MPeriod, MPhase, KeltnerPeriod, Ratio, 0, Mode, HighLevel, MiddleLevel, LowLevel)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XCCXCandleKeltnerPluse')
        return INIT_FAILED
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer5, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, ExtLineBuffer6, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer7, INDICATOR_DATA)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    ArraySetAsSeries(ExtLineBuffer7, True)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'XCCXCandleKeltnerPluse(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBrown)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, ExtLineBuffer1, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, ExtLineBuffer2, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, ExtLineBuffer3, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, ExtLineBuffer4, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(4, "", TimeFrame, Ind_Handle, 4, ExtLineBuffer5, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(5, "", TimeFrame, Ind_Handle, 5, ExtLineBuffer6, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(6, "", TimeFrame, Ind_Handle, 6, ExtLineBuffer7, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(7, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XCCXCandleKeltnerPluseHTF(_MQL5Indicator):
    name = 'XCCXCandleKeltnerPluse_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения цены
        'DPeriod': 15,  # период мувинга
        'DPhase': 15,  # параметр усреднения мувинга,
        'MSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения отклонения
        'MPeriod': 15,  # период среднего отклонения
        'MPhase': 15,  # среднего отклонения,
        'KeltnerPeriod': 100,  # период усреднения Келтнера
        'Ratio': 4.01,  # девиация канала
        'Shift': 0,  # сдвиг канала по горизонтали в барах
        'Mode': _Choice({1: 'по уровням перекупленности/перепроданности', 2: 'по границам канала Келтнера'}, default=1),  # метод индикации пробоя
        'HighLevel': 50,
        'MiddleLevel': 0,
        'LowLevel': -50,
    }

