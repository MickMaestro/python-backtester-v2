"""j_tpo — converted from MQL5: MQL5 Indicators/J_TPO/j_tpo.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 65280, 8421376, 255, 2763429]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [0.5, 0.0, -0.5], 'description': [], 'name': 'j_tpo', 'source': 'MQL5 Indicators/J_TPO/j_tpo.mq5', 'folder': 'J_TPO', 'inputs': [{'mql': 'Len_', 'py': 'Len_', 'param': 'Len_', 'type': 'int', 'default': 14, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
Len_ = _input('Len_', 14)  # Smoothing period
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
ExtBuffer = Arr(0, 0.0)
ColorExtBuffer = Arr(0, 0.0)
Len = 0
LenM = 0
LenP = 0
Kf = 0.0
Kl = 0.0
arr0 = Arr(0, 0.0)
arr1 = Arr(0, 0.0)
arr2 = Arr(0, 0.0)
arr3 = Arr(0, 0.0)
Arr0 = Arr(0, 0.0)
Arr1 = Arr(0, 0.0)
Arr2 = Arr(0, 0.0)
Arr3 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global Kf, Kl, Len, LenM, LenP, min_rates_total
    Len = MathMax(Len_, 3)
    LenM = Len - 1
    LenP = LenM + 1
    k = LenP
    Kf = _fdiv(12, k * (k - 1) * (k + 1))
    Kl = (LenP + 1) * 0.5
    min_rates_total = (2 * Len) + 1
    size = Len + 2
    if ArrayResize(arr0, size) < size:
        Print('Failed to distribute the memory for arr0[] array')
        return -1
    if ArrayResize(arr1, size) < size:
        Print('Failed to distribute the memory for arr1[] array')
        return -1
    if ArrayResize(arr2, size) < size:
        Print('Failed to distribute the memory for arr2[] array')
        return -1
    if ArrayResize(arr3, size) < size:
        Print('Failed to distribute the memory for arr3[] array')
        return -1
    ArrayInitialize(arr0, 0)
    ArrayInitialize(arr1, 0)
    ArrayInitialize(arr2, 0)
    ArrayInitialize(arr3, 0)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, ColorExtBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    ArraySetAsSeries(ExtBuffer, True)
    ArraySetAsSeries(ColorExtBuffer, True)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Count, _s_OnCalculate_run_
    if rates_total < min_rates_total:
        return 0
    limit1 = 0
    limit2 = 0
    run = 0
    count = 0
    fff = 0
    numbx = 0
    ppp = 0
    rrr = 0
    sss = 0
    invelue1 = 0.0
    invelue = 0.0
    tmp2 = 0.0
    outvelue = 0.0
    tmp1 = 0.0
    tmp = 0.0
    max_ = 0.0
    value = 0.0
    series = 0.0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit1 = rates_total - min_rates_total - 1
        limit2 = limit1 - 1
        ArrayInitialize(arr0, 0)
        ArrayInitialize(arr1, 0)
        ArrayInitialize(arr2, 0)
        ArrayInitialize(arr3, 0)
        _s_OnCalculate_Count = 0
        _s_OnCalculate_run_ = 0
    else:
        limit1 = rates_total - prev_calculated
        limit2 = limit1
    ArrayCopy(arr0, Arr0, 0, 0, WHOLE_ARRAY)
    ArrayCopy(arr1, Arr1, 0, 0, WHOLE_ARRAY)
    ArrayCopy(arr2, Arr2, 0, 0, WHOLE_ARRAY)
    ArrayCopy(arr3, Arr3, 0, 0, WHOLE_ARRAY)
    count = _s_OnCalculate_Count
    run = _s_OnCalculate_run_
    for bar in range(limit1, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            ArrayCopy(Arr0, arr0, 0, 0, WHOLE_ARRAY)
            ArrayCopy(Arr1, arr1, 0, 0, WHOLE_ARRAY)
            ArrayCopy(Arr2, arr2, 0, 0, WHOLE_ARRAY)
            ArrayCopy(Arr3, arr3, 0, 0, WHOLE_ARRAY)
            _s_OnCalculate_Count = count
            _s_OnCalculate_run_ = run
        series = PriceSeries(IPC, bar, open, low, high, close)
        tmp2 = 0.0
        tmp1 = 0.0
        if not count:
            count = 1
            run = 0
            invelue = series
            arr0[count] = invelue
        else:
            if count <= LenP:
                count += 1
            else:
                count = LenP + 1
            invelue1 = invelue
            invelue = series
            if count > LenP:
                fff = 2
                for fff in range(fff, LenP + 1):
                    arr0[fff - 1] = arr0[fff]
                else:
                    fff = _range_end(fff, LenP + 1, 1)
                arr0[LenP] = invelue
            else:
                arr0[count] = invelue
            if LenM >= count and invelue1 != invelue:
                run = 1
            if LenM == count and (not run):
                count = 0
        if count >= LenP:
            rrr = 1
            for rrr in range(rrr, LenP + 1):
                arr1[rrr] = arr0[rrr]
                arr2[rrr] = rrr
                arr3[rrr] = rrr
            else:
                rrr = _range_end(rrr, LenP + 1, 1)
            ppp = 1
            for ppp in range(ppp, LenP):
                max_ = arr1[ppp]
                numbx = ppp
                fff = ppp + 1
                fff = ppp + 1
                for fff in range(fff, LenP + 1):
                    if arr1[fff] < max_:
                        max_ = arr1[fff]
                        numbx = fff
                else:
                    fff = _range_end(fff, LenP + 1, 1)
                tmp = arr1[ppp]
                arr1[ppp] = arr1[numbx]
                arr1[numbx] = tmp
                tmp = arr2[ppp]
                arr2[ppp] = arr2[numbx]
                arr2[numbx] = tmp
            else:
                ppp = _range_end(ppp, LenP, 1)
            ppp = 1
            while LenP > ppp:
                fff = ppp + 1
                tmp2 = 1.0
                tmp1 = arr3[ppp]
                while tmp2 != 0:
                    if arr1[ppp] != arr1[fff]:
                        if (fff - ppp) > 1:
                            tmp1 = _fdiv(tmp1, fff - ppp)
                            sss = ppp
                            sss = ppp
                            for sss in range(sss, fff):
                                arr3[sss] = tmp1
                            else:
                                sss = _range_end(sss, fff, 1)
                        tmp2 = 0.0
                    else:
                        tmp1 += arr3[fff]
                        fff = fff + 1
                ppp = fff
            tmp1 = 0.0
            ppp = 1
            for ppp in range(ppp, LenP + 1):
                tmp1 += (arr3[ppp] - Kl) * (arr2[ppp] - Kl)
            else:
                ppp = _range_end(ppp, LenP + 1, 1)
            outvelue = Kf * tmp1
        else:
            outvelue = 0.0
        value = outvelue
        if value == 0:
            value = 1e-05
        ExtBuffer[bar] = value
    for bar in range(limit2, 0 - 1, -1):
        ColorExtBuffer[bar] = 0.0
        if ExtBuffer[bar] > 0:
            if ExtBuffer[bar] > ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 1.0
            if ExtBuffer[bar] < ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 2.0
        if ExtBuffer[bar] < 0:
            if ExtBuffer[bar] < ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 3.0
            if ExtBuffer[bar] > ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 4.0
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

# ---- static local variables
_s_OnCalculate_Count = 0
_s_OnCalculate_run_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JTpo(_MQL5Indicator):
    name = 'j_tpo'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Len_': 14,  # Smoothing period
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
    }

