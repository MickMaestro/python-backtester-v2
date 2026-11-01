"""AdaptiveCyberCycleSign — converted from MQL5: MQL5 Indicators/AdaptiveCyberCycleSign/AdaptiveCyberCycleSign.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'AdaptiveCyberCycle Sell', 2: 'AdaptiveCyberCycle Buy'}, 'levels': [], 'description': [], 'name': 'AdaptiveCyberCycleSign', 'source': 'MQL5 Indicators/AdaptiveCyberCycleSign/AdaptiveCyberCycleSign.mq5', 'folder': 'AdaptiveCyberCycleSign', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 0.07, 'label': 'Коэффициент индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha = _input('Alpha', 0.07)  # Коэффициент индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
CP_Handle = 0
ATR_Handle = 0
min_rates_total = 0
Count = Arr(0, 0)
Smooth = Arr(0, 0.0)
Price = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = 7
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global ATR_Handle, CP_Handle, min_rates_total
    ATR_Period = 10
    min_rates_total = MathMax(7 + 6, ATR_Period)
    ArrayResize(Count, 7)
    ArrayResize(Smooth, 7)
    ArrayResize(Price, 7)
    ArrayInitialize(Smooth, 0.0)
    ArrayInitialize(Price, 0.0)
    CP_Handle = iCustom(None, 0, 'CyclePeriod', Alpha)
    if CP_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CyclePeriod')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 172)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 172)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(BuyBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Adaptive Cyber Cycle Sign(', DoubleToString(Alpha, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Cycle1, _s_OnCalculate_Cycle2, _s_OnCalculate_Trigger1
    if (BarsCalculated(CP_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    MaxBar = 0
    limit = 0
    bar = 0
    bar0 = 0
    bar1 = 0
    bar2 = 0
    bar3 = 0
    K0 = 0.0
    K1 = 0.0
    K2 = 0.0
    K3 = 0.0
    period = Arr(1, 0.0, dyn=False)
    ATR = Arr(1, 0.0, dyn=False)
    alpha1 = 0.0
    Cycle0 = 0.0
    Trigger0 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        _s_OnCalculate_Cycle2 = 0.0
        _s_OnCalculate_Cycle1 = 0.0
        _s_OnCalculate_Trigger1 = 0.0
    else:
        limit = rates_total - prev_calculated
    MaxBar = rates_total - min_rates_total - 3
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        bar0 = Count[0]
        bar1 = Count[1]
        bar2 = Count[2]
        bar3 = Count[3]
        Price[bar0] = (high[bar] + low[bar]) / 2.0
        Smooth[bar0] = (Price[bar0] + (2.0 * Price[bar1]) + (2.0 * Price[bar2]) + Price[bar3]) / 6.0
        if bar <= MaxBar:
            if CopyBuffer(CP_Handle, 0, bar, 1, period) <= 0:
                return 0
            alpha1 = _fdiv(2.0, period[0] + 1.0)
            K0 = MathPow(1.0 - (0.5 * alpha1), 2)
            K1 = 2.0
            K2 = K1 * (1.0 - alpha1)
            K3 = MathPow(1.0 - alpha1, 2)
            Cycle0 = (K0 * (Smooth[bar0] - (K1 * Smooth[bar1]) + Smooth[bar2])) + (K2 * _s_OnCalculate_Cycle1) - (K3 * _s_OnCalculate_Cycle2)
        else:
            Cycle0 = (Price[bar0] - (2.0 * Price[bar1]) + Price[bar2]) / 4.0
        Trigger0 = _s_OnCalculate_Cycle1
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_Cycle1 < _s_OnCalculate_Trigger1 and Cycle0 > Trigger0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_Cycle1 > _s_OnCalculate_Trigger1 and Cycle0 < Trigger0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar > 0:
            _s_OnCalculate_Cycle2 = _s_OnCalculate_Cycle1
            _s_OnCalculate_Cycle1 = Cycle0
            _s_OnCalculate_Trigger1 = Trigger0
            Recount_ArrayZeroPos(Count)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_Cycle2 = 0.0
_s_OnCalculate_Cycle1 = 0.0
_s_OnCalculate_Trigger1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdaptiveCyberCycleSign(_MQL5Indicator):
    name = 'AdaptiveCyberCycleSign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 0.07,  # Коэффициент индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

