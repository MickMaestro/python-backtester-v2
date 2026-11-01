"""Price period SMA — converted from MQL5: MQL5 Indicators/Price period SMA/Price period SMA.mq5

Copyright: Copyright 2021, Lilita Bogackova; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, Lilita Bogackova', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329434], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'symbolPrice', 2: 'symbolSMA'}, 'levels': [], 'description': [], 'name': 'Price period SMA', 'source': 'MQL5 Indicators/Price period SMA/Price period SMA.mq5', 'folder': 'Price period SMA', 'inputs': [{'mql': '_symbolName', 'py': '_symbolName', 'param': None, 'type': 'string', 'default': '0', 'label': 'Symbol, 0 = take a symbol from the chart', 'sinput': False}, {'mql': '_useSMA', 'py': '_useSMA', 'param': '_useSMA', 'type': 'int', 'default': 1, 'label': 'Use moving average', 'sinput': False}, {'mql': '_appliedPrice', 'py': '_appliedPrice', 'param': '_appliedPrice', 'type': 'int', 'default': 7, 'label': 'Price', 'sinput': False}, {'mql': '_createVLine', 'py': '_createVLine', 'param': '_createVLine', 'type': 'bool', 'default': True, 'label': 'Create a period dividing line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_USE_SMA
HOUR_SMA = 0
DAY_SMA = 1
_enum('ENUM_USE_SMA', {0: 'HOUR_SMA', 1: 'DAY_SMA'})

# ---- inputs and global variables
_symbolName = _input('_symbolName', '0')  # Symbol, 0 = take a symbol from the chart
_useSMA = _input('_useSMA', DAY_SMA)  # Use moving average
_appliedPrice = _input('_appliedPrice', PRICE_WEIGHTED)  # Price
_createVLine = _input('_createVLine', True)  # Create a period dividing line
barsCalculated = 0
symbolHandle = -1
currDateTime = 0
seperator = 0
dateTime = 0
settPeriod = 1
timeStatic = 0
shortName = ''
symbolName = ''
chartSetSymbolPeriod = False
period = 0
symbolPriceBuffer = Arr(0, 0.0)
symbolSMABuffer = Arr(0, 0.0)
symbolPriceHandleBuffer = Arr(0, 0.0)

def OnInit():
    global chartSetSymbolPeriod, period, seperator, shortName, symbolHandle, symbolName
    SetIndexBuffer(0, symbolPriceBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, symbolSMABuffer, INDICATOR_DATA)
    SetIndexBuffer(2, symbolPriceHandleBuffer, INDICATOR_CALCULATIONS)
    period = PERIOD_CURRENT
    symbolName = _symbolName
    if StringLen(_symbolName) <= 1:
        symbolName = Symbol()
    _sw1 = _useSMA
    if _sw1 == HOUR_SMA:
        seperator = 1
        shortName = StringFormat('PP SMA (%s, %s)', symbolName, 'HOUR SMA')
        if Period() >= PERIOD_H1:
            period = PERIOD_M1
    elif _sw1 == DAY_SMA:
        seperator = 10
        shortName = StringFormat('PP SMA (%s, %s)', symbolName, 'DAY SMA')
        if Period() >= PERIOD_D1:
            period = PERIOD_M15
    IndicatorSetString(INDICATOR_SHORTNAME, shortName)
    symbolHandle = iMA(symbolName, PERIOD_CURRENT, settPeriod, 0, MODE_SMA, _appliedPrice)
    if symbolHandle == INVALID_HANDLE:
        return INIT_FAILED
    chartSetSymbolPeriod = False
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_SMAperiod, _s_OnCalculate_calculated_min, barsCalculated, chartSetSymbolPeriod, currDateTime, dateTime, timeStatic
    i = 0
    limit = 0
    periodSeperatorValue = 0.0
    if _s_OnCalculate_calculated_min == INT_MAX:
        calculated = BarsCalculated(symbolHandle)
        if calculated <= settPeriod:
            _s_OnCalculate_calculated_min = INT_MAX
            return 0
        if _s_OnCalculate_calculated_min > (calculated - settPeriod):
            _s_OnCalculate_calculated_min = calculated - settPeriod
        calculated = Bars(Symbol(), PERIOD_CURRENT)
        if calculated <= settPeriod:
            _s_OnCalculate_calculated_min = INT_MAX
            return 0
        if _s_OnCalculate_calculated_min > (calculated - settPeriod):
            _s_OnCalculate_calculated_min = calculated - settPeriod
    values_to_copy = 0
    if (prev_calculated == 0 or _s_OnCalculate_calculated_min != barsCalculated) or rates_total > (prev_calculated + 1):
        if _s_OnCalculate_calculated_min >= rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = _s_OnCalculate_calculated_min
    else:
        values_to_copy = rates_total - prev_calculated + 2
    barsCalculated = _s_OnCalculate_calculated_min
    limit = rates_total - values_to_copy
    FillArrayFromBuffer(symbolPriceHandleBuffer, symbolHandle, values_to_copy)
    i = limit + 1
    for i in range(i, rates_total):
        symbolPriceBuffer[i] = symbolPriceHandleBuffer[i]
        dateTime = DateTime(time[i], seperator)
        if dateTime != currDateTime:
            _s_OnCalculate_SMAperiod = -1
            currDateTime = dateTime
            if _createVLine and i >= (rates_total - (_idiv(1440, _idiv(PeriodSeconds(PERIOD_CURRENT), 60)) * seperator)):
                if not VLineCreate(time[i]):
                    Print('Error creating object: ', GetLastError())
        if time[i] != timeStatic:
            _s_OnCalculate_SMAperiod += 1
            timeStatic = time[i]
        symbolSMABuffer[i] = _fdiv(symbolPriceBuffer[i] * 2.0, 1.0 + _s_OnCalculate_SMAperiod) + (symbolSMABuffer[i - 1] * (1.0 - _fdiv(2.0, 1.0 + _s_OnCalculate_SMAperiod)))
    else:
        i = _range_end(i, rates_total, 1)
    if not chartSetSymbolPeriod:
        chartSetSymbolPeriod = ChartSetSymbolPeriod(ChartID(), Symbol(), period)
        ChartRedraw()
    return rates_total

def DateTime(time, sep):
    dt = MqlDateTime()
    TimeToStruct(time, dt)
    if sep == 1:
        return dt.hour
    else:
        return dt.day_of_week

def VLineCreate(time=0):
    global _s_VLineCreate_count
    ResetLastError()
    if ObjectFind(ChartID(), 'PP SMA' + IntegerToString((_s_VLineCreate_count := _s_VLineCreate_count + 1))) < 0:
        if not ObjectCreate(ChartID(), 'PP SMA' + IntegerToString(_s_VLineCreate_count), OBJ_VLINE, 0, time, 0):
            return False
        else:
            ObjectSetInteger(ChartID(), 'PP SMA' + IntegerToString(_s_VLineCreate_count), OBJPROP_COLOR, clrGreen)
            ChartRedraw(ChartID())
    return True

def FillArrayFromBuffer(ind_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, ind_buffer) < 0:
        PrintFormat('Failed to copy data from indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'PP SMA')

# ---- static local variables
_s_OnCalculate_calculated_min = INT_MAX
_s_OnCalculate_SMAperiod = 0
_s_VLineCreate_count = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PricePeriodSMA(_MQL5Indicator):
    name = 'Price period SMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        '_useSMA': _Choice({0: 'Hourly moving average', 1: 'Daily moving average'}, default=1),  # Use moving average
        '_appliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),  # Price
        '_createVLine': True,  # Create a period dividing line
    }

