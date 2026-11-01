"""Zigzag2_R_Arrows — converted from MQL5: MQL5 Indicators/Zigzag2_R_Arrows/Zigzag2_R_Arrows.mq5

ZigZag
Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [8721863], 2: [7451452]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Up Zigzag2_R_Arrows', 2: 'Down Zigzag2_R_Arrows'}, 'levels': [], 'description': ['ZigZag'], 'name': 'Zigzag2_R_Arrows', 'source': 'MQL5 Indicators/Zigzag2_R_Arrows/Zigzag2_R_Arrows.mq5', 'folder': 'Zigzag2_R_Arrows', 'inputs': [{'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'uint', 'default': 217, 'label': 'лейба верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'uint', 'default': 218, 'label': 'лейба нижнего фрактала', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
UpLable = _input('UpLable', 217)  # лейба верхнего фрактала
DnLable = _input('DnLable', 218)  # лейба нижнего фрактала
ZigzagPeakBuffer = Arr(0, 0.0)
ZigzagLawnBuffer = Arr(0, 0.0)
HighMapBuffer = Arr(0, 0.0)
LowMapBuffer = Arr(0, 0.0)
level = 3  # recounting's depth
downloadhistory = False
dExtDeviation = 0.0
min_rates_total = 0

def OnInit():
    global dExtDeviation, min_rates_total
    min_rates_total = ExtDepth + ExtBackstep
    dExtDeviation = ExtDeviation * Point()
    SetIndexBuffer(0, ZigzagLawnBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ZigzagPeakBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, HighMapBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, LowMapBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(ZigzagLawnBuffer, True)
    ArraySetAsSeries(ZigzagPeakBuffer, True)
    ArraySetAsSeries(HighMapBuffer, True)
    ArraySetAsSeries(LowMapBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, DnLable)
    PlotIndexSetInteger(1, PLOT_ARROW, UpLable)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'Zigzag2_R_Arrows(ExtDepth=', ExtDepth, 'ExtDeviation = ', ExtDeviation, 'ExtBackstep = ', ExtBackstep, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    iii = 0
    counterZ = 0
    whatlookfor = 0
    back = 0
    lasthighpos = 0
    lastlowpos = 0
    val = 0.0
    res = 0.0
    curlow = 9999999999.0
    curhigh = 0.0
    lasthigh = 0.0
    lastlow = 999999999.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        ArrayInitialize(ZigzagPeakBuffer, None)
        ArrayInitialize(ZigzagLawnBuffer, None)
        ArrayInitialize(HighMapBuffer, None)
        ArrayInitialize(LowMapBuffer, None)
    else:
        limit = rates_total - prev_calculated
        while counterZ < level and iii < 100:
            res = ZigzagPeakBuffer[iii] + ZigzagLawnBuffer[iii]
            if res:
                counterZ += 1
            iii += 1
        iii -= 1
        limit = iii
        if LowMapBuffer[iii]:
            curlow = LowMapBuffer[iii]
            whatlookfor = 1
        else:
            curhigh = HighMapBuffer[iii]
            whatlookfor = -1
        iii = limit - 1
        for iii in range(iii, 0 - 1, -1):
            ZigzagPeakBuffer[iii] = 0.0
            ZigzagLawnBuffer[iii] = 0.0
            LowMapBuffer[iii] = 0.0
            HighMapBuffer[iii] = 0.0
        else:
            iii = _range_end(iii, 0 - 1, -1)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        val = low[ArrayMinimum(low, bar, ExtDepth)]
        if val == lastlow:
            val = 0.0
        else:
            lastlow = val
            if (low[bar] - val) > dExtDeviation:
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = LowMapBuffer[bar + back]
                    if res and res > val:
                        LowMapBuffer[bar + back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        if low[bar] == val:
            LowMapBuffer[bar] = val
        else:
            LowMapBuffer[bar] = 0.0
        val = high[ArrayMaximum(high, bar, ExtDepth)]
        if val == lasthigh:
            val = 0.0
        else:
            lasthigh = val
            if (val - high[bar]) > dExtDeviation:
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = HighMapBuffer[bar + back]
                    if res and res < val:
                        HighMapBuffer[bar + back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        if high[bar] == val:
            HighMapBuffer[bar] = val
        else:
            HighMapBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if not whatlookfor:
        lastlow = 0.0
        lasthigh = 0.0
    else:
        lastlow = curlow
        lasthigh = curhigh
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        res = 0.0
        _sw1 = whatlookfor
        if _sw1 == 0:
            if (not lastlow) and (not lasthigh):
                if HighMapBuffer[bar]:
                    lasthigh = high[bar]
                    lasthighpos = bar
                    whatlookfor = -1
                    ZigzagPeakBuffer[bar] = lasthigh
                    res = 1.0
                if LowMapBuffer[bar]:
                    lastlow = low[bar]
                    lastlowpos = bar
                    whatlookfor = 1
                    ZigzagLawnBuffer[bar] = lastlow
                    res = 1.0
        elif _sw1 == 1:
            if (LowMapBuffer[bar] and LowMapBuffer[bar] < lastlow) and (not HighMapBuffer[bar]):
                ZigzagLawnBuffer[lastlowpos] = 0.0
                lastlowpos = bar
                lastlow = LowMapBuffer[bar]
                ZigzagLawnBuffer[bar] = lastlow
                res = 1.0
            if HighMapBuffer[bar] and (not LowMapBuffer[bar]):
                lasthigh = HighMapBuffer[bar]
                lasthighpos = bar
                ZigzagPeakBuffer[bar] = lasthigh
                whatlookfor = -1
                res = 1.0
        elif _sw1 == -1:
            if (HighMapBuffer[bar] and HighMapBuffer[bar] > lasthigh) and (not LowMapBuffer[bar]):
                ZigzagPeakBuffer[lasthighpos] = 0.0
                lasthighpos = bar
                lasthigh = HighMapBuffer[bar]
                ZigzagPeakBuffer[bar] = lasthigh
            if LowMapBuffer[bar] and (not HighMapBuffer[bar]):
                lastlow = LowMapBuffer[bar]
                lastlowpos = bar
                ZigzagLawnBuffer[bar] = lastlow
                whatlookfor = 1
        else:
            return rates_total
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Zigzag2RArrows(_MQL5Indicator):
    name = 'Zigzag2_R_Arrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
        'UpLable': 217,  # лейба верхнего фрактала
        'DnLable': 218,  # лейба нижнего фрактала
    }

