"""colorrmacd — converted from MQL5: MQL5 Indicators/ColorRMACD_HTF/colorrmacd.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [8421504, 8421376, 14822282, 6053069, 16711935], 2: [8421504, 65280, 255]}, 'widths': {1: 2, 2: 3}, 'styles': {1: 0, 2: 4}, 'labels': {1: 'RMACD', 2: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'colorrmacd', 'source': 'MQL5 Indicators/ColorRMACD_HTF/colorrmacd.mq5', 'folder': 'ColorRMACD_HTF', 'inputs': [{'mql': 'Fast_RVI', 'py': 'Fast_RVI', 'param': 'Fast_RVI', 'type': 'uint', 'default': 12, 'label': 'Период быстрой средней', 'sinput': False}, {'mql': 'Slow_TRVI', 'py': 'Slow_TRVI', 'param': 'Slow_TRVI', 'type': 'uint', 'default': 26, 'label': 'Период медленной средней', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объем', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'uint', 'default': 9, 'label': 'Период сигнальной линии', 'sinput': False}, {'mql': 'Signal_Phase', 'py': 'Signal_Phase', 'param': 'Signal_Phase', 'type': 'int', 'default': 100, 'label': 'Параметр сигнальной линии', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Количество подаваемых алертов', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Fast_RVI = _input('Fast_RVI', 12)  # Период быстрой средней
Slow_TRVI = _input('Slow_TRVI', 26)  # Период медленной средней
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объем
Signal_Method = _input('Signal_Method', MODE_JJMA)  # Метод усреднения сигнальной линии
Signal_XMA = _input('Signal_XMA', 9)  # Период сигнальной линии
Signal_Phase = _input('Signal_Phase', 100)  # Параметр сигнальной линии
AlertCount = _input('AlertCount', 0)  # Количество подаваемых алертов
RVI_Handle = 0
TRVI_Handle = 0
min_rates_total = 0
min_rates = 0
RMACDBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
ColorRMACDBuffer = Arr(0, 0.0)
ColorSignBuffer = Arr(0, 0.0)

def OnInit():
    global RVI_Handle, TRVI_Handle, min_rates, min_rates_total
    min_rates = _int(MathMax(Fast_RVI, Slow_TRVI + 8))
    min_rates_total = min_rates + XMA1.GetStartBars(Signal_Method, Signal_XMA, Signal_Phase)
    RVI_Handle = iRVI(None, 0, Fast_RVI)
    if RVI_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора RVI')
    TRVI_Handle = iCustom(None, 0, 'TRVI', Slow_TRVI, VolumeType, 0)
    if TRVI_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора TRVI')
    SetIndexBuffer(0, RMACDBuffer, INDICATOR_DATA)
    ArraySetAsSeries(RMACDBuffer, True)
    SetIndexBuffer(1, ColorRMACDBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorRMACDBuffer, True)
    SetIndexBuffer(2, SignBuffer, INDICATOR_DATA)
    ArraySetAsSeries(SignBuffer, True)
    SetIndexBuffer(3, ColorSignBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorSignBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    XMA1.XMALengthCheck('Fast_RVI', Fast_RVI)
    XMA1.XMALengthCheck('Slow_TRVI', Slow_TRVI)
    XMA1.XMALengthCheck('Signal_XMA', Signal_XMA)
    XMA1.XMAPhaseCheck('Signal_Phase', Signal_Phase, Signal_Method)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(Signal_Method)
    StringConcatenate(shortname, 'RMACD( ', Fast_RVI, ', ', Slow_TRVI, ', ', Smooth, ', ', Signal_XMA, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DnCount, _s_OnCalculate_UpCount
    if (BarsCalculated(RVI_Handle) < rates_total or BarsCalculated(TRVI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    RVI = Arr(0, 0.0)
    TRVI = Arr(0, 0.0)
    rmacd = 0.0
    sign_xma = 0.0
    maxbar = rates_total - 1 - min_rates
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RVI_Handle, MAIN_LINE, 0, to_copy, RVI) <= 0:
        return 0
    if CopyBuffer(TRVI_Handle, SIGNAL_LINE, 0, to_copy, TRVI) <= 0:
        return 0
    ArraySetAsSeries(RVI, True)
    ArraySetAsSeries(TRVI, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        rmacd = RVI[bar] - TRVI[bar]
        sign_xma = XMA1.XMASeries(maxbar, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, rmacd, bar, True)
        RMACDBuffer[bar] = rmacd
        SignBuffer[bar] = sign_xma
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorRMACDBuffer[bar] = 0.0
        if RMACDBuffer[bar] > 0:
            if RMACDBuffer[bar] > RMACDBuffer[bar + 1]:
                ColorRMACDBuffer[bar] = 1.0
            if RMACDBuffer[bar] < RMACDBuffer[bar + 1]:
                ColorRMACDBuffer[bar] = 2.0
        if RMACDBuffer[bar] < 0:
            if RMACDBuffer[bar] < RMACDBuffer[bar + 1]:
                ColorRMACDBuffer[bar] = 3.0
            if RMACDBuffer[bar] > RMACDBuffer[bar + 1]:
                ColorRMACDBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorSignBuffer[bar] = 0.0
        if RMACDBuffer[bar] > SignBuffer[bar + 1]:
            ColorSignBuffer[bar] = 1.0
        if RMACDBuffer[bar] < SignBuffer[bar + 1]:
            ColorSignBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if rates_total != prev_calculated:
        _s_OnCalculate_UpCount = 0
        _s_OnCalculate_DnCount = 0
    bar1 = 1
    bar2 = 2
    if (_s_OnCalculate_UpCount < AlertCount and ColorSignBuffer[bar1] == 2) and ColorSignBuffer[bar2] == 1:
        _s_OnCalculate_UpCount += 1
        Alert('RMACD индикатор ' + Symbol() + EnumToString(PERIOD_CURRENT, 'ENUM_TIMEFRAMES') + ': Сигнал на покупку ' + Symbol())
    if (_s_OnCalculate_DnCount < AlertCount and ColorSignBuffer[bar1] == 1) and ColorSignBuffer[bar2] == 2:
        _s_OnCalculate_DnCount += 1
        Alert('RMACD индикатор ' + Symbol() + EnumToString(PERIOD_CURRENT, 'ENUM_TIMEFRAMES') + ': Сигнал на продажу ' + Symbol())
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_OnCalculate_UpCount = 0
_s_OnCalculate_DnCount = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorrmacd(_MQL5Indicator):
    name = 'colorrmacd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast_RVI': 12,  # Период быстрой средней
        'Slow_TRVI': 26,  # Период медленной средней
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объем
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения сигнальной линии
        'Signal_XMA': 9,  # Период сигнальной линии
        'Signal_Phase': 100,  # Параметр сигнальной линии
        'AlertCount': 0,  # Количество подаваемых алертов
    }

