"""ConsecutiveRSI — converted from MQL5: MQL5 Indicators/ConsecutiveRSI/ConsecutiveRSI.mq5

Detect bullish and bearish consecutive candles when entering overbought or oversold territory
Copyright: Jay Davis; Link: https://tidyneat.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Jay Davis', 'link': 'https://tidyneat.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 5, 'indicator_maximum': 100.0, 'indicator_minimum': 0.0}, 'types': {1: 1, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [16748574], 2: [42495], 3: [42495], 4: [15570276], 5: [15570276]}, 'widths': {1: 1, 2: 3, 3: 3, 4: 3, 5: 3}, 'styles': {1: 0}, 'labels': {1: 'iRSI', 2: 'Bullish_OverSold', 3: 'Bearish OverSold', 4: 'Bullish_OverBought', 5: 'Bearish_OverBought'}, 'levels': [70.0, 30.0], 'description': ['Detect bullish and bearish consecutive candles when entering overbought or oversold territory'], 'name': 'ConsecutiveRSI', 'source': 'MQL5 Indicators/ConsecutiveRSI/ConsecutiveRSI.mq5', 'folder': 'ConsecutiveRSI', 'inputs': [{'mql': 'consecutive', 'py': 'consecutive', 'param': 'consecutive', 'type': 'int', 'default': 3, 'label': 'No. of Consecutive candles', 'sinput': False}, {'mql': 'RSI_parameters', 'py': 'RSI_parameters', 'param': None, 'type': 'string', 'default': '===================================', 'label': '', 'sinput': False}, {'mql': 'ma_period', 'py': 'ma_period', 'param': 'ma_period', 'type': 'int', 'default': 14, 'label': 'period of averaging', 'sinput': False}, {'mql': 'overBought', 'py': 'overBought', 'param': 'overBought', 'type': 'int', 'default': 70, 'label': '', 'sinput': False}, {'mql': 'overSold', 'py': 'overSold', 'param': 'overSold', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 0, 'label': 'timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
consecutive = _input('consecutive', 3)  # No. of Consecutive candles
RSI_parameters = _input('RSI_parameters', '===================================')
ma_period = _input('ma_period', 14)  # period of averaging
overBought = _input('overBought', 70)
overSold = _input('overSold', 30)
applied_price = _input('applied_price', PRICE_CLOSE)  # type of price
period = _input('period', PERIOD_CURRENT)  # timeframe
iRSIBuffer = Arr(0, 0.0)
bulloversold = Arr(0, 0.0)
bearoversold = Arr(0, 0.0)
bulloverbought = Arr(0, 0.0)
bearoverbought = Arr(0, 0.0)
handle = 0
short_name = ""
bars_calculated = 0

def OnInit():
    global handle, short_name
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overBought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, overSold)
    display = 'OverBought ' + _str(overBought)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, display)
    display = 'OverSold ' + _str(overSold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, display)
    SetIndexBuffer(0, iRSIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, bulloversold, INDICATOR_DATA)
    SetIndexBuffer(2, bearoversold, INDICATOR_DATA)
    SetIndexBuffer(3, bulloverbought, INDICATOR_DATA)
    SetIndexBuffer(4, bearoverbought, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 246)
    PlotIndexSetInteger(2, PLOT_ARROW, 248)
    PlotIndexSetInteger(3, PLOT_ARROW, 246)
    PlotIndexSetInteger(4, PLOT_ARROW, 248)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    handle = iRSI(name, period, ma_period, applied_price)
    if handle == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iRSI indicator for the symbol %s/%s, error code %d', name, EnumToString(period, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    short_name = StringFormat('iRSI(%s/%s, %d, %d)', name, EnumToString(period, 'ENUM_TIMEFRAMES'), ma_period, applied_price)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated = BarsCalculated(handle)
    if calculated <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(iRSIBuffer, handle, values_to_copy):
        return 0
    comm = StringFormat('%s ==>  Updated value in the indicator %s: %d', TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS), short_name, values_to_copy)
    Comment(comm)
    bars_calculated = calculated
    ArraySetAsSeries(open, False)
    ArraySetAsSeries(close, False)
    startValue = prev_calculated
    if startValue == 0:
        startValue = consecutive
    for i in range(rates_total, startValue, -1):
        if i <= (rates_total - consecutive):
            if iRSIBuffer[i] > overBought and iRSIBuffer[i - 1] < overBought:
                if ConsecutiveBulls(i, open, close):
                    bulloverbought[i] = iRSIBuffer[i]
                elif ConsecutiveBears(i, open, close):
                    bearoverbought[i] = iRSIBuffer[i]
            elif iRSIBuffer[i] < overSold and iRSIBuffer[i - 1] > overSold:
                if ConsecutiveBulls(i, open, close):
                    bulloversold[i] = iRSIBuffer[i]
                elif ConsecutiveBears(i, open, close):
                    bearoversold[i] = iRSIBuffer[i]
    return rates_total

def FillArrayFromBuffer(rsi_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, rsi_buffer) < 0:
        PrintFormat('Failed to copy data from the iRSI indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    Comment('')

def ConsecutiveBulls(bar, open, close):
    for i in range(0, consecutive):
        if open[bar - i] > close[bar - i]:
            return False
    return True

def ConsecutiveBears(bar, open, close):
    for i in range(0, consecutive):
        if open[bar - i] < close[bar - i]:
            return False
    return True

# ---- global variables initialised from expressions
name = Symbol()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ConsecutiveRSI(_MQL5Indicator):
    name = 'ConsecutiveRSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'consecutive': 3,  # No. of Consecutive candles
        'ma_period': 14,  # period of averaging
        'overBought': 70,
        'overSold': 30,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
        'period': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # timeframe
    }
    y_range = (0.0, 100.0)

