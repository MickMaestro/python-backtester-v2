"""rd-trendtrigger — converted from MQL5: MQL5 Indicators/RD-TrendTrigger/rd-trendtrigger.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [15624315]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RD-TrendTrigger'}, 'levels': [50.0, -50.0], 'description': [], 'name': 'rd-trendtrigger', 'source': 'MQL5 Indicators/RD-TrendTrigger/rd-trendtrigger.mq5', 'folder': 'RD-TrendTrigger', 'inputs': [{'mql': 'Regress', 'py': 'Regress', 'param': 'Regress', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'T3Length', 'py': 'T3Length', 'param': 'T3Length', 'type': 'uint', 'default': 5, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'T3Phase', 'py': 'T3Phase', 'param': 'T3Phase', 'type': 'int', 'default': 70, 'label': 'smoothing parameter', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Regress = _input('Regress', 15)
T3Length = _input('T3Length', 5)  # smoothing depth
T3Phase = _input('T3Phase', 70)  # smoothing parameter
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
min_rates_ = 0
min_rates_total = 0

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = _int((2 * Regress) + 1)
    min_rates_total = min_rates_ + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RD-TrendTrigger')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    HighestHighRecent = 0.0
    HighestHighOlder = 0.0
    LowestLowRecent = 0.0
    LowestLowOlder = 0.0
    BuyPower = 0.0
    SellPower = 0.0
    TTF = 0.0
    Res = 0.0
    limit = 0
    maxbar = 0
    maxbar = rates_total - min_rates_
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        HighestHighRecent = High[ArrayMaximum(High, bar, Regress)]
        HighestHighOlder = High[ArrayMaximum(High, bar + Regress, Regress)]
        LowestLowRecent = Low[ArrayMinimum(Low, bar, Regress)]
        LowestLowOlder = Low[ArrayMinimum(Low, bar + Regress, Regress)]
        BuyPower = HighestHighRecent - LowestLowOlder
        SellPower = HighestHighOlder - LowestLowRecent
        Res = BuyPower + SellPower
        if Res:
            TTF = _fdiv(BuyPower - SellPower, 0.5 * Res) * 100
        else:
            TTF = 0.0
        IndBuffer[bar] = T3.T3Series(maxbar, prev_calculated, rates_total, MODE_T3, T3Phase, T3Length, TTF, bar, True)
    return rates_total

# ---- global variables initialised from expressions
T3 = _alloc(CT3)
T3.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RdTrendtrigger(_MQL5Indicator):
    name = 'rd-trendtrigger'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Regress': 15,
        'T3Length': 5,  # smoothing depth
        'T3Phase': 70,  # smoothing parameter
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

