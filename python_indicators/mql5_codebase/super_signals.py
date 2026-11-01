"""super-signals — converted from MQL5: MQL5 Indicators/super-signals/super-signals.mq5

super-signals
Copyright: CCopyright © 2006, Nick Bilak, beluck[AT]gmail.com; Link: http://www.forex-tsd.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'CCopyright © 2006, Nick Bilak, beluck[AT]gmail.com', 'link': 'http://www.forex-tsd.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [16748574]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'super-signals Sell', 2: 'super-signals Buy'}, 'levels': [], 'description': ['super-signals'], 'name': 'super-signals', 'source': 'MQL5 Indicators/super-signals/super-signals.mq5', 'folder': 'super-signals', 'inputs': [{'mql': 'dist', 'py': 'dist', 'param': 'dist', 'type': 'uint', 'default': 24, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
dist = _input('dist', 24)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
ATRPeriod = 0

def OnInit():
    global ATRPeriod, min_rates_total
    ATRPeriod = 10
    min_rates_total = _int(MathMax(dist + 1, ATRPeriod))
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'super-signals Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'super-signals Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'super-signals'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = _int(rates_total - prev_calculated + _idiv(dist, 2))
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    for bar in range(limit, 0 - 1, -1):
        AvgRange = 0.0
        for count in range(bar, bar + ATRPeriod + 1):
            AvgRange += MathAbs(high[count] - low[count])
        Range = _fdiv(AvgRange, ATRPeriod)
        Range = Range / 3
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        barX = bar - _idiv(dist, 2)
        HH = ArrayMaximum(high, barX, dist)
        LL = ArrayMinimum(low, barX, dist)
        if bar == HH:
            SellBuffer[bar] = high[HH] + Range
        if bar == LL:
            BuyBuffer[bar] = low[LL] - Range
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperSignals(_MQL5Indicator):
    name = 'super-signals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'dist': 24,
    }

