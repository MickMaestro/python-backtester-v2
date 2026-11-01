"""ma_distance_from_price — converted from MQL5: MQL5 Indicators/Ma_Distance_From_Price/ma_distance_from_price.mq5

Ma_Distance_From_Price
Copyright: Copyright © 2013, David W Honeywell; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, David W Honeywell', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [42495], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Ma_Distance_From_Price Sell', 2: 'Ma_Distance_From_Price Buy'}, 'levels': [], 'description': ['Ma_Distance_From_Price'], 'name': 'ma_distance_from_price', 'source': 'MQL5 Indicators/Ma_Distance_From_Price/ma_distance_from_price.mq5', 'folder': 'Ma_Distance_From_Price', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'PipLevel', 'py': 'PipLevel', 'param': 'PipLevel', 'type': 'int', 'default': 15, 'label': 'trigger level from moving in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 13)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
PipLevel = _input('PipLevel', 15)  # trigger level from moving in points
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
dPipLevel = 0.0
min_rates_total = 0
ATRPeriod = 0
MA_Handle = 0

def OnInit():
    global ATRPeriod, MA_Handle, dPipLevel, min_rates_total
    ATRPeriod = 10
    min_rates_total = _int(MathMax(ATRPeriod, MAPeriod + 1))
    dPipLevel = PipLevel * Point()
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Ma_Distance_From_Price'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def CountRange(High, Low, period, index):
    AvgRange = 0.0
    for count in range(index + period - 1, index - 1, -1):
        AvgRange += MathAbs(High[count] - Low[count])
    Range = _fdiv(AvgRange, period)
    Range *= 0.5
    return Range

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(MA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Range = 0.0
    MA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    to_copy = limit + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        if MA[bar] > (high[bar] + dPipLevel):
            Range = CountRange(high, low, ATRPeriod, bar)
            SellBuffer[bar] = high[bar] + Range
        if MA[bar] < (low[bar] - dPipLevel):
            Range = CountRange(high, low, ATRPeriod, bar)
            BuyBuffer[bar] = low[bar] - Range
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaDistanceFromPrice(_MQL5Indicator):
    name = 'ma_distance_from_price'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 13,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'PipLevel': 15,  # trigger level from moving in points
    }

