"""Brooky_Trend_Strength — converted from MQL5: MQL5 Indicators/Brooky Trend Strength for MT5/Brooky_Trend_Strength.mq5

Copyright: © 2023, Ryan Lawrence Johnson; Link: https://www.mql5.com/en/users/rjo/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© 2023, Ryan Lawrence Johnson', 'link': 'https://www.mql5.com/en/users/rjo/seller', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 6}, 'types': {}, 'colors': {1: [16711680], 2: [16711680], 3: [3937500], 4: [8421504], 5: [16748574], 6: [13353215]}, 'widths': {1: 1, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2}, 'styles': {7: 0, 8: 0, 9: 0}, 'labels': {}, 'levels': [0.0], 'description': [], 'name': 'Brooky_Trend_Strength', 'source': 'MQL5 Indicators/Brooky Trend Strength for MT5/Brooky_Trend_Strength.mq5', 'folder': 'Brooky Trend Strength for MT5', 'inputs': [{'mql': 'Calculation_Periods', 'py': 'Calculation_Periods', 'param': None, 'type': 'string', 'default': 'Amount of Bars used to Calculate', 'label': '', 'sinput': True}, {'mql': 'slow_period', 'py': 'slow_period', 'param': 'slow_period', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'fast_period', 'py': 'fast_period', 'param': 'fast_period', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'signal_period', 'py': 'signal_period', 'param': 'signal_period', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'slow_period_method', 'py': 'slow_period_method', 'param': 'slow_period_method', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'fast_period_method', 'py': 'fast_period_method', 'param': 'fast_period_method', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'signal_period_method', 'py': 'signal_period_method', 'param': 'signal_period_method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_Constant', 'py': 'Price_Constant', 'param': 'Price_Constant', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Sensitivity', 'py': 'Sensitivity', 'param': None, 'type': 'string', 'default': 'Control Strength Sensitivity', 'label': '', 'sinput': False}, {'mql': 'min_move', 'py': 'min_move', 'param': 'min_move', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'hi_lo_bars_back', 'py': 'hi_lo_bars_back', 'param': 'hi_lo_bars_back', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Calculation_Periods = _input('Calculation_Periods', 'Amount of Bars used to Calculate')
slow_period = _input('slow_period', 26)
fast_period = _input('fast_period', 12)
signal_period = _input('signal_period', 9)
slow_period_method = _input('slow_period_method', MODE_EMA)
fast_period_method = _input('fast_period_method', MODE_EMA)
signal_period_method = _input('signal_period_method', MODE_SMA)
Price_Constant = _input('Price_Constant', PRICE_CLOSE)
Sensitivity = _input('Sensitivity', 'Control Strength Sensitivity')
min_move = _input('min_move', 1.0)
hi_lo_bars_back = _input('hi_lo_bars_back', 5)
handle_ma_now = 0
handle_iatr = 0
handle_istddev = 0
copyBars = 0
limit = 0
bar = 0
slow_array = Arr(0, 0.0)
up_hist = Arr(0, 0.0)
dn_hist = Arr(0, 0.0)
tup_hist = Arr(0, 0.0)
tdn_hist = Arr(0, 0.0)
sig_array = Arr(0, 0.0)
move_array = Arr(0, 0.0)
ma_now = Arr(0, 0.0)
iatr = Arr(0, 0.0)
istddev = Arr(0, 0.0)

def OnDeinit(reason):
    if handle_ma_now != INVALID_HANDLE:
        IndicatorRelease(handle_ma_now)
    if handle_istddev != INVALID_HANDLE:
        IndicatorRelease(handle_istddev)
    if handle_iatr != INVALID_HANDLE:
        IndicatorRelease(handle_iatr)

def OnInit():
    global handle_iatr, handle_istddev, handle_ma_now
    SetIndexBuffer(0, slow_array, INDICATOR_DATA)
    SetIndexBuffer(1, up_hist, INDICATOR_DATA)
    SetIndexBuffer(2, dn_hist, INDICATOR_DATA)
    SetIndexBuffer(3, sig_array, INDICATOR_DATA)
    SetIndexBuffer(4, tup_hist, INDICATOR_DATA)
    SetIndexBuffer(5, tdn_hist, INDICATOR_DATA)
    SetIndexBuffer(6, move_array, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ma_now, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, iatr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, istddev, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(5, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(0, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(1, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(2, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(3, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(4, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(5, PLOT_LINE_STYLE, STYLE_SOLID)
    handle_ma_now = iCustom(None, 0, 'Custom_Moving_Average_sep_win', fast_period, 0, fast_period_method, Price_Constant)
    handle_istddev = iCustom(None, 0, 'StdDev_sep_win', slow_period, 0, slow_period_method, Price_Constant)
    handle_iatr = iCustom(None, 0, 'ATR_sep_win', slow_period, Price_Constant)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Brooky Trend Strength ' + 'Period (' + _str(slow_period) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bar, copyBars, limit
    if prev_calculated < 0 or rates_total < (slow_period - 1):
        return 0
    ArraySetAsSeries(slow_array, True)
    ArraySetAsSeries(up_hist, True)
    ArraySetAsSeries(dn_hist, True)
    ArraySetAsSeries(tup_hist, True)
    ArraySetAsSeries(tdn_hist, True)
    ArraySetAsSeries(sig_array, True)
    ArraySetAsSeries(move_array, True)
    ArraySetAsSeries(ma_now, True)
    ArraySetAsSeries(istddev, True)
    ArraySetAsSeries(iatr, True)
    if prev_calculated == 0:
        limit = rates_total - slow_period - 1
        copyBars = rates_total - slow_period - 1
    else:
        limit = rates_total - prev_calculated
        copyBars = rates_total - prev_calculated
    if (CopyBuffer(handle_ma_now, 0, 0, copyBars, ma_now) <= 0 or CopyBuffer(handle_istddev, 0, 0, copyBars, istddev) <= 0) or CopyBuffer(handle_iatr, 0, 0, copyBars, iatr) <= 0:
        return -1
    bar = limit
    while bar >= 0:
        move_array[bar] = MathAbs((iHighest(None, 0, MODE_HIGH, hi_lo_bars_back, bar) - iLowest(None, 0, MODE_LOW, hi_lo_bars_back, bar)) * Point() * 100000)
        slow_array[bar] = istddev[bar] - iatr[bar]
        if ma_now[bar] >= ma_now[bar + 1] and move_array[bar] >= min_move:
            up_hist[bar] = slow_array[bar]
        if ma_now[bar] <= ma_now[bar + 1] and move_array[bar] >= min_move:
            dn_hist[bar] = slow_array[bar]
        if ma_now[bar] <= ma_now[bar + 1] and move_array[bar] <= min_move:
            tup_hist[bar] = slow_array[bar]
        if ma_now[bar] >= ma_now[bar + 1] and move_array[bar] <= min_move:
            tdn_hist[bar] = slow_array[bar]
        bar -= 1
    bar = limit
    while bar >= 0:
        sig_array[bar] = iMAOnArray_u(slow_array, signal_period, 0, signal_period_method, bar)
        bar -= 1
    return rates_total - 1

def iMAOnArray_u(array, period, ma_shift, ma_method, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    total = ArraySize(array)
    if total <= period:
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
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BrookyTrendStrength(_MQL5Indicator):
    name = 'Brooky_Trend_Strength'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'slow_period': 26,
        'fast_period': 12,
        'signal_period': 9,
        'slow_period_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'fast_period_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'signal_period_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_Constant': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'min_move': 1.0,
        'hi_lo_bars_back': 5,
    }

