"""XRSI_Histogram_Vol — converted from MQL5: MQL5 Indicators/XRSI_Histogram_Vol/XRSI_Histogram_Vol.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 10, 4: 1, 5: 1}, 'colors': {1: [16760576], 2: [16711680], 3: [65280, 8421376, 14381203, 2763429, 16711935], 4: [16711680], 5: [16760576]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 1, 5: 1}, 'styles': {1: 4, 2: 4, 3: 0, 4: 4, 5: 4}, 'labels': {1: 'XRSI_Histogram_Vol Max', 2: 'XRSI_Histogram_Vol Res', 3: 'XRSI_Histogram_Vol', 4: 'XRSI_Histogram_Vol Supr', 5: 'XRSI_Histogram_Vol Min'}, 'levels': [], 'description': [], 'name': 'XRSI_Histogram_Vol', 'source': 'MQL5 Indicators/XRSI_Histogram_Vol/XRSI_Histogram_Vol.mq5', 'folder': 'XRSI_Histogram_Vol', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'цена', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'HighLevel2', 'py': 'HighLevel2', 'param': 'HighLevel2', 'type': 'int', 'default': 20, 'label': 'уровень перекупленности 2', 'sinput': False}, {'mql': 'HighLevel1', 'py': 'HighLevel1', 'param': 'HighLevel1', 'type': 'int', 'default': 15, 'label': 'уровень перекупленности 1', 'sinput': False}, {'mql': 'LowLevel1', 'py': 'LowLevel1', 'param': 'LowLevel1', 'type': 'int', 'default': -15, 'label': 'уровень перепроданности 1', 'sinput': False}, {'mql': 'LowLevel2', 'py': 'LowLevel2', 'param': 'LowLevel2', 'type': 'int', 'default': -20, 'label': 'уровень перепроданности 2', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 14)  # период индикатора
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # цена
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
HighLevel2 = _input('HighLevel2', 20)  # уровень перекупленности 2
HighLevel1 = _input('HighLevel1', 15)  # уровень перекупленности 1
LowLevel1 = _input('LowLevel1', -15)  # уровень перепроданности 1
LowLevel2 = _input('LowLevel2', -20)  # уровень перепроданности 2
MA_SMethod = _input('MA_SMethod', MODE_SMA_)  # Метод усреднения
MA_Length = _input('MA_Length', 12)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # параметр первого сглаживания,
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
MaxIndBuffer = Arr(0, 0.0)
MinIndBuffer = Arr(0, 0.0)
RSI_Handle = 0
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global RSI_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(RSIPeriod)
    min_rates_total = min_rates_1 + GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    RSI_Handle = iRSI(None, 0, RSIPeriod, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    SetIndexBuffer(0, MaxIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(MaxIndBuffer, True)
    SetIndexBuffer(1, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    SetIndexBuffer(4, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(5, MinIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(MinIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XRSI_Histogram_Vol(' + _str(RSIPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(RSI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    vol = 0.0
    xvol = 0.0
    maxbar = rates_total - min_rates_1 - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if VolumeType == VOLUME_TICK:
        ArraySetAsSeries(Tick_Volume, True)
    else:
        ArraySetAsSeries(Volume, True)
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, IndBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] -= 50
        if VolumeType == VOLUME_TICK:
            vol = float(Tick_Volume[bar])
        else:
            vol = float(Volume[bar])
        IndBuffer[bar] *= vol
        IndBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, IndBuffer[bar], bar, True)
        xvol = XMA2.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, vol, bar, True)
        MaxIndBuffer[bar] = HighLevel2 * xvol
        UpIndBuffer[bar] = HighLevel1 * xvol
        DnIndBuffer[bar] = LowLevel1 * xvol
        MinIndBuffer[bar] = LowLevel2 * xvol
        clr = _int(2.0)
        if IndBuffer[bar] > MaxIndBuffer[bar]:
            clr = _int(0.0)
        elif IndBuffer[bar] > UpIndBuffer[bar]:
            clr = _int(1.0)
        elif IndBuffer[bar] < MinIndBuffer[bar]:
            clr = _int(4.0)
        elif IndBuffer[bar] < DnIndBuffer[bar]:
            clr = _int(3.0)
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XRSIHistogramVol(_MQL5Indicator):
    name = 'XRSI_Histogram_Vol'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 14,  # период индикатора
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # цена
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'HighLevel2': 20,  # уровень перекупленности 2
        'HighLevel1': 15,  # уровень перекупленности 1
        'LowLevel1': -15,  # уровень перепроданности 1
        'LowLevel2': -20,  # уровень перепроданности 2
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'MA_Length': 12,  # Глубина сглаживания
        'MA_Phase': 15,  # параметр первого сглаживания,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

