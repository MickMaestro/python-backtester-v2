"""vip_dsr — converted from MQL5: MQL5 Indicators/VIP_DSR/vip_dsr.mq5

Copyright: Copyright © 2010, KingLion; Link: http://www.metastock.org.ua/; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, KingLion', 'link': 'http://www.metastock.org.ua/', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [25600], 2: [2237106], 3: [755384]}, 'widths': {1: 2, 2: 2, 3: 1}, 'styles': {1: 0, 2: 0, 3: 2}, 'labels': {1: 'Resistance', 2: 'Support', 3: 'Mean'}, 'levels': [], 'description': [], 'name': 'vip_dsr', 'source': 'MQL5 Indicators/VIP_DSR/vip_dsr.mq5', 'folder': 'VIP_DSR', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Custom_Indicator = 'VIP Dynamic Support/Resistance'
Web_Address = 'www.metastock.org.ua'
Support = Arr(0, 0.0)
Resistance = Arr(0, 0.0)
Mean = Arr(0, 0.0)
Pivot = Arr(0, 0.0)
MA = Arr(0, 0.0)
counted_bars = 0

def OnInit():
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, Custom_Indicator + ' | ' + Web_Address)
    SetIndexBuffer(0, Resistance)
    SetIndexBuffer(1, Support)
    SetIndexBuffer(2, Mean)
    SetIndexBuffer(3, Pivot)
    SetIndexBuffer(4, MA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 25)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 25)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, 25)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global counted_bars
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(Resistance, True)
    ArraySetAsSeries(Support, True)
    ArraySetAsSeries(Mean, True)
    ArraySetAsSeries(Pivot, True)
    ArraySetAsSeries(MA, True)
    bars = Bars(Symbol(), Period())
    if bars <= 0:
        synchronized = False
        attempts = 0
        while attempts < 5:
            if SeriesInfoInteger(Symbol(), 0, SERIES_SYNCHRONIZED):
                synchronized = True
                break
            attempts += 1
            Sleep(10)
        if not synchronized:
            return rates_total
    counted_bars = 0
    if prev_calculated > 0:
        counted_bars = prev_calculated - 1
    if bars <= 25:
        return 0
    i = bars - counted_bars - 28
    if counted_bars > 0:
        i += 1
    else:
        Resistance[i] = high[i]
        Support[i] = low[i]
    j = 0
    j = 0
    for j in range(j, i):
        Pivot[j] = (high[iHighest_u(Symbol(), Period(), 2, 3, j)] + low[iLowest_u(Symbol(), Period(), 1, 3, j)] + close[j]) / 3.0
    else:
        j = _range_end(j, i, 1)
    j = 0
    for j in range(j, i):
        MA[j] = iMASMA(Pivot, bars, 25, 0, MODE_SMA, j)
    else:
        j = _range_end(j, i, 1)
    j = i - 1
    for j in range(j, 0 - 1, -1):
        if Pivot[j + 1] > MA[j + 1] and Pivot[j] < MA[j]:
            Resistance[j] = high[iHighest_u(Symbol(), Period(), 2, 28, j)]
        else:
            Resistance[j] = Resistance[j + 1]
    else:
        j = _range_end(j, 0 - 1, -1)
    j = i - 1
    for j in range(j, 0 - 1, -1):
        if Pivot[j + 1] < MA[j + 1] and Pivot[j] > MA[j]:
            Support[j] = low[iLowest_u(Symbol(), Period(), 1, 28, j)]
        else:
            Support[j] = Support[j + 1]
    else:
        j = _range_end(j, 0 - 1, -1)
    j = 0
    for j in range(j, i):
        Mean[j] = NormalizeDouble((Resistance[j] + Support[j]) / 2.0, Digits())
    else:
        j = _range_end(j, i, 1)
    return rates_total

def iHighest_u(symbol, timeframe, type_, count=WHOLE_ARRAY, start=0):
    rc = 0
    if start < 0:
        return rc
    if count <= 0:
        count = Bars(symbol, timeframe)
    if type_ == 0:
        Open = Arr(0, 0.0)
        ArraySetAsSeries(Open, True)
        CopyOpen(symbol, timeframe, start, count, Open)
        rc = ArrayMaximum(Open, 0, count) + start
    elif type_ == 1:
        Low = Arr(0, 0.0)
        ArraySetAsSeries(Low, True)
        CopyLow(symbol, timeframe, start, count, Low)
        rc = ArrayMaximum(Low, 0, count) + start
    elif type_ == 2:
        High = Arr(0, 0.0)
        ArraySetAsSeries(High, True)
        CopyHigh(symbol, timeframe, start, count, High)
        rc = ArrayMaximum(High, 0, count) + start
    elif type_ == 3:
        Close = Arr(0, 0.0)
        ArraySetAsSeries(Close, True)
        CopyClose(symbol, timeframe, start, count, Close)
        rc = ArrayMaximum(Close, 0, count) + start
    elif type_ == 4:
        Volume = Arr(0, 0)
        ArraySetAsSeries(Volume, True)
        CopyTickVolume(symbol, timeframe, start, count, Volume)
        rc = ArrayMaximum(Volume, 0, count) + start
    elif type_ == 5:
        Time = Arr(0, 0)
        ArraySetAsSeries(Time, True)
        CopyTime(symbol, timeframe, start, count, Time)
        rc = ArrayMaximum(Time, 0, count) + start
    return rc

def iLowest_u(symbol, timeframe, type_, count=WHOLE_ARRAY, start=0):
    rc = 0
    if start < 0:
        return -1
    if count <= 0:
        count = Bars(symbol, timeframe)
    if type_ == 0:
        Open = Arr(0, 0.0)
        ArraySetAsSeries(Open, True)
        CopyOpen(symbol, timeframe, start, count, Open)
        rc = ArrayMinimum(Open, 0, count) + start
    elif type_ == 1:
        Low = Arr(0, 0.0)
        ArraySetAsSeries(Low, True)
        CopyLow(symbol, timeframe, start, count, Low)
        rc = ArrayMinimum(Low, 0, count) + start
    elif type_ == 2:
        High = Arr(0, 0.0)
        ArraySetAsSeries(High, True)
        CopyHigh(symbol, timeframe, start, count, High)
        rc = ArrayMinimum(High, 0, count) + start
    elif type_ == 3:
        Close = Arr(0, 0.0)
        ArraySetAsSeries(Close, True)
        CopyClose(symbol, timeframe, start, count, Close)
        rc = ArrayMinimum(Close, 0, count) + start
    elif type_ == 4:
        Volume = Arr(0, 0)
        ArraySetAsSeries(Volume, True)
        CopyTickVolume(symbol, timeframe, start, count, Volume)
        rc = ArrayMinimum(Volume, 0, count) + start
    elif type_ == 5:
        Time = Arr(0, 0)
        ArraySetAsSeries(Time, True)
        CopyTime(symbol, timeframe, start, count, Time)
        rc = ArrayMinimum(Time, 0, count) + start
    return rc

def iMASMA(array, total, period, ma_shift, ma_method, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period - ma_shift):
        return 0.0
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VipDsr(_MQL5Indicator):
    name = 'vip_dsr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

