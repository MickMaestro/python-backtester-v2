"""trend — converted from MQL5: MQL5 Indicators/Trend/trend.mq5

Copyright: Copyright © 2008, Ramdass; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Ramdass', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [65280, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Trend'}, 'levels': [], 'description': [], 'name': 'trend', 'source': 'MQL5 Indicators/Trend/trend.mq5', 'folder': 'Trend', 'inputs': [{'mql': 'Bands_Mode', 'py': 'Bands_Mode', 'param': 'Bands_Mode', 'type': 'int', 'default': 0, 'label': 'BB line for the calculation', 'sinput': False}, {'mql': 'bands_period', 'py': 'bands_period', 'param': 'bands_period', 'type': 'int', 'default': 20, 'label': 'BB averaging period', 'sinput': False}, {'mql': 'bands_deviation', 'py': 'bands_deviation', 'param': 'bands_deviation', 'type': 'double', 'default': 2.0, 'label': 'BB deviation', 'sinput': False}, {'mql': 'bands_price', 'py': 'bands_price', 'param': 'bands_price', 'type': 'int', 'default': 1, 'label': 'BB price', 'sinput': False}, {'mql': 'power_period', 'py': 'power_period', 'param': 'power_period', 'type': 'int', 'default': 13, 'label': 'period of averaging', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MODE
MODE_MAIN = 0
MODE_HIGH = 1
MODE_LOW = 2
_enum('MODE', {0: 'MODE_MAIN', 1: 'MODE_HIGH', 2: 'MODE_LOW'})

# ---- inputs and global variables
Bands_Mode = _input('Bands_Mode', MODE_MAIN)  # BB line for the calculation
bands_period = _input('bands_period', 20)  # BB averaging period
bands_deviation = _input('bands_deviation', 2.0)  # BB deviation
bands_price = _input('bands_price', PRICE_CLOSE)  # BB price
power_period = _input('power_period', 13)  # period of averaging
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
min_rates_total = 0
Bands_Handle = 0
Bulls_Handle = 0
Bears_Handle = 0

def OnInit():
    global Bands_Handle, Bears_Handle, Bulls_Handle, min_rates_total
    min_rates_total = MathMax(bands_period, power_period)
    Bands_Handle = iBands(None, 0, bands_period, 0, bands_deviation, bands_price)
    if Bands_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of Bands indicator')
    Bulls_Handle = iBullsPower(None, 0, power_period)
    if Bulls_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the BullsPower indicator')
    Bears_Handle = iBearsPower(None, 0, power_period)
    if Bears_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the BearsPower indicator')
    SetIndexBuffer(0, BullsBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BullsBuffer, True)
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BearsBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = 'Trend'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, begin, price):
    if ((BarsCalculated(Bands_Handle) < rates_total or BarsCalculated(Bulls_Handle) < rates_total) or BarsCalculated(Bears_Handle) < rates_total) or rates_total < (min_rates_total + begin):
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Bands = Arr(0, 0.0)
    Bulls = Arr(0, 0.0)
    Bears = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total - begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Bands_Handle, Bands_Mode, 0, to_copy, Bands) <= 0:
        return 0
    if CopyBuffer(Bulls_Handle, Bands_Mode, 0, to_copy, Bulls) <= 0:
        return 0
    if CopyBuffer(Bears_Handle, Bands_Mode, 0, to_copy, Bears) <= 0:
        return 0
    ArraySetAsSeries(Bands, True)
    ArraySetAsSeries(Bulls, True)
    ArraySetAsSeries(Bears, True)
    ArraySetAsSeries(price, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BullsBuffer[bar] = price[bar] - Bands[bar]
        BearsBuffer[bar] = -(Bears[bar] + Bulls[bar])
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trend(_MQL5Indicator):
    name = 'trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Bands_Mode': _Choice({0: 'main line', 1: 'high line', 2: 'low line'}, default=0),  # BB line for the calculation
        'bands_period': 20,  # BB averaging period
        'bands_deviation': 2.0,  # BB deviation
        'bands_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # BB price
        'power_period': 13,  # period of averaging
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

