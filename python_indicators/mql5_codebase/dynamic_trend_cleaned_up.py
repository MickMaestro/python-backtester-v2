"""dynamic_trend_cleaned_up — converted from MQL5: MQL5 Indicators/Dynamic_trend_cleaned_up/dynamic_trend_cleaned_up.mq5

Copyright: Copyright © 2004, OfficeFX Group; Link: http:// officefx.nm.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, OfficeFX Group', 'link': 'http:// officefx.nm.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [55295], 2: [16711935], 3: [65280]}, 'widths': {1: 1, 2: 4, 3: 4}, 'styles': {1: 0}, 'labels': {1: 'DynamicLine', 2: 'Sell', 3: 'Buy'}, 'levels': [], 'description': [], 'name': 'dynamic_trend_cleaned_up', 'source': 'MQL5 Indicators/Dynamic_trend_cleaned_up/dynamic_trend_cleaned_up.mq5', 'folder': 'Dynamic_trend_cleaned_up', 'inputs': [{'mql': 'Percent', 'py': 'Percent', 'param': 'Percent', 'type': 'uint', 'default': 150, 'label': 'Percent dynamic channel', 'sinput': False}, {'mql': 'MaxPeriod', 'py': 'MaxPeriod', 'param': 'MaxPeriod', 'type': 'uint', 'default': 50, 'label': 'Maximal period for calculate trend', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Percent = _input('Percent', 150)  # Percent dynamic channel
MaxPeriod = _input('MaxPeriod', 50)  # Maximal period for calculate trend
IndBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
dPercent = 0.0
min_rates_total = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, dPercent, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MaxPeriod) + 5
    min_rates_total = MathMax(ATR_Period, min_rates_total)
    dPercent = Percent * Point()
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(2, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Dynamic_trend_cleaned_upg'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    bar2 = 0
    bar3 = 0
    HH = 0.0
    LL = 0.0
    ATR = Arr(0, 0.0)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        IndBuffer[limit + 1] = close[limit + 1]
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HH = close[ArrayMaximum(close, bar + 1, MaxPeriod)]
        LL = close[ArrayMinimum(close, bar + 1, MaxPeriod)]
        if close[bar] < IndBuffer[bar + 1]:
            IndBuffer[bar] = HH - dPercent
        else:
            IndBuffer[bar] = LL + dPercent
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        bar2 = bar + 2
        bar3 = bar + 3
        if close[bar2] > IndBuffer[bar2] and close[bar2] < IndBuffer[bar3]:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if close[bar2] < IndBuffer[bar2] and close[bar2] > IndBuffer[bar3]:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynamicTrendCleanedUp(_MQL5Indicator):
    name = 'dynamic_trend_cleaned_up'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Percent': 150,  # Percent dynamic channel
        'MaxPeriod': 50,  # Maximal period for calculate trend
    }

