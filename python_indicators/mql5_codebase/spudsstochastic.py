"""spudsstochastic — converted from MQL5: MQL5 Indicators/SpudsStochastic/spudsstochastic.mq5

The composition of the indicator - 8 stochastic oscillators.
Parameters «slow» and «period %D» leave the default – 3.
Parameter %K will change from 6 to 24.
The result - 8 stochastics with parameters (6, 3, 3), (7, 3, 3), (8, 3, 3) … (24, 3, 3).
All indicators are used only the main line.
Copyright: Copyright © 2012, Vladimir Hlystov; Link: cmillion@narod.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Vladimir Hlystov', 'link': 'cmillion@narod.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 9, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 10}, 'colors': {1: [12632256], 2: [16711680], 3: [16711680], 4: [16711680], 5: [65535], 6: [255], 7: [255], 8: [255], 9: [8421504, 16711935, 8421376]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 5}, 'styles': {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 0}, 'labels': {1: 'Стохастик 1', 2: 'Стохастик 2', 3: 'Стохастик 3', 4: 'Стохастик 4', 5: 'Стохастик 5', 6: 'Стохастик 6', 7: 'Стохастик 7', 8: 'Стохастик 8', 9: 'Сигнал'}, 'levels': [], 'description': ['The composition of the indicator - 8 stochastic oscillators.', 'Parameters «slow» and «period %D» leave the default – 3.', 'Parameter %K will change from 6 to 24.', 'The result - 8 stochastics with parameters (6, 3, 3), (7, 3, 3), (8, 3, 3) … (24, 3, 3).', 'All indicators are used only the main line.'], 'name': 'spudsstochastic', 'source': 'MQL5 Indicators/SpudsStochastic/spudsstochastic.mq5', 'folder': 'SpudsStochastic', 'inputs': [{'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'int', 'default': 85, 'label': 'level of overbought zone', 'sinput': False}, {'mql': 'LevelDn', 'py': 'LevelDn', 'param': 'LevelDn', 'type': 'int', 'default': 15, 'label': 'level of oversold zone', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'smoothing type', 'sinput': False}, {'mql': 'price_field', 'py': 'price_field', 'param': 'price_field', 'type': 'int', 'default': 0, 'label': 'stochastic calculation method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Gray = 0x808080  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# ---- inputs and global variables
LevelUp = _input('LevelUp', 85)  # level of overbought zone
LevelDn = _input('LevelDn', 15)  # level of oversold zone
ma_method = _input('ma_method', MODE_SMA)  # smoothing type
price_field = _input('price_field', STO_LOWHIGH)  # stochastic calculation method
LineBuffer1 = Arr(0, 0.0)
LineBuffer2 = Arr(0, 0.0)
LineBuffer3 = Arr(0, 0.0)
LineBuffer4 = Arr(0, 0.0)
LineBuffer5 = Arr(0, 0.0)
LineBuffer6 = Arr(0, 0.0)
LineBuffer7 = Arr(0, 0.0)
LineBuffer8 = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
ColorSignBuffer = Arr(0, 0.0)
min_rates_total = 0
STO_Handle = Arr(8, 0, dyn=False)
Signal = 0

def OnInit():
    global Signal, min_rates_total
    min_rates_total = 24 + 3 + 3 + 1
    Signal = 0
    STO_Handle[0] = iStochastic(None, 0, 6, 3, 3, ma_method, price_field)
    STO_Handle[1] = iStochastic(None, 0, 9, 3, 3, ma_method, price_field)
    STO_Handle[2] = iStochastic(None, 0, 12, 3, 3, ma_method, price_field)
    STO_Handle[3] = iStochastic(None, 0, 14, 3, 3, ma_method, price_field)
    STO_Handle[4] = iStochastic(None, 0, 16, 3, 3, ma_method, price_field)
    STO_Handle[5] = iStochastic(None, 0, 19, 3, 3, ma_method, price_field)
    STO_Handle[6] = iStochastic(None, 0, 21, 3, 3, ma_method, price_field)
    STO_Handle[7] = iStochastic(None, 0, 24, 3, 3, ma_method, price_field)
    if STO_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    if STO_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    if STO_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    if STO_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    if STO_Handle[4] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    if STO_Handle[5] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    if STO_Handle[6] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    if STO_Handle[7] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    SetIndexBuffer(0, LineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, LineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, LineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, LineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, LineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(5, LineBuffer6, INDICATOR_DATA)
    SetIndexBuffer(6, LineBuffer7, INDICATOR_DATA)
    SetIndexBuffer(7, LineBuffer8, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LineBuffer1, True)
    ArraySetAsSeries(LineBuffer2, True)
    ArraySetAsSeries(LineBuffer3, True)
    ArraySetAsSeries(LineBuffer4, True)
    ArraySetAsSeries(LineBuffer5, True)
    ArraySetAsSeries(LineBuffer6, True)
    ArraySetAsSeries(LineBuffer7, True)
    ArraySetAsSeries(LineBuffer8, True)
    SetIndexBuffer(8, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SignBuffer, True)
    SetIndexBuffer(9, ColorSignBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(9, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorSignBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Spuds Stochastic(', EnumToString(ma_method, 'ENUM_MA_METHOD'), ', ', EnumToString(price_field, 'ENUM_STO_PRICE'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, LevelUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LevelDn)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, Gray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Signal
    if (((((((BarsCalculated(STO_Handle[0]) < rates_total or BarsCalculated(STO_Handle[1]) < rates_total) or BarsCalculated(STO_Handle[2]) < rates_total) or BarsCalculated(STO_Handle[3]) < rates_total) or BarsCalculated(STO_Handle[4]) < rates_total) or BarsCalculated(STO_Handle[5]) < rates_total) or BarsCalculated(STO_Handle[6]) < rates_total) or BarsCalculated(STO_Handle[7]) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(STO_Handle[0], MAIN_LINE, 0, to_copy, LineBuffer1) <= 0:
        return 0
    if CopyBuffer(STO_Handle[1], MAIN_LINE, 0, to_copy, LineBuffer2) <= 0:
        return 0
    if CopyBuffer(STO_Handle[2], MAIN_LINE, 0, to_copy, LineBuffer3) <= 0:
        return 0
    if CopyBuffer(STO_Handle[3], MAIN_LINE, 0, to_copy, LineBuffer4) <= 0:
        return 0
    if CopyBuffer(STO_Handle[4], MAIN_LINE, 0, to_copy, LineBuffer5) <= 0:
        return 0
    if CopyBuffer(STO_Handle[5], MAIN_LINE, 0, to_copy, LineBuffer6) <= 0:
        return 0
    if CopyBuffer(STO_Handle[6], MAIN_LINE, 0, to_copy, LineBuffer7) <= 0:
        return 0
    if CopyBuffer(STO_Handle[7], MAIN_LINE, 0, to_copy, LineBuffer8) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SignBuffer[bar] = EMPTY_VALUE
        ColorSignBuffer[bar] = 0.0
        if (((((((LineBuffer1[bar + 1] > LevelUp and LineBuffer2[bar + 1] > LevelUp) and LineBuffer3[bar + 1] > LevelUp) and LineBuffer4[bar + 1] > LevelUp) and LineBuffer5[bar + 1] > LevelUp) and LineBuffer6[bar + 1] > LevelUp) and LineBuffer7[bar + 1] > LevelUp) and LineBuffer8[bar + 1] > LevelUp) or (((((((LineBuffer1[bar + 1] < LevelDn and LineBuffer2[bar + 1] < LevelDn) and LineBuffer3[bar + 1] < LevelDn) and LineBuffer4[bar + 1] < LevelDn) and LineBuffer5[bar + 1] < LevelDn) and LineBuffer6[bar + 1] < LevelDn) and LineBuffer7[bar + 1] < LevelDn) and LineBuffer8[bar + 1] < LevelDn):
            Signal = 0
        if (((((((LineBuffer1[bar] > LevelDn and LineBuffer2[bar] > LevelDn) and LineBuffer3[bar] > LevelDn) and LineBuffer4[bar] > LevelDn) and LineBuffer5[bar] > LevelDn) and LineBuffer6[bar] > LevelDn) and LineBuffer7[bar] > LevelDn) and LineBuffer8[bar] > LevelDn) and (((((((LineBuffer1[bar + 1] < LevelDn or LineBuffer2[bar + 1] < LevelDn) or LineBuffer3[bar + 1] < LevelDn) or LineBuffer4[bar + 1] < LevelDn) or LineBuffer5[bar + 1] < LevelDn) or LineBuffer6[bar + 1] < LevelDn) or LineBuffer7[bar + 1] < LevelDn) or LineBuffer8[bar + 1] < LevelDn):
            if not Signal:
                SignBuffer[bar] = 100.0
                ColorSignBuffer[bar] = 2.0
                Signal = 1
        if (((((((LineBuffer1[bar] < LevelUp and LineBuffer2[bar] < LevelUp) and LineBuffer3[bar] < LevelUp) and LineBuffer4[bar] < LevelUp) and LineBuffer5[bar] < LevelUp) and LineBuffer6[bar] < LevelUp) and LineBuffer7[bar] < LevelUp) and LineBuffer8[bar] < LevelUp) and (((((((LineBuffer1[bar + 1] > LevelUp or LineBuffer2[bar + 1] > LevelUp) or LineBuffer3[bar + 1] > LevelUp) or LineBuffer4[bar + 1] > LevelUp) or LineBuffer5[bar + 1] > LevelUp) or LineBuffer6[bar + 1] > LevelUp) or LineBuffer7[bar + 1] > LevelUp) or LineBuffer8[bar + 1] > LevelUp):
            if not Signal:
                SignBuffer[bar] = 100.0
                ColorSignBuffer[bar] = 1.0
                Signal = -1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Spudsstochastic(_MQL5Indicator):
    name = 'spudsstochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LevelUp': 85,  # level of overbought zone
        'LevelDn': 15,  # level of oversold zone
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # smoothing type
        'price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # stochastic calculation method
    }
    y_range = (0.0, 100.0)

