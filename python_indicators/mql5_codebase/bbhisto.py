"""bbhisto — converted from MQL5: MQL5 Indicators/bbhisto/bbhisto.mq5

Copyright: Copyright © 2005, Nick Bilak; Link: http://metatrader.50webs.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Nick Bilak', 'link': 'http://metatrader.50webs.com/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 3, 2: 5, 3: 5}, 'colors': {1: [13382297], 2: [16760576], 3: [16711935]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Histogram', 2: 'Buy', 3: 'Sell'}, 'levels': [], 'description': [], 'name': 'bbhisto', 'source': 'MQL5 Indicators/bbhisto/bbhisto.mq5', 'folder': 'bbhisto', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 13)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
MA_Handle = 0
STD_Handle = 0

def OnInit():
    global MA_Handle, STD_Handle, min_rates_total
    min_rates_total = _int(MAPeriod)
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of iMA')
        return INIT_FAILED
    STD_Handle = iStdDev(None, 0, MAPeriod, 0, MAType, MAPrice)
    if STD_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStdDev indicator')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'bbhisto')
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(MA_Handle) < rates_total or BarsCalculated(STD_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MA = Arr(0, 0.0)
    STD = Arr(0, 0.0)
    BB = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    if CopyBuffer(STD_Handle, 0, 0, to_copy, STD) <= 0:
        return 0
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(STD, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        IndBuffer[bar] = EMPTY_VALUE
        if STD[bar] < 0.0001:
            STD[bar] = 0.0001
        BB = (4 * _fdiv(close[bar] + (2 * STD[bar]) - MA[bar], 4 * STD[bar])) - 2
        BB = BB / 3
        IndBuffer[bar] = BB
        if BB >= 0:
            UpBuffer[bar] = 1.0
        else:
            DnBuffer[bar] = -1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bbhisto(_MQL5Indicator):
    name = 'bbhisto'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 13,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

