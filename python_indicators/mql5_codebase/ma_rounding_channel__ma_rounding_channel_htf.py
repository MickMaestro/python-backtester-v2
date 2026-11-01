"""ma_rounding_channel — converted from MQL5: MQL5 Indicators/MA_Rounding_Channel_HTF/ma_rounding_channel.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [13828244], 2: [16748574], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 3: 0}, 'labels': {1: 'MA Rounding', 2: 'Up MA Rounding', 3: 'Down MA Rounding'}, 'levels': [], 'description': [], 'name': 'ma_rounding_channel', 'source': 'MQL5 Indicators/MA_Rounding_Channel_HTF/ma_rounding_channel.mq5', 'folder': 'MA_Rounding_Channel_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'MaRound', 'py': 'MaRound', 'param': 'MaRound', 'type': 'uint', 'default': 50, 'label': 'Коэффициент округления', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 12, 'label': 'Период ATR для ширины канала', 'sinput': False}, {'mql': 'ATR_Factor', 'py': 'ATR_Factor', 'param': 'ATR_Factor', 'type': 'double', 'default': 1.0, 'label': 'Коэффициент девиации канала', 'sinput': False}, {'mql': 'ChanContinuity', 'py': 'ChanContinuity', 'param': 'ChanContinuity', 'type': 'bool', 'default': False, 'label': 'Непрерывность канала', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XLength = _input('XLength', 12)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
MaRound = _input('MaRound', 50)  # Коэффициент округления
ATRPeriod = _input('ATRPeriod', 12)  # Период ATR для ширины канала
ATR_Factor = _input('ATR_Factor', 1.0)  # Коэффициент девиации канала
ChanContinuity = _input('ChanContinuity', False)  # Непрерывность канала
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
MaRo = 0.0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, MaRo, min_rates_total
    min_rates_total = XMA1.GetStartBars(XMA_Method, XLength, XPhase) + 2
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    MaRo = Point() * MaRound
    ATR_Handle = iATR(None, PERIOD_CURRENT, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_ARROW, 167)
    SetIndexBuffer(2, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_ARROW, 167)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'MA Rounding(', XLength, ', ', MaRound, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_MovAle1, _s_OnCalculate_MovAve1, _s_OnCalculate_range1
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    price_ = 0.0
    MovAve0 = 0.0
    MovAle0 = 0.0
    res0 = 0.0
    res1 = 0.0
    Range = Arr(0, 0.0)
    range0 = 0.0
    to_copy = 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 2
        _s_OnCalculate_MovAve1 = PriceSeries(IPC, first, open, low, high, close)
        _s_OnCalculate_MovAle1 = 0.0
        _s_OnCalculate_range1 = 0.0
    else:
        first = prev_calculated - 1
    range0 = _s_OnCalculate_range1
    to_copy = rates_total - first
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, Range) <= 0:
        return 0
    ArraySetAsSeries(Range, True)
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        MovAve0 = XMA1.XMASeries(2, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price_, bar, False)
        res1 = IndBuffer[bar - 1]
        if ((((MovAve0 > (_s_OnCalculate_MovAve1 + MaRo) or MovAve0 < (_s_OnCalculate_MovAve1 - MaRo)) or MovAve0 > (res1 + MaRo)) or MovAve0 < (res1 - MaRo)) or (MovAve0 > res1 and _s_OnCalculate_MovAle1 == 1)) or (MovAve0 < res1 and _s_OnCalculate_MovAle1 == -1):
            IndBuffer[bar] = MovAve0
        else:
            IndBuffer[bar] = res1
        MovAle0 = 0.0
        res0 = IndBuffer[bar]
        if res0 < res1:
            MovAle0 = -1.0
        if res0 > res1:
            MovAle0 = 1.0
        if res0 == res1:
            MovAle0 = _s_OnCalculate_MovAle1
        UpBuffer[bar] = 0.0
        DnBuffer[bar] = 0.0
        if res0 == res1:
            if res1 != IndBuffer[bar - 2]:
                range0 = Range[rates_total - bar - 1] * ATR_Factor
            else:
                range0 = _s_OnCalculate_range1
            UpBuffer[bar] = res0 + range0
            DnBuffer[bar] = res0 - range0
        elif ChanContinuity:
            UpBuffer[bar] = UpBuffer[bar - 1]
            DnBuffer[bar] = DnBuffer[bar - 1]
        if bar < (rates_total - 1):
            _s_OnCalculate_MovAle1 = MovAle0
            _s_OnCalculate_MovAve1 = MovAve0
            _s_OnCalculate_range1 = range0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_OnCalculate_MovAle1 = 0.0
_s_OnCalculate_MovAve1 = 0.0
_s_OnCalculate_range1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaRoundingChannel(_MQL5Indicator):
    name = 'ma_rounding_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 12,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simplе Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'MaRound': 50,  # Коэффициент округления
        'ATRPeriod': 12,  # Период ATR для ширины канала
        'ATR_Factor': 1.0,  # Коэффициент девиации канала
        'ChanContinuity': False,  # Непрерывность канала
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

