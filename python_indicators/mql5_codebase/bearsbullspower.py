"""BearsBullsPower — converted from MQL5: MQL5 Indicators/BearsBullsPower/BearsBullsPower.mq5

Copyright: Copyright 2019, MetaQuotes Software Corp.; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2019, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 3, 2: 3, 3: 3}, 'colors': {}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'BullsPower', 2: 'BearsPower'}, 'levels': [], 'description': [], 'name': 'BearsBullsPower', 'source': 'MQL5 Indicators/BearsBullsPower/BearsBullsPower.mq5', 'folder': 'BearsBullsPower', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 13, 'label': 'Power Period', 'sinput': False}, {'mql': 'BullsColor', 'py': 'BullsColor', 'param': None, 'type': 'color', 'default': 16776960, 'label': 'Bulls Color', 'sinput': False}, {'mql': 'BearsColor', 'py': 'BearsColor', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Beasr Color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 13)  # Power Period
BullsColor = _input('BullsColor', clrAqua)  # Bulls Color
BearsColor = _input('BearsColor', clrYellow)  # Beasr Color
ExtBullsBuffer = Arr(0, 0.0)
ExtBearsBuffer = Arr(0, 0.0)
ExtBullBuffer1 = Arr(0, 0.0)
ExtTempBuffer = Arr(0, 0.0)
ExtEmaHandle = 0

def OnInit():
    global ExtEmaHandle
    SetIndexBuffer(0, ExtBullsBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBearsBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtBullBuffer1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtTempBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpPeriod - 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpPeriod - 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpPeriod - 1)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, BullsColor)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, BearsColor)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, BullsColor)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BBPower(' + _str(InpPeriod) + ')')
    ExtEmaHandle = iMA(None, 0, InpPeriod, 0, MODE_EMA, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    limit = 0
    if rates_total < InpPeriod:
        return 0
    calculated = BarsCalculated(ExtEmaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtEmaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtEmaHandle, 0, 0, to_copy, ExtTempBuffer) <= 0:
        Print('getting ExtEmaHandle is failed! Error', GetLastError())
        return 0
    if prev_calculated < InpPeriod:
        limit = InpPeriod
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtBullsBuffer[i] = high[i] - ExtTempBuffer[i]
        ExtBearsBuffer[i] = low[i] - ExtTempBuffer[i]
        if ExtBullsBuffer[i] < 0.0:
            ExtBullBuffer1[i] = ExtBullsBuffer[i]
        else:
            ExtBullBuffer1[i] = EMPTY_VALUE
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BearsBullsPower(_MQL5Indicator):
    name = 'BearsBullsPower'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 13,  # Power Period
    }

