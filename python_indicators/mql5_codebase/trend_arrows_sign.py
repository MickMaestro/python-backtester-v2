"""trend_arrows_sign — converted from MQL5: MQL5 Indicators/trend_arrows_sign/trend_arrows_sign.mq5

Copyright: Copyright © 2012, Vladimir Mametov; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Vladimir Mametov', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Buy trend_arrows signal', 2: 'Sell trend_arrows signal'}, 'levels': [], 'description': [], 'name': 'trend_arrows_sign', 'source': 'MQL5 Indicators/trend_arrows_sign/trend_arrows_sign.mq5', 'folder': 'trend_arrows_sign', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 15, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'iFullPeriods', 'py': 'iFullPeriods', 'param': 'iFullPeriods', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 15)  # Период индикатора
iFullPeriods = _input('iFullPeriods', 1)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
arr = Arr(0, 0)
boolp1 = False
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = _int(iPeriod + iFullPeriods)
    ATR_Period = 15
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    ArrayResize(arr, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'trend_arrows(', _str(iPeriod), ', ', _str(iFullPeriods), ', ', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 3 * min_rates_total)
    ArraySetAsSeries(SignUp, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    SetIndexBuffer(1, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 3 * min_rates_total)
    ArraySetAsSeries(SignDown, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_TrendDown_prev, _s_OnCalculate_TrendUp_prev, boolp1
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    ATR = Arr(0, 0.0)
    TrendUp = 0.0
    TrendDown = 0.0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        tms1 = rates_total - 2 - min_rates_total
        while not isDelimeter(Period(), time, tms1):
            tms1 -= 1
        boolp1 = (tms1 != 0)
        tms1 -= 1
        for rrr in range(0, _int(iPeriod)):
            while not isDelimeter(Period(), time, tms1):
                tms1 -= 1
            tms1 -= 1
        tms1 += 1
        limit = tms1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        TrendUp = 0.0
        TrendDown = 0.0
        SignUp[bar] = 0.0
        SignDown[bar] = 0.0
        HH = AverageHigh(high, time, bar)
        LL = AverageLow(low, time, bar)
        if close[bar] > HH:
            TrendUp = LL
        else:
            if close[bar] < LL:
                TrendDown = HH
            else:
                if _s_OnCalculate_TrendDown_prev:
                    TrendDown = HH
                if _s_OnCalculate_TrendUp_prev:
                    TrendUp = LL
        if (not _s_OnCalculate_TrendUp_prev) and TrendUp:
            SignUp[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if (not _s_OnCalculate_TrendDown_prev) and TrendDown:
            SignDown[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_TrendUp_prev = TrendUp
            _s_OnCalculate_TrendDown_prev = TrendDown
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def AverageHigh(High, Time, index):
    global boolp1
    hhv = 0.0
    ret = 0.0
    nbars = index
    max_ = _int(iPeriod + iFullPeriods)
    boolp1 = False
    for iii in range(0, max_):
        while not isDelimeter(Period(), Time, nbars):
            nbars += 1
        if not boolp1:
            boolp1 = (nbars != 0)
        arr[iii] = nbars
        nbars += 1
    for count in range(_int(iPeriod - 1), 0, -1):
        hhv = High[ArrayMaximum(High, arr[count - 1] + 1, arr[count] - arr[count - 1])]
        ret += hhv
    if iFullPeriods == 1:
        hhv = High[ArrayMaximum(High, arr[iPeriod - 1] + 1, arr[iPeriod] - arr[iPeriod - 1])]
        ret += hhv
        ret = _fdiv(ret, NormalizeDouble(iPeriod, 0))
    else:
        hhv = High[ArrayMaximum(High, index, arr[0] - index)]
        ret += hhv
        ret = _fdiv(ret, NormalizeDouble(iPeriod, 0))
    return ret

def AverageLow(Low, Time, index):
    global boolp1
    llv = 0.0
    ret = 0.0
    nbars = index
    max_ = _int(iPeriod + iFullPeriods)
    boolp1 = False
    for iii in range(0, max_):
        while not isDelimeter(Period(), Time, nbars):
            nbars += 1
        if not boolp1:
            boolp1 = (nbars != 0)
        arr[iii] = nbars
        nbars += 1
    for count in range(_int(iPeriod - 1), 0, -1):
        llv = Low[ArrayMinimum(Low, arr[count - 1] + 1, arr[count] - arr[count - 1])]
        ret += llv
    if iFullPeriods == 1:
        llv = Low[ArrayMinimum(Low, arr[iPeriod - 1] + 1, arr[iPeriod] - arr[iPeriod - 1])]
        ret += llv
        ret = _fdiv(ret, NormalizeDouble(iPeriod, 0))
    else:
        llv = Low[ArrayMinimum(Low, index, arr[0] - index)]
        ret += llv
        ret = _fdiv(ret, NormalizeDouble(iPeriod, 0))
    return ret

def isDelimeter(TimFrame, Time, index):
    tm = MqlDateTime()
    TimeToStruct(Time[index], tm)
    blper = False
    _sw1 = TimFrame
    if _sw1 == PERIOD_M1:
        blper = tm.min == 0
    elif _sw1 == PERIOD_M2:
        blper = tm.min == 0
    elif _sw1 == PERIOD_M3:
        blper = tm.min == 0
    elif _sw1 == PERIOD_M4:
        blper = tm.min == 0
    elif _sw1 == PERIOD_M5:
        blper = tm.min == 0
    elif _sw1 == PERIOD_M6:
        blper = tm.min == 0
    elif _sw1 == PERIOD_M10:
        blper = tm.min == 0
    elif _sw1 == PERIOD_M12:
        blper = tm.min == 0
    elif _sw1 == PERIOD_M15:
        blper = tm.min == 0
    elif _sw1 == PERIOD_M20:
        blper = tm.min == 0
    elif _sw1 == PERIOD_M30:
        blper = tm.min == 0 and MathMod(tm.hour, 4.0) == 0.0
    elif _sw1 == PERIOD_H1:
        blper = tm.min == 0 and MathMod(tm.hour, 4.0) == 0.0
    elif _sw1 == PERIOD_H2:
        blper = tm.min == 0 and MathMod(tm.hour, 4.0) == 0.0
    elif _sw1 == PERIOD_H3:
        blper = tm.min == 0 and MathMod(tm.hour, 4.0) == 0.0
    elif _sw1 == PERIOD_H4:
        blper = tm.min == 0 and tm.hour == 0
    elif _sw1 == PERIOD_H6:
        blper = tm.min == 0 and tm.hour == 0
    elif _sw1 == PERIOD_H8:
        blper = tm.min == 0 and tm.hour == 0
    elif _sw1 == PERIOD_H12:
        blper = tm.min == 0 and tm.hour == 0
    elif _sw1 == PERIOD_D1:
        blper = tm.day_of_week == 1 and tm.hour == 0
    elif _sw1 == PERIOD_W1:
        tm2 = MqlDateTime()
        TimeToStruct(Time[index + 1], tm2)
        blper = (tm.day == 1 or (tm.day == 2 and tm2.day != 1)) or (tm.day == 3 and tm2.day != 2)
    elif _sw1 == PERIOD_MN1:
        tm2 = MqlDateTime()
        TimeToStruct(Time[index + 1], tm2)
        blper = (tm.day == 1 or (tm.day == 2 and tm2.day != 1)) or (tm.day == 3 and tm2.day != 2)
    return blper

# ---- static local variables
_s_OnCalculate_TrendUp_prev = 0.0
_s_OnCalculate_TrendDown_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendArrowsSign(_MQL5Indicator):
    name = 'trend_arrows_sign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 15,  # Период индикатора
        'iFullPeriods': 1,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

