"""LRMA — converted from MQL5: MQL5 Indicators/LRMA_HTF/LRMA.mq5

Copyright: 2010,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh
from backtester.mql5.lib.indicatorsalgorithms import *  # #include indicatorsalgorithms.mqh

MQL5_META = {'props': {'copyright': '2010,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3329330]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'LRMA', 'source': 'MQL5 Indicators/LRMA_HTF/LRMA.mq5', 'folder': 'LRMA_HTF', 'inputs': [{'mql': 'LRMAPeriod', 'py': 'LRMAPeriod', 'param': 'LRMAPeriod', 'type': 'int', 'default': 13, 'label': 'Период LRMA', 'sinput': False}, {'mql': 'LRMAShift', 'py': 'LRMAShift', 'param': 'LRMAShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг LRMA по горизонтали в барах', 'sinput': False}, {'mql': 'LRMAPriceShift', 'py': 'LRMAPriceShift', 'param': 'LRMAPriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг LRMA по вертикали в пунктах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh', 'indicatorsalgorithms.mqh']}

# ---- inputs and global variables
LRMAPeriod = _input('LRMAPeriod', 13)  # Период LRMA
LRMAShift = _input('LRMAShift', 0)  # Сдвиг LRMA по горизонтали в барах
LRMAPriceShift = _input('LRMAPriceShift', 0)  # Сдвиг LRMA по вертикали в пунктах
ExtLineBuffer = Arr(0, 0.0)
dPriceShift = 0.0

def OnInit():
    global dPriceShift
    short_name = 'LRMA'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + '(' + _str(LRMAPeriod) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, LRMAPeriod + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, LRMAShift)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    dPriceShift = Point() * LRMAPriceShift
    LRMA1 = CMoving_Average()
    LRMA1.MALengthCheck_1('LRMAPeriod', LRMAPeriod)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (begin + LRMAPeriod):
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = begin
        bar = 0
        for bar in range(bar, begin + 1):
            ExtLineBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, begin + 1, 1)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtLineBuffer[bar] = _s_OnCalculate_LRMA1.LRMASeries(begin, prev_calculated, rates_total, LRMAPeriod, price[bar], bar, False) + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LRMA1 = CLRMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LRMA(_MQL5Indicator):
    name = 'LRMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LRMAPeriod': 13,  # Период LRMA
        'LRMAShift': 0,  # Сдвиг LRMA по горизонтали в барах
        'LRMAPriceShift': 0,  # Сдвиг LRMA по вертикали в пунктах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

