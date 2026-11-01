"""binarywave_htf — converted from MQL5: MQL5 Indicators/BinaryWave_HTF/binarywave_htf.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [0.0], 'description': [], 'name': 'binarywave_htf', 'source': 'MQL5 Indicators/BinaryWave_HTF/binarywave_htf.mq5', 'folder': 'BinaryWave_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'WeightMA', 'py': 'WeightMA', 'param': 'WeightMA', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightMACD', 'py': 'WeightMACD', 'param': 'WeightMACD', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightOsMA', 'py': 'WeightOsMA', 'param': 'WeightOsMA', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightCCI', 'py': 'WeightCCI', 'param': 'WeightCCI', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightMOM', 'py': 'WeightMOM', 'param': 'WeightMOM', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightRSI', 'py': 'WeightRSI', 'param': 'WeightRSI', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightADX', 'py': 'WeightADX', 'param': 'WeightADX', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastMACD', 'py': 'FastMACD', 'param': 'FastMACD', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowMACD', 'py': 'SlowMACD', 'param': 'SlowMACD', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalMACD', 'py': 'SignalMACD', 'param': 'SignalMACD', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'PriceMACD', 'py': 'PriceMACD', 'param': 'PriceMACD', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalPeriod', 'py': 'SignalPeriod', 'param': 'SignalPeriod', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'OsMAPrice', 'py': 'OsMAPrice', 'param': 'OsMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'MOMPeriod', 'py': 'MOMPeriod', 'param': 'MOMPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MOMPrice', 'py': 'MOMPrice', 'param': 'MOMPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'bMA_Method', 'py': 'bMA_Method', 'param': 'bMA_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'bLength', 'py': 'bLength', 'param': 'bLength', 'type': 'int', 'default': 5, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'bPhase', 'py': 'bPhase', 'param': 'bPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_JJMA = 4
MODE_JurX = 5
MODE_ParMA = 6
MODE_T3 = 7
MODE_VIDYA = 8
MODE_AMA = 9
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_JJMA', 5: 'MODE_JurX', 6: 'MODE_ParMA', 7: 'MODE_T3', 8: 'MODE_VIDYA', 9: 'MODE_AMA'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
WeightMA = _input('WeightMA', 1.0)
WeightMACD = _input('WeightMACD', 1.0)
WeightOsMA = _input('WeightOsMA', 1.0)
WeightCCI = _input('WeightCCI', 1.0)
WeightMOM = _input('WeightMOM', 1.0)
WeightRSI = _input('WeightRSI', 1.0)
WeightADX = _input('WeightADX', 1.0)
MAPeriod = _input('MAPeriod', 13)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
FastMACD = _input('FastMACD', 12)
SlowMACD = _input('SlowMACD', 26)
SignalMACD = _input('SignalMACD', 9)
PriceMACD = _input('PriceMACD', PRICE_CLOSE)
FastPeriod = _input('FastPeriod', 12)
SlowPeriod = _input('SlowPeriod', 26)
SignalPeriod = _input('SignalPeriod', 9)
OsMAPrice = _input('OsMAPrice', PRICE_CLOSE)
CCIPeriod = _input('CCIPeriod', 14)
CCIPrice = _input('CCIPrice', PRICE_MEDIAN)
MOMPeriod = _input('MOMPeriod', 14)
MOMPrice = _input('MOMPrice', PRICE_CLOSE)
RSIPeriod = _input('RSIPeriod', 14)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
ADXPeriod = _input('ADXPeriod', 14)
bMA_Method = _input('bMA_Method', MODE_JJMA)  # Метод усреднения
bLength = _input('bLength', 5)  # Глубина сглаживания
bPhase = _input('bPhase', 100)  # Параметр сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора BinaryWave не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'BinaryWave' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol_, TimeFrame, 'BinaryWave', WeightMA, WeightMACD, WeightOsMA, WeightCCI, WeightMOM, WeightRSI, WeightADX, MAPeriod, MAType, MAPrice, FastMACD, SlowMACD, SignalMACD, PriceMACD, FastPeriod, SlowPeriod, SignalPeriod, OsMAPrice, CCIPeriod, CCIPrice, MOMPeriod, MOMPrice, RSIPeriod, RSIPrice, ADXPeriod, bMA_Method, bLength, bPhase, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора BinaryWave')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'BinaryWave(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer, time, rates_total, prev_calculated, min_rates_total):
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
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BinarywaveHtf(_MQL5Indicator):
    name = 'binarywave_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'WeightMA': 1.0,
        'WeightMACD': 1.0,
        'WeightOsMA': 1.0,
        'WeightCCI': 1.0,
        'WeightMOM': 1.0,
        'WeightRSI': 1.0,
        'WeightADX': 1.0,
        'MAPeriod': 13,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'FastMACD': 12,
        'SlowMACD': 26,
        'SignalMACD': 9,
        'PriceMACD': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'FastPeriod': 12,
        'SlowPeriod': 26,
        'SignalPeriod': 9,
        'OsMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'CCIPeriod': 14,
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),
        'MOMPeriod': 14,
        'MOMPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSIPeriod': 14,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'ADXPeriod': 14,
        'bMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'bLength': 5,  # Глубина сглаживания
        'bPhase': 100,  # Параметр сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

