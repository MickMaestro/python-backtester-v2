"""ZZ_Close — converted from MQL5: MQL5 Indicators/ZigZag Color for Line Chart/ZZ_Close.mq5

ZigZag
Copyright: Copyright 2022, D4rk Ryd3r; Link: https://twitter.com/DarkRyd3r; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, D4rk Ryd3r', 'link': 'https://twitter.com/DarkRyd3r', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [9639167, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ZigZag'}, 'levels': [], 'description': ['ZigZag'], 'name': 'ZZ_Close', 'source': 'MQL5 Indicators/ZigZag Color for Line Chart/ZZ_Close.mq5', 'folder': 'ZigZag Color for Line Chart', 'inputs': [{'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtDepth = _input('ExtDepth', 12)
min_rates_total = 0
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
ZZLBuffer = Arr(0, 0.0)
ZZHBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(ExtDepth)
    SetIndexBuffer(0, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, ZZLBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ZZHBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    ArraySetAsSeries(ZZLBuffer, True)
    ArraySetAsSeries(ZZHBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'ZZ_Close(ExtDepth=', ExtDepth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_lasthigh, _s_OnCalculate_lasthighpos, _s_OnCalculate_lastlow, _s_OnCalculate_lastlowpos
    if rates_total < min_rates_total:
        return 0
    limit = 0
    climit = 0
    bar = 0
    curlowpos = 0
    curhighpos = 0
    pos = 0
    curlow = 0.0
    curhigh = 0.0
    min_ = 0.0
    max_ = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        climit = limit
        _s_OnCalculate_lasthighpos = limit
        _s_OnCalculate_lastlowpos = limit
        _s_OnCalculate_lastlow = close[limit]
        _s_OnCalculate_lasthigh = close[limit]
    else:
        limit = rates_total - prev_calculated
        climit = limit + min_rates_total
        lim = rates_total - prev_calculated
        limit = lim + MathMax(_s_OnCalculate_lasthighpos, _s_OnCalculate_lastlowpos)
        _s_OnCalculate_lasthighpos += lim
        _s_OnCalculate_lastlowpos += lim
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        LowestBuffer[bar] = 0.0
        ZZLBuffer[bar] = 0.0
        curlowpos = ArrayMinimum(close, bar, ExtDepth)
        curlow = close[curlowpos]
        if _s_OnCalculate_lasthighpos > curlowpos:
            ZZLBuffer[curlowpos] = curlow
            min_ = 999999999.0
            pos = _s_OnCalculate_lasthighpos
            for rrr in range(_s_OnCalculate_lasthighpos, curlowpos - 1, -1):
                if not ZZLBuffer[rrr]:
                    continue
                if ZZLBuffer[rrr] < min_:
                    min_ = ZZLBuffer[rrr]
                    pos = rrr
                LowestBuffer[rrr] = 0.0
            LowestBuffer[pos] = min_
        _s_OnCalculate_lastlowpos = curlowpos
        _s_OnCalculate_lastlow = curlow
        HighestBuffer[bar] = 0.0
        ZZHBuffer[bar] = 0.0
        curhighpos = ArrayMaximum(close, bar, ExtDepth)
        curhigh = close[curhighpos]
        if curhigh <= _s_OnCalculate_lasthigh:
            _s_OnCalculate_lasthigh = curhigh
        else:
            if _s_OnCalculate_lastlowpos > curhighpos:
                ZZHBuffer[curhighpos] = curhigh
                max_ = -999999999.0
                pos = _s_OnCalculate_lastlowpos
                for rrr in range(_s_OnCalculate_lastlowpos, curhighpos - 1, -1):
                    if not ZZHBuffer[rrr]:
                        continue
                    if ZZHBuffer[rrr] > max_:
                        max_ = ZZHBuffer[rrr]
                        pos = rrr
                    HighestBuffer[rrr] = 0.0
                HighestBuffer[pos] = max_
            _s_OnCalculate_lasthighpos = curhighpos
            _s_OnCalculate_lasthigh = curhigh
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = climit
    for bar in range(bar, 0 - 1, -1):
        max_ = HighestBuffer[bar]
        min_ = LowestBuffer[bar]
        if (not max_) and (not min_):
            ColorBuffer[bar] = ColorBuffer[bar + 1]
        if max_ and min_:
            if ColorBuffer[bar + 1] == 0:
                ColorBuffer[bar] = 1.0
            else:
                ColorBuffer[bar] = 0.0
        if max_ and (not min_):
            ColorBuffer[bar] = 1.0
        if (not max_) and min_:
            ColorBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_lasthighpos = 0
_s_OnCalculate_lastlowpos = 0
_s_OnCalculate_lasthigh = 0.0
_s_OnCalculate_lastlow = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZZClose(_MQL5Indicator):
    name = 'ZZ_Close'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
    }

