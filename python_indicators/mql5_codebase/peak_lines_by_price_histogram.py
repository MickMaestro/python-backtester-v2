"""peak_lines_by_price_histogram — converted from MQL5: MQL5 Indicators/Peak Lines by Price Histogram/peak_lines_by_price_histogram.mq5

Copyright: Copyright 2015, fxborg; Link: http://blog.livedoor.jp/fxborg/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, fxborg', 'link': 'http://blog.livedoor.jp/fxborg/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 32, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [55295], 2: [55295], 3: [255], 4: [255], 5: [16711935], 6: [16711935], 7: [16760576], 8: [16760576]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'labels': {1: '1st Peek daily', 2: '2nd Peek daily', 3: '1st Peek short', 4: '2nd Peek short', 5: '1st Peek medium', 6: '2nd Peek medium', 7: '1st Peek long', 8: '2nd Peek long'}, 'levels': [], 'description': [], 'name': 'peak_lines_by_price_histogram', 'source': 'MQL5 Indicators/Peak Lines by Price Histogram/peak_lines_by_price_histogram.mq5', 'folder': 'Peak Lines by Price Histogram', 'inputs': [{'mql': 'InpBinRange', 'py': 'InpBinRange', 'param': 'InpBinRange', 'type': 'double', 'default': 2.5, 'label': 'Bin range of price histogram', 'sinput': False}, {'mql': 'InpCalcTime', 'py': 'InpCalcTime', 'param': 'InpCalcTime', 'type': 'int', 'default': 4, 'label': 'Calculation Time(hour)', 'sinput': False}, {'mql': 'InpShortTermPeriod', 'py': 'InpShortTermPeriod', 'param': 'InpShortTermPeriod', 'type': 'int', 'default': 3, 'label': 'Short term period(day)', 'sinput': False}, {'mql': 'InpMediumTermPeriod', 'py': 'InpMediumTermPeriod', 'param': 'InpMediumTermPeriod', 'type': 'int', 'default': 7, 'label': 'Medium term period(day)', 'sinput': False}, {'mql': 'InpLongTermPeriod', 'py': 'InpLongTermPeriod', 'param': 'InpLongTermPeriod', 'type': 'int', 'default': 26, 'label': 'Long term period(day)', 'sinput': False}, {'mql': 'InpUsingVolumeWeight', 'py': 'InpUsingVolumeWeight', 'param': 'InpUsingVolumeWeight', 'type': 'bool', 'default': True, 'label': 'Using TickVolume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBinRange = _input('InpBinRange', 2.5)  # Bin range of price histogram
InpCalcTime = _input('InpCalcTime', 4)  # Calculation Time(hour)
InpShortTermPeriod = _input('InpShortTermPeriod', 3)  # Short term period(day)
InpMediumTermPeriod = _input('InpMediumTermPeriod', 7)  # Medium term period(day)
InpLongTermPeriod = _input('InpLongTermPeriod', 26)  # Long term period(day)
InpUsingVolumeWeight = _input('InpUsingVolumeWeight', True)  # Using TickVolume
PivotHour = 4  # Pivot period (hour)
d1_period = 24 * 12  # for 5min
st_period = InpShortTermPeriod * 24 * 12  # for 5min
mt_period = InpMediumTermPeriod * 24  # for 1h
lt_period = InpLongTermPeriod * 24  # for 1h
zoom_out_factor = 8
Day1Buffer = Arr(0, 0.0)
Short1Buffer = Arr(0, 0.0)
Medium1Buffer = Arr(0, 0.0)
Long1Buffer = Arr(0, 0.0)
Day2Buffer = Arr(0, 0.0)
Short2Buffer = Arr(0, 0.0)
Medium2Buffer = Arr(0, 0.0)
Long2Buffer = Arr(0, 0.0)
D1Buffer = Arr(0, 0.0)
D2Buffer = Arr(0, 0.0)
D3Buffer = Arr(0, 0.0)
D4Buffer = Arr(0, 0.0)
S1Buffer = Arr(0, 0.0)
S2Buffer = Arr(0, 0.0)
S3Buffer = Arr(0, 0.0)
S4Buffer = Arr(0, 0.0)
M1Buffer = Arr(0, 0.0)
M2Buffer = Arr(0, 0.0)
M3Buffer = Arr(0, 0.0)
M4Buffer = Arr(0, 0.0)
M5Buffer = Arr(0, 0.0)
M6Buffer = Arr(0, 0.0)
M7Buffer = Arr(0, 0.0)
M8Buffer = Arr(0, 0.0)
L1Buffer = Arr(0, 0.0)
L2Buffer = Arr(0, 0.0)
L3Buffer = Arr(0, 0.0)
L4Buffer = Arr(0, 0.0)
L5Buffer = Arr(0, 0.0)
L6Buffer = Arr(0, 0.0)
L7Buffer = Arr(0, 0.0)
L8Buffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 1 + _idiv(InpLongTermPeriod * PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
    SetIndexBuffer(0, Day1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Day2Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, Short1Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, Short2Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, Medium1Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, Medium2Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, Long1Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, Long2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    PlotIndexSetInteger(2, PLOT_ARROW, 158)
    PlotIndexSetInteger(3, PLOT_ARROW, 158)
    PlotIndexSetInteger(4, PLOT_ARROW, 158)
    PlotIndexSetInteger(5, PLOT_ARROW, 158)
    PlotIndexSetInteger(6, PLOT_ARROW, 158)
    PlotIndexSetInteger(7, PLOT_ARROW, 158)
    SetIndexBuffer(8, D1Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, D2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, D3Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, D4Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, S1Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, S2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, S3Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, S4Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, M1Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, M2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(18, M3Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(19, M4Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(20, M5Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(21, M6Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(22, M7Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(23, M8Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(24, L1Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(25, L2Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(26, L3Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(27, L4Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(28, L5Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(29, L6Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(30, L7Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(31, L8Buffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHIFT, 1)
    PlotIndexSetInteger(1, PLOT_SHIFT, 1)
    PlotIndexSetInteger(2, PLOT_SHIFT, 1)
    PlotIndexSetInteger(3, PLOT_SHIFT, 1)
    PlotIndexSetInteger(4, PLOT_SHIFT, 1)
    PlotIndexSetInteger(5, PLOT_SHIFT, 1)
    PlotIndexSetInteger(6, PLOT_SHIFT, 1)
    PlotIndexSetInteger(7, PLOT_SHIFT, 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Peak Lines')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    first = 0
    if rates_total <= min_rates_total:
        return 0
    first = min_rates_total - 1
    if (first + 1) < prev_calculated:
        first = prev_calculated - 2
    i = first
    for i in range(i, rates_total):
        tm0 = MqlDateTime()
        tm1 = MqlDateTime()
        TimeToStruct(time[i], tm0)
        TimeToStruct(time[i - 1], tm1)
        is_update = False
        if ((not tm0.hour) != tm0.hour and tm0.hour == InpCalcTime) and tm0.hour == InpCalcTime:
            d1_peaks = Arr(0, 0)
            st_peaks = Arr(0, 0)
            mt_peaks = Arr(0, 0)
            lt_peaks = Arr(0, 0)
            ok = calc_ds_peaks(d1_peaks, st_peaks, time[i])
            ok = ok and calc_ml_peaks(lt_peaks, mt_peaks, time[i])
            if ok:
                d1_sz = ArraySize(d1_peaks)
                if d1_sz > 0:
                    D1Buffer[i] = d1_peaks[0] * Point()
                else:
                    D1Buffer[i] = 0.0
                if d1_sz > 1:
                    D2Buffer[i] = d1_peaks[1] * Point()
                else:
                    D2Buffer[i] = 0.0
                if d1_sz > 2:
                    D3Buffer[i] = d1_peaks[2] * Point()
                else:
                    D3Buffer[i] = 0.0
                if d1_sz > 3:
                    D4Buffer[i] = d1_peaks[3] * Point()
                else:
                    D4Buffer[i] = 0.0
                st_sz = ArraySize(st_peaks)
                if st_sz > 0:
                    S1Buffer[i] = st_peaks[0] * Point()
                else:
                    S1Buffer[i] = 0.0
                if st_sz > 1:
                    S2Buffer[i] = st_peaks[1] * Point()
                else:
                    S2Buffer[i] = 0.0
                if st_sz > 2:
                    S3Buffer[i] = st_peaks[2] * Point()
                else:
                    S3Buffer[i] = 0.0
                if st_sz > 3:
                    S4Buffer[i] = st_peaks[3] * Point()
                else:
                    S4Buffer[i] = 0.0
                mt_sz = ArraySize(mt_peaks)
                if mt_sz > 0:
                    M1Buffer[i] = mt_peaks[0] * Point()
                else:
                    M1Buffer[i] = 0.0
                if mt_sz > 1:
                    M2Buffer[i] = mt_peaks[1] * Point()
                else:
                    M2Buffer[i] = 0.0
                if mt_sz > 2:
                    M3Buffer[i] = mt_peaks[2] * Point()
                else:
                    M3Buffer[i] = 0.0
                if mt_sz > 3:
                    M4Buffer[i] = mt_peaks[3] * Point()
                else:
                    M4Buffer[i] = 0.0
                if mt_sz > 4:
                    M5Buffer[i] = mt_peaks[4] * Point()
                else:
                    M5Buffer[i] = 0.0
                if mt_sz > 5:
                    M6Buffer[i] = mt_peaks[5] * Point()
                else:
                    M6Buffer[i] = 0.0
                if mt_sz > 6:
                    M7Buffer[i] = mt_peaks[6] * Point()
                else:
                    M7Buffer[i] = 0.0
                if mt_sz > 7:
                    M8Buffer[i] = mt_peaks[7] * Point()
                else:
                    M8Buffer[i] = 0.0
                lt_sz = ArraySize(lt_peaks)
                if lt_sz > 0:
                    L1Buffer[i] = lt_peaks[0] * Point()
                else:
                    L1Buffer[i] = 0.0
                if lt_sz > 1:
                    L2Buffer[i] = lt_peaks[1] * Point()
                else:
                    L2Buffer[i] = 0.0
                if lt_sz > 2:
                    L3Buffer[i] = lt_peaks[2] * Point()
                else:
                    L3Buffer[i] = 0.0
                if lt_sz > 3:
                    L4Buffer[i] = lt_peaks[3] * Point()
                else:
                    L4Buffer[i] = 0.0
                if lt_sz > 4:
                    L5Buffer[i] = lt_peaks[4] * Point()
                else:
                    L5Buffer[i] = 0.0
                if lt_sz > 5:
                    L6Buffer[i] = lt_peaks[5] * Point()
                else:
                    L6Buffer[i] = 0.0
                if lt_sz > 6:
                    L7Buffer[i] = lt_peaks[6] * Point()
                else:
                    L7Buffer[i] = 0.0
                if lt_sz > 7:
                    L8Buffer[i] = lt_peaks[7] * Point()
                else:
                    L8Buffer[i] = 0.0
                is_update = True
        if not is_update:
            D1Buffer[i] = 0.0
            D2Buffer[i] = 0.0
            D3Buffer[i] = 0.0
            D4Buffer[i] = 0.0
            S1Buffer[i] = 0.0
            S2Buffer[i] = 0.0
            S3Buffer[i] = 0.0
            S4Buffer[i] = 0.0
            M1Buffer[i] = 0.0
            M2Buffer[i] = 0.0
            M3Buffer[i] = 0.0
            M4Buffer[i] = 0.0
            M5Buffer[i] = 0.0
            M6Buffer[i] = 0.0
            M7Buffer[i] = 0.0
            M8Buffer[i] = 0.0
            L1Buffer[i] = 0.0
            L2Buffer[i] = 0.0
            L3Buffer[i] = 0.0
            L4Buffer[i] = 0.0
            L5Buffer[i] = 0.0
            L6Buffer[i] = 0.0
            L7Buffer[i] = 0.0
            L8Buffer[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    i = first
    for i in range(i, rates_total):
        h = Arr(0, 0.0)
        l = Arr(0, 0.0)
        c = Arr(0, 0.0)
        CopyHigh(Symbol(), PERIOD_H1, _DT(time[i]), PivotHour, h)
        CopyLow(Symbol(), PERIOD_H1, _DT(time[i]), PivotHour, l)
        CopyClose(Symbol(), PERIOD_H1, _DT(time[i]), 1, c)
        hi = h[ArrayMaximum(h)]
        lo = l[ArrayMinimum(l)]
        cl = c[0]
        pp = (cl + hi + lo) / 3
        s1 = (pp * 2) - hi
        r1 = (pp * 2) - lo
        s2 = pp - (r1 - s1)
        r2 = pp - s1 + r1
        set_1d_peeks(s2, r2, i)
        set_st_peeks(s2, r2, i)
        set_mt_peeks(s2, r2, i)
        set_lt_peeks(s2, r2, i)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def set_1d_peeks(s2, r2, i):
    d1cnt = 0
    if D1Buffer[i] > 0:
        Day1Buffer[i] = D1Buffer[i]
    else:
        Day1Buffer[i] = Day1Buffer[i - 1]
    d1cnt += 1
    if s2 <= D2Buffer[i] and D2Buffer[i] <= r2:
        if d1cnt == 0:
            Day1Buffer[i] = D2Buffer[i]
        else:
            Day2Buffer[i] = D2Buffer[i]
        d1cnt += 1
    if (d1cnt < 2 and s2 <= D3Buffer[i]) and D3Buffer[i] <= r2:
        if d1cnt == 0:
            Day1Buffer[i] = D3Buffer[i]
        else:
            Day2Buffer[i] = D3Buffer[i]
        d1cnt += 1
    if (d1cnt < 2 and s2 <= D4Buffer[i]) and D4Buffer[i] <= r2:
        if d1cnt == 0:
            Day1Buffer[i] = D4Buffer[i]
        else:
            Day2Buffer[i] = D4Buffer[i]
        d1cnt += 1
    if d1cnt < 2:
        Day2Buffer[i] = Day2Buffer[i - 1]

def set_st_peeks(s2, r2, i):
    s_cnt = 0
    if s2 <= S1Buffer[i] and S1Buffer[i] <= r2:
        Short1Buffer[i] = S1Buffer[i]
        s_cnt += 1
    if s2 <= S2Buffer[i] and S2Buffer[i] <= r2:
        if s_cnt == 0:
            Short1Buffer[i] = S2Buffer[i]
        else:
            Short2Buffer[i] = S2Buffer[i]
        s_cnt += 1
    if (s_cnt < 2 and s2 <= S3Buffer[i]) and S3Buffer[i] <= r2:
        if s_cnt == 0:
            Short1Buffer[i] = S3Buffer[i]
        else:
            Short2Buffer[i] = S3Buffer[i]
        s_cnt += 1
    if (s_cnt < 2 and s2 <= S4Buffer[i]) and S4Buffer[i] <= r2:
        if s_cnt == 0:
            Short1Buffer[i] = S4Buffer[i]
        else:
            Short2Buffer[i] = S4Buffer[i]
        s_cnt += 1
    if s_cnt < 1:
        Short1Buffer[i] = Short1Buffer[i - 1]
    if s_cnt < 2:
        Short2Buffer[i] = Short2Buffer[i - 1]

def set_mt_peeks(s2, r2, i):
    m_cnt = 0
    if s2 <= M1Buffer[i] and M1Buffer[i] <= r2:
        Medium1Buffer[i] = M1Buffer[i]
        m_cnt += 1
    if s2 <= M2Buffer[i] and M2Buffer[i] <= r2:
        if m_cnt == 0:
            Medium1Buffer[i] = M2Buffer[i]
        else:
            Medium2Buffer[i] = M2Buffer[i]
        m_cnt += 1
    if (m_cnt < 2 and s2 <= M3Buffer[i]) and M3Buffer[i] <= r2:
        if m_cnt == 0:
            Medium1Buffer[i] = M3Buffer[i]
        else:
            Medium2Buffer[i] = M3Buffer[i]
        m_cnt += 1
    if (m_cnt < 2 and s2 <= M4Buffer[i]) and M4Buffer[i] <= r2:
        if m_cnt == 0:
            Medium1Buffer[i] = M4Buffer[i]
        else:
            Medium2Buffer[i] = M4Buffer[i]
        m_cnt += 1
    if (m_cnt < 2 and s2 <= M5Buffer[i]) and M5Buffer[i] <= r2:
        if m_cnt == 0:
            Medium1Buffer[i] = M5Buffer[i]
        else:
            Medium2Buffer[i] = M5Buffer[i]
        m_cnt += 1
    if (m_cnt < 2 and s2 <= M6Buffer[i]) and M6Buffer[i] <= r2:
        if m_cnt == 0:
            Medium1Buffer[i] = M6Buffer[i]
        else:
            Medium2Buffer[i] = M6Buffer[i]
        m_cnt += 1
    if (m_cnt < 2 and s2 <= M7Buffer[i]) and M7Buffer[i] <= r2:
        if m_cnt == 0:
            Medium1Buffer[i] = M7Buffer[i]
        else:
            Medium2Buffer[i] = M7Buffer[i]
        m_cnt += 1
    if (m_cnt < 2 and s2 <= M8Buffer[i]) and M8Buffer[i] <= r2:
        if m_cnt == 0:
            Medium1Buffer[i] = M8Buffer[i]
        else:
            Medium2Buffer[i] = M8Buffer[i]
        m_cnt += 1
    if m_cnt < 1:
        Medium1Buffer[i] = Medium1Buffer[i - 1]
    if m_cnt < 2:
        Medium2Buffer[i] = Medium2Buffer[i - 1]

def set_lt_peeks(s2, r2, i):
    l_cnt = 0
    if s2 <= L1Buffer[i] and L1Buffer[i] <= r2:
        Long1Buffer[i] = L1Buffer[i]
        l_cnt += 1
    elif s2 <= L2Buffer[i] and L2Buffer[i] <= r2:
        if l_cnt == 0:
            Long1Buffer[i] = L2Buffer[i]
        else:
            Long2Buffer[i] = L2Buffer[i]
        l_cnt += 1
    elif (l_cnt < 2 and s2 <= L3Buffer[i]) and L3Buffer[i] <= r2:
        if l_cnt == 0:
            Long1Buffer[i] = L3Buffer[i]
        else:
            Long2Buffer[i] = L3Buffer[i]
        l_cnt += 1
    elif (l_cnt < 2 and s2 <= L4Buffer[i]) and L4Buffer[i] <= r2:
        if l_cnt == 0:
            Long1Buffer[i] = L4Buffer[i]
        else:
            Long2Buffer[i] = L4Buffer[i]
        l_cnt += 1
    elif (l_cnt < 2 and s2 <= L5Buffer[i]) and L5Buffer[i] <= r2:
        if l_cnt == 0:
            Long1Buffer[i] = L5Buffer[i]
        else:
            Long2Buffer[i] = L5Buffer[i]
        l_cnt += 1
    elif (l_cnt < 2 and s2 <= L6Buffer[i]) and L6Buffer[i] <= r2:
        if l_cnt == 0:
            Long1Buffer[i] = L6Buffer[i]
        else:
            Long2Buffer[i] = L6Buffer[i]
        l_cnt += 1
    elif (l_cnt < 2 and s2 <= L7Buffer[i]) and L7Buffer[i] <= r2:
        if l_cnt == 0:
            Long1Buffer[i] = L7Buffer[i]
        else:
            Long2Buffer[i] = L7Buffer[i]
        l_cnt += 1
    elif (l_cnt < 2 and s2 <= L8Buffer[i]) and L8Buffer[i] <= r2:
        if l_cnt == 0:
            Long1Buffer[i] = L8Buffer[i]
        else:
            Long2Buffer[i] = L8Buffer[i]
        l_cnt += 1
    if l_cnt < 1:
        Long1Buffer[i] = Long1Buffer[i - 1]
    if l_cnt < 2:
        Long2Buffer[i] = Long2Buffer[i - 1]

def calc_ds_peaks(d1_peaks, st_peaks, t):
    m5high = Arr(0, 0.0)
    m5low = Arr(0, 0.0)
    m5vol = Arr(0, 0)
    ArraySetAsSeries(m5high, True)
    ArraySetAsSeries(m5low, True)
    ArraySetAsSeries(m5vol, True)
    m5_len1 = CopyTickVolume(Symbol(), PERIOD_M5, _DT(t), st_period, m5vol)
    m5_len2 = CopyHigh(Symbol(), PERIOD_M5, _DT(t), st_period, m5high)
    m5_len3 = CopyLow(Symbol(), PERIOD_M5, _DT(t), st_period, m5low)
    if (st_period == m5_len1 and m5_len1 == m5_len2) and m5_len2 == m5_len3:
        st_offset = _int(MathRound(_fdiv(m5low[ArrayMinimum(m5low)], Point())))
        calc_histgram(st_peaks, m5high, m5low, m5vol, st_period, st_offset, InpBinRange)
        d1_offset = _int(MathRound(_fdiv(m5low[ArrayMinimum(m5low, 0, d1_period)], Point())))
        calc_histgram(d1_peaks, m5high, m5low, m5vol, d1_period, d1_offset, InpBinRange, d1_period)
        return True
    return False

def calc_ml_peaks(lt_peaks, mt_peaks, t):
    h1high = Arr(0, 0.0)
    h1low = Arr(0, 0.0)
    h1vol = Arr(0, 0)
    ArraySetAsSeries(h1high, True)
    ArraySetAsSeries(h1low, True)
    ArraySetAsSeries(h1vol, True)
    h1_len1 = CopyTickVolume(Symbol(), PERIOD_H1, _DT(t), lt_period, h1vol)
    h1_len2 = CopyHigh(Symbol(), PERIOD_H1, _DT(t), lt_period, h1high)
    h1_len3 = CopyLow(Symbol(), PERIOD_H1, _DT(t), lt_period, h1low)
    if (lt_period == h1_len1 and h1_len1 == h1_len2) and h1_len2 == h1_len3:
        lt_offset = _int(MathRound(_fdiv(h1low[ArrayMinimum(h1low)], Point())))
        calc_histgram(lt_peaks, h1high, h1low, h1vol, lt_period, lt_offset, InpBinRange * 16)
        mt_offset = _int(MathRound(_fdiv(h1low[ArrayMinimum(h1low, 0, mt_period)], Point())))
        calc_histgram(mt_peaks, h1high, h1low, h1vol, mt_period, mt_offset, InpBinRange * 8, mt_period)
        return True
    return False

def calc_histgram(peaks, hi, lo, vol, len_, offset, binRange, barcount=None):
    factor = zoom_out_factor
    if barcount == 0:
        barcount = len_
    work = Arr(0, 0, dims=(2,))
    binRangeZO = binRange * factor
    limit = _int(MathRound(_fdiv(hi[ArrayMaximum(hi, 0, barcount)], Point())))
    steps = _int(MathRound(_fdiv(limit - offset, binRange))) + 1
    stepsZO = _int(MathRound(_fdiv(limit - offset, binRangeZO))) + 1
    vh = Arr(0, 0)
    vhZO = Arr(0, 0)
    ArrayResize(vh, steps)
    ArrayInitialize(vh, 0)
    ArrayResize(vhZO, stepsZO)
    ArrayInitialize(vhZO, 0)
    for j in range(barcount - 1, 0 - 1, -1):
        v = 1
        if InpUsingVolumeWeight:
            v = _int(MathRound(MathSqrt(MathMin(vol[j], 1))))
        l = _int(MathRound(_fdiv(lo[j], Point())))
        h = _int(MathRound(_fdiv(hi[j], Point())))
        min_ = _int(MathRound(_fdiv(l - offset, binRange)))
        max_ = _int(MathRound(_fdiv(h - offset, binRange)))
        minZO = _int(MathRound(_fdiv(l - offset, binRangeZO)))
        maxZO = _int(MathRound(_fdiv(h - offset, binRangeZO)))
        for k in range(min_, max_ + 1):
            vh[k] += v
        for k in range(minZO, maxZO + 1):
            vhZO[k] += v
    peak_count = find_peaks(work, vhZO, stepsZO, binRangeZO)
    for j in range(0, peak_count):
        base = MathMin(steps - 1, work[j][1] * factor)
        max_ = vh[base]
        peak = base
        for k in range(0, factor):
            if (steps - 1) < (base + k):
                break
            if max_ < vh[base + k]:
                max_ = vh[base + k]
                peak = base + k
        work[j][1] = peak
    cnt = 0
    for j in range(peak_count - 1, 0 - 1, -1):
        cnt += 1
        ArrayResize(peaks, cnt)
        peaks[cnt - 1] = _int(MathRound(offset + (vh[work[j][1]] * binRange) + (binRange / 2)))
    return peak_count

def find_peaks(peaks, vh, steps, binrange):
    if steps <= 10:
        ArrayResize(peaks, 1)
        peaks[0][1] = ArrayMaximum(vh)
        peaks[0][0] = vh[peaks[0][1]]
        return 1
    count = 0
    for i in range(2, steps - 2):
        max_ = MathMax(MathMax(MathMax(MathMax(vh[i - 2], vh[i - 1]), vh[i]), vh[i + 1]), vh[i + 2])
        if vh[i] == max_:
            count += 1
            ArrayResize(peaks, count)
            peaks[count - 1][0] = vh[i]
            peaks[count - 1][1] = i
    if count > 1:
        ArraySort(peaks)
    return count

def TimeHour_u(t):
    tm = MqlDateTime()
    TimeToStruct(t, tm)
    return tm.hour


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PeakLinesByPriceHistogram(_MQL5Indicator):
    name = 'peak_lines_by_price_histogram'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBinRange': 2.5,  # Bin range of price histogram
        'InpCalcTime': 4,  # Calculation Time(hour)
        'InpShortTermPeriod': 3,  # Short term period(day)
        'InpMediumTermPeriod': 7,  # Medium term period(day)
        'InpLongTermPeriod': 26,  # Long term period(day)
        'InpUsingVolumeWeight': True,  # Using TickVolume
    }

