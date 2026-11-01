"""braintrend — converted from MQL5: MQL5 Indicators/BrainTrend1 and BrainTrend2/braintrend.mq5

Copyright: Copyright © 2005, BrainTrading Inc.; Link: http://www.braintrading.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, BrainTrading Inc.', 'link': 'http://www.braintrading.com/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4, 'indicator_maximum': 1.2, 'indicator_minimum': 0.4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [255], 2: [14822282], 3: [255], 4: [14822282]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {}, 'labels': {1: 'Brain1Sell', 2: 'Brain1Buy', 3: 'Brain2Sell', 4: 'Brain2Buy'}, 'levels': [0.8], 'description': [], 'name': 'braintrend', 'source': 'MQL5 Indicators/BrainTrend1 and BrainTrend2/braintrend.mq5', 'folder': 'BrainTrend1 and BrainTrend2', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 7, 'label': 'ATR period', 'sinput': False}, {'mql': 'STO_Period', 'py': 'STO_Period', 'param': 'STO_Period', 'type': 'int', 'default': 9, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'STO_Price', 'py': 'STO_Price', 'param': 'STO_Price', 'type': 'int', 'default': 0, 'label': 'Prices calculation method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 7)  # ATR period
STO_Period = _input('STO_Period', 9)  # Stochastic period
MA_Method = _input('MA_Method', MODE_SMA)  # Smoothing method
STO_Price = _input('STO_Price', STO_LOWHIGH)  # Prices calculation method
SellBuffer1 = Arr(0, 0.0)
BuyBuffer1 = Arr(0, 0.0)
SellBuffer2 = Arr(0, 0.0)
BuyBuffer2 = Arr(0, 0.0)
min_rates_total = 0
Brain1_Handle = 0
Brain2_Handle = 0

def OnInit():
    global Brain1_Handle, Brain2_Handle, min_rates_total
    min_rates_total = MathMax(ATR_Period, STO_Period) + 2
    Brain1_Handle = iCustom(None, 0, 'BrainTrend1', ATR_Period, STO_Period, MA_Method, STO_Price)
    if Brain1_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the BrainTrend1 indicator')
        return 1
    Brain2_Handle = iCustom(None, 0, 'BrainTrend2', ATR_Period)
    if Brain2_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the BrainTrend2 indicator')
        return 1
    SetIndexBuffer(0, SellBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 167)
    ArraySetAsSeries(SellBuffer1, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, BuyBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 167)
    ArraySetAsSeries(BuyBuffer1, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(2, SellBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    ArraySetAsSeries(SellBuffer2, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, BuyBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyBuffer2, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    short_name = 'BrainTrend'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Brain1_Handle) < rates_total or BarsCalculated(Brain2_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Brain1 = Arr(0, 0.0)
    Brain2 = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - min_rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
        limit = rates_total - prev_calculated
    if CopyBuffer(Brain1_Handle, 4, 0, to_copy, Brain1) <= 0:
        return 0
    if CopyBuffer(Brain2_Handle, 4, 0, to_copy, Brain2) <= 0:
        return 0
    ArraySetAsSeries(Brain1, True)
    ArraySetAsSeries(Brain2, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer1[bar] = 0.0
        BuyBuffer2[bar] = 0.0
        SellBuffer1[bar] = 0.0
        SellBuffer2[bar] = 0.0
        if Brain1[bar] == 1:
            BuyBuffer1[bar] = 1.0
        elif Brain1[bar] == 2:
            SellBuffer1[bar] = 1.0
        if Brain2[bar] == 1:
            BuyBuffer2[bar] = 0.6
        elif Brain2[bar] == 2:
            SellBuffer2[bar] = 0.6
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Braintrend(_MQL5Indicator):
    name = 'braintrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 7,  # ATR period
        'STO_Period': 9,  # Stochastic period
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
        'STO_Price': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Prices calculation method
    }
    y_range = (0.4, 1.2)

