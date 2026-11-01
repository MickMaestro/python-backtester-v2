"""Iin_MA_Signal — converted from MQL5: MQL5 Indicators/Iin_MA_Signal/Iin_MA_Signal.mq5

Copyright: Copyright © 2007, Iin Zulkarnainn; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Iin Zulkarnainn', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Iin_MA_Signal Sell', 2: 'Iin_MA_Signal Buy'}, 'levels': [], 'description': [''], 'name': 'Iin_MA_Signal', 'source': 'MQL5 Indicators/Iin_MA_Signal/Iin_MA_Signal.mq5', 'folder': 'Iin_MA_Signal', 'inputs': [{'mql': 'FastMAPeriod', 'py': 'FastMAPeriod', 'param': 'FastMAPeriod', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'FastMAType', 'py': 'FastMAType', 'param': 'FastMAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastMAPrice', 'py': 'FastMAPrice', 'param': 'FastMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'SlowMAPeriod', 'py': 'SlowMAPeriod', 'param': 'SlowMAPeriod', 'type': 'uint', 'default': 22, 'label': '', 'sinput': False}, {'mql': 'SlowMAType', 'py': 'SlowMAType', 'param': 'SlowMAType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SlowMAPrice', 'py': 'SlowMAPrice', 'param': 'SlowMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastMAPeriod = _input('FastMAPeriod', 10)
FastMAType = _input('FastMAType', MODE_EMA)
FastMAPrice = _input('FastMAPrice', PRICE_CLOSE)
SlowMAPeriod = _input('SlowMAPeriod', 22)
SlowMAType = _input('SlowMAType', MODE_SMA)
SlowMAPrice = _input('SlowMAPrice', PRICE_CLOSE)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
AtrPeriod = 0
FsMA_Handle = 0
SlMA_Handle = 0

def OnInit():
    global AtrPeriod, FsMA_Handle, SlMA_Handle, min_rates_total
    AtrPeriod = 10
    min_rates_total = _int(MathMax(MathMax(FastMAPeriod, SlowMAPeriod) + 3, AtrPeriod))
    FsMA_Handle = iMA(None, 0, FastMAPeriod, 0, FastMAType, FastMAPrice)
    if FsMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    SlMA_Handle = iMA(None, 0, SlowMAPeriod, 0, SlowMAType, SlowMAPrice)
    if SlMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 175)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 175)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Iin_MA_Signal(' + _str(FastMAPeriod) + ',' + _str(SlowMAPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def GetRange(index, High, Low, Len):
    AvgRange = 0.0
    for count in range(_int(index + Len - 1), index - 1, -1):
        AvgRange += MathAbs(High[count] - Low[count])
    return _fdiv(AvgRange, Len)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend
    if (BarsCalculated(FsMA_Handle) < rates_total or BarsCalculated(SlMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    FsMA = Arr(0, 0.0)
    SlMA = Arr(0, 0.0)
    fasterMAnow = 0.0
    slowerMAnow = 0.0
    fasterMAprevious = 0.0
    slowerMAprevious = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    ArraySetAsSeries(FsMA, True)
    ArraySetAsSeries(SlMA, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if CopyBuffer(FsMA_Handle, 0, 0, to_copy, FsMA) <= 0:
        return 0
    if CopyBuffer(SlMA_Handle, 0, 0, to_copy, SlMA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        fasterMAnow = FsMA[bar]
        fasterMAprevious = FsMA[bar + 1]
        slowerMAnow = SlMA[bar]
        slowerMAprevious = SlMA[bar + 1]
        if (_s_OnCalculate_trend <= 0 and fasterMAnow > slowerMAnow) and fasterMAprevious < slowerMAprevious:
            BuyBuffer[bar] = low[bar] - (GetRange(bar, high, low, AtrPeriod) * 0.5)
            if bar:
                _s_OnCalculate_trend = 1
        if (_s_OnCalculate_trend >= 0 and fasterMAnow < slowerMAnow) and fasterMAprevious > slowerMAprevious:
            SellBuffer[bar] = high[bar] + (GetRange(bar, high, low, AtrPeriod) * 0.5)
            if bar:
                _s_OnCalculate_trend = -1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IinMASignal(_MQL5Indicator):
    name = 'Iin_MA_Signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastMAPeriod': 10,
        'FastMAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'FastMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'SlowMAPeriod': 22,
        'SlowMAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'SlowMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

