"""barsmaxminsystem — converted from MQL5: MQL5 Indicators/BarsMaxMinSystem/barsmaxminsystem.mq5

Indicator for three-bars system of maximums/minimums by Larry Williams
Copyright: Copyright 2012, Rone; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 12, 'indicator_plots': 4}, 'types': {1: 17, 2: 8, 3: 1, 4: 1}, 'colors': {1: [32768, 3937500], 2: [16711680, 42495], 3: [16748574], 4: [4678655]}, 'widths': {1: 2, 2: 3, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Candle Open;Candle High;Candle Low;Candle Close', 2: 'Up Trend MA;Down Trend MA', 3: 'High MA', 4: 'Low MA'}, 'levels': [], 'description': ['Indicator for three-bars system of maximums/minimums by Larry Williams'], 'name': 'barsmaxminsystem', 'source': 'MQL5 Indicators/BarsMaxMinSystem/barsmaxminsystem.mq5', 'folder': 'BarsMaxMinSystem', 'inputs': [{'mql': 'InpMaMethod', 'py': 'InpMaMethod', 'param': 'InpMaMethod', 'type': 'int', 'default': 0, 'label': 'MA method (for all)', 'sinput': False}, {'mql': 'InpTrendMaPeriod', 'py': 'InpTrendMaPeriod', 'param': 'InpTrendMaPeriod', 'type': 'int', 'default': 10, 'label': 'Trend МА period', 'sinput': False}, {'mql': 'InpHighMaPeriod', 'py': 'InpHighMaPeriod', 'param': 'InpHighMaPeriod', 'type': 'int', 'default': 3, 'label': 'High МА period', 'sinput': False}, {'mql': 'InpLowMaPeriod', 'py': 'InpLowMaPeriod', 'param': 'InpLowMaPeriod', 'type': 'int', 'default': 3, 'label': 'Low МА period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMaMethod = _input('InpMaMethod', MODE_SMA)  # MA method (for all)
InpTrendMaPeriod = _input('InpTrendMaPeriod', 10)  # Trend МА period
InpHighMaPeriod = _input('InpHighMaPeriod', 3)  # High МА period
InpLowMaPeriod = _input('InpLowMaPeriod', 3)  # Low МА period
CandleOpenBuffer = Arr(0, 0.0)
CandleHighBuffer = Arr(0, 0.0)
CandleLowBuffer = Arr(0, 0.0)
CandleCloseBuffer = Arr(0, 0.0)
CandleColors = Arr(0, 0.0)
TrendMaBuffer = Arr(0, 0.0)
TrendMaColors = Arr(0, 0.0)
HighMaBuffer = Arr(0, 0.0)
LowMaBuffer = Arr(0, 0.0)
MaBuffer = Arr(0, 0.0)
HMaBuffer = Arr(0, 0.0)
LMaBuffer = Arr(0, 0.0)
minRequiredBars = 0
maHandle = 0
highMaHandle = 0
lowMaHandle = 0

def OnInit():
    global highMaHandle, lowMaHandle, maHandle, minRequiredBars
    minRequiredBars = MathMax(InpTrendMaPeriod, MathMax(InpHighMaPeriod, InpLowMaPeriod))
    SetIndexBuffer(0, CandleOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, CandleHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, CandleLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, CandleCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, CandleColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, TrendMaBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, TrendMaColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, HighMaBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, LowMaBuffer, INDICATOR_DATA)
    SetIndexBuffer(9, MaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, HMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, LMaBuffer, INDICATOR_CALCULATIONS)
    for i in range(0, 9):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'BarsMaxMinSystem (' + _str(InpTrendMaPeriod) + ', ' + _str(InpHighMaPeriod) + ', ' + _str(InpLowMaPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    maHandle = iMA(Symbol(), Period(), InpTrendMaPeriod, 0, InpMaMethod, PRICE_CLOSE)
    highMaHandle = iMA(Symbol(), Period(), InpHighMaPeriod, 0, InpMaMethod, PRICE_HIGH)
    lowMaHandle = iMA(Symbol(), Period(), InpLowMaPeriod, 0, InpMaMethod, PRICE_LOW)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    startBar = 0
    if rates_total < minRequiredBars:
        Print('Not enough bars for the calculation.')
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        if (CopyBuffer(maHandle, 0, 0, rates_total, MaBuffer) <= 0 or CopyBuffer(highMaHandle, 0, 0, rates_total, HMaBuffer) <= 0) or CopyBuffer(lowMaHandle, 0, 0, rates_total, LMaBuffer) <= 0:
            Print('Indicator data copy error.')
            return 0
        startBar = minRequiredBars
    else:
        toCopy = rates_total - prev_calculated
        if toCopy == 0:
            toCopy = 1
        if (CopyBuffer(maHandle, 0, 0, toCopy, MaBuffer) < toCopy or CopyBuffer(highMaHandle, 0, 0, toCopy, HMaBuffer) < toCopy) or CopyBuffer(lowMaHandle, 0, 0, toCopy, LMaBuffer) < toCopy:
            Print('Indicator data copy error.')
            return 0
        startBar = prev_calculated - 1
    for bar in range(startBar, rates_total):
        maValue = MaBuffer[bar]
        HighMaBuffer[bar] = HMaBuffer[bar] - maValue
        LowMaBuffer[bar] = LMaBuffer[bar] - maValue
        CandleOpenBuffer[bar] = open[bar] - maValue
        CandleHighBuffer[bar] = high[bar] - maValue
        CandleLowBuffer[bar] = low[bar] - maValue
        CandleCloseBuffer[bar] = close[bar] - maValue
        CandleColors[bar] = 0.0
        if CandleCloseBuffer[bar] < CandleOpenBuffer[bar]:
            CandleColors[bar] = 1.0
        TrendMaBuffer[bar] = 0.0
        TrendMaColors[bar] = 0.0
        if MaBuffer[bar] < MaBuffer[bar - 1]:
            TrendMaColors[bar] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Barsmaxminsystem(_MQL5Indicator):
    name = 'barsmaxminsystem'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method (for all)
        'InpTrendMaPeriod': 10,  # Trend МА period
        'InpHighMaPeriod': 3,  # High МА period
        'InpLowMaPeriod': 3,  # Low МА period
    }

