"""bollinger_squeeze_v9 — converted from MQL5: MQL5 Indicators/Bollinger_Squeeze_v9_HTF/bollinger_squeeze_v9.mq5

Copyright: Copyright © 2006, Akuma99; Link: http://www.beginnertrader.com ; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Akuma99', 'link': 'http://www.beginnertrader.com ', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [255, 14053594, 8421504, 16748574, 65280], 2: [14822282]}, 'widths': {1: 4, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bollinger_Squeeze_v9 HISTOGRAM', 2: 'Bollinger_Squeeze_v9 LINE'}, 'levels': [], 'description': [], 'name': 'bollinger_squeeze_v9', 'source': 'MQL5 Indicators/Bollinger_Squeeze_v9_HTF/bollinger_squeeze_v9.mq5', 'folder': 'Bollinger_Squeeze_v9_HTF', 'inputs': [{'mql': 'triggerType', 'py': 'triggerType', 'param': 'triggerType', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'stochPeriod_trigger1', 'py': 'stochPeriod_trigger1', 'param': 'stochPeriod_trigger1', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'cciPeriod_trigger2', 'py': 'cciPeriod_trigger2', 'param': 'cciPeriod_trigger2', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'rsiPeriod_trigger3', 'py': 'rsiPeriod_trigger3', 'param': 'rsiPeriod_trigger3', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'macd_fastEMA_trigger4', 'py': 'macd_fastEMA_trigger4', 'param': 'macd_fastEMA_trigger4', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'macd_slowEMA_trigger4', 'py': 'macd_slowEMA_trigger4', 'param': 'macd_slowEMA_trigger4', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'macd_macdEMA_trigger4', 'py': 'macd_macdEMA_trigger4', 'param': 'macd_macdEMA_trigger4', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'momentumPeriod_trigger5', 'py': 'momentumPeriod_trigger5', 'param': 'momentumPeriod_trigger5', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Mode
ENAME_STOCHASTIC = 1
ENAME_CCI = 2
ENAME_RSI = 3
ENAME_MACD = 4
ENAME_MOMENTUM = 5
_enum('Mode', {1: 'ENAME_STOCHASTIC', 2: 'ENAME_CCI', 3: 'ENAME_RSI', 4: 'ENAME_MACD', 5: 'ENAME_MOMENTUM'})

# ---- inputs and global variables
triggerType = _input('triggerType', ENAME_MACD)
stochPeriod_trigger1 = _input('stochPeriod_trigger1', 14)
cciPeriod_trigger2 = _input('cciPeriod_trigger2', 50)
rsiPeriod_trigger3 = _input('rsiPeriod_trigger3', 10)
macd_fastEMA_trigger4 = _input('macd_fastEMA_trigger4', 5)
macd_slowEMA_trigger4 = _input('macd_slowEMA_trigger4', 13)
macd_macdEMA_trigger4 = _input('macd_macdEMA_trigger4', 1)
momentumPeriod_trigger5 = _input('momentumPeriod_trigger5', 14)
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
LineBuffer = Arr(0, 0.0)
bolPrd = 20
bolDev = 2.0
keltPrd = 20
keltFactor = 1.5
Ind_Handle = 0
ATR_Handle = 0
Std_Handle = 0

def OnInit():
    global ATR_Handle, Ind_Handle, Std_Handle, min_rates_total
    _sw1 = triggerType
    if _sw1 == 1:
        min_rates_total = _int(stochPeriod_trigger1 + 3 + 3)
    elif _sw1 == 2:
        min_rates_total = _int(cciPeriod_trigger2)
    elif _sw1 == 3:
        min_rates_total = _int(rsiPeriod_trigger3)
    elif _sw1 == 4:
        min_rates_total = 5 + 13 + 1
    elif _sw1 == 5:
        min_rates_total = _int(momentumPeriod_trigger5)
    min_rates_total = MathMax(MathMax(min_rates_total, bolPrd), keltPrd)
    _sw2 = triggerType
    if _sw2 == 1:
        Ind_Handle = iStochastic(None, 0, stochPeriod_trigger1, 3, 3, MODE_SMA, STO_CLOSECLOSE)
    elif _sw2 == 2:
        Ind_Handle = iCCI(None, 0, cciPeriod_trigger2, PRICE_CLOSE)
    elif _sw2 == 3:
        Ind_Handle = iRSI(None, 0, rsiPeriod_trigger3, PRICE_CLOSE)
    elif _sw2 == 4:
        Ind_Handle = iMACD(None, 0, 5, 13, 1, PRICE_CLOSE)
    elif _sw2 == 5:
        Ind_Handle = iMomentum(None, 0, momentumPeriod_trigger5, PRICE_CLOSE)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора!')
    ATR_Handle = iATR(None, 0, keltPrd)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора!')
    Std_Handle = iStdDev(None, 0, bolPrd, 0, MODE_SMA, PRICE_CLOSE)
    if Std_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора!')
    _sw3 = triggerType
    if _sw3 == 1:
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 30)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -30)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    elif _sw3 == 2:
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
    elif _sw3 == 3:
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 20)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -20)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    elif _sw3 == 4:
        IndicatorSetInteger(INDICATOR_LEVELS, 0)
    elif _sw3 == 5:
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -1)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    SetIndexBuffer(2, LineBuffer, INDICATOR_DATA)
    ArraySetAsSeries(LineBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    _sw4 = triggerType
    if _sw4 == 1:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with Stochastic (' + _str(stochPeriod_trigger1) + ',3,3)')
    elif _sw4 == 2:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with CCI (' + _str(cciPeriod_trigger2) + ',CLOSE)')
    elif _sw4 == 3:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with RSI (' + _str(rsiPeriod_trigger3) + ',CLOSE)')
    elif _sw4 == 4:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with MACD (5,13,1,CLOSE)')
    elif _sw4 == 5:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Squeeze with Momentum (' + _str(momentumPeriod_trigger5) + ',CLOSE)')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(Ind_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or BarsCalculated(Std_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    clr = 0
    d = 0.0
    Value = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    STD = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, Value) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(Std_Handle, 0, 0, to_copy, STD) <= 0:
        return 0
    ArraySetAsSeries(Value, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(STD, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        _sw5 = triggerType
        if _sw5 == 1:
            d = Value[bar] - 50
        elif _sw5 == 2:
            d = Value[bar]
        elif _sw5 == 3:
            d = Value[bar] - 50
        elif _sw5 == 4:
            d = Value[bar]
        elif _sw5 == 5:
            d = Value[bar] - 100
        IndBuffer[bar] = d
        LineBuffer[bar] = d
        clr = 2
        if d > 0:
            clr = 4
        elif d < 0:
            clr = 0
        bbs = _fdiv(bolDev * STD[bar], ATR[bar] * keltFactor)
        if bbs < 1:
            if d > 0:
                clr = 3
            else:
                clr = 1
        else:
            if d > 0:
                clr = 4
            else:
                clr = 0
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerSqueezeV9(_MQL5Indicator):
    name = 'bollinger_squeeze_v9'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'triggerType': _Choice({1: 'stochastic', 2: 'cci', 3: 'rsi', 4: 'macd', 5: 'momentum'}, default=4),
        'stochPeriod_trigger1': 14,
        'cciPeriod_trigger2': 50,
        'rsiPeriod_trigger3': 10,
        'macd_fastEMA_trigger4': 5,
        'macd_slowEMA_trigger4': 13,
        'macd_macdEMA_trigger4': 1,
        'momentumPeriod_trigger5': 14,
    }

