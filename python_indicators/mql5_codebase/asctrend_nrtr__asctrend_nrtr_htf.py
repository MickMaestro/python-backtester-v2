"""ASCtrend_NRTR — converted from MQL5: MQL5 Indicators/ASCtrend_NRTR_HTF/ASCtrend_NRTR.mq5

ASCtrend_NRTR
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16748574], 2: [255], 3: [16711680], 4: [16711935]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'ASCtrend NRTR Up', 2: 'ASCtrend NRTR Down', 3: 'ASCtrend Buy signal', 4: 'ASCtrend Sell signal'}, 'levels': [], 'description': ['ASCtrend_NRTR'], 'name': 'ASCtrend_NRTR', 'source': 'MQL5 Indicators/ASCtrend_NRTR_HTF/ASCtrend_NRTR.mq5', 'folder': 'ASCtrend_NRTR_HTF', 'inputs': [{'mql': 'RISK', 'py': 'RISK', 'param': 'RISK', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'AtrRatio', 'py': 'AtrRatio', 'param': 'AtrRatio', 'type': 'double', 'default': 0.24, 'label': 'коэфициент ATR удаления NRTR', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RISK = _input('RISK', 4)
AtrRatio = _input('AtrRatio', 0.24)  # коэфициент ATR удаления NRTR
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
TrendUp = Arr(0, 0.0)
TrendDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
min_rates_total = 0
x1 = 0
x2 = 0
value10 = 0
value11 = 0
WPR_Handle = Arr(3, 0, dyn=False)
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_total, value10, value11, x1, x2
    x1 = 67 + RISK
    x2 = 33 - RISK
    value10 = 2
    value11 = value10
    min_rates_total = MathMax(3 + (RISK * 2), 9) + 1
    AtrPeriod = 10
    min_rates_total = MathMax(min_rates_total, AtrPeriod)
    WPR_Handle[0] = iWPR(None, 0, 3)
    if WPR_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR 1')
    WPR_Handle[1] = iWPR(None, 0, 4)
    if WPR_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR 2')
    WPR_Handle[2] = iWPR(None, 0, 3 + (RISK * 2))
    if WPR_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR 3')
    ATR_Handle = iATR(None, 0, AtrPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
    SetIndexBuffer(0, TrendUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(TrendUp, True)
    SetIndexBuffer(1, TrendDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(TrendDown, True)
    SetIndexBuffer(2, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignUp, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    SetIndexBuffer(3, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignDown, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'ASCtrend_NRTR'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend_prev, value11
    if (((BarsCalculated(WPR_Handle[0]) < rates_total or BarsCalculated(WPR_Handle[1]) < rates_total) or BarsCalculated(WPR_Handle[2]) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    count = 0
    iii = 0
    trend = 0
    value2 = 0.0
    value3 = 0.0
    Vel = 0.0
    WPR = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    TrueCount = 0.0
    Range = 0.0
    AvgRange = 0.0
    MRO1 = 0.0
    MRO2 = 0.0
    newstop = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_trend_prev = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(WPR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        trend = _s_OnCalculate_trend_prev
        Range = 0.0
        AvgRange = 0.0
        count = bar
        for count in range(count, bar + 9 + 1):
            AvgRange = AvgRange + MathAbs(high[count] - low[count])
        else:
            count = _range_end(count, bar + 9 + 1, 1)
        Range = AvgRange / 10
        count = bar
        TrueCount = 0.0
        while count < (bar + 9) and TrueCount < 1:
            if MathAbs(open[count] - close[count + 1]) >= (Range * 2.0):
                TrueCount += 1
            count += 1
        if TrueCount >= 1:
            MRO1 = count
        else:
            MRO1 = -1.0
        count = bar
        TrueCount = 0.0
        while count < (bar + 6) and TrueCount < 1:
            if MathAbs(close[count + 3] - close[count]) >= (Range * 4.6):
                TrueCount += 1
            count += 1
        if TrueCount >= 1:
            MRO2 = count
        else:
            MRO2 = -1.0
        if MRO1 > -1:
            value11 = 0
        else:
            value11 = value10
        if MRO2 > -1:
            value11 = 1
        else:
            value11 = value10
        if CopyBuffer(WPR_Handle[value11], 0, bar, 1, WPR) <= 0:
            return 0
        value2 = 100 - MathAbs(WPR[0])
        SignUp[bar] = 0.0
        SignDown[bar] = 0.0
        value3 = 0.0
        if value2 < x2:
            iii = 1
            while (bar + iii) < rates_total:
                if CopyBuffer(WPR_Handle[value11], 0, bar + iii, 1, WPR) <= 0:
                    return 0
                Vel = 100 - MathAbs(WPR[0])
                if Vel >= x2 and Vel <= x1:
                    iii += 1
                else:
                    break
            if Vel > x1:
                value3 = high[bar] + (Range * 0.5)
                SignDown[bar] = value3
                trend = -1
        if value2 > x1:
            iii = 1
            while (bar + iii) < rates_total:
                if CopyBuffer(WPR_Handle[value11], 0, bar + iii, 1, WPR) <= 0:
                    return 0
                Vel = 100 - MathAbs(WPR[0])
                if Vel >= x2 and Vel <= x1:
                    iii += 1
                else:
                    break
            if Vel < x2:
                value3 = low[bar] - (Range * 0.5)
                SignUp[bar] = value3
                trend = 1
        TrendUp[bar] = 0.0
        TrendDown[bar] = 0.0
        if trend > 0:
            newstop = low[bar] - (AtrRatio * ATR[bar])
            if _s_OnCalculate_trend_prev > 0:
                if newstop > TrendUp[bar + 1]:
                    TrendUp[bar] = newstop
                else:
                    TrendUp[bar] = TrendUp[bar + 1]
            else:
                TrendUp[bar] = newstop
        if trend < 0:
            newstop = high[bar] + (AtrRatio * ATR[bar])
            if _s_OnCalculate_trend_prev < 0:
                if newstop < TrendDown[bar + 1]:
                    TrendDown[bar] = newstop
                else:
                    TrendDown[bar] = TrendDown[bar + 1]
            else:
                TrendDown[bar] = newstop
        if bar:
            _s_OnCalculate_trend_prev = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ASCtrendNRTR(_MQL5Indicator):
    name = 'ASCtrend_NRTR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RISK': 4,
        'AtrRatio': 0.24,  # коэфициент ATR удаления NRTR
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

