"""is7n_trend_1 — converted from MQL5: MQL5 Indicators/iS7N_TREND_1/is7n_trend_1.mq5

Copyright: Copyright 2010, SHOOTER777; Link: s7n@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, SHOOTER777', 'link': 's7n@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9109504]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'iTREND_1'}, 'levels': [], 'description': [], 'name': 'is7n_trend_1', 'source': 'MQL5 Indicators/iS7N_TREND_1/is7n_trend_1.mq5', 'folder': 'iS7N_TREND_1', 'inputs': [{'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Per = _input('Per', 14)
iMx = 300  # max bars to calculate
dPlot = Arr(0, 0.0)
dBuf_1 = Arr(0, 0.0)
dBuf_2 = Arr(0, 0.0)
dBuf_3 = Arr(0, 0.0)
dBuf_4 = Arr(0, 0.0)
ihMA_1 = 0
ihMA_2 = 0
P0 = 0
P2 = 0
P4 = 0
iIndCnt = 0
iBufCnt = 0
iRT = 0
iPC = 0
limit = 0
sShNm = ""
eee = 0.0

def OnInit():
    global ihMA_1, ihMA_2
    iPer = StringConcatenate(_GlobRef(globals(), 'sShNm'), 'iS7N_TREND_1( ', Per, ' )')
    iBars_ = Bars(Symbol(), Period())
    SetIndexBuffer(0, dPlot, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'TREND_1')
    SetIndexBuffer(1, dBuf_1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, dBuf_2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, dBuf_3, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, sShNm)
    vInPr()
    ihMA_1 = iMA(Symbol(), 0, P0, 0, MODE_EMA, PRICE_CLOSE)
    ihMA_2 = iMA(Symbol(), 0, P2, 0, MODE_EMA, PRICE_CLOSE)
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    global iBufCnt, iMx, limit
    if prev_calculated <= 0:
        for i in range(0, rates_total - 1 + 1):
            dPlot[i] = EMPTY_VALUE
            dBuf_1[i] = EMPTY_VALUE
            dBuf_2[i] = EMPTY_VALUE
            dBuf_3[i] = EMPTY_VALUE
    iMn = 10 * P0
    if iMn > rates_total:
        return 0
    if iMn > iMx:
        iMx = iMn
    if iMx > rates_total:
        iMx = rates_total
    limP0 = 0
    preMx = 1
    if prev_calculated <= 0:
        limit = rates_total - iMx
        limP0 = limit + P0
    else:
        limit = prev_calculated - preMx
        limP0 = limit
    iBufCnt = limit - 1
    ArrayResize(dBuf_4, P0)
    vInt()
    for iii in range(limit, rates_total - 1 + 1):
        dBuf_3[iii] = (2.0 * dBuf_2[iii]) - dBuf_1[iii]
    for iii in range(limP0, rates_total - 1 + 1):
        ArrayCopy(dBuf_4, dBuf_3, 0, iii, P0)
        dPlot[iii] = iMAOnArrayMQL4(dBuf_4, 0, P2, 0, 3, 0)
    return rates_total

def vInPr():
    global P0, P2, P4
    P0 = Per
    P2 = _idiv(Per, 2)
    P4 = _int(MathSqrt(Per))

def vInt():
    n1 = 0
    n2 = 0
    n1 = CopyBuffer(ihMA_1, 0, 0, iBufCnt + 1, dBuf_1)
    n2 = CopyBuffer(ihMA_2, 0, 0, iBufCnt + 1, dBuf_2)

def iMAOnArrayMQL4(array, total, period, ma_shift, ma_method, shift):
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


class Is7nTrend1(_MQL5Indicator):
    name = 'is7n_trend_1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Per': 14,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

