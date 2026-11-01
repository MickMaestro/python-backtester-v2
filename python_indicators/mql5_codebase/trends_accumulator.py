"""Trends_Accumulator — converted from MQL5: MQL5 Indicators/Trends Accumulator/Trends_Accumulator.mq5

Trends Accumulator
Copyright: Copyright 2016, quebralim; Link: https://www.mql5.com/en/users/quebralim; Version: 1.4

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, quebralim', 'link': 'https://www.mql5.com/en/users/quebralim', 'version': '1.4', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [14822282]}, 'widths': {1: 10}, 'styles': {}, 'labels': {1: 'Trends Accumulator'}, 'levels': [], 'description': ['Trends Accumulator'], 'name': 'Trends_Accumulator', 'source': 'MQL5 Indicators/Trends Accumulator/Trends_Accumulator.mq5', 'folder': 'Trends Accumulator', 'inputs': [{'mql': 'Threshold', 'py': 'Threshold', 'param': 'Threshold', 'type': 'uint', 'default': 20, 'label': 'Threshold (in points)', 'sinput': False}, {'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'uint', 'default': 6, 'label': 'MA Period (in bars)', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 1, 'label': 'MA Method', 'sinput': False}, {'mql': 'MA_Price', 'py': 'MA_Price', 'param': 'MA_Price', 'type': 'int', 'default': 6, 'label': 'MA Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Threshold = _input('Threshold', 20)  # Threshold (in points)
MA_Period = _input('MA_Period', 6)  # MA Period (in bars)
MA_Method = _input('MA_Method', MODE_EMA)  # MA Method
MA_Price = _input('MA_Price', PRICE_TYPICAL)  # MA Price
bTA = Arr(0, 0.0)  # TA Buffer
bMA = Arr(0, 0.0)  # MA Buffer
hMA = 0  # MA Handler

def OnInit():
    global hMA
    if MA_Period < 1:
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, bTA, INDICATOR_DATA)
    SetIndexBuffer(1, bMA, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MA_Period)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Accumulator (' + _str(Threshold) + ',' + _str(MA_Period) + ')')
    hMA = iMA(Symbol(), Period(), MA_Period, 0, MA_Method, MA_Price)
    if hMA == INVALID_HANDLE:
        Print('Failed to initilize the MA indicator!')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= _int(MA_Period):
        return 0
    ResetLastError()
    if BarsCalculated(hMA) < rates_total:
        Print('Not all data of MA is calculated. Error #', GetLastError())
        return prev_calculated
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated + 2
    if False:
        return 0
    ResetLastError()
    if CopyBuffer(hMA, 0, 0, to_copy, bMA) <= 0:
        Print('Failed getting MA! Error #', GetLastError())
        return prev_calculated
    i = 0
    if prev_calculated <= _int(MA_Period):
        i = _int(MA_Period)
    else:
        i = prev_calculated - 1
    iMax = 0
    while i < (rates_total - 1):
        if False:
            return 0
        bTA[i] = bTA[i - 1] + bMA[i] - bMA[i - 1]
        if (bTA[i] * bTA[i - 1]) > 0:
            iMax = MaxAround(i)
        else:
            iMax = MaxAround(i - 1)
        if (bTA[iMax] > 0 and (bTA[iMax] - bTA[i]) >= (Threshold * Point())) or (bTA[iMax] < 0 and (bTA[i] - bTA[iMax]) >= (Threshold * Point())):
            bTA[iMax + 1] = bMA[iMax + 1] - bMA[iMax]
            for k in range(iMax + 2, i + 1):
                bTA[k] = bTA[k - 1] + bMA[k] - bMA[k - 1]
        i += 1
    bTA[i] = bTA[i - 1] + bMA[i] - bMA[i - 1]
    return i

def MaxAround(i):
    iMax = i
    if bTA[i] > 0:
        while i > 0 and bTA[(i := i - 1)] > 0:
            if bTA[i] > bTA[iMax]:
                iMax = i
    elif bTA[i] < 0:
        while i > 0 and bTA[(i := i - 1)] < 0:
            if bTA[i] < bTA[iMax]:
                iMax = i
    return iMax


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendsAccumulator(_MQL5Indicator):
    name = 'Trends_Accumulator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Threshold': 20,  # Threshold (in points)
        'MA_Period': 6,  # MA Period (in bars)
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA Method
        'MA_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # MA Price
    }

