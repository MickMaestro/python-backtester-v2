"""BrainTrend2Stop — converted from MQL5: MQL5 Indicators/BrainTrend2Stop/BrainTrend2Stop.mq5

Copyright: Copyright © 2005, BrainTrading Inc.; Link: http://www.braintrading.com/; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, BrainTrading Inc.', 'link': 'http://www.braintrading.com/', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 1, 4: 1}, 'colors': {1: [255], 2: [16711680], 3: [255], 4: [16711680]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2}, 'styles': {3: 0, 4: 0}, 'labels': {1: 'BrainSell', 2: 'BrainBuy', 3: 'Brain2Sell', 4: 'Brain2Buy'}, 'levels': [], 'description': [], 'name': 'BrainTrend2Stop', 'source': 'MQL5 Indicators/BrainTrend2Stop/BrainTrend2Stop.mq5', 'folder': 'BrainTrend2Stop', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 7)
SellStopBuffer = Arr(0, 0.0)
BuyStopBuffer = Arr(0, 0.0)
SellStopBuffer_ = Arr(0, 0.0)
BuyStopBuffer_ = Arr(0, 0.0)
river = True
river_ = False
glava = 0
glava_ = 0
StartBars = 0
p = 0
P_ = 0
OldTrend = 0
r = 0.0
R_ = 0.0
artp_2 = 0.0
s = 0.0
dartp = 0.0
cecf = 0.0
Emaxtra = 0.0
Emaxtra_ = 0.0
Values_ = Arr(0, 0.0)
Values = Arr(0, 0.0)

def OnInit():
    global StartBars, artp_2, cecf, dartp, s
    s = 1.5
    cecf = 0.7
    dartp = 7.0
    artp_2 = 0.5 * ATR_Period * (ATR_Period + 1.0)
    StartBars = ATR_Period + 2
    if ArrayResize(Values, ATR_Period) < ATR_Period:
        Print('Не удалось распределить память под массив Values')
    if ArrayResize(Values_, ATR_Period) < ATR_Period:
        Print('Не удалось распределить память под массив Values_')
    SetIndexBuffer(0, SellStopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Brain2SellStop')
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    ArraySetAsSeries(SellStopBuffer, True)
    SetIndexBuffer(1, BuyStopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Brain2BuyStop')
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyStopBuffer, True)
    SetIndexBuffer(2, SellStopBuffer_, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(2, PLOT_LABEL, 'Brain2SellStop')
    ArraySetAsSeries(SellStopBuffer_, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, BuyStopBuffer_, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(3, PLOT_LABEL, 'Brain2BuyStop')
    ArraySetAsSeries(BuyStopBuffer_, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'BrainTrend2Stop'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Emaxtra, Emaxtra_, OldTrend, glava, glava_, p, r, river, river_
    if rates_total < StartBars:
        return 0
    bar = 0
    J = 0
    limit = 0
    Curr = 0
    to_copy = 0
    ATR = 0.0
    widcha = 0.0
    TR = 0.0
    Spread = 0.0
    r1 = 0.0
    Weight = 0.0
    Series1 = 0.0
    High = 0.0
    Low = 0.0
    range2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
        to_copy = rates_total
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
        to_copy = rates_total - prev_calculated + 1
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(spread, True)
    ArraySetAsSeries(Values, True)
    ArraySetAsSeries(Values_, True)
    p = P_
    r = R_
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
        BuyStopBuffer[bar] = 0.0
        SellStopBuffer[bar] = 0.0
        BuyStopBuffer_[bar] = 0.0
        SellStopBuffer_[bar] = 0.0
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
            r1 = Low - range2
            if r1 < r and OldTrend > 0:
                r1 = r
            BuyStopBuffer[bar] = r1
            BuyStopBuffer_[bar] = r1
            if bar != 0:
                r = r1
                OldTrend = 1
        else:
            r1 = High + range2
            if r1 > r and OldTrend < 0:
                r1 = r
            SellStopBuffer[bar] = r1
            SellStopBuffer_[bar] = r1
            if bar != 0:
                r = r1
                OldTrend = -1
        if (not BuyStopBuffer[bar]) and (not SellStopBuffer[bar]):
            BuyStopBuffer[bar] = BuyStopBuffer[bar + 1]
            SellStopBuffer[bar] = SellStopBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BrainTrend2Stop(_MQL5Indicator):
    name = 'BrainTrend2Stop'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 7,
    }

