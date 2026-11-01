"""roc — converted from MQL5: MQL5 Indicators/Price Rate of Change (ROC)/roc.mq5

Rate of Change
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11186720]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Rate of Change'], 'name': 'roc', 'source': 'MQL5 Indicators/Price Rate of Change (ROC)/roc.mq5', 'folder': 'Price Rate of Change (ROC)', 'inputs': [{'mql': 'InpRocPeriod', 'py': 'InpRocPeriod', 'param': 'InpRocPeriod', 'type': 'int', 'default': 12, 'label': 'Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpRocPeriod = _input('InpRocPeriod', 12)  # Period
ExtRocBuffer = Arr(0, 0.0)
ExtRocPeriod = 0

def OnInit():
    global ExtRocPeriod
    if InpRocPeriod < 1:
        ExtRocPeriod = 12
        Print('Incorrect value for input variable InpRocPeriod =', InpRocPeriod, 'Indicator will use value =', ExtRocPeriod, 'for calculations.')
    else:
        ExtRocPeriod = InpRocPeriod
    SetIndexBuffer(0, ExtRocBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ROC(' + _str(ExtRocPeriod) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtRocPeriod)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < ExtRocPeriod:
        return 0
    pos = prev_calculated - 1
    if pos < ExtRocPeriod:
        pos = ExtRocPeriod
    for i in range(pos, rates_total):
        if price[i] == 0.0:
            ExtRocBuffer[i] = 0.0
        else:
            ExtRocBuffer[i] = _fdiv(price[i] - price[i - ExtRocPeriod], price[i]) * 100
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Roc(_MQL5Indicator):
    name = 'roc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpRocPeriod': 12,  # Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

