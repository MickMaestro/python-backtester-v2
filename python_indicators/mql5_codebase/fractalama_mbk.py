"""fractalama_mbk — converted from MQL5: MQL5 Indicators/FractalAMA/fractalama_mbk.mq5

Copyright: Copyright © 2005, MrPip; Link: mbkennelfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MrPip', 'link': 'mbkennelfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [36095], 2: [13458026]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'FractalAMA', 2: 'Trigger'}, 'levels': [], 'description': [], 'name': 'fractalama_mbk', 'source': 'MQL5 Indicators/FractalAMA/fractalama_mbk.mq5', 'folder': 'FractalAMA', 'inputs': [{'mql': 'RPeriod', 'py': 'RPeriod', 'param': 'RPeriod', 'type': 'uint', 'default': 16, 'label': '', 'sinput': False}, {'mql': 'multiplier', 'py': 'multiplier', 'param': 'multiplier', 'type': 'double', 'default': 4.6, 'label': '', 'sinput': False}, {'mql': 'signal_multiplier', 'py': 'signal_multiplier', 'param': 'signal_multiplier', 'type': 'double', 'default': 2.5, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RPeriod = _input('RPeriod', 16)
multiplier = _input('multiplier', 4.6)
signal_multiplier = _input('signal_multiplier', 2.5)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
FrAmaBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
N = 0

def Range(index, Low, High, period):
    return High[ArrayMaximum(High, index, period)] - Low[ArrayMinimum(Low, index, period)]

def DEst(index, Low, High, period):
    R1 = 0.0
    R2 = 0.0
    R3 = 0.0
    n2 = _idiv(period, 2)
    R3 = _fdiv(Range(index, Low, High, period), period)
    R1 = _fdiv(Range(index, Low, High, n2), n2)
    R2 = _fdiv(Range(index + n2, Low, High, n2), n2)
    return (MathLog(R1 + R2) - MathLog(R3)) * 1.442695

def OnInit():
    global N, min_rates_total
    min_rates_total = _int(RPeriod)
    N = _int(MathFloor(_idiv(RPeriod, 2)) * 2)
    SetIndexBuffer(0, FrAmaBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(FrAmaBuffer, True)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(TriggerBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'FractalAMA(', RPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    dimension_estimate = 0.0
    alpha = 0.0
    alphas = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        start = limit + 1
        FrAmaBuffer[start] = close[start]
        TriggerBuffer[start] = close[start]
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        dimension_estimate = DEst(bar, low, high, N)
        alpha = MathExp((-multiplier) * (dimension_estimate - 1.0))
        alphas = MathExp((-signal_multiplier) * (dimension_estimate - 1.0))
        alpha = MathMin(alpha, 1.0)
        alpha = MathMax(alpha, 0.01)
        FrAmaBuffer[bar] = (alpha * close[bar]) + ((1.0 - alpha) * FrAmaBuffer[bar + 1])
        TriggerBuffer[bar] = (alphas * FrAmaBuffer[bar]) + ((1.0 - alphas) * TriggerBuffer[bar + 1])
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalamaMbk(_MQL5Indicator):
    name = 'fractalama_mbk'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RPeriod': 16,
        'multiplier': 4.6,
        'signal_multiplier': 2.5,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

