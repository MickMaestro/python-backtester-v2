"""colorschaffmomentumtrendcycle — converted from MQL5: MQL5 Indicators/ColorSchaffMomentumTrendCycle_HTF/colorschaffmomentumtrendcycle.mq5

Schaff Trend Cycle - Cyclical Stoch over Stoch over Momentum MACD.
The code adapted Nikolay Kositsin.
Copyright: Copyright © 2011, EarnForex.com; Link: http://www.earnforex.com; Version: 2.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, EarnForex.com', 'link': 'http://www.earnforex.com', 'version': '2.10', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': -110.0, 'indicator_maximum': 110.0}, 'types': {1: 10}, 'colors': {1: [9639167, 13850042, 55295, 4163021, 13434880, 16748574, 32768, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Schaff Momentum Trend Cycle'}, 'levels': [], 'description': ['Schaff Trend Cycle - Cyclical Stoch over Stoch over Momentum MACD.', 'The code adapted Nikolay Kositsin.'], 'name': 'colorschaffmomentumtrendcycle', 'source': 'MQL5 Indicators/ColorSchaffMomentumTrendCycle_HTF/colorschaffmomentumtrendcycle.mq5', 'folder': 'ColorSchaffMomentumTrendCycle_HTF', 'inputs': [{'mql': 'Fast_Momentum', 'py': 'Fast_Momentum', 'param': 'Fast_Momentum', 'type': 'uint', 'default': 23, 'label': 'Период быстрого Momentum', 'sinput': False}, {'mql': 'Slow_Momentum', 'py': 'Slow_Momentum', 'param': 'Slow_Momentum', 'type': 'uint', 'default': 50, 'label': 'Период медленного Momentum', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Cycle', 'py': 'Cycle', 'param': 'Cycle', 'type': 'uint', 'default': 10, 'label': 'Период стохастического осциллятора', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 60, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -60, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Fast_Momentum = _input('Fast_Momentum', 23)  # Период быстрого Momentum
Slow_Momentum = _input('Slow_Momentum', 50)  # Период медленного Momentum
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # Ценовая константа
Cycle = _input('Cycle', 10)  # Период стохастического осциллятора
HighLevel = _input('HighLevel', 60)
MiddleLevel = _input('MiddleLevel', 0)
LowLevel = _input('LowLevel', -60)
STC_Buffer = Arr(0, 0.0)
ColorSTC_Buffer = Arr(0, 0.0)
Count = Arr(0, 0)
st1_pass = False
st2_pass = False
MACD = Arr(0, 0.0)
ST = Arr(0, 0.0)
Factor = 0.0
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
Ind1_Handle = 0
Ind2_Handle = 0

def Recount_ArrayZeroPos(CoArr, Rates_total, Bar):
    global _s_Recount_ArrayZeroPos_count
    if not Bar:
        return
    numb = 0
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = _int(Cycle) - 1
    for iii in range(0, _int(Cycle)):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > (_int(Cycle) - 1):
            numb -= _int(Cycle)
        CoArr[iii] = numb

def OnInit():
    global Factor, Ind1_Handle, Ind2_Handle, min_rates_1, min_rates_2, min_rates_total, st1_pass, st2_pass
    min_rates_1 = _int(Fast_Momentum)
    min_rates_2 = _int(Slow_Momentum)
    min_rates_total = MathMax(min_rates_1, min_rates_2) + _int(Cycle) + 1
    Ind1_Handle = iMomentum(Symbol(), PERIOD_CURRENT, Fast_Momentum, AppliedPrice)
    if Ind1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Momentum 1')
        return INIT_FAILED
    Ind2_Handle = iMomentum(Symbol(), PERIOD_CURRENT, Slow_Momentum, AppliedPrice)
    if Ind2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Momentum 2')
        return INIT_FAILED
    if ArrayResize(ST, Cycle) < _int(Cycle):
        Print('Не удалось распределить память под массив ST')
        return INIT_FAILED
    if ArrayResize(MACD, Cycle) < _int(Cycle):
        Print('Не удалось распределить память под массив MACD')
        return INIT_FAILED
    if ArrayResize(Count, Cycle) < _int(Cycle):
        Print('Не удалось распределить память под массив Count')
        return INIT_FAILED
    Factor = 0.5
    st1_pass = False
    st2_pass = False
    SetIndexBuffer(0, STC_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(STC_Buffer, True)
    SetIndexBuffer(1, ColorSTC_Buffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorSTC_Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Schaff Momentum Trend Cycle( ', Fast_Momentum, ', ', Slow_Momentum, ', ', Cycle, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMediumSeaGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global st1_pass, st2_pass
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind1_Handle) < Bars(Symbol(), PERIOD_CURRENT):
        return prev_calculated
    if BarsCalculated(Ind2_Handle) < Bars(Symbol(), PERIOD_CURRENT):
        return prev_calculated
    fastMomentum = Arr(0, 0.0)
    slowMomentum = Arr(0, 0.0)
    LLV = 0.0
    HHV = 0.0
    limit = 0
    to_copy = 0
    bar = 0
    Bar0 = 0
    Bar1 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        STC_Buffer[limit + 1] = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind1_Handle, 0, 0, to_copy, fastMomentum) <= 0:
        return 0
    if CopyBuffer(Ind2_Handle, 0, 0, to_copy, slowMomentum) <= 0:
        return 0
    ArraySetAsSeries(fastMomentum, True)
    ArraySetAsSeries(slowMomentum, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Bar0 = Count[0]
        Bar1 = Count[1]
        MACD[Bar0] = fastMomentum[bar] - slowMomentum[bar]
        LLV = MACD[ArrayMinimum(MACD)]
        HHV = MACD[ArrayMaximum(MACD)]
        if (HHV - LLV) != 0:
            ST[Bar0] = _fdiv(MACD[Bar0] - LLV, HHV - LLV) * 100
        else:
            ST[Bar0] = ST[Bar1]
        if st1_pass:
            ST[Bar0] = (Factor * (ST[Bar0] - ST[Bar1])) + ST[Bar1]
        st1_pass = True
        LLV = ST[ArrayMinimum(ST)]
        HHV = ST[ArrayMaximum(ST)]
        if (HHV - LLV) != 0:
            STC_Buffer[bar] = (_fdiv(ST[Bar0] - LLV, HHV - LLV) * 200) - 100
        else:
            STC_Buffer[bar] = STC_Buffer[bar + 1]
        if st2_pass:
            STC_Buffer[bar] = (Factor * (STC_Buffer[bar] - STC_Buffer[bar + 1])) + STC_Buffer[bar + 1]
        st2_pass = True
        Recount_ArrayZeroPos(Count, rates_total, bar)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Sts = STC_Buffer[bar]
        dSts = Sts - STC_Buffer[bar + 1]
        clr = 4
        if Sts > 0:
            if Sts > HighLevel:
                if dSts >= 0:
                    clr = 7
                else:
                    clr = 6
            else:
                if dSts >= 0:
                    clr = 5
                else:
                    clr = 4
        if Sts < 0:
            if Sts < LowLevel:
                if dSts < 0:
                    clr = 0
                else:
                    clr = 1
            else:
                if dSts < 0:
                    clr = 2
                else:
                    clr = 3
        ColorSTC_Buffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorschaffmomentumtrendcycle(_MQL5Indicator):
    name = 'colorschaffmomentumtrendcycle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast_Momentum': 23,  # Период быстрого Momentum
        'Slow_Momentum': 50,  # Период медленного Momentum
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Ценовая константа
        'Cycle': 10,  # Период стохастического осциллятора
        'HighLevel': 60,
        'MiddleLevel': 0,
        'LowLevel': -60,
    }
    y_range = (-110.0, 110.0)

