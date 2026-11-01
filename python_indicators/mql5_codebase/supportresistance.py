"""SupportResistance — converted from MQL5: MQL5 Indicators/Support and Resistance indicator for MQL5/SupportResistance.mq5

Copyright: Mueller Peter; Link: https://www.mql5.com/en/users/mullerp04; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Mueller Peter', 'link': 'https://www.mql5.com/en/users/mullerp04', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Support', 2: 'Resistance'}, 'levels': [], 'description': [], 'name': 'SupportResistance', 'source': 'MQL5 Indicators/Support and Resistance indicator for MQL5/SupportResistance.mq5', 'folder': 'Support and Resistance indicator for MQL5', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 20, 'label': 'The period of the indicator', 'sinput': False}, {'mql': 'overlook', 'py': 'overlook', 'param': 'overlook', 'type': 'int', 'default': 10, 'label': 'The overlook of period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 20)  # The period of the indicator
overlook = _input('overlook', 10)  # The overlook of period
Box__v = False
ResBuffer = Arr(0, 0.0)
SuppBuffer = Arr(0, 0.0)

def Resistance(starting, high):
    high1 = high[ArrayMaximum(high, starting, period)]
    high2 = high[ArrayMaximum(high, starting, period + overlook)]
    if high1 == high2:
        return high1
    else:
        return 0.0

def Support(starting, low):
    low1 = low[ArrayMinimum(low, starting, period)]
    low2 = low[ArrayMinimum(low, starting, period + overlook)]
    if low1 == low2:
        return low1
    else:
        return 0.0

def OnInit():
    SetIndexBuffer(0, ResBuffer)
    SetIndexBuffer(1, SuppBuffer)
    Start = MathMax(period, overlook)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Start)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Start)
    ArraySetAsSeries(ResBuffer, False)
    ArraySetAsSeries(SuppBuffer, False)
    return INIT_SUCCEEDED

def IsNewCandle():
    global _s_IsNewCandle_saved_candle_time
    if iTime(Symbol(), PERIOD_CURRENT, 0) == _s_IsNewCandle_saved_candle_time:
        return False
    else:
        _s_IsNewCandle_saved_candle_time = iTime(Symbol(), PERIOD_CURRENT, 0)
    return True

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Box__v
    if False:
        return 0
    i = 0
    Savedmin = 0.0
    Savedmax = 0.0
    ArraySetAsSeries(ResBuffer, False)
    ArraySetAsSeries(SuppBuffer, False)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    if (rates_total <= (period + overlook) or period <= 0) or overlook < 0:
        return 0
    i = 0
    for i in range(i, period + overlook):
        SuppBuffer[i] = EMPTY_VALUE
        ResBuffer[i] = EMPTY_VALUE
    else:
        i = _range_end(i, period + overlook, 1)
    i = MathMax(period + overlook, rates_total - 3000)
    i
    while i < rates_total:
        BounceUp = (((Support(rates_total - i, high) * 3) + Resistance(rates_total - i, high)) / 4) < close[rates_total - i]
        BounceBack = ((Support(rates_total - i, low) + (Resistance(rates_total - i, low) * 3)) / 4) > close[rates_total - i]
        if (((Support(rates_total - i, low) != 0 and Resistance(rates_total - i, high) != 0) and (not Box__v)) and BounceBack) and BounceUp:
            SuppBuffer[i] = Support(rates_total - i, low)
            ResBuffer[i] = Resistance(rates_total - i, high)
            Savedmin = Support(rates_total - i, low)
            Savedmax = Resistance(rates_total - i, high)
            Box__v = True
        elif (low[rates_total - i] > Savedmin and high[rates_total - i] < Savedmax) and Box__v:
            SuppBuffer[i] = Savedmin
            ResBuffer[i] = Savedmax
            Box__v = True
        else:
            SuppBuffer[i] = EMPTY_VALUE
            ResBuffer[i] = EMPTY_VALUE
            Box__v = False
        i += 1
    return rates_total

# ---- static local variables
_s_IsNewCandle_saved_candle_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SupportResistance(_MQL5Indicator):
    name = 'SupportResistance'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 20,  # The period of the indicator
        'overlook': 10,  # The overlook of period
    }

