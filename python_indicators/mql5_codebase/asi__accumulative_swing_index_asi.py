"""asi — converted from MQL5: MQL5 Indicators/Accumulative Swing Index - ASI/asi.mq5

Copyright: Copyright © 2007, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [5275647]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ASI'}, 'levels': [], 'description': [], 'name': 'asi', 'source': 'MQL5 Indicators/Accumulative Swing Index - ASI/asi.mq5', 'folder': 'Accumulative Swing Index - ASI', 'inputs': [{'mql': 'T', 'py': 'T_v', 'param': 'T_v', 'type': 'uint', 'default': 300, 'label': 'Предел отклонения', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'uint', 'default': 1, 'label': 'ATR период', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
T_v = _input('T_v', 300)  # Предел отклонения
ATRPeriod = _input('ATRPeriod', 1)  # ATR период
ExtBuffer = Arr(0, 0.0)
Ind_Handle = 0
dT = 0.0
min_rates_total = 0

def OnInit():
    global Ind_Handle, dT, min_rates_total
    min_rates_total = _int(ATRPeriod + 1)
    Ind_Handle = iATR(Symbol(), PERIOD_CURRENT, ATRPeriod)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iATR')
        return INIT_FAILED
    dT = Point() * T_v
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ASI')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or BarsCalculated(Ind_Handle) < rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    bar1 = 0
    ATR = Arr(0, 0.0)
    TR = 0.0
    ER = 0.0
    K = 0.0
    SH = 0.0
    R = 0.0
    res = 0.0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        bar1 = limit + 1
        ExtBuffer[bar1] = high[bar1] - low[bar1]
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        bar1 = bar + 1
        TR = ATR[bar]
        if close[bar + 1] >= low[bar] and close[bar + 1] <= high[bar]:
            ER = 0.0
        else:
            if close[bar1] > high[bar]:
                ER = MathAbs(high[bar] - close[bar1])
            if close[bar1] < low[bar]:
                ER = MathAbs(low[bar] - close[bar1])
        K = MathMax(MathAbs(high[bar] - close[bar1]), MathAbs(low[bar] - close[bar1]))
        SH = MathAbs(close[bar1] - open[bar1])
        R = TR - (0.5 * ER) + (0.25 * SH)
        if R:
            res = _fdiv(50 * (close[bar] - close[bar + 1] + (0.5 * (close[bar] - open[bar])) + (0.25 * (close[bar + 1] - open[bar + 1]))) * _fdiv(K, dT), R)
        else:
            res = 0.0
        ExtBuffer[bar] = ExtBuffer[bar + 1] + res
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Asi(_MQL5Indicator):
    name = 'asi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'T_v': 300,  # Предел отклонения
        'ATRPeriod': 1,  # ATR период
    }

