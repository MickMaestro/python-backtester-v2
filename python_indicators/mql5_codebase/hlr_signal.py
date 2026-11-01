"""hlr_signal — converted from MQL5: MQL5 Indicators/HLR_Signal/hlr_signal.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_maximum': 1.9, 'indicator_minimum': 0.3, 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 12}, 'colors': {1: [7504122, 7451452], 2: [7504122, 7451452]}, 'widths': {1: 3, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Signal line', 2: 'Signal Arrow'}, 'levels': [], 'description': [''], 'name': 'hlr_signal', 'source': 'MQL5 Indicators/HLR_Signal/hlr_signal.mq5', 'folder': 'HLR_Signal', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 0, 'label': 'Пробойный алгоритм', 'sinput': False}, {'mql': 'HLR_Range', 'py': 'HLR_Range', 'param': 'HLR_Range', 'type': 'uint', 'default': 40, 'label': 'Период усреднения индикатора', 'sinput': False}, {'mql': 'HLR_UpLevel', 'py': 'HLR_UpLevel', 'param': 'HLR_UpLevel', 'type': 'uint', 'default': 80, 'label': 'Уровень перекупленности', 'sinput': False}, {'mql': 'HLR_DnLevel', 'py': 'HLR_DnLevel', 'param': 'HLR_DnLevel', 'type': 'uint', 'default': 20, 'label': 'Уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Alg_Method
MODE_IN = 0
MODE_OUT = 1
_enum('Alg_Method', {0: 'MODE_IN', 1: 'MODE_OUT'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
Mode = _input('Mode', MODE_IN)  # Пробойный алгоритм
HLR_Range = _input('HLR_Range', 40)  # Период усреднения индикатора
HLR_UpLevel = _input('HLR_UpLevel', 80)  # Уровень перекупленности
HLR_DnLevel = _input('HLR_DnLevel', 20)  # Уровень перепроданности
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
        Print('IndInit(', Number, '): Период графика для индикатора HLR не может быть меньше периода текущего графика')
        return False
    Ind[Number].m_Handle = iCustom(Symbol(), Ind[Number].m_TimeFrame, 'HLR', HLR_Range, 0)
    if Ind[Number].m_Handle == INVALID_HANDLE:
        Print('IndInit(', Number, '): Не удалось получить хендл индикатора HLR')
        return False
    BIndex = (Number * 4) + 0
    PIndex = (Number * 2) + 0
    InitTsIndBuffer(BIndex, PIndex, Ind[Number].m_LineBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 1, Ind[Number].m_ColorLineBuffer)
    InitTsIndArrBuffer(BIndex + 2, PIndex + 1, Ind[Number].m_ArrowBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 3, Ind[Number].m_ColorArrowBuffer)
    tmf = GetStringTimeframe(Ind[Number].m_TimeFrame)
    PlotIndexSetString(PIndex + 0, PLOT_LABEL, 'HLR' + 'Line(' + tmf + ')')
    PlotIndexSetString(PIndex + 1, PLOT_LABEL, 'HLR' + 'Arrow(' + tmf + ')')
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
    PlotIndexSetInteger(Plot, PLOT_ARROW, 171)
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
            Buff = Arr(2, 0.0, dyn=False)
            if CopyBuffer(Ind[Number].m_Handle, 0, _DT(Time0), 2, Buff) <= 0:
                return (0 != 0)
            if Mode == MODE_IN:
                if Buff[1] > HLR_UpLevel and Buff[0] <= HLR_UpLevel:
                    Ind[Number].m_ArrowBuffer[bar] = Number + 1.0
                    Ind[Number].m_ColorArrowBuffer[bar] = 1.0
                    Ind[Number].m_ColorLineBuffer[bar] = 1.0
                if Buff[1] < HLR_DnLevel and Buff[0] >= HLR_DnLevel:
                    Ind[Number].m_ArrowBuffer[bar] = Number + 1.0
                    Ind[Number].m_ColorArrowBuffer[bar] = 0.0
                    Ind[Number].m_ColorLineBuffer[bar] = 0.0
            else:
                if Buff[1] < HLR_UpLevel and Buff[0] >= HLR_UpLevel:
                    Ind[Number].m_ArrowBuffer[bar] = Number + 1.0
                    Ind[Number].m_ColorArrowBuffer[bar] = 0.0
                    Ind[Number].m_ColorLineBuffer[bar] = 0.0
                if Buff[1] > HLR_DnLevel and Buff[0] <= HLR_DnLevel:
                    Ind[Number].m_ArrowBuffer[bar] = Number + 1.0
                    Ind[Number].m_ColorArrowBuffer[bar] = 1.0
                    Ind[Number].m_ColorLineBuffer[bar] = 1.0
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
    IndicatorSetString(INDICATOR_SHORTNAME, 'HLR_Signal')
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


class HlrSignal(_MQL5Indicator):
    name = 'hlr_signal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'Mode': _Choice({0: 'Алгоритм на входе в зоны ПЗ и ПП', 1: 'Алгоритм на выходе в зоны ПЗ и ПП'}, default=0),  # Пробойный алгоритм
        'HLR_Range': 40,  # Период усреднения индикатора
        'HLR_UpLevel': 80,  # Уровень перекупленности
        'HLR_DnLevel': 20,  # Уровень перепроданности
    }
    y_range = (0.3, 1.9)

