"""Boa_ZigZag_Arrows_Duplex — converted from MQL5: MQL5 Indicators/Boa_ZigZag_Arrows_Duplex/Boa_ZigZag_Arrows_Duplex.mq5

Дв разнопериодных казахских удава
Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: mandorr@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'mandorr@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16748574], 2: [9639167], 3: [16776960], 4: [42495]}, 'widths': {1: 5, 2: 5, 3: 5, 4: 5}, 'styles': {}, 'labels': {1: 'Slow Boa_ZigZag Dn', 2: 'Slow Boa_ZigZag Up', 3: 'Fast Boa_ZigZag Dn', 4: 'Fast Boa_ZigZag Up'}, 'levels': [], 'description': ['Дв разнопериодных казахских удава'], 'name': 'Boa_ZigZag_Arrows_Duplex', 'source': 'MQL5 Indicators/Boa_ZigZag_Arrows_Duplex/Boa_ZigZag_Arrows_Duplex.mq5', 'folder': 'Boa_ZigZag_Arrows_Duplex', 'inputs': [{'mql': 'SlowLength', 'py': 'SlowLength', 'param': 'SlowLength', 'type': 'uint', 'default': 42, 'label': 'период медленного зигзага', 'sinput': False}, {'mql': 'FastLength', 'py': 'FastLength', 'param': 'FastLength', 'type': 'uint', 'default': 6, 'label': 'период быстрого зигзага', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SlowLength = _input('SlowLength', 42)  # период медленного зигзага
FastLength = _input('FastLength', 6)  # период быстрого зигзага
ZigzagLawnBuffer1 = Arr(0, 0.0)
ZigzagPeakBuffer1 = Arr(0, 0.0)
ZigzagLawnBuffer2 = Arr(0, 0.0)
ZigzagPeakBuffer2 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(MathMax(SlowLength, FastLength)) + 1
    shortname = Box("")
    StringConcatenate(shortname, 'Boa_ZigZag_Arrows_Duplex(', _str(SlowLength), ', ', _str(FastLength), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, ZigzagLawnBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(ZigzagLawnBuffer1, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 162)
    SetIndexBuffer(1, ZigzagPeakBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(ZigzagPeakBuffer1, True)
    PlotIndexSetInteger(1, PLOT_ARROW, 162)
    SetIndexBuffer(2, ZigzagLawnBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ZigzagLawnBuffer2, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    SetIndexBuffer(3, ZigzagPeakBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ZigzagPeakBuffer2, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    climit = 0
    bar = 0
    HH = 0.0
    LL = 0.0
    BH = 0.0
    BL = 0.0
    zu = 0
    zd = 0
    Swing = 0
    Swing_n = 0
    limit = rates_total - min_rates_total
    climit = limit
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    Swing = 0
    Swing_n = 0
    zu = limit
    zd = limit
    BH = high[limit]
    BL = low[limit]
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ZigzagLawnBuffer1[bar] = 0.0
        ZigzagPeakBuffer1[bar] = 0.0
        HH = high[ArrayMaximum(high, bar + 1, SlowLength)]
        LL = low[ArrayMinimum(low, bar + 1, SlowLength)]
        if low[bar] < LL and high[bar] > HH:
            Swing = 2
            if Swing_n == 1:
                zu = bar + 1
            if Swing_n == -1:
                zd = bar + 1
        else:
            if low[bar] < LL:
                Swing = -1
            if high[bar] > HH:
                Swing = 1
        if Swing != Swing_n and Swing_n != 0:
            if Swing == 2:
                Swing = -Swing_n
                BH = high[bar]
                BL = low[bar]
            if Swing == 1:
                if BL == low[zd]:
                    ZigzagLawnBuffer1[zd] = BL
                else:
                    ZigzagLawnBuffer1[zd - 1] = BL
            if Swing == -1:
                if BH == high[zu]:
                    ZigzagPeakBuffer1[zu] = BH
                else:
                    ZigzagPeakBuffer1[zu - 1] = BH
            BH = high[bar]
            BL = low[bar]
        if Swing == 1:
            if high[bar] >= BH:
                BH = high[bar]
                zu = bar
        if Swing == -1:
            if low[bar] <= BL:
                BL = low[bar]
                zd = bar
        Swing_n = Swing
    else:
        bar = _range_end(bar, 0 - 1, -1)
    Swing = 0
    Swing_n = 0
    zu = limit
    zd = limit
    BH = high[limit]
    BL = low[limit]
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ZigzagLawnBuffer2[bar] = 0.0
        ZigzagPeakBuffer2[bar] = 0.0
        HH = high[ArrayMaximum(high, bar + 1, FastLength)]
        LL = low[ArrayMinimum(low, bar + 1, FastLength)]
        if low[bar] < LL and high[bar] > HH:
            Swing = 2
            if Swing_n == 1:
                zu = bar + 1
            if Swing_n == -1:
                zd = bar + 1
        else:
            if low[bar] < LL:
                Swing = -1
            if high[bar] > HH:
                Swing = 1
        if Swing != Swing_n and Swing_n != 0:
            if Swing == 2:
                Swing = -Swing_n
                BH = high[bar]
                BL = low[bar]
            if Swing == 1:
                if BL == low[zd]:
                    ZigzagLawnBuffer2[zd] = BL
                else:
                    ZigzagLawnBuffer2[zd - 1] = BL
            if Swing == -1:
                if BH == high[zu]:
                    ZigzagPeakBuffer2[zu] = BH
                else:
                    ZigzagPeakBuffer2[zu - 1] = BH
            BH = high[bar]
            BL = low[bar]
        if Swing == 1:
            if high[bar] >= BH:
                BH = high[bar]
                zu = bar
        if Swing == -1:
            if low[bar] <= BL:
                BL = low[bar]
                zd = bar
        Swing_n = Swing
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BoaZigZagArrowsDuplex(_MQL5Indicator):
    name = 'Boa_ZigZag_Arrows_Duplex'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'SlowLength': 42,  # период медленного зигзага
        'FastLength': 6,  # период быстрого зигзага
    }

