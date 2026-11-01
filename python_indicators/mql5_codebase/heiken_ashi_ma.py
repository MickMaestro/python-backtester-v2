"""Heiken_Ashi_MA — converted from MQL5: MQL5 Indicators/Moving Average based on Heiken-Ashi/Heiken_Ashi_MA.mq5

Moving Average based on Heiken-Ashi
Copyright: Copyright 2025, ProtimeTrader.; Link: https://www.mql5.com/en/users/protimetrader; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, ProtimeTrader.', 'link': 'https://www.mql5.com/en/users/protimetrader', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16748574, 255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Moving Average based on Heiken-Ashi'], 'name': 'Heiken_Ashi_MA', 'source': 'MQL5 Indicators/Moving Average based on Heiken-Ashi/Heiken_Ashi_MA.mq5', 'folder': 'Moving Average based on Heiken-Ashi', 'inputs': [{'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 0, 'label': 'Timeframe for Heiken Ashi calculation', 'sinput': False}, {'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'int', 'default': 13, 'label': 'Moving Average period', 'sinput': False}, {'mql': 'InpMAShift', 'py': 'InpMAShift', 'param': 'InpMAShift', 'type': 'int', 'default': 0, 'label': 'MA shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 2, 'label': 'MA method', 'sinput': False}, {'mql': 'InpMAAppliedPrice', 'py': 'InpMAAppliedPrice', 'param': 'InpMAAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Source price for MA', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTimeframe = _input('InpTimeframe', PERIOD_CURRENT)  # Timeframe for Heiken Ashi calculation
InpMAPeriod = _input('InpMAPeriod', 13)  # Moving Average period
InpMAShift = _input('InpMAShift', 0)  # MA shift
InpMAMethod = _input('InpMAMethod', MODE_SMMA)  # MA method
InpMAAppliedPrice = _input('InpMAAppliedPrice', PRICE_CLOSE)  # Source price for MA
ExtLineBuffer = Arr(0, 0.0)  # Buffer 0: MA values
ExtLineColorBuffer = Arr(0, 0.0)  # Buffer 1: Color index
ExtPriceBuffer = Arr(0, 0.0)  # Buffer 2: Source price from Heiken Ashi
ExtHAOpenPriceBuffer = Arr(0, 0.0)
ExtHAHighPriceBuffer = Arr(0, 0.0)
ExtHALowPriceBuffer = Arr(0, 0.0)
ExtHAClosePriceBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtPriceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtHAOpenPriceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtHAHighPriceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtHALowPriceBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtHAClosePriceBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpMAPeriod)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpMAShift)
    short_name = ""
    _sw1 = InpMAMethod
    if _sw1 == MODE_EMA:
        short_name = 'EMA'
    elif _sw1 == MODE_LWMA:
        short_name = 'LWMA'
    elif _sw1 == MODE_SMA:
        short_name = 'SMA'
    elif _sw1 == MODE_SMMA:
        short_name = 'SMMA'
    else:
        short_name = 'unknown'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + '(' + _str(InpMAPeriod) + ')')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (InpMAPeriod - 1 + begin):
        warn_msg = 'Not enough bars to calculate Heiken Ashi MA (need at least ' + IntegerToString(InpMAPeriod) + ' bars)'
        Comment(warn_msg)
        Print(warn_msg)
        return 0
    else:
        Comment('')
    start = (0 if (prev_calculated == 0) else 1)
    if prev_calculated == 0:
        last = rates_total - 1
        ExtHAOpenPriceBuffer[last] = iOpen(Symbol(), InpTimeframe, start)
        ExtHAClosePriceBuffer[last] = iClose(Symbol(), InpTimeframe, start)
        ExtHAHighPriceBuffer[last] = iHigh(Symbol(), InpTimeframe, start)
        ExtHALowPriceBuffer[last] = iLow(Symbol(), InpTimeframe, start)
    for i in range(start, rates_total):
        CalculateHeikenAshi(rates_total, i)
    for i in range(start, rates_total):
        _sw2 = InpMAAppliedPrice
        if _sw2 == PRICE_OPEN:
            ExtPriceBuffer[i] = ExtHAOpenPriceBuffer[i]
        elif _sw2 == PRICE_HIGH:
            ExtPriceBuffer[i] = ExtHAHighPriceBuffer[i]
        elif _sw2 == PRICE_LOW:
            ExtPriceBuffer[i] = ExtHALowPriceBuffer[i]
        elif _sw2 == PRICE_MEDIAN:
            ExtPriceBuffer[i] = (ExtHAHighPriceBuffer[i] + ExtHALowPriceBuffer[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            ExtPriceBuffer[i] = (ExtHAHighPriceBuffer[i] + ExtHALowPriceBuffer[i] + ExtHAClosePriceBuffer[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            ExtPriceBuffer[i] = (ExtHAHighPriceBuffer[i] + ExtHALowPriceBuffer[i] + ExtHAClosePriceBuffer[i] + ExtHAClosePriceBuffer[i]) / 4.0
        else:
            ExtPriceBuffer[i] = ExtHAClosePriceBuffer[i]
    _sw3 = InpMAMethod
    if _sw3 == MODE_EMA:
        CalculateEMA(rates_total, prev_calculated, begin, ExtPriceBuffer)
    elif _sw3 == MODE_LWMA:
        CalculateLWMA(rates_total, prev_calculated, begin, ExtPriceBuffer)
    elif _sw3 == MODE_SMA:
        CalculateSimpleMA(rates_total, prev_calculated, begin, ExtPriceBuffer)
    elif _sw3 == MODE_SMMA:
        CalculateSmoothedMA(rates_total, prev_calculated, begin, ExtPriceBuffer)
    return rates_total

def CalculateHeikenAshi(total, ind):
    i = ind
    o = iOpen(Symbol(), InpTimeframe, total - i - 1)
    h = iHigh(Symbol(), InpTimeframe, total - i - 1)
    l = iLow(Symbol(), InpTimeframe, total - i - 1)
    c = iClose(Symbol(), InpTimeframe, total - i - 1)
    ha_close = (o + h + l + c) / 4.0
    ha_open = (((ExtHAOpenPriceBuffer[i - 1] + ExtHAClosePriceBuffer[i - 1]) / 2.0) if (i > 0) else ((o + c) / 2.0))
    ha_high = MathMax(h, MathMax(ha_open, ha_close))
    ha_low = MathMin(l, MathMin(ha_open, ha_close))
    ExtHAOpenPriceBuffer[i] = ha_open
    ExtHAClosePriceBuffer[i] = ha_close
    ExtHAHighPriceBuffer[i] = ha_high
    ExtHALowPriceBuffer[i] = ha_low
    ExtLineColorBuffer[i] = (0.0 if (ha_close > ha_open) else 1.0)

def CalculateSimpleMA(rates_total, prev_calculated, begin, price):
    start = (InpMAPeriod if (prev_calculated == 0) else (prev_calculated - 1))
    for i in range(start, rates_total):
        sum_ = 0.0
        for j in range(0, InpMAPeriod):
            sum_ += price[i - j]
        ExtLineBuffer[i] = sum_ / InpMAPeriod

def CalculateEMA(rates_total, prev_calculated, begin, price):
    k = _fdiv(2.0, InpMAPeriod + 1.0)
    start = (InpMAPeriod if (prev_calculated == 0) else (prev_calculated - 1))
    if prev_calculated == 0:
        ExtLineBuffer[InpMAPeriod - 1] = price[InpMAPeriod - 1]
    for i in range(start, rates_total):
        ExtLineBuffer[i] = (price[i] * k) + (ExtLineBuffer[i - 1] * (1 - k))

def CalculateLWMA(rates_total, prev_calculated, begin, price):
    weight_sum = _idiv(InpMAPeriod * (InpMAPeriod + 1), 2)
    start = (InpMAPeriod if (prev_calculated == 0) else (prev_calculated - 1))
    for i in range(start, rates_total):
        sum_ = 0.0
        for j in range(0, InpMAPeriod):
            sum_ += price[i - j] * (InpMAPeriod - j)
        ExtLineBuffer[i] = _fdiv(sum_, weight_sum)

def CalculateSmoothedMA(rates_total, prev_calculated, begin, price):
    start = (InpMAPeriod if (prev_calculated == 0) else (prev_calculated - 1))
    if prev_calculated == 0:
        sum_ = 0.0
        for i in range(0, InpMAPeriod):
            sum_ += price[i]
        ExtLineBuffer[InpMAPeriod - 1] = sum_ / InpMAPeriod
        start = InpMAPeriod
    for i in range(start, rates_total):
        ExtLineBuffer[i] = ((ExtLineBuffer[i - 1] * (InpMAPeriod - 1)) + price[i]) / InpMAPeriod


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikenAshiMA(_MQL5Indicator):
    name = 'Heiken_Ashi_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe for Heiken Ashi calculation
        'InpMAPeriod': 13,  # Moving Average period
        'InpMAShift': 0,  # MA shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # MA method
        'InpMAAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Source price for MA
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

