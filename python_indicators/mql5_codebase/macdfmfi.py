"""MACDfMFI — converted from MQL5: MQL5 Indicators/MACD_MFI/MACDfMFI.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 3, 2: 1, 3: 8}, 'colors': {1: [8421504], 2: [255], 3: [8421504, 16748574, 16711935]}, 'widths': {1: 2, 2: 1, 3: 3}, 'styles': {1: 0, 2: 4, 3: 0}, 'labels': {1: 'MACD', 2: 'Signal Line', 3: 'MFI'}, 'levels': [], 'description': [], 'name': 'MACDfMFI', 'source': 'MQL5 Indicators/MACD_MFI/MACDfMFI.mq5', 'folder': 'MACD_MFI', 'inputs': [{'mql': 'Fast_MA', 'py': 'Fast_MA', 'param': 'Fast_MA', 'type': 'int', 'default': 12, 'label': 'период быстрого мувинга MACD', 'sinput': False}, {'mql': 'Slow_MA', 'py': 'Slow_MA', 'param': 'Slow_MA', 'type': 'int', 'default': 26, 'label': 'глубина  медленного мувинга MACD', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 1, 'label': 'метод усреднения индикатора', 'sinput': False}, {'mql': 'Signal_SMA', 'py': 'Signal_SMA', 'param': 'Signal_SMA', 'type': 'int', 'default': 9, 'label': 'период сигнальной линии', 'sinput': False}, {'mql': 'AppliedPrice_', 'py': 'AppliedPrice_', 'param': 'AppliedPrice_', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'MFIPeriod', 'py': 'MFIPeriod', 'param': 'MFIPeriod', 'type': 'uint', 'default': 12, 'label': 'период MFI', 'sinput': False}, {'mql': 'MFIVolumeType', 'py': 'MFIVolumeType', 'param': 'MFIVolumeType', 'type': 'int', 'default': 0, 'label': 'объём MFI', 'sinput': False}, {'mql': 'caliber', 'py': 'caliber', 'param': 'caliber', 'type': 'double', 'default': 4.0, 'label': 'масштабирование', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_APPLIED_PRICE_
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
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
Fast_MA = _input('Fast_MA', 12)  # период быстрого мувинга MACD
Slow_MA = _input('Slow_MA', 26)  # глубина  медленного мувинга MACD
MA_Method_ = _input('MA_Method_', MODE_EMA)  # метод усреднения индикатора
Signal_SMA = _input('Signal_SMA', 9)  # период сигнальной линии
AppliedPrice_ = _input('AppliedPrice_', PRICE_CLOSE_)  # ценовая константа
MFIPeriod = _input('MFIPeriod', 12)  # период MFI
MFIVolumeType = _input('MFIVolumeType', VOLUME_TICK)  # объём MFI
caliber = _input('caliber', 4.0)  # масштабирование
MACDBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
MFIBuffer = Arr(0, 0.0)
ColorMFIBuffer = Arr(0, 0.0)
positive_ = 0.0
negative_ = 0.0
macd_start = 0
sig_start = 0
mfi_start = 0

def OnInit():
    global macd_start, mfi_start, sig_start
    if MA_Method_ != MODE_EMA:
        macd_start = MathMax(Fast_MA, Slow_MA)
    else:
        macd_start = 0
    sig_start = macd_start + Signal_SMA
    mfi_start = sig_start + _int(MFIPeriod) + 2
    SetIndexBuffer(0, MACDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, macd_start)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, sig_start)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    SetIndexBuffer(2, MFIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, mfi_start + 1)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    SetIndexBuffer(3, ColorMFIBuffer, INDICATOR_COLOR_INDEX)
    shortname = Box("")
    StringConcatenate(shortname, 'MACD_MFI(', Fast_MA, ',', Slow_MA, ',', Signal_SMA, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global negative_, positive_
    if rates_total < mfi_start:
        return 0
    first = 0
    bar = 0
    price_ = 0.0
    fast_ma = 0.0
    slow_ma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        negative_ = 0.0
        positive_ = negative_
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(AppliedPrice_, bar, open, low, high, close)
        fast_ma = _s_OnCalculate_MA1.MASeries(0, prev_calculated, rates_total, Fast_MA, MA_Method_, price_, bar, False)
        slow_ma = _s_OnCalculate_MA2.MASeries(0, prev_calculated, rates_total, Slow_MA, MA_Method_, price_, bar, False)
        MACDBuffer[bar] = fast_ma - slow_ma
        SignBuffer[bar] = _s_OnCalculate_MA3.SMASeries(macd_start, prev_calculated, rates_total, Signal_SMA, MACDBuffer[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = mfi_start + 1
    bar = first
    for bar in range(bar, rates_total):
        if MFIVolumeType == VOLUME_TICK:
            CalculateMFI(bar, MACDBuffer, tick_volume, MFIBuffer)
        else:
            CalculateMFI(bar, MACDBuffer, volume, MFIBuffer)
        ColorMFIBuffer[bar] = 0.0
        if MFIBuffer[bar] > SignBuffer[bar]:
            ColorMFIBuffer[bar] = 1.0
        if MFIBuffer[bar] < SignBuffer[bar]:
            ColorMFIBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def CalculateMFI(index, InBuffer, VolBuffer, OutBuffer):
    dPositiveMF = 0.0
    dNegativeMF = 0.0
    dCurrentTP = float(VolBuffer[index])
    for kkk in range(1, _int(MFIPeriod) + 1):
        iii = index - kkk
        dPreviousTP = float(VolBuffer[iii])
        if dCurrentTP > dPreviousTP:
            dPositiveMF += VolBuffer[iii - 1] * dCurrentTP
        if dCurrentTP < dPreviousTP:
            dNegativeMF += VolBuffer[iii - 1] * dCurrentTP
        dCurrentTP = dPreviousTP
    if dNegativeMF:
        OutBuffer[index] = caliber * Point() * (50.0 - _fdiv(100.0, 1 + _fdiv(dPositiveMF, dNegativeMF)))
    else:
        OutBuffer[index] = caliber * Point() * 100.0

# ---- static local variables
_s_OnCalculate_MA1 = CMoving_Average()
_s_OnCalculate_MA2 = CMoving_Average()
_s_OnCalculate_MA3 = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDfMFI(_MQL5Indicator):
    name = 'MACDfMFI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast_MA': 12,  # период быстрого мувинга MACD
        'Slow_MA': 26,  # глубина  медленного мувинга MACD
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # метод усреднения индикатора
        'Signal_SMA': 9,  # период сигнальной линии
        'AppliedPrice_': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'MFIPeriod': 12,  # период MFI
        'MFIVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём MFI
        'caliber': 4.0,  # масштабирование
    }

