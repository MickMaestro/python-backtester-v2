"""highslowssignal — converted from MQL5: MQL5 Indicators/HighsLowsSignal_HTF/highslowssignal.mq5

Copyright: Copyright © 2006, Robert Hill; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Robert Hill', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16748574]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'HighsLowsSignal Sell', 2: 'HighsLowsSignal Buy'}, 'levels': [], 'description': [], 'name': 'highslowssignal', 'source': 'MQL5 Indicators/HighsLowsSignal_HTF/highslowssignal.mq5', 'folder': 'HighsLowsSignal_HTF', 'inputs': [{'mql': 'HowManyCandles', 'py': 'HowManyCandles', 'param': 'HowManyCandles', 'type': 'uint', 'default': 3, 'label': 'The number of candlesticks of a directed price change', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HowManyCandles = _input('HowManyCandles', 3)  # The number of candlesticks of a directed price change
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 4)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 171)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 171)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'HighsLowsSignal')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    HigherHighs = 0
    HigherLows = 0
    LowerHighs = 0
    LowerLows = 0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HigherHighs = 0
        HigherLows = 0
        LowerHighs = 0
        LowerLows = 0
        end = bar + _int(HowManyCandles)
        for index in range(bar, end):
            index1 = index + 1
            if high[index] > high[index1]:
                HigherHighs += 1
            if low[index] > low[index1]:
                HigherLows += 1
            if high[index] < high[index1]:
                LowerHighs += 1
            if low[index] < low[index1]:
                LowerLows += 1
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if HigherHighs == HowManyCandles and HigherLows == HowManyCandles:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        elif LowerHighs == HowManyCandles and LowerLows == HowManyCandles:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Highslowssignal(_MQL5Indicator):
    name = 'highslowssignal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HowManyCandles': 3,  # The number of candlesticks of a directed price change
    }

