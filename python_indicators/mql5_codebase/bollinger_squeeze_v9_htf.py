"""bollinger_squeeze_v9_htf — converted from MQL5: MQL5 Indicators/Bollinger_Squeeze_v9_HTF/bollinger_squeeze_v9_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 14053594, 8421504, 16748574, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Bollinger_Squeeze_v9 HISTOGRAM'}, 'levels': [], 'description': [], 'name': 'bollinger_squeeze_v9_htf', 'source': 'MQL5 Indicators/Bollinger_Squeeze_v9_HTF/bollinger_squeeze_v9_htf.mq5', 'folder': 'Bollinger_Squeeze_v9_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'triggerType', 'py': 'triggerType', 'param': 'triggerType', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'stochPeriod_trigger1', 'py': 'stochPeriod_trigger1', 'param': 'stochPeriod_trigger1', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'cciPeriod_trigger2', 'py': 'cciPeriod_trigger2', 'param': 'cciPeriod_trigger2', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'rsiPeriod_trigger3', 'py': 'rsiPeriod_trigger3', 'param': 'rsiPeriod_trigger3', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'macd_fastEMA_trigger4', 'py': 'macd_fastEMA_trigger4', 'param': 'macd_fastEMA_trigger4', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'macd_slowEMA_trigger4', 'py': 'macd_slowEMA_trigger4', 'param': 'macd_slowEMA_trigger4', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'macd_macdEMA_trigger4', 'py': 'macd_macdEMA_trigger4', 'param': 'macd_macdEMA_trigger4', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'momentumPeriod_trigger5', 'py': 'momentumPeriod_trigger5', 'param': 'momentumPeriod_trigger5', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Mode
ENAME_STOCHASTIC = 1
ENAME_CCI = 2
ENAME_RSI = 3
ENAME_MACD = 4
ENAME_MOMENTUM = 5
_enum('Mode', {1: 'ENAME_STOCHASTIC', 2: 'ENAME_CCI', 3: 'ENAME_RSI', 4: 'ENAME_MACD', 5: 'ENAME_MOMENTUM'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
triggerType = _input('triggerType', ENAME_MACD)
stochPeriod_trigger1 = _input('stochPeriod_trigger1', 14)
cciPeriod_trigger2 = _input('cciPeriod_trigger2', 50)
rsiPeriod_trigger3 = _input('rsiPeriod_trigger3', 10)
macd_fastEMA_trigger4 = _input('macd_fastEMA_trigger4', 5)
macd_slowEMA_trigger4 = _input('macd_slowEMA_trigger4', 13)
macd_macdEMA_trigger4 = _input('macd_macdEMA_trigger4', 1)
momentumPeriod_trigger5 = _input('momentumPeriod_trigger5', 14)
ReDraw = _input('ReDraw', True)  # Повтор отображения инфомации на пустых барах
min_rates_total = 0
Ind_Handle = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 3
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора Bollinger_Squeeze_v9 не может быть меньше периода текущего графика')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Bollinger_Squeeze_v9', triggerType, stochPeriod_trigger1, cciPeriod_trigger2, rsiPeriod_trigger3, macd_fastEMA_trigger4, macd_slowEMA_trigger4, macd_macdEMA_trigger4, momentumPeriod_trigger5)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Bollinger_Squeeze_v9')
        return INIT_FAILED
    _sw1 = triggerType
    if _sw1 == 1:
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 30)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -30)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    elif _sw1 == 2:
        IndicatorSetInteger(INDICATOR_LEVELS, 4)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 200)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 100)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -100)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, -200)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)
    elif _sw1 == 3:
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 20)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -20)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    elif _sw1 == 4:
        IndicatorSetInteger(INDICATOR_LEVELS, 0)
    elif _sw1 == 5:
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -1)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    _sw2 = triggerType
    if _sw2 == 1:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with Stochastic (' + _str(stochPeriod_trigger1) + ',3,3)')
    elif _sw2 == 2:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with CCI (' + _str(cciPeriod_trigger2) + ',CLOSE)')
    elif _sw2 == 3:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with RSI (' + _str(rsiPeriod_trigger3) + ',CLOSE)')
    elif _sw2 == 4:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with MACD (5,13,1,CLOSE)')
    elif _sw2 == 5:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with Momentum (' + _str(momentumPeriod_trigger5) + ',CLOSE)')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    Ind = Arr(1, 0.0, dyn=False)
    Col = Arr(1, 0.0, dyn=False)
    IndTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = EMPTY_VALUE
        ColorIndBuffer[bar] = 0.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, IndTime) <= 0:
            return 0
        if time[bar] >= IndTime[0] and time[bar + 1] < IndTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 1, Ind) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 1, _DT(time[bar]), 1, Col) <= 0:
                return 0
            IndBuffer[bar] = Ind[0]
            ColorIndBuffer[bar] = Col[0]
        if ReDraw:
            if IndBuffer[bar + 1] != EMPTY_VALUE and IndBuffer[bar] == EMPTY_VALUE:
                IndBuffer[bar] = IndBuffer[bar + 1]
                ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerSqueezeV9Htf(_MQL5Indicator):
    name = 'bollinger_squeeze_v9_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'triggerType': _Choice({1: 'stochastic', 2: 'cci', 3: 'rsi', 4: 'macd', 5: 'momentum'}, default=4),
        'stochPeriod_trigger1': 14,
        'cciPeriod_trigger2': 50,
        'rsiPeriod_trigger3': 10,
        'macd_fastEMA_trigger4': 5,
        'macd_slowEMA_trigger4': 13,
        'macd_macdEMA_trigger4': 1,
        'momentumPeriod_trigger5': 14,
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }

