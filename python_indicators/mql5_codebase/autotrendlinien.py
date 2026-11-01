"""autotrendlinien — converted from MQL5: MQL5 Indicators/AutoTrendLinien/autotrendlinien.mq5

Copyright: Copyright © 2006, ANG3110@latchess.com; Link: ANG3110@latchess.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, ANG3110@latchess.com', 'link': 'ANG3110@latchess.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'autotrendlinien', 'source': 'MQL5 Indicators/AutoTrendLinien/autotrendlinien.mq5', 'folder': 'AutoTrendLinien', 'inputs': [{'mql': 'Hours', 'py': 'Hours', 'param': 'Hours', 'type': 'int', 'default': 24, 'label': 'Channel period in hours', 'sinput': False}, {'mql': 'UpChannelColor', 'py': 'UpChannelColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Upper line color', 'sinput': False}, {'mql': 'MdChannelColor', 'py': 'MdChannelColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Middle line color', 'sinput': False}, {'mql': 'DnChannelColor', 'py': 'DnChannelColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Lower line color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DodgerBlue = 0xFF901E  # MQL4 colour name
Gray = 0x808080  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# ---- inputs and global variables
Hours = _input('Hours', 24)  # Channel period in hours
min_rates_total = 0
lr = 0.0
lr0 = 0.0
lrp = 0.0
sx = 0.0
sy = 0.0
sxy = 0.0
sx2 = 0.0
aa = 0.0
bb = 0.0
hai = 0.0
lai = 0.0
dhi = 0.0
dli = 0.0
dhm = 0.0
dlm = 0.0
ha0 = 0.0
hap = 0.0
la0 = 0.0
lap = 0.0
price_p1 = 0.0
price_p0 = 0.0
price_p2 = 0.0
price_01 = 0.0
price_00 = 0.0
price_02 = 0.0
dh = 0.0
dl = 0.0
dh_1 = 0.0
dl_1 = 0.0
dh_2 = 0.0
dl_2 = 0.0
f = 0
f0 = 0
f1 = 0
p = 0
ai_1 = 0
ai_2 = 0
bi_1 = 0
bi_2 = 0
p1 = 0
p0 = 0
p2 = 0
fp = 0

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)

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
    global min_rates_total, p
    p = _idiv(Hours * 60 * 60, PeriodSeconds())
    min_rates_total = p + 1
    shortname = 'SAutoTrendLinien'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnDeinit(reason):
    ObjectDelete(0, 'Upper Line')
    ObjectDelete(0, 'Middle Line')
    ObjectDelete(0, 'Lower Line')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global aa, ai_1, ai_2, bb, bi_1, bi_2, dh, dh_1, dh_2, dhi, dhm, dl, dl_1, dl_2, dli, dlm, f, f1, fp, ha0, hai, hap, la0, lai, lap, lr, lr0, lrp, p, p0, p1, p2, price_00, price_01, price_02, price_p0, price_p1, price_p2, sx, sx2, sxy, sy
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    i = 0
    n = 0
    if f == 1:
        if prev_calculated <= 0:
            p1 = iBarShift_u(Symbol(), Period(), ObjectGetInteger(0, 'Upper Line', OBJPROP_TIME, 0))
            p0 = iBarShift_u(Symbol(), Period(), ObjectGetInteger(0, 'Middle Line', OBJPROP_TIME, 0))
            p2 = iBarShift_u(Symbol(), Period(), ObjectGetInteger(0, 'Lower Line', OBJPROP_TIME, 0))
        else:
            p1 = p
            p0 = p
            p2 = p
        if fp == 0 and p != p1:
            p = p1
            fp = 1
        if fp == 0 and p != p0:
            p = p0
            fp = 1
        if fp == 0 and p != p2:
            p = p2
            fp = 1
    sx = 0.0
    sy = 0.0
    sxy = 0.0
    sx2 = 0.0
    n = 0
    for n in range(n, p + 1):
        sx += n
        sy += _int(time[n])
        sxy += n * close[n]
        sx2 += MathPow(n, 2)
    else:
        n = _range_end(n, p + 1, 1)
    aa = _fdiv((sx * sy) - ((p + 1) * sxy), MathPow(sx, 2) - ((p + 1) * sx2))
    bb = _fdiv(sy - (aa * sx), p + 1)
    i = 0
    for i in range(i, p + 1):
        lr = bb + (aa * i)
        dh = high[i] - lr
        dl = low[i] - lr
        if i < _idiv(p, 2):
            if i == 0:
                dh_1 = 0.0
                dl_1 = 0.0
                ai_1 = i
                bi_1 = i
            if dh >= dh_1:
                dh_1 = dh
                ai_1 = i
            if dl <= dl_1:
                dl_1 = dl
                bi_1 = i
        if i >= _idiv(p, 2):
            if i == _idiv(p, 2):
                dh_2 = 0.0
                dl_2 = 0.0
                ai_2 = i
                bi_2 = i
            if dh >= dh_2:
                dh_2 = dh
                ai_2 = i
            if dl <= dl_2:
                dl_2 = dl
                bi_2 = i
    else:
        i = _range_end(i, p + 1, 1)
    lr0 = bb
    lrp = bb + (aa * (i + p))
    if MathAbs(ai_1 - ai_2) > MathAbs(bi_1 - bi_2):
        f = 1
    if MathAbs(ai_1 - ai_2) < MathAbs(bi_1 - bi_2):
        f = 2
    if MathAbs(ai_1 - ai_2) == MathAbs(bi_1 - bi_2):
        if MathAbs(dh_1 - dh_2) < MathAbs(dl_1 - dl_2):
            f = 1
        if MathAbs(dh_1 - dh_2) >= MathAbs(dl_1 - dl_2):
            f = 2
    if f == 1:
        n = 0
        for n in range(n, 20 + 1):
            f1 = 0
            i = 0
            for i in range(i, p + 1):
                hai = _fdiv(high[ai_1] * (i - ai_2), ai_1 - ai_2) + _fdiv(high[ai_2] * (i - ai_1), ai_2 - ai_1)
                if i == 0 or i == _idiv(p, 2):
                    dhm = 0.0
                if (high[i] - hai) > dhm and i < _idiv(p, 2):
                    ai_1 = i
                    f1 = 1
                if (high[i] - hai) > dhm and i >= _idiv(p, 2):
                    ai_2 = i
                    f1 = 1
            else:
                i = _range_end(i, p + 1, 1)
            if f == 0:
                break
        else:
            n = _range_end(n, 20 + 1, 1)
        i = 0
        for i in range(i, p + 1):
            hai = _fdiv(high[ai_1] * (i - ai_2), ai_1 - ai_2) + _fdiv(high[ai_2] * (i - ai_1), ai_2 - ai_1)
            dli = low[i] - hai
            if i == 0:
                dlm = 0.0
            if dli < dlm:
                dlm = dli
        else:
            i = _range_end(i, p + 1, 1)
        ha0 = _fdiv(high[ai_1] * (0 - ai_2), ai_1 - ai_2) + _fdiv(high[ai_2] * (0 - ai_1), ai_2 - ai_1)
        hap = _fdiv(high[ai_1] * (p - ai_2), ai_1 - ai_2) + _fdiv(high[ai_2] * (p - ai_1), ai_2 - ai_1)
        price_p1 = hap
        price_p0 = hap + (dlm / 2)
        price_p2 = hap + dlm
        price_01 = ha0
        price_00 = ha0 + (dlm / 2)
        price_02 = ha0 + dlm
    if f == 2:
        n = 0
        for n in range(n, 20 + 1):
            f1 = 0
            i = 0
            for i in range(i, p + 1):
                lai = _fdiv(low[bi_1] * (i - bi_2), bi_1 - bi_2) + _fdiv(low[bi_2] * (i - bi_1), bi_2 - bi_1)
                if i == 0 or i == _idiv(p, 2):
                    dlm = 0.0
                if (low[i] - lai) < dlm and i < _idiv(p, 2):
                    bi_1 = i
                    f1 = 1
                if (low[i] - lai) < dlm and i >= _idiv(p, 2):
                    bi_2 = i
                    f1 = 1
            else:
                i = _range_end(i, p + 1, 1)
            if f == 0:
                break
        else:
            n = _range_end(n, 20 + 1, 1)
        i = 0
        for i in range(i, p + 1):
            lai = _fdiv(low[bi_1] * (i - bi_2), bi_1 - bi_2) + _fdiv(low[bi_2] * (i - bi_1), bi_2 - bi_1)
            dhi = high[i] - lai
            if i == 0:
                dhm = 0.0
            if dhi > dhm:
                dhm = dhi
        else:
            i = _range_end(i, p + 1, 1)
        la0 = _fdiv(low[bi_1] * (0 - bi_2), bi_1 - bi_2) + _fdiv(low[bi_2] * (0 - bi_1), bi_2 - bi_1)
        lap = _fdiv(low[bi_1] * (p - bi_2), bi_1 - bi_2) + _fdiv(low[bi_2] * (p - bi_1), bi_2 - bi_1)
        price_p1 = lap
        price_p0 = lap + (dhm / 2)
        price_p2 = lap + dhm
        price_01 = la0
        price_00 = la0 + (dhm / 2)
        price_02 = la0 + dhm
    SetTline(0, 'Upper Line', 0, time[p], price_p1, time[0], price_01, UpChannelColor, STYLE_SOLID, 2, 'Upper Line')
    SetTline(0, 'Middle Line', 0, time[p], price_p0, time[0], price_00, MdChannelColor, STYLE_DOT, 1, 'Middle Line')
    SetTline(0, 'Lower Line', 0, time[p], price_p2, time[0], price_02, DnChannelColor, STYLE_SOLID, 2, 'Lower Line')
    f = 1
    p1 = p
    p0 = p
    p2 = p
    fp = 0
    return rates_total

# ---- global variables initialised from expressions
UpChannelColor = _input('UpChannelColor', _uint(DodgerBlue))  # Upper line color
MdChannelColor = _input('MdChannelColor', _uint(Gray))  # Middle line color
DnChannelColor = _input('DnChannelColor', _uint(Magenta))  # Lower line color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Autotrendlinien(_MQL5Indicator):
    name = 'autotrendlinien'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Hours': 24,  # Channel period in hours
    }

