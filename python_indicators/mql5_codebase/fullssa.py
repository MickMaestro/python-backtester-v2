"""fullssa — converted from MQL5: MQL5 Indicators/FullSSA/fullssa.mq5

Copyright: Copyright © 2007, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.ssa import *  # #include ssa.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2007, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'FullSSA'}, 'levels': [], 'description': [], 'name': 'fullssa', 'source': 'MQL5 Indicators/FullSSA/fullssa.mq5', 'folder': 'FullSSA', 'inputs': [{'mql': 'Lag', 'py': 'Lag', 'param': 'Lag', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'NumComps', 'py': 'NumComps', 'param': 'NumComps', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'PeriodNorm', 'py': 'PeriodNorm', 'param': 'PeriodNorm', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'iN', 'py': 'iN', 'param': 'iN', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['ssa.mqh']}

# ---- inputs and global variables
Lag = _input('Lag', 10)
NumComps = _input('NumComps', 2)
PeriodNorm = _input('PeriodNorm', 10)
iN = _input('iN', 100)
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
TimeSeriesBuffer = Arr(0, 0.0)
MA_Handle = 0
STD_Handle = 0

def OnInit():
    global MA_Handle, STD_Handle, min_rates_total
    min_rates_total = _int(MathMax(Lag, PeriodNorm))
    MA_Handle = iMA(None, 0, PeriodNorm, 0, MODE_SMA, PRICE_CLOSE)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    STD_Handle = iStdDev(None, 0, PeriodNorm, 0, MODE_SMA, PRICE_CLOSE)
    if STD_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStdDev indicator')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, TimeSeriesBuffer, INDICATOR_DATA)
    ArraySetAsSeries(TimeSeriesBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FullSSA')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(MA_Handle) < rates_total or BarsCalculated(STD_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - iN)
    to_copy = 0
    limit = 0
    bar = 0
    MA = Arr(0, 0.0)
    STD = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        bar = rates_total - 1
        for bar in range(bar, limit, -1):
            IndBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, limit, -1)
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
        res = close[bar] - MA[bar]
        if STD[bar]:
            TimeSeriesBuffer[bar] = _fdiv(res, 3 * STD[bar])
        else:
            TimeSeriesBuffer[bar] = res / 0.1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    fastsingular(TimeSeriesBuffer, iN, Lag, NumComps, IndBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fullssa(_MQL5Indicator):
    name = 'fullssa'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Lag': 10,
        'NumComps': 2,
        'PeriodNorm': 10,
        'iN': 100,
    }

