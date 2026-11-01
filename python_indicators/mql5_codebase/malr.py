"""malr — converted from MQL5: MQL5 Indicators/MALR/malr.mq5

Copyright: BECEMAL; Link: http://www.becemal.ru/; Version: 1.44

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'BECEMAL', 'link': 'http://www.becemal.ru/', 'version': '1.44', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [55295], 2: [65280], 3: [255], 4: [2263842], 5: [3937500]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'MALR', 2: 'MALRH', 3: 'MALRL', 4: 'MALRHH', 5: 'MALRLL'}, 'levels': [], 'description': [], 'name': 'malr', 'source': 'MQL5 Indicators/MALR/malr.mq5', 'folder': 'MALR', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 120, 'label': 'MA Period', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 0, 'label': 'MA Shift', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied Price', 'sinput': False}, {'mql': 'ChannelReversal', 'py': 'ChannelReversal', 'param': 'ChannelReversal', 'type': 'double', 'default': 0.7071067811865476, 'label': 'Channel Reversal', 'sinput': False}, {'mql': 'ChannelBreakout', 'py': 'ChannelBreakout', 'param': 'ChannelBreakout', 'type': 'double', 'default': 0.7071067811865476, 'label': 'Channel Breakout // 1.4142135623730950488016887242097;', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 120)  # MA Period
MAShift = _input('MAShift', 0)  # MA Shift
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # Applied Price
ChannelReversal = _input('ChannelReversal', 0.7071067811865476)  # Channel Reversal
ChannelBreakout = _input('ChannelBreakout', 0.7071067811865476)  # Channel Breakout // 1.4142135623730950488016887242097;
FF = Arr(0, 0.0)
FFL = Arr(0, 0.0)
FFH = Arr(0, 0.0)
FFLL = Arr(0, 0.0)
FFHH = Arr(0, 0.0)
hSMA = INVALID_HANDLE
hLwMA = INVALID_HANDLE

def OnInit():
    global hLwMA, hSMA
    SetIndexBuffer(0, FF, INDICATOR_DATA)
    SetIndexBuffer(1, FFH, INDICATOR_DATA)
    SetIndexBuffer(2, FFL, INDICATOR_DATA)
    SetIndexBuffer(3, FFHH, INDICATOR_DATA)
    SetIndexBuffer(4, FFLL, INDICATOR_DATA)
    ResetLastError()
    if ((((not ArraySetAsSeries(FF, False)) or (not ArraySetAsSeries(FFL, False))) or (not ArraySetAsSeries(FFH, False))) or (not ArraySetAsSeries(FFLL, False))) or (not ArraySetAsSeries(FFHH, False)):
        Print('ArraySetAsSeries for Main Calcutions, Error ', GetLastError())
        return -1
    hSMA = iMA(Symbol(), Period(), MAPeriod, MAShift, MODE_SMA, AppliedPrice)
    if hSMA == INVALID_HANDLE:
        Print('No SMA! Error # ', GetLastError())
        return -1
    hLwMA = iMA(Symbol(), Period(), MAPeriod, MAShift, MODE_LWMA, AppliedPrice)
    if hLwMA == INVALID_HANDLE:
        Print('No LWMA! Error # ', GetLastError())
        return -1
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = begin + MAPeriod + 1
    else:
        limit = prev_calculated - 1
    if limit <= 0 or limit >= rates_total:
        Print('No Data!')
        return -1
    i = limit
    for i in range(i, rates_total):
        if False:
            return 0
        MA = Arr.of([0.0], fill=0.0, dyn=False, size=1)
        if CopyBuffer(hSMA, 0, rates_total - i, 1, MA) < 1:
            return i - 1
        tSMA = MA[0]
        if tSMA == 0.0:
            return i - 1
        MA[0] = 0.0
        if CopyBuffer(hLwMA, 0, rates_total - i, 1, MA) < 1:
            return i - 1
        tLWMA = MA[0]
        if tLWMA == 0.0:
            return i - 1
        FF[i] = (3.0 * tLWMA) - (2.0 * tSMA)
    else:
        i = _range_end(i, rates_total, 1)
    i = limit
    for i in range(i, rates_total):
        if False:
            return 0
        StdDev = 0.0
        tMA = FF[i]
        for j in range(0, MAPeriod):
            t = price[i - j] - FF[i - j]
            StdDev += t * t
        StdDev = MathSqrt(StdDev / MAPeriod)
        tS = StdDev * ChannelReversal
        tS2 = StdDev * (ChannelReversal + ChannelBreakout)
        FFL[i] = tMA - tS
        FFH[i] = tMA + tS
        FFLL[i] = tMA - tS2
        FFHH[i] = tMA + tS2
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Malr(_MQL5Indicator):
    name = 'malr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 120,  # MA Period
        'MAShift': 0,  # MA Shift
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied Price
        'ChannelReversal': 0.7071067811865476,  # Channel Reversal
        'ChannelBreakout': 0.7071067811865476,  # Channel Breakout // 1.4142135623730950488016887242097;
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

