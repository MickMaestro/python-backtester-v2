"""Stopreversal — converted from MQL5: MQL5 Indicators/Stopreversal/Stopreversal.mq5

Copyright: Copyright 2012, Dominic; Link: dr_richard_gaines@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Dominic', 'link': 'dr_richard_gaines@yahoo.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 5, 2: 5}, 'styles': {}, 'labels': {1: 'Stopreversal Sell', 2: 'Stopreversal Buy'}, 'levels': [], 'description': [], 'name': 'Stopreversal', 'source': 'MQL5 Indicators/Stopreversal/Stopreversal.mq5', 'folder': 'Stopreversal', 'inputs': [{'mql': 'nPips', 'py': 'nPips', 'param': 'nPips', 'type': 'double', 'default': 0.004, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_APPLIED_PRICE_
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
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
nPips = _input('nPips', 0.004)
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(2, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 238)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 236)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Stopreversal'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_PREV
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    price = 0.0
    price_prev = 0.0
    TrStopLevel = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_PREV = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        price = PriceSeries(IPC, bar, open, low, high, close)
        price_prev = PriceSeries(IPC, bar + 1, open, low, high, close)
        if price == _s_OnCalculate_PREV:
            TrStopLevel = _s_OnCalculate_PREV
        else:
            if price_prev < _s_OnCalculate_PREV and price < _s_OnCalculate_PREV:
                TrStopLevel = MathMin(_s_OnCalculate_PREV, price * (1 + nPips))
            else:
                if price_prev > _s_OnCalculate_PREV and price > _s_OnCalculate_PREV:
                    TrStopLevel = MathMax(_s_OnCalculate_PREV, price * (1 - nPips))
                else:
                    if price > _s_OnCalculate_PREV:
                        TrStopLevel = price * (1 - nPips)
                    else:
                        TrStopLevel = price * (1 + nPips)
        if (price > TrStopLevel and price_prev < _s_OnCalculate_PREV) and _s_OnCalculate_PREV:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 1) / 3)
        if (price < TrStopLevel and price_prev > _s_OnCalculate_PREV) and _s_OnCalculate_PREV:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 1) / 3)
        if bar:
            _s_OnCalculate_PREV = TrStopLevel
    else:
        bar = _range_end(bar, 0 - 1, -1)
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
_s_OnCalculate_PREV = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stopreversal(_MQL5Indicator):
    name = 'Stopreversal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'nPips': 0.004,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
    }

