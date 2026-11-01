"""w_ad — converted from MQL5: MQL5 Indicators/Williams'Accumulation_Distribution (W_A_D)/w_ad.mq5

Larry Williams' Accumulation/Distribution
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11186720]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ["Larry Williams' Accumulation/Distribution"], 'name': 'w_ad', 'source': "MQL5 Indicators/Williams'Accumulation_Distribution (W_A_D)/w_ad.mq5", 'folder': "Williams'Accumulation_Distribution (W_A_D)", 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtWADBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtWADBuffer)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'W_A/D')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < 2:
        return 0
    pos = prev_calculated - 1
    if pos <= 0:
        pos = 1
        ExtWADBuffer[0] = 0.0
    for i in range(pos, rates_total):
        hi = High[i]
        lo = Low[i]
        cl = Close[i]
        prev_cl = Close[i - 1]
        trh = MathMax(hi, prev_cl)
        trl = MathMin(lo, prev_cl)
        if IsEqualDoubles(cl, prev_cl, Point()):
            ExtWADBuffer[i] = ExtWADBuffer[i - 1]
        else:
            if cl > prev_cl:
                ExtWADBuffer[i] = ExtWADBuffer[i - 1] + cl - trl
            else:
                ExtWADBuffer[i] = ExtWADBuffer[i - 1] + cl - trh
    return rates_total

def IsEqualDoubles(d1, d2, epsilon):
    if epsilon < 0.0:
        epsilon = -epsilon
    if epsilon > 0.1:
        epsilon = 1e-05
    diff = d1 - d2
    if diff > epsilon or diff < (-epsilon):
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WAd(_MQL5Indicator):
    name = 'w_ad'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

