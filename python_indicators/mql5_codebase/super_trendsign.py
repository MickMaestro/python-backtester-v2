"""super_trendsign — converted from MQL5: MQL5 Indicators/Super_TrendSign/super_trendsign.mq5

Copyright: Copyright © 2005, Jason Robinson (jnrtrading).; Link: http://www.jnrtrading.co.uk; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Jason Robinson (jnrtrading).', 'link': 'http://www.jnrtrading.co.uk', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [36095], 2: [13422920]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Sell Super_Trend signal', 2: 'Buy Super_Trend signal'}, 'levels': [], 'description': [], 'name': 'super_trendsign', 'source': 'MQL5 Indicators/Super_TrendSign/super_trendsign.mq5', 'folder': 'Super_TrendSign', 'inputs': [{'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'int', 'default': 14, 'label': 'Период индикатора CCI', 'sinput': False}, {'mql': 'Level', 'py': 'Level', 'param': 'Level', 'type': 'int', 'default': 0, 'label': 'Уровень срабатывания CCI', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCIPeriod = _input('CCIPeriod', 14)  # Период индикатора CCI
Level = _input('Level', 0)  # Уровень срабатывания CCI
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
UpDownShift = 0.0
min_rates_total = 0
CCI_Handle = 0
ATR_Handle = 0

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
    global ATR_Handle, CCI_Handle, UpDownShift, min_rates_total
    ATR_Period = 15
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    CCI_Handle = iCCI(None, 0, CCIPeriod, PRICE_TYPICAL)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CCI')
        return INIT_FAILED
    min_rates_total = CCIPeriod + 1
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    UpDownShift = GetUpDownShift(Period()) * Point()
    shortname = Box("")
    StringConcatenate(shortname, 'Super_Trend(', _str(CCIPeriod), ', ', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(BuyBuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_TrendDown_prev, _s_OnCalculate_TrendUp_prev
    if (BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(CCI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    CCI = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    cciTrendNow = 0.0
    cciTrendPrevious = 0.0
    TrendUp = 0.0
    TrendDown = 0.0
    limit = 0
    to_copy = 0
    bar = 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(CCI, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    to_copy += 1
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        cciTrendNow = CCI[bar] + 70
        cciTrendPrevious = CCI[bar + 1] + 70
        if cciTrendNow >= Level and cciTrendPrevious < Level:
            _s_OnCalculate_TrendUp_prev = _s_OnCalculate_TrendDown_prev
        if cciTrendNow <= Level and cciTrendPrevious > Level:
            _s_OnCalculate_TrendDown_prev = _s_OnCalculate_TrendUp_prev
        if cciTrendNow > Level:
            TrendDown = 0.0
            TrendUp = low[bar] - UpDownShift
            if close[bar] < open[bar] and _s_OnCalculate_TrendDown_prev != _s_OnCalculate_TrendUp_prev:
                TrendUp = _s_OnCalculate_TrendUp_prev
            if TrendUp < _s_OnCalculate_TrendUp_prev and _s_OnCalculate_TrendDown_prev != _s_OnCalculate_TrendUp_prev:
                TrendUp = _s_OnCalculate_TrendUp_prev
            if high[bar] < high[bar + 1] and _s_OnCalculate_TrendDown_prev != _s_OnCalculate_TrendUp_prev:
                TrendUp = _s_OnCalculate_TrendUp_prev
        if cciTrendNow < Level:
            TrendUp = 0.0
            TrendDown = high[bar] + UpDownShift
            if close[bar] > open[bar] and _s_OnCalculate_TrendUp_prev != _s_OnCalculate_TrendDown_prev:
                _s_OnCalculate_TrendDown_prev = _s_OnCalculate_TrendDown_prev
            if TrendDown > _s_OnCalculate_TrendDown_prev and _s_OnCalculate_TrendDown_prev != _s_OnCalculate_TrendUp_prev:
                TrendDown = _s_OnCalculate_TrendDown_prev
            if low[bar] > low[bar + 1] and _s_OnCalculate_TrendUp_prev != _s_OnCalculate_TrendDown_prev:
                TrendDown = _s_OnCalculate_TrendDown_prev
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_TrendDown_prev and TrendUp:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_TrendUp_prev and TrendDown:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_TrendUp_prev = TrendUp
            _s_OnCalculate_TrendDown_prev = TrendDown
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_TrendUp_prev = 0.0
_s_OnCalculate_TrendDown_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperTrendsign(_MQL5Indicator):
    name = 'super_trendsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCIPeriod': 14,  # Период индикатора CCI
        'Level': 0,  # Уровень срабатывания CCI
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

