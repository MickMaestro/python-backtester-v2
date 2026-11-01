"""forexprofitboost_2nb_htf — converted from MQL5: MQL5 Indicators/ForexProfitBoost_2nb_HTF/forexprofitboost_2nb_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 4, 2: 4, 3: 4}, 'colors': {1: [42495], 2: [9639167], 3: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'ForexProfitBoost_2nb 1', 2: 'ForexProfitBoost_2nb 2', 3: 'ForexProfitBoost_2nb 3'}, 'levels': [], 'description': [], 'name': 'forexprofitboost_2nb_htf', 'source': 'MQL5 Indicators/ForexProfitBoost_2nb_HTF/forexprofitboost_2nb_htf.mq5', 'folder': 'ForexProfitBoost_2nb_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'MAPeriod1', 'py': 'MAPeriod1', 'param': 'MAPeriod1', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'MAType1', 'py': 'MAType1', 'param': 'MAType1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice1', 'py': 'MAPrice1', 'param': 'MAPrice1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPeriod2', 'py': 'MAPeriod2', 'param': 'MAPeriod2', 'type': 'uint', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'MAType2', 'py': 'MAType2', 'param': 'MAType2', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MAPrice2', 'py': 'MAPrice2', 'param': 'MAPrice2', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'BBDeviation', 'py': 'BBDeviation', 'param': 'BBDeviation', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'BBShift', 'py': 'BBShift', 'param': 'BBShift', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
MAPeriod1 = _input('MAPeriod1', 7)
MAType1 = _input('MAType1', MODE_EMA)
MAPrice1 = _input('MAPrice1', PRICE_CLOSE)
MAPeriod2 = _input('MAPeriod2', 21)
MAType2 = _input('MAType2', MODE_SMA)
MAPrice2 = _input('MAPrice2', PRICE_CLOSE)
BBPeriod = _input('BBPeriod', 15)
BBDeviation = _input('BBDeviation', 1.0)
BBShift = _input('BBShift', 1)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Up1IndBuffer = Arr(0, 0.0)
Dn1IndBuffer = Arr(0, 0.0)
Up2IndBuffer = Arr(0, 0.0)
Dn2IndBuffer = Arr(0, 0.0)
Up3IndBuffer = Arr(0, 0.0)
Dn3IndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('ForexProfitBoost_2nb', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'ForexProfitBoost_2nb', MAPeriod1, MAType1, MAPrice1, MAPeriod2, MAType2, MAPrice2, BBPeriod, BBDeviation, BBShift)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ForexProfitBoost_2nb')
        return INIT_FAILED
    IndInit(0, Up1IndBuffer, INDICATOR_DATA)
    IndInit(1, Dn1IndBuffer, INDICATOR_DATA)
    IndInit(2, Up2IndBuffer, INDICATOR_DATA)
    IndInit(3, Dn2IndBuffer, INDICATOR_DATA)
    IndInit(4, Up3IndBuffer, INDICATOR_DATA)
    IndInit(5, Dn3IndBuffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    PlotInit(1, EMPTY_VALUE, 0, Shift)
    PlotInit(2, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'ForexProfitBoost_2nb', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, Up1IndBuffer, 1, Dn1IndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 2, Up2IndBuffer, 3, Dn2IndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 4, Up3IndBuffer, 5, Dn3IndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, UpBuffNumb, UpIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
            UpArr = Arr(1, 0.0, dyn=False)
            DnArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, UpBuffNumb, _DT(iTime_[bar]), 1, UpArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, DnBuffNumb, _DT(iTime_[bar]), 1, DnArr) <= 0:
                return (0 != 0)
            UpIndBuf[bar] = UpArr[0]
            DnIndBuf[bar] = DnArr[0]
        else:
            UpIndBuf[bar] = UpIndBuf[bar + 1]
            DnIndBuf[bar] = DnIndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(3, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Forexprofitboost2nbHtf(_MQL5Indicator):
    name = 'forexprofitboost_2nb_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'MAPeriod1': 7,
        'MAType1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'MAPeriod2': 21,
        'MAType2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'MAPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'BBPeriod': 15,
        'BBDeviation': 1.0,
        'BBShift': 1,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

