"""coeffofline_true — converted from MQL5: MQL5 Indicators/CoeffofLine_true_HTF/coeffofline_true.mq5

Copyright: Ramdass - Conversion only; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Ramdass - Conversion only', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [15624315]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'coeffofline_true', 'source': 'MQL5 Indicators/CoeffofLine_true_HTF/coeffofline_true.mq5', 'folder': 'CoeffofLine_true_HTF', 'inputs': [{'mql': 'SMMAPeriod', 'py': 'SMMAPeriod', 'param': 'SMMAPeriod', 'type': 'int', 'default': 5, 'label': 'Период усреднения', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SMMAPeriod = _input('SMMAPeriod', 5)  # Период усреднения
ExtLineBuffer = Arr(0, 0.0)
Handle_v = 0

def OnInit():
    global Handle_v
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (2 * SMMAPeriod) + 3)
    ArraySetAsSeries(ExtLineBuffer, True)
    Handle_v = iMA(None, 0, SMMAPeriod, 3, MODE_SMMA, PRICE_MEDIAN)
    if Handle_v == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора SMMA')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Handle_v) < rates_total or rates_total < ((2 * SMMAPeriod) - 1):
        return 0
    to_copy = 0
    limit = 0
    Count = 0
    bar = 0
    cnt = 0
    iii = 0
    ndot = SMMAPeriod
    Sum = 0.0
    SMMA = Arr(0, 0.0)
    TYVar = 0.0
    ZYVar = 0.0
    TIndicatorVar = 0.0
    ZIndicatorVar = 0.0
    M = 0.0
    N = 0.0
    AY = 0.0
    AIndicator = 0.0
    ArraySetAsSeries(SMMA, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - SMMAPeriod - ndot - 1
        to_copy = rates_total - SMMAPeriod
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + ndot + 1
    if CopyBuffer(Handle_v, 0, 0, to_copy, SMMA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        TYVar = 0.0
        ZYVar = 0.0
        N = 0.0
        M = 0.0
        TIndicatorVar = 0.0
        ZIndicatorVar = 0.0
        cnt = ndot
        for cnt in range(cnt, 1 - 1, -1):
            iii = bar + cnt - 1
            Sum = (high[iii] + low[iii]) / 2
            Count = SMMAPeriod + 1 - cnt
            ZYVar += ((high[bar + cnt - 1] + low[bar + cnt - 1]) / 2) * (6 - cnt)
            TYVar += Sum
            N += cnt * cnt
            M += cnt
            ZIndicatorVar += SMMA[iii] * Count
            TIndicatorVar += SMMA[iii]
        else:
            cnt = _range_end(cnt, 1 - 1, -1)
        AY = _fdiv(TYVar + _fdiv((N - (2 * ZYVar)) * ndot, M), M)
        AIndicator = _fdiv(TIndicatorVar + _fdiv((N - (2 * ZIndicatorVar)) * ndot, M), M)
        if ((((((Symbol() == 'EURUSD' or Symbol() == 'GBPUSD') or Symbol() == 'USDCAD') or Symbol() == 'USDCHF') or Symbol() == 'EURGBP') or Symbol() == 'EURCHF') or Symbol() == 'AUDUSD') or Symbol() == 'GBPCHF':
            ExtLineBuffer[bar] = -1000 * MathLog(_fdiv(AY, AIndicator))
        else:
            ExtLineBuffer[bar] = 1000 * MathLog(_fdiv(AY, AIndicator))
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CoeffoflineTrue(_MQL5Indicator):
    name = 'coeffofline_true'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SMMAPeriod': 5,  # Период усреднения
    }

