"""multicandlesignal — converted from MQL5: MQL5 Indicators/MultiCandleSignal/multicandlesignal.mq5

Copyright: Copyright © 2013, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.10', 'window': 'separate', 'indicator_maximum': 7.9, 'indicator_minimum': 0.3, 'indicator_buffers': 28, 'indicator_plots': 21}, 'types': {1: 8, 2: 5, 3: 5, 4: 8, 5: 5, 6: 5, 7: 8, 8: 5, 9: 5, 10: 8, 11: 5, 12: 5, 13: 8, 14: 5, 15: 5, 16: 8, 17: 5, 18: 5, 19: 8, 20: 5, 21: 5}, 'colors': {1: [8421504, 16711935, 32768], 2: [65280], 3: [255], 4: [8421504, 16711935, 32768], 5: [65280], 6: [255], 7: [8421504, 16711935, 32768], 8: [65280], 9: [255], 10: [8421504, 16711935, 32768], 11: [65280], 12: [255], 13: [8421504, 16711935, 32768], 14: [65280], 15: [255], 16: [8421504, 16711935, 32768], 17: [65280], 18: [255], 19: [8421504, 16711935, 32768], 20: [65280], 21: [255]}, 'widths': {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 5, 9: 3, 10: 3, 11: 3, 12: 3, 13: 3, 14: 3, 15: 3, 16: 3, 17: 3, 18: 3, 19: 3, 20: 3, 21: 3}, 'styles': {1: 0, 4: 0, 7: 0, 10: 0, 13: 0, 16: 0, 19: 0}, 'labels': {1: 'Signal line 1', 2: 'Up Candle 1', 3: 'Down Candle 1', 4: 'Signal line 2', 5: 'Up Candle 2', 6: 'Down Candle 2', 7: 'Signal line 3', 8: 'Up Candle 3', 9: 'Down Candle 3', 10: 'Signal line 4', 11: 'Up Candle 4', 12: 'Down Candle 4', 13: 'Signal line 5', 14: 'Up Candle 5', 15: 'Down Candle 5', 16: 'Signal line 6', 17: 'Up Candle 6', 18: 'Down Candle 6', 19: 'Signal line 7', 20: 'Up Candle 7', 21: 'Down Candle 7'}, 'levels': [], 'description': [''], 'name': 'multicandlesignal', 'source': 'MQL5 Indicators/MultiCandleSignal/multicandlesignal.mq5', 'folder': 'MultiCandleSignal', 'inputs': [{'mql': 'TimeFrame0', 'py': 'TimeFrame0', 'param': 'TimeFrame0', 'type': 'int', 'default': 16408, 'label': '1 Chart period', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16396, 'label': '2 Chart period', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16392, 'label': '3 Chart period', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16390, 'label': '4 Chart period', 'sinput': False}, {'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16388, 'label': '5 Chart period', 'sinput': False}, {'mql': 'TimeFrame5', 'py': 'TimeFrame5', 'param': 'TimeFrame5', 'type': 'int', 'default': 16387, 'label': '6 Chart period', 'sinput': False}, {'mql': 'TimeFrame6', 'py': 'TimeFrame6', 'param': 'TimeFrame6', 'type': 'int', 'default': 16385, 'label': '7 Chart period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame0 = _input('TimeFrame0', PERIOD_D1)  # 1 Chart period
TimeFrame1 = _input('TimeFrame1', PERIOD_H12)  # 2 Chart period
TimeFrame2 = _input('TimeFrame2', PERIOD_H8)  # 3 Chart period
TimeFrame3 = _input('TimeFrame3', PERIOD_H6)  # 4 Chart period
TimeFrame4 = _input('TimeFrame4', PERIOD_H4)  # 5 Chart period
TimeFrame5 = _input('TimeFrame5', PERIOD_H3)  # 6 Chart period
TimeFrame6 = _input('TimeFrame6', PERIOD_H1)  # 7 Chart period
min_rates_total = 0

class CIndBuffers(MqlObject):
    _q_fields = ('m_UpBuffer', 'm_DnBuffer', 'm_LineBuffer', 'm_ColorLineBuffer', 'm_TimeFrame')
    def __init__(self, *args):
        self.m_UpBuffer = Arr(0, 0.0)
        self.m_DnBuffer = Arr(0, 0.0)
        self.m_LineBuffer = Arr(0, 0.0)
        self.m_ColorLineBuffer = Arr(0, 0.0)
        self.m_TimeFrame = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def IndInit(Number):
    if Ind[Number].m_TimeFrame < Period() and Ind[Number].m_TimeFrame != PERIOD_CURRENT:
        Print('IndInit(', Number, '): The Candle indicator chart period cannot be less than the current chart period')
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
    PlotIndexSetInteger(Plot, PLOT_ARROW, 167)
    ArraySetAsSeries(IndBuffer, True)

def InitTsIndColorBuffer(Number, Plot, IndColorBuffer, Draw_Begin):
    SetIndexBuffer(Number, IndColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    ArraySetAsSeries(IndColorBuffer, True)

def IndOnCalculate(Number, Limit, Time, Rates_Total, Prev_Calculated):
    limit_ = 0
    iOpen_ = Arr(1, 0.0, dyn=False)
    iClose_ = Arr(1, 0.0, dyn=False)
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
        Ind[Number].m_LineBuffer[bar] = Number + 1.0
        Ind[Number].m_ColorLineBuffer[bar] = 0.0
        Time0 = Time[bar]
        if CopyTime(Symbol(), Ind[Number].m_TimeFrame, _DT(Time0), 1, Time_) <= 0:
            return (0 != 0)
        if Time0 >= Time_[0] and Time[bar + 1] < Time_[0]:
            _s_IndOnCalculate_LastCountBar[Number] = bar
            if CopyOpen(Symbol(), Ind[Number].m_TimeFrame, _DT(Time0), 1, iOpen_) <= 0:
                return (0 != 0)
            if CopyClose(Symbol(), Ind[Number].m_TimeFrame, _DT(Time0), 1, iClose_) <= 0:
                return (0 != 0)
            if iClose_[0] > iOpen_[0]:
                Ind[Number].m_UpBuffer[bar] = Number + 1.0
                Ind[Number].m_ColorLineBuffer[bar] = 2.0
            if iClose_[0] < iOpen_[0]:
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
    IndicatorSetString(INDICATOR_SHORTNAME, 'MultiCandleSignal')
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Multicandlesignal(_MQL5Indicator):
    name = 'multicandlesignal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # 1 Chart period
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # 2 Chart period
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16392),  # 3 Chart period
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # 4 Chart period
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # 5 Chart period
        'TimeFrame5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16387),  # 6 Chart period
        'TimeFrame6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # 7 Chart period
    }
    y_range = (0.3, 7.9)

