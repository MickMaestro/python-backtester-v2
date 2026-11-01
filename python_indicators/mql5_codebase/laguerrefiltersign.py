"""LaguerreFilterSign — converted from MQL5: MQL5 Indicators/LaguerreFilterSign/LaguerreFilterSign.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'LaguerreFilter Sell', 2: 'LaguerreFilter Buy'}, 'levels': [], 'description': [], 'name': 'LaguerreFilterSign', 'source': 'MQL5 Indicators/LaguerreFilterSign/LaguerreFilterSign.mq5', 'folder': 'LaguerreFilterSign', 'inputs': [{'mql': 'Gamma', 'py': 'Gamma', 'param': 'Gamma', 'type': 'double', 'default': 0.7, 'label': 'коэффициент индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Gamma = _input('Gamma', 0.7)  # коэффициент индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
min_rates_total = 0
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0

def Get_Price(High, Low, bar):
    return (High[bar] + Low[bar]) / 2

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 4)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 172)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 172)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Laguerre Filter(', DoubleToString(Gamma, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Fir_, _s_OnCalculate_L0A_, _s_OnCalculate_L0_, _s_OnCalculate_L1A_, _s_OnCalculate_L1_, _s_OnCalculate_L2A_, _s_OnCalculate_L2_, _s_OnCalculate_L3A_, _s_OnCalculate_L3_, _s_OnCalculate_Laguerre_
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    L0 = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    L0A = 0.0
    L1A = 0.0
    L2A = 0.0
    L3A = 0.0
    Laguerre = 0.0
    Fir = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    L0 = _s_OnCalculate_L0_
    L1 = _s_OnCalculate_L1_
    L2 = _s_OnCalculate_L2_
    L3 = _s_OnCalculate_L3_
    L0A = _s_OnCalculate_L0A_
    L1A = _s_OnCalculate_L1A_
    L2A = _s_OnCalculate_L2A_
    L3A = _s_OnCalculate_L3A_
    bar = first
    for bar in range(bar, rates_total):
        L0A = L0
        L1A = L1
        L2A = L2
        L3A = L3
        L0 = ((1 - Gamma) * Get_Price(high, low, bar)) + (Gamma * L0A)
        L1 = ((-Gamma) * L0) + L0A + (Gamma * L1A)
        L2 = ((-Gamma) * L1) + L1A + (Gamma * L2A)
        L3 = ((-Gamma) * L2) + L2A + (Gamma * L3A)
        if bar > min_rates_total:
            Laguerre = (L0 + (2.0 * L1) + (2.0 * L2) + L3) / 6.0
            Fir = ((1.0 * Get_Price(high, low, bar - 0)) + (2.0 * Get_Price(high, low, bar - 1)) + (2.0 * Get_Price(high, low, bar - 2)) + (1.0 * Get_Price(high, low, bar - 3))) / 6.0
        else:
            _s_OnCalculate_L0_ = Get_Price(high, low, bar)
            _s_OnCalculate_L1_ = _s_OnCalculate_L0_
            _s_OnCalculate_L2_ = _s_OnCalculate_L0_
            _s_OnCalculate_L3_ = _s_OnCalculate_L0_
            Fir = _s_OnCalculate_L0_
            Laguerre = Fir
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        if _s_OnCalculate_Fir_ <= _s_OnCalculate_Laguerre_ and Fir > Laguerre:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_Fir_ >= _s_OnCalculate_Laguerre_ and Fir < Laguerre:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if rates_total != prev_calculated and bar == (rates_total - 2):
            _s_OnCalculate_L0_ = L0
            _s_OnCalculate_L1_ = L1
            _s_OnCalculate_L2_ = L2
            _s_OnCalculate_L3_ = L3
            _s_OnCalculate_L0A_ = L0A
            _s_OnCalculate_L1A_ = L1A
            _s_OnCalculate_L2A_ = L2A
            _s_OnCalculate_L3A_ = L3A
        if bar < (rates_total - 1):
            _s_OnCalculate_Laguerre_ = Laguerre
            _s_OnCalculate_Fir_ = Fir
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_L0_ = 0.0
_s_OnCalculate_L1_ = 0.0
_s_OnCalculate_L2_ = 0.0
_s_OnCalculate_L3_ = 0.0
_s_OnCalculate_L0A_ = 0.0
_s_OnCalculate_L1A_ = 0.0
_s_OnCalculate_L2A_ = 0.0
_s_OnCalculate_L3A_ = 0.0
_s_OnCalculate_Laguerre_ = 0.0
_s_OnCalculate_Fir_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LaguerreFilterSign(_MQL5Indicator):
    name = 'LaguerreFilterSign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Gamma': 0.7,  # коэффициент индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

