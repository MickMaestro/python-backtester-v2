"""adaptivecgoscillator — converted from MQL5: MQL5 Indicators/AdaptiveCGOscillator_HTF/adaptivecgoscillator.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Adaptive CG Oscillator', 2: 'Trigger'}, 'levels': [0.0], 'description': [], 'name': 'adaptivecgoscillator', 'source': 'MQL5 Indicators/AdaptiveCGOscillator_HTF/adaptivecgoscillator.mq5', 'folder': 'AdaptiveCGOscillator_HTF', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 0.07, 'label': 'Коэффициент усреднения индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha = _input('Alpha', 0.07)  # Коэффициент усреднения индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ACGBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
CP_Handle = 0
min_rates_total = 0

def OnInit():
    global CP_Handle, min_rates_total
    min_rates_total = 1
    CP_Handle = iCustom(None, 0, 'CyclePeriod', Alpha)
    if CP_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CyclePeriod')
        return INIT_FAILED
    SetIndexBuffer(0, ACGBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Adaptive CG Oscillator(', DoubleToString(Alpha, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(CP_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    intperiod = 0
    price = 0.0
    Num = 0.0
    Denom = 0.0
    period = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if CopyBuffer(CP_Handle, 0, rates_total - 1 - bar, 1, period) <= 0:
            return 0
        intperiod = _int(MathFloor(period[0] / 2.0))
        Num = 0.0
        Denom = 0.0
        if bar < intperiod:
            intperiod = bar
        for count in range(0, intperiod):
            price = (high[bar - count] + low[bar - count]) / 2.0
            Num += (1.0 + count) * price
            Denom += price
        if Denom != 0.0:
            ACGBuffer[bar] = _fdiv(-Num, Denom) + ((intperiod + 1.0) / 2.0)
        else:
            ACGBuffer[bar] = EMPTY_VALUE
        TriggerBuffer[bar] = ACGBuffer[bar - 1]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Adaptivecgoscillator(_MQL5Indicator):
    name = 'adaptivecgoscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 0.07,  # Коэффициент усреднения индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

