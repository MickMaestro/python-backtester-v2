"""i-bul_jerk — converted from MQL5: MQL5 Indicators/i-Bul_Jerk/i-bul_jerk.mq5

Copyright: Copyright © 2013, Ким Игорь В. aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Ким Игорь В. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'i-Bul_Jerk Sell', 2: 'i-Bul_Jerk Buy'}, 'levels': [], 'description': [], 'name': 'i-bul_jerk', 'source': 'MQL5 Indicators/i-Bul_Jerk/i-bul_jerk.mq5', 'folder': 'i-Bul_Jerk', 'inputs': [{'mql': 'NumbOfBars', 'py': 'NumbOfBars', 'param': 'NumbOfBars', 'type': 'uint', 'default': 3, 'label': 'Количество сигнальных баров', 'sinput': False}, {'mql': 'PriceDistance', 'py': 'PriceDistance', 'param': 'PriceDistance', 'type': 'uint', 'default': 1000, 'label': 'Расстояние в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
NumbOfBars = _input('NumbOfBars', 3)  # Количество сигнальных баров
PriceDistance = _input('PriceDistance', 1000)  # Расстояние в пунктах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
dPriceDistance = 0.0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, dPriceDistance, min_rates_total
    dPriceDistance = Point() * PriceDistance
    ATR_Period = 15
    min_rates_total = _int(MathMax(ATR_Period, NumbOfBars))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'i-Bul_Jerk'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        bs = GetSignal(bar, High, Low, Close)
        if bs > 0:
            BuyBuffer[bar] = Low[bar] - (0.3 * ATR[bar])
        if bs < 0:
            SellBuffer[bar] = High[bar] + (0.3 * ATR[bar])
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def GetSignal(nb, high, low, close):
    bs = 0
    hi = NormalizeDouble(high[ArrayMaximum(high, nb, NumbOfBars)], Digits())
    lo = NormalizeDouble(low[ArrayMinimum(low, nb, NumbOfBars)], Digits())
    if (close[nb] - lo) >= dPriceDistance:
        bs = -1
    if (hi - close[nb]) >= dPriceDistance:
        bs = 1
    return bs


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IBulJerk(_MQL5Indicator):
    name = 'i-bul_jerk'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'NumbOfBars': 3,  # Количество сигнальных баров
        'PriceDistance': 1000,  # Расстояние в пунктах
    }

