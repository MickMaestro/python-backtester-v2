"""Four_MA_Strength_HTF — converted from MQL5: MQL5 Indicators/Four_MA_Strength_HTF/Four_MA_Strength_HTF.mq5

DX_Smoothed с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {1: 0}, 'labels': {1: 'Four_MA_Strength Upper', 2: 'Four_MA_Strength Lower'}, 'levels': [], 'description': ['DX_Smoothed с фиксированным во входных параметрах таймфреймом'], 'name': 'Four_MA_Strength_HTF', 'source': 'MQL5 Indicators/Four_MA_Strength_HTF/Four_MA_Strength_HTF.mq5', 'folder': 'Four_MA_Strength_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'Ma1_Period', 'py': 'Ma1_Period', 'param': 'Ma1_Period', 'type': 'int', 'default': 8, 'label': 'Averaging period 1 for calculation.', 'sinput': False}, {'mql': 'Ma1_Method', 'py': 'Ma1_Method', 'param': 'Ma1_Method', 'type': 'int', 'default': 1, 'label': 'MA method 1. It can be any of the Moving Average method enumeration value.', 'sinput': False}, {'mql': 'Ma1_Price', 'py': 'Ma1_Price', 'param': 'Ma1_Price', 'type': 'int', 'default': 1, 'label': 'Applied price 1. It can be any of Applied price enumeration values.', 'sinput': False}, {'mql': 'Ma2_Period', 'py': 'Ma2_Period', 'param': 'Ma2_Period', 'type': 'int', 'default': 24, 'label': 'Averaging period 2 for calculation.', 'sinput': False}, {'mql': 'Ma2_Method', 'py': 'Ma2_Method', 'param': 'Ma2_Method', 'type': 'int', 'default': 1, 'label': 'MA metho 2. It can be any of the Moving Average method enumeration value.', 'sinput': False}, {'mql': 'Ma2_Price', 'py': 'Ma2_Price', 'param': 'Ma2_Price', 'type': 'int', 'default': 1, 'label': 'Applied price 2. It can be any of Applied price enumeration values.', 'sinput': False}, {'mql': 'Ma3_Period', 'py': 'Ma3_Period', 'param': 'Ma3_Period', 'type': 'int', 'default': 72, 'label': 'Averaging period 3 for calculation.', 'sinput': False}, {'mql': 'Ma3_Method', 'py': 'Ma3_Method', 'param': 'Ma3_Method', 'type': 'int', 'default': 1, 'label': 'MA method 3. It can be any of the Moving Average method enumeration value.', 'sinput': False}, {'mql': 'Ma3_Price', 'py': 'Ma3_Price', 'param': 'Ma3_Price', 'type': 'int', 'default': 1, 'label': 'Applied price 3. It can be any of Applied price enumeration values.', 'sinput': False}, {'mql': 'Ma4_Period', 'py': 'Ma4_Period', 'param': 'Ma4_Period', 'type': 'int', 'default': 216, 'label': 'Averaging period 4 for calculation.', 'sinput': False}, {'mql': 'Ma4_Method', 'py': 'Ma4_Method', 'param': 'Ma4_Method', 'type': 'int', 'default': 1, 'label': 'MA method 4. It can be any of the Moving Average method enumeration value.', 'sinput': False}, {'mql': 'Ma4_Price', 'py': 'Ma4_Price', 'param': 'Ma4_Price', 'type': 'int', 'default': 1, 'label': 'Applied price 4. It can be any of Applied price enumeration values.', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 3.501, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -3.501, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
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
Shift = _input('Shift', 0)  # Сдвиг
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('Four_MA_Strength', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Four_MA_Strength', Ma1_Period, Ma1_Method, Ma1_Price, Ma2_Period, Ma2_Method, Ma2_Price, Ma3_Period, Ma3_Method, Ma3_Price, Ma4_Period, Ma4_Method, Ma4_Price, HighLevel, LowLevel)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Four_MA_Strength')
        return INIT_FAILED
    IndInit(0, Ind1Buffer, EMPTY_VALUE, min_rates_total, Shift)
    IndInit(1, Ind2Buffer, EMPTY_VALUE, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Four_MA_Strength', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
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
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, Ind1Buffer, 1, Ind2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb1, IndBuf1, BuffNumb2, IndBuf2, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb1, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf1[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuffNumb2, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf2[bar] = Arr_[0]
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FourMAStrengthHTF(_MQL5Indicator):
    name = 'Four_MA_Strength_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
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
        'Shift': 0,  # Сдвиг
    }

