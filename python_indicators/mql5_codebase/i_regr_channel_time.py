"""i-regr_channel_time — converted from MQL5: MQL5 Indicators/i-Regression Channel/i-regr_channel_time.mq5

Copyright: Copyright © 2009, kharko; Version: 1.40

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, kharko', 'link': '', 'version': '1.40', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [65280], 2: [16711935], 3: [8421504]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'i-Regression Channel Up', 2: 'i-Regression Channel Down', 4: 'i-Regression Channel Middle'}, 'levels': [], 'description': [], 'name': 'i-regr_channel_time', 'source': 'MQL5 Indicators/i-Regression Channel/i-regr_channel_time.mq5', 'folder': 'i-Regression Channel', 'inputs': [{'mql': 'degree', 'py': 'degree', 'param': 'degree', 'type': 'int', 'default': 1, 'label': 'Regression degree (changes from 1 to 61)', 'sinput': False}, {'mql': 'kstd', 'py': 'kstd', 'param': 'kstd', 'type': 'double', 'default': 1.0, 'label': 'Channel width', 'sinput': False}, {'mql': 'data', 'py': 'data', 'param': None, 'type': 'datetime', 'default': 0, 'label': 'Channel calculation start date', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'shift', 'py': 'shift', 'param': 'shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the channel', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
degree = _input('degree', 1)  # Regression degree (changes from 1 to 61)
kstd = _input('kstd', 1.0)  # Channel width
data = _input('data', StringToInteger('2009.02.25 16:00'))  # Channel calculation start date
Applied_price = _input('Applied_price', PRICE_CLOSE)  # Applied price
shift = _input('shift', 0)  # Horizontal shift of the channel
FxBuffer = Arr(0, 0.0)
SqhBuffer = Arr(0, 0.0)
SqlBuffer = Arr(0, 0.0)
ai = Arr(0, 0.0, dims=(65,))
b = Arr(0, 0.0)
c = Arr(0, 0.0)
x = Arr(0, 0.0)
y = Arr(0, 0.0)
sx = Arr(0, 0.0)
qq = 0.0
mm = 0.0
tt = 0.0
sq = 0.0
sum_ = 0.0
ip = 0
p = 0
n = 0
f = 0
ii = 0
jj = 0
kk = 0
ll = 0
nn = 0
i0 = 0
limit = 0
min_rates_total = 0

def iBarShift_u(symbol, timeframe, time):
    if time < 0:
        return -1
    Arr_ = Arr(0, 0)
    time1 = 0
    time1 = SeriesInfoInteger(symbol, timeframe, SERIES_LASTBAR_DATE)
    if CopyTime(symbol, timeframe, _DT(time), _DT(time1), Arr_) > 0:
        size = ArraySize(Arr_)
        return size - 1
    else:
        return -1

def OnInit():
    global min_rates_total
    min_rates_total = 1
    ArrayResize(ai, degree + 2)
    ArrayResize(b, degree + 2)
    ArrayResize(c, degree + 2)
    ArrayResize(x, degree + 2)
    ArrayResize(y, degree + 2)
    ArrayResize(sx, 2 * (degree + 3))
    SetIndexBuffer(0, SqhBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_SHIFT, shift)
    ArraySetAsSeries(SqhBuffer, True)
    SetIndexBuffer(1, SqlBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_SHIFT, shift)
    ArraySetAsSeries(SqlBuffer, True)
    SetIndexBuffer(2, FxBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_SHIFT, shift)
    ArraySetAsSeries(FxBuffer, True)
    shortname = 'i-Regr Channel'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ii, ip, jj, kk, limit, ll, min_rates_total, mm, n, nn, p, qq, sq, sum_, tt
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    if rates_total == prev_calculated:
        return rates_total
    else:
        min_rates_total = iBarShift_u(Symbol(), PERIOD_CURRENT, data) + 1
        if not min_rates_total:
            min_rates_total = rates_total
        limit = min_rates_total - 1
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    mi = 0
    ip = limit
    p = ip
    sx[1] = p + 1
    nn = degree + 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - p - 1)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - p - 1)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, rates_total - p - 1)
    mi = 1
    for mi in range(mi, (nn * 2) - 2 + 1):
        sum_ = 0.0
        n = i0
        while n <= (i0 + p):
            sum_ += MathPow(n, mi)
            n += 1
        sx[mi + 1] = sum_
    else:
        mi = _range_end(mi, (nn * 2) - 2 + 1, 1)
    mi = 1
    while mi <= nn:
        sum_ = 0.0
        n = i0
        while n <= (i0 + p):
            if mi == 1:
                sum_ += PriceSeries(Applied_price, n, open, low, high, close)
            else:
                sum_ += PriceSeries(Applied_price, n, open, low, high, close) * MathPow(n, mi - 1)
            n += 1
        b[mi] = sum_
        mi += 1
    jj = 1
    while jj <= nn:
        ii = 1
        while ii <= nn:
            kk = ii + jj - 1
            ai[ii][jj] = sx[kk]
            ii += 1
        jj += 1
    kk = 1
    while kk <= (nn - 1):
        ll = 0
        mm = 0.0
        ii = kk
        while ii <= nn:
            if MathAbs(ai[ii][kk]) > mm:
                mm = MathAbs(ai[ii][kk])
                ll = ii
            ii += 1
        if ll == 0:
            return 0
        if ll != kk:
            jj = 1
            while jj <= nn:
                tt = ai[kk][jj]
                ai[kk][jj] = ai[ll][jj]
                ai[ll][jj] = tt
                jj += 1
            tt = b[kk]
            b[kk] = b[ll]
            b[ll] = tt
        ii = kk + 1
        while ii <= nn:
            qq = _fdiv(ai[ii][kk], ai[kk][kk])
            jj = 1
            while jj <= nn:
                if jj == kk:
                    ai[ii][jj] = 0.0
                else:
                    ai[ii][jj] = ai[ii][jj] - (qq * ai[kk][jj])
                jj += 1
            b[ii] = b[ii] - (qq * b[kk])
            ii += 1
        kk += 1
    x[nn] = _fdiv(b[nn], ai[nn][nn])
    ii = nn - 1
    while ii >= 1:
        tt = 0.0
        jj = 1
        while jj <= (nn - ii):
            tt = tt + (ai[ii][ii + jj] * x[ii + jj])
            x[ii] = _fdiv(1, ai[ii][ii]) * (b[ii] - tt)
            jj += 1
        ii -= 1
    n = i0
    while n <= (i0 + p):
        sum_ = 0.0
        kk = 1
        while kk <= degree:
            sum_ += x[kk + 1] * MathPow(n, kk)
            kk += 1
        FxBuffer[n] = x[1] + sum_
        n += 1
    sq = 0.0
    n = i0
    while n <= (i0 + p):
        sq += MathPow(PriceSeries(Applied_price, n, open, low, high, close) - FxBuffer[n], 2)
        n += 1
    sq = MathSqrt(_fdiv(sq, p + 1)) * kstd
    n = i0 + p
    while n <= (rates_total - 1):
        FxBuffer[n] = 0.0
        SqhBuffer[n] = 0.0
        SqlBuffer[n] = 0.0
        n += 1
    n = i0
    while n <= (i0 + p):
        if FxBuffer[n]:
            SqhBuffer[n] = FxBuffer[n] + sq
            SqlBuffer[n] = FxBuffer[n] - sq
        else:
            SqhBuffer[n] = 0.0
            SqlBuffer[n] = 0.0
        n += 1
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IRegrChannelTime(_MQL5Indicator):
    name = 'i-regr_channel_time'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'degree': 1,  # Regression degree (changes from 1 to 61)
        'kstd': 1.0,  # Channel width
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Applied price
        'shift': 0,  # Horizontal shift of the channel
    }

