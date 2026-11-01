"""KWAN_RDP — converted from MQL5: MQL5 Indicators/KWAN_RDP_HTF/KWAN_RDP.mq5

Metatrader4 Code by jjk2. Based on MBA Thesis from Simon Fraser University written by C.E. ALDEA.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': 0.0}, 'types': {1: 10}, 'colors': {1: [16776960, 8421504, 9639167]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'KWAN_RDP'}, 'levels': [], 'description': ['Metatrader4 Code by jjk2. Based on MBA Thesis from Simon Fraser University written by C.E. ALDEA.'], 'name': 'KWAN_RDP', 'source': 'MQL5 Indicators/KWAN_RDP_HTF/KWAN_RDP.mq5', 'folder': 'KWAN_RDP_HTF', 'inputs': [{'mql': 'DeMarker_Period', 'py': 'DeMarker_Period', 'param': 'DeMarker_Period', 'type': 'uint', 'default': 14, 'label': 'период DeMarker', 'sinput': False}, {'mql': 'MFIPeriod', 'py': 'MFIPeriod', 'param': 'MFIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора MFI', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'MomentumPeriod', 'py': 'MomentumPeriod', 'param': 'MomentumPeriod', 'type': 'uint', 'default': 14, 'label': 'Период индикатора Momentum', 'sinput': False}, {'mql': 'MomentumPrice', 'py': 'MomentumPrice', 'param': 'MomentumPrice', 'type': 'int', 'default': 1, 'label': 'Цена индикатора Momentum', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 7, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
DeMarker_Period = _input('DeMarker_Period', 14)  # период DeMarker
MFIPeriod = _input('MFIPeriod', 14)  # период индикатора MFI
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
MomentumPeriod = _input('MomentumPeriod', 14)  # Период индикатора Momentum
MomentumPrice = _input('MomentumPrice', PRICE_CLOSE)  # Цена индикатора Momentum
XMA_Method = _input('XMA_Method', MODE_JJMA)  # метод усреднения
XLength = _input('XLength', 7)  # глубина сглаживания
XPhase = _input('XPhase', 100)  # параметр сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0
DeMarker_Handle = 0
MFI_Handle = 0
Mom_Handle = 0

def OnInit():
    global DeMarker_Handle, MFI_Handle, Mom_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(DeMarker_Period + 1)
    min_rates_1 = _int(MathMax(min_rates_1, MathMax(MFIPeriod, MomentumPeriod)))
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method, XLength, XPhase)
    DeMarker_Handle = iDeMarker(None, 0, DeMarker_Period)
    if DeMarker_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iDeMarkerastic')
        return INIT_FAILED
    MFI_Handle = iMFI(None, 0, MFIPeriod, VolumeType)
    if MFI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMFI')
        return INIT_FAILED
    Mom_Handle = iMomentum(Symbol(), PERIOD_CURRENT, MomentumPeriod, MomentumPrice)
    if Mom_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMomentum')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ColorIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KWAN_RDP')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(DeMarker_Handle) < rates_total or BarsCalculated(MFI_Handle) < rates_total) or BarsCalculated(Mom_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    maxbar = 0
    DeMarker = Arr(0, 0.0)
    MFI = Arr(0, 0.0)
    Mom = Arr(0, 0.0)
    kwan = 0.0
    maxbar = rates_total - min_rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(DeMarker, True)
    ArraySetAsSeries(MFI, True)
    ArraySetAsSeries(Mom, True)
    if CopyBuffer(DeMarker_Handle, 0, 0, to_copy, DeMarker) <= 0:
        return 0
    if CopyBuffer(MFI_Handle, 0, 0, to_copy, MFI) <= 0:
        return 0
    if CopyBuffer(Mom_Handle, 0, 0, to_copy, Mom) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if Mom[bar]:
            kwan = _fdiv(100 * DeMarker[bar] * MFI[bar], Mom[bar])
        else:
            kwan = 100.0
        IndBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, kwan, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if not prev_calculated:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorIndBuffer[bar] = 1.0
        if IndBuffer[bar] > IndBuffer[bar + 1]:
            ColorIndBuffer[bar] = 0.0
        if IndBuffer[bar] < IndBuffer[bar + 1]:
            ColorIndBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KWANRDP(_MQL5Indicator):
    name = 'KWAN_RDP'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DeMarker_Period': 14,  # период DeMarker
        'MFIPeriod': 14,  # период индикатора MFI
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'MomentumPeriod': 14,  # Период индикатора Momentum
        'MomentumPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена индикатора Momentum
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'XLength': 7,  # глубина сглаживания
        'XPhase': 100,  # параметр сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

