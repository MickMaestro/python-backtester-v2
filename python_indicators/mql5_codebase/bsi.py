"""BSI — converted from MQL5: MQL5 Indicators/BSI Trend and Channel/BSI.mq5

Copyright: Copyright 2022, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 14, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 5, 7: 5, 8: 1}, 'colors': {1: [42495], 2: [8421504], 3: [16776960], 4: [9639167], 5: [13828244], 6: [255], 7: [16711680], 8: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 2, 8: 1}, 'styles': {1: 1, 2: 2, 3: 1, 4: 0, 5: 0, 8: 2}, 'labels': {1: 'Trend High', 2: 'Trend Regr', 3: 'Trend Low', 4: 'Tango Line', 5: 'Tango MA', 6: 'Reversal Bar', 7: 'Reversal Bar', 8: 'BSI'}, 'levels': [], 'description': [], 'name': 'BSI', 'source': 'MQL5 Indicators/BSI Trend and Channel/BSI.mq5', 'folder': 'BSI Trend and Channel', 'inputs': [{'mql': 'InpChannelPeriod', 'py': 'InpChannelPeriod', 'param': 'InpChannelPeriod', 'type': 'int', 'default': 30, 'label': 'Channel Period', 'sinput': False}, {'mql': 'InpTrendPeriod', 'py': 'InpTrendPeriod', 'param': 'InpTrendPeriod', 'type': 'int', 'default': 30, 'label': 'Trend Period', 'sinput': False}, {'mql': 'InpReversalNoiseFilter', 'py': 'InpReversalNoiseFilter', 'param': 'InpReversalNoiseFilter', 'type': 'double', 'default': 5.0, 'label': 'NoiseFilter (Minimam Reversal Spread)', 'sinput': False}, {'mql': 'InpUsingVolumeWeight', 'py': 'InpUsingVolumeWeight', 'param': 'InpUsingVolumeWeight', 'type': 'bool', 'default': True, 'label': 'UseingVolumeWeight', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpChannelPeriod = _input('InpChannelPeriod', 30)  # Channel Period
InpTrendPeriod = _input('InpTrendPeriod', 30)  # Trend Period
InpReversalNoiseFilter = _input('InpReversalNoiseFilter', 5.0)  # NoiseFilter (Minimam Reversal Spread)
InpUsingVolumeWeight = _input('InpUsingVolumeWeight', True)  # UseingVolumeWeight
min_rates_total = 0
UpTrendBuffer = Arr(0, 0.0)
LoTrendBuffer = Arr(0, 0.0)
MdTrendBuffer = Arr(0, 0.0)
TangoBuffer = Arr(0, 0.0)
TangoMaBuffer = Arr(0, 0.0)
TopBuffer = Arr(0, 0.0)
BtmBuffer = Arr(0, 0.0)
SlopeBuffer = Arr(0, 0.0)
BSIBuffer = Arr(0, 0.0)
HighesBuffer = Arr(0, 0.0)
LowesBuffer = Arr(0, 0.0)
VolBuffer = Arr(0, 0.0)
UpRangeBuffer = Arr(0, 0.0)
DnRangeBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 1 + MathMax(InpTrendPeriod, InpChannelPeriod) + 1
    SetIndexBuffer(0, UpTrendBuffer)
    SetIndexBuffer(1, MdTrendBuffer)
    SetIndexBuffer(2, LoTrendBuffer)
    SetIndexBuffer(3, TangoBuffer)
    SetIndexBuffer(4, TangoMaBuffer)
    SetIndexBuffer(5, TopBuffer)
    SetIndexBuffer(6, BtmBuffer)
    SetIndexBuffer(7, BSIBuffer)
    SetIndexBuffer(8, HighesBuffer)
    SetIndexBuffer(9, LowesBuffer)
    SetIndexBuffer(10, SlopeBuffer)
    SetIndexBuffer(11, UpRangeBuffer)
    SetIndexBuffer(12, DnRangeBuffer)
    SetIndexBuffer(13, VolBuffer)
    PlotIndexSetInteger(5, PLOT_ARROW, 159)
    PlotIndexSetInteger(6, PLOT_ARROW, 159)
    PlotIndexSetInteger(0, PLOT_SHIFT, 1)
    PlotIndexSetInteger(1, PLOT_SHIFT, 1)
    PlotIndexSetInteger(2, PLOT_SHIFT, 1)
    PlotIndexSetInteger(3, PLOT_SHIFT, 1)
    PlotIndexSetInteger(4, PLOT_SHIFT, 1)
    PlotIndexSetInteger(7, PLOT_SHIFT, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    j = 0
    k = 0
    first = 0
    if rates_total <= min_rates_total:
        return 0
    ArraySetAsSeries(UpTrendBuffer, False)
    ArraySetAsSeries(MdTrendBuffer, False)
    ArraySetAsSeries(LoTrendBuffer, False)
    ArraySetAsSeries(TangoBuffer, False)
    ArraySetAsSeries(TangoMaBuffer, False)
    ArraySetAsSeries(TopBuffer, False)
    ArraySetAsSeries(BtmBuffer, False)
    ArraySetAsSeries(BSIBuffer, False)
    ArraySetAsSeries(HighesBuffer, False)
    ArraySetAsSeries(LowesBuffer, False)
    ArraySetAsSeries(UpRangeBuffer, False)
    ArraySetAsSeries(DnRangeBuffer, False)
    ArraySetAsSeries(SlopeBuffer, False)
    ArraySetAsSeries(VolBuffer, False)
    ArraySetAsSeries(time, False)
    ArraySetAsSeries(high, False)
    ArraySetAsSeries(low, False)
    ArraySetAsSeries(close, False)
    ArraySetAsSeries(tick_volume, False)
    first = InpChannelPeriod - 1
    if (first + 1) < prev_calculated:
        first = prev_calculated - 2
    else:
        i = 0
        for i in range(i, first):
            LowesBuffer[i] = 0.0
            HighesBuffer[i] = 0.0
            VolBuffer[i] = 0.0
        else:
            i = _range_end(i, first, 1)
    i = first
    for i in range(i, rates_total):
        dmin = 1000000.0
        dmax = -1000000.0
        volmax = 0
        k = i - InpChannelPeriod + 1
        for k in range(k, i + 1):
            if dmin > low[k]:
                dmin = low[k]
            if dmax < high[k]:
                dmax = high[k]
            if InpUsingVolumeWeight and volmax < tick_volume[k]:
                volmax = tick_volume[k]
        else:
            k = _range_end(k, i + 1, 1)
        LowesBuffer[i] = dmin
        HighesBuffer[i] = dmax
        if InpUsingVolumeWeight:
            VolBuffer[i] = float(volmax)
    else:
        i = _range_end(i, rates_total, 1)
    first = InpChannelPeriod - 1
    if (first + 1) < prev_calculated:
        first = prev_calculated - 2
    i = first
    for i in range(i, rates_total):
        btm_pos = 0
        top_pos = 0
        j = i - 1
        for j in range(j, 1, -1):
            if (LowesBuffer[j - 2] - (RevNoiseFilter * Point())) > LowesBuffer[j - 1] and LowesBuffer[j - 1] == LowesBuffer[j]:
                btm_pos = j - 1
                BtmBuffer[btm_pos] = LowesBuffer[btm_pos]
                break
            if (HighesBuffer[j - 2] + (RevNoiseFilter * Point())) < HighesBuffer[j - 1] and HighesBuffer[j - 1] == HighesBuffer[j]:
                top_pos = j - 1
                TopBuffer[top_pos] = HighesBuffer[top_pos]
                break
        else:
            j = _range_end(j, 1, -1)
        turn_pos = 0
        if btm_pos != 0 or top_pos != 0:
            if btm_pos != 0:
                turn_pos = btm_pos
            else:
                turn_pos = top_pos
            range_lo = 1000000.0
            range_hi = -1000000.0
            j = turn_pos
            for j in range(j, i - 1 + 1):
                if range_hi < high[j]:
                    range_hi = high[j]
                if range_lo > low[j]:
                    range_lo = low[j]
            else:
                j = _range_end(j, i - 1 + 1, 1)
            prev_high = MathMax(MathMax(MathMax(high[turn_pos - 4], high[turn_pos - 3]), high[turn_pos - 2]), high[turn_pos - 1])
            prev_low = MathMin(MathMin(MathMin(low[turn_pos - 4], low[turn_pos - 3]), low[turn_pos - 2]), low[turn_pos - 1])
            UpRangeBuffer[i] = MathMax(range_hi, prev_high)
            TangoBuffer[i] = (range_hi + range_lo) / 2
            DnRangeBuffer[i] = MathMin(range_lo, prev_low)
    else:
        i = _range_end(i, rates_total, 1)
    MaPeriod = _int(MathRound(_idiv(InpChannelPeriod, 2)))
    first = InpChannelPeriod - 1 + MaPeriod - 1
    if (first + 1) < prev_calculated:
        first = prev_calculated - 2
    else:
        i = 0
        for i in range(i, first):
            TangoMaBuffer[i] = EMPTY_VALUE
        else:
            i = _range_end(i, first, 1)
    i = first
    for i in range(i, rates_total):
        sum_ = 0.0
        k = i - MaPeriod + 1
        for k in range(k, i + 1):
            sum_ += TangoBuffer[k]
        else:
            k = _range_end(k, i + 1, 1)
        TangoMaBuffer[i] = _fdiv(sum_, MaPeriod)
        BSIBuffer[i] = calc_bsi(high, low, close, tick_volume, i, InpChannelPeriod)
    else:
        i = _range_end(i, rates_total, 1)
    first = min_rates_total - 1
    if (first + 1) < prev_calculated:
        first = prev_calculated - 2
    i = first
    for i in range(i, rates_total):
        is_update = False
        ma1 = TangoMaBuffer[i - 1]
        ma2 = TangoMaBuffer[i]
        bsi1 = BSIBuffer[i - 1]
        bsi2 = BSIBuffer[i]
        if (MathMax(ma1, ma2) < bsi2 and bsi1 < bsi2) or (MathMin(ma1, ma2) > bsi2 and bsi1 > bsi2):
            a = Box(0.0)
            b = Box(0.0)
            price = Arr(0, 0.0)
            upper = Arr(0, 0.0)
            lower = Arr(0, 0.0)
            ArraySetAsSeries(price, True)
            ArraySetAsSeries(upper, True)
            ArraySetAsSeries(lower, True)
            chk_h = CopyHigh(Symbol(), PERIOD_CURRENT, _DT(time[i]), InpTrendPeriod, upper)
            chk_l = CopyLow(Symbol(), PERIOD_CURRENT, _DT(time[i]), InpTrendPeriod, lower)
            chk_c = CopyClose(Symbol(), PERIOD_CURRENT, _DT(time[i]), InpTrendPeriod, price)
            if chk_c < InpTrendPeriod:
                continue
            if chk_h != chk_c or chk_l != chk_c:
                continue
            if not calc_regression(a, b, InpTrendPeriod, price):
                continue
            mid = a.v
            h1 = 0.0
            h2 = 0.0
            l1 = 0.0
            l2 = 0.0
            h1 = 0.0
            h2 = 0.0
            l1 = 0.0
            l2 = 0.0
            j = 0
            for j in range(j, InpTrendPeriod):
                if h1 < (upper[j] - mid):
                    h1 = upper[j] - mid
                elif h2 < (upper[j] - mid):
                    h2 = upper[j] - mid
                if l1 < (mid - lower[j]):
                    l1 = mid - lower[j]
                elif l2 < (mid - lower[j]):
                    l2 = mid - lower[j]
                mid += b.v
            else:
                j = _range_end(j, InpTrendPeriod, 1)
            if HighesBuffer[i - 1] < HighesBuffer[i] or LowesBuffer[i - 1] > LowesBuffer[i]:
                UpTrendBuffer[i] = a.v + ((h1 + h2) / 2)
                LoTrendBuffer[i] = a.v - ((l1 + l2) / 2)
                MdTrendBuffer[i] = a.v
                SlopeBuffer[i] = b.v
                j = 1
                for j in range(j, InpTrendPeriod):
                    UpTrendBuffer[i - j] = UpTrendBuffer[i - j + 1] + b.v
                    LoTrendBuffer[i - j] = LoTrendBuffer[i - j + 1] + b.v
                    MdTrendBuffer[i - j] = MdTrendBuffer[i - j + 1] + b.v
                else:
                    j = _range_end(j, InpTrendPeriod, 1)
                is_update = True
        else:
            is_update = True
            UpTrendBuffer[i] = UpRangeBuffer[i]
            LoTrendBuffer[i] = DnRangeBuffer[i]
            MdTrendBuffer[i] = (UpRangeBuffer[i] + DnRangeBuffer[i]) / 2
            SlopeBuffer[i] = 0.0
        if not is_update:
            if SlopeBuffer[i - 1] == 0:
                UpTrendBuffer[i - 1] = UpRangeBuffer[i - 1]
                LoTrendBuffer[i - 1] = DnRangeBuffer[i - 1]
                MdTrendBuffer[i] = (UpRangeBuffer[i - 1] + DnRangeBuffer[i - 1]) / 2
                SlopeBuffer[i - 1] = 0.0
            SlopeBuffer[i] = SlopeBuffer[i - 1]
            UpTrendBuffer[i] = UpTrendBuffer[i - 1] - SlopeBuffer[i]
            LoTrendBuffer[i] = LoTrendBuffer[i - 1] - SlopeBuffer[i]
            MdTrendBuffer[i] = MdTrendBuffer[i - 1] - SlopeBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def calc_regression(a, b, span, price):
    sumy = 0.0
    sumx = 0.0
    sumxy = 0.0
    sumx2 = 0.0
    x = 0
    cnt = 0
    x = 0
    for x in range(x, span):
        if price[x] == 0:
            continue
        sumx += x
        sumx2 += x * x
        sumy += price[x]
        sumxy += price[x] * x
        cnt += 1
    else:
        x = _range_end(x, span, 1)
    c = (sumx2 * cnt) - (sumx * sumx)
    if c == 0.0:
        return False
    b.v = _fdiv((sumxy * cnt) - (sumx * sumy), c)
    a.v = _fdiv(sumy - (sumx * b.v), cnt)
    return True

def calc_bsi(hi, lo, cl, vol, pos, span):
    k = 0
    sumpos = 0.0
    sumneg = 0.0
    sumhigh = 0.0
    sumpvol = 0.0
    sumnvol = 0.0
    k = pos - span + 1
    for k in range(k, pos + 1):
        v = 1.0
        if InpUsingVolumeWeight and VolBuffer[k] > 0:
            vol_fact = MathSqrt(VolBuffer[k])
            v = _fdiv(MathSqrt(vol[k]), vol_fact)
        ratio = 0.0
        sp = hi[k] - lo[k]
        if not ((cl[k - 1] - (sp * 0.2)) > cl[k]):
            ratio = (-1 * _fdiv(lo[k], TangoMaBuffer[k])) + 2
            sumpos += (cl[k] - lo[k]) * ratio * v
        if not ((cl[k - 1] + (sp * 0.2)) < cl[k]):
            ratio = (-1 * _fdiv(hi[k], TangoMaBuffer[k])) + 2
            sumneg += (hi[k] - cl[k]) * ratio * v
    else:
        k = _range_end(k, pos + 1, 1)
    tmppos = 0.0
    tmpneg = 0.0
    tmppos = _fdiv(_fdiv(sumpos, span), Point())
    tmpneg = _fdiv(_fdiv(sumneg, span), Point())
    bsi = 0.0
    if (tmppos + tmpneg) != 0:
        bsi = TangoMaBuffer[pos] + (8 * Point() * (tmppos - tmpneg) * MathAbs(_fdiv(tmppos - tmpneg, tmppos + tmpneg)))
    else:
        bsi = TangoMaBuffer[pos] + 0.0
    return bsi

# ---- global variables initialised from expressions
RevNoiseFilter = InpReversalNoiseFilter * Point()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BSI(_MQL5Indicator):
    name = 'BSI'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpChannelPeriod': 30,  # Channel Period
        'InpTrendPeriod': 30,  # Trend Period
        'InpReversalNoiseFilter': 5.0,  # NoiseFilter (Minimam Reversal Spread)
        'InpUsingVolumeWeight': True,  # UseingVolumeWeight
    }

