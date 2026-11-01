"""jfatlspeed_htf — converted from MQL5: MQL5 Indicators/JFatlSpeed HTF/jfatlspeed_htf.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [255], 2: [65280], 3: [16711935], 4: [65535]}, 'widths': {1: 4, 2: 4, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME" Sell Max"', 2: 'INDICATOR_NAME" Buy Max"', 3: 'INDICATOR_NAME" Sell Min"', 4: 'INDICATOR_NAME" Buy Min"'}, 'levels': [], 'description': [], 'name': 'jfatlspeed_htf', 'source': 'MQL5 Indicators/JFatlSpeed HTF/jfatlspeed_htf.mq5', 'folder': 'JFatlSpeed HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'LableShift', 'py': 'LableShift', 'param': 'LableShift', 'type': 'uint', 'default': 100, 'label': 'Labels vertical shift', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Number of alerts', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'Signal bar index, 0 is a current bar', 'sinput': False}, {'mql': 'Length_', 'py': 'Length_', 'param': 'Length_', 'type': 'int', 'default': 8, 'label': 'JMA period of Fatl smoothing', 'sinput': False}, {'mql': 'Phase_', 'py': 'Phase_', 'param': 'Phase_', 'type': 'int', 'default': 100, 'label': 'JMA parameter of Fatl smoothing,', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'int', 'default': 1, 'label': 'Momentum indicator period for rate measuring', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'int', 'default': 2, 'label': 'Depth of the JMA smoothing of the indicator', 'sinput': False}, {'mql': 'SmPhase', 'py': 'SmPhase', 'param': 'SmPhase', 'type': 'int', 'default': 100, 'label': 'Parameter of the JMA smoothing of the indicator', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
LableShift = _input('LableShift', 100)  # Labels vertical shift
AlertCount = _input('AlertCount', 0)  # Number of alerts
SignalBar = _input('SignalBar', 1)  # Signal bar index, 0 is a current bar
Length_ = _input('Length_', 8)  # JMA period of Fatl smoothing
Phase_ = _input('Phase_', 100)  # JMA parameter of Fatl smoothing,
MomPeriod = _input('MomPeriod', 1)  # Momentum indicator period for rate measuring
Smooth = _input('Smooth', 2)  # Depth of the JMA smoothing of the indicator
SmPhase = _input('SmPhase', 100)  # Parameter of the JMA smoothing of the indicator
IPC = _input('IPC', PRICE_CLOSE_)  # price constant
BuyMaxBuffer = Arr(0, 0.0)
SellMaxBuffer = Arr(0, 0.0)
BuyMinBuffer = Arr(0, 0.0)
SellMinBuffer = Arr(0, 0.0)
Init = False
Symbol_ = ""
Word = ""
min_rates_total = 0
JFAccel_Handle = 0

def OnInit():
    global Init, JFAccel_Handle, Symbol_, Word, min_rates_total
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('ColorJFatlSpeed indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    min_rates_total = _idiv((39 + 30 + MomPeriod + 30 + 1) * PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT))
    Symbol_ = Symbol()
    Word = 'JFatl Speed' + ' indicator: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    JFAccel_Handle = iCustom(Symbol_, TimeFrame, 'ColorJFatlSpeed', Length_, Phase_, MomPeriod, Smooth, SmPhase, IPC, 0)
    if JFAccel_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ColorJFatlSpeed indicator')
        return INIT_FAILED
    SetIndexBuffer(0, SellMaxBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 174)
    ArraySetAsSeries(SellMaxBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyMaxBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 174)
    ArraySetAsSeries(BuyMaxBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellMinBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 174)
    ArraySetAsSeries(SellMinBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, BuyMinBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 174)
    ArraySetAsSeries(BuyMinBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'JFatl Speed')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DnCount, _s_OnCalculate_DnCount_, _s_OnCalculate_LastCountBar, _s_OnCalculate_UpCount, _s_OnCalculate_UpCount_
    if rates_total < min_rates_total or (not Init):
        return 0
    if BarsCalculated(JFAccel_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    JFAccel = Arr(2, 0.0, dyn=False)
    limit = 0
    bar = 0
    JFAccelTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyMaxBuffer[bar] = 0.0
        SellMaxBuffer[bar] = 0.0
        BuyMinBuffer[bar] = 0.0
        SellMinBuffer[bar] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, JFAccelTime) <= 0:
            return 0
        if time[bar] >= JFAccelTime[0] and time[bar + 1] < JFAccelTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(JFAccel_Handle, 0, _DT(time[bar]), 2, JFAccel) <= 0:
                return 0
            if JFAccel[1] < 0:
                if JFAccel[0] > JFAccel[1]:
                    SellMaxBuffer[bar] = high[bar] + (LableShift * Point())
                else:
                    SellMinBuffer[bar] = high[bar] + (LableShift * Point())
            else:
                if JFAccel[0] > JFAccel[1]:
                    BuyMinBuffer[bar] = low[bar] - (LableShift * Point())
                else:
                    BuyMaxBuffer[bar] = low[bar] - (LableShift * Point())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if rates_total != prev_calculated:
        _s_OnCalculate_UpCount = 0
        _s_OnCalculate_DnCount = 0
        _s_OnCalculate_UpCount_ = 0
        _s_OnCalculate_DnCount_ = 0
    if _s_OnCalculate_UpCount < AlertCount and BuyMaxBuffer[SignalBar]:
        _s_OnCalculate_UpCount += 1
        Alert(Word + ': Strong signal for buying by ' + Symbol_)
    if _s_OnCalculate_DnCount < AlertCount and SellMaxBuffer[SignalBar]:
        _s_OnCalculate_DnCount += 1
        Alert(Word + ': Strong signal for buying by ' + Symbol_)
    if _s_OnCalculate_UpCount_ < AlertCount and BuyMinBuffer[SignalBar]:
        _s_OnCalculate_UpCount_ += 1
        Alert(Word + ': Weak signal for buying by ' + Symbol_)
    if _s_OnCalculate_DnCount_ < AlertCount and SellMinBuffer[SignalBar]:
        _s_OnCalculate_DnCount_ += 1
        Alert(Word + ': Weak signal for selling by ' + Symbol_)
    return rates_total

# ---- static local variables
_s_OnCalculate_UpCount = 0
_s_OnCalculate_DnCount = 0
_s_OnCalculate_UpCount_ = 0
_s_OnCalculate_DnCount_ = 0
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JfatlspeedHtf(_MQL5Indicator):
    name = 'jfatlspeed_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'LableShift': 100,  # Labels vertical shift
        'AlertCount': 0,  # Number of alerts
        'SignalBar': 1,  # Signal bar index, 0 is a current bar
        'Length_': 8,  # JMA period of Fatl smoothing
        'Phase_': 100,  # JMA parameter of Fatl smoothing,
        'MomPeriod': 1,  # Momentum indicator period for rate measuring
        'Smooth': 2,  # Depth of the JMA smoothing of the indicator
        'SmPhase': 100,  # Parameter of the JMA smoothing of the indicator
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # price constant
    }

