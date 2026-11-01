"""Four_MA_Strength — converted from MQL5: MQL5 Indicators/Four_MA_Strength_HTF/Four_MA_Strength.mq5

Copyright: Copyright © 2006, Custom Built For kurkafund on 11/05/2006 by David Honeywell; Link: kurkafund@yahoo.com , transport.david@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Custom Built For kurkafund on 11/05/2006 by David Honeywell', 'link': 'kurkafund@yahoo.com , transport.david@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Four_MA_Strength Upper', 2: 'Four_MA_Strength Lower'}, 'levels': [], 'description': [], 'name': 'Four_MA_Strength', 'source': 'MQL5 Indicators/Four_MA_Strength_HTF/Four_MA_Strength.mq5', 'folder': 'Four_MA_Strength_HTF', 'inputs': [{'mql': 'Ma1_Period', 'py': 'Ma1_Period', 'param': 'Ma1_Period', 'type': 'int', 'default': 8, 'label': 'Averaging period 1 for calculation.', 'sinput': False}, {'mql': 'Ma1_Method', 'py': 'Ma1_Method', 'param': 'Ma1_Method', 'type': 'int', 'default': 1, 'label': 'MA method 1. It can be any of the Moving Average method enumeration value.', 'sinput': False}, {'mql': 'Ma1_Price', 'py': 'Ma1_Price', 'param': 'Ma1_Price', 'type': 'int', 'default': 1, 'label': 'Applied price 1. It can be any of Applied price enumeration values.', 'sinput': False}, {'mql': 'Ma2_Period', 'py': 'Ma2_Period', 'param': 'Ma2_Period', 'type': 'int', 'default': 24, 'label': 'Averaging period 2 for calculation.', 'sinput': False}, {'mql': 'Ma2_Method', 'py': 'Ma2_Method', 'param': 'Ma2_Method', 'type': 'int', 'default': 1, 'label': 'MA metho 2. It can be any of the Moving Average method enumeration value.', 'sinput': False}, {'mql': 'Ma2_Price', 'py': 'Ma2_Price', 'param': 'Ma2_Price', 'type': 'int', 'default': 1, 'label': 'Applied price 2. It can be any of Applied price enumeration values.', 'sinput': False}, {'mql': 'Ma3_Period', 'py': 'Ma3_Period', 'param': 'Ma3_Period', 'type': 'int', 'default': 72, 'label': 'Averaging period 3 for calculation.', 'sinput': False}, {'mql': 'Ma3_Method', 'py': 'Ma3_Method', 'param': 'Ma3_Method', 'type': 'int', 'default': 1, 'label': 'MA method 3. It can be any of the Moving Average method enumeration value.', 'sinput': False}, {'mql': 'Ma3_Price', 'py': 'Ma3_Price', 'param': 'Ma3_Price', 'type': 'int', 'default': 1, 'label': 'Applied price 3. It can be any of Applied price enumeration values.', 'sinput': False}, {'mql': 'Ma4_Period', 'py': 'Ma4_Period', 'param': 'Ma4_Period', 'type': 'int', 'default': 216, 'label': 'Averaging period 4 for calculation.', 'sinput': False}, {'mql': 'Ma4_Method', 'py': 'Ma4_Method', 'param': 'Ma4_Method', 'type': 'int', 'default': 1, 'label': 'MA method 4. It can be any of the Moving Average method enumeration value.', 'sinput': False}, {'mql': 'Ma4_Price', 'py': 'Ma4_Price', 'param': 'Ma4_Price', 'type': 'int', 'default': 1, 'label': 'Applied price 4. It can be any of Applied price enumeration values.', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 3.501, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -3.501, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Ma1_Period = _input('Ma1_Period', 8)  # Averaging period 1 for calculation.
Ma1_Method = _input('Ma1_Method', MODE_EMA)  # MA method 1. It can be any of the Moving Average method enumeration value.
Ma1_Price = _input('Ma1_Price', PRICE_CLOSE)  # Applied price 1. It can be any of Applied price enumeration values.
Ma2_Period = _input('Ma2_Period', 24)  # Averaging period 2 for calculation.
Ma2_Method = _input('Ma2_Method', MODE_EMA)  # MA metho 2. It can be any of the Moving Average method enumeration value.
Ma2_Price = _input('Ma2_Price', PRICE_CLOSE)  # Applied price 2. It can be any of Applied price enumeration values.
Ma3_Period = _input('Ma3_Period', 72)  # Averaging period 3 for calculation.
Ma3_Method = _input('Ma3_Method', MODE_EMA)  # MA method 3. It can be any of the Moving Average method enumeration value.
Ma3_Price = _input('Ma3_Price', PRICE_CLOSE)  # Applied price 3. It can be any of Applied price enumeration values.
Ma4_Period = _input('Ma4_Period', 216)  # Averaging period 4 for calculation.
Ma4_Method = _input('Ma4_Method', MODE_EMA)  # MA method 4. It can be any of the Moving Average method enumeration value.
Ma4_Price = _input('Ma4_Price', PRICE_CLOSE)  # Applied price 4. It can be any of Applied price enumeration values.
HighLevel = _input('HighLevel', 3.501)  # уровень перекупленности
LowLevel = _input('LowLevel', -3.501)  # уровень перепроданности
LowerBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
min_rates_total = 0
MA_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = MathMax(Ma1_Period, MathMax(Ma2_Period, MathMax(Ma3_Period, Ma4_Period))) + 1
    MA_Handle[0] = iMA(None, 0, Ma1_Period, 0, Ma1_Method, Ma1_Price)
    if MA_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 1')
        return INIT_FAILED
    MA_Handle[1] = iMA(None, 0, Ma2_Period, 0, Ma2_Method, Ma2_Price)
    if MA_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 2')
        return INIT_FAILED
    MA_Handle[2] = iMA(None, 0, Ma3_Period, 0, Ma3_Method, Ma3_Price)
    if MA_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 3')
        return INIT_FAILED
    MA_Handle[3] = iMA(None, 0, Ma4_Period, 0, Ma4_Method, Ma4_Price)
    if MA_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 4')
        return INIT_FAILED
    SetIndexBuffer(0, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(LowerBuffer, True)
    SetIndexBuffer(1, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpperBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    short_name = 'Four_MA_Strength'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMediumSeaGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(MA_Handle[0]) < rates_total or BarsCalculated(MA_Handle[1]) < rates_total) or BarsCalculated(MA_Handle[2]) < rates_total) or BarsCalculated(MA_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Ma1 = Arr(0, 0.0)
    Ma2 = Arr(0, 0.0)
    Ma3 = Arr(0, 0.0)
    Ma4 = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MA_Handle[0], 0, 0, to_copy, Ma1) <= 0:
        return 0
    if CopyBuffer(MA_Handle[1], 0, 0, to_copy, Ma2) <= 0:
        return 0
    if CopyBuffer(MA_Handle[2], 0, 0, to_copy, Ma3) <= 0:
        return 0
    if CopyBuffer(MA_Handle[3], 0, 0, to_copy, Ma4) <= 0:
        return 0
    ArraySetAsSeries(Ma1, True)
    ArraySetAsSeries(Ma2, True)
    ArraySetAsSeries(Ma3, True)
    ArraySetAsSeries(Ma4, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ustrength1 = 0.0
        ustrength2 = 0.0
        ustrength3 = 0.0
        ustrength4 = 0.0
        ustrength5 = 0.0
        ustrength6 = 0.0
        dstrength1 = 0.0
        dstrength2 = 0.0
        dstrength3 = 0.0
        dstrength4 = 0.0
        dstrength5 = 0.0
        dstrength6 = 0.0
        Ma1_0 = Ma1[bar] * 1000
        Ma2_0 = Ma2[bar] * 1000
        Ma3_0 = Ma3[bar] * 1000
        Ma4_0 = Ma4[bar] * 1000
        if Ma1_0 > Ma2_0:
            ustrength1 = 0.25
        if Ma1_0 < Ma2_0:
            dstrength1 = -0.25
        if Ma1_0 > Ma2_0 and Ma1_0 > Ma3_0:
            ustrength2 = 0.5
        if Ma1_0 < Ma2_0 and Ma1_0 < Ma3_0:
            dstrength2 = -0.5
        if (Ma1_0 > Ma2_0 and Ma1_0 > Ma3_0) and Ma1_0 > Ma4_0:
            ustrength3 = 0.75
        if (Ma1_0 < Ma2_0 and Ma1_0 < Ma3_0) and Ma1_0 < Ma4_0:
            dstrength3 = -0.75
        if ((Ma1_0 > Ma2_0 and Ma1_0 > Ma3_0) and Ma1_0 > Ma4_0) and Ma2_0 > Ma3_0:
            ustrength4 = 1.0
        if ((Ma1_0 < Ma2_0 and Ma1_0 < Ma3_0) and Ma1_0 < Ma4_0) and Ma2_0 < Ma3_0:
            dstrength4 = -1.0
        if (((Ma1_0 > Ma2_0 and Ma1_0 > Ma3_0) and Ma1_0 > Ma4_0) and Ma2_0 > Ma3_0) and Ma2_0 > Ma4_0:
            ustrength5 = 1.25
        if (((Ma1_0 < Ma2_0 and Ma1_0 < Ma3_0) and Ma1_0 < Ma4_0) and Ma2_0 < Ma3_0) and Ma2_0 < Ma4_0:
            dstrength5 = -1.25
        if ((((Ma1_0 > Ma2_0 and Ma1_0 > Ma3_0) and Ma1_0 > Ma4_0) and Ma2_0 > Ma3_0) and Ma2_0 > Ma4_0) and Ma3_0 > Ma4_0:
            ustrength6 = 1.5
        if ((((Ma1_0 < Ma2_0 and Ma1_0 < Ma3_0) and Ma1_0 < Ma4_0) and Ma2_0 < Ma3_0) and Ma2_0 < Ma4_0) and Ma3_0 > Ma4_0:
            dstrength6 = -1.5
        UpperBuffer[bar] = ustrength1 + ustrength2 + ustrength3 + ustrength4 + ustrength5 + ustrength6
        LowerBuffer[bar] = dstrength1 + dstrength2 + dstrength3 + dstrength4 + dstrength5 + dstrength6
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FourMAStrength(_MQL5Indicator):
    name = 'Four_MA_Strength'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Ma1_Period': 8,  # Averaging period 1 for calculation.
        'Ma1_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA method 1. It can be any of the Moving Average method enumeration value.
        'Ma1_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price 1. It can be any of Applied price enumeration values.
        'Ma2_Period': 24,  # Averaging period 2 for calculation.
        'Ma2_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA metho 2. It can be any of the Moving Average method enumeration value.
        'Ma2_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price 2. It can be any of Applied price enumeration values.
        'Ma3_Period': 72,  # Averaging period 3 for calculation.
        'Ma3_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA method 3. It can be any of the Moving Average method enumeration value.
        'Ma3_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price 3. It can be any of Applied price enumeration values.
        'Ma4_Period': 216,  # Averaging period 4 for calculation.
        'Ma4_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA method 4. It can be any of the Moving Average method enumeration value.
        'Ma4_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price 4. It can be any of Applied price enumeration values.
        'HighLevel': 3.501,  # уровень перекупленности
        'LowLevel': -3.501,  # уровень перепроданности
    }

