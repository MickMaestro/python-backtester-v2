"""multix2masignal — converted from MQL5: MQL5 Indicators/MultiX2MASignal/multix2masignal.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_maximum': 4.9, 'indicator_minimum': 0.4, 'indicator_buffers': 16, 'indicator_plots': 12}, 'types': {1: 8, 2: 5, 3: 5, 4: 8, 5: 5, 6: 5, 7: 8, 8: 5, 9: 5, 10: 8, 11: 5, 12: 5}, 'colors': {1: [8421504, 16711935, 65280], 2: [8421376], 3: [255], 4: [8421504, 16711935, 65280], 5: [8421376], 6: [255], 7: [8421504, 16711935, 65280], 8: [8421376], 9: [255], 10: [8421504, 16711935, 65280], 11: [8421376], 12: [255]}, 'widths': {1: 3, 2: 5, 3: 5, 4: 3, 5: 5, 6: 5, 7: 3, 8: 5, 9: 5, 10: 3, 11: 5, 12: 5}, 'styles': {1: 0, 4: 0, 7: 0, 10: 0}, 'labels': {1: 'Signal line 1', 2: 'Up X2MA 1', 3: 'Down X2MA 1', 4: 'Signal line 2', 5: 'Up X2MA 2', 6: 'Down X2MA 2', 7: 'Signal line 3', 8: 'Up X2MA 3', 9: 'Down X2MA 3', 10: 'Signal line 4', 11: 'Up X2MA 4', 12: 'Down X2MA 4'}, 'levels': [], 'description': [''], 'name': 'multix2masignal', 'source': 'MQL5 Indicators/MultiX2MASignal/multix2masignal.mq5', 'folder': 'MultiX2MASignal', 'inputs': [{'mql': 'TimeFrame0', 'py': 'TimeFrame0', 'param': 'TimeFrame0', 'type': 'int', 'default': 16396, 'label': '1 Chart period', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16390, 'label': '2 Chart period', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16387, 'label': '3 Chart period', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16385, 'label': '4 Chart period', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'First smoothing averaging method', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 5, 'label': 'First smoothing depth', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 100, 'label': 'First smoothing parameter', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'Second smoothing averaging method', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 3, 'label': 'Second smoothing depth', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Second smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# ---- inputs and global variables
TimeFrame0 = _input('TimeFrame0', PERIOD_H12)  # 1 Chart period
TimeFrame1 = _input('TimeFrame1', PERIOD_H6)  # 2 Chart period
TimeFrame2 = _input('TimeFrame2', PERIOD_H3)  # 3 Chart period
TimeFrame3 = _input('TimeFrame3', PERIOD_H1)  # 4 Chart period
MA_Method1 = _input('MA_Method1', MODE_SMA)  # First smoothing averaging method
Length1 = _input('Length1', 5)  # First smoothing depth
Phase1 = _input('Phase1', 100)  # First smoothing parameter
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # Second smoothing averaging method
Length2 = _input('Length2', 3)  # Second smoothing depth
Phase2 = _input('Phase2', 100)  # Second smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Init = False
min_rates_total = 0

class CIndBuffers(MqlObject):
    _q_fields = ('m_UpBuffer', 'm_DnBuffer', 'm_LineBuffer', 'm_ColorLineBuffer', 'm_Handle', 'm_TimeFrame')
    def __init__(self, *args):
        self.m_UpBuffer = Arr(0, 0.0)
        self.m_DnBuffer = Arr(0, 0.0)
        self.m_LineBuffer = Arr(0, 0.0)
        self.m_ColorLineBuffer = Arr(0, 0.0)
        self.m_Handle = 0
        self.m_TimeFrame = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def IndInit(Number, XMAMethod1, XLength1, XPhase1, XMAMethod2, XLength2, XPhase2, XIPC):
    global Init
    if Ind[Number].m_TimeFrame < Period() and Ind[Number].m_TimeFrame != PERIOD_CURRENT:
        Print('IndInit(', Number, '): The X2MA indicator chart period cannot be less than the current chart period')
        Init = False
        return False
    Ind[Number].m_Handle = iCustom(None, Ind[Number].m_TimeFrame, 'X2MA', XMAMethod1, XLength1, XPhase1, XMAMethod2, XLength2, XPhase2, XIPC, 0, 0)
    if Ind[Number].m_Handle == INVALID_HANDLE:
        Print('IndInit(', Number, '): Failed to get the X2MA indicator handle')
        Init = False
        return False
    Numb = (Number * 4) + 0
    InitTsIndBuffer(Numb, Ind[Number].m_LineBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(Numb + 1, Ind[Number].m_ColorLineBuffer, min_rates_total)
    InitTsIndBuffer(Numb + 2, Ind[Number].m_UpBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndBuffer(Numb + 3, Ind[Number].m_DnBuffer, EMPTY_VALUE, min_rates_total)
    return True

def InitTsIndBuffer(Number, IndBuffer, Empty_Value, Draw_Begin):
    SetIndexBuffer(Number, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    ArraySetAsSeries(IndBuffer, True)

def InitTsIndColorBuffer(Number, IndColorBuffer, Draw_Begin):
    SetIndexBuffer(Number, IndColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    ArraySetAsSeries(IndColorBuffer, True)

def IndOnCalculate(Number, Limit, Time, Rates_Total, Prev_Calculated):
    limit_ = 0
    X2MA = Arr(2, 0.0, dyn=False)
    Time_ = Arr(1, 0, dyn=False)
    Time0 = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        _s_IndOnCalculate_LastCountBar[Number] = Rates_Total
        limit_ = Limit
    else:
        limit_ = _int(_s_IndOnCalculate_LastCountBar[Number]) + Limit
    for bar in range(_int(limit_), 0 - 1, -1):
        Ind[Number].m_UpBuffer[bar] = EMPTY_VALUE
        Ind[Number].m_DnBuffer[bar] = EMPTY_VALUE
        Ind[Number].m_LineBuffer[bar] = Number + 1
        Ind[Number].m_ColorLineBuffer[bar] = 0.0
        Time0 = Time[bar]
        if CopyTime(Symbol(), Ind[Number].m_TimeFrame, _DT(Time0), 1, Time_) <= 0:
            return (0 != 0)
        if Time0 >= Time_[0] and Time[bar + 1] < Time_[0]:
            _s_IndOnCalculate_LastCountBar[Number] = bar
            if CopyBuffer(Ind[Number].m_Handle, 0, _DT(Time0), 2, X2MA) <= 0:
                return (0 != 0)
            if X2MA[1] > X2MA[0]:
                Ind[Number].m_UpBuffer[bar] = Number + 1
                Ind[Number].m_ColorLineBuffer[bar] = 2.0
            if X2MA[1] < X2MA[0]:
                Ind[Number].m_DnBuffer[bar] = Number + 1
                Ind[Number].m_ColorLineBuffer[bar] = 1.0
        if Ind[Number].m_ColorLineBuffer[bar + 1] and (not Ind[Number].m_ColorLineBuffer[bar]):
            Ind[Number].m_ColorLineBuffer[bar] = Ind[Number].m_ColorLineBuffer[bar + 1]
    return True

def OnInit():
    global Init, min_rates_total
    min_rates_total = 3
    Init = True
    Ind[0].m_TimeFrame = TimeFrame0
    Ind[1].m_TimeFrame = TimeFrame1
    Ind[2].m_TimeFrame = TimeFrame2
    Ind[3].m_TimeFrame = TimeFrame3
    for count in range(0, 4):
        if not IndInit(count, MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, IPC):
            Init = False
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'MultiX2MASignal')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or (not Init):
        return 0
    for count in range(0, 4):
        if BarsCalculated(Ind[count].m_Handle) < Bars(Symbol(), Ind[count].m_TimeFrame):
            return prev_calculated
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    for count in range(0, 4):
        if not IndOnCalculate(count, limit, time, rates_total, prev_calculated):
            return 0
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(4, 0, dyn=False, factory=CIndBuffers)

# ---- static local variables
_s_IndOnCalculate_LastCountBar = Arr(4, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Multix2masignal(_MQL5Indicator):
    name = 'multix2masignal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # 1 Chart period
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # 2 Chart period
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16387),  # 3 Chart period
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # 4 Chart period
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # First smoothing averaging method
        'Length1': 5,  # First smoothing depth
        'Phase1': 100,  # First smoothing parameter
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Second smoothing averaging method
        'Length2': 3,  # Second smoothing depth
        'Phase2': 100,  # Second smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
    }
    y_range = (0.4, 4.9)

