"""kaufwmacross_htf — converted from MQL5: MQL5 Indicators/KaufWMAcross_HTF/kaufwmacross_htf.mq5

Индикатор KaufWMAcross с возможностью изменения таймфрема во входных параметрах
Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [7504122], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'KaufWMAcross Sell', 2: 'KaufWMAcross Buy'}, 'levels': [], 'description': ['Индикатор KaufWMAcross с возможностью изменения таймфрема во входных параметрах'], 'name': 'kaufwmacross_htf', 'source': 'MQL5 Indicators/KaufWMAcross_HTF/kaufwmacross_htf.mq5', 'folder': 'KaufWMAcross_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'ama_period', 'py': 'ama_period', 'param': 'ama_period', 'type': 'uint', 'default': 9, 'label': 'Период AMA', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'uint', 'default': 2, 'label': 'Период быстрой скользящей', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'uint', 'default': 30, 'label': 'Период медленной скользящей', 'sinput': False}, {'mql': 'AMAPrice', 'py': 'AMAPrice', 'param': 'AMAPrice', 'type': 'int', 'default': 1, 'label': 'Цена AMA', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 13, 'label': 'Период MA', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 3, 'label': 'Метод усреднения MA', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'Цена MA', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'SellSymb', 'py': 'SellSymb', 'param': 'SellSymb', 'type': 'uint', 'default': 234, 'label': 'Значок продажи', 'sinput': False}, {'mql': 'BuySymb', 'py': 'BuySymb', 'param': 'BuySymb', 'type': 'uint', 'default': 233, 'label': 'Значок покупки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
ama_period = _input('ama_period', 9)  # Период AMA
fast_ma_period = _input('fast_ma_period', 2)  # Период быстрой скользящей
slow_ma_period = _input('slow_ma_period', 30)  # Период медленной скользящей
AMAPrice = _input('AMAPrice', PRICE_CLOSE)  # Цена AMA
MAPeriod = _input('MAPeriod', 13)  # Период MA
MAType = _input('MAType', MODE_LWMA)  # Метод усреднения MA
MAPrice = _input('MAPrice', PRICE_CLOSE)  # Цена MA
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellSymb = _input('SellSymb', 234)  # Значок продажи
BuySymb = _input('BuySymb', 233)  # Значок покупки
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('KaufWMAcross', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'KaufWMAcross', ama_period, fast_ma_period, slow_ma_period, AMAPrice, MAPeriod, MAType, MAPrice)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора KaufWMAcross')
        return INIT_FAILED
    IndInit(0, DnBuffer, 0.0, min_rates_total, Shift, SellSymb)
    IndInit(1, UpBuffer, 0.0, min_rates_total, Shift, BuySymb)
    shortname = Box("")
    StringConcatenate(shortname, 'KaufWMAcross', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, DnBuffer, 1, UpBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift, Symb):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_ARROW, Symb)
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
        IndBuf1[bar] = 0.0
        IndBuf2[bar] = 0.0
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr1 = Arr(1, 0.0, dyn=False)
            Arr2 = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb1, _DT(iTime_[bar]), 1, Arr1) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb2, _DT(iTime_[bar]), 1, Arr2) <= 0:
                return (0 != 0)
            IndBuf1[bar] = Arr1[0]
            IndBuf2[bar] = Arr2[0]
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


class KaufwmacrossHtf(_MQL5Indicator):
    name = 'kaufwmacross_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'ama_period': 9,  # Период AMA
        'fast_ma_period': 2,  # Период быстрой скользящей
        'slow_ma_period': 30,  # Период медленной скользящей
        'AMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена AMA
        'MAPeriod': 13,  # Период MA
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Метод усреднения MA
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена MA
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'SellSymb': 234,  # Значок продажи
        'BuySymb': 233,  # Значок покупки
    }

