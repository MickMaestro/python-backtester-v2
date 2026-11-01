"""Volume_Weighted_MA_Cloud — converted from MQL5: MQL5 Indicators/Volume_Weighted_MA_Cloud/Volume_Weighted_MA_Cloud.mq5

Copyright: Copyright © 2011, StatBars TO; Link: http://ridecrufter.narod.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, StatBars TO', 'link': 'http://ridecrufter.narod.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 8}, 'colors': {1: [15658671], 2: [12695295], 3: [16711935, 8421504, 16711680]}, 'widths': {3: 5}, 'styles': {3: 0}, 'labels': {1: 'Upper Cloud', 2: 'Lower Cloud', 3: 'Volume_Weighted_MA'}, 'levels': [], 'description': [], 'name': 'Volume_Weighted_MA_Cloud', 'source': 'MQL5 Indicators/Volume_Weighted_MA_Cloud/Volume_Weighted_MA_Cloud.mq5', 'folder': 'Volume_Weighted_MA_Cloud', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Dev', 'py': 'Dev', 'param': 'Dev', 'type': 'uint', 'default': 20, 'label': 'Девиация заливки фоном', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
Length = _input('Length', 12)  # глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Dev = _input('Dev', 20)  # Девиация заливки фоном
LineBuffer = Arr(0, 0.0)
ColorLineBuffer = Arr(0, 0.0)
UpCloudBuffer1 = Arr(0, 0.0)
UpCloudBuffer2 = Arr(0, 0.0)
DnCloudBuffer1 = Arr(0, 0.0)
DnCloudBuffer2 = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
Vol = Arr(0, 0.0)

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = _int(Length)
    dPriceShift = Point() * PriceShift
    ArrayResize(Vol, Length)
    SetIndexBuffer(0, UpCloudBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, UpCloudBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, DnCloudBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, DnCloudBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, LineBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ColorLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'Volume_Weighted_MA(', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    mov = 0.0
    sum_ = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        sum_ = 0.0
        for kkk in range(_int(bar - Length + 1), bar + 1):
            index = bar - kkk
            if VolumeType == VOLUME_TICK:
                Vol[index] = float(tick_volume[kkk])
            else:
                Vol[index] = float(volume[kkk])
            sum_ += Vol[index]
        for rrr in range(0, _int(Length)):
            Vol[rrr] = _fdiv(Vol[rrr], sum_)
        mov = 0.0
        for kkk in range(_int(bar - Length + 1), bar + 1):
            mov += PriceSeries(IPC, kkk, open, low, high, close) * Vol[bar - kkk]
        DnCloudBuffer1[bar] = mov + dPriceShift
        UpCloudBuffer2[bar] = DnCloudBuffer1[bar]
        LineBuffer[bar] = UpCloudBuffer2[bar]
        UpCloudBuffer1[bar] = LineBuffer[bar] * Dev
        DnCloudBuffer2[bar] = LineBuffer[bar] / Dev
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 1
        if LineBuffer[bar - 1] < LineBuffer[bar]:
            clr = 2
        if LineBuffer[bar - 1] > LineBuffer[bar]:
            clr = 0
        ColorLineBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeWeightedMACloud(_MQL5Indicator):
    name = 'Volume_Weighted_MA_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 12,  # глубина сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'Dev': 20,  # Девиация заливки фоном
    }

