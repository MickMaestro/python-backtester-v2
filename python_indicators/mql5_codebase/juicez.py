"""JuiceZ — converted from MQL5: MQL5 Indicators/JuiceZ/JuiceZ.mq5

Copyright: Copyright © 2007, Perky_z; Link: http://fxovereasy.atspace.com/index; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Perky_z', 'link': 'http://fxovereasy.atspace.com/index', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [10156544, 8421504]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Juice'}, 'levels': [], 'description': [], 'name': 'JuiceZ', 'source': 'MQL5 Indicators/JuiceZ/JuiceZ.mq5', 'folder': 'JuiceZ', 'inputs': [{'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'uint', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalPeriod', 'py': 'SignalPeriod', 'param': 'SignalPeriod', 'type': 'uint', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'OsMAPrice', 'py': 'OsMAPrice', 'param': 'OsMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Level', 'py': 'Level', 'param': 'Level', 'type': 'uint', 'default': 40, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastPeriod = _input('FastPeriod', 12)
SlowPeriod = _input('SlowPeriod', 26)
SignalPeriod = _input('SignalPeriod', 9)
OsMAPrice = _input('OsMAPrice', PRICE_CLOSE)
Level = _input('Level', 40)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
OsMA_Handle = 0

def OnInit():
    global OsMA_Handle, min_rates_total
    min_rates_total = _int(MathMax(FastPeriod, SlowPeriod) + SignalPeriod)
    OsMA_Handle = iOsMA(None, 0, FastPeriod, SlowPeriod, SignalPeriod, OsMAPrice)
    if OsMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iOsMA')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = 'Juice'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(OsMA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    OsMA_ = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(OsMA_Handle, 0, 0, to_copy, IndBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = MathAbs(IndBuffer[bar])
        IndBuffer[bar] = _fdiv(IndBuffer[bar], Point())
        IndBuffer[bar] -= Level
        clr = 1
        if IndBuffer[bar] > 0:
            clr = 0
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JuiceZ(_MQL5Indicator):
    name = 'JuiceZ'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastPeriod': 12,
        'SlowPeriod': 26,
        'SignalPeriod': 9,
        'OsMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Level': 40,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

