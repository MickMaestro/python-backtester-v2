"""ifxanalyser — converted from MQL5: MQL5 Indicators/iFXAnalyser_HTF/ifxanalyser.mq5

Copyright: Copyright © 2006, Renato P. dos Santos; Link: http://www.strategybuilderfx.com/forums/showthread.php?t=16086; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Renato P. dos Santos', 'link': 'http://www.strategybuilderfx.com/forums/showthread.php?t=16086', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Div', 2: 'Slope', 3: 'Acel'}, 'levels': [], 'description': [''], 'name': 'ifxanalyser', 'source': 'MQL5 Indicators/iFXAnalyser_HTF/ifxanalyser.mq5', 'folder': 'iFXAnalyser_HTF', 'inputs': [{'mql': 'FastMAPeriod', 'py': 'FastMAPeriod', 'param': 'FastMAPeriod', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'FastMAType', 'py': 'FastMAType', 'param': 'FastMAType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'FastMAPrice', 'py': 'FastMAPrice', 'param': 'FastMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'SlowMAPeriod', 'py': 'SlowMAPeriod', 'param': 'SlowMAPeriod', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'SlowMAType', 'py': 'SlowMAType', 'param': 'SlowMAType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SlowMAPrice', 'py': 'SlowMAPrice', 'param': 'SlowMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastMAPeriod = _input('FastMAPeriod', 4)
FastMAType = _input('FastMAType', MODE_SMA)
FastMAPrice = _input('FastMAPrice', PRICE_CLOSE)
SlowMAPeriod = _input('SlowMAPeriod', 6)
SlowMAType = _input('SlowMAType', MODE_SMA)
SlowMAPrice = _input('SlowMAPrice', PRICE_CLOSE)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
min_rates_total = 0
FsMA_Handle = 0
SlMA_Handle = 0

def OnInit():
    global FsMA_Handle, SlMA_Handle, min_rates_total
    min_rates_total = _int(MathMax(FastMAPeriod, SlowMAPeriod) + 3)
    FsMA_Handle = iMA(Symbol(), PERIOD_CURRENT, FastMAPeriod, 0, FastMAType, FastMAPrice)
    if FsMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Fast iMA')
        return INIT_FAILED
    SlMA_Handle = iMA(Symbol(), PERIOD_CURRENT, SlowMAPeriod, 0, SlowMAType, SlowMAPrice)
    if SlMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Slow iMA')
        return INIT_FAILED
    SetIndexBuffer(0, Ind1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind1Buffer, True)
    SetIndexBuffer(1, Ind2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind2Buffer, True)
    SetIndexBuffer(2, Ind3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind3Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'i-iFXAnalyser(', FastMAPeriod, ',', SlowMAPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(FsMA_Handle) < rates_total or BarsCalculated(SlMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    FsMA = Arr(0, 0.0)
    SlMA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 3
    if CopyBuffer(FsMA_Handle, 0, 0, to_copy, FsMA) <= 0:
        return 0
    if CopyBuffer(SlMA_Handle, 0, 0, to_copy, SlMA) <= 0:
        return 0
    ArraySetAsSeries(FsMA, True)
    ArraySetAsSeries(SlMA, True)
    bar = 0
    for bar in range(bar, limit):
        Ind1Buffer[bar] = FsMA[bar] - SlMA[bar]
        diff = FsMA[bar + 1] - SlMA[bar + 1]
        Ind2Buffer[bar] = Ind1Buffer[bar] - diff
        Ind3Buffer[bar] = Ind2Buffer[bar] - diff - (FsMA[bar + 2] - SlMA[bar + 2])
    else:
        bar = _range_end(bar, limit, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ifxanalyser(_MQL5Indicator):
    name = 'ifxanalyser'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastMAPeriod': 4,
        'FastMAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'FastMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'SlowMAPeriod': 6,
        'SlowMAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'SlowMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

