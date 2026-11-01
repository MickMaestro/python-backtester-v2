"""braintrend2 — converted from MQL5: MQL5 Indicators/BrainTrend2/braintrend2.mq5

Copyright: Copyright © 2005, BrainTrading Inc.; Link: http://www.braintrading.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, BrainTrading Inc.', 'link': 'http://www.braintrading.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {1: 'Flat; UpTrend; DownTrend;'}, 'levels': [], 'description': [], 'name': 'braintrend2', 'source': 'MQL5 Indicators/BrainTrend2/braintrend2.mq5', 'folder': 'BrainTrend2', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Lime = 0x00FF00  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 7)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
river = True
river_ = False
glava = 0
glava_ = 0
StartBars = 0
dartp = 0.0
cecf = 0.0
Emaxtra = 0.0
Emaxtra_ = 0.0
Values_ = Arr(0, 0.0)
Values = Arr(0, 0.0)

def OnInit():
    global StartBars, cecf, dartp
    dartp = 7.0
    cecf = 0.7
    StartBars = ATR_Period + 2
    if ArrayResize(Values, ATR_Period) < ATR_Period:
        Print('Failed to distribute the memory for Values array')
    if ArrayResize(Values_, ATR_Period) < ATR_Period:
        Print('Failed to distribute the memory for Values array_')
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    for i in range(0, 3):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, ExtColor[i])
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'BrainTrend1'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Emaxtra, Emaxtra_, glava, glava_, river, river_
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
        ExtOpenBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        ExtLowBuffer[bar] = 0.0
        ExtCloseBuffer[bar] = 0.0
        ExtColorsBuffer[bar] = 0.0
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
            ExtOpenBuffer[bar] = open[bar]
            ExtHighBuffer[bar] = High
            ExtLowBuffer[bar] = Low
            ExtCloseBuffer[bar] = close[bar]
            ExtColorsBuffer[bar] = 1.0
        else:
            ExtOpenBuffer[bar] = open[bar]
            ExtHighBuffer[bar] = High
            ExtLowBuffer[bar] = Low
            ExtCloseBuffer[bar] = close[bar]
            ExtColorsBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
ExtColor = Arr.of([CLR_NONE, _uint(Lime), _uint(Magenta)], fill=0, dyn=False, size=3)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Braintrend2(_MQL5Indicator):
    name = 'braintrend2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 7,
    }

