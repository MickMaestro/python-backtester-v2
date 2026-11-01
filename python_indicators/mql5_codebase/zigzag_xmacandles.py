"""ZigZag_XMACandles — converted from MQL5: MQL5 Indicators/ZigZag_XMACandles/ZigZag_XMACandles.mq5

ZigZag_XMACandles
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 17, 2: 6}, 'colors': {1: [13850042, 13458026, 32768], 2: [8388736]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'XMACandles Open;XMACandles High;XMACandles Low;XMACandles Close', 2: 'ZigZag_XMACandles'}, 'levels': [], 'description': ['ZigZag_XMACandles'], 'name': 'ZigZag_XMACandles', 'source': 'MQL5 Indicators/ZigZag_XMACandles/ZigZag_XMACandles.mq5', 'folder': 'ZigZag_XMACandles', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 7, 'label': 'Метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 12, 'label': 'Глубина первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр первого сглаживания,', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_T3)  # Метод усреднения первого сглаживания
Length1 = _input('Length1', 12)  # Глубина первого сглаживания
Phase1 = _input('Phase1', 15)  # Параметр первого сглаживания,
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
Ind_Handle = 0

def OnInit():
    global Ind_Handle, min_rates_1, min_rates_total
    Ind_Handle = iCustom(None, 0, 'XMACandles', MA_Method1, Length1, Phase1, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XMACandles!')
        return INIT_FAILED
    min_rates_1 = GetStartBars(MA_Method1, Length1, Phase1)
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
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZigZag_MACD')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LASThigh0, LASThigh1, LASThighpos, LASTlow0, LASTlow1, LASTlowpos
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
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
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 1, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 2, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 3, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, 4, 0, to_copy, ExtColorBuffer) <= 0:
        return 0
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


class ZigZagXMACandles(_MQL5Indicator):
    name = 'ZigZag_XMACandles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения первого сглаживания
        'Length1': 12,  # Глубина первого сглаживания
        'Phase1': 15,  # Параметр первого сглаживания,
        'ExtDepth': 3,
        'ExtDeviation': 3.0,
        'ExtBackstep': 10,
    }

