"""price_heatmap_v1.05 — converted from MQL5: MQL5 Indicators/Price Heatmap/price_heatmap_v1.05.mq5

Copyright: Copyright 2015, fxborg; Link: http://blog.livedoor.jp/fxborg/; Version: 1.05

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, fxborg', 'link': 'http://blog.livedoor.jp/fxborg/', 'version': '1.05', 'window': 'chart', 'indicator_buffers': 47, 'indicator_plots': 21}, 'types': {1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12, 12: 12, 13: 12, 14: 12, 15: 12, 16: 12, 17: 12, 18: 12, 19: 12, 20: 12, 21: 14}, 'colors': {21: [16728112]}, 'widths': {1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10, 11: 10, 12: 10, 13: 10, 14: 10, 15: 10, 16: 10, 17: 10, 18: 10, 19: 10, 20: 10, 21: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'price_heatmap_v1.05', 'source': 'MQL5 Indicators/Price Heatmap/price_heatmap_v1.05.mq5', 'folder': 'Price Heatmap', 'inputs': [{'mql': 'InpHistogramTF', 'py': 'InpHistogramTF', 'param': 'InpHistogramTF', 'type': 'int', 'default': 5, 'label': 'Histgram Time Frame', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 180, 'label': 'HistGramPeriod', 'sinput': False}, {'mql': 'InpBinRange', 'py': 'InpBinRange', 'param': 'InpBinRange', 'type': 'double', 'default': 5.0, 'label': 'BinRange', 'sinput': False}, {'mql': 'InpShowBars', 'py': 'InpShowBars', 'param': 'InpShowBars', 'type': 'bool', 'default': True, 'label': 'ShowBars', 'sinput': False}, {'mql': 'InpColorPattern', 'py': 'InpColorPattern', 'param': 'InpColorPattern', 'type': 'int', 'default': 1, 'label': '1:Green  2:Blue', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpHistogramTF = _input('InpHistogramTF', PERIOD_M5)  # Histgram Time Frame
InpPeriod = _input('InpPeriod', 180)  # HistGramPeriod
InpBinRange = _input('InpBinRange', 5.0)  # BinRange
InpShowBars = _input('InpShowBars', True)  # ShowBars
InpColorPattern = _input('InpColorPattern', 1)  # 1:Green  2:Blue
AvgVolPeriod = 100
Hst1Buf = Arr(0, 0.0)
Hst2Buf = Arr(0, 0.0)
Hst3Buf = Arr(0, 0.0)
Hst4Buf = Arr(0, 0.0)
Hst5Buf = Arr(0, 0.0)
Hst6Buf = Arr(0, 0.0)
Hst7Buf = Arr(0, 0.0)
Hst8Buf = Arr(0, 0.0)
Hst9Buf = Arr(0, 0.0)
Hst10Buf = Arr(0, 0.0)
Hst11Buf = Arr(0, 0.0)
Hst12Buf = Arr(0, 0.0)
Hst13Buf = Arr(0, 0.0)
Hst14Buf = Arr(0, 0.0)
Hst15Buf = Arr(0, 0.0)
Hst16Buf = Arr(0, 0.0)
Hst17Buf = Arr(0, 0.0)
Hst18Buf = Arr(0, 0.0)
Hst19Buf = Arr(0, 0.0)
Hst20Buf = Arr(0, 0.0)
Col1Buf = Arr(0, 0.0)
Col2Buf = Arr(0, 0.0)
Col3Buf = Arr(0, 0.0)
Col4Buf = Arr(0, 0.0)
Col5Buf = Arr(0, 0.0)
Col6Buf = Arr(0, 0.0)
Col7Buf = Arr(0, 0.0)
Col8Buf = Arr(0, 0.0)
Col9Buf = Arr(0, 0.0)
Col10Buf = Arr(0, 0.0)
Col11Buf = Arr(0, 0.0)
Col12Buf = Arr(0, 0.0)
Col13Buf = Arr(0, 0.0)
Col14Buf = Arr(0, 0.0)
Col15Buf = Arr(0, 0.0)
Col16Buf = Arr(0, 0.0)
Col17Buf = Arr(0, 0.0)
Col18Buf = Arr(0, 0.0)
Col19Buf = Arr(0, 0.0)
Col20Buf = Arr(0, 0.0)
VolBuf = Arr(0, 0.0)
OpenBuf = Arr(0, 0.0)
HighBuf = Arr(0, 0.0)
LowBuf = Arr(0, 0.0)
CloseBuf = Arr(0, 0.0)
CandleColBuf = Arr(0, 0.0)
CheckBuf = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    if PeriodSeconds(PERIOD_CURRENT) < PeriodSeconds(InpHistogramTF):
        Alert('Histogram Time Frame is too Large')
        return INIT_FAILED
    min_rates_total = _int(MathRound(_idiv(PeriodSeconds(InpHistogramTF), PeriodSeconds(PERIOD_CURRENT)) * InpPeriod)) + AvgVolPeriod + 1
    i = 0
    SetIndexBuffer(i, Hst1Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col1Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst2Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col2Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst3Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col3Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst4Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col4Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst5Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col5Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst6Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col6Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst7Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col7Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst8Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col8Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst9Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col9Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst10Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col10Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst11Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col11Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst12Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col12Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst13Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col13Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst14Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col14Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst15Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col15Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst16Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col16Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst17Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col17Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst18Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col18Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst19Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col19Buf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer((i := i + 1), Hst20Buf, INDICATOR_DATA)
    SetIndexBuffer((i := i + 1), Col20Buf, INDICATOR_COLOR_INDEX)
    i = 0
    for i in range(i, 20):
        PlotIndexSetInteger(i, PLOT_ARROW, 110)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, min_rates_total)
        setPlotColor(i)
    else:
        i = _range_end(i, 20, 1)
    SetIndexBuffer(40, OpenBuf, INDICATOR_DATA)
    SetIndexBuffer(41, HighBuf, INDICATOR_DATA)
    SetIndexBuffer(42, LowBuf, INDICATOR_DATA)
    SetIndexBuffer(43, CloseBuf, INDICATOR_DATA)
    SetIndexBuffer(44, CandleColBuf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(45, VolBuf, INDICATOR_CALCULATIONS)
    SetIndexBuffer(46, CheckBuf, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(46, PLOT_EMPTY_VALUE, 0)
    short_name = 'Price HeatMap v1.05'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    first = 0
    if rates_total <= min_rates_total:
        return 0
    first = min_rates_total
    if (first + 1) < prev_calculated and CheckBuf[prev_calculated - 3] == 1.0:
        first = prev_calculated - 2
    i = first
    for i in range(i, rates_total):
        if InpShowBars:
            OpenBuf[i] = open[i]
            HighBuf[i] = high[i]
            LowBuf[i] = low[i]
            CloseBuf[i] = close[i]
            CandleColBuf[i] = (1.0 if ((close[i] - open[i]) < 0) else 0.0)
        setEmptyValue(i)
        peaks = Arr(0, 0)
        hist = Arr(0, 0)
        offset = Box(0)
        if not generate_histgram(offset, peaks, hist, time[i], InpHistogramTF, InpBinRange, InpPeriod):
            continue
        CheckBuf[i] = 1.0
        sz = ArraySize(hist)
        imax = sz - 1
        max_hist = 1.0
        peak_cnt = ArraySize(peaks)
        peak_j = 0
        if peak_cnt > 0:
            peak_j = peaks[0]
            max_hist = hist[peak_j]
        VolBuf[i] = float(tick_volume[i])
        if (min_rates_total + AvgVolPeriod) >= i:
            continue
        avg = 0
        for k in range(0, AvgVolPeriod):
            avg += _long(VolBuf[i - k])
        avg = _long(MathRound(_idiv(avg, AvgVolPeriod)))
        histogram_bars = (_idiv(PeriodSeconds(InpHistogramTF), PeriodSeconds(PERIOD_CURRENT)) * InpPeriod) + 1
        cur_vol = 0.0
        k = 0
        while k < histogram_bars:
            cur_vol += float(tick_volume[i])
            k += 1
        cur_vol = _fdiv(cur_vol, histogram_bars)
        if cur_vol < (avg * 0.8):
            max_hist = MathRound(max_hist * 1.5)
        pos = 0
        if imax > 20:
            if peak_j > -1:
                pos = MathMax(0, peak_j - 5)
            else:
                pos = _int(MathRound(_idiv(imax - 20, 2)))
        for j in range(1, 20 + 1):
            col = 0
            peak = EMPTY_VALUE
            if pos < sz:
                peak = (offset.v + (pos * InpBinRange) + (InpBinRange / 2)) * (0.01 if (Digits() <= 3) else 0.0001)
                col = MathMin(25, _int(MathRound(_fdiv(hist[pos], max_hist) * 25)))
                if j == 1:
                    Hst1Buf[i] = peak
                    Col1Buf[i] = col
                if j == 2:
                    Hst2Buf[i] = peak
                    Col2Buf[i] = col
                if j == 3:
                    Hst3Buf[i] = peak
                    Col3Buf[i] = col
                if j == 4:
                    Hst4Buf[i] = peak
                    Col4Buf[i] = col
                if j == 5:
                    Hst5Buf[i] = peak
                    Col5Buf[i] = col
                if j == 6:
                    Hst6Buf[i] = peak
                    Col6Buf[i] = col
                if j == 7:
                    Hst7Buf[i] = peak
                    Col7Buf[i] = col
                if j == 8:
                    Hst8Buf[i] = peak
                    Col8Buf[i] = col
                if j == 9:
                    Hst9Buf[i] = peak
                    Col9Buf[i] = col
                if j == 10:
                    Hst10Buf[i] = peak
                    Col10Buf[i] = col
                if j == 11:
                    Hst11Buf[i] = peak
                    Col11Buf[i] = col
                if j == 12:
                    Hst12Buf[i] = peak
                    Col12Buf[i] = col
                if j == 13:
                    Hst13Buf[i] = peak
                    Col13Buf[i] = col
                if j == 14:
                    Hst14Buf[i] = peak
                    Col14Buf[i] = col
                if j == 15:
                    Hst15Buf[i] = peak
                    Col15Buf[i] = col
                if j == 16:
                    Hst16Buf[i] = peak
                    Col16Buf[i] = col
                if j == 17:
                    Hst17Buf[i] = peak
                    Col17Buf[i] = col
                if j == 18:
                    Hst18Buf[i] = peak
                    Col18Buf[i] = col
                if j == 19:
                    Hst19Buf[i] = peak
                    Col19Buf[i] = col
                if j == 20:
                    Hst20Buf[i] = peak
                    Col20Buf[i] = col
            pos += 1
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

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

def setPlotColor(plot):
    PlotIndexSetInteger(plot, PLOT_COLOR_INDEXES, 26)
    n = 0
    for i in range(0, 12 + 1):
        if InpColorPattern == 2:
            PlotIndexSetInteger(plot, PLOT_LINE_COLOR, ((n := n + 1) - 1), toRGB(100 + (i * 13), 0, 153 + _int(MathRound(i * 8.5))))
        else:
            PlotIndexSetInteger(plot, PLOT_LINE_COLOR, ((n := n + 1) - 1), toRGB(100 + (i * 13), 153 + _int(MathRound(i * 8.5)), 0))
    for i in range(1, 13 + 1):
        if InpColorPattern == 2:
            PlotIndexSetInteger(plot, PLOT_LINE_COLOR, ((n := n + 1) - 1), toRGB(255, 0, 255 - (i * 15)))
        else:
            PlotIndexSetInteger(plot, PLOT_LINE_COLOR, ((n := n + 1) - 1), toRGB(255, 255 - (i * 15), 0))

def toRGB(r, g, b):
    r = MathMin(255, MathMax(0, r))
    g = MathMin(255, MathMax(0, g))
    b = MathMin(255, MathMax(0, b))
    return StringToColor(IntegerToString(r) + ',' + IntegerToString(g) + ',' + IntegerToString(b))

def setEmptyValue(i):
    Hst1Buf[i] = EMPTY_VALUE
    Hst2Buf[i] = EMPTY_VALUE
    Hst3Buf[i] = EMPTY_VALUE
    Hst4Buf[i] = EMPTY_VALUE
    Hst5Buf[i] = EMPTY_VALUE
    Hst6Buf[i] = EMPTY_VALUE
    Hst7Buf[i] = EMPTY_VALUE
    Hst8Buf[i] = EMPTY_VALUE
    Hst9Buf[i] = EMPTY_VALUE
    Hst10Buf[i] = EMPTY_VALUE
    Hst11Buf[i] = EMPTY_VALUE
    Hst12Buf[i] = EMPTY_VALUE
    Hst13Buf[i] = EMPTY_VALUE
    Hst14Buf[i] = EMPTY_VALUE
    Hst15Buf[i] = EMPTY_VALUE
    Hst16Buf[i] = EMPTY_VALUE
    Hst17Buf[i] = EMPTY_VALUE
    Hst18Buf[i] = EMPTY_VALUE
    Hst19Buf[i] = EMPTY_VALUE
    Hst20Buf[i] = EMPTY_VALUE
    Col1Buf[i] = 0.0
    Col2Buf[i] = 0.0
    Col3Buf[i] = 0.0
    Col4Buf[i] = 0.0
    Col5Buf[i] = 0.0
    Col6Buf[i] = 0.0
    Col7Buf[i] = 0.0
    Col8Buf[i] = 0.0
    Col9Buf[i] = 0.0
    Col10Buf[i] = 0.0
    Col11Buf[i] = 0.0
    Col12Buf[i] = 0.0
    Col13Buf[i] = 0.0
    Col14Buf[i] = 0.0
    Col15Buf[i] = 0.0
    Col16Buf[i] = 0.0
    Col17Buf[i] = 0.0
    Col18Buf[i] = 0.0
    Col19Buf[i] = 0.0
    Col20Buf[i] = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceHeatmapV105(_MQL5Indicator):
    name = 'price_heatmap_v1.05'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpHistogramTF': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=5),  # Histgram Time Frame
        'InpPeriod': 180,  # HistGramPeriod
        'InpBinRange': 5.0,  # BinRange
        'InpShowBars': True,  # ShowBars
        'InpColorPattern': 1,  # 1:Green  2:Blue
    }

