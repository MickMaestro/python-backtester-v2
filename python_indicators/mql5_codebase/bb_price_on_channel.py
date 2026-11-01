"""bb_price_on_channel — converted from MQL5: MQL5 Indicators/Price on Bollinger Channel/bb_price_on_channel.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 1, 2: 14, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Bollinger High', 2: 'Open;High;Low;Close', 3: 'Bollinger Low'}, 'levels': [50.0, -50.0], 'description': [], 'name': 'bb_price_on_channel', 'source': 'MQL5 Indicators/Price on Bollinger Channel/bb_price_on_channel.mq5', 'folder': 'Price on Bollinger Channel', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'deviation', 'py': 'deviation', 'param': 'deviation', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'price', 'py': 'price', 'param': 'price', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 15)
deviation = _input('deviation', 2.0)
price = _input('price', PRICE_WEIGHTED)
MABuffer = Arr(0, 0.0)
MABuffer2 = Arr(0, 0.0)
BolingerBuffer = Arr(0, 0.0)
BolingerBuffer_l = Arr(0, 0.0)
BarsBuffer1 = Arr(0, 0.0)
BarsBuffer2 = Arr(0, 0.0)
BarsBuffer3 = Arr(0, 0.0)
BarsBuffer4 = Arr(0, 0.0)
ma_handle = 0
symbol = ""
indx1 = 100000

def OnInit():
    global ma_handle, symbol
    SetIndexBuffer(0, BolingerBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BarsBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, BarsBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, BarsBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, BarsBuffer4, INDICATOR_DATA)
    SetIndexBuffer(5, BolingerBuffer_l, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    SetIndexBuffer(6, MABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, MABuffer2, INDICATOR_CALCULATIONS)
    symbol = Symbol()
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bolkinger View (' + symbol + '):  ')
    ma_handle = iBands(Symbol(), 0, period, 0, deviation, price)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ma_handle) < rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        to_copy += 1
    CopyBuffer(ma_handle, 0, 0, to_copy, MABuffer)
    CopyBuffer(ma_handle, 1, 0, to_copy, MABuffer2)
    for i in range(0, rates_total):
        BolingerBuffer[i] = (MABuffer2[i] - MABuffer[i]) * indx1
        BolingerBuffer_l[i] = -BolingerBuffer[i]
        BarsBuffer1[i] = (open[i] - MABuffer[i]) * indx1
        BarsBuffer2[i] = (high[i] - MABuffer[i]) * indx1
        BarsBuffer3[i] = (low[i] - MABuffer[i]) * indx1
        BarsBuffer4[i] = (close[i] - MABuffer[i]) * indx1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BbPriceOnChannel(_MQL5Indicator):
    name = 'bb_price_on_channel'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 15,
        'deviation': 2.0,
        'price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),
    }

