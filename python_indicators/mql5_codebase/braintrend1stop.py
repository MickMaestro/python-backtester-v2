"""braintrend1stop — converted from MQL5: MQL5 Indicators/BrainTrend1Stop/braintrend1stop.mq5

Copyright: Copyright © 2005, BrainTrading Inc.; Link: http://www.braintrading.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, BrainTrading Inc.', 'link': 'http://www.braintrading.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 1, 4: 1}, 'colors': {1: [16711935], 2: [16776960], 3: [16711935], 4: [16776960]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2}, 'styles': {3: 0, 4: 0}, 'labels': {1: 'Brain1Sell', 2: 'Brain1Buy', 3: 'Brain1Sell', 4: 'Brain1Buy'}, 'levels': [], 'description': [], 'name': 'braintrend1stop', 'source': 'MQL5 Indicators/BrainTrend1Stop/braintrend1stop.mq5', 'folder': 'BrainTrend1Stop', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 7, 'label': 'Period of ATR', 'sinput': False}, {'mql': 'STO_Period', 'py': 'STO_Period', 'param': 'STO_Period', 'type': 'int', 'default': 9, 'label': 'Period of Stochastic', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '/Method of averaging', 'sinput': False}, {'mql': 'STO_Price', 'py': 'STO_Price', 'param': 'STO_Price', 'type': 'int', 'default': 0, 'label': 'Method of prices calculation', 'sinput': False}, {'mql': 'Stop_dPeriod', 'py': 'Stop_dPeriod', 'param': 'Stop_dPeriod', 'type': 'int', 'default': 3, 'label': 'Period expansion for a stop', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 7)  # Period of ATR
STO_Period = _input('STO_Period', 9)  # Period of Stochastic
MA_Method = _input('MA_Method', MODE_SMA)  # /Method of averaging
STO_Price = _input('STO_Price', STO_LOWHIGH)  # Method of prices calculation
Stop_dPeriod = _input('Stop_dPeriod', 3)  # Period expansion for a stop
SellStopBuffer = Arr(0, 0.0)
BuyStopBuffer = Arr(0, 0.0)
SellStopBuffer_ = Arr(0, 0.0)
BuyStopBuffer_ = Arr(0, 0.0)
d = 0.0
s = 0.0
r = 0.0
R_ = 0.0
p = 0
x1 = 0
x2 = 0
P_ = 0
StartBars = 0
ATR_Handle = 0
ATR1_Handle = 0
STO_Handle = 0

def OnInit():
    global ATR1_Handle, ATR_Handle, STO_Handle, StartBars, d, s, x1, x2
    d = 2.3
    s = 1.5
    x1 = 53
    x2 = 47
    StartBars = MathMax(MathMax(ATR_Period, STO_Period), ATR_Period + Stop_dPeriod) + 2
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    ATR1_Handle = iATR(None, 0, ATR_Period + Stop_dPeriod)
    if ATR1_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the indicator ATR1')
    STO_Handle = iStochastic(None, 0, STO_Period, STO_Period, 1, MA_Method, STO_Price)
    if STO_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Stochastic indicator')
    SetIndexBuffer(0, SellStopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Brain1SellStop')
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    ArraySetAsSeries(SellStopBuffer, True)
    SetIndexBuffer(1, BuyStopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Brain1BuyStop')
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyStopBuffer, True)
    SetIndexBuffer(2, SellStopBuffer_, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(2, PLOT_LABEL, 'Brain1SellStop')
    ArraySetAsSeries(SellStopBuffer_, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, BuyStopBuffer_, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(3, PLOT_LABEL, 'Brain1BuyStop')
    ArraySetAsSeries(BuyStopBuffer_, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'BrainTrend1Stop'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global P_, R_, p, r
    if (BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(STO_Handle) < rates_total) or rates_total < StartBars:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    range_ = 0.0
    range1 = 0.0
    val1 = 0.0
    val2 = 0.0
    val3 = 0.0
    value2 = Arr(0, 0.0)
    Range = Arr(0, 0.0)
    Range1 = Arr(0, 0.0)
    value3 = 0.0
    value4 = 0.0
    value5 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - StartBars
    else:
        to_copy = rates_total - prev_calculated + 1
        limit = rates_total - prev_calculated
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, Range) <= 0:
        return 0
    if CopyBuffer(STO_Handle, 0, 0, to_copy, value2) <= 0:
        return 0
    if CopyBuffer(ATR1_Handle, 0, 0, to_copy, Range1) <= 0:
        return 0
    ArraySetAsSeries(Range, True)
    ArraySetAsSeries(Range1, True)
    ArraySetAsSeries(value2, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    p = P_
    r = R_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            P_ = p
            R_ = r
        range_ = _fdiv(Range[bar], d)
        range1 = Range1[bar] * s
        val1 = 0.0
        val2 = 0.0
        val3 = MathAbs(close[bar] - close[bar + 2])
        SellStopBuffer[bar] = 0.0
        BuyStopBuffer[bar] = 0.0
        SellStopBuffer_[bar] = 0.0
        BuyStopBuffer_[bar] = 0.0
        if val3 > range_:
            if value2[bar] < x2 and p != 1:
                value3 = high[bar] + (range1 / 4)
                val1 = value3
                p = 1
                r = val1
                SellStopBuffer[bar] = val1
                SellStopBuffer_[bar] = val1
            if value2[bar] > x1 and p != 2:
                value3 = low[bar] - (range1 / 4)
                val2 = value3
                p = 2
                r = val2
                BuyStopBuffer[bar] = val2
                BuyStopBuffer_[bar] = val2
        value4 = high[bar] + range1
        value5 = low[bar] - range1
        if val1 == 0 and val2 == 0:
            if p == 1:
                if value4 < r:
                    r = value4
                SellStopBuffer[bar] = r
                SellStopBuffer_[bar] = r
            if p == 2:
                if value5 > r:
                    r = value5
                BuyStopBuffer[bar] = r
                BuyStopBuffer_[bar] = r
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Braintrend1stop(_MQL5Indicator):
    name = 'braintrend1stop'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 7,  # Period of ATR
        'STO_Period': 9,  # Period of Stochastic
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # /Method of averaging
        'STO_Price': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Method of prices calculation
        'Stop_dPeriod': 3,  # Period expansion for a stop
    }

