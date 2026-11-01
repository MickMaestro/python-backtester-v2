"""din_fibo_nex — converted from MQL5: MQL5 Indicators/Din_fibo_Nex_HTF/din_fibo_nex.mq5

Индикатор линии перемещения трейлинстопа
Copyright: Copyright © 2006, unknown author, get from kaizer, conversed by Rosh; Link: http://forum.alpari-idc.ru/profile.php?mode=viewprofile&u=4196161; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, unknown author, get from kaizer, conversed by Rosh', 'link': 'http://forum.alpari-idc.ru/profile.php?mode=viewprofile&u=4196161', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [8421376], 2: [128]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Din_fibo_Nex MaH', 2: 'Din_fibo_Nex MaL'}, 'levels': [], 'description': ['Индикатор линии перемещения трейлинстопа'], 'name': 'din_fibo_nex', 'source': 'MQL5 Indicators/Din_fibo_Nex_HTF/din_fibo_nex.mq5', 'folder': 'Din_fibo_Nex_HTF', 'inputs': [{'mql': 'Fibo_Channel_Period', 'py': 'Fibo_Channel_Period', 'param': 'Fibo_Channel_Period', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Ratio', 'py': 'Ratio', 'param': 'Ratio', 'type': 'double', 'default': 0.786, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Fibo_Channel_Period = _input('Fibo_Channel_Period', 3)
Ratio = _input('Ratio', 0.786)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
tvBuffer = Arr(0, 0.0)
min_rates_total = 0

def isDelimeter(TimeFrame, Rates_total, Time, shift):
    result = False
    tm = MqlDateTime()
    TimeToStruct(Time[shift], tm)
    _sw1 = TimeFrame
    if _sw1 == PERIOD_M1:
        result = tm.min == 0
    elif _sw1 == PERIOD_M2:
        result = tm.min == 0
    elif _sw1 == PERIOD_M3:
        result = tm.min == 0
    elif _sw1 == PERIOD_M4:
        result = tm.min == 0
    elif _sw1 == PERIOD_M5:
        result = tm.min == 0
    elif _sw1 == PERIOD_M6:
        result = tm.min == 0
    elif _sw1 == PERIOD_M10:
        result = tm.min == 0
    elif _sw1 == PERIOD_M12:
        result = tm.min == 0
    elif _sw1 == PERIOD_M15:
        result = tm.min == 0
    elif _sw1 == PERIOD_M20:
        result = tm.min == 0
    elif _sw1 == PERIOD_M30:
        result = tm.min == 0 and MathMod(tm.hour, 4.0) == 0
    elif _sw1 == PERIOD_H1:
        result = tm.min == 0 and MathMod(tm.hour, 4.0) == 0
    elif _sw1 == PERIOD_H2:
        result = tm.min == 0 and MathMod(tm.hour, 4.0) == 0
    elif _sw1 == PERIOD_H3:
        result = tm.min == 0 and tm.hour == 0
    elif _sw1 == PERIOD_H4:
        result = tm.min == 0 and tm.hour == 0
    elif _sw1 == PERIOD_H6:
        result = tm.min == 0 and tm.hour == 0
    elif _sw1 == PERIOD_H8:
        result = tm.min == 0 and tm.hour == 0
    elif _sw1 == PERIOD_H12:
        result = tm.min == 0 and tm.hour == 0
    elif _sw1 == PERIOD_D1:
        result = tm.day_of_week == MONDAY and tm.hour == 0
    elif _sw1 == PERIOD_W1:
        tm1 = MqlDateTime()
        TimeToStruct(Time[MathMin(Rates_total - 1, shift + 1)], tm1)
        result = (tm.day == 1 or (tm.day == 2 and tm1.day != 1)) or (tm.day == 3 and tm1.day != 2)
    else:
        Print('Недопустимый таймфрейм!!!')
    return result

def SetHnL(Rates_total, Low, High, Close, shift):
    i = shift + 1
    counterPeriod = 0
    first = 0
    while counterPeriod < _int(Fibo_Channel_Period):
        while i < Rates_total and (not tvBuffer[i]):
            i += 1
        if not first:
            first = i
        counterPeriod += 1
        i += 1
    i -= 1
    hh = ArrayMaximum(High, shift + 1, i - shift)
    ll = ArrayMinimum(Low, shift + 1, i - shift)
    tv = NormalizeDouble((High[hh] + Low[ll] + Close[shift + 1]) / 3.0, Digits())
    diff = NormalizeDouble(((High[hh] - Low[ll]) / 2.0) * Ratio, Digits())
    MaH = tv + diff
    MaL = tv - diff
    tvBuffer[shift] = tv
    ExtLineBuffer1[shift] = MaH
    ExtLineBuffer2[shift] = MaL
    SetMovingHnL(first, shift)
    return

def SetMovingHnL(DelimeterBar, CurBar):
    m_cnt = 0
    deltaH = 0.0
    deltaL = 0.0
    deltaH = _fdiv(ExtLineBuffer1[DelimeterBar] - ExtLineBuffer1[CurBar], DelimeterBar - CurBar)
    deltaL = _fdiv(ExtLineBuffer2[DelimeterBar] - ExtLineBuffer2[CurBar], DelimeterBar - CurBar)
    m_cnt = DelimeterBar - 1
    for m_cnt in range(m_cnt, CurBar, -1):
        ExtLineBuffer1[m_cnt] = ExtLineBuffer1[m_cnt + 1] - deltaH
        ExtLineBuffer2[m_cnt] = ExtLineBuffer2[m_cnt + 1] - deltaL
    else:
        m_cnt = _range_end(m_cnt, CurBar, -1)
    m_cnt = DelimeterBar - 1
    for m_cnt in range(m_cnt, CurBar, -1):
        ExtLineBuffer1[m_cnt] = NormalizeDouble(ExtLineBuffer1[m_cnt], Digits())
        ExtLineBuffer2[m_cnt] = NormalizeDouble(ExtLineBuffer2[m_cnt], Digits())
    else:
        m_cnt = _range_end(m_cnt, CurBar, -1)
    return

def SetValuesNullBar(Rates_total, Low, High, Close, shift):
    i = shift
    while not tvBuffer[i]:
        i += 1
    for j in range(i - 1, shift, -1):
        ExtLineBuffer1[j] = 0.0
        ExtLineBuffer2[j] = 0.0
    first = 0
    i = shift
    counterPeriod = 0
    while counterPeriod < _int(Fibo_Channel_Period):
        while i < Rates_total and (not tvBuffer[i]):
            i += 1
        if not first:
            first = i
        counterPeriod += 1
        i += 1
    i -= 1
    hh = ArrayMaximum(High, shift, i - shift)
    ll = ArrayMinimum(Low, shift, i - shift)
    tv = NormalizeDouble((High[hh] + Low[ll] + Close[shift]) / 3.0, Digits())
    diff = NormalizeDouble(((High[hh] - Low[ll]) / 2.0) * Ratio, Digits())
    MaH = tv + diff
    MaL = tv - diff
    ExtLineBuffer1[shift] = MaH
    ExtLineBuffer2[shift] = MaL
    SetMovingHnL(first, shift)

def OnInit():
    global min_rates_total
    if Period() == PERIOD_MN1:
        Print('Недопустимый таймфрейм!!!')
        return INIT_FAILED
    min_rates_total = _int(20 * Fibo_Channel_Period) + 1
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, tvBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(tvBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Din_fibo_Nex(', Fibo_Channel_Period, ',', DoubleToString(Ratio, 4), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        bar = rates_total - 1
        while not isDelimeter(Period(), rates_total, time, bar):
            bar -= 1
        first = bar
        bar -= 1
        counterPeriod = 0
        while counterPeriod < _int(Fibo_Channel_Period):
            while not isDelimeter(Period(), rates_total, time, bar):
                bar -= 1
            bar -= 1
            counterPeriod += 1
        bar += 1
        hh = ArrayMaximum(high, bar + 1, first - bar)
        ll = ArrayMinimum(low, bar + 1, first - bar)
        tv = NormalizeDouble((high[hh] + low[ll] + close[bar + 1]) / 3.0, Digits())
        MaH = tv + NormalizeDouble(((high[hh] - low[ll]) / 2.0) * Ratio, Digits())
        MaL = tv - NormalizeDouble(((high[hh] - low[ll]) / 2.0) * Ratio, Digits())
        tvBuffer[bar] = tv
        ExtLineBuffer1[bar] = MaH
        ExtLineBuffer2[bar] = MaL
        limit = bar - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        tvBuffer[bar] = 0.0
        if isDelimeter(Period(), rates_total, time, bar):
            SetHnL(rates_total, low, high, close, bar)
        if not bar:
            SetValuesNullBar(rates_total, low, high, close, bar)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DinFiboNex(_MQL5Indicator):
    name = 'din_fibo_nex'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Fibo_Channel_Period': 3,
        'Ratio': 0.786,
    }

