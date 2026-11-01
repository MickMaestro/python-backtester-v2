"""nrtr_rosh_v2 — converted from MQL5: MQL5 Indicators/NRTR Rosh v2/nrtr_rosh_v2.mq5

Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [255], 2: [65280], 3: [16776960], 4: [16711935]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {}, 'labels': {1: 'Sell', 2: 'Buy', 3: 'Ceil', 4: 'Floor'}, 'levels': [], 'description': [], 'name': 'nrtr_rosh_v2', 'source': 'MQL5 Indicators/NRTR Rosh v2/nrtr_rosh_v2.mq5', 'folder': 'NRTR Rosh v2', 'inputs': [{'mql': 'PerATR', 'py': 'PerATR', 'param': 'PerATR', 'type': 'int', 'default': 40, 'label': '', 'sinput': False}, {'mql': 'kATR', 'py': 'kATR', 'param': 'kATR', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'useSendMail', 'py': 'useSendMail', 'param': 'useSendMail', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PerATR = _input('PerATR', 40)
kATR = _input('kATR', 2.0)
useSendMail = _input('useSendMail', False)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
Ceil = Arr(0, 0.0)
Floor = Arr(0, 0.0)
Trend = Arr(0, 0.0)
ATR = Arr(0, 0.0)
Handle_v = 0

def OnInit():
    global Handle_v
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 251)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(1, PLOT_LABEL, 'Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 251)
    ArraySetAsSeries(BuyBuffer, True)
    SetIndexBuffer(2, Ceil, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(2, PLOT_LABEL, 'Ceil')
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    ArraySetAsSeries(Ceil, True)
    SetIndexBuffer(3, Floor, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(3, PLOT_LABEL, 'Floor')
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    ArraySetAsSeries(Floor, True)
    SetIndexBuffer(4, Trend, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Trend, True)
    SetIndexBuffer(5, ATR, INDICATOR_DATA)
    ArraySetAsSeries(ATR, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'NRTR Rosh')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    Handle_v = iATR(None, 0, PerATR)
    if Handle_v == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')

def BreakDown(shift, Close):
    if Close[shift] > SellBuffer[shift + 1]:
        return True
    return False

def BreakUp(shift, Close):
    if Close[shift] < BuyBuffer[shift + 1]:
        return True
    return False

def BreakFloor(shift, High):
    if High[shift] < Floor[shift + 1]:
        return True
    return False

def BreakCeil(shift, Low):
    if Low[shift] > Ceil[shift + 1]:
        return True
    return False

def Uptrend(shift):
    result = False
    if Trend[shift + 1] == 1:
        result = True
    if Trend[shift + 1] == -1:
        result = False
    if Trend[shift + 1] != 1 and Trend[shift + 1] != -1:
        Print('Attention! Trend is not determined, abnormal situation. Bar from the end ', Bars(None, 0) - shift)
    return result

def NewCeil(shift, Close):
    Ceil[shift] = Close[shift]
    Floor[shift] = 0.0

def NewFloor(shift, Close):
    Floor[shift] = Close[shift]
    Ceil[shift] = 0.0

def SetBuyBuffer(shift, Close):
    BuyBuffer[shift] = Close[shift] - (kATR * ATR[shift])
    SellBuffer[shift] = 0.0

def SetSellBuffer(shift, Close):
    SellBuffer[shift] = Close[shift] + (kATR * ATR[shift])
    BuyBuffer[shift] = 0.0

def NewTrend(shift, Close):
    if Trend[shift + 1] == 1:
        Trend[shift] = -1.0
        NewFloor(shift, Close)
        SetSellBuffer(shift, Close)
    else:
        Trend[shift] = 1.0
        NewCeil(shift, Close)
        SetBuyBuffer(shift, Close)
    if Trend[shift + 1] != 1 and Trend[shift + 1] != -1:
        Print('Attention! Trend is not determined, abnormal situation')

def CopyLastValues(shift):
    SellBuffer[shift] = SellBuffer[shift + 1]
    BuyBuffer[shift] = BuyBuffer[shift + 1]
    Ceil[shift] = Ceil[shift + 1]
    Floor[shift] = Floor[shift + 1]
    Trend[shift] = Trend[shift + 1]

def SendSMS(shift):
    if ((IsNewBar() and (Trend[shift + 1] * Trend[shift + 2]) == -1) and shift == 0) and useSendMail:
        if Trend[shift + 1] == 1:
            SendMail('NRTR ', Symbol() + ' ' + EnumToString(Period(), '') + ' turned upwards, Ask = ' + DoubleToString(SymbolInfoDouble(None, SYMBOL_ASK), Digits()))
        else:
            SendMail('NRTR ', Symbol() + ' ' + EnumToString(Period(), '') + ' turned downwards, Bid = ' + DoubleToString(SymbolInfoDouble(None, SYMBOL_BID), Digits()))

def IsNewBar():
    global _s_IsNewBar_Told
    Tnew = Arr(1, 0, dyn=False)
    CopyTime(Symbol(), 0, 0, 1, Tnew)
    if Tnew[0] != _s_IsNewBar_Told:
        _s_IsNewBar_Told = Tnew[0]
        return True
    return False

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (PerATR - 1):
        return 0
    limit = 0
    to_copy = 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - PerATR - 1
        to_copy = rates_total
        if CopyBuffer(Handle_v, 0, 0, to_copy, ATR) <= 0:
            return 0
        closeX = close[limit + 1]
        openX = open[limit + 1]
        if closeX > openX:
            Trend[limit + 1] = 1.0
            Ceil[limit + 1] = closeX
            BuyBuffer[limit + 1] = closeX - (kATR * ATR[limit + 1])
        if closeX < openX:
            Trend[limit + 1] = -1.0
            Floor[limit + 1] = closeX
            SellBuffer[limit + 1] = closeX + (kATR * ATR[limit + 1])
        if closeX == openX:
            Trend[limit + 1] = 1.0
            Ceil[limit + 1] = closeX
            BuyBuffer[limit + 1] = closeX - (kATR * ATR[limit + 1])
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
        if CopyBuffer(Handle_v, 0, 0, to_copy, ATR) <= 0:
            return 0
    for cnt in range(limit, 0 - 1, -1):
        Trend[cnt] = 0.0
        if Uptrend(cnt):
            if BreakCeil(cnt, low):
                NewCeil(cnt, close)
                SetBuyBuffer(cnt, close)
                Trend[cnt] = 1.0
                continue
            if BreakUp(cnt, close):
                NewTrend(cnt, close)
                continue
            CopyLastValues(cnt)
        else:
            if BreakFloor(cnt, high):
                NewFloor(cnt, close)
                SetSellBuffer(cnt, close)
                Trend[cnt] = -1.0
                continue
            if BreakDown(cnt, close):
                NewTrend(cnt, close)
                continue
            CopyLastValues(cnt)
    return rates_total

# ---- static local variables
_s_IsNewBar_Told = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NrtrRoshV2(_MQL5Indicator):
    name = 'nrtr_rosh_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PerATR': 40,
        'kATR': 2.0,
        'useSendMail': False,
    }

