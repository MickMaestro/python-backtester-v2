"""BW_Zone_Trading — converted from MQL5: MQL5 Indicators/BW_Zone_Trading/BW_Zone_Trading.mq5

Modified BW Zone Trading
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 16, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 17}, 'colors': {1: [16711680], 2: [255], 3: [16711680], 4: [2237106], 5: [3329330, 17919, 8421504]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Signal Up', 2: 'Signal Down', 3: 'Bullish zone', 4: 'Bearish zone', 5: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Modified BW Zone Trading'], 'name': 'BW_Zone_Trading', 'source': 'MQL5 Indicators/BW_Zone_Trading/BW_Zone_Trading.mq5', 'folder': 'BW_Zone_Trading', 'inputs': [{'mql': 'InpPeriodFastMA', 'py': 'InpPeriodFastMA', 'param': 'InpPeriodFastMA', 'type': 'uint', 'default': 5, 'label': 'AO Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlowMA', 'py': 'InpPeriodSlowMA', 'param': 'InpPeriodSlowMA', 'type': 'uint', 'default': 35, 'label': 'AO Slow MA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 5, 'label': 'AO Applied price', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'AO Calculation method', 'sinput': False}, {'mql': 'InpAccDec', 'py': 'InpAccDec', 'param': 'InpAccDec', 'type': 'uint', 'default': 5, 'label': 'AC smoothing period', 'sinput': False}, {'mql': 'InpFilter', 'py': 'InpFilter', 'param': 'InpFilter', 'type': 'int', 'default': 0, 'label': 'Filter type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_FILTER_TYPE
FILTER_TYPE_ONE = 0
FILTER_TYPE_TWO = 1
FILTER_TYPE_THREE = 2
_enum('ENUM_FILTER_TYPE', {0: 'FILTER_TYPE_ONE', 1: 'FILTER_TYPE_TWO', 2: 'FILTER_TYPE_THREE'})

# ---- inputs and global variables
InpPeriodFastMA = _input('InpPeriodFastMA', 5)  # AO Fast MA period
InpPeriodSlowMA = _input('InpPeriodSlowMA', 35)  # AO Slow MA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_MEDIAN)  # AO Applied price
InpMethod = _input('InpMethod', MODE_SMA)  # AO Calculation method
InpAccDec = _input('InpAccDec', 5)  # AC smoothing period
InpFilter = _input('InpFilter', FILTER_TYPE_ONE)  # Filter type
BufferArrUP = Arr(0, 0.0)
BufferArrDN = Arr(0, 0.0)
BufferBullish = Arr(0, 0.0)
BufferBearish = Arr(0, 0.0)
BufferOpen = Arr(0, 0.0)
BufferHigh = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
BufferClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferAO = Arr(0, 0.0)
BufferAC = Arr(0, 0.0)
BufferSigAO = Arr(0, 0.0)
BufferSigAC = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
period_fast_ma = 0
period_slow_ma = 0
acc_dec = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global acc_dec, handle_fma, handle_sma, period_fast_ma, period_slow_ma
    period_fast_ma = (1 if (InpPeriodFastMA < 1) else InpPeriodFastMA)
    period_slow_ma = (1 if (InpPeriodSlowMA < 1) else InpPeriodSlowMA)
    acc_dec = (1 if (InpAccDec < 1) else InpAccDec)
    SetIndexBuffer(0, BufferArrUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferArrDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBullish, INDICATOR_DATA)
    SetIndexBuffer(3, BufferBearish, INDICATOR_DATA)
    SetIndexBuffer(4, BufferOpen, INDICATOR_DATA)
    SetIndexBuffer(5, BufferHigh, INDICATOR_DATA)
    SetIndexBuffer(6, BufferLow, INDICATOR_DATA)
    SetIndexBuffer(7, BufferClose, INDICATOR_DATA)
    SetIndexBuffer(8, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(9, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferAO, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferAC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferSigAO, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferSigAC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, BufferSignal, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'BW Zone(' + _str(period_fast_ma) + ',' + _str(period_slow_ma) + ',' + _str(acc_dec) + ')')
    PlotIndexSetInteger(0, PLOT_ARROW, 32)
    PlotIndexSetInteger(1, PLOT_ARROW, 32)
    PlotIndexSetInteger(2, PLOT_ARROW, 32)
    PlotIndexSetInteger(3, PLOT_ARROW, 32)
    PlotIndexSetInteger(4, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferArrUP, True)
    ArraySetAsSeries(BufferArrDN, True)
    ArraySetAsSeries(BufferBullish, True)
    ArraySetAsSeries(BufferBearish, True)
    ArraySetAsSeries(BufferOpen, True)
    ArraySetAsSeries(BufferHigh, True)
    ArraySetAsSeries(BufferLow, True)
    ArraySetAsSeries(BufferClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferAO, True)
    ArraySetAsSeries(BufferAC, True)
    ArraySetAsSeries(BufferSigAO, True)
    ArraySetAsSeries(BufferSigAC, True)
    ArraySetAsSeries(BufferSignal, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fast_ma, 0, InpMethod, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The Fast iMA(', _str(period_fast_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_sma = iMA(None, PERIOD_CURRENT, period_slow_ma, 0, InpMethod, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The Slow iMA(', _str(period_slow_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(period_fast_ma, fmax(period_slow_ma, acc_dec))
    if rates_total < max_:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferArrUP, EMPTY_VALUE)
        ArrayInitialize(BufferArrDN, EMPTY_VALUE)
        ArrayInitialize(BufferBullish, EMPTY_VALUE)
        ArrayInitialize(BufferBearish, EMPTY_VALUE)
        ArrayInitialize(BufferOpen, 0)
        ArrayInitialize(BufferHigh, 0)
        ArrayInitialize(BufferLow, 0)
        ArrayInitialize(BufferClose, 0)
        ArrayInitialize(BufferFMA, EMPTY_VALUE)
        ArrayInitialize(BufferSMA, EMPTY_VALUE)
        ArrayInitialize(BufferAO, 0)
        ArrayInitialize(BufferAC, 0)
        ArrayInitialize(BufferSigAO, 0)
        ArrayInitialize(BufferSigAC, 0)
        ArrayInitialize(BufferSignal, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferAO[i] = BufferFMA[i] - BufferSMA[i]
    for i in range(limit, 0 - 1, -1):
        BufferAC[i] = BufferAO[i] - MAOnArray(BufferAO, 0, acc_dec, 0, InpMethod, i)
    for i in range(limit, 0 - 1, -1):
        BufferBearish[i] = EMPTY_VALUE
        BufferBullish[i] = BufferBearish[i]
        BufferArrDN[i] = BufferBullish[i]
        BufferArrUP[i] = BufferArrDN[i]
        BufferSignal[i] = 2.0
        BufferSigAO[i] = (0 if (BufferAO[i] > BufferAO[i + 1]) else 1 if (BufferAO[i] < BufferAO[i + 1]) else BufferSigAO[i + 1])
        BufferSigAC[i] = (0 if (BufferAC[i] > BufferAC[i + 1]) else 1 if (BufferAC[i] < BufferAC[i + 1]) else BufferSigAC[i + 1])
        BufferSignal[i] = ((0 if (BufferSigAO[i] == 0 and BufferSigAC[i] == 0) else 1 if (BufferSigAO[i] == 1 and BufferSigAC[i] == 1) else 2) if (InpFilter == FILTER_TYPE_ONE) else BufferSigAO[i] if (InpFilter == FILTER_TYPE_TWO) else BufferSigAC[i] if (InpFilter == FILTER_TYPE_THREE) else 2)
        BufferBullish[i] = (low[i] if (BufferSignal[i] == 0) else EMPTY_VALUE)
        BufferBearish[i] = (high[i] if (BufferSignal[i] == 1) else EMPTY_VALUE)
        BufferArrUP[i] = (low[i] if (BufferBullish[i] != EMPTY_VALUE and BufferBullish[i + 1] == EMPTY_VALUE) else EMPTY_VALUE)
        BufferArrDN[i] = (high[i] if (BufferBearish[i] != EMPTY_VALUE and BufferBearish[i + 1] == EMPTY_VALUE) else EMPTY_VALUE)
        BufferOpen[i] = open[i]
        BufferHigh[i] = high[i]
        BufferLow[i] = low[i]
        BufferClose[i] = close[i]
        BufferColors[i] = BufferSignal[i]
    return rates_total

def MAOnArray(array, total, period, ma_shift, ma_method, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period - ma_shift):
        return 0.0
    _sw1 = ma_method
    if _sw1 == MODE_SMA:
        total = ArrayCopy(arr, array, 0, shift + ma_shift, period)
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        i = 0
        pos = total - 1
        i = 1
        while i < period:
            sum_ += arr[pos]
            i += 1
            pos -= 1
        while pos >= 0:
            sum_ += arr[pos]
            buf[pos] = _fdiv(sum_, period)
            sum_ -= arr[pos + period - 1]
            pos -= 1
        return buf[0]
    elif _sw1 == MODE_EMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        pr = _fdiv(2.0, period + 1)
        pos = total - 2
        while pos >= 0:
            if pos == (total - 2):
                buf[pos + 1] = array[pos + 1]
            buf[pos] = (array[pos] * pr) + (buf[pos + 1] * (1 - pr))
            pos -= 1
        return buf[shift + ma_shift]
    elif _sw1 == MODE_SMMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        i = 0
        k = 0
        pos = 0
        pos = total - period
        while pos >= 0:
            if pos == (total - period):
                i = 0
                k = pos
                while i < period:
                    sum_ += array[k]
                    buf[k] = 0.0
                    i += 1
                    k += 1
            else:
                sum_ = (buf[pos + 1] * (period - 1)) + array[pos]
            buf[pos] = _fdiv(sum_, period)
            pos -= 1
        return buf[shift + ma_shift]
    elif _sw1 == MODE_LWMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        lsum = 0.0
        price = 0.0
        i = 0
        weight = 0
        pos = total - 1
        i = 1
        while i <= period:
            price = array[pos]
            sum_ += price * i
            lsum += price
            weight += i
            i += 1
            pos -= 1
        pos += 1
        i = pos + period
        while pos >= 0:
            buf[pos] = _fdiv(sum_, weight)
            if pos == 0:
                break
            pos -= 1
            i -= 1
            price = array[pos]
            sum_ = sum_ - lsum + (price * period)
            lsum -= array[i]
            lsum += price
        return buf[shift + ma_shift]
    else:
        return 0.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BWZoneTrading(_MQL5Indicator):
    name = 'BW_Zone_Trading'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastMA': 5,  # AO Fast MA period
        'InpPeriodSlowMA': 35,  # AO Slow MA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # AO Applied price
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # AO Calculation method
        'InpAccDec': 5,  # AC smoothing period
        'InpFilter': _Choice({0: 'By AO and AC', 1: 'By AO', 2: 'By AC'}, default=0),  # Filter type
    }

