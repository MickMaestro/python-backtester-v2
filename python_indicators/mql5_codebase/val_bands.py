"""val_bands — converted from MQL5: MQL5 Indicators/Val_Bands/val_bands.mq5

Copyright: Copyright © 2010, Fomenko; Link: http://faa1947@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Fomenko', 'link': 'http://faa1947@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 10, 2: 1, 3: 1, 4: 1}, 'colors': {1: [8421504, 255, 65280, 65535], 2: [65280], 3: [65535], 4: [255]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 4, 3: 4, 4: 4}, 'labels': {1: 'Val Histogram', 2: 'Mov', 3: 'Up', 4: 'Down'}, 'levels': [], 'description': [], 'name': 'val_bands', 'source': 'MQL5 Indicators/Val_Bands/val_bands.mq5', 'folder': 'Val_Bands', 'inputs': [{'mql': 'BandsPeriod', 'py': 'BandsPeriod', 'param': 'BandsPeriod', 'type': 'int', 'default': 14, 'label': 'Calculation period', 'sinput': False}, {'mql': 'BandsDeviations', 'py': 'BandsDeviations', 'param': 'BandsDeviations', 'type': 'double', 'default': 1.0, 'label': 'Standard deviation size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BandsPeriod = _input('BandsPeriod', 14)  # Calculation period
BandsDeviations = _input('BandsDeviations', 1.0)  # Standard deviation size
min_rates_total = 0
HMA_Handle = 0
LMA_Handle = 0
UpBuffer = Arr(0, 0.0)
DownBuffer = Arr(0, 0.0)
MaBuffer = Arr(0, 0.0)
ValBuffer = Arr(0, 0.0)
ColorValBuffer = Arr(0, 0.0)

def OnInit():
    global HMA_Handle, LMA_Handle, min_rates_total
    min_rates_total = BandsPeriod
    HMA_Handle = iMA(None, 0, BandsPeriod, 0, MODE_SMA, PRICE_HIGH)
    if HMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    LMA_Handle = iMA(None, 0, BandsPeriod, 0, MODE_SMA, PRICE_LOW)
    if LMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    SetIndexBuffer(0, ValBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ValBuffer, True)
    SetIndexBuffer(1, ColorValBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorValBuffer, True)
    SetIndexBuffer(2, MaBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MaBuffer, True)
    SetIndexBuffer(3, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(4, DownBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DownBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Val_Bands( ', BandsPeriod, ', ', BandsDeviations, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(HMA_Handle) < rates_total or BarsCalculated(LMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    k = 0
    HMA = Arr(0, 0.0)
    LMA = Arr(0, 0.0)
    sum_ = 0.0
    oldval = 0.0
    newres = 0.0
    deviation = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    if CopyBuffer(HMA_Handle, 0, 0, to_copy, HMA) <= 0:
        return 0
    if CopyBuffer(LMA_Handle, 0, 0, to_copy, LMA) <= 0:
        return 0
    ArraySetAsSeries(HMA, True)
    ArraySetAsSeries(LMA, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ValBuffer[bar] = _fdiv(high[bar] - low[bar], Point())
        MaBuffer[bar] = _fdiv(HMA[bar] - LMA[bar], Point())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        sum_ = 0.0
        k = bar + BandsPeriod - 1
        oldval = MaBuffer[bar]
        while k >= bar:
            newres = ValBuffer[k] - oldval
            sum_ += newres * newres
            k -= 1
        deviation = BandsDeviations * MathSqrt(sum_ / BandsPeriod)
        UpBuffer[bar] = oldval + deviation
        DownBuffer[bar] = oldval - deviation
        ColorValBuffer[bar] = 0.0
        if ValBuffer[bar] > UpBuffer[bar]:
            ColorValBuffer[bar] = 3.0
        elif ValBuffer[bar] > MaBuffer[bar]:
            ColorValBuffer[bar] = 2.0
        elif ValBuffer[bar] > DownBuffer[bar]:
            ColorValBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ValBands(_MQL5Indicator):
    name = 'val_bands'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BandsPeriod': 14,  # Calculation period
        'BandsDeviations': 1.0,  # Standard deviation size
    }

