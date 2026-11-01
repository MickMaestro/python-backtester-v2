"""braintrend2sig — converted from MQL5: MQL5 Indicators/BrainTrend2Sig/braintrend2sig.mq5

Copyright: Copyright © 2005, BrainTrading Inc.; Link: http://www.braintrading.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, BrainTrading Inc.', 'link': 'http://www.braintrading.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Brain2Sell', 2: 'Brain2Buy'}, 'levels': [], 'description': [], 'name': 'braintrend2sig', 'source': 'MQL5 Indicators/BrainTrend2Sig/braintrend2sig.mq5', 'folder': 'BrainTrend2Sig', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 7)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
river = True
river_ = False
glava = 0
glava_ = 0
StartBars = 0
OldTrend = 0
ATR_Handle = 0
s = 0.0
dartp = 0.0
cecf = 0.0
Emaxtra = 0.0
Emaxtra_ = 0.0
Values_ = Arr(0, 0.0)
Values = Arr(0, 0.0)

def OnInit():
    global StartBars, cecf, dartp, s
    s = 1.5
    dartp = 7.0
    cecf = 0.7
    StartBars = ATR_Period + 2
    if ArrayResize(Values, ATR_Period) < ATR_Period:
        Print('Failed to distribute the memory for Values array')
    if ArrayResize(Values_, ATR_Period) < ATR_Period:
        Print('Failed to distribute the memory for Values array_')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Brain2Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Brain2Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'BrainTrend2Sig'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Emaxtra, Emaxtra_, OldTrend, glava, glava_, river, river_
    if rates_total < StartBars:
        return 0
    bar = 0
    J = 0
    limit = 0
    Curr = 0
    ATR = 0.0
    widcha = 0.0
    TR = 0.0
    Spread = 0.0
    range2 = 0.0
    Weight = 0.0
    Series1 = 0.0
    High = 0.0
    Low = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
        Emaxtra = close[limit + 1]
        glava = 0
        T_Series2 = close[limit + 2]
        T_Series1 = close[limit + 1]
        if T_Series2 > T_Series1:
            river = True
        else:
            river = False
        TR = spread[limit] + high[limit] - low[limit]
        if MathAbs(spread[limit] + high[limit] - T_Series1) > TR:
            TR = MathAbs(spread[limit] + high[limit] - T_Series1)
        if MathAbs(low[limit] - T_Series1) > TR:
            TR = MathAbs(low[limit] - T_Series1)
        ArrayInitialize(Values, TR)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(spread, True)
    ArraySetAsSeries(Values, True)
    ArraySetAsSeries(Values_, True)
    glava = glava_
    Emaxtra = Emaxtra_
    river = river_
    ArrayCopy(Values, Values_, 0, WHOLE_ARRAY)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            glava_ = glava
            Emaxtra_ = Emaxtra
            river_ = river
            ArrayCopy(Values_, Values, 0, WHOLE_ARRAY)
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        Spread = spread[bar] * Point()
        High = high[bar]
        Low = low[bar]
        Series1 = close[bar + 1]
        TR = Spread + High - Low
        if MathAbs(Spread + High - Series1) > TR:
            TR = MathAbs(Spread + High - Series1)
        if MathAbs(Low - Series1) > TR:
            TR = MathAbs(Low - Series1)
        Values[glava] = TR
        ATR = 0.0
        Weight = ATR_Period
        Curr = glava
        J = 0
        for J in range(J, ATR_Period - 1 + 1):
            ATR += Values[Curr] * Weight
            Weight -= 1.0
            Curr -= 1
            if Curr == -1:
                Curr = ATR_Period - 1
        else:
            J = _range_end(J, ATR_Period - 1 + 1, 1)
        ATR = _fdiv(2.0 * ATR, dartp * (dartp + 1.0))
        glava += 1
        range2 = (ATR * s) / 4
        if glava == ATR_Period:
            glava = 0
        widcha = cecf * ATR
        if river and Low < (Emaxtra - widcha):
            river = False
            Emaxtra = Spread + High
        if (not river) and (Spread + High) > (Emaxtra + widcha):
            river = True
            Emaxtra = Low
        if river and Low > Emaxtra:
            Emaxtra = Low
        if (not river) and (Spread + High) < Emaxtra:
            Emaxtra = Spread + High
        if river:
            if OldTrend < 0:
                BuyBuffer[bar] = Low - range2
            if bar != 0:
                OldTrend = 1
        else:
            if OldTrend > 0:
                SellBuffer[bar] = High + range2
            if bar != 0:
                OldTrend = -1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Braintrend2sig(_MQL5Indicator):
    name = 'braintrend2sig'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 7,
    }

