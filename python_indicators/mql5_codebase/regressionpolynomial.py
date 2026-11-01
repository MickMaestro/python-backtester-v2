"""RegressionPolynomial — converted from MQL5: MQL5 Indicators/RegressionPolynomial/RegressionPolynomial.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [13959039, 15631086]}, 'widths': {}, 'styles': {}, 'labels': {1: 'RegressionPolynomial'}, 'levels': [], 'description': [], 'name': 'RegressionPolynomial', 'source': 'MQL5 Indicators/RegressionPolynomial/RegressionPolynomial.mq5', 'folder': 'RegressionPolynomial', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 55, 'label': 'Период мувинга', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 8, 'label': 'Глубина сглаживания сигнальной линии', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания сигнальной линии', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 6, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'degree', 'py': 'degree', 'param': 'degree', 'type': 'uint', 'default': 1, 'label': 'Алгоритм расчёта', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
period = _input('period', 55)  # Период мувинга
XMA_Method = _input('XMA_Method', MODE_SMA_)  # Метод усреднения сигнальной линии
XLength = _input('XLength', 8)  # Глубина сглаживания сигнальной линии
XPhase = _input('XPhase', 15)  # Параметр сглаживания сигнальной линии
IPC = _input('IPC', PRICE_TYPICAL)  # Ценовая константа
degree = _input('degree', 1)  # Алгоритм расчёта
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
min_rates_ = 0

def OnInit():
    global dPriceShift, min_rates_, min_rates_total
    min_rates_ = _int(period)
    min_rates_total = min_rates_ + GetStartBars(XMA_Method, XLength, XPhase)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'RegressionPolynomial(', XLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    sma = 0.0
    lwma = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        if degree != 1 and degree != 2:
            first = min_rates_
        else:
            first = 0
        sma = _s_OnCalculate_XMA2.XMASeries(0, prev_calculated, rates_total, MODE_SMA_, 0, period, 0.0, 0, False)
        lwma = _s_OnCalculate_XMA3.XMASeries(0, prev_calculated, rates_total, MODE_LWMA_, 0, period, 0.0, 0, False)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if degree == 1:
            price = PriceSeries(IPC, bar, open, low, high, close)
            sma = _s_OnCalculate_XMA2.XMASeries(0, prev_calculated, rates_total, MODE_SMA_, 0, period, price, bar, False)
            lwma = _s_OnCalculate_XMA3.XMASeries(0, prev_calculated, rates_total, MODE_LWMA_, 0, period, price, bar, False)
            UpBuffer[bar] = regression_LRMA(sma, lwma)
        elif degree == 2:
            price = PriceSeries(IPC, bar, open, low, high, close)
            sma = _s_OnCalculate_XMA2.XMASeries(0, prev_calculated, rates_total, MODE_SMA_, 0, period, price, bar, False)
            lwma = _s_OnCalculate_XMA3.XMASeries(0, prev_calculated, rates_total, MODE_LWMA_, 0, period, price, bar, False)
            if bar < min_rates_:
                continue
            UpBuffer[bar] = regression_QRMA(sma, lwma, period, bar, IPC, open, low, high, close)
        else:
            UpBuffer[bar] = regression_regressionPolynomial(bar, period, degree, IPC, open, low, high, close)
        DnBuffer[bar] = XMA1.XMASeries(min_rates_, prev_calculated, rates_total, XMA_Method, XPhase, XLength, UpBuffer[bar], bar, False) + dPriceShift
        UpBuffer[bar] += dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def regression_LRMA(Sma, Lwma):
    return (3 * Sma) - (2 * Lwma)

def regression_QRMA(Sma, Lwma, len_, shift, price, Open, Low, High, Close):
    qwma = ma_qwma(len_, shift, price, Open, Low, High, Close)
    value = (3.0 * Sma) + (qwma * (10 - _idiv(15, len_ + 2))) - (Lwma * (12 - _idiv(15, len_ + 2)))
    return value

def ma_qwma(len_, shift, price, Open, Low, High, Close):
    sum_ = 0.0
    j = 0
    i = 0
    j = shift
    i = 1
    while j > (shift - len_):
        sum_ += PriceSeries(price, j, Open, Low, High, Close) * MathPow(len_ - i + 1, 2)
        j -= 1
        i += 1
    value = _fdiv(6.0, len_ * (len_ + 1) * ((2 * len_) + 1))
    return value * sum_

def regression_regressionPolynomial(shift, len_, fdegree, price, Open, Low, High, Close):
    a = Arr(10, 0.0, dyn=False, dims=(10,))
    b = Arr(10, 0.0, dyn=False)
    x = Arr(10, 0.0, dyn=False)
    sx = Arr(20, 0.0, dyn=False)
    n = 0
    i = 0
    k = 0
    t = 0.0
    degree1 = 0
    ArrayInitialize(a, 0.0)
    ArrayInitialize(b, 0.0)
    sx[1] = len_ + 1
    degree1 = fdegree + 1
    i = 1
    for i in range(i, (degree1 * 2) - 2 + 1):
        sx[i + 1] = 0.0
        n = 0
        for n in range(n, len_ + 1):
            sx[i + 1] += MathPow(n, i)
        else:
            n = _range_end(n, len_ + 1, 1)
    else:
        i = _range_end(i, (degree1 * 2) - 2 + 1, 1)
    i = 1
    for i in range(i, degree1 + 1):
        b[i] = 0.0
        n = 0
        for n in range(n, len_ + 1):
            if i == 1:
                b[i] += PriceSeries(price, shift - n, Open, Low, High, Close)
            else:
                b[i] += PriceSeries(price, shift - n, Open, Low, High, Close) * MathPow(n, i - 1)
        else:
            n = _range_end(n, len_ + 1, 1)
    else:
        i = _range_end(i, degree1 + 1, 1)
    for j in range(1, degree1 + 1):
        i = 1
        for i in range(i, degree1 + 1):
            k = i + j - 1
            a[i][j] = sx[k]
        else:
            i = _range_end(i, degree1 + 1, 1)
    k = 1
    for k in range(k, degree1 - 1 + 1):
        l = 0
        mm = 0.0
        i = k
        for i in range(i, degree1 + 1):
            if MathAbs(a[i][k]) > mm:
                mm = MathAbs(a[i][k])
                l = i
        else:
            i = _range_end(i, degree1 + 1, 1)
        if not l:
            return 0.0
        if l != k:
            for j in range(1, degree1 + 1):
                t = a[(k, j)[-1]]
                a[k][j] = a[l][j]
                a[l][j] = t
            t = b[k]
            b[k] = b[l]
            b[l] = t
        div = 0.0
        i = k + 1
        for i in range(i, degree1 + 1):
            div = _fdiv(a[i][k], a[k][k])
            for j in range(1, degree1 + 1):
                if j == k:
                    a[i][j] = 0.0
                else:
                    a[i][j] = a[i][j] - (div * a[k][j])
            b[i] = b[i] - (div * b[k])
        else:
            i = _range_end(i, degree1 + 1, 1)
    else:
        k = _range_end(k, degree1 - 1 + 1, 1)
    x[degree1] = _fdiv(b[degree1], a[degree1][degree1])
    i = fdegree
    for i in range(i, 1 - 1, -1):
        t = 0.0
        for j in range(1, degree1 - i + 1):
            t = t + (a[i][i + j] * x[i + j])
            x[i] = _fdiv(1, a[i][i]) * (b[i] - t)
    else:
        i = _range_end(i, 1 - 1, -1)
    value = x[1]
    i = 1
    while k <= fdegree:
        value += x[i + 1] * MathPow(n, i)
        i += 1
    return value

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_OnCalculate_XMA2 = CXMA()
_s_OnCalculate_XMA3 = CXMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RegressionPolynomial(_MQL5Indicator):
    name = 'RegressionPolynomial'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 55,  # Период мувинга
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения сигнальной линии
        'XLength': 8,  # Глубина сглаживания сигнальной линии
        'XPhase': 15,  # Параметр сглаживания сигнальной линии
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=6),  # Ценовая константа
        'degree': 1,  # Алгоритм расчёта
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

