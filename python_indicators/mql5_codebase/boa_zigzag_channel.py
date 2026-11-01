"""Boa_ZigZag_channel — converted from MQL5: MQL5 Indicators/Boa_ZigZag_channel/Boa_ZigZag_channel.mq5

Казахский удав в виде канала
Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: mandorr@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'mandorr@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 7, 2: 8, 3: 8, 4: 5, 5: 5}, 'colors': {1: [16443110], 2: [3329330, 13850042], 3: [3329330, 13850042], 4: [16711680], 5: [16711935]}, 'widths': {2: 2, 3: 2, 4: 2, 5: 2}, 'styles': {}, 'labels': {1: 'Boa_ZigZag_channel Cloud', 2: 'Up Boa_ZigZag_channel', 3: 'Down Boa_ZigZag_channel', 4: 'Up Boa_ZigZag_Arrows', 5: 'Down Boa_ZigZag_Arrows'}, 'levels': [], 'description': ['Казахский удав в виде канала'], 'name': 'Boa_ZigZag_channel', 'source': 'MQL5 Indicators/Boa_ZigZag_channel/Boa_ZigZag_channel.mq5', 'folder': 'Boa_ZigZag_channel', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'uint', 'default': 159, 'label': 'лейба верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'uint', 'default': 159, 'label': 'лейба нижнего фрактала', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 6)
UpLable = _input('UpLable', 159)  # лейба верхнего фрактала
DnLable = _input('DnLable', 159)  # лейба нижнего фрактала
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
ColorUpperBuffer = Arr(0, 0.0)
ColorLowerBuffer = Arr(0, 0.0)
ZigzagPeakBuffer = Arr(0, 0.0)
ZigzagLawnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(Length) + 1
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorUpperBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, LowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ColorLowerBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, ZigzagPeakBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ZigzagLawnBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    ArraySetAsSeries(UpperBuffer, True)
    ArraySetAsSeries(LowerBuffer, True)
    ArraySetAsSeries(ColorUpperBuffer, True)
    ArraySetAsSeries(ColorLowerBuffer, True)
    ArraySetAsSeries(ZigzagLawnBuffer, True)
    ArraySetAsSeries(ZigzagPeakBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, DnLable)
    PlotIndexSetInteger(4, PLOT_ARROW, UpLable)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'Boa_ZigZag_channel(Length=', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

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
    LastLawn_prev = 0.0
    LastLawn = 0.0
    LastPeak_prev = 0.0
    LastPeak = 0.0
    zu = 0
    zd = 0
    Swing = 0
    Swing_n = 0
    limit = rates_total - min_rates_total
    climit = limit
    Swing = 0
    Swing_n = 0
    zu = limit
    zd = limit
    BH = high[limit]
    BL = low[limit]
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    LastPeak = high[ArrayMaximum(high, limit, Length)]
    LastPeak_prev = LastPeak
    LastLawn = low[ArrayMinimum(low, limit, Length)]
    LastLawn_prev = LastLawn
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ZigzagLawnBuffer[bar] = 0.0
        ZigzagPeakBuffer[bar] = 0.0
        HH = high[ArrayMaximum(high, bar + 1, Length)]
        LL = low[ArrayMinimum(low, bar + 1, Length)]
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
                ZigzagLawnBuffer[zd] = BL
                LastLawn_prev = LastLawn
                LastLawn = BL
                LowerBuffer[zd] = BL
                DnBuffer[zd] = LowerBuffer[zd]
                if LastLawn_prev > LastLawn:
                    ColorLowerBuffer[zd] = 1.0
                elif LastLawn_prev < LastLawn:
                    ColorLowerBuffer[zd] = 0.0
                else:
                    ColorLowerBuffer[zd] = ColorLowerBuffer[zd + 1]
            if Swing == -1:
                ZigzagPeakBuffer[zu] = BH
                LastPeak_prev = LastPeak
                LastPeak = BH
                UpperBuffer[zu] = BH
                UpBuffer[zu] = UpperBuffer[zu]
                if LastPeak_prev > LastPeak:
                    ColorUpperBuffer[zu] = 1.0
                elif LastPeak_prev < LastPeak:
                    ColorUpperBuffer[zu] = 0.0
                else:
                    ColorUpperBuffer[zu] = ColorUpperBuffer[zu + 1]
            BH = high[bar]
            BL = low[bar]
        if ZigzagPeakBuffer[zu]:
            for index in range(zu - 1, bar - 1, -1):
                UpBuffer[index] = UpBuffer[index + 1]
                UpperBuffer[index] = UpperBuffer[index + 1]
                ColorUpperBuffer[index] = ColorUpperBuffer[index + 1]
        else:
            UpperBuffer[bar] = LastPeak
            UpBuffer[bar] = UpperBuffer[bar]
            ColorUpperBuffer[bar] = ColorUpperBuffer[bar + 1]
        if ZigzagLawnBuffer[zd]:
            for index in range(zd - 1, bar - 1, -1):
                DnBuffer[index] = DnBuffer[index + 1]
                LowerBuffer[index] = LowerBuffer[index + 1]
                ColorLowerBuffer[index] = ColorLowerBuffer[index + 1]
        else:
            LowerBuffer[bar] = LowerBuffer[bar + 1]
            DnBuffer[bar] = LowerBuffer[bar]
            ColorLowerBuffer[bar] = ColorLowerBuffer[bar + 1]
        if (not ZigzagPeakBuffer[zu]) and (not ZigzagLawnBuffer[zd]):
            LowerBuffer[bar] = LastLawn
            DnBuffer[bar] = LowerBuffer[bar]
            ColorLowerBuffer[bar] = ColorLowerBuffer[bar + 1]
            UpperBuffer[bar] = LastPeak
            UpBuffer[bar] = UpperBuffer[bar]
            ColorUpperBuffer[bar] = ColorUpperBuffer[bar + 1]
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


class BoaZigZagChannel(_MQL5Indicator):
    name = 'Boa_ZigZag_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Length': 6,
        'UpLable': 159,  # лейба верхнего фрактала
        'DnLable': 159,  # лейба нижнего фрактала
    }

