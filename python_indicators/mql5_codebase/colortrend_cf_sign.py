"""colortrend_cf_sign — converted from MQL5: MQL5 Indicators/ColorTrend_CF_Sign/colortrend_cf_sign.mq5

Copyright: Converted by and Copyright: Ronald Verwer/ROVERCOM; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Converted by and Copyright: Ronald Verwer/ROVERCOM', 'link': '', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [36095], 2: [16776960]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Trend_CF Sell', 2: 'Trend_CF Buy'}, 'levels': [], 'description': [], 'name': 'colortrend_cf_sign', 'source': 'MQL5 Indicators/ColorTrend_CF_Sign/colortrend_cf_sign.mq5', 'folder': 'ColorTrend_CF_Sign', 'inputs': [{'mql': 'Period_', 'py': 'Period_', 'param': 'Period_', 'type': 'uint', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period_ = _input('Period_', 30)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
Count = Arr(0, 0)
min_rates_total = 0
x_p = Arr(0, 0.0)
x_n = Arr(0, 0.0)
y_p = Arr(0, 0.0)
y_n = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = _int(Period_) - 1
    for iii in range(0, _int(Period_)):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > (_int(Period_) - 1):
            numb -= _int(Period_)
        CoArr[iii] = numb

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    min_rates_total = _int(MathMax(Period_, ATR_Period))
    ArrayResize(x_p, Period_)
    ArrayResize(x_n, Period_)
    ArrayResize(y_p, Period_)
    ArrayResize(y_n, Period_)
    ArrayResize(Count, Period_)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 124)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 124)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'ColorTrend_CF_Sign(', Period_, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Lower1, _s_OnCalculate_Upper1
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    bar0 = 0
    bar1 = 0
    barq = 0
    chp = 0.0
    chn = 0.0
    cffp = 0.0
    cffn = 0.0
    dprice = 0.0
    Upper = 0.0
    Lower = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dprice = close[bar] - close[bar - 1]
        bar0 = Count[0]
        bar1 = Count[1]
        if dprice > 0:
            x_p[bar0] = dprice
            y_p[bar0] = x_p[bar0] + y_p[bar1]
            x_n[bar0] = 0.0
            y_n[bar0] = 0.0
        else:
            x_n[bar0] = -dprice
            y_n[bar0] = x_n[bar0] + y_n[bar1]
            x_p[bar0] = 0.0
            y_p[bar0] = 0.0
        if bar < min_rates_total:
            if bar < (rates_total - 1):
                Recount_ArrayZeroPos(Count)
            continue
        chp = 0.0
        chn = 0.0
        cffp = 0.0
        cffn = 0.0
        for q in range(_int(Period_) - 1, 0 - 1, -1):
            barq = Count[q]
            chp += x_p[barq]
            chn += x_n[barq]
            cffp += y_p[barq]
            cffn += y_n[barq]
        Upper = _fdiv(chp - cffn, Point())
        Lower = _fdiv(chn - cffp, Point())
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_Upper1 <= _s_OnCalculate_Lower1 and Upper > Lower:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_Upper1 >= _s_OnCalculate_Lower1 and Upper < Lower:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count)
            _s_OnCalculate_Upper1 = Upper
            _s_OnCalculate_Lower1 = Lower
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_Upper1 = 0.0
_s_OnCalculate_Lower1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColortrendCfSign(_MQL5Indicator):
    name = 'colortrend_cf_sign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_': 30,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

