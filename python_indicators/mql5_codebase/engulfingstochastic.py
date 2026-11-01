"""EngulfingStochastic — converted from MQL5: MQL5 Indicators/Engulfing Stochastic/EngulfingStochastic.mq5

Detect bullish and bearish engulfing candles when entering overbought or oversold territory
Copyright: Jay Davis; Link: https://www.mql5.com/en/blogs/post/724674; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Jay Davis', 'link': 'https://www.mql5.com/en/blogs/post/724674', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1, 2: 1, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [11186720], 2: [255], 3: [42495], 4: [42495], 5: [15570276], 6: [15570276]}, 'widths': {1: 1, 2: 1, 3: 3, 4: 3, 5: 3, 6: 3}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'Stochastic', 2: 'Signal', 3: 'Bullish_OverSold', 4: 'Bearish OverSold', 5: 'Bullish_OverBought', 6: 'Bearish_OverBought'}, 'levels': [80.0, 20.0], 'description': ['Detect bullish and bearish engulfing candles when entering overbought or oversold territory'], 'name': 'EngulfingStochastic', 'source': 'MQL5 Indicators/Engulfing Stochastic/EngulfingStochastic.mq5', 'folder': 'Engulfing Stochastic', 'inputs': [{'mql': 'overSold', 'py': 'overSold', 'param': 'overSold', 'type': 'int', 'default': 20, 'label': 'Over Sold', 'sinput': False}, {'mql': 'overBought', 'py': 'overBought', 'param': 'overBought', 'type': 'int', 'default': 80, 'label': 'Over Bought', 'sinput': False}, {'mql': 'type', 'py': 'type_', 'param': 'type_', 'type': 'int', 'default': 1, 'label': 'type of the function', 'sinput': False}, {'mql': 'Kperiod', 'py': 'Kperiod', 'param': 'Kperiod', 'type': 'int', 'default': 5, 'label': 'the K period (the number of bars for calculation)', 'sinput': False}, {'mql': 'Dperiod', 'py': 'Dperiod', 'param': 'Dperiod', 'type': 'int', 'default': 3, 'label': 'the D period (the period of primary smoothing)', 'sinput': False}, {'mql': 'slowing', 'py': 'slowing', 'param': 'slowing', 'type': 'int', 'default': 3, 'label': 'period of final smoothing', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'type of smoothing', 'sinput': False}, {'mql': 'price_field', 'py': 'price_field', 'param': 'price_field', 'type': 'int', 'default': 0, 'label': 'method of calculation of the Stochastic', 'sinput': False}, {'mql': 'symbol', 'py': 'symbol', 'param': None, 'type': 'string', 'default': ' ', 'label': 'symbol', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 0, 'label': 'timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Creation
Call_iStochastic = 0
Call_IndicatorCreate = 1
_enum('Creation', {0: 'Call_iStochastic', 1: 'Call_IndicatorCreate'})

# ---- inputs and global variables
overSold = _input('overSold', 20)  # Over Sold
overBought = _input('overBought', 80)  # Over Bought
type_ = _input('type_', Call_IndicatorCreate)  # type of the function
Kperiod = _input('Kperiod', 5)  # the K period (the number of bars for calculation)
Dperiod = _input('Dperiod', 3)  # the D period (the period of primary smoothing)
slowing = _input('slowing', 3)  # period of final smoothing
ma_method = _input('ma_method', MODE_SMA)  # type of smoothing
price_field = _input('price_field', STO_LOWHIGH)  # method of calculation of the Stochastic
symbol = _input('symbol', ' ')  # symbol
period = _input('period', PERIOD_CURRENT)  # timeframe
StochasticBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
BullishOverSold = Arr(0, 0.0)
BearishOverSold = Arr(0, 0.0)
BullishOverBought = Arr(0, 0.0)
BearishOverBought = Arr(0, 0.0)
handle = 0
short_name = ""
bars_calculated = 0

def OnInit():
    global handle, name, short_name
    display = 'OverBought ' + _str(overBought)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, display)
    display = 'OverSold ' + _str(overSold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, display)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overBought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, overSold)
    SetIndexBuffer(0, StochasticBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, BullishOverSold, INDICATOR_DATA)
    SetIndexBuffer(3, BearishOverSold, INDICATOR_DATA)
    SetIndexBuffer(4, BullishOverBought, INDICATOR_DATA)
    SetIndexBuffer(5, BearishOverBought, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 236)
    PlotIndexSetInteger(3, PLOT_ARROW, 238)
    PlotIndexSetInteger(4, PLOT_ARROW, 236)
    PlotIndexSetInteger(5, PLOT_ARROW, 238)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    name = symbol
    StringTrimRight(_GlobRef(globals(), 'name'))
    StringTrimLeft(_GlobRef(globals(), 'name'))
    if StringLen(name) == 0:
        name = Symbol()
    if type_ == Call_iStochastic:
        handle = iStochastic(name, period, Kperiod, Dperiod, slowing, ma_method, price_field)
    else:
        pars = Arr(5, 0, dyn=False, factory=MqlParam)
        pars[0].type = TYPE_INT
        pars[0].integer_value = Kperiod
        pars[1].type = TYPE_INT
        pars[1].integer_value = Dperiod
        pars[2].type = TYPE_INT
        pars[2].integer_value = slowing
        pars[3].type = TYPE_INT
        pars[3].integer_value = ma_method
        pars[4].type = TYPE_INT
        pars[4].integer_value = price_field
        handle = IndicatorCreate(name, period, IND_STOCHASTIC, 5, pars)
    if handle == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iStochastic indicator for the symbol %s/%s, error code %d', name, EnumToString(period, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    short_name = StringFormat('Stoch(%s, %d, %d, %d)', name, Kperiod, Dperiod, slowing)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overBought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, overSold)
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
    if not FillArraysFromBuffers(StochasticBuffer, SignalBuffer, handle, values_to_copy):
        return 0
    comm = StringFormat('%s ==>  Updated value in the indicator %s: %d', TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS), short_name, values_to_copy)
    Comment(comm)
    bars_calculated = calculated
    OverBoughtAndSoldCalculations(rates_total, prev_calculated, open, close)
    return rates_total

def OverBoughtAndSoldCalculations(total, done, open, close):
    for i in range(done, total):
        if i != 0:
            if SignalBuffer[i] > overBought and SignalBuffer[i - 1] < overBought:
                if CheckForEngulfing(open[i - 1], close[i - 1], open[i], close[i]) == True:
                    if open[i] < close[i]:
                        BullishOverBought[i] = SignalBuffer[i]
                    else:
                        BearishOverBought[i] = SignalBuffer[i]
            elif SignalBuffer[i] < overSold and SignalBuffer[i - 1] > overSold:
                if CheckForEngulfing(open[i - 1], close[i - 1], open[i], close[i]) == True:
                    if open[i] < close[i]:
                        BullishOverSold[i] = SignalBuffer[i]
                    else:
                        BearishOverSold[i] = SignalBuffer[i]

def CheckForEngulfing(open1, close1, open2, close2):
    if (open1 >= close2 and close1 <= open2) and open1 < close1:
        return True
    elif (open1 <= close2 and close1 >= open2) and open1 > open2:
        return True
    return False

def FillArraysFromBuffers(main_buffer, signal_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, MAIN_LINE, 0, amount, main_buffer) < 0:
        PrintFormat('Failed to copy data from the iStochastic indicator, error code %d', GetLastError())
        return False
    if CopyBuffer(ind_handle, SIGNAL_LINE, 0, amount, signal_buffer) < 0:
        PrintFormat('Failed to copy data from the iStochastic indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    Comment('')

# ---- global variables initialised from expressions
name = symbol


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EngulfingStochastic(_MQL5Indicator):
    name = 'EngulfingStochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'overSold': 20,  # Over Sold
        'overBought': 80,  # Over Bought
        'type_': _Choice({0: 'use iStochastic', 1: 'use IndicatorCreate'}, default=1),  # type of the function
        'Kperiod': 5,  # the K period (the number of bars for calculation)
        'Dperiod': 3,  # the D period (the period of primary smoothing)
        'slowing': 3,  # period of final smoothing
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # type of smoothing
        'price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # method of calculation of the Stochastic
        'period': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # timeframe
    }
    y_range = (0.0, 100.0)

