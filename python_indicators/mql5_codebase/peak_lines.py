"""peak_lines — converted from MQL5: MQL5 Indicators/Price Heatmap/peak_lines.mq5

Copyright: Copyright 2015, fxborg; Link: http://blog.livedoor.jp/fxborg/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, fxborg', 'link': 'http://blog.livedoor.jp/fxborg/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 40, 'indicator_plots': 10}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5}, 'colors': {1: [16724630], 2: [15741590], 3: [15086230], 4: [14430870], 5: [13775510], 6: [13120150], 7: [12464790], 8: [11809430], 9: [11154070], 10: [10498710]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'peak_lines', 'source': 'MQL5 Indicators/Price Heatmap/peak_lines.mq5', 'folder': 'Price Heatmap', 'inputs': [{'mql': 'InpCalcTime', 'py': 'InpCalcTime', 'param': 'InpCalcTime', 'type': 'int', 'default': 4, 'label': 'Calculation Time(hour)', 'sinput': False}, {'mql': 'InpDailyPeriod', 'py': 'InpDailyPeriod', 'param': 'InpDailyPeriod', 'type': 'int', 'default': 60, 'label': 'DailyPeriod(hour)', 'sinput': False}, {'mql': 'InpFastPeriod', 'py': 'InpFastPeriod', 'param': 'InpFastPeriod', 'type': 'int', 'default': 180, 'label': 'FastPeriod(hour)', 'sinput': False}, {'mql': 'InpSlowPeriod', 'py': 'InpSlowPeriod', 'param': 'InpSlowPeriod', 'type': 'int', 'default': 30, 'label': 'SlowPeriod(day)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpCalcTime = _input('InpCalcTime', 4)  # Calculation Time(hour)
InpDailyPeriod = _input('InpDailyPeriod', 60)  # DailyPeriod(hour)
InpFastPeriod = _input('InpFastPeriod', 180)  # FastPeriod(hour)
InpSlowPeriod = _input('InpSlowPeriod', 30)  # SlowPeriod(day)
FastPeriod = InpFastPeriod * 2  # (30min)
SlowPeriod = 24 * InpSlowPeriod * 2  # (30min)
DailyPeriod = InpDailyPeriod * 12  # (60h/5min)
D1BinRange = 5
BinRange = 15
P1Buffer = Arr(0, 0.0)
P2Buffer = Arr(0, 0.0)
P3Buffer = Arr(0, 0.0)
P4Buffer = Arr(0, 0.0)
P5Buffer = Arr(0, 0.0)
P6Buffer = Arr(0, 0.0)
P7Buffer = Arr(0, 0.0)
P8Buffer = Arr(0, 0.0)
P9Buffer = Arr(0, 0.0)
P10Buffer = Arr(0, 0.0)
D1Buffer = Arr(0, 0.0)
D2Buffer = Arr(0, 0.0)
D3Buffer = Arr(0, 0.0)
D4Buffer = Arr(0, 0.0)
D5Buffer = Arr(0, 0.0)
D6Buffer = Arr(0, 0.0)
D7Buffer = Arr(0, 0.0)
D8Buffer = Arr(0, 0.0)
D9Buffer = Arr(0, 0.0)
D10Buffer = Arr(0, 0.0)
F1Buffer = Arr(0, 0.0)
F2Buffer = Arr(0, 0.0)
F3Buffer = Arr(0, 0.0)
F4Buffer = Arr(0, 0.0)
F5Buffer = Arr(0, 0.0)
F6Buffer = Arr(0, 0.0)
F7Buffer = Arr(0, 0.0)
F8Buffer = Arr(0, 0.0)
F9Buffer = Arr(0, 0.0)
F10Buffer = Arr(0, 0.0)
S1Buffer = Arr(0, 0.0)
S2Buffer = Arr(0, 0.0)
S3Buffer = Arr(0, 0.0)
S4Buffer = Arr(0, 0.0)
S5Buffer = Arr(0, 0.0)
S6Buffer = Arr(0, 0.0)
S7Buffer = Arr(0, 0.0)
S8Buffer = Arr(0, 0.0)
S9Buffer = Arr(0, 0.0)
S10Buffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 100
    SetIndexBuffer(0, P1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, P2Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, P3Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, P4Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, P5Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, P6Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, P7Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, P8Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, P9Buffer, INDICATOR_DATA)
    SetIndexBuffer(9, P10Buffer, INDICATOR_DATA)
    SetIndexBuffer(10, D1Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, D2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, D3Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, D4Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, D5Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, D6Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, D7Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, D8Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(18, D9Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(19, D10Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(20, F1Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(21, F2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(22, F3Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(23, F4Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(24, F5Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(25, F6Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(26, F7Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(27, F8Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(28, F9Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(29, F10Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(30, S1Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(31, S2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(32, S3Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(33, S4Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(34, S5Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(35, S6Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(36, S7Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(37, S8Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(38, S9Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(39, S10Buffer, INDICATOR_CALCULATIONS)
    for i in range(0, 10):
        PlotIndexSetInteger(i, PLOT_ARROW, 158)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, min_rates_total)
    short_name = 'Peak Line Histogram Test'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    first = 0
    if rates_total <= min_rates_total:
        return 0
    first = 1000
    if (first + 1) < prev_calculated:
        first = prev_calculated - 2
    i = first
    for i in range(i, rates_total):
        is_update = False
        tm0 = MqlDateTime()
        tm1 = MqlDateTime()
        TimeToStruct(time[i], tm0)
        TimeToStruct(time[i - 1], tm1)
        if tm1.hour != tm0.hour and tm0.hour == InpCalcTime:
            is_update = True
            calc_peaks(1, PERIOD_M5, D1BinRange, DailyPeriod, i, time[i], 1)
            calc_peaks(2, PERIOD_M30, BinRange, FastPeriod, i, time[i], 2)
            calc_peaks(3, PERIOD_M30, BinRange, SlowPeriod, i, time[i], 2)
        if not is_update:
            D1Buffer[i] = D1Buffer[i - 1]
            D2Buffer[i] = D2Buffer[i - 1]
            D3Buffer[i] = D3Buffer[i - 1]
            D4Buffer[i] = D4Buffer[i - 1]
            D5Buffer[i] = D5Buffer[i - 1]
            D6Buffer[i] = D6Buffer[i - 1]
            D7Buffer[i] = D7Buffer[i - 1]
            D8Buffer[i] = D8Buffer[i - 1]
            D9Buffer[i] = D9Buffer[i - 1]
            D10Buffer[i] = D10Buffer[i - 1]
            F1Buffer[i] = F1Buffer[i - 1]
            F2Buffer[i] = F2Buffer[i - 1]
            F3Buffer[i] = F3Buffer[i - 1]
            F4Buffer[i] = F4Buffer[i - 1]
            F5Buffer[i] = F5Buffer[i - 1]
            F6Buffer[i] = F6Buffer[i - 1]
            F7Buffer[i] = F7Buffer[i - 1]
            F8Buffer[i] = F8Buffer[i - 1]
            F9Buffer[i] = F9Buffer[i - 1]
            F10Buffer[i] = F10Buffer[i - 1]
            S1Buffer[i] = S1Buffer[i - 1]
            S2Buffer[i] = S2Buffer[i - 1]
            S3Buffer[i] = S3Buffer[i - 1]
            S4Buffer[i] = S4Buffer[i - 1]
            S5Buffer[i] = S5Buffer[i - 1]
            S6Buffer[i] = S6Buffer[i - 1]
            S7Buffer[i] = S7Buffer[i - 1]
            S8Buffer[i] = S8Buffer[i - 1]
            S9Buffer[i] = S9Buffer[i - 1]
            S10Buffer[i] = S10Buffer[i - 1]
        ma = (high[i] + low[i] + close[i]) / 3
        res = getPeaks(ma, BinRange * 2, i)
        if res > 0.0:
            append_peaks(i, res, 0)
        else:
            P1Buffer[i] = P1Buffer[i - 1]
            P2Buffer[i] = P2Buffer[i - 1]
            P3Buffer[i] = P3Buffer[i - 1]
            P4Buffer[i] = P4Buffer[i - 1]
            P5Buffer[i] = P5Buffer[i - 1]
            P6Buffer[i] = P6Buffer[i - 1]
            P7Buffer[i] = P7Buffer[i - 1]
            P8Buffer[i] = P8Buffer[i - 1]
            P9Buffer[i] = P9Buffer[i - 1]
            P10Buffer[i] = P10Buffer[i - 1]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def getPeaks(v, binRange, i):
    min_ = v - (binRange * (0.01 if (Digits() <= 3) else 0.0001) * 1.5)
    max_ = v + (binRange * (0.01 if (Digits() <= 3) else 0.0001) * 1.5)
    if min_ <= P1Buffer[i - 1] and P1Buffer[i - 1] <= max_:
        return 0.0
    if min_ <= P2Buffer[i - 1] and P2Buffer[i - 1] <= max_:
        return 0.0
    if min_ <= P3Buffer[i - 1] and P3Buffer[i - 1] <= max_:
        return 0.0
    if min_ <= P4Buffer[i - 1] and P4Buffer[i - 1] <= max_:
        return 0.0
    if min_ <= P5Buffer[i - 1] and P5Buffer[i - 1] <= max_:
        return 0.0
    if min_ <= P6Buffer[i - 1] and P6Buffer[i - 1] <= max_:
        return 0.0
    if min_ <= P7Buffer[i - 1] and P7Buffer[i - 1] <= max_:
        return 0.0
    if min_ <= P8Buffer[i - 1] and P8Buffer[i - 1] <= max_:
        return 0.0
    if min_ <= P9Buffer[i - 1] and P9Buffer[i - 1] <= max_:
        return 0.0
    if min_ <= P10Buffer[i - 1] and P10Buffer[i - 1] <= max_:
        return 0.0
    min_ = v - (binRange * (0.01 if (Digits() <= 3) else 0.0001))
    max_ = v + (binRange * (0.01 if (Digits() <= 3) else 0.0001))
    if min_ <= D1Buffer[i] and D1Buffer[i] <= max_:
        return D1Buffer[i]
    if min_ <= D2Buffer[i] and D2Buffer[i] <= max_:
        return D2Buffer[i]
    if min_ <= D3Buffer[i] and D3Buffer[i] <= max_:
        return D3Buffer[i]
    if min_ <= D4Buffer[i] and D4Buffer[i] <= max_:
        return D4Buffer[i]
    if min_ <= D5Buffer[i] and D5Buffer[i] <= max_:
        return D5Buffer[i]
    if min_ <= D6Buffer[i] and D6Buffer[i] <= max_:
        return D6Buffer[i]
    if min_ <= D7Buffer[i] and D7Buffer[i] <= max_:
        return D7Buffer[i]
    if min_ <= D8Buffer[i] and D8Buffer[i] <= max_:
        return D8Buffer[i]
    if min_ <= D9Buffer[i] and D9Buffer[i] <= max_:
        return D9Buffer[i]
    if min_ <= D10Buffer[i] and D10Buffer[i] <= max_:
        return D10Buffer[i]
    if min_ <= S1Buffer[i] and S1Buffer[i] <= max_:
        return S1Buffer[i]
    if min_ <= S2Buffer[i] and S2Buffer[i] <= max_:
        return S2Buffer[i]
    if min_ <= S3Buffer[i] and S3Buffer[i] <= max_:
        return S3Buffer[i]
    if min_ <= S4Buffer[i] and S4Buffer[i] <= max_:
        return S4Buffer[i]
    if min_ <= S5Buffer[i] and S5Buffer[i] <= max_:
        return S5Buffer[i]
    if min_ <= S6Buffer[i] and S6Buffer[i] <= max_:
        return S6Buffer[i]
    if min_ <= S7Buffer[i] and S7Buffer[i] <= max_:
        return S7Buffer[i]
    if min_ <= S8Buffer[i] and S8Buffer[i] <= max_:
        return S8Buffer[i]
    if min_ <= S9Buffer[i] and S9Buffer[i] <= max_:
        return S9Buffer[i]
    if min_ <= S10Buffer[i] and S10Buffer[i] <= max_:
        return S10Buffer[i]
    if min_ <= F1Buffer[i] and F1Buffer[i] <= max_:
        return F1Buffer[i]
    if min_ <= F2Buffer[i] and F2Buffer[i] <= max_:
        return F2Buffer[i]
    if min_ <= F3Buffer[i] and F3Buffer[i] <= max_:
        return F3Buffer[i]
    if min_ <= F4Buffer[i] and F4Buffer[i] <= max_:
        return F4Buffer[i]
    if min_ <= F5Buffer[i] and F5Buffer[i] <= max_:
        return F5Buffer[i]
    if min_ <= F6Buffer[i] and F6Buffer[i] <= max_:
        return F6Buffer[i]
    if min_ <= F7Buffer[i] and F7Buffer[i] <= max_:
        return F7Buffer[i]
    if min_ <= F8Buffer[i] and F8Buffer[i] <= max_:
        return F8Buffer[i]
    if min_ <= F9Buffer[i] and F9Buffer[i] <= max_:
        return F9Buffer[i]
    if min_ <= F10Buffer[i] and F10Buffer[i] <= max_:
        return F10Buffer[i]
    return 0.0

def calc_peaks(opt, tf, binRange, period, i, t, limit):
    peaks = Arr(0, 0)
    hist = Arr(0, 0)
    offset = Box(0)
    if generate_histgram(offset, peaks, hist, t, tf, binRange, period):
        peak_cnt = ArraySize(peaks)
        if peak_cnt > 0:
            line_cnt = 0
            for j in range(0, MathMin(limit, peak_cnt)):
                peak = (offset.v + (peaks[j] * binRange) + _idiv(binRange, 2)) * (0.01 if (Digits() <= 3) else 0.0001)
                append_peaks(i, peak, opt)

def generate_histgram(offset, tf_peaks, tf_hist, t, tf, binRange, histPeriod):
    tf_high = Arr(0, 0.0)
    tf_low = Arr(0, 0.0)
    tf_vol = Arr(0, 0)
    ArraySetAsSeries(tf_high, True)
    ArraySetAsSeries(tf_low, True)
    ArraySetAsSeries(tf_vol, True)
    tf_len1 = CopyTickVolume(Symbol(), tf, _DT(t), histPeriod, tf_vol)
    tf_len2 = CopyHigh(Symbol(), tf, _DT(t), histPeriod, tf_high)
    tf_len3 = CopyLow(Symbol(), tf, _DT(t), histPeriod, tf_low)
    tf_ok = (histPeriod == tf_len1 and tf_len1 == tf_len2) and tf_len2 == tf_len3
    if not tf_ok:
        return False
    offset.v = _int(MathRound(_fdiv(tf_low[ArrayMinimum(tf_low)], (0.01 if (Digits() <= 3) else 0.0001))))
    limit = _int(MathRound(_fdiv(tf_high[ArrayMaximum(tf_high)], (0.01 if (Digits() <= 3) else 0.0001))))
    calc_histgram(tf_peaks, tf_hist, tf_high, tf_low, tf_vol, offset.v, limit, binRange, histPeriod)
    return True

def calc_histgram(peaks, hist, hi, lo, vol, offset, limit, binRange, histPeriod):
    j = 0
    k = 0
    steps = _int(MathRound(_fdiv(limit - offset, binRange))) + 1
    ArrayResize(hist, steps)
    ArrayInitialize(hist, 0)
    j = histPeriod - 1
    for j in range(j, 0 - 1, -1):
        l = _int(MathRound(_fdiv(lo[j], (0.01 if (Digits() <= 3) else 0.0001))))
        h = _int(MathRound(_fdiv(hi[j], (0.01 if (Digits() <= 3) else 0.0001))))
        v = _int(MathRound(MathSqrt(MathMin(vol[j], 1))))
        min_ = _int(MathRound(_fdiv(l - offset, binRange)))
        max_ = _int(MathRound(_fdiv(h - offset, binRange)))
        k = min_
        for k in range(k, max_ + 1):
            hist[k] += v
        else:
            k = _range_end(k, max_ + 1, 1)
    else:
        j = _range_end(j, 0 - 1, -1)
    work = Arr(0, 0, dims=(2,))
    peak_count = find_peaks(work, hist, steps, binRange)
    ArrayResize(peaks, 0, peak_count)
    top = 0
    cnt = 0
    j = peak_count - 1
    for j in range(j, 0 - 1, -1):
        if j == (peak_count - 1):
            top = work[j][0]
        if work[j][0] > (top * 0.1):
            cnt += 1
            ArrayResize(peaks, cnt, peak_count)
            peaks[cnt - 1] = work[j][1]
    else:
        j = _range_end(j, 0 - 1, -1)
    return True

def find_peaks(peaks, hist, steps, binrange):
    if steps <= 10:
        ArrayResize(peaks, 1)
        peaks[0][1] = ArrayMaximum(hist)
        peaks[0][0] = hist[peaks[0][1]]
        return 1
    count = 0
    for i in range(2, steps - 2):
        max_ = MathMax(MathMax(MathMax(MathMax(hist[i - 2], hist[i - 1]), hist[i]), hist[i + 1]), hist[i + 2])
        if hist[i] == max_:
            count += 1
            ArrayResize(peaks, count)
            total = hist[i - 2] + hist[i - 1] + hist[i] + hist[i + 1] + hist[i + 2]
            peaks[count - 1][0] = total
            peaks[count - 1][1] = i
    if count > 1:
        ArraySort(peaks)
    return count

def append_peaks(i, v, opt):
    if opt == 0:
        P1Buffer[i] = v
        P2Buffer[i] = P1Buffer[i - 1]
        P3Buffer[i] = P2Buffer[i - 1]
        P4Buffer[i] = P3Buffer[i - 1]
        P5Buffer[i] = P4Buffer[i - 1]
        P6Buffer[i] = P5Buffer[i - 1]
        P7Buffer[i] = P6Buffer[i - 1]
        P8Buffer[i] = P7Buffer[i - 1]
        P9Buffer[i] = P8Buffer[i - 1]
        P10Buffer[i] = P9Buffer[i - 1]
    elif opt == 1:
        D1Buffer[i] = v
        D2Buffer[i] = D1Buffer[i - 1]
        D3Buffer[i] = D2Buffer[i - 1]
        D4Buffer[i] = D3Buffer[i - 1]
        D5Buffer[i] = D4Buffer[i - 1]
        D6Buffer[i] = D5Buffer[i - 1]
        D7Buffer[i] = D6Buffer[i - 1]
        D8Buffer[i] = D7Buffer[i - 1]
        D9Buffer[i] = D8Buffer[i - 1]
        D10Buffer[i] = D9Buffer[i - 1]
    elif opt == 2:
        F1Buffer[i] = v
        F2Buffer[i] = F1Buffer[i - 1]
        F3Buffer[i] = F2Buffer[i - 1]
        F4Buffer[i] = F3Buffer[i - 1]
        F5Buffer[i] = F4Buffer[i - 1]
        F6Buffer[i] = F5Buffer[i - 1]
        F7Buffer[i] = F6Buffer[i - 1]
        F8Buffer[i] = F7Buffer[i - 1]
        F9Buffer[i] = F8Buffer[i - 1]
        F10Buffer[i] = F9Buffer[i - 1]
    elif opt == 3:
        S1Buffer[i] = v
        S2Buffer[i] = S1Buffer[i - 1]
        S3Buffer[i] = S2Buffer[i - 1]
        S4Buffer[i] = S3Buffer[i - 1]
        S5Buffer[i] = S4Buffer[i - 1]
        S6Buffer[i] = S5Buffer[i - 1]
        S7Buffer[i] = S6Buffer[i - 1]
        S8Buffer[i] = S7Buffer[i - 1]
        S9Buffer[i] = S8Buffer[i - 1]
        S10Buffer[i] = S9Buffer[i - 1]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PeakLines(_MQL5Indicator):
    name = 'peak_lines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpCalcTime': 4,  # Calculation Time(hour)
        'InpDailyPeriod': 60,  # DailyPeriod(hour)
        'InpFastPeriod': 180,  # FastPeriod(hour)
        'InpSlowPeriod': 30,  # SlowPeriod(day)
    }

