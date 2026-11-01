"""instantaneous_trendfiltersign — converted from MQL5: MQL5 Indicators/Instantaneous_TrendFilterSign/instantaneous_trendfiltersign.mq5

Copyright: Copyright © 2006, Luis Guilherme Damiani; Link: http://www.damianifx.com.br; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Luis Guilherme Damiani', 'link': 'http://www.damianifx.com.br', 'version': '1.00', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Instantaneous_TrendFilter Sell', 2: 'Instantaneous_TrendFilter Buy'}, 'levels': [], 'description': [], 'name': 'instantaneous_trendfiltersign', 'source': 'MQL5 Indicators/Instantaneous_TrendFilterSign/instantaneous_trendfiltersign.mq5', 'folder': 'Instantaneous_TrendFilterSign', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 0.07, 'label': 'Коэффициент индикатора', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
Alpha = _input('Alpha', 0.07)  # Коэффициент индикатора
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0
K0 = 0.0
K1 = 0.0
K2 = 0.0
K3 = 0.0
K4 = 0.0

def OnInit():
    global ATR_Handle, K0, K1, K2, K3, K4, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 4)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    A2 = Alpha * Alpha
    K0 = Alpha - (A2 / 4.0)
    K1 = 0.5 * A2
    K2 = Alpha - (0.75 * A2)
    K3 = 2.0 * (1.0 - Alpha)
    K4 = MathPow(1.0 - Alpha, 2)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    shortname = Box("")
    StringConcatenate(shortname, 'Instantaneous_TrendFilter(', Alpha, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ITrend1, _s_OnCalculate_ITrend2, _s_OnCalculate_Trigger1
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price0 = 0.0
    price1 = 0.0
    price2 = 0.0
    ITrend0 = 0.0
    Trigger0 = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        _s_OnCalculate_ITrend1 = PriceSeries(IPC, first - 1, open, low, high, close)
        _s_OnCalculate_ITrend2 = PriceSeries(IPC, first - 2, open, low, high, close)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price0 = PriceSeries(IPC, bar, open, low, high, close)
        price1 = PriceSeries(IPC, bar - 1, open, low, high, close)
        price2 = PriceSeries(IPC, bar - 2, open, low, high, close)
        if bar < min_rates_total:
            ITrend0 = (price0 + (2.0 * price1) + price2) / 4.0
        else:
            ITrend0 = (K0 * price0) + (K1 * price1) - (K2 * price2) + (K3 * _s_OnCalculate_ITrend1) - (K4 * _s_OnCalculate_ITrend2)
        Trigger0 = (2.0 * ITrend0) - _s_OnCalculate_ITrend2
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_ITrend1 <= _s_OnCalculate_Trigger1 and ITrend0 > Trigger0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_ITrend1 >= _s_OnCalculate_Trigger1 and ITrend0 < Trigger0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            _s_OnCalculate_ITrend2 = _s_OnCalculate_ITrend1
            _s_OnCalculate_ITrend1 = ITrend0
            _s_OnCalculate_Trigger1 = Trigger0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]

# ---- static local variables
_s_OnCalculate_ITrend1 = 0.0
_s_OnCalculate_ITrend2 = 0.0
_s_OnCalculate_Trigger1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class InstantaneousTrendfiltersign(_MQL5Indicator):
    name = 'instantaneous_trendfiltersign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 0.07,  # Коэффициент индикатора
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

