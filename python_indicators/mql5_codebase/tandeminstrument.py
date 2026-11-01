"""tandeminstrument — converted from MQL5: MQL5 Indicators/TandemInstrument/tandeminstrument.mq5

Copyright: Copyright 2012, Evgeniy Trofimov; Link: https://login.mql5.com/ru/users/EvgeTrofi; Version: 1.15

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Missing include files: MyMQL_v2.1.mqh
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Evgeniy Trofimov', 'link': 'https://login.mql5.com/ru/users/EvgeTrofi', 'version': '1.15', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421376, 6333684]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'tandeminstrument', 'source': 'MQL5 Indicators/TandemInstrument/tandeminstrument.mq5', 'folder': 'TandemInstrument', 'inputs': [{'mql': 'S', 'py': 'S', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Indirect instrument', 'sinput': False}, {'mql': 'P', 'py': 'P', 'param': 'P', 'type': 'int', 'default': 400, 'label': 'Field of training', 'sinput': False}, {'mql': 'Optimum', 'py': 'Optimum', 'param': 'Optimum', 'type': 'int', 'default': 50, 'label': 'Interval of retraining', 'sinput': False}, {'mql': 'Correlation', 'py': 'Correlation', 'param': 'Correlation', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': ['MyMQL_v2.1.mqh'], 'imports': [], 'libraries': []}

# enum Corr
Direct = 0
Indirect = 1
_enum('Corr', {0: 'Direct', 1: 'Indirect'})

# ---- inputs and global variables
S = _input('S', 'GBPUSD')  # Indirect instrument
P = _input('P', 400)  # Field of training
Optimum = _input('Optimum', 50)  # Interval of retraining
Correlation = _input('Correlation', Direct)
K = 0.0  # The density coefficient of indirect instrument
High_Win = 0.0  # Maximum price of basic instrument
Low_Win = 0.0  # Minimum price of basic instrument
L = 0.0  # Minimum price of indirect instrument
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
LastOptimization = 0

def OnInit():
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetString(0, PLOT_LABEL, S + ' Open;' + S + ' High;' + S + ' Low;' + S + ' Close')
    IndicatorSetString(INDICATOR_SHORTNAME, S)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LastOptimization, _s_OnCalculate_LastTime
    ArraySetAsSeries(time, True)
    beg = rates_total - prev_calculated - 1
    if ExtOpenBuffer[1] == 0.0:
        beg = rates_total - 2
        _s_OnCalculate_LastTime = 0
        LastOptimization = 0
    for i in range(beg, 0 - 1, -1):
        if _s_OnCalculate_LastTime < time[i]:
            ExtOpenBuffer[i] = 0.0
            ExtHighBuffer[i] = 0.0
            ExtLowBuffer[i] = 0.0
            ExtCloseBuffer[i] = 0.0
            if Optimum > 0:
                if (LastOptimization + (Optimum * (iTime(Symbol(), Period(), i) - iTime(Symbol(), Period(), i + 1)))) < iTime(Symbol(), Period(), i):
                    Optimization(i, P)
                    LastOptimization = iTime(Symbol(), Period(), i)
            IndicatorPrint(i, rates_total)
            _s_OnCalculate_LastTime = time[i]
    IndicatorPrint(0, rates_total)
    txt = 'compressed'
    if K > 1:
        txt = 'extended'
    Comment('/The density coefficient of indirect instrument ' + S + ': ' + DoubleToString(K, 5) + ' (' + txt + ')')
    return rates_total

def Optimization(fBegin=0, fLen=200):
    global High_Win, K, L, Low_Win
    if Symbol() == S:
        Print('choose the same currency pairs ' + S + '!!!')
    High_Win = GetExtremumPrice(Symbol(), Period(), fBegin, fLen, 0)
    Low_Win = GetExtremumPrice(Symbol(), Period(), fBegin, fLen, 1)
    H = GetExtremumPrice(S, Period(), fBegin, fLen, 0)
    L = GetExtremumPrice(S, Period(), fBegin, fLen, 1)
    if (H - L) == 0:
        K = 1.0
    else:
        K = _fdiv(High_Win - Low_Win, H - L)

def GetExtremumPrice(fSymbol, fTF, fBegin=0, fLen=1, fType=0):
    Prices = Arr(0, 0.0)
    i = 0
    ArraySetAsSeries(Prices, True)
    if fType == 0:
        CopyHigh(fSymbol, fTF, fBegin, fLen, Prices)
        i = ArrayMaximum(Prices)
    else:
        CopyLow(fSymbol, fTF, fBegin, fLen, Prices)
        i = ArrayMinimum(Prices)
    return Prices[i]

def IndicatorPrint(Candle, rates_total):
    global LastOptimization
    Candle2 = iBarShift(S, Period(), iTime(Symbol(), Period(), Candle))
    Candle2Last = iBarShift(S, Period(), iTime(Symbol(), Period(), Candle + 1))
    ExtOpenBuffer[Candle] = (K * (iOpen(S, Period(), Candle2) - L)) + Low_Win
    ExtHighBuffer[Candle] = (K * (iHigh(S, Period(), Candle2) - L)) + Low_Win
    ExtLowBuffer[Candle] = (K * (iLow(S, Period(), Candle2) - L)) + Low_Win
    ExtCloseBuffer[Candle] = (K * (iClose(S, Period(), Candle2) - L)) + Low_Win
    if Correlation == Indirect:
        ExtOpenBuffer[Candle] = High_Win - (ExtOpenBuffer[Candle] - Low_Win)
        ExtCloseBuffer[Candle] = High_Win - (ExtCloseBuffer[Candle] - Low_Win)
        ExtHighBuffer[Candle] = High_Win - (ExtHighBuffer[Candle] - Low_Win)
        ExtLowBuffer[Candle] = High_Win - (ExtLowBuffer[Candle] - Low_Win)
    if ExtOpenBuffer[Candle] > ExtCloseBuffer[Candle]:
        ExtColorBuffer[Candle] = 0.0
    else:
        ExtColorBuffer[Candle] = 1.0
    if (Candle + 1) > (rates_total - 1):
        return
    if (ExtCloseBuffer[Candle + 1] > iClose(S, Period(), Candle2Last) and ExtCloseBuffer[Candle] < iClose(S, Period(), Candle2)) or (ExtCloseBuffer[Candle + 1] < iClose(S, Period(), Candle2Last) and ExtCloseBuffer[Candle] > iClose(S, Period(), Candle2)):
        LastOptimization = 0

# ---- static local variables
_s_OnCalculate_LastTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tandeminstrument(_MQL5Indicator):
    name = 'tandeminstrument'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'P': 400,  # Field of training
        'Optimum': 50,  # Interval of retraining
        'Correlation': _Choice({0: 'Direct', 1: 'Indirect'}, default=0),
    }

