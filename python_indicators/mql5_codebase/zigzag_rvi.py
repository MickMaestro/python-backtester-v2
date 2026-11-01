"""ZigZag_RVI — converted from MQL5: MQL5 Indicators/ZigZag_RVI/ZigZag_RVI.mq5

ZigZag
Copyright: Copyright © 2016, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 6}, 'colors': {1: [10025880, 13353215], 2: [16711680]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'RVI Oscillator', 2: 'ZigZag_RVI'}, 'levels': [], 'description': ['ZigZag'], 'name': 'ZigZag_RVI', 'source': 'MQL5 Indicators/ZigZag_RVI/ZigZag_RVI.mq5', 'folder': 'ZigZag_RVI', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 0, 'label': 'Вариант построения', 'sinput': False}, {'mql': 'RVI_period', 'py': 'RVI_period', 'param': 'RVI_period', 'type': 'uint', 'default': 13, 'label': 'период RVI', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 0.1, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -0.1, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE
MODE_MAIN = 0
MODE_SIGNAL = 1
_enum('ENUM_MODE', {0: 'MODE_MAIN', 1: 'MODE_SIGNAL'})

# ---- inputs and global variables
Mode = _input('Mode', MODE_MAIN)  # Вариант построения
RVI_period = _input('RVI_period', 13)  # период RVI
ExtDepth = _input('ExtDepth', 3)
ExtDeviation = _input('ExtDeviation', 0.1)
ExtBackstep = _input('ExtBackstep', 3)
HighLevel = _input('HighLevel', 0.1)  # уровень перезакупа
LowLevel = _input('LowLevel', -0.1)  # уровень перепроданности
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
RVIBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
LASTlowpos = 0
LASThighpos = 0
LASTColor = 0
LASTlow0 = 0.0
LASTlow1 = 0.0
LASThigh0 = 0.0
LASThigh1 = 0.0
min_rates_1 = 0
min_rates_total = 0
RVI_Handle = 0

def OnInit():
    global RVI_Handle, min_rates_1, min_rates_total
    RVI_Handle = iRVI(None, 0, RVI_period)
    if RVI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRVI')
        return INIT_FAILED
    min_rates_1 = _int(RVI_period)
    min_rates_total = _int(min_rates_1 + ExtDepth + ExtBackstep)
    SetIndexBuffer(0, RVIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, HighestBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(RVIBuffer, True)
    ArraySetAsSeries(SignBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, 3)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZigZag_RVI')
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrDodgerBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LASThigh0, LASThigh1, LASThighpos, LASTlow0, LASTlow1, LASTlowpos
    if BarsCalculated(RVI_Handle) < rates_total or rates_total < min_rates_total:
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
    if CopyBuffer(RVI_Handle, 0, 0, to_copy, RVIBuffer) <= 0:
        return 0
    if CopyBuffer(RVI_Handle, 1, 0, to_copy, SignBuffer) <= 0:
        return 0
    if Mode == MODE_MAIN:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            if rates_total != prev_calculated and bar == 0:
                LASTlow0 = lastlow0
                LASThigh0 = lasthigh0
            LowestBuffer[bar] = EMPTY_VALUE
            HighestBuffer[bar] = EMPTY_VALUE
            val = RVIBuffer[ArrayMinimum(RVIBuffer, bar, ExtDepth)]
            if val == lastlow0:
                val = EMPTY_VALUE
            else:
                lastlow0 = val
                if (RVIBuffer[bar] - val) > ExtDeviation:
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
            val = RVIBuffer[ArrayMaximum(RVIBuffer, bar, ExtDepth)]
            if val == lasthigh0:
                val = EMPTY_VALUE
            else:
                lasthigh0 = val
                if (val - RVIBuffer[bar]) > ExtDeviation:
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
    if Mode == MODE_SIGNAL:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            if rates_total != prev_calculated and bar == 0:
                LASTlow0 = lastlow0
                LASThigh0 = lasthigh0
            LowestBuffer[bar] = EMPTY_VALUE
            HighestBuffer[bar] = EMPTY_VALUE
            val = SignBuffer[ArrayMinimum(SignBuffer, bar, ExtDepth)]
            if val == lastlow0:
                val = EMPTY_VALUE
            else:
                lastlow0 = val
                if (SignBuffer[bar] - val) > ExtDeviation:
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
            val = SignBuffer[ArrayMaximum(SignBuffer, bar, ExtDepth)]
            if val == lasthigh0:
                val = EMPTY_VALUE
            else:
                lasthigh0 = val
                if (val - SignBuffer[bar]) > ExtDeviation:
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


class ZigZagRVI(_MQL5Indicator):
    name = 'ZigZag_RVI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Mode': _Choice({0: 'Зигзаг по основной линии индикатора', 1: 'Зигзаг по сигнальной линии индикатора'}, default=0),  # Вариант построения
        'RVI_period': 13,  # период RVI
        'ExtDepth': 3,
        'ExtDeviation': 0.1,
        'ExtBackstep': 3,
        'HighLevel': 0.1,  # уровень перезакупа
        'LowLevel': -0.1,  # уровень перепроданности
    }

