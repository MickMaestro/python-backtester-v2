"""tdi2_bars — converted from MQL5: MQL5 Indicators/TDI-2 BARS/tdi2_bars.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [16711935, 2763429, 8421504, 8421376, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TDI2_BARS'}, 'levels': [], 'description': [], 'name': 'tdi2_bars', 'source': 'MQL5 Indicators/TDI-2 BARS/tdi2_bars.mq5', 'folder': 'TDI-2 BARS', 'inputs': [{'mql': 'TdiMethod', 'py': 'TdiMethod', 'param': 'TdiMethod', 'type': 'int', 'default': 0, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'TdiPeriod', 'py': 'TdiPeriod', 'param': 'TdiPeriod', 'type': 'int', 'default': 20, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'TdiPhase', 'py': 'TdiPhase', 'param': 'TdiPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
TdiMethod = _input('TdiMethod', MODE_SMA)  # Method of averaging
TdiPeriod = _input('TdiPeriod', 20)  # Smoothing depth
TdiPhase = _input('TdiPhase', 15)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
TDI2_Handle = 0

def OnInit():
    global TDI2_Handle, min_rates_total
    min_rates_1 = TdiPeriod
    min_rates_2 = min_rates_1 + GetStartBars(TdiMethod, TdiPeriod, TdiPhase)
    min_rates_total = min_rates_1 + min_rates_2 + (2 * GetStartBars(TdiMethod, TdiPeriod, TdiPhase))
    TDI2_Handle = iCustom(None, 0, 'TDI-2', TdiMethod, TdiPeriod, TdiPhase, IPC, 0)
    if TDI2_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the iTDI-2 indicator')
        return INIT_FAILED
    SetIndexBuffer(0, DnIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(1, UpIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(2, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TDI2_BARS')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(TDI2_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    TDI2P = Arr(0, 0.0)
    TDI2M = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(TDI2P, True)
    ArraySetAsSeries(TDI2M, True)
    if CopyBuffer(TDI2_Handle, 1, 0, to_copy, TDI2P) <= 0:
        return 0
    if CopyBuffer(TDI2_Handle, 0, 0, to_copy, TDI2M) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpIndBuffer[bar] = High[bar]
        DnIndBuffer[bar] = Low[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if TDI2P[bar] > TDI2M[bar]:
            if Open[bar] < Close[bar]:
                clr = 4
            if Open[bar] > Close[bar]:
                clr = 3
        if TDI2P[bar] < TDI2M[bar]:
            if Open[bar] > Close[bar]:
                clr = 0
            if Open[bar] < Close[bar]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tdi2Bars(_MQL5Indicator):
    name = 'tdi2_bars'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TdiMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Method of averaging
        'TdiPeriod': 20,  # Smoothing depth
        'TdiPhase': 15,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Price constant
    }

