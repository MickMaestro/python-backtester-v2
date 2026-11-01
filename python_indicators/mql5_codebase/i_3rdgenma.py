"""3rdGenMA — converted from MQL5: MQL5 Indicators/3rd Generation Moving Average MT5/3rdGenMA.mq5

3rd Generation MA based on research paper by Dr. Manfred
Offers least possible lag but still provides price smoothing.
Copyright: www.Wolfforex.com, 2025; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.Wolfforex.com, 2025', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['3rd Generation MA based on research paper by Dr. Manfred', 'Offers least possible lag but still provides price smoothing.'], 'name': '3rdGenMA', 'source': 'MQL5 Indicators/3rd Generation Moving Average MT5/3rdGenMA.mq5', 'folder': '3rd Generation Moving Average MT5', 'inputs': [{'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'MA_Sampling_Period', 'py': 'MA_Sampling_Period', 'param': 'MA_Sampling_Period', 'type': 'int', 'default': 220, 'label': 'MA_Sampling_Period (should be more than 4 * MA_Period)', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MA_Applied_Price', 'py': 'MA_Applied_Price', 'param': 'MA_Applied_Price', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Period = _input('MA_Period', 50)
MA_Sampling_Period = _input('MA_Sampling_Period', 220)  # MA_Sampling_Period (should be more than 4 * MA_Period)
MA_Method = _input('MA_Method', MODE_EMA)
MA_Applied_Price = _input('MA_Applied_Price', PRICE_TYPICAL)
MA3G = Arr(0, 0.0)
MA1 = Arr(0, 0.0)
MA2 = Arr(0, 0.0)
Lambda = 0.0
Alpha = 0.0
handle = 0
FirstRun = True

def OnInit():
    global Alpha, Lambda, handle
    short_name = ""
    if MA_Sampling_Period < (MA_Period * 4):
        Print('MA_Sampling_Period should be >= MA_Period * 4.')
        return INIT_FAILED
    SetIndexBuffer(0, MA3G, INDICATOR_DATA)
    SetIndexBuffer(1, MA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, MA2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(MA3G, True)
    ArraySetAsSeries(MA1, True)
    ArraySetAsSeries(MA2, True)
    _sw1 = MA_Method
    if _sw1 == MODE_EMA:
        short_name = '3GEMA('
    elif _sw1 == MODE_SMMA:
        short_name = '3GSMMA('
    elif _sw1 == MODE_LWMA:
        short_name = '3GLWMA('
    else:
        short_name = '3GSMA('
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + IntegerToString(MA_Period) + ',' + IntegerToString(MA_Sampling_Period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    handle = iMA(None, 0, MA_Sampling_Period, 0, MA_Method, MA_Applied_Price)
    if handle == INVALID_HANDLE:
        Print('Failed to initialize Moving Average.')
        return INIT_FAILED
    Lambda = _fdiv(1.0 * MA_Sampling_Period, 1.0 * MA_Period)
    Alpha = _fdiv(Lambda * (MA_Sampling_Period - 1), MA_Sampling_Period - Lambda)
    Print('Lambda = ', Lambda, '; Alpha = ', Alpha)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tickvolume, volume, spread):
    global FirstRun
    i = 0
    ExtCountedBars = 0
    TotalPeriod = MA_Period + MA_Sampling_Period
    if rates_total <= TotalPeriod:
        Print('Not enough bars.')
        return 0
    if FirstRun:
        ExtCountedBars = 0
    else:
        ExtCountedBars = prev_calculated
        if ExtCountedBars < 0:
            return -1
        if (rates_total - ExtCountedBars) < TotalPeriod:
            ExtCountedBars = rates_total - TotalPeriod
    MABars = rates_total - ExtCountedBars + MA_Period + 2
    if MABars > rates_total:
        MABars = rates_total
    if CopyBuffer(handle, 0, 0, MABars, MA1) != MABars:
        return 0
    MAonMABars = rates_total - ExtCountedBars + MA_Period
    if MAonMABars > rates_total:
        MAonMABars = rates_total
    iMAOnArrayMQL4(MA1, MAonMABars, MA_Period, MA_Method, MA2)
    i = rates_total - ExtCountedBars - 1
    for i in range(i, 0 - 1, -1):
        MA3G[i] = ((Alpha + 1) * MA1[i]) - (Alpha * MA2[i])
    else:
        i = _range_end(i, 0 - 1, -1)
    FirstRun = False
    return rates_total

def iMAOnArrayMQL4(array, total, period, ma_method, buf):
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total <= period:
        return
    _sw2 = ma_method
    if _sw2 == MODE_SMA:
        total = ArrayCopy(arr, array, 0, 0, period)
        if ArrayResize(buf, total) < 0:
            return
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
        return
    elif _sw2 == MODE_EMA:
        if ArrayResize(buf, total) < 0:
            return
        pr = _fdiv(2.0, period + 1)
        pos = total - 2
        while pos >= 0:
            if pos == (total - 2) and buf[pos + 1] == EMPTY_VALUE:
                buf[pos + 1] = array[pos + 1]
            buf[pos] = (array[pos] * pr) + (buf[pos + 1] * (1 - pr))
            pos -= 1
        return
    elif _sw2 == MODE_SMMA:
        if ArrayResize(buf, total) < 0:
            return
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
        return
    elif _sw2 == MODE_LWMA:
        if ArrayResize(buf, total) < 0:
            return
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
        return
    else:
        return


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind3rdGenMA(_MQL5Indicator):
    name = '3rdGenMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Period': 50,
        'MA_Sampling_Period': 220,  # MA_Sampling_Period (should be more than 4 * MA_Period)
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MA_Applied_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),
    }

