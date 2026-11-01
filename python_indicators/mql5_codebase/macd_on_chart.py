"""macd_on_chart — converted from MQL5: MQL5 Indicators/MACD On Chart/macd_on_chart.mq5

Copyright: Copyright © 2007, Khashayar Talebi; Link: http://www.stct.info; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Khashayar Talebi', 'link': 'http://www.stct.info', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'MACD_On_Chart Sell', 2: 'MACD_On_Chart Buy'}, 'levels': [], 'description': [], 'name': 'macd_on_chart', 'source': 'MQL5 Indicators/MACD On Chart/macd_on_chart.mq5', 'folder': 'MACD On Chart', 'inputs': [{'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'uint', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalSMA', 'py': 'SignalSMA', 'param': 'SignalSMA', 'type': 'uint', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'Applied_Price', 'py': 'Applied_Price', 'param': 'Applied_Price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastEMA = _input('FastEMA', 12)
SlowEMA = _input('SlowEMA', 26)
SignalSMA = _input('SignalSMA', 9)
Applied_Price = _input('Applied_Price', PRICE_CLOSE)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
Macd_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, Macd_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(FastEMA, SlowEMA) + SignalSMA + 1)
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    Macd_Handle = iMACD(Symbol(), PERIOD_CURRENT, FastEMA, SlowEMA, SignalSMA, Applied_Price)
    if Macd_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of iMACD')
        return INIT_FAILED
    ATR_Handle = iATR(Symbol(), PERIOD_CURRENT, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'MACD_On_Chart'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Macd_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MACD = Arr(0, 0.0)
    SIGN = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(Macd_Handle, MAIN_LINE, 0, to_copy, MACD) <= 0:
        return 0
    if CopyBuffer(Macd_Handle, SIGNAL_LINE, 0, to_copy, SIGN) <= 0:
        return 0
    to_copy -= 1
    if CopyBuffer(ATR_Handle, MAIN_LINE, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(MACD, True)
    ArraySetAsSeries(SIGN, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if MACD[bar] > SIGN[bar] and MACD[bar + 1] <= SIGN[bar + 1]:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if MACD[bar] < SIGN[bar] and MACD[bar + 1] >= SIGN[bar + 1]:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MacdOnChart(_MQL5Indicator):
    name = 'macd_on_chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastEMA': 12,
        'SlowEMA': 26,
        'SignalSMA': 9,
        'Applied_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

