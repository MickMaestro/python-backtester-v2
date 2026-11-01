"""multit3_trixx7signal — converted from MQL5: MQL5 Indicators/MultiT3_TRIXx7Signal/multit3_trixx7signal.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.30

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.30', 'window': 'separate', 'indicator_maximum': 7.9, 'indicator_minimum': 0.3, 'indicator_buffers': 28, 'indicator_plots': 21}, 'types': {1: 8, 2: 5, 3: 5, 4: 8, 5: 5, 6: 5, 7: 8, 8: 5, 9: 5, 10: 8, 11: 5, 12: 5, 13: 8, 14: 5, 15: 5, 16: 8, 17: 5, 18: 5, 19: 8, 20: 5, 21: 5}, 'colors': {1: [8421504, 16711935, 16711680], 2: [16711680], 3: [255], 4: [8421504, 16711935, 16711680], 5: [16711680], 6: [255], 7: [8421504, 16711935, 16711680], 8: [16711680], 9: [255], 10: [8421504, 16711935, 16711680], 11: [16711680], 12: [255], 13: [8421504, 16711935, 16711680], 14: [16711680], 15: [255], 16: [8421504, 16711935, 16711680], 17: [16711680], 18: [255], 19: [8421504, 16711935, 16711680], 20: [16711680], 21: [255]}, 'widths': {1: 3, 2: 5, 3: 5, 4: 3, 5: 5, 6: 5, 7: 3, 8: 5, 9: 5, 10: 3, 11: 5, 12: 5, 13: 3, 14: 5, 15: 5, 16: 3, 17: 5, 18: 5, 19: 3, 20: 5, 21: 5}, 'styles': {1: 0, 4: 0, 7: 0, 10: 0, 13: 0, 16: 0, 19: 0}, 'labels': {1: 'Signal line 1', 2: 'Up T3_TRIX 1', 3: 'Down T3_TRIX 1', 4: 'Signal line 2', 5: 'Up T3_TRIX 2', 6: 'Down T3_TRIX 2', 7: 'Signal line 3', 8: 'Up T3_TRIX 3', 9: 'Down T3_TRIX 3', 10: 'Signal line 4', 11: 'Up T3_TRIX 4', 12: 'Down T3_TRIX 4', 13: 'Signal line 5', 14: 'Up T3_TRIX 5', 15: 'Down T3_TRIX 5', 16: 'Signal line 6', 17: 'Up T3_TRIX 6', 18: 'Down T3_TRIX 6', 19: 'Signal line 7', 20: 'Up T3_TRIX 7', 21: 'Down T3_TRIX 7'}, 'levels': [], 'description': [''], 'name': 'multit3_trixx7signal', 'source': 'MQL5 Indicators/MultiT3_TRIXx7Signal/multit3_trixx7signal.mq5', 'folder': 'MultiT3_TRIXx7Signal', 'inputs': [{'mql': 'TimeFrame0', 'py': 'TimeFrame0', 'param': 'TimeFrame0', 'type': 'int', 'default': 16408, 'label': '1 Chart period', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16396, 'label': '2 Chart period', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16392, 'label': '3 Chart period', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16390, 'label': '4 Chart period', 'sinput': False}, {'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16388, 'label': '5 Chart period', 'sinput': False}, {'mql': 'TimeFrame5', 'py': 'TimeFrame5', 'param': 'TimeFrame5', 'type': 'int', 'default': 16387, 'label': '6 Chart period', 'sinput': False}, {'mql': 'TimeFrame6', 'py': 'TimeFrame6', 'param': 'TimeFrame6', 'type': 'int', 'default': 16385, 'label': '7 Chart period', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 10, 'label': 'Depth of the first averaging', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 18, 'label': 'Depth of the slow averaging', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 70, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
TimeFrame0 = _input('TimeFrame0', PERIOD_D1)  # 1 Chart period
TimeFrame1 = _input('TimeFrame1', PERIOD_H12)  # 2 Chart period
TimeFrame2 = _input('TimeFrame2', PERIOD_H8)  # 3 Chart period
TimeFrame3 = _input('TimeFrame3', PERIOD_H6)  # 4 Chart period
TimeFrame4 = _input('TimeFrame4', PERIOD_H4)  # 5 Chart period
TimeFrame5 = _input('TimeFrame5', PERIOD_H3)  # 6 Chart period
TimeFrame6 = _input('TimeFrame6', PERIOD_H1)  # 7 Chart period
XMA_Method = _input('XMA_Method', MODE_T3)  # Method of averaging
XLength1 = _input('XLength1', 10)  # Depth of the first averaging
XLength2 = _input('XLength2', 18)  # Depth of the slow averaging
XPhase = _input('XPhase', 70)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
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

def IndInit(Number):
    if Ind[Number].m_TimeFrame < Period() and Ind[Number].m_TimeFrame != PERIOD_CURRENT:
        Print('IndInit(', Number, '): The T3_TRIX indicator chart period cannot be less than the current chart period')
        return False
    Ind[Number].m_Handle = iCustom(Symbol(), Ind[Number].m_TimeFrame, 'T3_TRIX', XMA_Method, XLength1, XLength2, XPhase, IPC)
    if Ind[Number].m_Handle == INVALID_HANDLE:
        Print('IndInit(', Number, '): Failed to receive the T3_TRIX indicator handle')
        return False
    BIndex = (Number * 4) + 0
    PIndex = (Number * 3) + 0
    InitTsIndBuffer(BIndex, PIndex, Ind[Number].m_LineBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 1, PIndex, Ind[Number].m_ColorLineBuffer, min_rates_total)
    InitTsIndArrBuffer(BIndex + 2, PIndex + 1, Ind[Number].m_UpBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndArrBuffer(BIndex + 3, PIndex + 2, Ind[Number].m_DnBuffer, EMPTY_VALUE, min_rates_total)
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

def InitTsIndColorBuffer(Number, Plot, IndColorBuffer, Draw_Begin):
    SetIndexBuffer(Number, IndColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    ArraySetAsSeries(IndColorBuffer, True)

def IndOnCalculate(Number, Limit, Time, Rates_Total, Prev_Calculated):
    limit_ = 0
    T3_TRIX = Arr(2, 0.0, dyn=False)
    Time_ = Arr(1, 0, dyn=False)
    Time0 = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit_ = Limit
        _s_IndOnCalculate_LastCountBar[Number] = limit_
        _s_IndOnCalculate_PrevLastCountBar[Number] = limit_
    else:
        limit_ = _int(MathMin(_s_IndOnCalculate_PrevLastCountBar[Number] + Limit, Rates_Total - 2))
    for bar in range(limit_, 0 - 1, -1):
        Ind[Number].m_UpBuffer[bar] = EMPTY_VALUE
        Ind[Number].m_DnBuffer[bar] = EMPTY_VALUE
        Ind[Number].m_LineBuffer[bar] = Number + 1.0
        Ind[Number].m_ColorLineBuffer[bar] = 0.0
        Time0 = Time[bar]
        if CopyTime(Symbol(), Ind[Number].m_TimeFrame, _DT(Time0), 1, Time_) <= 0:
            return (0 != 0)
        if Time0 >= Time_[0] and Time[bar + 1] < Time_[0]:
            if bar:
                _s_IndOnCalculate_PrevLastCountBar[Number] = _s_IndOnCalculate_LastCountBar[Number]
            _s_IndOnCalculate_LastCountBar[Number] = bar
            if CopyBuffer(Ind[Number].m_Handle, 2, _DT(Time0), 2, T3_TRIX) <= 0:
                return (0 != 0)
            if T3_TRIX[1] > T3_TRIX[0]:
                Ind[Number].m_UpBuffer[bar] = Number + 1.0
                Ind[Number].m_ColorLineBuffer[bar] = 2.0
            if T3_TRIX[1] < T3_TRIX[0]:
                Ind[Number].m_DnBuffer[bar] = Number + 1.0
                Ind[Number].m_ColorLineBuffer[bar] = 1.0
        if Ind[Number].m_ColorLineBuffer[bar + 1] and (not Ind[Number].m_ColorLineBuffer[bar]):
            Ind[Number].m_ColorLineBuffer[bar] = Ind[Number].m_ColorLineBuffer[bar + 1]
    return True

def OnInit():
    global min_rates_total
    min_rates_total = 3
    Ind[0].m_TimeFrame = TimeFrame0
    Ind[1].m_TimeFrame = TimeFrame1
    Ind[2].m_TimeFrame = TimeFrame2
    Ind[3].m_TimeFrame = TimeFrame3
    Ind[4].m_TimeFrame = TimeFrame4
    Ind[5].m_TimeFrame = TimeFrame5
    Ind[6].m_TimeFrame = TimeFrame6
    for count in range(0, 7):
        if not IndInit(count):
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'MultiT3_TRIXSignal')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    for count in range(0, 7):
        if not IndOnCalculate(count, limit, time, rates_total, prev_calculated):
            return 0
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(7, 0, dyn=False, factory=CIndBuffers)

# ---- static local variables
_s_IndOnCalculate_LastCountBar = Arr(7, 0, dyn=False)
_s_IndOnCalculate_PrevLastCountBar = Arr(7, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Multit3Trixx7signal(_MQL5Indicator):
    name = 'multit3_trixx7signal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # 1 Chart period
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # 2 Chart period
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16392),  # 3 Chart period
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # 4 Chart period
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # 5 Chart period
        'TimeFrame5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16387),  # 6 Chart period
        'TimeFrame6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # 7 Chart period
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Method of averaging
        'XLength1': 10,  # Depth of the first averaging
        'XLength2': 18,  # Depth of the slow averaging
        'XPhase': 70,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Price constant
    }
    y_range = (0.3, 7.9)

