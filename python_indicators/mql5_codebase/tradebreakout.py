"""tradebreakout — converted from MQL5: MQL5 Indicators/TradeBreakOut/tradebreakout.mq5

Red line crossing 0 from above is a support breakout signal.
Green line crossing 0 from below is a resistance breakout signal.
Copyright: Copyright © 2013, Andriy Moraru; Link: http://www.earnforex.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Andriy Moraru', 'link': 'http://www.earnforex.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [8421376]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Resistance Breakout', 2: 'Support Breakout'}, 'levels': [0.0], 'description': ['Red line crossing 0 from above is a support breakout signal.', 'Green line crossing 0 from below is a resistance breakout signal.'], 'name': 'tradebreakout', 'source': 'MQL5 Indicators/TradeBreakOut/tradebreakout.mq5', 'folder': 'TradeBreakOut', 'inputs': [{'mql': 'L', 'py': 'L', 'param': 'L', 'type': 'uint', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'PriceType', 'py': 'PriceType', 'param': 'PriceType', 'type': 'int', 'default': 1, 'label': 'price calculation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum price_type
Close = 0
HighLow = 1
_enum('price_type', {0: 'Close', 1: 'HighLow'})

# ---- inputs and global variables
L = _input('L', 50)  # Period
PriceType = _input('PriceType', HighLow)  # price calculation
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(L)
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TradeBreakOut')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    HH = 0.0
    LL = 0.0
    HC = 0.0
    LC = 0.0
    if PriceType == Close:
        ArraySetAsSeries(close, True)
    else:
        ArraySetAsSeries(high, True)
        ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        bar = rates_total - 1
        for bar in range(bar, limit, -1):
            ExtLineBuffer1[bar] = 0.0
            ExtLineBuffer2[bar] = 0.0
        else:
            bar = _range_end(bar, limit, -1)
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if PriceType == Close:
            HC = close[ArrayMaximum(close, bar, L)]
            LC = close[ArrayMinimum(close, bar, L)]
            ExtLineBuffer2[bar] = _fdiv(close[bar] - HC, HC)
            ExtLineBuffer1[bar] = _fdiv(close[bar] - LC, LC)
        else:
            HH = high[ArrayMaximum(high, bar, L)]
            LL = low[ArrayMinimum(low, bar, L)]
            ExtLineBuffer2[bar] = _fdiv(high[bar] - HH, HH)
            ExtLineBuffer1[bar] = _fdiv(low[bar] - LL, LL)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tradebreakout(_MQL5Indicator):
    name = 'tradebreakout'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'L': 50,  # Period
        'PriceType': _Choice({0: 'by close prices', 1: 'by extremums'}, default=1),  # price calculation
    }

