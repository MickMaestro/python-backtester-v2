"""forexprofitboost_2nbsign — converted from MQL5: MQL5 Indicators/ForexProfitBoost_2nbSign/forexprofitboost_2nbsign.mq5

Copyright: Copyright © 2015, TradeLikeaPro.ru; Link: http://tradelikeapro.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, TradeLikeaPro.ru', 'link': 'http://tradelikeapro.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [55295], 2: [8388352]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'ForexProfitBoost_2nb Sell', 2: 'ForexProfitBoost_2nb Buy'}, 'levels': [], 'description': [], 'name': 'forexprofitboost_2nbsign', 'source': 'MQL5 Indicators/ForexProfitBoost_2nbSign/forexprofitboost_2nbsign.mq5', 'folder': 'ForexProfitBoost_2nbSign', 'inputs': [{'mql': 'MAPeriod1', 'py': 'MAPeriod1', 'param': 'MAPeriod1', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'MAType1', 'py': 'MAType1', 'param': 'MAType1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice1', 'py': 'MAPrice1', 'param': 'MAPrice1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPeriod2', 'py': 'MAPeriod2', 'param': 'MAPeriod2', 'type': 'uint', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'MAType2', 'py': 'MAType2', 'param': 'MAType2', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MAPrice2', 'py': 'MAPrice2', 'param': 'MAPrice2', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod1 = _input('MAPeriod1', 7)
MAType1 = _input('MAType1', MODE_EMA)
MAPrice1 = _input('MAPrice1', PRICE_CLOSE)
MAPeriod2 = _input('MAPeriod2', 21)
MAType2 = _input('MAType2', MODE_SMA)
MAPrice2 = _input('MAPrice2', PRICE_CLOSE)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
MA1_Handle = 0
MA2_Handle = 0
BB_Handle = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, MA1_Handle, MA2_Handle, min_rates_total
    ATR_Period = 10
    min_rates_total = _int(MathMax(MAPeriod1, MAPeriod2)) + 1
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    MA1_Handle = iMA(None, 0, MAPeriod1, 0, MAType1, MAPrice1)
    if MA1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 1')
        return INIT_FAILED
    MA2_Handle = iMA(None, 0, MAPeriod2, 0, MAType2, MAPrice2)
    if MA2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 2')
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
    shortname = 'ForexProfitBoost_2nbSign'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if ((BarsCalculated(MA1_Handle) < rates_total or BarsCalculated(MA2_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    MA1 = Arr(0, 0.0)
    MA2 = Arr(0, 0.0)
    ATR = Arr(1, 0.0, dyn=False)
    limit = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(MA1, True)
    ArraySetAsSeries(MA2, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    to_copy = limit + 2
    if CopyBuffer(MA1_Handle, 0, 0, to_copy, MA1) <= 0:
        return 0
    if CopyBuffer(MA2_Handle, 0, 0, to_copy, MA2) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if MA1[bar] > MA2[bar]:
            if MA1[bar + 1] <= MA2[bar + 1]:
                if CopyBuffer(ATR_Handle, 0, bar, 1, ATR) <= 0:
                    return 0
                BuyBuffer[bar] = Low[bar] - ((ATR[0] * 3) / 8)
        else:
            if MA1[bar + 1] >= MA2[bar + 1]:
                if CopyBuffer(ATR_Handle, 0, bar, 1, ATR) <= 0:
                    return 0
                SellBuffer[bar] = High[bar] + ((ATR[0] * 3) / 8)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Forexprofitboost2nbsign(_MQL5Indicator):
    name = 'forexprofitboost_2nbsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod1': 7,
        'MAType1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'MAPeriod2': 21,
        'MAType2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'MAPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

