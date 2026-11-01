"""Stalin_NRTR — converted from MQL5: MQL5 Indicators/Stalin_x10/Stalin_NRTR.mq5

Copyright: Copyright © 2011, Andrey Vassiliev (MoneyJinn); Link: http://www.vassiliev.ru/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Andrey Vassiliev (MoneyJinn)', 'link': 'http://www.vassiliev.ru/', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [65280], 2: [16711935], 3: [3329330], 4: [9639167], 5: [3329330], 6: [9639167]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 5, 6: 5}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'NRTR Line Up', 2: 'NRTR Line Down', 3: 'NRTR Up', 4: 'NRTR Down', 5: 'Buy NRTR signal', 6: 'Sell NRTR signal'}, 'levels': [], 'description': [], 'name': 'Stalin_NRTR', 'source': 'MQL5 Indicators/Stalin_x10/Stalin_NRTR.mq5', 'folder': 'Stalin_x10', 'inputs': [{'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Fast', 'py': 'Fast', 'param': 'Fast', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Slow', 'py': 'Slow', 'param': 'Slow', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'RSI', 'py': 'RSI', 'param': 'RSI', 'type': 'int', 'default': 17, 'label': '', 'sinput': False}, {'mql': 'Confirm', 'py': 'Confirm', 'param': 'Confirm', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Flat', 'py': 'Flat', 'param': 'Flat', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'AtrRatio', 'py': 'AtrRatio', 'param': 'AtrRatio', 'type': 'double', 'default': 0.375, 'label': '', 'sinput': False}, {'mql': 'SoundAlert', 'py': 'SoundAlert', 'param': 'SoundAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EmailAlert', 'py': 'EmailAlert', 'param': 'EmailAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAMethod = _input('MAMethod', MODE_EMA)
MAShift = _input('MAShift', 0)
Fast = _input('Fast', 14)
Slow = _input('Slow', 21)
RSI = _input('RSI', 17)
Confirm = _input('Confirm', _int(0.0))
Flat = _input('Flat', _int(0.0))
AtrRatio = _input('AtrRatio', 0.375)
SoundAlert = _input('SoundAlert', False)
EmailAlert = _input('EmailAlert', False)
UpBuffer1 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
UpBuffer2 = Arr(0, 0.0)
DnBuffer2 = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
IUP = 0.0
IDN = 0.0
E1 = 0.0
E2 = 0.0
Confirm2 = 0.0
Flat2 = 0.0
ATR_ = Arr(0, 0.0)
min_rates_total = 0
trend = 0
trend_prev = 0
SLMA_Handle = 0
FSMA_Handle = 0
RSI_Handle = 0
ATR_Handle = 0

def BU(i, Low, Time):
    global E1, trend
    if Low[i] >= (E1 + Flat2) or Low[i] <= (E1 - Flat2):
        if trend <= 0:
            BuyBuffer[i] = Low[i] - (AtrRatio * ATR_[i])
        E1 = Low[i]
        trend = 1
        Alerts(i, 'UP ' + Symbol() + ' ' + TimeToString(Time[i]))

def BD(i, High, Time):
    global E2, trend
    if High[i] >= (E2 + Flat2) or High[i] <= (E2 - Flat2):
        if trend >= 0:
            SellBuffer[i] = High[i] + (AtrRatio * ATR_[i])
        E2 = High[i]
        trend = -1
        Alerts(i, 'DN ' + Symbol() + ' ' + TimeToString(Time[i]))

def Alerts(pos, txt):
    if SoundAlert == True and pos == 1:
        PlaySound('alert.wav')
    if EmailAlert == True and pos == 1:
        SendMail('Stalin alert signal: ' + txt, txt)

def OnInit():
    global ATR_Handle, Confirm2, E1, E2, FSMA_Handle, Flat2, IDN, IUP, RSI_Handle, SLMA_Handle, min_rates_total
    min_rates_total = MathMax(RSI, MathMax(Slow, Fast))
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, min_rates_total) + 1
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
            return INIT_FAILED
    SLMA_Handle = iMA(None, 0, Slow, MAShift, MAMethod, PRICE_CLOSE)
    if SLMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    FSMA_Handle = iMA(None, 0, Fast, MAShift, MAMethod, PRICE_CLOSE)
    if FSMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer1, True)
    SetIndexBuffer(1, DnBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(DnBuffer1, True)
    SetIndexBuffer(2, UpBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer2, True)
    SetIndexBuffer(3, DnBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(DnBuffer2, True)
    SetIndexBuffer(4, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 171)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(BuyBuffer, True)
    SetIndexBuffer(5, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_ARROW, 171)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(SellBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Stalin_NRTR'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global IDN, IUP, trend, trend_prev
    if ((((RSI and BarsCalculated(RSI_Handle) < rates_total) or BarsCalculated(SLMA_Handle) < rates_total) or BarsCalculated(FSMA_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    RSI_ = Arr(0, 0.0)
    SLMA_ = Arr(0, 0.0)
    FSMA_ = Arr(0, 0.0)
    range_ = 0.0
    stop = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        to_copy = rates_total
        trend_prev = 0
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
    ArraySetAsSeries(ATR_, True)
    if CopyBuffer(SLMA_Handle, 0, 0, to_copy, SLMA_) <= 0:
        return 0
    if CopyBuffer(FSMA_Handle, 0, 0, to_copy, FSMA_) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy - 1, ATR_) <= 0:
        return 0
    if RSI:
        ArraySetAsSeries(RSI_, True)
        if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI_) <= 0:
            return 0
    for bar in range(limit, 0 - 1, -1):
        DnBuffer2[bar] = 0.0
        UpBuffer2[bar] = DnBuffer2[bar]
        DnBuffer1[bar] = UpBuffer2[bar]
        UpBuffer1[bar] = DnBuffer1[bar]
        SellBuffer[bar] = UpBuffer1[bar]
        BuyBuffer[bar] = SellBuffer[bar]
        trend = trend_prev
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
        range_ = AtrRatio * ATR_[bar]
        if trend > 0:
            if BuyBuffer[bar]:
                UpBuffer2[bar] = BuyBuffer[bar]
                UpBuffer1[bar] = UpBuffer2[bar]
                DnBuffer1[bar] = DnBuffer1[bar + 1]
            else:
                stop = low[bar] - range_
                if stop < UpBuffer1[bar + 1]:
                    stop = UpBuffer1[bar + 1]
                UpBuffer2[bar] = stop
                UpBuffer1[bar] = UpBuffer2[bar]
        if trend < 0:
            if SellBuffer[bar]:
                DnBuffer2[bar] = SellBuffer[bar]
                DnBuffer1[bar] = DnBuffer2[bar]
                UpBuffer1[bar] = UpBuffer1[bar + 1]
            else:
                stop = high[bar] + range_
                if stop > DnBuffer1[bar + 1]:
                    stop = DnBuffer1[bar + 1]
                DnBuffer2[bar] = stop
                DnBuffer1[bar] = DnBuffer2[bar]
        if bar:
            trend_prev = trend
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StalinNRTR(_MQL5Indicator):
    name = 'Stalin_NRTR'
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
        'AtrRatio': 0.375,
        'SoundAlert': False,
        'EmailAlert': False,
    }

