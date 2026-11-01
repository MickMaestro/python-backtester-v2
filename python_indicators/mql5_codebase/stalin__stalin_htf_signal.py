"""Stalin — converted from MQL5: MQL5 Indicators/Stalin_HTF_Signal/Stalin.mq5

Copyright: Copyright © 2011, Andrey Vassiliev (MoneyJinn); Link: http://www.vassiliev.ru/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Andrey Vassiliev (MoneyJinn)', 'link': 'http://www.vassiliev.ru/', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [12695295], 2: [16436871]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Stalin Sell', 2: 'Stalin Buy'}, 'levels': [], 'description': [], 'name': 'Stalin', 'source': 'MQL5 Indicators/Stalin_HTF_Signal/Stalin.mq5', 'folder': 'Stalin_HTF_Signal', 'inputs': [{'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Fast', 'py': 'Fast', 'param': 'Fast', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Slow', 'py': 'Slow', 'param': 'Slow', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'RSI', 'py': 'RSI', 'param': 'RSI', 'type': 'int', 'default': 17, 'label': '', 'sinput': False}, {'mql': 'Confirm', 'py': 'Confirm', 'param': 'Confirm', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Flat', 'py': 'Flat', 'param': 'Flat', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SoundAlert', 'py': 'SoundAlert', 'param': 'SoundAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EmailAlert', 'py': 'EmailAlert', 'param': 'EmailAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAMethod = _input('MAMethod', MODE_EMA)
MAShift = _input('MAShift', 0)
Fast = _input('Fast', 14)
Slow = _input('Slow', 21)
RSI = _input('RSI', 17)
Confirm = _input('Confirm', _int(0.0))
Flat = _input('Flat', _int(0.0))
SoundAlert = _input('SoundAlert', False)
EmailAlert = _input('EmailAlert', False)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
IUP = 0.0
IDN = 0.0
E1 = 0.0
E2 = 0.0
Confirm2 = 0.0
Flat2 = 0.0
StartBars = 0
SLMA_Handle = 0
FSMA_Handle = 0
RSI_Handle = 0

def BU(i, Low, Time):
    global E1
    if Low[i] >= (E1 + Flat2) or Low[i] <= (E1 - Flat2):
        BuyBuffer[i] = Low[i]
        E1 = BuyBuffer[i]
        Alerts(i, 'UP ' + Symbol() + ' ' + TimeToString(Time[i]))

def BD(i, High, Time):
    global E2
    if High[i] >= (E2 + Flat2) or High[i] <= (E2 - Flat2):
        SellBuffer[i] = High[i]
        E2 = SellBuffer[i]
        Alerts(i, 'DN ' + Symbol() + ' ' + TimeToString(Time[i]))

def Alerts(pos, txt):
    if SoundAlert == True and pos == 1:
        PlaySound('alert.wav')
    if EmailAlert == True and pos == 1:
        SendMail('Stalin alert signal: ' + txt, txt)

def OnInit():
    global Confirm2, E1, E2, FSMA_Handle, Flat2, IDN, IUP, RSI_Handle, SLMA_Handle, StartBars
    StartBars = MathMax(RSI, MathMax(Slow, Fast))
    IUP = 0.0
    IDN = 0.0
    E1 = 0.0
    E2 = 0.0
    if Digits() == 3 or Digits() == 5:
        Point10 = 10 * Point()
        Confirm2 = Point10
        Flat2 = Flat * Point10
    else:
        Confirm2 = Confirm * Point()
        Flat2 = Flat * Point()
    if RSI:
        RSI_Handle = iRSI(None, 0, RSI, PRICE_CLOSE)
        if RSI_Handle == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора iRSI')
    SLMA_Handle = iMA(None, 0, Slow, MAShift, MAMethod, PRICE_CLOSE)
    if SLMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
    FSMA_Handle = iMA(None, 0, Fast, MAShift, MAMethod, PRICE_CLOSE)
    if FSMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Stalin Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Stalin Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Stalin'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global IDN, IUP
    if (((RSI and BarsCalculated(RSI_Handle) < rates_total) or BarsCalculated(SLMA_Handle) < rates_total) or BarsCalculated(FSMA_Handle) < rates_total) or rates_total < StartBars:
        return 0
    to_copy = 0
    limit = 0
    RSI_ = Arr(0, 0.0)
    SLMA_ = Arr(0, 0.0)
    FSMA_ = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
        to_copy = rates_total
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 2
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(SLMA_, True)
    ArraySetAsSeries(FSMA_, True)
    if CopyBuffer(SLMA_Handle, 0, 0, to_copy, SLMA_) <= 0:
        return 0
    if CopyBuffer(FSMA_Handle, 0, 0, to_copy, FSMA_) <= 0:
        return 0
    if RSI:
        ArraySetAsSeries(RSI_, True)
        if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI_) <= 0:
            return 0
    for bar in range(limit, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if (FSMA_[bar + 1] < SLMA_[bar + 1] and FSMA_[bar] > SLMA_[bar]) and ((not RSI) or RSI_[bar] > 50):
            if not Confirm2:
                BU(bar, low, time)
            else:
                IUP = low[bar]
                IDN = 0.0
        if (FSMA_[bar + 1] > SLMA_[bar + 1] and FSMA_[bar] < SLMA_[bar]) and ((not RSI) or RSI_[bar] < 50):
            if not Confirm2:
                BD(bar, high, time)
            else:
                IDN = high[bar]
                IUP = 0.0
        if (IUP and (high[bar] - IUP) >= Confirm2) and close[bar] <= high[bar]:
            BU(bar, low, time)
            IUP = 0.0
        if (IDN and (IDN - low[bar]) >= Confirm2) and open[bar] >= close[bar]:
            BD(bar, high, time)
            IDN = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stalin(_MQL5Indicator):
    name = 'Stalin'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAShift': 0,
        'Fast': 14,
        'Slow': 21,
        'RSI': 17,
        'Confirm': 0,
        'Flat': 0,
        'SoundAlert': False,
        'EmailAlert': False,
    }

