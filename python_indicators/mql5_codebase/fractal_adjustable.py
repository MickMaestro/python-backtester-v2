"""Fractal_adjustable — converted from MQL5: MQL5 Indicators/Fractals - adjustable period and prices/Fractal_adjustable.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Fractal_adjustable', 'source': 'MQL5 Indicators/Fractals - adjustable period and prices/Fractal_adjustable.mq5', 'folder': 'Fractals - adjustable period and prices', 'inputs': [{'mql': 'FractalPeriod', 'py': 'FractalPeriod', 'param': 'FractalPeriod', 'type': 'int', 'default': 5, 'label': 'Fractal period: 5 for built in fractal', 'sinput': False}, {'mql': 'PriceHigh', 'py': 'PriceHigh', 'param': 'PriceHigh', 'type': 'int', 'default': 3, 'label': 'Price high', 'sinput': False}, {'mql': 'PriceLow', 'py': 'PriceLow', 'param': 'PriceLow', 'type': 'int', 'default': 4, 'label': 'Price low', 'sinput': False}, {'mql': 'UpperArrowDisplacement', 'py': 'UpperArrowDisplacement', 'param': 'UpperArrowDisplacement', 'type': 'double', 'default': 0.2, 'label': 'Upper arrow displacement', 'sinput': False}, {'mql': 'LowerArrowDisplacement', 'py': 'LowerArrowDisplacement', 'param': 'LowerArrowDisplacement', 'type': 'double', 'default': 0.2, 'label': 'Lower arrow displacement', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FractalPeriod = _input('FractalPeriod', 5)  # Fractal period: 5 for built in fractal
PriceHigh = _input('PriceHigh', PRICE_HIGH)  # Price high
PriceLow = _input('PriceLow', PRICE_LOW)  # Price low
UpperArrowDisplacement = _input('UpperArrowDisplacement', 0.2)  # Upper arrow displacement
LowerArrowDisplacement = _input('LowerArrowDisplacement', 0.2)  # Lower arrow displacement
v1 = Arr(0, 0.0)
v2 = Arr(0, 0.0)
f_pd = 0

def OnInit():
    global f_pd
    f_pd = FractalPeriod
    if MathMod(f_pd, 2) == 0:
        f_pd = f_pd + 1
    SetIndexBuffer(0, v1, INDICATOR_DATA)
    SetIndexBuffer(1, v2, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fractals - adjustable price')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = MathMin(MathMax(rates_total - prev_calculated, f_pd), rates_total - 1)
    half = _idiv(f_pd, 2)
    for i in range(limit, half - 1, -1):
        found = True
        compareTo = iMAMQL4("", 0, 1, 0, MODE_SMA, PriceHigh, i)
        for k in range(1, half + 1):
            if (i + k) < rates_total and iMAMQL4("", 0, 1, 0, MODE_SMA, PriceHigh, i + k) > compareTo:
                found = False
                break
            if (i - k) >= 0 and iMAMQL4("", 0, 1, 0, MODE_SMA, PriceHigh, i - k) >= compareTo:
                found = False
                break
        if found:
            v1[i] = high[i] + (iATRMQL4("", 0, 20, i) * UpperArrowDisplacement)
        else:
            v1[i] = EMPTY_VALUE
        found = True
        compareTo = iMAMQL4("", 0, 1, 0, MODE_SMA, PriceLow, i)
        for k in range(1, half + 1):
            if (i + k) < rates_total and iMAMQL4("", 0, 1, 0, MODE_SMA, PriceLow, i + k) < compareTo:
                found = False
                break
            if (i - k) >= 0 and iMAMQL4("", 0, 1, 0, MODE_SMA, PriceLow, i - k) <= compareTo:
                found = False
                break
        if found:
            v2[i] = low[i] - (iATRMQL4("", 0, 20, i) * LowerArrowDisplacement)
        else:
            v2[i] = EMPTY_VALUE
    return rates_total

def iMAMQL4(symbol, tf, period, ma_shift, method, price, shift):
    timeframe = TFMigrate(tf)
    ma_method = MethodMigrate(method)
    applied_price = PriceMigrate(price)
    handle = iMA(symbol, timeframe, period, ma_shift, ma_method, applied_price)
    if handle < 0:
        Print('The iMA object is not created: Error', GetLastError())
        return -1.0
    else:
        return CopyBufferMQL4(handle, 0, shift)

def iATRMQL4(symbol, tf, period, shift):
    timeframe = TFMigrate(tf)
    handle = iATR(symbol, timeframe, period)
    if handle < 0:
        Print(' The iATR  object is not created: Error ', GetLastError())
        return -1.0
    else:
        return CopyBufferMQL4(handle, 0, shift)

def TFMigrate(tf):
    _sw1 = tf
    if _sw1 == 0:
        return PERIOD_CURRENT
    elif _sw1 == 1:
        return PERIOD_M1
    elif _sw1 == 5:
        return PERIOD_M5
    elif _sw1 == 15:
        return PERIOD_M15
    elif _sw1 == 30:
        return PERIOD_M30
    elif _sw1 == 60:
        return PERIOD_H1
    elif _sw1 == 240:
        return PERIOD_H4
    elif _sw1 == 1440:
        return PERIOD_D1
    elif _sw1 == 10080:
        return PERIOD_W1
    elif _sw1 == 43200:
        return PERIOD_MN1
    elif _sw1 == 2:
        return PERIOD_M2
    elif _sw1 == 3:
        return PERIOD_M3
    elif _sw1 == 4:
        return PERIOD_M4
    elif _sw1 == 6:
        return PERIOD_M6
    elif _sw1 == 10:
        return PERIOD_M10
    elif _sw1 == 12:
        return PERIOD_M12
    elif _sw1 == 16385:
        return PERIOD_H1
    elif _sw1 == 16386:
        return PERIOD_H2
    elif _sw1 == 16387:
        return PERIOD_H3
    elif _sw1 == 16388:
        return PERIOD_H4
    elif _sw1 == 16390:
        return PERIOD_H6
    elif _sw1 == 16392:
        return PERIOD_H8
    elif _sw1 == 16396:
        return PERIOD_H12
    elif _sw1 == 16408:
        return PERIOD_D1
    elif _sw1 == 32769:
        return PERIOD_W1
    elif _sw1 == 49153:
        return PERIOD_MN1
    else:
        return PERIOD_CURRENT

def MethodMigrate(method):
    _sw2 = method
    if _sw2 == 0:
        return MODE_SMA
    elif _sw2 == 1:
        return MODE_EMA
    elif _sw2 == 2:
        return MODE_SMMA
    elif _sw2 == 3:
        return MODE_LWMA
    else:
        return MODE_SMA

def PriceMigrate(price):
    _sw3 = price
    if _sw3 == 1:
        return PRICE_CLOSE
    elif _sw3 == 2:
        return PRICE_OPEN
    elif _sw3 == 3:
        return PRICE_HIGH
    elif _sw3 == 4:
        return PRICE_LOW
    elif _sw3 == 5:
        return PRICE_MEDIAN
    elif _sw3 == 6:
        return PRICE_TYPICAL
    elif _sw3 == 7:
        return PRICE_WEIGHTED
    else:
        return PRICE_CLOSE

def CopyBufferMQL4(handle, index, shift):
    buf = Arr(0, 0.0)
    _sw4 = index
    if _sw4 == 0:
        if CopyBuffer(handle, 0, shift, 1, buf) > 0:
            return buf[0]
    elif _sw4 == 1:
        if CopyBuffer(handle, 1, shift, 1, buf) > 0:
            return buf[0]
    elif _sw4 == 2:
        if CopyBuffer(handle, 2, shift, 1, buf) > 0:
            return buf[0]
    elif _sw4 == 3:
        if CopyBuffer(handle, 3, shift, 1, buf) > 0:
            return buf[0]
    elif _sw4 == 4:
        if CopyBuffer(handle, 4, shift, 1, buf) > 0:
            return buf[0]
    else:
        pass
    return EMPTY_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalAdjustable(_MQL5Indicator):
    name = 'Fractal_adjustable'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'FractalPeriod': 5,  # Fractal period: 5 for built in fractal
        'PriceHigh': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=3),  # Price high
        'PriceLow': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=4),  # Price low
        'UpperArrowDisplacement': 0.2,  # Upper arrow displacement
        'LowerArrowDisplacement': 0.2,  # Lower arrow displacement
    }

