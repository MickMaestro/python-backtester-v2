"""CHOWithFlat — converted from MQL5: MQL5 Indicators/CHOWithFlat/CHOWithFlat.mq5

Money Flow Index With Flat
Copyright: Copyright © 2014, Powered byStep; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Powered byStep', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 7, 2: 1}, 'colors': {1: [16748574, 42495], 2: [9470064]}, 'widths': {2: 5}, 'styles': {2: 0}, 'labels': {1: 'CHO Oscillator', 2: 'Flat'}, 'levels': [0.0], 'description': ['Money Flow Index With Flat'], 'name': 'CHOWithFlat', 'source': 'MQL5 Indicators/CHOWithFlat/CHOWithFlat.mq5', 'folder': 'CHOWithFlat', 'inputs': [{'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 20, 'label': 'Период для расчета Боллинджера', 'sinput': False}, {'mql': 'StdDeviation', 'py': 'StdDeviation', 'param': 'StdDeviation', 'type': 'double', 'default': 2.0, 'label': 'Девиация Боллинджера', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены Боллинджера', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'uint', 'default': 3, 'label': 'период быстрого усреднения', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'uint', 'default': 10, 'label': 'метод медленного усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 13, 'label': 'Период усреднения сигнальной линии', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 0, 'label': 'Тип усреднения сигнальной линии', 'sinput': False}, {'mql': 'flat', 'py': 'flat', 'param': 'flat', 'type': 'uint', 'default': 100, 'label': 'величина флэта в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
BBPeriod = _input('BBPeriod', 20)  # Период для расчета Боллинджера
StdDeviation = _input('StdDeviation', 2.0)  # Девиация Боллинджера
applied_price = _input('applied_price', PRICE_CLOSE)  # Тип цены Боллинджера
XMA_Method = _input('XMA_Method', MODE_SMA)  # метод усреднения
FastPeriod = _input('FastPeriod', 3)  # период быстрого усреднения
SlowPeriod = _input('SlowPeriod', 10)  # метод медленного усреднения
XPhase = _input('XPhase', 15)  # параметр сглаживания,
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
MAPeriod = _input('MAPeriod', 13)  # Период усреднения сигнальной линии
MAType = _input('MAType', MODE_SMA)  # Тип усреднения сигнальной линии
flat = _input('flat', 100)  # величина флэта в пунктах
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
IndBuffer1 = Arr(0, 0.0)
BB_Handle = 0
CHO_Handle = 0
MA_Handle = 0
min_rates_total = 0

def OnInit():
    global BB_Handle, CHO_Handle, MA_Handle, min_rates_total
    min_rates_total = _int(MathMax(MathMax(BBPeriod, FastPeriod), SlowPeriod))
    BB_Handle = iBands(Symbol(), PERIOD_CURRENT, BBPeriod, 0, StdDeviation, applied_price)
    if BB_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBands')
        return INIT_FAILED
    CHO_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'CHO', XMA_Method, FastPeriod, SlowPeriod, XPhase, VolumeType)
    if CHO_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCHO')
        return INIT_FAILED
    MA_Handle = iMA(Symbol(), PERIOD_CURRENT, MAPeriod, 0, MAType, CHO_Handle)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    ArraySetAsSeries(SignalBuffer, True)
    SetIndexBuffer(2, IndBuffer1, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer1, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CHOWithFlat')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(BB_Handle) < rates_total or BarsCalculated(CHO_Handle) < rates_total) or BarsCalculated(MA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MainCHO = Arr(0, 0.0)
    SignCHO = Arr(0, 0.0)
    UpBB = Arr(0, 0.0)
    MainBB = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(BB_Handle, UPPER_BAND, 0, to_copy, UpBB) <= 0:
        return 0
    if CopyBuffer(BB_Handle, BASE_LINE, 0, to_copy, MainBB) <= 0:
        return 0
    if CopyBuffer(CHO_Handle, MAIN_LINE, 0, to_copy, MainCHO) <= 0:
        return 0
    if CopyBuffer(MA_Handle, MAIN_LINE, 0, to_copy, SignCHO) <= 0:
        return 0
    ArraySetAsSeries(UpBB, True)
    ArraySetAsSeries(MainBB, True)
    ArraySetAsSeries(MainCHO, True)
    ArraySetAsSeries(SignCHO, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        res = _fdiv(UpBB[bar] - MainBB[bar], Point())
        if res < flat:
            if MainCHO[bar] > SignCHO[bar]:
                IndBuffer[bar] = 1e-08
                SignalBuffer[bar] = 1e-08
                IndBuffer1[bar] = 0.0
            if MainCHO[bar] < SignCHO[bar]:
                IndBuffer[bar] = 1e-08
                SignalBuffer[bar] = 1e-08
                IndBuffer1[bar] = 0.0
        else:
            IndBuffer1[bar] = EMPTY_VALUE
            IndBuffer[bar] = MainCHO[bar]
            SignalBuffer[bar] = SignCHO[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CHOWithFlat(_MQL5Indicator):
    name = 'CHOWithFlat'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BBPeriod': 20,  # Период для расчета Боллинджера
        'StdDeviation': 2.0,  # Девиация Боллинджера
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены Боллинджера
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'FastPeriod': 3,  # период быстрого усреднения
        'SlowPeriod': 10,  # метод медленного усреднения
        'XPhase': 15,  # параметр сглаживания,
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'MAPeriod': 13,  # Период усреднения сигнальной линии
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Тип усреднения сигнальной линии
        'flat': 100,  # величина флэта в пунктах
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

