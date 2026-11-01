"""bvsb — converted from MQL5: MQL5 Indicators/BvsB/bvsb.mq5

Bears vs Bulls
Copyright: Copyright © 2012, VladMsk; Link: vlad@rosfi.ru; Version: 1.4

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, VladMsk', 'link': 'vlad@rosfi.ru', 'version': '1.4', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bears', 2: 'Bulls'}, 'levels': [], 'description': ['Bears vs Bulls'], 'name': 'bvsb', 'source': 'MQL5 Indicators/BvsB/bvsb.mq5', 'folder': 'BvsB', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 14, 'label': 'MA Period', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 2, 'label': 'MA Method', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied Price', 'sinput': False}, {'mql': 'NeedBars', 'py': 'NeedBars', 'param': 'NeedBars', 'type': 'int', 'default': 4096, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 14)  # MA Period
MAMethod = _input('MAMethod', MODE_SMMA)  # MA Method
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # Applied Price
NeedBars = _input('NeedBars', 4096)
Bears = Arr(0, 0.0)
Bulls = Arr(0, 0.0)
PlotDrawBegin = 0
hMA = INVALID_HANDLE

def OnInit():
    SetIndexBuffer(0, Bears, INDICATOR_DATA)
    SetIndexBuffer(1, Bulls, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BvsB(' + IntegerToString(MAPeriod) + ')')
    if (not ArraySetAsSeries(Bears, False)) or (not ArraySetAsSeries(Bulls, False)):
        Print('ArraySetAsSeries for Main Calcutions, Error ', GetLastError())
        return -1
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global PlotDrawBegin, hMA
    if (not ArraySetAsSeries(low, False)) or (not ArraySetAsSeries(high, False)):
        Print('ArraySetAsSeries for low[] or high[], Error ', GetLastError())
        return 0
    if hMA == INVALID_HANDLE:
        hMA = iMA(Symbol(), Period(), MAPeriod, 0, MAMethod, AppliedPrice)
        if hMA == INVALID_HANDLE:
            Print('No MA! Error # ', GetLastError())
            return 0
    i = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        begin = MAPeriod + 1
        PlotDrawBegin = begin
        if PlotDrawBegin < (rates_total - NeedBars):
            PlotDrawBegin = rates_total - NeedBars
        if PlotDrawBegin <= 0 or PlotDrawBegin >= rates_total:
            Print('No DATA!')
            return 0
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, PlotDrawBegin)
        nbegin = PlotDrawBegin - begin
        if nbegin > begin:
            begin = nbegin
        limit = begin
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        if False:
            return 0
        MA = Arr.of([0.0], fill=0.0, dyn=False, size=1)
        if CopyBuffer(hMA, 0, rates_total - i, 1, MA) < 1:
            return i - 1
        tMA = MA[0]
        Bears[i] = _fdiv(tMA - low[i], Point())
        Bulls[i] = _fdiv(high[i] - tMA, Point())
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bvsb(_MQL5Indicator):
    name = 'bvsb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 14,  # MA Period
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # MA Method
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied Price
        'NeedBars': 4096,
    }

