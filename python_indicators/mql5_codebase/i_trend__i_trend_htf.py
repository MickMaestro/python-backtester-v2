"""i_trend — converted from MQL5: MQL5 Indicators/i_Trend_HTF/i_trend.mq5

Copyright: Copyright © 2007, NNN; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, NNN', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [10025880, 11823615]}, 'widths': {}, 'styles': {}, 'labels': {1: 'i_Trend'}, 'levels': [], 'description': [], 'name': 'i_trend', 'source': 'MQL5 Indicators/i_Trend_HTF/i_trend.mq5', 'folder': 'i_Trend_HTF', 'inputs': [{'mql': 'Price_Type', 'py': 'Price_Type', 'param': 'Price_Type', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'deviation', 'py': 'deviation', 'param': 'deviation', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'BBPrice', 'py': 'BBPrice', 'param': 'BBPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'BBMode', 'py': 'BBMode', 'param': 'BBMode', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Mode
Mode_1 = 0
Mode_2 = 1
Mode_3 = 2
_enum('Mode', {0: 'Mode_1', 1: 'Mode_2', 2: 'Mode_3'})

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
Price_Type = _input('Price_Type', PRICE_CLOSE_)
MAPeriod = _input('MAPeriod', 13)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
BBPeriod = _input('BBPeriod', 20)
deviation = _input('deviation', 2.0)
BBPrice = _input('BBPrice', PRICE_CLOSE)
BBMode = _input('BBMode', Mode_1)
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
MA_Handle = 0
BB_Handle = 0

def OnInit():
    global BB_Handle, MA_Handle, min_rates_total
    min_rates_total = _int(MathMax(MAPeriod, BBPeriod))
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    BB_Handle = iBands(None, 0, BBPeriod, 0, deviation, BBPrice)
    if BB_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBB')
        return INIT_FAILED
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'i_Trend')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(MA_Handle) < rates_total or BarsCalculated(BB_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    price = 0.0
    MA = Arr(0, 0.0)
    BB = Arr(0, 0.0)
    limit = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(BB, True)
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    to_copy = limit + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    if CopyBuffer(BB_Handle, BBMode, 0, to_copy, BB) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        price = PriceSeries(Price_Type, bar, open, low, high, close)
        ExtABuffer[bar] = price - BB[bar]
        ExtBBuffer[bar] = -(low[bar] + high[bar] - (2 * MA[bar]))
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ITrend(_MQL5Indicator):
    name = 'i_trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price_Type': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),
        'MAPeriod': 13,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'BBPeriod': 20,
        'deviation': 2.0,
        'BBPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'BBMode': _Choice({0: 'Базовая линия', 1: 'Верхняя линия', 2: 'Нижняя линия'}, default=0),
    }

