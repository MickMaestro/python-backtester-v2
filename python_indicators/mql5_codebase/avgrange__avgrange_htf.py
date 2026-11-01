"""avgrange — converted from MQL5: MQL5 Indicators/AvgRange_HTF/avgrange.mq5

Copyright: Copyright © 2005, tageiger aka fxid10t@yahoo.com; Link: http://www.metatrader.org; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, tageiger aka fxid10t@yahoo.com', 'link': 'http://www.metatrader.org', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper', 2: 'Lover'}, 'levels': [], 'description': [''], 'name': 'avgrange', 'source': 'MQL5 Indicators/AvgRange_HTF/avgrange.mq5', 'folder': 'AvgRange_HTF', 'inputs': [{'mql': 'RangePeriod', 'py': 'RangePeriod', 'param': 'RangePeriod', 'type': 'uint', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RangePeriod = _input('RangePeriod', 200)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(RangePeriod) + 2
    SetIndexBuffer(0, Ind1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind1Buffer, True)
    SetIndexBuffer(1, Ind2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind2Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'AvgRange(', RangePeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    sum_rng = 0.0
    avg_rng = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = 0
    for bar in range(bar, limit):
        sum_rng = 0.0
        for iii in range(0, _int(RangePeriod)):
            sum_rng += high[bar + iii] - low[bar + iii]
        avg_rng = sum_rng / RangePeriod
        avg_rng = avg_rng / 2.0
        Ind1Buffer[bar] = close[bar] + avg_rng
        Ind2Buffer[bar] = close[bar] - avg_rng
    else:
        bar = _range_end(bar, limit, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Avgrange(_MQL5Indicator):
    name = 'avgrange'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RangePeriod': 200,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

