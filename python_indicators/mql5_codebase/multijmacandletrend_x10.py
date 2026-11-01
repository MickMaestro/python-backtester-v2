"""MultiJMACandleTrend_x10 — converted from MQL5: MQL5 Indicators/MultiJMACandleTrend_x10/MultiJMACandleTrend_x10.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.61

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.61', 'window': 'separate', 'indicator_maximum': 10.9, 'indicator_minimum': 0.3, 'indicator_buffers': 40, 'indicator_plots': 20}, 'types': {1: 8, 2: 12, 3: 8, 4: 12, 5: 8, 6: 12, 7: 8, 8: 12, 9: 8, 10: 12, 11: 8, 12: 12, 13: 8, 14: 12, 15: 8, 16: 12, 17: 8, 18: 12, 19: 8, 20: 12}, 'colors': {1: [16748574, 16711935], 2: [16748574, 16711935], 3: [16748574, 16711935], 4: [16748574, 16711935], 5: [16748574, 16711935], 6: [16748574, 16711935], 7: [16748574, 16711935], 8: [16748574, 16711935], 9: [16748574, 16711935], 10: [16748574, 16711935], 11: [16748574, 16711935], 12: [16748574, 16711935], 13: [16748574, 16711935], 14: [16748574, 16711935], 15: [16748574, 16711935], 16: [16748574, 16711935], 17: [16748574, 16711935], 18: [16748574, 16711935], 19: [16748574, 16711935], 20: [16748574, 16711935]}, 'widths': {1: 3, 2: 2, 3: 3, 4: 2, 5: 3, 6: 2, 7: 3, 8: 2, 9: 3, 10: 2, 11: 3, 12: 2, 13: 3, 14: 2, 15: 3, 16: 2, 17: 3, 18: 2, 19: 3, 20: 2}, 'styles': {1: 0, 3: 0, 5: 0, 7: 0, 9: 0, 11: 0, 13: 0, 15: 0, 17: 0, 19: 0}, 'labels': {1: 'Signal line 1', 2: 'Signal Arrow 1', 3: 'Signal line 2', 4: 'Signal Arrow 2', 5: 'Signal line 3', 6: 'Signal Arrow 3', 7: 'Signal line 4', 8: 'Signal Arrow 4', 9: 'Signal line 5', 10: 'Signal Arrow 5', 11: 'Signal line 6', 12: 'Signal Arrow 6', 13: 'Signal line 7', 14: 'Signal Arrow 7', 15: 'Signal line 8', 16: 'Signal Arrow 8', 17: 'Signal line 9', 18: 'Signal Arrow 9', 19: 'Signal line 10', 20: 'Signal Arrow 10'}, 'levels': [], 'description': [''], 'name': 'MultiJMACandleTrend_x10', 'source': 'MQL5 Indicators/MultiJMACandleTrend_x10/MultiJMACandleTrend_x10.mq5', 'folder': 'MultiJMACandleTrend_x10', 'inputs': [{'mql': 'TimeFrame0', 'py': 'TimeFrame0', 'param': 'TimeFrame0', 'type': 'int', 'default': 16385, 'label': 'период графика 1', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16386, 'label': 'период графика 2', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16387, 'label': 'период графика 3', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16388, 'label': 'период графика 4', 'sinput': False}, {'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16390, 'label': 'период графика 5', 'sinput': False}, {'mql': 'TimeFrame5', 'py': 'TimeFrame5', 'param': 'TimeFrame5', 'type': 'int', 'default': 16392, 'label': 'период графика 6', 'sinput': False}, {'mql': 'TimeFrame6', 'py': 'TimeFrame6', 'param': 'TimeFrame6', 'type': 'int', 'default': 16396, 'label': 'период графика 7', 'sinput': False}, {'mql': 'TimeFrame7', 'py': 'TimeFrame7', 'param': 'TimeFrame7', 'type': 'int', 'default': 16408, 'label': 'период графика 8', 'sinput': False}, {'mql': 'TimeFrame8', 'py': 'TimeFrame8', 'param': 'TimeFrame8', 'type': 'int', 'default': 32769, 'label': 'период графика 9', 'sinput': False}, {'mql': 'TimeFrame9', 'py': 'TimeFrame9', 'param': 'TimeFrame9', 'type': 'int', 'default': 49153, 'label': 'период графика 10', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 30, 'label': 'глубина усреднения', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
TimeFrame0 = _input('TimeFrame0', PERIOD_H1)  # период графика 1
TimeFrame1 = _input('TimeFrame1', PERIOD_H2)  # период графика 2
TimeFrame2 = _input('TimeFrame2', PERIOD_H3)  # период графика 3
TimeFrame3 = _input('TimeFrame3', PERIOD_H4)  # период графика 4
TimeFrame4 = _input('TimeFrame4', PERIOD_H6)  # период графика 5
TimeFrame5 = _input('TimeFrame5', PERIOD_H8)  # период графика 6
TimeFrame6 = _input('TimeFrame6', PERIOD_H12)  # период графика 7
TimeFrame7 = _input('TimeFrame7', PERIOD_D1)  # период графика 8
TimeFrame8 = _input('TimeFrame8', PERIOD_W1)  # период графика 9
TimeFrame9 = _input('TimeFrame9', PERIOD_MN1)  # период графика 10
MA_Method1 = _input('MA_Method1', MODE_JJMA)  # метод усреднения
Length1 = _input('Length1', 30)  # глубина усреднения
Phase1 = _input('Phase1', 15)  # параметр усреднения,
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
min_rates_total = 0

class CIndBuffers(MqlObject):
    _q_fields = ('m_ArrBuffer', 'm_ColorArrBuffer', 'm_LineBuffer', 'm_ColorLineBuffer', 'm_Handle', 'm_TimeFrame')
    def __init__(self, *args):
        self.m_ArrBuffer = Arr(0, 0.0)
        self.m_ColorArrBuffer = Arr(0, 0.0)
        self.m_LineBuffer = Arr(0, 0.0)
        self.m_ColorLineBuffer = Arr(0, 0.0)
        self.m_Handle = 0
        self.m_TimeFrame = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def IndInit(Number):
    Ind[Number].m_Handle = iCustom(Symbol(), Ind[Number].m_TimeFrame, 'JMACandleTrend', MA_Method1, Length1, Phase1, Gap, 171, 171)
    if Ind[Number].m_Handle == INVALID_HANDLE:
        Print('IndInit(', Number, '): Не удалось получить хендл индикатора JMACandleTrend')
        return False
    BIndex = (Number * 4) + 0
    PIndex = (Number * 2) + 0
    InitTsIndBuffer(BIndex, PIndex, Ind[Number].m_LineBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 1, Ind[Number].m_ColorLineBuffer, min_rates_total)
    InitTsIndArrBuffer(BIndex + 2, PIndex + 1, Ind[Number].m_ArrBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 3, Ind[Number].m_ColorArrBuffer, min_rates_total)
    tmf = GetStringTimeframe(Ind[Number].m_TimeFrame)
    PlotIndexSetString(PIndex + 0, PLOT_LABEL, 'JMACandleTrend_x10' + '(' + tmf + ')')
    PlotIndexSetString(PIndex + 1, PLOT_LABEL, 'JMACandleTrend_x10' + 'Arr(' + tmf + ')')
    return True

def InitTsIndBuffer(Number, Plot, IndBuffer, Empty_Value, Draw_Begin):
    SetIndexBuffer(Number, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Plot, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Plot, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(IndBuffer, True)

def InitTsIndArrBuffer(Number, Plot, IndBuffer, Empty_Value, Draw_Begin):
    SetIndexBuffer(Number, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Plot, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Plot, PLOT_ARROW, 172)
    PlotIndexSetInteger(Plot, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(IndBuffer, True)

def InitTsIndColorBuffer(Number, IndColorBuffer, Draw_Begin):
    SetIndexBuffer(Number, IndColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(IndColorBuffer, True)

def IndOnCalculate(Number, Limit, Time, Rates_Total, Prev_Calculated):
    limit_ = 0
    Main = Arr(1, 0.0, dyn=False)
    Time_ = Arr(1, 0, dyn=False)
    Time0 = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit_ = Limit
        _s_IndOnCalculate_LastCountBar[Number] = limit_
    else:
        limit_ = _int(MathMin(_s_IndOnCalculate_LastCountBar[Number] + Limit, Rates_Total - 2))
    for bar in range(limit_, 0 - 1, -1):
        Ind[Number].m_ArrBuffer[bar] = EMPTY_VALUE
        Ind[Number].m_LineBuffer[bar] = Number + 1.0
        Time0 = Time[bar]
        if CopyTime(Symbol(), Ind[Number].m_TimeFrame, _DT(Time0), 1, Time_) <= 0:
            return False
        if Time0 >= Time_[0] and Time[bar + 1] < Time_[0]:
            _s_IndOnCalculate_LastCountBar[Number] = bar
            Ind[Number].m_ArrBuffer[bar] = Number + 1.0
            Ind[Number].m_ColorLineBuffer[bar] = 2.0
            Up = Arr(1, 0.0, dyn=False)
            Dn = Arr(1, 0.0, dyn=False)
            if CopyBuffer(Ind[Number].m_Handle, 0, _DT(Time0), 1, Up) <= 0:
                return (0 != 0)
            if CopyBuffer(Ind[Number].m_Handle, 1, _DT(Time0), 1, Dn) <= 0:
                return (0 != 0)
            if Up[0]:
                Ind[Number].m_ColorLineBuffer[bar] = 0.0
                Ind[Number].m_ColorArrBuffer[bar] = 0.0
            if Dn[0]:
                Ind[Number].m_ColorLineBuffer[bar] = 1.0
                Ind[Number].m_ColorArrBuffer[bar] = 1.0
            if (not Up[0]) and (not Dn[0]):
                Ind[Number].m_ColorLineBuffer[bar] = Ind[Number].m_ColorLineBuffer[bar + 1]
                Ind[Number].m_ColorArrBuffer[bar] = Ind[Number].m_ColorLineBuffer[bar + 1]
        else:
            Ind[Number].m_ColorLineBuffer[bar] = Ind[Number].m_ColorLineBuffer[bar + 1]
    return True

def OnInit():
    global min_rates_total
    min_rates_total = 100
    Ind[0].m_TimeFrame = TimeFrame0
    Ind[1].m_TimeFrame = TimeFrame1
    Ind[2].m_TimeFrame = TimeFrame2
    Ind[3].m_TimeFrame = TimeFrame3
    Ind[4].m_TimeFrame = TimeFrame4
    Ind[5].m_TimeFrame = TimeFrame5
    Ind[6].m_TimeFrame = TimeFrame6
    Ind[7].m_TimeFrame = TimeFrame7
    Ind[8].m_TimeFrame = TimeFrame8
    Ind[9].m_TimeFrame = TimeFrame9
    for count in range(0, 10):
        if not IndInit(count):
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'MultiJMACandleTrend_x10')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for count in range(0, 10):
        if not TimeFramesCheck('JMACandleTrend_x10', Ind[count].m_TimeFrame):
            return 0
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    for count in range(0, 10):
        if not IndOnCalculate(count, limit, time, rates_total, prev_calculated):
            return 0
    return rates_total

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- global variables initialised from expressions
Ind = Arr(10, 0, dyn=False, factory=CIndBuffers)

# ---- static local variables
_s_IndOnCalculate_LastCountBar = Arr(10, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiJMACandleTrendX10(_MQL5Indicator):
    name = 'MultiJMACandleTrend_x10'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 1
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16386),  # период графика 2
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16387),  # период графика 3
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # период графика 4
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # период графика 5
        'TimeFrame5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16392),  # период графика 6
        'TimeFrame6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # период графика 7
        'TimeFrame7': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # период графика 8
        'TimeFrame8': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=32769),  # период графика 9
        'TimeFrame9': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=49153),  # период графика 10
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'Length1': 30,  # глубина усреднения
        'Phase1': 15,  # параметр усреднения,
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
    }
    y_range = (0.3, 10.9)

