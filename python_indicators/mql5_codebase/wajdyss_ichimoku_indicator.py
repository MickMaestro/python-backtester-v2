"""wajdyss_Ichimoku_Indicator — converted from MQL5: MQL5 Indicators/Wajdyss_Ichimoku_Indicator/wajdyss_Ichimoku_Indicator.mq5

Copyright: Copyright © 2009, Wajdyss; Link: wajdyss@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Wajdyss', 'link': 'wajdyss@yahoo.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [13458026], 2: [3329330], 3: [9639167]}, 'widths': {1: 3, 2: 5, 3: 5}, 'styles': {1: 0}, 'labels': {1: 'Kijun Sen', 2: 'Buy wajdyss_Ichimoku', 3: 'Sell wajdyss_Ichimoku'}, 'levels': [], 'description': [''], 'name': 'wajdyss_Ichimoku_Indicator', 'source': 'MQL5 Indicators/Wajdyss_Ichimoku_Indicator/wajdyss_Ichimoku_Indicator.mq5', 'folder': 'Wajdyss_Ichimoku_Indicator', 'inputs': [{'mql': 'Kijun', 'py': 'Kijun', 'param': 'Kijun', 'type': 'uint', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Kijun = _input('Kijun', 26)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtLineBuffer0 = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = _int(Kijun)
    ATR_Period = 15
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(ExtLineBuffer0, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(BuyBuffer, True)
    ArraySetAsSeries(SellBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'wajdyss_Ichimoku_Indicator')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ATR = Arr(0, 0.0)
    kijun = 0.0
    kijun_prev = 0.0
    price = 0.0
    High = 0.0
    Low = 0.0
    limit = 0
    bar = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        High = high[bar]
        Low = low[bar]
        index = bar + _int(Kijun) - 1
        while index > bar:
            price = high[index]
            if High < price:
                High = price
            price = low[index]
            if Low > price:
                Low = price
            index -= 1
        kijun = (High + Low) / 2
        ExtLineBuffer0[bar] = kijun
        kijun_prev = ExtLineBuffer0[bar + 1]
        if close[bar] >= kijun and close[bar + 1] < kijun_prev:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 16)
        elif close[bar] <= kijun and close[bar + 1] > kijun_prev:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 16)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WajdyssIchimokuIndicator(_MQL5Indicator):
    name = 'wajdyss_Ichimoku_Indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Kijun': 26,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

