"""NRTR_Gator — converted from MQL5: MQL5 Indicators/NRTR_Gator/NRTR_Gator.mq5

Copyright: Copyright 2010, Rosh; Link: http://forexsystems.ru/phpBB/index.php; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, Rosh', 'link': 'http://forexsystems.ru/phpBB/index.php', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 11}, 'colors': {1: [4678655], 2: [16760576], 3: [16760576], 4: [4678655], 5: [32768, 255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {}, 'labels': {1: 'Линия продажи', 2: 'Линия покупки', 3: 'Потолок', 4: 'Пол', 5: 'Бар'}, 'levels': [], 'description': [], 'name': 'NRTR_Gator', 'source': 'MQL5 Indicators/NRTR_Gator/NRTR_Gator.mq5', 'folder': 'NRTR_Gator', 'inputs': [{'mql': 'PerATR', 'py': 'PerATR', 'param': 'PerATR', 'type': 'int', 'default': 40, 'label': '', 'sinput': False}, {'mql': 'kATR', 'py': 'kATR', 'param': 'kATR', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'useSendMail', 'py': 'useSendMail', 'param': 'useSendMail', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
UpBar = Arr(0, 0.0)
DownBar = Arr(0, 0.0)
ColorBar = Arr(0, 0.0)
GatorTrend = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0
Alligator_Handle = 0
sm_Bars = 0
supervizerShift = 0
SymbolSpread = 0
GatorBars = 0

def OnInit():
    global ATR_Handle, Alligator_Handle, min_rates_total
    min_rates_total = PerATR + 1
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 251)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 251)
    ArraySetAsSeries(BuyBuffer, True)
    SetIndexBuffer(2, Ceil, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    ArraySetAsSeries(Ceil, True)
    SetIndexBuffer(3, Floor, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    ArraySetAsSeries(Floor, True)
    SetIndexBuffer(4, UpBar, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpBar, True)
    SetIndexBuffer(5, DownBar, INDICATOR_DATA)
    ArraySetAsSeries(DownBar, True)
    SetIndexBuffer(6, ColorBar, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBar, True)
    SetIndexBuffer(7, Trend, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Trend, True)
    SetIndexBuffer(8, GatorTrend, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(GatorTrend, True)
    SetIndexBuffer(9, ATR, INDICATOR_DATA)
    ArraySetAsSeries(ATR, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'NRTR_Gator')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ATR_Handle = iATR(None, 0, PerATR)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    Alligator_Handle = iAlligator(None, 0, 13, 8, 8, 5, 5, 3, MODE_SMMA, PRICE_MEDIAN)
    if Alligator_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Alligator')
        return INIT_FAILED
    return INIT_SUCCEEDED

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
        Print('Внимание! Тренд не определен, такого быть не может. Бар от конца ', Bars(None, 0) - shift)
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
        Print('Внимание! Тренд не определен, такого быть не может')

def CopyLastValues(shift):
    SellBuffer[shift] = SellBuffer[shift + 1]
    BuyBuffer[shift] = BuyBuffer[shift + 1]
    Ceil[shift] = Ceil[shift + 1]
    Floor[shift] = Floor[shift + 1]
    Trend[shift] = Trend[shift + 1]

def SendSMS(shift):
    if ((IsNewBar() and (Trend[shift + 1] * Trend[shift + 2]) == -1) and shift == 0) and useSendMail:
        if Trend[shift + 1] == 1:
            SendMail('NRTR ', Symbol() + ' ' + EnumToString(Period(), '') + ' развернулся вверх, Ask = ' + DoubleToString(SymbolInfoDouble(None, SYMBOL_ASK), Digits()))
        else:
            SendMail('NRTR ', Symbol() + ' ' + EnumToString(Period(), '') + ' развернулся вниз, Bid = ' + DoubleToString(SymbolInfoDouble(None, SYMBOL_BID), Digits()))

def IsNewBar():
    global _s_IsNewBar_Told
    Tnew = Arr(1, 0, dyn=False)
    CopyTime(Symbol(), 0, 0, 1, Tnew)
    if Tnew[0] != _s_IsNewBar_Told:
        _s_IsNewBar_Told = Tnew[0]
        return True
    return False

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global supervizerShift
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(ATR_Handle) < rates_total:
        return prev_calculated
    if BarsCalculated(Alligator_Handle) < rates_total:
        return prev_calculated
    limit = 0
    to_copy = 0
    GATORJAW = Arr(0, 0.0)
    GATORTEETH = Arr(0, 0.0)
    GATORLIPS = Arr(0, 0.0)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(GATORJAW, True)
    ArraySetAsSeries(GATORTEETH, True)
    ArraySetAsSeries(GATORLIPS, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - PerATR - 1
        to_copy = rates_total
        if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
            return prev_calculated
        if CopyBuffer(Alligator_Handle, GATORJAW_LINE, 0, to_copy, GATORJAW) <= 0:
            return prev_calculated
        if CopyBuffer(Alligator_Handle, GATORTEETH_LINE, 0, to_copy, GATORTEETH) <= 0:
            return prev_calculated
        if CopyBuffer(Alligator_Handle, GATORLIPS_LINE, 0, to_copy, GATORLIPS) <= 0:
            return prev_calculated
        closeX = close[limit + 1]
        openX = open[limit + 1]
        limit1 = limit + 1
        if closeX > openX:
            Trend[limit1] = 1.0
            Ceil[limit1] = closeX
            BuyBuffer[limit1] = closeX - (kATR * ATR[limit1])
        if closeX < openX:
            Trend[limit1] = -1.0
            Floor[limit1] = closeX
            SellBuffer[limit1] = closeX + (kATR * ATR[limit1])
        if closeX == openX:
            Trend[limit1] = 1.0
            Ceil[limit1] = closeX
            BuyBuffer[limit1] = closeX - (kATR * ATR[limit1])
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
        if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
            return prev_calculated
        if CopyBuffer(Alligator_Handle, GATORJAW_LINE, 0, to_copy, GATORJAW) <= 0:
            return prev_calculated
        if CopyBuffer(Alligator_Handle, GATORTEETH_LINE, 0, to_copy, GATORTEETH) <= 0:
            return prev_calculated
        if CopyBuffer(Alligator_Handle, GATORLIPS_LINE, 0, to_copy, GATORLIPS) <= 0:
            return prev_calculated
    for bar in range(limit, 0 - 1, -1):
        supervizerShift = bar
        if GATORJAW[bar] < GATORTEETH[bar] and GATORTEETH[bar] < GATORLIPS[bar]:
            GatorTrend[bar] = 1.0
        if GATORJAW[bar] > GATORTEETH[bar] and GATORTEETH[bar] > GATORLIPS[bar]:
            GatorTrend[bar] = -1.0
        if Uptrend(bar):
            if BreakCeil(bar, low):
                NewCeil(bar, close)
                SetBuyBuffer(bar, close)
                Trend[bar] = 1.0
                continue
            if BreakUp(bar, close):
                NewTrend(bar, close)
                continue
            CopyLastValues(bar)
        else:
            if BreakFloor(bar, high):
                NewFloor(bar, close)
                SetSellBuffer(bar, close)
                Trend[bar] = -1.0
                continue
            if BreakDown(bar, close):
                NewTrend(bar, close)
                continue
            CopyLastValues(bar)
        if DownBar[bar] > UpBar[bar]:
            ColorBar[bar] = 1.0
        else:
            ColorBar[bar] = 0.0
    return rates_total

# ---- static local variables
_s_IsNewBar_Told = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NRTRGator(_MQL5Indicator):
    name = 'NRTR_Gator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PerATR': 40,
        'kATR': 2.0,
        'useSendMail': False,
    }

