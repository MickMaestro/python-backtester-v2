"""multimarsisignal — converted from MQL5: MQL5 Indicators/MultiMaRsiSignal/multimarsisignal.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_maximum': 5.9, 'indicator_minimum': 0.4, 'indicator_buffers': 20, 'indicator_plots': 10}, 'types': {1: 8, 2: 12, 3: 8, 4: 12, 5: 8, 6: 12, 7: 8, 8: 12, 9: 8, 10: 12}, 'colors': {1: [16711935, 8421504, 65280], 2: [255, 11119017, 8421376], 3: [16711935, 8421504, 65280], 4: [255, 11119017, 8421376], 5: [16711935, 8421504, 65280], 6: [255, 11119017, 8421376], 7: [16711935, 8421504, 65280], 8: [255, 11119017, 8421376], 9: [16711935, 8421504, 65280], 10: [255, 11119017, 8421376]}, 'widths': {1: 3, 2: 5, 3: 3, 4: 5, 5: 3, 6: 5, 7: 3, 8: 5, 9: 3, 10: 5}, 'styles': {1: 0, 3: 0, 5: 0, 7: 0, 9: 0}, 'labels': {1: 'Signal line 1', 2: 'Trend 1', 3: 'Signal line 2', 4: 'Trend 2', 5: 'Signal line 3', 6: 'Trend 3', 7: 'Signal line 4', 8: 'Trend 4', 9: 'Signal line 5', 10: 'Trend 5'}, 'levels': [], 'description': [''], 'name': 'multimarsisignal', 'source': 'MQL5 Indicators/MultiMaRsiSignal/multimarsisignal.mq5', 'folder': 'MultiMaRsiSignal', 'inputs': [{'mql': 'TimeFrame0', 'py': 'TimeFrame0', 'param': 'TimeFrame0', 'type': 'int', 'default': 16396, 'label': '1 Chart period', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16392, 'label': '2 Chart period', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16388, 'label': '3 Chart period', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16386, 'label': '4 Chart period', 'sinput': False}, {'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16385, 'label': '5 Chart period', 'sinput': False}, {'mql': 'nPeriodRsi', 'py': 'nPeriodRsi', 'param': 'nPeriodRsi', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'nRSIPrice', 'py': 'nRSIPrice', 'param': 'nRSIPrice', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'nPeriodRsiLong', 'py': 'nPeriodRsiLong', 'param': 'nPeriodRsiLong', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'nRSIPriceLong', 'py': 'nRSIPriceLong', 'param': 'nRSIPriceLong', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'nPeriodMa', 'py': 'nPeriodMa', 'param': 'nPeriodMa', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'nMAType', 'py': 'nMAType', 'param': 'nMAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'nMAPrice', 'py': 'nMAPrice', 'param': 'nMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'nPeriodMaLong', 'py': 'nPeriodMaLong', 'param': 'nPeriodMaLong', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'nMATypeLong', 'py': 'nMATypeLong', 'param': 'nMATypeLong', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'nMAPriceLong', 'py': 'nMAPriceLong', 'param': 'nMAPriceLong', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame0 = _input('TimeFrame0', PERIOD_H12)  # 1 Chart period
TimeFrame1 = _input('TimeFrame1', PERIOD_H8)  # 2 Chart period
TimeFrame2 = _input('TimeFrame2', PERIOD_H4)  # 3 Chart period
TimeFrame3 = _input('TimeFrame3', PERIOD_H2)  # 4 Chart period
TimeFrame4 = _input('TimeFrame4', PERIOD_H1)  # 5 Chart period
nPeriodRsi = _input('nPeriodRsi', 3)
nRSIPrice = _input('nRSIPrice', PRICE_WEIGHTED)
nPeriodRsiLong = _input('nPeriodRsiLong', 13)
nRSIPriceLong = _input('nRSIPriceLong', PRICE_MEDIAN)
nPeriodMa = _input('nPeriodMa', 5)
nMAType = _input('nMAType', MODE_EMA)
nMAPrice = _input('nMAPrice', PRICE_CLOSE)
nPeriodMaLong = _input('nPeriodMaLong', 10)
nMATypeLong = _input('nMATypeLong', MODE_EMA)
nMAPriceLong = _input('nMAPriceLong', PRICE_CLOSE)
Init = False
min_rates_total = 0

class CIndBuffers(MqlObject):
    _q_fields = ('m_ArrayBuffer', 'm_ColorArrayBuffer', 'm_LineBuffer', 'm_ColorLineBuffer', 'm_Handle', 'm_TimeFrame')
    def __init__(self, *args):
        self.m_ArrayBuffer = Arr(0, 0.0)
        self.m_ColorArrayBuffer = Arr(0, 0.0)
        self.m_LineBuffer = Arr(0, 0.0)
        self.m_ColorLineBuffer = Arr(0, 0.0)
        self.m_Handle = Arr(4, 0, dyn=False)
        self.m_TimeFrame = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def IndInit(Number):
    global Init
    if Ind[Number].m_TimeFrame < Period() and Ind[Number].m_TimeFrame != PERIOD_CURRENT:
        Print('IndInit(', Number, '): MaRsi indicator chart period cannot be less than the current chart period')
        Init = False
        return False
    Ind[Number].m_Handle[0] = iRSI(None, Ind[Number].m_TimeFrame, nPeriodRsi, nRSIPrice)
    Ind[Number].m_Handle[1] = iRSI(None, Ind[Number].m_TimeFrame, nPeriodRsiLong, nRSIPriceLong)
    Ind[Number].m_Handle[2] = iMA(None, Ind[Number].m_TimeFrame, nPeriodMa, 0, nMAType, nMAPrice)
    Ind[Number].m_Handle[3] = iMA(None, Ind[Number].m_TimeFrame, nPeriodMaLong, 0, nMATypeLong, nMAPriceLong)
    if Ind[Number].m_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI indicator')
        Init = False
        return False
    if Ind[Number].m_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI indicator')
        Init = False
        return False
    if Ind[Number].m_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        Init = False
        return False
    if Ind[Number].m_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        Init = False
        return False
    BIndex = (Number * 4) + 0
    PIndex = (Number * 2) + 0
    InitTsIndBuffer(BIndex, PIndex, Ind[Number].m_LineBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 1, PIndex, Ind[Number].m_ColorLineBuffer, min_rates_total)
    InitTsIndArrBuffer(BIndex + 2, PIndex + 1, Ind[Number].m_ArrayBuffer, EMPTY_VALUE, min_rates_total)
    InitTsIndColorBuffer(BIndex + 3, PIndex + 1, Ind[Number].m_ColorArrayBuffer, min_rates_total)
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
    PlotIndexSetInteger(Plot, PLOT_ARROW, 115)
    ArraySetAsSeries(IndBuffer, True)

def InitTsIndColorBuffer(Number, Plot, IndColorBuffer, Draw_Begin):
    SetIndexBuffer(Number, IndColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    ArraySetAsSeries(IndColorBuffer, True)

def IndOnCalculate(Number, Limit, Time, Rates_Total, Prev_Calculated):
    limit_ = 0
    MA0 = Arr(1, 0.0, dyn=False)
    MA1 = Arr(1, 0.0, dyn=False)
    RSI0 = Arr(1, 0.0, dyn=False)
    RSI1 = Arr(1, 0.0, dyn=False)
    Time_ = Arr(1, 0, dyn=False)
    Time0 = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        _s_IndOnCalculate_LastCountBar[Number] = Rates_Total
        limit_ = Limit
    else:
        limit_ = _int(_s_IndOnCalculate_LastCountBar[Number]) + Limit
    for bar in range(_int(limit_), 0 - 1, -1):
        Ind[Number].m_ArrayBuffer[bar] = EMPTY_VALUE
        Ind[Number].m_LineBuffer[bar] = Number + 1
        Ind[Number].m_ColorArrayBuffer[bar] = EMPTY_VALUE
        Ind[Number].m_ColorLineBuffer[bar] = 0.0
        Time0 = Time[bar]
        if CopyTime(Symbol(), Ind[Number].m_TimeFrame, _DT(Time0), 1, Time_) <= 0:
            return (0 != 0)
        if Time0 >= Time_[0] and Time[bar + 1] < Time_[0]:
            _s_IndOnCalculate_LastCountBar[Number] = bar
            if CopyBuffer(Ind[Number].m_Handle[0], 0, _DT(Time0), 1, MA0) <= 0:
                return (0 != 0)
            if CopyBuffer(Ind[Number].m_Handle[1], 0, _DT(Time0), 1, MA1) <= 0:
                return (0 != 0)
            if CopyBuffer(Ind[Number].m_Handle[2], 0, _DT(Time0), 1, RSI0) <= 0:
                return (0 != 0)
            if CopyBuffer(Ind[Number].m_Handle[3], 0, _DT(Time0), 1, RSI1) <= 0:
                return (0 != 0)
            res = 0
            if MA0[0] > MA1[0]:
                res = 1
            if MA0[0] < MA1[0]:
                res = -1
            if RSI0[0] > RSI1[0]:
                res += 1
            if RSI0[0] < RSI1[0]:
                res -= 1
            res = MathMax(MathMin(1, res), -1) + 1
            numb = _int(Number + 1)
            Ind[Number].m_ArrayBuffer[bar] = numb
            Ind[Number].m_LineBuffer[bar] = numb
            Ind[Number].m_ColorArrayBuffer[bar] = res
            Ind[Number].m_ColorLineBuffer[bar] = res
        if Ind[Number].m_ArrayBuffer[bar] == EMPTY_VALUE:
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
    Ind[4].m_TimeFrame = TimeFrame4
    for count in range(0, 5):
        if not IndInit(count):
            Init = False
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'MultiMaRsiSignal')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or (not Init):
        return 0
    for count in range(0, 5):
        for iii in range(0, 4):
            if BarsCalculated(Ind[count].m_Handle[iii]) < Bars(Symbol(), Ind[count].m_TimeFrame):
                return prev_calculated
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    for count in range(0, 5):
        if not IndOnCalculate(count, limit, time, rates_total, prev_calculated):
            return 0
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(5, 0, dyn=False, factory=CIndBuffers)

# ---- static local variables
_s_IndOnCalculate_LastCountBar = Arr(5, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Multimarsisignal(_MQL5Indicator):
    name = 'multimarsisignal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # 1 Chart period
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16392),  # 2 Chart period
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # 3 Chart period
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16386),  # 4 Chart period
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # 5 Chart period
        'nPeriodRsi': 3,
        'nRSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),
        'nPeriodRsiLong': 13,
        'nRSIPriceLong': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),
        'nPeriodMa': 5,
        'nMAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'nMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'nPeriodMaLong': 10,
        'nMATypeLong': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'nMAPriceLong': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }
    y_range = (0.4, 5.9)

