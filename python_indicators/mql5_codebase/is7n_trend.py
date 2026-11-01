"""is7n_trend — converted from MQL5: MQL5 Indicators/iS7N_TREND.mq5/is7n_trend.mq5

Copyright: Copyright 2010, SHOOTER777; Link: s7n@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, SHOOTER777', 'link': 's7n@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [9109504, 15128749]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'iTREND'}, 'levels': [], 'description': [], 'name': 'is7n_trend', 'source': 'MQL5 Indicators/iS7N_TREND.mq5/is7n_trend.mq5', 'folder': 'iS7N_TREND.mq5', 'inputs': [{'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 20, 'label': 'indicator period', 'sinput': False}, {'mql': 'eC', 'py': 'eC', 'param': 'eC', 'type': 'int', 'default': 1, 'label': 'color scheme', 'sinput': False}, {'mql': 'Up', 'py': 'Up', 'param': None, 'type': 'color', 'default': 0, 'label': 'bull color (uptrend)', 'sinput': False}, {'mql': 'Down', 'py': 'Down', 'param': None, 'type': 'color', 'default': 0, 'label': 'bear color (downtrend)', 'sinput': False}, {'mql': 'iMax', 'py': 'iMax', 'param': 'iMax', 'type': 'int', 'default': 200, 'label': 'calc and plot iMx bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkBlue = 0x8B0000  # MQL4 colour name
LightBlue = 0xE6D8AD  # MQL4 colour name

# enum eColor
one_color_indicator = 0
two_color_indicator = 1
_enum('eColor', {0: 'one_color_indicator', 1: 'two_color_indicator'})

# ---- inputs and global variables
Per = _input('Per', 20)  # indicator period
eC = _input('eC', 1)  # color scheme
iMax = _input('iMax', 200)  # calc and plot iMx bars
dPlot = Arr(0, 0.0)
dColor = Arr(0, 0.0)
dBuf_I = Arr(0, 0.0)
dBuf_1 = Arr(0, 0.0)
dBuf_2 = Arr(0, 0.0)
ihMA_1 = 0
ihMA_2 = 0
P0 = 0
P2 = 0
P4 = 0
iMx = 0
limit = 0
sShNm = ""

def OnInit():
    global iMx
    iPer = StringConcatenate(_GlobRef(globals(), 'sShNm'), 'iS7N_TREND( ', Per, ' )')
    iBars_ = Bars(Symbol(), Period())
    iMx = iMax
    Print(' Total ', iBars_, ' bars in the history are available')
    SetIndexBuffer(0, dPlot, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'TREND')
    ArraySetAsSeries(dPlot, True)
    SetIndexBuffer(1, dColor, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(dColor, True)
    SetIndexBuffer(2, dBuf_I, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(dBuf_I, True)
    ArraySetAsSeries(dBuf_1, True)
    ArraySetAsSeries(dBuf_2, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, sShNm)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, Up)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Down)
    if eC == 0:
        Print('One color mode is selected')
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Up)
    else:
        Print('Two-color mode is selected')
    vInPr()
    if not vInHandl():
        Print('???There was an error in initialization???')
        Print('Error  №', GetLastError())
        return -1
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    global iMx, limit
    if prev_calculated <= 0:
        for i in range(0, rates_total - 1 + 1):
            dPlot[i] = EMPTY_VALUE
    iMn = 10 * P0
    if iMn > rates_total:
        return 0
    if iMn > iMx:
        iMx = iMn
    if iMx > rates_total:
        iMx = rates_total
    iii = 0
    preMx = 1
    if prev_calculated <= 0:
        limit = iMx
        Print('The indicator will be calculated for the ', limit - P0, ' last bars')
        Print('After that, the indicator will be calculated for the ', P0 + preMx, ' last bars')
    else:
        limit = P0 + preMx
    ArrayResize(dBuf_1, limit)
    ArrayResize(dBuf_2, limit)
    if not vCopy():
        return 0
    iii = 0
    for iii in range(iii, limit):
        dBuf_I[iii] = (2.0 * dBuf_2[iii]) - dBuf_1[iii]
    else:
        iii = _range_end(iii, limit, 1)
    ArrayResize(dBuf_I, limit)
    iii = 0
    while iii < (limit - P0):
        dPlot[iii] = iLWMA(dBuf_I, P4, iii)
        iii += 1
    iii = 0
    for iii in range(iii, limit - P0):
        if dPlot[iii] > dPlot[iii + 1]:
            dColor[iii] = 0.0
        else:
            dColor[iii] = 1.0
    else:
        iii = _range_end(iii, limit - P0, 1)
    ChartRedraw()
    return rates_total

def vInPr():
    global P0, P2, P4
    P0 = Per
    P2 = _idiv(Per, 2)
    P4 = _int(MathSqrt(Per))

def vInHandl():
    global ihMA_1, ihMA_2
    Print('Get the indicator handles for the iS7N_TREND indicator')
    ihMA_1 = iMA(Symbol(), 0, P0, 0, MODE_EMA, PRICE_CLOSE)
    ihMA_2 = iMA(Symbol(), 0, P2, 0, MODE_EMA, PRICE_CLOSE)
    if ihMA_1 < 0 or ihMA_1 < 0:
        Print(' Error creating indicators')
        return False
    else:
        Print('The handles has been initialized successfully')
        Print('The main      : Period = ', P0, '   Handle =', ihMA_1)
        Print('The secondary : Period = ', P2, '   Handle =', ihMA_2)
        return True

def vCopy():
    n1 = 0
    n2 = 0
    n1 = CopyBuffer(ihMA_1, 0, 0, limit, dBuf_1)
    n2 = CopyBuffer(ihMA_2, 0, 0, limit, dBuf_2)
    if n1 == -1 or n2 == -1:
        Print('Error in call of the CopyBuffer function, error №=', GetLastError())
        return False
    else:
        return True

def iLWMA(array, period, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period):
        return 0.0
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
    return buf[shift]

# ---- global variables initialised from expressions
Up = _input('Up', _uint(DarkBlue))  # bull color (uptrend)
Down = _input('Down', _uint(LightBlue))  # bear color (downtrend)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Is7nTrend(_MQL5Indicator):
    name = 'is7n_trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Per': 20,  # indicator period
        'eC': _Choice({0: 'one_color_indicator', 1: 'two_color_indicator'}, default=1),  # color scheme
        'iMax': 200,  # calc and plot iMx bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

