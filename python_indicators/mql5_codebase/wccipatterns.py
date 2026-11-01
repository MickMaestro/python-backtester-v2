"""wccipatterns — converted from MQL5: MQL5 Indicators/WcciPatterns/wccipatterns.mq5

The Woodies CCI Paterns indicator
Detailed description of the indicator work is in the code of this indicator!!!
The indicator signals identified by numbers from 1 to 8;
the green color palette is used for the uptrend trading signals,
the red for the downtrend, the blue for the TLB and HTLB;
Copyright: Copyright © 2009, Yuri Ershtad

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Yuri Ershtad', 'link': '', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [7451452], 2: [17919], 3: [16760576], 4: [6053069], 5: [4678655], 6: [3329330], 7: [5275647], 8: [255]}, 'widths': {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3}, 'styles': {}, 'labels': {1: 'Zero-line Reject (ZLR), trend', 2: 'Shamu Trade, counter-trend', 3: 'Trend Line Break (TLB), both', 4: 'Vegas Trade (VT), counter-trend', 5: 'Ghost Trade, counter-trend', 6: 'Reverse Divergence, trend', 7: 'Hook from Extremes (HFE), counter-trend', 8: 'Exit signal'}, 'levels': [], 'description': ['The Woodies CCI Paterns indicator', 'Detailed description of the indicator work is in the code of this indicator!!!', 'The indicator signals identified by numbers from 1 to 8;', 'the green color palette is used for the uptrend trading signals,', 'the red for the downtrend, the blue for the TLB and HTLB;'], 'name': 'wccipatterns', 'source': 'MQL5 Indicators/WcciPatterns/wccipatterns.mq5', 'folder': 'WcciPatterns', 'inputs': [{'mql': 'fastPeriod', 'py': 'fastPeriod', 'param': 'fastPeriod', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'slowPeriod', 'py': 'slowPeriod', 'param': 'slowPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
fastPeriod = _input('fastPeriod', 6)
slowPeriod = _input('slowPeriod', 14)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ZlrBuffer = Arr(0, 0.0)  # 1. Zero-line Reject (ZLR)      -- trend
ShamuBuffer = Arr(0, 0.0)  # 2. Shamu Trade                 -- counter
TlbBuffer = Arr(0, 0.0)  # 3. Trend Line Break (TLB/HTLB) -- both
VegasBuffer = Arr(0, 0.0)  # 4. Vegas Trade (VT)			         -- counter
GhostBuffer = Arr(0, 0.0)  # 5. Ghost Trade                 -- counter
RevdevBuffer = Arr(0, 0.0)  # 6. Reverse Divergence          -- trend
HooksBuffer = Arr(0, 0.0)  # 7. Hook from Extremes (HFE)    -- counter
ExitBuffer = Arr(0, 0.0)  # 8. Exit signals
FCCIBuffer = Arr(0, 0.0)  # 9. Буфер для быстрого CCI
SCCIBuffer = Arr(0, 0.0)  # 10. Буфер для медленного CCI
min_rates_total = 0
FCCI_Handle = 0
SCCI_Handle = 0

def OnInit():
    global FCCI_Handle, SCCI_Handle, min_rates_total
    min_rates_total = _int(MathMax(fastPeriod, slowPeriod) + 20)
    FCCI_Handle = iCCI(None, 0, fastPeriod, PRICE_CLOSE)
    if FCCI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iCCI fast indicator')
    SCCI_Handle = iCCI(None, 0, slowPeriod, PRICE_CLOSE)
    if SCCI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iCCI slow indicator')
    IndicatorInit(0, Shift, min_rates_total, EMPTY_VALUE, 140, ZlrBuffer)
    IndicatorInit(1, Shift, min_rates_total, EMPTY_VALUE, 141, ShamuBuffer)
    IndicatorInit(2, Shift, min_rates_total, EMPTY_VALUE, 142, TlbBuffer)
    IndicatorInit(3, Shift, min_rates_total, EMPTY_VALUE, 143, VegasBuffer)
    IndicatorInit(4, Shift, min_rates_total, EMPTY_VALUE, 144, GhostBuffer)
    IndicatorInit(5, Shift, min_rates_total, EMPTY_VALUE, 145, RevdevBuffer)
    IndicatorInit(6, Shift, min_rates_total, EMPTY_VALUE, 146, HooksBuffer)
    IndicatorInit(7, Shift, min_rates_total, EMPTY_VALUE, 251, ExitBuffer)
    SetIndexBuffer(8, FCCIBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(FCCIBuffer, True)
    SetIndexBuffer(9, SCCIBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(SCCIBuffer, True)
    short_name = 'Woodies CCI Paterns (' + _str(fastPeriod) + ',' + _str(slowPeriod) + ',' + _str(Shift) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def IndicatorInit(number, shift, drawbegin, empty_value, arrow, Arrow):
    SetIndexBuffer(number, Arrow, INDICATOR_DATA)
    PlotIndexSetInteger(number, PLOT_SHIFT, shift)
    PlotIndexSetInteger(number, PLOT_DRAW_BEGIN, drawbegin)
    PlotIndexSetDouble(number, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(number, PLOT_ARROW, arrow)
    ArraySetAsSeries(Arrow, True)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if (BarsCalculated(SCCI_Handle) < rates_total or BarsCalculated(FCCI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - min_rates_total - 1
    else:
        to_copy = rates_total - prev_calculated
        limit = rates_total - prev_calculated
    if CopyBuffer(FCCI_Handle, 0, 0, to_copy, FCCIBuffer) <= 0:
        return 0
    if CopyBuffer(SCCI_Handle, 0, 0, to_copy, SCCIBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        delta = 25
        level = 100
        slowCCI = Arr(20, 0.0, dyn=False)
        fastCCI = Arr(20, 0.0, dyn=False)
        up = 0
        dn = 0
        upnt = 5
        dpnt = 5
        ArrayCopy(fastCCI, FCCIBuffer, 0, bar, 20)
        ArrayCopy(slowCCI, SCCIBuffer, 0, bar, 20)
        for a in range(0, 9):
            if slowCCI[a] > 0:
                up += 1
            else:
                dn += 1
        delta = 20
        level = 80
        ZlrBuffer[bar] = EMPTY_VALUE
        if ((((dn >= 6 and slowCCI[0] < slowCCI[1]) and slowCCI[2] < slowCCI[1]) and MathAbs(slowCCI[0]) < level) and MathAbs(slowCCI[1]) < level) and MathAbs(slowCCI[1] - slowCCI[2]) > delta:
            ZlrBuffer[bar] = High[bar] + (upnt * Point())
            upnt += 5
        if ((((up >= 6 and slowCCI[0] > slowCCI[1]) and slowCCI[2] > slowCCI[1]) and MathAbs(slowCCI[0]) < level) and MathAbs(slowCCI[1]) < level) and MathAbs(slowCCI[1] - slowCCI[2]) > delta:
            ZlrBuffer[bar] = Low[bar] - (dpnt * Point())
            dpnt += 5
        delta = 15
        level = 50
        ShamuBuffer[bar] = EMPTY_VALUE
        if ((((((dn >= 6 and slowCCI[0] > (slowCCI[1] + delta)) and slowCCI[1] < slowCCI[2]) and slowCCI[2] > slowCCI[3]) and slowCCI[1] <= level) and slowCCI[1] >= (-level)) and slowCCI[2] <= level) and slowCCI[2] >= (-level):
            ShamuBuffer[bar] = Low[bar] - (dpnt * Point())
            dpnt += 5
        if ((((((up >= 6 and slowCCI[0] < (slowCCI[1] - delta)) and slowCCI[1] > slowCCI[2]) and slowCCI[2] < slowCCI[3]) and slowCCI[1] >= (-level)) and slowCCI[1] <= level) and slowCCI[2] >= (-level)) and slowCCI[2] <= level:
            ShamuBuffer[bar] = High[bar] + (upnt * Point())
            upnt += 5
        delta = 25
        level = 100
        TlbBuffer[bar] = EMPTY_VALUE
        min1 = 0.0
        min2 = 0.0
        min3 = 0.0
        max1 = 0.0
        max2 = 0.0
        max3 = 0.0
        tmin1 = 0
        tmin2 = 0
        tmin3 = 0
        tmax1 = 0
        tmax2 = 0
        tmax3 = 0
        kmin = 0.0
        kmax = 0.0
        line = 0.0
        for a in range(0, 18):
            if slowCCI[a] <= slowCCI[a + 1] and slowCCI[a + 1] >= slowCCI[a + 2]:
                if max1 != 0 and max2 == 0:
                    max2 = slowCCI[a + 1]
                    tmax2 = Time[a + 1 + bar]
                    kmax = _fdiv(100 * (max2 - max1), tmax2 - tmax1)
                if max1 == 0:
                    max1 = slowCCI[a + 1]
                    tmax1 = Time[a + 1 + bar]
            if slowCCI[a] >= slowCCI[a + 1] and slowCCI[a + 1] <= slowCCI[a + 2]:
                if min1 != 0 and min2 == 0:
                    min2 = slowCCI[a + 1]
                    tmin2 = Time[a + 1 + bar]
                    kmin = _fdiv(100 * (min2 - min1), tmin2 - tmin1)
                if min1 == 0:
                    min1 = slowCCI[a + 1]
                    tmin1 = Time[a + 1 + bar]
        if (kmax != 0 and dn >= 6) and (max1 < (-level) or max2 < (-level)):
            line = (((Time[bar] - tmax1) * kmax) / 100) + max1
            if slowCCI[1] < line and slowCCI[0] >= line:
                TlbBuffer[bar] = Low[bar] - (dpnt * Point())
                dpnt += 5
        if (kmin != 0 and up >= 6) and (min1 > level or min2 > level):
            line = (((Time[bar] - tmin1) * kmin) / 100) + min1
            if slowCCI[1] > line and slowCCI[0] <= line:
                TlbBuffer[bar] = High[bar] + (upnt * Point())
                upnt += 5
        if (kmin != 0 and dn >= 6) and (min1 < (-level) or min2 < (-level)):
            line = (((Time[bar] - tmin1) * kmin) / 100) + min1
            if slowCCI[1] > line and slowCCI[0] < line:
                TlbBuffer[bar] = High[bar] + (upnt * Point())
                upnt = 5
        if (kmax != 0 and up >= 6) and (max1 > level or max2 > level):
            line = (((Time[bar] - tmax1) * kmax) / 100) + max1
            if slowCCI[1] < line and slowCCI[0] > line:
                TlbBuffer[bar] = Low[bar] - (dpnt * Point())
                dpnt = 5
        delta = 10
        limit = 200
        max1 = 0.0
        max2 = 0.0
        tmax1 = 0
        tmax2 = 0
        min1 = 0.0
        min2 = 0.0
        tmin1 = 0
        tmin2 = 0
        VegasBuffer[bar] = EMPTY_VALUE
        if dn >= 6:
            for a in range(13, 1 - 1, -1):
                if ((slowCCI[a] <= slowCCI[a + 1] and slowCCI[a + 1] >= slowCCI[a + 2]) and min1 != 0) and max1 == 0:
                    max1 = slowCCI[a + 1]
                    tmax1 = a + 1
                if (((slowCCI[a] >= slowCCI[a + 1] and slowCCI[a + 1] <= slowCCI[a + 2]) and min1 == 0) and slowCCI[a + 1] <= (-limit)) and (a + 1) >= 5:
                    min1 = slowCCI[a + 1]
                    tmin1 = a + 1
        if up >= 6:
            for a in range(13, 1 - 1, -1):
                if ((slowCCI[a] >= slowCCI[a + 1] and slowCCI[a + 1] <= slowCCI[a + 2]) and min2 != 0) and max2 == 0:
                    min2 = slowCCI[a + 1]
                    tmin2 = a + 1
                if (((slowCCI[a] <= slowCCI[a + 1] and slowCCI[a + 1] >= slowCCI[a + 2]) and max2 == 0) and slowCCI[a + 1] >= limit) and (a + 1) >= 5:
                    max2 = slowCCI[a + 1]
                    tmax2 = a + 1
        if (((dn >= 6 and max1 != 0) and slowCCI[1] < max1) and slowCCI[0] >= max1) and (slowCCI[0] - delta) > slowCCI[1]:
            VegasBuffer[bar] = Low[bar] - (dpnt * Point())
            dpnt += 5
        if (((up >= 6 and min2 != 0) and slowCCI[1] > min2) and slowCCI[0] <= min2) and (slowCCI[0] + delta) < slowCCI[1]:
            VegasBuffer[bar] = High[bar] + (upnt * Point())
            upnt += 5
        delta = 15
        level = 50
        max1 = 0.0
        max2 = 0.0
        max3 = 0.0
        tmax1 = 0
        tmax2 = 0
        tmax3 = 0
        min1 = 0.0
        min2 = 0.0
        min3 = 0.0
        tmin1 = 0
        tmin2 = 0
        tmin3 = 0
        GhostBuffer[bar] = EMPTY_VALUE
        if up >= 6:
            for a in range(0, 18):
                if slowCCI[a] <= slowCCI[a + 1] and slowCCI[a + 1] >= slowCCI[a + 2]:
                    if max2 != 0 and max3 == 0:
                        max3 = slowCCI[a + 1]
                    if max1 != 0 and max2 == 0:
                        max2 = slowCCI[a + 1]
                    if max1 == 0:
                        max1 = slowCCI[a + 1]
        if dn >= 6:
            for a in range(0, 18):
                if slowCCI[a] >= slowCCI[a + 1] and slowCCI[a + 1] <= slowCCI[a + 2]:
                    if min2 != 0 and min3 == 0:
                        min3 = slowCCI[a + 1]
                    if min1 != 0 and min2 == 0:
                        min2 = slowCCI[a + 1]
                    if min1 == 0:
                        min1 = slowCCI[a + 1]
        if ((((((dn >= 6 and min3 != 0) and min1 > min2) and min3 > (min2 + delta)) and min1 < 0) and (slowCCI[0] - delta) > min1) and slowCCI[0] > slowCCI[1]) and (not ((slowCCI[1] - delta) > min1)):
            GhostBuffer[bar] = Low[bar] - (dpnt * Point())
            dpnt += 5
        if ((((((up >= 6 and max3 != 0) and max1 < max2) and max3 < (max2 - delta)) and max1 > 0) and (slowCCI[0] + delta) < max1) and slowCCI[0] < slowCCI[1]) and (not ((slowCCI[1] + delta) < max1)):
            GhostBuffer[bar] = High[bar] + (upnt * Point())
            upnt += 5
        delta = 20
        level = 70
        max1 = 0.0
        max2 = 0.0
        tmax1 = 0
        tmax2 = 0
        min1 = 0.0
        min2 = 0.0
        tmin1 = 0
        tmin2 = 0
        RevdevBuffer[bar] = EMPTY_VALUE
        if dn >= 6:
            for a in range(0, 18):
                if slowCCI[a] <= slowCCI[a + 1] and slowCCI[a + 1] >= slowCCI[a + 2]:
                    if (max1 != 0 and tmax1 < 3) and max2 == 0:
                        max2 = slowCCI[a + 1]
                        tmax2 = a + 1
                    if max1 == 0:
                        max1 = slowCCI[a + 1]
                        tmax1 = a + 1
        if up >= 6:
            for a in range(0, 18):
                if slowCCI[a] >= slowCCI[a + 1] and slowCCI[a + 1] <= slowCCI[a + 2]:
                    if (min1 != 0 and tmin1 < 3) and min2 == 0:
                        min2 = slowCCI[a + 1]
                        tmin2 = a + 1
                    if min1 == 0:
                        min1 = slowCCI[a + 1]
                        tmin1 = a + 1
        if (((((((dn >= 6 and max1 <= 0) and max2 != 0) and max1 > max2) and max1 >= (-level)) and (tmax2 - tmax1) >= 3) and (slowCCI[0] + delta) < max1) and slowCCI[0] < slowCCI[1]) and (not ((slowCCI[1] + delta) < max1)):
            RevdevBuffer[bar] = High[bar] + (upnt * Point())
            upnt += 5
        if (((((((up >= 6 and min1 >= 0) and min2 != 0) and min1 < min2) and min1 <= level) and (tmin2 - tmin1) >= 3) and (slowCCI[0] - delta) > min1) and slowCCI[0] > slowCCI[1]) and (not ((slowCCI[1] - delta) > min1)):
            RevdevBuffer[bar] = Low[bar] - (dpnt * Point())
            dpnt += 5
        delta = 10
        level = 200
        HooksBuffer[bar] = EMPTY_VALUE
        if ((dn >= 6 and slowCCI[1] <= (-level)) and slowCCI[0] > (-level)) and slowCCI[1] < (slowCCI[0] - delta):
            HooksBuffer[bar] = Low[bar] - (dpnt * Point())
            dpnt += 5
        if ((up >= 6 and slowCCI[1] >= level) and slowCCI[0] < level) and slowCCI[1] > (slowCCI[0] - delta):
            HooksBuffer[bar] = High[bar] + (upnt * Point())
            upnt += 5
        if HooksBuffer[bar] != EMPTY_VALUE:
            if up >= 6:
                ExitBuffer[bar] = High[bar] + (upnt * Point())
                upnt += 5
            if dn >= 6:
                ExitBuffer[bar] = Low[bar] - (dpnt * Point())
                dpnt += 5
        if TlbBuffer[bar] != EMPTY_VALUE:
            if up >= 6 and TlbBuffer[bar] > High[bar]:
                ExitBuffer[bar] = High[bar] + (upnt * Point())
                upnt += 5
            if dn >= 6 and TlbBuffer[bar] < Low[bar]:
                ExitBuffer[bar] = Low[bar] - (dpnt * Point())
                dpnt += 5
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wccipatterns(_MQL5Indicator):
    name = 'wccipatterns'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'fastPeriod': 6,
        'slowPeriod': 14,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

