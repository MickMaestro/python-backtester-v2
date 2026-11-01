"""aggressiveness — converted from MQL5: MQL5 Indicators/Aggressiveness/aggressiveness.mq5

Copyright: Copyright © 2009, Trofimov Evgeniy Vitalyevich; Link: http://TrofimovVBA.narod.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Trofimov Evgeniy Vitalyevich', 'link': 'http://TrofimovVBA.narod.ru/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Aggressiveness'}, 'levels': [], 'description': [], 'name': 'aggressiveness', 'source': 'MQL5 Indicators/Aggressiveness/aggressiveness.mq5', 'folder': 'Aggressiveness', 'inputs': [{'mql': 'MyPeriod', 'py': 'MyPeriod', 'param': 'MyPeriod', 'type': 'uint', 'default': 22, 'label': '', 'sinput': False}, {'mql': 'Lot', 'py': 'Lot', 'param': 'Lot', 'type': 'double', 'default': 0.0, 'label': 'Lot (0 - in points, >0 - in the deposit currency)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MyPeriod = _input('MyPeriod', 22)
Lot = _input('Lot', 0.0)  # Lot (0 - in points, >0 - in the deposit currency)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(MyPeriod + 1)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = ""
    if not Lot:
        shortname = 'Aggressiveness(' + _str(MyPeriod) + '), (pips) = '
    else:
        shortname = 'Aggressiveness(' + _str(MyPeriod) + '), (' + AccountInfoString(ACCOUNT_CURRENCY) + '·' + DoubleToString(Lot, 2) + ') = '
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Sum = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Sum = 0.0
        for x in range(0, _int(MyPeriod)):
            barx = bar - x
            if close[barx] > open[barx]:
                Sum += close[barx] - close[barx - 1]
            else:
                Sum += close[barx - 1] - close[barx]
        IndBuffer[bar] = _fdiv(Sum, Point() * MyPeriod)
        if Lot:
            TICKVALUE = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_VALUE)
            if not TICKVALUE:
                return prev_calculated
            IndBuffer[bar] *= TICKVALUE * Lot
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Aggressiveness(_MQL5Indicator):
    name = 'aggressiveness'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MyPeriod': 22,
        'Lot': 0.0,  # Lot (0 - in points, >0 - in the deposit currency)
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

