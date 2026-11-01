"""ZigZag_MomentumCandle — converted from MQL5: MQL5 Indicators/ZigZag_MomentumCandle/ZigZag_MomentumCandle.mq5

ZigZag_MomentumCandle
Copyright: Copyright © 2016, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 17, 2: 6}, 'colors': {1: [255, 8421504, 16760576], 2: [1262987]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'MomentumCandle Open;MomentumCandle High;MomentumCandle Low;MomentumCandle Close', 2: 'ZigZag_Momentum'}, 'levels': [], 'description': ['ZigZag_MomentumCandle'], 'name': 'ZigZag_MomentumCandle', 'source': 'MQL5 Indicators/ZigZag_MomentumCandle/ZigZag_MomentumCandle.mq5', 'folder': 'ZigZag_MomentumCandle', 'inputs': [{'mql': 'Momentum_period', 'py': 'Momentum_period', 'param': 'Momentum_period', 'type': 'uint', 'default': 12, 'label': 'период индикатора', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Momentum_period = _input('Momentum_period', 12)  # период индикатора
ExtDepth = _input('ExtDepth', 3)
ExtDeviation = _input('ExtDeviation', 3.0)
ExtBackstep = _input('ExtBackstep', 10)
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
LASTlowpos = 0
LASThighpos = 0
LASTColor = 0
LASTlow0 = 0.0
LASTlow1 = 0.0
LASThigh0 = 0.0
LASThigh1 = 0.0
min_rates_1 = 0
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_1, min_rates_total
    Ind_Handle[0] = iMomentum(None, 0, Momentum_period, PRICE_OPEN)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMomentum[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iMomentum(None, 0, Momentum_period, PRICE_HIGH)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMomentum[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iMomentum(None, 0, Momentum_period, PRICE_LOW)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMomentum[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iMomentum(None, 0, Momentum_period, PRICE_CLOSE)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMomentum[' + _str(3) + ']!')
        return INIT_FAILED
    min_rates_1 = _int(Momentum_period)
    min_rates_total = min_rates_1 + _int(ExtDepth + ExtBackstep)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    SetIndexBuffer(5, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, HighestBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZigZag_Momentum')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LASThigh0, LASThigh1, LASThighpos, LASTlow0, LASTlow1, LASTlowpos
    if (((BarsCalculated(Ind_Handle[0]) < rates_total or BarsCalculated(Ind_Handle[1]) < rates_total) or BarsCalculated(Ind_Handle[2]) < rates_total) or BarsCalculated(Ind_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
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
        lastlow0 = LASTlow0
        lasthigh0 = LASThigh0
        lastlow1 = LASTlow1
        lasthigh1 = LASThigh1
        lastlowpos = LASTlowpos + limit
        lasthighpos = LASThighpos + limit
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            LASTlow0 = lastlow0
            LASThigh0 = lasthigh0
        LowestBuffer[bar] = EMPTY_VALUE
        HighestBuffer[bar] = EMPTY_VALUE
        val = ExtLowBuffer[ArrayMinimum(ExtLowBuffer, bar, ExtDepth)]
        if val == lastlow0:
            val = EMPTY_VALUE
        else:
            lastlow0 = val
            if (ExtLowBuffer[bar] - val) > (ExtDeviation * Point()):
                val = EMPTY_VALUE
            else:
                back = 1
                for back in range(back, _int(ExtBackstep) + 1):
                    res = LowestBuffer[bar + back]
                    if res != EMPTY_VALUE and res > val:
                        LowestBuffer[bar + back] = EMPTY_VALUE
                else:
                    back = _range_end(back, _int(ExtBackstep) + 1, 1)
        LowestBuffer[bar] = val
        val = ExtHighBuffer[ArrayMaximum(ExtHighBuffer, bar, ExtDepth)]
        if val == lasthigh0:
            val = EMPTY_VALUE
        else:
            lasthigh0 = val
            if (val - ExtHighBuffer[bar]) > (ExtDeviation * Point()):
                val = EMPTY_VALUE
            else:
                back = 1
                for back in range(back, _int(ExtBackstep) + 1):
                    res = HighestBuffer[bar + back]
                    if res != EMPTY_VALUE and res < val:
                        HighestBuffer[bar + back] = EMPTY_VALUE
                else:
                    back = _range_end(back, _int(ExtBackstep) + 1, 1)
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


class ZigZagMomentumCandle(_MQL5Indicator):
    name = 'ZigZag_MomentumCandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Momentum_period': 12,  # период индикатора
        'ExtDepth': 3,
        'ExtDeviation': 3.0,
        'ExtBackstep': 10,
    }

