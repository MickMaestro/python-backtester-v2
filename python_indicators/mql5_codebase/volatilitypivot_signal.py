"""volatilitypivot_signal — converted from MQL5: MQL5 Indicators/VolatilityPivot_Signal/volatilitypivot_signal.mq5

Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_maximum': 1.9, 'indicator_minimum': 0.3, 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 12}, 'colors': {1: [16711935, 8421504, 13749760], 2: [16711935, 8421504, 13749760]}, 'widths': {1: 3, 2: 5}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Signal line', 2: 'Signal Arrow'}, 'levels': [], 'description': [''], 'name': 'volatilitypivot_signal', 'source': 'MQL5 Indicators/VolatilityPivot_Signal/volatilitypivot_signal.mq5', 'folder': 'VolatilityPivot_Signal', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'atr_range', 'py': 'atr_range', 'param': 'atr_range', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'ima_range', 'py': 'ima_range', 'param': 'ima_range', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'atr_factor', 'py': 'atr_factor', 'param': 'atr_factor', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'DeltaPrice', 'py': 'DeltaPrice', 'param': 'DeltaPrice', 'type': 'uint', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Mode_
Mode_ATR = 0
Mode_Price = 1
_enum('Mode_', {0: 'Mode_ATR', 1: 'Mode_Price'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
atr_range = _input('atr_range', 100)
ima_range = _input('ima_range', 10)
atr_factor = _input('atr_factor', 3.0)
Mode = _input('Mode', Mode_ATR)
DeltaPrice = _input('DeltaPrice', 200)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
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
        Print('IndInit(', Number, '): The VolatilityPivot indicator chart period cannot be less than the current chart period')
        return False
    Ind[Number].m_Handle = iCustom(Symbol(), Ind[Number].m_TimeFrame, 'VolatilityPivot', atr_range, ima_range, atr_factor, Mode_ATR, DeltaPrice, 0)
    if Ind[Number].m_Handle == INVALID_HANDLE:
        Print('IndInit(', Number, '): Failed to get the VolatilityPivot indicator handle')
        return False
    BIndex = (Number * 4) + 0
    PIndex = (Number * 2) + 0
    InitTsIndBuffer(BIndex, PIndex, Ind[Number].m_LineBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 1, Ind[Number].m_ColorLineBuffer)
    InitTsIndArrBuffer(BIndex + 2, PIndex + 1, Ind[Number].m_ArrowBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 3, Ind[Number].m_ColorArrowBuffer)
    tmf = GetStringTimeframe(Ind[Number].m_TimeFrame)
    PlotIndexSetString(PIndex + 0, PLOT_LABEL, 'VolatilityPivot' + 'Line(' + tmf + ')')
    PlotIndexSetString(PIndex + 1, PLOT_LABEL, 'VolatilityPivot' + 'Arrow(' + tmf + ')')
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
    PlotIndexSetInteger(Plot, PLOT_ARROW, 119)
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
            Ind[Number].m_ColorLineBuffer[bar] = 1.0
            Up = Arr(1, 0.0, dyn=False)
            Dn = Arr(1, 0.0, dyn=False)
            if CopyBuffer(Ind[Number].m_Handle, 0, _DT(Time0), 1, Up) <= 0:
                return (0 != 0)
            if CopyBuffer(Ind[Number].m_Handle, 1, _DT(Time0), 1, Dn) <= 0:
                return (0 != 0)
            if Up[0] != EMPTY_VALUE:
                Ind[Number].m_ColorLineBuffer[bar] = 2.0
            if Dn[0] != EMPTY_VALUE:
                Ind[Number].m_ColorLineBuffer[bar] = 0.0
            Ind[Number].m_ColorArrowBuffer[bar] = Ind[Number].m_ColorLineBuffer[bar]
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
    IndicatorSetString(INDICATOR_SHORTNAME, 'VolatilityPivot(' + GetStringTimeframe(Ind[0].m_TimeFrame) + ')')
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


class VolatilitypivotSignal(_MQL5Indicator):
    name = 'volatilitypivot_signal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'atr_range': 100,
        'ima_range': 10,
        'atr_factor': 3.0,
        'Mode': _Choice({0: 'ATR', 1: 'price deviation'}, default=0),
        'DeltaPrice': 200,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }
    y_range = (0.3, 1.9)

