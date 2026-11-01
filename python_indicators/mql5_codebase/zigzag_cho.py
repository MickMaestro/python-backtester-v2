"""ZigZag_CHO — converted from MQL5: MQL5 Indicators/ZigZag_CHO/ZigZag_CHO.mq5

ZigZag
Copyright: Copyright © 2016, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 6}, 'colors': {1: [3329330], 2: [14822282]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Chaikin Oscillator', 2: 'ZigZag_CHO'}, 'levels': [], 'description': ['ZigZag'], 'name': 'ZigZag_CHO', 'source': 'MQL5 Indicators/ZigZag_CHO/ZigZag_CHO.mq5', 'folder': 'ZigZag_CHO', 'inputs': [{'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'uint', 'default': 3, 'label': 'быстрый период', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'uint', 'default': 10, 'label': 'медленный период', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 1, 'label': 'тип сглаживания', 'sinput': False}, {'mql': 'applied_volume', 'py': 'applied_volume', 'param': 'applied_volume', 'type': 'int', 'default': 0, 'label': 'используемый объем', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
fast_ma_period = _input('fast_ma_period', 3)  # быстрый период
slow_ma_period = _input('slow_ma_period', 10)  # медленный период
ma_method = _input('ma_method', MODE_EMA)  # тип сглаживания
applied_volume = _input('applied_volume', VOLUME_TICK)  # используемый объем
ExtDepth = _input('ExtDepth', 3)
ExtDeviation = _input('ExtDeviation', 3)
ExtBackstep = _input('ExtBackstep', 3)
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
CHOBuffer = Arr(0, 0.0)
LASTlowpos = 0
LASThighpos = 0
LASTColor = 0
LASTlow0 = 0.0
LASTlow1 = 0.0
LASThigh0 = 0.0
LASThigh1 = 0.0
min_rates_1 = 0
min_rates_total = 0
CHO_Handle = 0

def OnInit():
    global CHO_Handle, min_rates_1, min_rates_total
    CHO_Handle = iChaikin(None, 0, fast_ma_period, slow_ma_period, ma_method, applied_volume)
    if CHO_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iChaikin')
        return INIT_FAILED
    min_rates_1 = _int(MathMax(fast_ma_period, slow_ma_period))
    min_rates_total = min_rates_1 + ExtDepth + ExtBackstep
    SetIndexBuffer(0, CHOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, HighestBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(CHOBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZigZag_CHO')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LASThigh0, LASThigh1, LASThighpos, LASTlow0, LASTlow1, LASTlowpos
    if BarsCalculated(CHO_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    climit = 0
    bar = 0
    back = 0
    lasthighpos = 0
    lastlowpos = 0
    curlow = 0.0
    curhigh = 0.0
    lasthigh0 = EMPTY_VALUE
    lastlow0 = EMPTY_VALUE
    lasthigh1 = 0.0
    lastlow1 = 0.0
    val = 0.0
    res = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        lastlow1 = -1.0
        lasthigh1 = -1.0
        lastlowpos = -1
        lasthighpos = -1
    else:
        limit = rates_total - prev_calculated
        climit = limit + min_rates_total
        lastlow0 = LASTlow0
        lasthigh0 = LASThigh0
        lastlow1 = LASTlow1
        lasthigh1 = LASThigh1
        lastlowpos = LASTlowpos + limit
        lasthighpos = LASThighpos + limit
    to_copy = limit + 1
    if CopyBuffer(CHO_Handle, 0, 0, to_copy, CHOBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            LASTlow0 = lastlow0
            LASThigh0 = lasthigh0
        LowestBuffer[bar] = EMPTY_VALUE
        HighestBuffer[bar] = EMPTY_VALUE
        val = CHOBuffer[ArrayMinimum(CHOBuffer, bar, ExtDepth)]
        if val == lastlow0:
            val = EMPTY_VALUE
        else:
            lastlow0 = val
            if (CHOBuffer[bar] - val) > ExtDeviation:
                val = EMPTY_VALUE
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = LowestBuffer[bar + back]
                    if res != EMPTY_VALUE and res > val:
                        LowestBuffer[bar + back] = EMPTY_VALUE
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        LowestBuffer[bar] = val
        val = CHOBuffer[ArrayMaximum(CHOBuffer, bar, ExtDepth)]
        if val == lasthigh0:
            val = EMPTY_VALUE
        else:
            lasthigh0 = val
            if (val - CHOBuffer[bar]) > ExtDeviation:
                val = EMPTY_VALUE
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = HighestBuffer[bar + back]
                    if res != EMPTY_VALUE and res < val:
                        HighestBuffer[bar + back] = EMPTY_VALUE
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        HighestBuffer[bar] = val
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            LASTlow1 = lastlow1
            LASThigh1 = lasthigh1
            LASTlowpos = lastlowpos
            LASThighpos = lasthighpos
        curlow = LowestBuffer[bar]
        curhigh = HighestBuffer[bar]
        if curlow == EMPTY_VALUE and curhigh == EMPTY_VALUE:
            continue
        if curhigh != EMPTY_VALUE:
            if lasthigh1 > 0:
                if lasthigh1 < curhigh:
                    HighestBuffer[lasthighpos] = EMPTY_VALUE
                else:
                    HighestBuffer[bar] = EMPTY_VALUE
            if ((lasthigh1 < curhigh or lasthigh1 < 0) or curhigh == EMPTY_VALUE) or lasthigh1 == EMPTY_VALUE:
                lasthigh1 = curhigh
                lasthighpos = bar
            lastlow1 = -1.0
        if curlow != EMPTY_VALUE:
            if lastlow1 > 0:
                if lastlow1 > curlow:
                    LowestBuffer[lastlowpos] = EMPTY_VALUE
                else:
                    LowestBuffer[bar] = EMPTY_VALUE
            if ((curlow < lastlow1 or lastlow1 < 0) or curlow == EMPTY_VALUE) or lastlow1 == EMPTY_VALUE:
                lastlow1 = curlow
                lastlowpos = bar
            lasthigh1 = -1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigZagCHO(_MQL5Indicator):
    name = 'ZigZag_CHO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'fast_ma_period': 3,  # быстрый период
        'slow_ma_period': 10,  # медленный период
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # тип сглаживания
        'applied_volume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # используемый объем
        'ExtDepth': 3,
        'ExtDeviation': 3,
        'ExtBackstep': 3,
    }

