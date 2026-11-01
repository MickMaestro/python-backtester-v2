"""Keltner_Channel — converted from MQL5: MQL5 Indicators/Keltner Channel MT5/Keltner_Channel.mq5

Displays classical Keltner Channel technical indicator.
You can modify main MA period, mode of the MA and type of prices used in MA.
Buy when candle closes above the upper band.
Sell when candle closes below the lower band.
Use a *very conservative* stop-loss and 3-4 times higher take-profit.
Link: https://t.me/ForexEaPremium; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'https://t.me/ForexEaPremium', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [255]}, 'widths': {}, 'styles': {2: 3}, 'labels': {1: 'KC-Up', 2: 'KC-Mid', 3: 'KC-Low'}, 'levels': [], 'description': ['Displays classical Keltner Channel technical indicator.', 'You can modify main MA period, mode of the MA and type of prices used in MA.', 'Buy when candle closes above the upper band.', 'Sell when candle closes below the lower band.', 'Use a *very conservative* stop-loss and 3-4 times higher take-profit.'], 'name': 'Keltner_Channel', 'source': 'MQL5 Indicators/Keltner Channel MT5/Keltner_Channel.mq5', 'folder': 'Keltner Channel MT5', 'inputs': [{'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Mode_MA', 'py': 'Mode_MA', 'param': 'Mode_MA', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_Type', 'py': 'Price_Type', 'param': 'Price_Type', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Period = _input('MA_Period', 10)
Mode_MA = _input('Mode_MA', MODE_SMA)
Price_Type = _input('Price_Type', PRICE_TYPICAL)
Upper = Arr(0, 0.0)
Middle = Arr(0, 0.0)
Lower = Arr(0, 0.0)
MA_Buffer = 0.0

def OnInit():
    SetIndexBuffer(0, Upper, INDICATOR_DATA)
    SetIndexBuffer(1, Middle, INDICATOR_DATA)
    SetIndexBuffer(2, Lower, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Keltner Channel (' + IntegerToString(MA_Period) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, High, Low, close, tick_volume, volume, spread):
    limit = 0
    avg = 0.0
    counted_bars = prev_calculated
    if counted_bars < 0:
        return -1
    if counted_bars > 0:
        counted_bars -= 1
    limit = counted_bars
    if limit < MA_Period:
        limit = MA_Period
    myMA = iMA(None, 0, MA_Period, 0, Mode_MA, Price_Type)
    if CopyBuffer(myMA, 0, 0, rates_total, Middle) != rates_total:
        return 0
    for i in range(rates_total - 1, limit - 1, -1):
        avg = findAvg(MA_Period, i, High, Low)
        Upper[i] = Middle[i] + avg
        Lower[i] = Middle[i] - avg
    return rates_total

def findAvg(period, shift, High, Low):
    sum_ = 0.0
    for i in range(shift, shift - period, -1):
        sum_ += High[i] - Low[i]
    sum_ = _fdiv(sum_, period)
    return sum_


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KeltnerChannel(_MQL5Indicator):
    name = 'Keltner_Channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Period': 10,
        'Mode_MA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_Type': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),
    }

