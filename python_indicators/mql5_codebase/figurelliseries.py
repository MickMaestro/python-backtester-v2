"""figurelliseries — converted from MQL5: MQL5 Indicators/FigurelliSeries/figurelliseries.mq5

Copyright: Copyright © 2010, Rogerio Figurelli; Link: http://www.quantafinance.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Rogerio Figurelli', 'link': 'http://www.quantafinance.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [13382297]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'FigurelliSeries'}, 'levels': [0.0], 'description': [], 'name': 'figurelliseries', 'source': 'MQL5 Indicators/FigurelliSeries/figurelliseries.mq5', 'folder': 'FigurelliSeries', 'inputs': [{'mql': 'StartPeriod', 'py': 'StartPeriod', 'param': 'StartPeriod', 'type': 'uint', 'default': 6, 'label': 'initial period', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 6, 'label': 'periods calculation step', 'sinput': False}, {'mql': 'Total', 'py': 'Total', 'param': 'Total', 'type': 'uint', 'default': 36, 'label': 'number of Moving Averages', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': 'Moving Averages smoothing type', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'price timeseries of Moving Averages', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StartPeriod = _input('StartPeriod', 6)  # initial period
Step = _input('Step', 6)  # periods calculation step
Total = _input('Total', 36)  # number of Moving Averages
MAType = _input('MAType', MODE_EMA)  # Moving Averages smoothing type
MAPrice = _input('MAPrice', PRICE_CLOSE)  # price timeseries of Moving Averages
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
MA_Handle = Arr(0, 0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(StartPeriod + (Step * (Total - 1)))
    if ArrayResize(MA_Handle, Total) < _int(Total):
        Print('Failed to distribute the memory for MA_Handle[] array')
    for count in range(0, _int(Total)):
        MA_Handle[count] = iMA(None, 0, StartPeriod + (Step * count), 0, MAType, MAPrice)
        if MA_Handle[count] == INVALID_HANDLE:
            Print(' Failed to get the iMA indicator handle')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FigurelliSeries')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    for count in range(0, _int(Total)):
        if BarsCalculated(MA_Handle[count]) < rates_total:
            return 0
    limit = 0
    bar = 0
    MA = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        tot_Ask = 0.0
        tot_Bid = 0.0
        for count in range(0, _int(Total)):
            if CopyBuffer(MA_Handle[count], 0, bar, 1, MA) <= 0:
                return 0
            if close[bar] < MA[0]:
                tot_Ask += 1
            if close[bar] > MA[0]:
                tot_Bid += 1
        IndBuffer[bar] = tot_Bid - tot_Ask
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Figurelliseries(_MQL5Indicator):
    name = 'figurelliseries'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartPeriod': 6,  # initial period
        'Step': 6,  # periods calculation step
        'Total': 36,  # number of Moving Averages
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Moving Averages smoothing type
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # price timeseries of Moving Averages
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

