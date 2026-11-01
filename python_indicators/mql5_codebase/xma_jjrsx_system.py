"""xma_jjrsx_system — converted from MQL5: MQL5 Indicators/XMA JJRSX System/xma_jjrsx_system.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16711935], 2: [65280], 3: [255], 4: [32768]}, 'widths': {1: 4, 2: 4, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME" Sell"', 2: 'INDICATOR_NAME" Buy"', 3: 'INDICATOR_NAME" Buy Stop"', 4: 'INDICATOR_NAME" Sell Stop"'}, 'levels': [], 'description': [], 'name': 'xma_jjrsx_system', 'source': 'MQL5 Indicators/XMA JJRSX System/xma_jjrsx_system.mq5', 'folder': 'XMA JJRSX System', 'inputs': [{'mql': 'SignalLableShift', 'py': 'SignalLableShift', 'param': 'SignalLableShift', 'type': 'uint', 'default': 100, 'label': 'Entries vertical shift', 'sinput': False}, {'mql': 'StopLableShift', 'py': 'StopLableShift', 'param': 'StopLableShift', 'type': 'uint', 'default': 300, 'label': 'Stops vertical shift', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Number of submitted alerts', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'Signal bar index, 0 is a current bar', 'sinput': False}, {'mql': 'TimeFrame_XMA', 'py': 'TimeFrame_XMA', 'param': 'TimeFrame_XMA', 'type': 'int', 'default': 16388, 'label': 'XMA chart period', 'sinput': False}, {'mql': 'MA_Method_XMA', 'py': 'MA_Method_XMA', 'param': 'MA_Method_XMA', 'type': 'int', 'default': 7, 'label': 'XMA averaging method', 'sinput': False}, {'mql': 'Length_XMA', 'py': 'Length_XMA', 'param': 'Length_XMA', 'type': 'int', 'default': 12, 'label': 'XMA smoothing depth', 'sinput': False}, {'mql': 'Phase_XMA', 'py': 'Phase_XMA', 'param': 'Phase_XMA', 'type': 'int', 'default': 15, 'label': 'XMA smoothing parameter [-100...+100]', 'sinput': False}, {'mql': 'IPC_XMA', 'py': 'IPC_XMA', 'param': 'IPC_XMA', 'type': 'int', 'default': 1, 'label': 'XMA applied price', 'sinput': False}, {'mql': 'Length_JJRSX', 'py': 'Length_JJRSX', 'param': 'Length_JJRSX', 'type': 'int', 'default': 8, 'label': 'JJRSX smoothing depth', 'sinput': False}, {'mql': 'Smooth_JJRSX', 'py': 'Smooth_JJRSX', 'param': 'Smooth_JJRSX', 'type': 'int', 'default': 8, 'label': 'JJRSX averaging JJMA depth', 'sinput': False}, {'mql': 'Phase_JJRSX', 'py': 'Phase_JJRSX', 'param': 'Phase_JJRSX', 'type': 'int', 'default': 100, 'label': 'JJRSX averaging JJMA parameter [-100..+100]', 'sinput': False}, {'mql': 'IPC_JJRSX', 'py': 'IPC_JJRSX', 'param': 'IPC_JJRSX', 'type': 'int', 'default': 1, 'label': 'JJRSX applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
SignalLableShift = _input('SignalLableShift', 100)  # Entries vertical shift
StopLableShift = _input('StopLableShift', 300)  # Stops vertical shift
AlertCount = _input('AlertCount', 0)  # Number of submitted alerts
SignalBar = _input('SignalBar', 1)  # Signal bar index, 0 is a current bar
TimeFrame_XMA = _input('TimeFrame_XMA', PERIOD_H4)  # XMA chart period
MA_Method_XMA = _input('MA_Method_XMA', MODE_T3)  # XMA averaging method
Length_XMA = _input('Length_XMA', 12)  # XMA smoothing depth
Phase_XMA = _input('Phase_XMA', 15)  # XMA smoothing parameter [-100...+100]
IPC_XMA = _input('IPC_XMA', PRICE_CLOSE)  # XMA applied price
Length_JJRSX = _input('Length_JJRSX', 8)  # JJRSX smoothing depth
Smooth_JJRSX = _input('Smooth_JJRSX', 8)  # JJRSX averaging JJMA depth
Phase_JJRSX = _input('Phase_JJRSX', 100)  # JJRSX averaging JJMA parameter [-100..+100]
IPC_JJRSX = _input('IPC_JJRSX', PRICE_CLOSE_)  # JJRSX applied price
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyStopBuffer = Arr(0, 0.0)
SellStopBuffer = Arr(0, 0.0)
Init = False
Symbol_ = ""
Word = ""
min_rates_total = 0
XMA_Handle = 0
JJRSX_Handle = 0

def OnInit():
    global Init, JJRSX_Handle, Symbol_, Word, XMA_Handle, min_rates_total
    Init = True
    if TimeFrame_XMA < Period() and TimeFrame_XMA != PERIOD_CURRENT:
        Print('XMA indicator chart period cannot be less than the current chart period')
        Init = False
        return 1
    min_rates_total = 36
    Symbol_ = Symbol()
    Word = 'XMA JJRSX System' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    XMA_Handle = iCustom(None, TimeFrame_XMA, 'XMA', MA_Method_XMA, Length_XMA, Phase_XMA, IPC_XMA, 0, 0)
    if XMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the XMA indicator')
        return 2
    JJRSX_Handle = iCustom(None, PERIOD_CURRENT, 'JJRSX', Length_JJRSX, Smooth_JJRSX, Phase_JJRSX, IPC_JJRSX)
    if JJRSX_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the JJRSX indicator')
        return 1
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, BuyStopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyStopBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, SellStopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    ArraySetAsSeries(SellStopBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XMA JJRSX System')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    Comment('XMA JJRSX System')
    return 0

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DnCount, _s_OnCalculate_DnCount_, _s_OnCalculate_StopSignal, _s_OnCalculate_UpCount, _s_OnCalculate_UpCount_
    if (BarsCalculated(JJRSX_Handle) < rates_total or rates_total < min_rates_total) or (not Init):
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    JJRSX = Arr(0, 0.0)
    XMA = Arr(4, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total + 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 4
    if CopyBuffer(JJRSX_Handle, 0, 0, to_copy, JJRSX) <= 0:
        return 0
    ArraySetAsSeries(XMA, True)
    ArraySetAsSeries(JJRSX, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        BuyStopBuffer[bar] = 0.0
        SellStopBuffer[bar] = 0.0
        if CopyBuffer(XMA_Handle, 0, _DT(time[bar]), 4, XMA) <= 0:
            return 0
        if (XMA[1] < XMA[2] and XMA[2] > XMA[3]) and _s_OnCalculate_StopSignal >= 0:
            _s_OnCalculate_StopSignal = -1
            BuyStopBuffer[bar] = high[bar] + (StopLableShift * Point())
        if (XMA[1] > XMA[2] and XMA[2] < XMA[3]) and _s_OnCalculate_StopSignal <= 0:
            _s_OnCalculate_StopSignal = 1
            SellStopBuffer[bar] = low[bar] - (StopLableShift * Point())
        if (JJRSX[bar + 2] < JJRSX[bar + 1] and JJRSX[bar + 1] > JJRSX[bar]) and XMA[3] < XMA[2]:
            SellBuffer[bar] = high[bar] + (SignalLableShift * Point())
        if (JJRSX[bar + 2] > JJRSX[bar + 1] and JJRSX[bar + 1] < JJRSX[bar]) and XMA[3] > XMA[2]:
            BuyBuffer[bar] = low[bar] - (SignalLableShift * Point())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if rates_total != prev_calculated:
        _s_OnCalculate_UpCount = 0
        _s_OnCalculate_DnCount = 0
        _s_OnCalculate_UpCount_ = 0
        _s_OnCalculate_DnCount_ = 0
    if _s_OnCalculate_UpCount < AlertCount and BuyBuffer[SignalBar]:
        _s_OnCalculate_UpCount += 1
        Alert(Word + ': Signal for buying by ' + Symbol_)
    if _s_OnCalculate_DnCount < AlertCount and SellBuffer[SignalBar]:
        _s_OnCalculate_DnCount += 1
        Alert(Word + ': Signal for selling by ' + Symbol_)
    if _s_OnCalculate_UpCount_ < AlertCount and BuyStopBuffer[SignalBar]:
        _s_OnCalculate_UpCount_ += 1
        Alert(Word + ': Signal for exiting short positions by ' + Symbol_)
    if _s_OnCalculate_DnCount_ < AlertCount and SellStopBuffer[SignalBar]:
        _s_OnCalculate_DnCount_ += 1
        Alert(Word + ': Signal for exiting long positions by ' + Symbol_)
    return rates_total

# ---- static local variables
_s_OnCalculate_UpCount = 0
_s_OnCalculate_DnCount = 0
_s_OnCalculate_UpCount_ = 0
_s_OnCalculate_DnCount_ = 0
_s_OnCalculate_StopSignal = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XmaJjrsxSystem(_MQL5Indicator):
    name = 'xma_jjrsx_system'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SignalLableShift': 100,  # Entries vertical shift
        'StopLableShift': 300,  # Stops vertical shift
        'AlertCount': 0,  # Number of submitted alerts
        'SignalBar': 1,  # Signal bar index, 0 is a current bar
        'TimeFrame_XMA': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # XMA chart period
        'MA_Method_XMA': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # XMA averaging method
        'Length_XMA': 12,  # XMA smoothing depth
        'Phase_XMA': 15,  # XMA smoothing parameter [-100...+100]
        'IPC_XMA': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # XMA applied price
        'Length_JJRSX': 8,  # JJRSX smoothing depth
        'Smooth_JJRSX': 8,  # JJRSX averaging JJMA depth
        'Phase_JJRSX': 100,  # JJRSX averaging JJMA parameter [-100..+100]
        'IPC_JJRSX': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # JJRSX applied price
    }

