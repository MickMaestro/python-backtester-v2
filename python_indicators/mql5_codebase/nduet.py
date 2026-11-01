"""nduet — converted from MQL5: MQL5 Indicators/NDuet/nduet.mq5

Copyright: Copyright © 2006, Tartan; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Tartan', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [255], 2: [16711680], 3: [65280], 4: [255]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'NDuet Fast Line', 2: 'NDuet Slow Line', 3: 'NDuet Buy', 4: 'NDuet Sell'}, 'levels': [], 'description': [], 'name': 'nduet', 'source': 'MQL5 Indicators/NDuet/nduet.mq5', 'folder': 'NDuet', 'inputs': [{'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'uint', 'default': 21, 'label': 'fast moving average period', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'uint', 'default': 55, 'label': 'slow moving average period', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'uint', 'default': 14, 'label': 'CCI period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastPeriod = _input('FastPeriod', 21)  # fast moving average period
SlowPeriod = _input('SlowPeriod', 55)  # slow moving average period
CCIPeriod = _input('CCIPeriod', 14)  # CCI period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
FastBuffer = Arr(0, 0.0)
SlowBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
FsMA_Handle = 0
SlMA_Handle = 0
CCI_Handle = 0
min_rates_total = 0
ATRPeriod = 0

def OnInit():
    global ATRPeriod, CCI_Handle, FsMA_Handle, SlMA_Handle, min_rates_total
    ATRPeriod = 10
    min_rates_total = _int(MathMax(MathMax(MathMax(FastPeriod + 2, SlowPeriod + 2), CCIPeriod), ATRPeriod))
    FsMA_Handle = iMA(None, 0, FastPeriod, 0, MODE_SMA, PRICE_CLOSE)
    if FsMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the fast iMA indicator')
    SlMA_Handle = iMA(None, 0, SlowPeriod, 0, MODE_SMA, PRICE_CLOSE)
    if SlMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    CCI_Handle = iCCI(None, 0, CCIPeriod, PRICE_CLOSE)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iCCI indicator')
    SetIndexBuffer(0, FastBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(FastBuffer, True)
    SetIndexBuffer(1, SlowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SlowBuffer, True)
    SetIndexBuffer(2, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    shortname = 'NDuet'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def CountRange(High, Low, period, index):
    AvgRange = 0.0
    for count in range(index + period - 1, index - 1, -1):
        AvgRange += MathAbs(High[count] - Low[count])
    Range = _fdiv(AvgRange, period)
    Range *= 0.5
    return Range

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_trend
    if ((BarsCalculated(FsMA_Handle) < rates_total or BarsCalculated(SlMA_Handle) < rates_total) or BarsCalculated(CCI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    trend = 0
    to_copy = 0
    mas = 0.0
    maf = 0.0
    mstwo = 0.0
    mftwo = 0.0
    CCI = Arr(0, 0.0)
    Range = 0.0
    res = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        to_copy = rates_total
        _s_OnCalculate_prev_trend = 0
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    ArraySetAsSeries(CCI, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if CopyBuffer(FsMA_Handle, 0, 0, to_copy, FastBuffer) <= 0:
        return 0
    if CopyBuffer(SlMA_Handle, 0, 0, to_copy, SlowBuffer) <= 0:
        return 0
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    trend = _s_OnCalculate_prev_trend
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        mas = SlowBuffer[bar]
        mstwo = SlowBuffer[bar + 2]
        maf = FastBuffer[bar]
        mftwo = FastBuffer[bar + 2]
        res = _fdiv(mas - maf, Point())
        if (((trend != -1 and mas > maf) and res < 10) and mstwo < mftwo) and CCI[bar] < 0:
            trend = -1
            Range = CountRange(high, low, ATRPeriod, bar)
            SellBuffer[bar] = high[bar] + Range
        if (((trend != 1 and mas < maf) and (-res) < 10) and mstwo > mftwo) and CCI[bar] > 0:
            trend = 1
            Range = CountRange(high, low, ATRPeriod, bar)
            BuyBuffer[bar] = low[bar] - Range
        if bar:
            _s_OnCalculate_prev_trend = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_trend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Nduet(_MQL5Indicator):
    name = 'nduet'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastPeriod': 21,  # fast moving average period
        'SlowPeriod': 55,  # slow moving average period
        'CCIPeriod': 14,  # CCI period
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

