"""fp — converted from MQL5: MQL5 Indicators/FP channel/fp.mq5

FP channel
Copyright: Copyright © 2006, Nick A. Zhilin; Link: rebus@dialup.etr.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Nick A. Zhilin', 'link': 'rebus@dialup.etr.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [13434880], 2: [11186720], 3: [2237106]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'FP', 2: '+FP', 3: '-FP'}, 'levels': [], 'description': ['FP channel'], 'name': 'fp', 'source': 'MQL5 Indicators/FP channel/fp.mq5', 'folder': 'FP channel', 'inputs': [{'mql': 'IPeriod', 'py': 'IPeriod', 'param': 'IPeriod', 'type': 'uint', 'default': 100, 'label': 'Indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
IPeriod = _input('IPeriod', 100)  # Indicator period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
FPBuffer = Arr(0, 0.0)
UpFPBuffer = Arr(0, 0.0)
DnFPBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(IPeriod)
    SetIndexBuffer(0, FPBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(FPBuffer, True)
    SetIndexBuffer(1, UpFPBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, DnFPBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpFPBuffer, True)
    ArraySetAsSeries(DnFPBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FP channel')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    max_ = 0.0
    min_ = 0.0
    pivot = 0.0
    middle = 0.0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    for bar in range(limit, 0 - 1, -1):
        max_ = high[ArrayMaximum(high, bar, IPeriod)]
        min_ = low[ArrayMinimum(low, bar, IPeriod)]
        pivot = (close[bar + 1] + close[bar + 2] + close[bar + 3]) / 3
        middle = (max_ + min_ + pivot) / 3
        FPBuffer[bar] = middle
        UpFPBuffer[bar] = ((3 * middle) - min_) / 2
        DnFPBuffer[bar] = ((3 * middle) - max_) / 2
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fp(_MQL5Indicator):
    name = 'fp'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IPeriod': 100,  # Indicator period
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

