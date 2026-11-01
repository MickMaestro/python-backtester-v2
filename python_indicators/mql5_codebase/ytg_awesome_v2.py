"""ytg_awesome_v2 — converted from MQL5: MQL5 Indicators/The 4-color АО indicator/ytg_awesome_v2.mq5

indicator ytg_Awesome_Oscillator
 
site:  http://ytg.com.ua
 
mail:  ytg@ytg.com.ua 
 
Skype:  yuriy.g.t
Copyright: Yuriy Tokman (YTG); Link: http://ytg.com.ua; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Yuriy Tokman (YTG)', 'link': 'http://ytg.com.ua', 'version': '2.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 16776960, 55295]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'ytg_AO'}, 'levels': [], 'description': ['indicator ytg_Awesome_Oscillator', ' ', 'site:  http://ytg.com.ua', ' ', 'mail:  ytg@ytg.com.ua ', ' ', 'Skype:  yuriy.g.t'], 'name': 'ytg_awesome_v2', 'source': 'MQL5 Indicators/The 4-color АО indicator/ytg_awesome_v2.mq5', 'folder': 'The 4-color АО indicator', 'inputs': [{'mql': 'Period_Fast', 'py': 'Period_Fast', 'param': 'Period_Fast', 'type': 'int', 'default': 5, 'label': 'fast MA period', 'sinput': False}, {'mql': 'Period_Slow', 'py': 'Period_Slow', 'param': 'Period_Slow', 'type': 'int', 'default': 34, 'label': 'slow MA period', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'smoothing type', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 5, 'label': 'type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period_Fast = _input('Period_Fast', 5)  # fast MA period
Period_Slow = _input('Period_Slow', 34)  # slow MA period
ma_method = _input('ma_method', MODE_SMA)  # smoothing type
applied_price = _input('applied_price', PRICE_MEDIAN)  # type of price
ExtAOBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
ExtFastBuffer = Arr(0, 0.0)
ExtSlowBuffer = Arr(0, 0.0)
ExtFastSMAHandle = 0
ExtSlowSMAHandle = 0
DATA_LIMIT = Period_Fast

def OnInit():
    global DATA_LIMIT, ExtFastSMAHandle, ExtSlowSMAHandle
    if Period_Slow > Period_Fast:
        DATA_LIMIT = Period_Slow
    SetIndexBuffer(0, ExtAOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtFastBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtSlowBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, DATA_LIMIT)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ytg_AO')
    ExtFastSMAHandle = iMA(None, 0, Period_Fast, 0, MODE_SMA, PRICE_MEDIAN)
    ExtSlowSMAHandle = iMA(None, 0, Period_Slow, 0, MODE_SMA, PRICE_MEDIAN)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= DATA_LIMIT:
        return 0
    calculated = BarsCalculated(ExtFastSMAHandle)
    if calculated < rates_total:
        Print('Not all data of ExtFastSMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtSlowSMAHandle)
    if calculated < rates_total:
        Print('Not all data of ExtSlowSMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
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
    if CopyBuffer(ExtFastSMAHandle, 0, 0, to_copy, ExtFastBuffer) <= 0:
        Print('Getting fast SMA is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtSlowSMAHandle, 0, 0, to_copy, ExtSlowBuffer) <= 0:
        Print('Getting slow SMA is failed! Error', GetLastError())
        return 0
    i = 0
    limit = 0
    if prev_calculated <= DATA_LIMIT:
        i = 0
        for i in range(i, DATA_LIMIT):
            ExtAOBuffer[i] = 0.0
        else:
            i = _range_end(i, DATA_LIMIT, 1)
        limit = DATA_LIMIT
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtAOBuffer[i] = _fdiv(ExtFastBuffer[i] - ExtSlowBuffer[i], Point())
        if ExtAOBuffer[i] > 0:
            if ExtAOBuffer[i] > ExtAOBuffer[i - 1]:
                ExtColorBuffer[i] = 0.0
            else:
                ExtColorBuffer[i] = 1.0
        else:
            if ExtAOBuffer[i] > ExtAOBuffer[i - 1]:
                ExtColorBuffer[i] = 2.0
            else:
                ExtColorBuffer[i] = 3.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YtgAwesomeV2(_MQL5Indicator):
    name = 'ytg_awesome_v2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_Fast': 5,  # fast MA period
        'Period_Slow': 34,  # slow MA period
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # smoothing type
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # type of price
    }

