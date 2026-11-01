"""Iin_MA_Signal_Candle — converted from MQL5: MQL5 Indicators/Iin_MA_Signal_Candle/Iin_MA_Signal_Candle.mq5

Copyright: Copyright © 2007, Iin Zulkarnainn; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Iin Zulkarnainn', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [3329330, 8421376, 8388736, 4678655]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Iin_MA_SignalOpen;Iin_MA_SignalHigh;Iin_MA_SignalLow;Iin_MA_SignalClose'}, 'levels': [], 'description': [''], 'name': 'Iin_MA_Signal_Candle', 'source': 'MQL5 Indicators/Iin_MA_Signal_Candle/Iin_MA_Signal_Candle.mq5', 'folder': 'Iin_MA_Signal_Candle', 'inputs': [{'mql': 'FastMAPeriod', 'py': 'FastMAPeriod', 'param': 'FastMAPeriod', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'FastMAType', 'py': 'FastMAType', 'param': 'FastMAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastMAPrice', 'py': 'FastMAPrice', 'param': 'FastMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'SlowMAPeriod', 'py': 'SlowMAPeriod', 'param': 'SlowMAPeriod', 'type': 'uint', 'default': 22, 'label': '', 'sinput': False}, {'mql': 'SlowMAType', 'py': 'SlowMAType', 'param': 'SlowMAType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SlowMAPrice', 'py': 'SlowMAPrice', 'param': 'SlowMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastMAPeriod = _input('FastMAPeriod', 10)
FastMAType = _input('FastMAType', MODE_EMA)
FastMAPrice = _input('FastMAPrice', PRICE_CLOSE)
SlowMAPeriod = _input('SlowMAPeriod', 22)
SlowMAType = _input('SlowMAType', MODE_SMA)
SlowMAPrice = _input('SlowMAPrice', PRICE_CLOSE)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
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
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Iin_MA_Signal_Candle(' + _str(FastMAPeriod) + ',' + _str(SlowMAPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def GetRange(index, High, Low, Len):
    AvgRange = 0.0
    for count in range(_int(index + Len - 1), index - 1, -1):
        AvgRange += MathAbs(High[count] - Low[count])
    return _fdiv(AvgRange, Len)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend_prev
    if (BarsCalculated(FsMA_Handle) < rates_total or BarsCalculated(SlMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    trend = 0
    FsMA = Arr(0, 0.0)
    SlMA = Arr(0, 0.0)
    fasterMAnow = 0.0
    slowerMAnow = 0.0
    fasterMAprevious = 0.0
    slowerMAprevious = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend_prev = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    ArraySetAsSeries(FsMA, True)
    ArraySetAsSeries(SlMA, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if CopyBuffer(FsMA_Handle, 0, 0, to_copy, FsMA) <= 0:
        return 0
    if CopyBuffer(SlMA_Handle, 0, 0, to_copy, SlMA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtOpenBuffer[bar] = open[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        ExtCloseBuffer[bar] = close[bar]
        ExtColorsBuffer[bar] = 3.0
        trend = _s_OnCalculate_trend_prev
        fasterMAnow = FsMA[bar]
        fasterMAprevious = FsMA[bar + 1]
        slowerMAnow = SlMA[bar]
        slowerMAprevious = SlMA[bar + 1]
        if (trend <= 0 and fasterMAnow > slowerMAnow) and fasterMAprevious < slowerMAprevious:
            trend = 1
        if (trend >= 0 and fasterMAnow < slowerMAnow) and fasterMAprevious > slowerMAprevious:
            trend = -1
        if trend > 0:
            if open[bar] <= close[bar]:
                ExtColorsBuffer[bar] = 0.0
            else:
                ExtColorsBuffer[bar] = 1.0
        if trend < 0:
            if open[bar] >= close[bar]:
                ExtColorsBuffer[bar] = 3.0
            else:
                ExtColorsBuffer[bar] = 2.0
        if bar:
            _s_OnCalculate_trend_prev = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IinMASignalCandle(_MQL5Indicator):
    name = 'Iin_MA_Signal_Candle'
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

