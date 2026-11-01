"""ema-crossover_signal — converted from MQL5: MQL5 Indicators/EMA-Crossover_Signal/ema-crossover_signal.mq5

EMA-Crossover_Signal
Copyright: Copyright © 2005, Jason Robinson (jnrtrading); Link: http://www.jnrtading.co.uk; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Jason Robinson (jnrtrading)', 'link': 'http://www.jnrtading.co.uk', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'EMA-Crossover_Signal Sell', 2: 'EMA-Crossover_Signal Buy'}, 'levels': [], 'description': ['EMA-Crossover_Signal'], 'name': 'ema-crossover_signal', 'source': 'MQL5 Indicators/EMA-Crossover_Signal/ema-crossover_signal.mq5', 'folder': 'EMA-Crossover_Signal', 'inputs': [{'mql': 'FasterMA', 'py': 'FasterMA', 'param': 'FasterMA', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'SlowerMA', 'py': 'SlowerMA', 'param': 'SlowerMA', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FasterMA = _input('FasterMA', 5)
SlowerMA = _input('SlowerMA', 6)
MAType = _input('MAType', MODE_LWMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
FsMA_Handle = 0
SlMA_Handle = 0

def OnInit():
    global FsMA_Handle, SlMA_Handle, min_rates_total
    min_rates_total = _int(MathMax(FasterMA, SlowerMA) + 3)
    FsMA_Handle = iMA(None, 0, FasterMA, 0, MAType, MAPrice)
    if FsMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    SlMA_Handle = iMA(None, 0, SlowerMA, 0, MAType, MAPrice)
    if SlMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'EMA-Crossover_Signal'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(FsMA_Handle) < rates_total or BarsCalculated(SlMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    AvgRange = 0.0
    Range = 0.0
    FsMA = Arr(0, 0.0)
    SlMA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(FsMA, True)
    ArraySetAsSeries(SlMA, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    to_copy = limit + 3
    if CopyBuffer(FsMA_Handle, 0, 0, to_copy, FsMA) <= 0:
        return 0
    if CopyBuffer(SlMA_Handle, 0, 0, to_copy, SlMA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        AvgRange = 0.0
        for count in range(bar + 9, bar - 1, -1):
            AvgRange += MathAbs(high[count] - low[count])
        Range = AvgRange / 10
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        if (FsMA[bar + 1] > SlMA[bar + 1] and FsMA[bar + 2] < SlMA[bar + 2]) and FsMA[bar] > SlMA[bar]:
            BuyBuffer[bar] = low[bar] - (Range * 0.5)
        elif (FsMA[bar + 1] < SlMA[bar + 1] and FsMA[bar + 2] > SlMA[bar + 2]) and FsMA[bar] < SlMA[bar]:
            SellBuffer[bar] = high[bar] + (Range * 0.5)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EmaCrossoverSignal(_MQL5Indicator):
    name = 'ema-crossover_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FasterMA': 5,
        'SlowerMA': 6,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

