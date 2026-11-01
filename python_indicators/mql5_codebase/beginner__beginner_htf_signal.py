"""beginner — converted from MQL5: MQL5 Indicators/Beginner_HTF_Signal/beginner.mq5

Beginner - basic indicator for marking chart's highs and lows.
Repaints.
Исправленая версия индикатора!
Copyright: Copyright © 2009, EarnForex; Link: http://www.earnforex.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, EarnForex', 'link': 'http://www.earnforex.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16748574]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Beginner Sell', 2: 'Beginner Buy'}, 'levels': [], 'description': ["Beginner - basic indicator for marking chart's highs and lows.", 'Repaints.', 'Исправленая версия индикатора!'], 'name': 'beginner', 'source': 'MQL5 Indicators/Beginner_HTF_Signal/beginner.mq5', 'folder': 'Beginner_HTF_Signal', 'inputs': [{'mql': 'Otstup', 'py': 'Otstup', 'param': 'Otstup', 'type': 'uint', 'default': 30, 'label': 'Shift', 'sinput': False}, {'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'uint', 'default': 9, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Otstup = _input('Otstup', 30)  # Shift
Per = _input('Per', 9)  # Period
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
ATRPeriod = 0

def OnInit():
    global ATRPeriod, min_rates_total
    ATRPeriod = 10
    min_rates_total = _int(MathMax(Per, ATRPeriod))
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'Beginner Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'Beginner Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Beginner'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def GetRange(Len, H, L, index):
    AvgRange = 0.0
    Range = 0.0
    AvgRange = 0.0
    for count in range(index, _int(index + Len)):
        AvgRange += MathAbs(H[count] - L[count])
    Range = _fdiv(AvgRange, Len)
    return Range

def OnCalculate(rates_total, prev_calculated, time, open, High, Low, Close, tick_volume, volume, spread):
    global _s_OnCalculate_trend
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    Range = 0.0
    SHMax = 0.0
    SHMin = 0.0
    diff = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend = 0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Range = GetRange(ATRPeriod, High, Low, bar) / 3
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        SHMax = High[ArrayMaximum(High, bar, Per)]
        SHMin = Low[ArrayMinimum(Low, bar, Per)]
        diff = ((SHMax - SHMin) * Otstup) / 100.0
        if Close[bar] < (SHMin + diff) and _s_OnCalculate_trend != -1:
            SellBuffer[bar] = High[bar] + Range
            if bar:
                _s_OnCalculate_trend = -1
        elif Close[bar] > (SHMax - diff) and _s_OnCalculate_trend != 1:
            BuyBuffer[bar] = Low[bar] - Range
            if bar:
                _s_OnCalculate_trend = 1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Beginner(_MQL5Indicator):
    name = 'beginner'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Otstup': 30,  # Shift
        'Per': 9,  # Period
    }

