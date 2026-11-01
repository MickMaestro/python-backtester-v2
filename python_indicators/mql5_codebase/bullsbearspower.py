"""bullsbearspower — converted from MQL5: MQL5 Indicators/Bulls Bears Power/bullsbearspower.mq5

Bulls Bears Power
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [15570276]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Bulls Bears Power'], 'name': 'bullsbearspower', 'source': 'MQL5 Indicators/Bulls Bears Power/bullsbearspower.mq5', 'folder': 'Bulls Bears Power', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'TypeMA', 'py': 'TypeMA', 'param': 'TypeMA', 'type': 'int', 'default': 1, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'TypePrice', 'py': 'TypePrice', 'param': 'TypePrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 13)  # Period
TypeMA = _input('TypeMA', MODE_EMA)  # Smoothing method
TypePrice = _input('TypePrice', PRICE_CLOSE)  # Applied price
ExtBBBuffer = Arr(0, 0.0)
ExtTempBuffer = Arr(0, 0.0)
ExtEmaHandle = 0

def OnInit():
    global ExtEmaHandle
    SetIndexBuffer(0, ExtBBBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTempBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpPeriod - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bulls Bears Power(' + _str(InpPeriod) + ')')
    ExtEmaHandle = iMA(None, 0, InpPeriod, 0, TypeMA, TypePrice)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if rates_total < InpPeriod:
        return 0
    calculated = BarsCalculated(ExtEmaHandle)
    if calculated < rates_total:
        Print('The last calculated bar is ', calculated, '. Error.', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if CopyBuffer(ExtEmaHandle, 0, 0, to_copy, ExtTempBuffer) <= 0:
        Print('Error in call of CopyBuffer', GetLastError())
        return 0
    if prev_calculated < InpPeriod:
        limit = InpPeriod
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtBBBuffer[i] = High[i] + Low[i] - (2 * ExtTempBuffer[i])
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bullsbearspower(_MQL5Indicator):
    name = 'bullsbearspower'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 13,  # Period
        'TypeMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing method
        'TypePrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

