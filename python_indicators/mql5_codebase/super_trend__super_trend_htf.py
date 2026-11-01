"""super_trend — converted from MQL5: MQL5 Indicators/Super_Trend_HTF/super_trend.mq5

Copyright: Copyright © 2005, Jason Robinson (jnrtrading).; Link: http://www.jnrtrading.co.uk; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Jason Robinson (jnrtrading).', 'link': 'http://www.jnrtrading.co.uk', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [7451452], 2: [255], 3: [13422920], 4: [36095]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Super_Trend Up', 2: 'Super_Trend Down', 3: 'Buy Super_Trend signal', 4: 'Sell Super_Trend signal'}, 'levels': [], 'description': [], 'name': 'super_trend', 'source': 'MQL5 Indicators/Super_Trend_HTF/super_trend.mq5', 'folder': 'Super_Trend_HTF', 'inputs': [{'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'int', 'default': 14, 'label': 'Период индикатора CCI', 'sinput': False}, {'mql': 'Level', 'py': 'Level', 'param': 'Level', 'type': 'int', 'default': 0, 'label': 'Уровень срабатывания CCI', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCIPeriod = _input('CCIPeriod', 14)  # Период индикатора CCI
Level = _input('Level', 0)  # Уровень срабатывания CCI
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
TrendUp = Arr(0, 0.0)
TrendDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
UpDownShift = 0.0
min_rates_total = 0
CCI_Handle = 0

def GetUpDownShift(Timeframe):
    _sw1 = Timeframe
    if _sw1 == PERIOD_M1:
        return 3
    elif _sw1 == PERIOD_M2:
        return 3
    elif _sw1 == PERIOD_M3:
        return 4
    elif _sw1 == PERIOD_M4:
        return 5
    elif _sw1 == PERIOD_M5:
        return 5
    elif _sw1 == PERIOD_M6:
        return 5
    elif _sw1 == PERIOD_M10:
        return 6
    elif _sw1 == PERIOD_M12:
        return 6
    elif _sw1 == PERIOD_M15:
        return 7
    elif _sw1 == PERIOD_M20:
        return 8
    elif _sw1 == PERIOD_M30:
        return 9
    elif _sw1 == PERIOD_H1:
        return 20
    elif _sw1 == PERIOD_H2:
        return 27
    elif _sw1 == PERIOD_H3:
        return 30
    elif _sw1 == PERIOD_H4:
        return 35
    elif _sw1 == PERIOD_H6:
        return 33
    elif _sw1 == PERIOD_H8:
        return 35
    elif _sw1 == PERIOD_H12:
        return 37
    elif _sw1 == PERIOD_D1:
        return 40
    elif _sw1 == PERIOD_W1:
        return 100
    elif _sw1 == PERIOD_MN1:
        return 120
    return 0

def OnInit():
    global CCI_Handle, UpDownShift, min_rates_total
    min_rates_total = CCIPeriod + 1
    CCI_Handle = iCCI(None, 0, CCIPeriod, PRICE_TYPICAL)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CCI')
        return INIT_FAILED
    UpDownShift = GetUpDownShift(Period()) * Point()
    shortname = Box("")
    StringConcatenate(shortname, 'Super_Trend(', _str(CCIPeriod), ', ', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
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
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(CCI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    CCI = Arr(0, 0.0)
    cciTrendNow = 0.0
    cciTrendPrevious = 0.0
    limit = 0
    to_copy = 0
    bar = 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(CCI, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    to_copy += 1
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SignUp[bar] = 0.0
        SignDown[bar] = 0.0
        SignUp[bar + 1] = 0.0
        SignDown[bar + 1] = 0.0
        cciTrendNow = CCI[bar] + 70
        cciTrendPrevious = CCI[bar + 1] + 70
        if cciTrendNow >= Level and cciTrendPrevious < Level:
            TrendUp[bar + 1] = TrendDown[bar + 1]
        if cciTrendNow <= Level and cciTrendPrevious > Level:
            TrendDown[bar + 1] = TrendUp[bar + 1]
        if cciTrendNow > Level:
            TrendDown[bar] = 0.0
            TrendUp[bar] = low[bar] - UpDownShift
            if close[bar] < open[bar] and TrendDown[bar + 1] != TrendUp[bar + 1]:
                TrendUp[bar] = TrendUp[bar + 1]
            if TrendUp[bar] < TrendUp[bar + 1] and TrendDown[bar + 1] != TrendUp[bar + 1]:
                TrendUp[bar] = TrendUp[bar + 1]
            if high[bar] < high[bar + 1] and TrendDown[bar + 1] != TrendUp[bar + 1]:
                TrendUp[bar] = TrendUp[bar + 1]
        if cciTrendNow < Level:
            TrendUp[bar] = 0.0
            TrendDown[bar] = high[bar] + UpDownShift
            if close[bar] > open[bar] and TrendUp[bar + 1] != TrendDown[bar + 1]:
                TrendDown[bar] = TrendDown[bar + 1]
            if TrendDown[bar] > TrendDown[bar + 1] and TrendDown[bar + 1] != TrendUp[bar + 1]:
                TrendDown[bar] = TrendDown[bar + 1]
            if low[bar] > low[bar + 1] and TrendUp[bar + 1] != TrendDown[bar + 1]:
                TrendDown[bar] = TrendDown[bar + 1]
        if TrendDown[bar + 1] != 0.0 and TrendUp[bar] != 0.0:
            SignUp[bar + 1] = TrendDown[bar + 1]
        if TrendUp[bar + 1] != 0.0 and TrendDown[bar] != 0.0:
            SignDown[bar + 1] = TrendUp[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperTrend(_MQL5Indicator):
    name = 'super_trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCIPeriod': 14,  # Период индикатора CCI
        'Level': 0,  # Уровень срабатывания CCI
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

