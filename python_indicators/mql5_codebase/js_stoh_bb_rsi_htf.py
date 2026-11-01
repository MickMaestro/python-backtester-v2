"""js-stoh-bb-rsi_htf — converted from MQL5: MQL5 Indicators/JS-Stoh-BB-RSI_HTF/js-stoh-bb-rsi_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16711680], 2: [8421376], 3: [14822282], 4: [255], 5: [255]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Stochastic', 2: 'RSI', 3: 'Stochastic Signal', 4: '+2Sigma Stochastic', 5: '-2Sigma Stochastic'}, 'levels': [80.0, 70.0, 50.0, 30.0, 20.0], 'description': [], 'name': 'js-stoh-bb-rsi_htf', 'source': 'MQL5 Indicators/JS-Stoh-BB-RSI_HTF/js-stoh-bb-rsi_htf.mq5', 'folder': 'JS-Stoh-BB-RSI_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'STO_KPeriod', 'py': 'STO_KPeriod', 'param': 'STO_KPeriod', 'type': 'uint', 'default': 5, 'label': 'K period стохастика', 'sinput': False}, {'mql': 'STO_DPeriod', 'py': 'STO_DPeriod', 'param': 'STO_DPeriod', 'type': 'uint', 'default': 3, 'label': 'D period стохастика', 'sinput': False}, {'mql': 'STO_Slowing', 'py': 'STO_Slowing', 'param': 'STO_Slowing', 'type': 'uint', 'default': 3, 'label': 'Slowing стохастика', 'sinput': False}, {'mql': 'STO_Method', 'py': 'STO_Method', 'param': 'STO_Method', 'type': 'int', 'default': 0, 'label': 'Тип сглаживания стохастика', 'sinput': False}, {'mql': 'STO_Price', 'py': 'STO_Price', 'param': 'STO_Price', 'type': 'int', 'default': 0, 'label': 'Способ расчета стохастика', 'sinput': False}, {'mql': 'BandsPeriod', 'py': 'BandsPeriod', 'param': 'BandsPeriod', 'type': 'uint', 'default': 10, 'label': 'Период усреднения BB', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'Девиация', 'sinput': False}, {'mql': 'RSI_Period', 'py': 'RSI_Period', 'param': 'RSI_Period', 'type': 'uint', 'default': 8, 'label': 'Период индикатора RSI', 'sinput': False}, {'mql': 'RSI_Price', 'py': 'RSI_Price', 'param': 'RSI_Price', 'type': 'int', 'default': 1, 'label': 'Тип цены для индикатора RSI', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
STO_KPeriod = _input('STO_KPeriod', 5)  # K period стохастика
STO_DPeriod = _input('STO_DPeriod', 3)  # D period стохастика
STO_Slowing = _input('STO_Slowing', 3)  # Slowing стохастика
STO_Method = _input('STO_Method', MODE_SMA)  # Тип сглаживания стохастика
STO_Price = _input('STO_Price', STO_LOWHIGH)  # Способ расчета стохастика
BandsPeriod = _input('BandsPeriod', 10)  # Период усреднения BB
BandsDeviation = _input('BandsDeviation', 1.0)  # Девиация
RSI_Period = _input('RSI_Period', 8)  # Период индикатора RSI
RSI_Price = _input('RSI_Price', PRICE_CLOSE)  # Тип цены для индикатора RSI
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
IndBuffer4 = Arr(0, 0.0)
IndBuffer5 = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора JS-Stoh-BB-RSI не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'JS-Stoh-BB-RSI_HTF' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol_, TimeFrame, 'JS-Stoh-BB-RSI', STO_KPeriod, STO_DPeriod, STO_Slowing, STO_Method, STO_Price, BandsPeriod, BandsDeviation, RSI_Period, RSI_Price, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора JS-Stoh-BB-RSI')
        return INIT_FAILED
    IndInit(0, IndBuffer1, INDICATOR_DATA)
    IndInit(1, IndBuffer2, INDICATOR_DATA)
    IndInit(2, IndBuffer3, INDICATOR_DATA)
    IndInit(3, IndBuffer4, INDICATOR_DATA)
    IndInit(4, IndBuffer5, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    PlotInit(1, EMPTY_VALUE, 0, Shift)
    PlotInit(2, EMPTY_VALUE, 0, Shift)
    PlotInit(3, EMPTY_VALUE, 0, Shift)
    PlotInit(4, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'JS-Stoh-BB-RSI_HTF(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer1, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 1, IndBuffer2, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 2, IndBuffer3, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 3, IndBuffer4, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 4, IndBuffer5, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(5, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JsStohBbRsiHtf(_MQL5Indicator):
    name = 'js-stoh-bb-rsi_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'STO_KPeriod': 5,  # K period стохастика
        'STO_DPeriod': 3,  # D period стохастика
        'STO_Slowing': 3,  # Slowing стохастика
        'STO_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Тип сглаживания стохастика
        'STO_Price': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Способ расчета стохастика
        'BandsPeriod': 10,  # Период усреднения BB
        'BandsDeviation': 1.0,  # Девиация
        'RSI_Period': 8,  # Период индикатора RSI
        'RSI_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены для индикатора RSI
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

