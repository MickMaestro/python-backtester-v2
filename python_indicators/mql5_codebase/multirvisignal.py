"""multirvisignal — converted from MQL5: MQL5 Indicators/MultiRVISignal/multirvisignal.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 16, 'indicator_plots': 12}, 'types': {1: 8, 2: 5, 3: 5, 4: 8, 5: 5, 6: 5, 7: 8, 8: 5, 9: 5, 10: 8, 11: 5, 12: 5}, 'colors': {1: [8421504, 255, 5737262], 2: [3329330], 3: [16711935], 4: [8421504, 255, 5737262], 5: [3329330], 6: [16711935], 7: [8421504, 255, 5737262], 8: [3329330], 9: [16711935], 10: [8421504, 255, 5737262], 11: [3329330], 12: [16711935]}, 'widths': {1: 3, 2: 5, 3: 5, 4: 3, 5: 5, 6: 5, 7: 3, 8: 5, 9: 5, 10: 3, 11: 5, 12: 5}, 'styles': {1: 0, 4: 0, 7: 0, 10: 0}, 'labels': {1: 'Signal line 1', 2: 'Up RVI 1', 3: 'Down RVI 1', 4: 'Signal line 2', 5: 'Up RVI 2', 6: 'Down RVI 2', 7: 'Signal line 3', 8: 'Up RVI 3', 9: 'Down RVI 3', 10: 'Signal line 4', 11: 'Up RVI 4', 12: 'Down RVI 4'}, 'levels': [], 'description': [''], 'name': 'multirvisignal', 'source': 'MQL5 Indicators/MultiRVISignal/multirvisignal.mq5', 'folder': 'MultiRVISignal', 'inputs': [{'mql': 'TimeFrame0', 'py': 'TimeFrame0', 'param': 'TimeFrame0', 'type': 'int', 'default': 16396, 'label': '1 Chart period', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16390, 'label': '2 Chart period', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16387, 'label': '3 Chart period', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16385, 'label': '4 Chart period', 'sinput': False}, {'mql': 'RVIPeriod', 'py': 'RVIPeriod', 'param': 'RVIPeriod', 'type': 'uint', 'default': 12, 'label': 'RVI period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame0 = _input('TimeFrame0', PERIOD_H12)  # 1 Chart period
TimeFrame1 = _input('TimeFrame1', PERIOD_H6)  # 2 Chart period
TimeFrame2 = _input('TimeFrame2', PERIOD_H3)  # 3 Chart period
TimeFrame3 = _input('TimeFrame3', PERIOD_H1)  # 4 Chart period
RVIPeriod = _input('RVIPeriod', 12)  # RVI period
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

def IndInit(Number, RVI_Period):
    global Init
    if Ind[Number].m_TimeFrame < Period() and Ind[Number].m_TimeFrame != PERIOD_CURRENT:
        Print('IndInit(', Number, '): The RVI indicator chart period cannot be less than the current chart period')
        Init = False
        return False
    Ind[Number].m_Handle = iRVI(None, Ind[Number].m_TimeFrame, RVI_Period)
    if Ind[Number].m_Handle == INVALID_HANDLE:
        Print('IndInit(', Number, '): Failed to get the RVI indicator handle')
        Init = False
        return False
    Numb = (Number * 4) + 0
    SetIndexBuffer(Numb, Ind[Number].m_LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Numb, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(Numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind[Number].m_LineBuffer, True)
    Numb += 1
    SetIndexBuffer(Numb, Ind[Number].m_ColorLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(Numb, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Ind[Number].m_ColorLineBuffer, True)
    Numb += 1
    if not SetIndexBuffer(Numb, Ind[Number].m_UpBuffer, INDICATOR_DATA):
        PlotIndexSetInteger(Numb, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(Numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind[Number].m_UpBuffer, True)
    Numb += 1
    SetIndexBuffer(Numb, Ind[Number].m_DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Numb, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(Numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind[Number].m_DnBuffer, True)
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
        if not IndInit(count, RVIPeriod):
            Init = False
            return INIT_FAILED
    shortname = Box("")
    StringConcatenate(shortname, 'MultiRVISignal( ', RVIPeriod, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def IndOnCalculate(Number, Limit, Time, Rates_Total, Prev_Calculated):
    limit_ = 0
    Main = Arr(1, 0.0, dyn=False)
    Signal = Arr(1, 0.0, dyn=False)
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
        Ind[Number].m_LineBuffer[bar] = Number
        Ind[Number].m_ColorLineBuffer[bar] = 0.0
        Time0 = Time[bar]
        if CopyTime(Symbol(), Ind[Number].m_TimeFrame, _DT(Time0), 1, Time_) <= 0:
            return (0 != 0)
        if Time0 >= Time_[0] and Time[bar + 1] < Time_[0]:
            _s_IndOnCalculate_LastCountBar[Number] = bar
            if CopyBuffer(Ind[Number].m_Handle, MAIN_LINE, _DT(Time0), 1, Main) <= 0:
                return (0 != 0)
            if CopyBuffer(Ind[Number].m_Handle, SIGNAL_LINE, _DT(Time0), 1, Signal) <= 0:
                return (0 != 0)
            if Main[0] > Signal[0]:
                Ind[Number].m_UpBuffer[bar] = Number
                Ind[Number].m_ColorLineBuffer[bar] = 2.0
            if Main[0] < Signal[0]:
                Ind[Number].m_DnBuffer[bar] = Number
                Ind[Number].m_ColorLineBuffer[bar] = 1.0
        if Ind[Number].m_ColorLineBuffer[bar + 1] and (not Ind[Number].m_ColorLineBuffer[bar]):
            Ind[Number].m_ColorLineBuffer[bar] = Ind[Number].m_ColorLineBuffer[bar + 1]
    return True

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


class Multirvisignal(_MQL5Indicator):
    name = 'multirvisignal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # 1 Chart period
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # 2 Chart period
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16387),  # 3 Chart period
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # 4 Chart period
        'RVIPeriod': 12,  # RVI period
    }

