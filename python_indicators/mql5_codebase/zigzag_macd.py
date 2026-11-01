"""ZigZag_MACD — converted from MQL5: MQL5 Indicators/ZigZag_MACD/ZigZag_MACD.mq5

ZigZag
Copyright: Copyright © 2016, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 6}, 'colors': {1: [13959039, 14804223], 2: [9639167]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'MACD Oscillator', 2: 'ZigZag_MACD'}, 'levels': [], 'description': ['ZigZag'], 'name': 'ZigZag_MACD', 'source': 'MQL5 Indicators/ZigZag_MACD/ZigZag_MACD.mq5', 'folder': 'ZigZag_MACD', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 0, 'label': 'Вариант построения', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'uint', 'default': 12, 'label': 'быстрый период', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'uint', 'default': 26, 'label': 'медленный период', 'sinput': False}, {'mql': 'sign_ma_period', 'py': 'sign_ma_period', 'param': 'sign_ma_period', 'type': 'uint', 'default': 9, 'label': 'период усреднения разности', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'тип цены', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'double', 'default': 10.0, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE
MODE_MAIN = 0
MODE_SIGNAL = 1
_enum('ENUM_MODE', {0: 'MODE_MAIN', 1: 'MODE_SIGNAL'})

# ---- inputs and global variables
Mode = _input('Mode', MODE_MAIN)  # Вариант построения
fast_ma_period = _input('fast_ma_period', 12)  # быстрый период
slow_ma_period = _input('slow_ma_period', 26)  # медленный период
sign_ma_period = _input('sign_ma_period', 9)  # период усреднения разности
applied_price = _input('applied_price', PRICE_CLOSE)  # тип цены
ExtDepth = _input('ExtDepth', 3)
ExtDeviation = _input('ExtDeviation', 10.0)
ExtBackstep = _input('ExtBackstep', 5)
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
MACDBuffer = Arr(0, 0.0)
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
MACD_Handle = 0

def OnInit():
    global MACD_Handle, min_rates_1, min_rates_total
    MACD_Handle = iMACD(None, 0, fast_ma_period, slow_ma_period, sign_ma_period, applied_price)
    if MACD_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMACD')
        return INIT_FAILED
    min_rates_1 = _int(MathMax(fast_ma_period, slow_ma_period) + sign_ma_period)
    min_rates_total = _int(min_rates_1 + ExtDepth + ExtBackstep)
    SetIndexBuffer(0, MACDBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, HighestBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(MACDBuffer, True)
    ArraySetAsSeries(SignBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, 3)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZigZag_MACD')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LASThigh0, LASThigh1, LASThighpos, LASTlow0, LASTlow1, LASTlowpos
    if BarsCalculated(MACD_Handle) < rates_total or rates_total < min_rates_total:
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
    if CopyBuffer(MACD_Handle, 0, 0, to_copy, MACDBuffer) <= 0:
        return 0
    if CopyBuffer(MACD_Handle, 1, 0, to_copy, SignBuffer) <= 0:
        return 0
    if Mode == MODE_MAIN:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            if rates_total != prev_calculated and bar == 0:
                LASTlow0 = lastlow0
                LASThigh0 = lasthigh0
            LowestBuffer[bar] = EMPTY_VALUE
            HighestBuffer[bar] = EMPTY_VALUE
            val = MACDBuffer[ArrayMinimum(MACDBuffer, bar, ExtDepth)]
            if val == lastlow0:
                val = EMPTY_VALUE
            else:
                lastlow0 = val
                if (MACDBuffer[bar] - val) > (ExtDeviation * Point()):
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
            val = MACDBuffer[ArrayMaximum(MACDBuffer, bar, ExtDepth)]
            if val == lasthigh0:
                val = EMPTY_VALUE
            else:
                lasthigh0 = val
                if (val - MACDBuffer[bar]) > (ExtDeviation * Point()):
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


class ZigZagMACD(_MQL5Indicator):
    name = 'ZigZag_MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Mode': _Choice({0: 'Зигзаг по основной линии индикатора', 1: 'Зигзаг по сигнальной линии индикатора'}, default=0),  # Вариант построения
        'fast_ma_period': 12,  # быстрый период
        'slow_ma_period': 26,  # медленный период
        'sign_ma_period': 9,  # период усреднения разности
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # тип цены
        'ExtDepth': 3,
        'ExtDeviation': 10.0,
        'ExtBackstep': 5,
    }

