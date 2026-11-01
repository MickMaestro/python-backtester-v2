"""MA-Candlesticks — converted from MQL5: MQL5 Indicators/Moving Average Candlesticks MT5/MA-Candlesticks.mq5

Displays the moving average in form of the candlesticks.
This way, the moving average is shown for Close, Open, High and Low.
Works with any trading instrument, timeframe, period, and MA type.
Link: https://t.me/ForexEaPremium; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'https://t.me/ForexEaPremium', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711680, 65535]}, 'widths': {}, 'styles': {}, 'labels': {1: 'MA Open;MA High;MA Low;MA Close'}, 'levels': [], 'description': ['Displays the moving average in form of the candlesticks.', 'This way, the moving average is shown for Close, Open, High and Low.', 'Works with any trading instrument, timeframe, period, and MA type.'], 'name': 'MA-Candlesticks', 'source': 'MQL5 Indicators/Moving Average Candlesticks MT5/MA-Candlesticks.mq5', 'folder': 'Moving Average Candlesticks MT5', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 10, 'label': 'MA Period', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 0, 'label': 'MA Type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtOBuffer = Arr(0, 0.0)
ExtHBuffer = Arr(0, 0.0)
ExtLBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
MACloseBuf = Arr(0, 0.0)
MAOpenBuf = Arr(0, 0.0)
MAHighBuf = Arr(0, 0.0)
MALowBuf = Arr(0, 0.0)
MAPeriod = _input('MAPeriod', 10)  # MA Period
MAType = _input('MAType', MODE_SMA)  # MA Type

def OnInit():
    SetIndexBuffer(0, ExtOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA-Candlesticks(' + IntegerToString(MAPeriod) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MAPeriod)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    myMA = 0
    myMA = iMA(None, 0, MAPeriod, 0, MAType, PRICE_CLOSE)
    if CopyBuffer(myMA, 0, 0, rates_total, MACloseBuf) != rates_total:
        return 0
    myMA = iMA(None, 0, MAPeriod, 0, MAType, PRICE_OPEN)
    if CopyBuffer(myMA, 0, 0, rates_total, MAOpenBuf) != rates_total:
        return 0
    myMA = iMA(None, 0, MAPeriod, 0, MAType, PRICE_HIGH)
    if CopyBuffer(myMA, 0, 0, rates_total, MAHighBuf) != rates_total:
        return 0
    myMA = iMA(None, 0, MAPeriod, 0, MAType, PRICE_LOW)
    if CopyBuffer(myMA, 0, 0, rates_total, MALowBuf) != rates_total:
        return 0
    limit = 0
    if prev_calculated <= 1:
        ExtLBuffer[0] = MALowBuf[0]
        ExtHBuffer[0] = MAHighBuf[0]
        ExtOBuffer[0] = MAOpenBuf[0]
        ExtCBuffer[0] = MACloseBuf[0]
        limit = 1
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        ExtOBuffer[i] = MAOpenBuf[i]
        ExtCBuffer[i] = MACloseBuf[i]
        if MAOpenBuf[i] < MACloseBuf[i]:
            ExtLBuffer[i] = MALowBuf[i]
            ExtHBuffer[i] = MAHighBuf[i]
            ExtColorBuffer[i] = 0.0
        else:
            ExtLBuffer[i] = MAHighBuf[i]
            ExtHBuffer[i] = MALowBuf[i]
            ExtColorBuffer[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACandlesticks(_MQL5Indicator):
    name = 'MA-Candlesticks'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 10,  # MA Period
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Type
    }

