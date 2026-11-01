"""Differential_Average_By_Sultonov_Signal — converted from MQL5: MQL5 Indicators/Differential_Average_By_Sultonov_Signal/Differential_Average_By_Sultonov_Signal.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_maximum': 1.9, 'indicator_minimum': 0.3, 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 12}, 'colors': {1: [16711680, 255], 2: [16711680, 255]}, 'widths': {1: 2, 2: 5}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Signal line', 2: 'Signal Arrow'}, 'levels': [], 'description': [''], 'name': 'Differential_Average_By_Sultonov_Signal', 'source': 'MQL5 Indicators/Differential_Average_By_Sultonov_Signal/Differential_Average_By_Sultonov_Signal.mq5', 'folder': 'Differential_Average_By_Sultonov_Signal', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'i_nPeriod', 'py': 'i_nPeriod', 'param': 'i_nPeriod', 'type': 'uint', 'default': 1000, 'label': 'Calculate period / Период расчета', 'sinput': False}, {'mql': 'XMethod', 'py': 'XMethod', 'param': 'XMethod', 'type': 'int', 'default': 0, 'label': 'метод усреднения сглаживания', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
i_nPeriod = _input('i_nPeriod', 1000)  # Calculate period / Период расчета
XMethod = _input('XMethod', MODE_SMA_)  # метод усреднения сглаживания
XLength = _input('XLength', 12)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
min_rates_total = 0

class CIndBuffers(MqlObject):
    _q_fields = ('m_LineBuffer', 'm_ColorLineBuffer', 'm_ArrowBuffer', 'm_ColorArrowBuffer', 'm_Handle', 'm_TimeFrame')
    def __init__(self, *args):
        self.m_LineBuffer = Arr(0, 0.0)
        self.m_ColorLineBuffer = Arr(0, 0.0)
        self.m_ArrowBuffer = Arr(0, 0.0)
        self.m_ColorArrowBuffer = Arr(0, 0.0)
        self.m_Handle = 0
        self.m_TimeFrame = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def IndInit(Number):
    if Ind[Number].m_TimeFrame < Period() and Ind[Number].m_TimeFrame != PERIOD_CURRENT:
        Print('IndInit(', Number, '): Период графика для индикатора Differential_Average_By_Sultonov не может быть меньше периода текущего графика')
        return False
    Ind[Number].m_Handle = iCustom(Symbol(), Ind[Number].m_TimeFrame, 'Differential_Average_By_Sultonov', i_nPeriod, XMethod, XLength, XPhase, IPC, 0)
    if Ind[Number].m_Handle == INVALID_HANDLE:
        Print('IndInit(', Number, '): Не удалось получить хендл индикатора Differential_Average_By_Sultonov')
        return False
    BIndex = (Number * 4) + 0
    PIndex = (Number * 2) + 0
    InitTsIndBuffer(BIndex, PIndex, Ind[Number].m_LineBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 1, Ind[Number].m_ColorLineBuffer)
    InitTsIndArrBuffer(BIndex + 2, PIndex + 1, Ind[Number].m_ArrowBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 3, Ind[Number].m_ColorArrowBuffer)
    tmf = GetStringTimeframe(Ind[Number].m_TimeFrame)
    PlotIndexSetString(PIndex + 0, PLOT_LABEL, 'Differential_Average_By_Sultonov' + 'Line(' + tmf + ')')
    PlotIndexSetString(PIndex + 1, PLOT_LABEL, 'Differential_Average_By_Sultonov' + 'Arrow(' + tmf + ')')
    return True

def InitTsIndBuffer(Number, Plot, IndBuffer, Empty_Value, Draw_Begin):
    SetIndexBuffer(Number, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Plot, PLOT_EMPTY_VALUE, Empty_Value)
    ArraySetAsSeries(IndBuffer, True)

def InitTsIndArrBuffer(Number, Plot, IndBuffer, Empty_Value, Draw_Begin):
    SetIndexBuffer(Number, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Plot, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Plot, PLOT_ARROW, 159)
    ArraySetAsSeries(IndBuffer, True)

def InitTsIndColorBuffer(Number, IndColorBuffer):
    SetIndexBuffer(Number, IndColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(IndColorBuffer, True)

def IndOnCalculate(Number, Limit, Time, Rates_Total, Prev_Calculated):
    limit_ = 0
    Time_ = Arr(1, 0, dyn=False)
    Time0 = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit_ = Limit
        _s_IndOnCalculate_LastCountBar[Number] = limit_
    else:
        limit_ = _int(MathMin(_s_IndOnCalculate_LastCountBar[Number] + Limit, Rates_Total - 2))
    for bar in range(limit_, 0 - 1, -1):
        Ind[Number].m_LineBuffer[bar] = Number + 1.0
        Ind[Number].m_ArrowBuffer[bar] = EMPTY_VALUE
        Ind[Number].m_ColorLineBuffer[bar] = EMPTY_VALUE
        Time0 = Time[bar]
        if CopyTime(Symbol(), Ind[Number].m_TimeFrame, _DT(Time0), 1, Time_) <= 0:
            return (0 != 0)
        if Time0 >= Time_[0] and Time[bar + 1] < Time_[0]:
            _s_IndOnCalculate_LastCountBar[Number] = bar
            Ind[Number].m_ArrowBuffer[bar] = Number + 1.0
            Ind[Number].m_ColorLineBuffer[bar] = 2.0
            Up = Arr(2, 0.0, dyn=False)
            Dn = Arr(2, 0.0, dyn=False)
            if CopyBuffer(Ind[Number].m_Handle, 0, _DT(Time0), 1, Up) <= 0:
                return (0 != 0)
            if CopyBuffer(Ind[Number].m_Handle, 1, _DT(Time0), 1, Dn) <= 0:
                return (0 != 0)
            diff1 = Up[0] - Dn[0]
            if diff1 > 0:
                Ind[Number].m_ColorLineBuffer[bar] = 0.0
                Ind[Number].m_ColorArrowBuffer[bar] = 0.0
            if diff1 < 0:
                Ind[Number].m_ColorLineBuffer[bar] = 1.0
                Ind[Number].m_ColorArrowBuffer[bar] = 1.0
        if Ind[Number].m_ColorLineBuffer[bar + 1] != EMPTY_VALUE and Ind[Number].m_ColorLineBuffer[bar] == EMPTY_VALUE:
            Ind[Number].m_ColorLineBuffer[bar] = Ind[Number].m_ColorLineBuffer[bar + 1]
    return True

def OnInit():
    global min_rates_total
    min_rates_total = 3
    Ind[0].m_TimeFrame = TimeFrame
    for count in range(0, 1):
        if not IndInit(count):
            return INIT_FAILED
    word = GetStringTimeframe(Ind[0].m_TimeFrame)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Differential_Average_By_Sultonov(' + word + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    for count in range(0, 1):
        if BarsCalculated(Ind[count].m_Handle) < Bars(Symbol(), Ind[count].m_TimeFrame):
            return prev_calculated
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    for count in range(0, 1):
        if not IndOnCalculate(count, limit, time, rates_total, prev_calculated):
            return 0
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(1, 0, dyn=False, factory=CIndBuffers)

# ---- static local variables
_s_IndOnCalculate_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DifferentialAverageBySultonovSignal(_MQL5Indicator):
    name = 'Differential_Average_By_Sultonov_Signal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'i_nPeriod': 1000,  # Calculate period / Период расчета
        'XMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения сглаживания
        'XLength': 12,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
    }
    y_range = (0.3, 1.9)

