"""XCCI_Candle_Vol — converted from MQL5: MQL5 Indicators/XCCI_Candle_Vol_HTF/XCCI_Candle_Vol.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 17, 4: 1}, 'colors': {1: [16443110], 2: [8421376], 3: [16776960, 16711680, 8421376, 17919, 2763429, 55295], 4: [3937500]}, 'widths': {2: 1, 4: 1}, 'styles': {2: 4, 4: 4}, 'labels': {1: 'XCCI_Candle_Vol Channel', 2: 'XCCI_Candle_Vol Res', 3: 'XCCI_Candle_Vol Open;XCCI_Candle_Vol High;XCCI_Candle_Vol Low;XCCI_Candle_Vol Close', 4: 'XCCI_Candle_Vol Supr'}, 'levels': [0.0], 'description': [], 'name': 'XCCI_Candle_Vol', 'source': 'MQL5 Indicators/XCCI_Candle_Vol_HTF/XCCI_Candle_Vol.mq5', 'folder': 'XCCI_Candle_Vol_HTF', 'inputs': [{'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 50, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -50, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 7, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
CCIPeriod = _input('CCIPeriod', 14)  # период индикатора
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
HighLevel = _input('HighLevel', 50)  # уровень перекупленности
LowLevel = _input('LowLevel', -50)  # уровень перепроданности
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
MA_SMethod = _input('MA_SMethod', MODE_T3)  # Метод усреднения
MA_Length = _input('MA_Length', 12)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # параметр первого сглаживания,
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
min_rates_1 = 0
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
UpCldIndBuffer = Arr(0, 0.0)
DnCldIndBuffer = Arr(0, 0.0)
CCI_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = _int(CCIPeriod)
    min_rates_total = min_rates_1 + GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    CCI_Handle[0] = iCCI(None, 0, CCIPeriod, PRICE_OPEN)
    if CCI_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI 1')
        return INIT_FAILED
    CCI_Handle[1] = iCCI(None, 0, CCIPeriod, PRICE_HIGH)
    if CCI_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI 2')
        return INIT_FAILED
    CCI_Handle[2] = iCCI(None, 0, CCIPeriod, PRICE_LOW)
    if CCI_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI 3')
        return INIT_FAILED
    CCI_Handle[3] = iCCI(None, 0, CCIPeriod, PRICE_CLOSE)
    if CCI_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI 4')
        return INIT_FAILED
    SetIndexBuffer(0, UpCldIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpCldIndBuffer, True)
    SetIndexBuffer(1, DnCldIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnCldIndBuffer, True)
    SetIndexBuffer(2, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(3, OpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, CloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(OpenBuffer, True)
    ArraySetAsSeries(HighBuffer, True)
    ArraySetAsSeries(LowBuffer, True)
    ArraySetAsSeries(CloseBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    SetIndexBuffer(8, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(DnIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XCCI_Candle_Vol(' + _str(CCIPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if (((BarsCalculated(CCI_Handle[0]) < rates_total or BarsCalculated(CCI_Handle[1]) < rates_total) or BarsCalculated(CCI_Handle[2]) < rates_total) or BarsCalculated(CCI_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    vol = 0.0
    xvol = 0.0
    maxbar = rates_total - min_rates_1 - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Open, True)
    if VolumeType == VOLUME_TICK:
        ArraySetAsSeries(Tick_Volume, True)
    else:
        ArraySetAsSeries(Volume, True)
    if CopyBuffer(CCI_Handle[0], 0, 0, to_copy, OpenBuffer) <= 0:
        return 0
    if CopyBuffer(CCI_Handle[1], 0, 0, to_copy, HighBuffer) <= 0:
        return 0
    if CopyBuffer(CCI_Handle[2], 0, 0, to_copy, LowBuffer) <= 0:
        return 0
    if CopyBuffer(CCI_Handle[3], 0, 0, to_copy, CloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(OpenBuffer[bar], CloseBuffer[bar])
        Max = MathMax(Max, LowBuffer[bar])
        Max = MathMax(Max, HighBuffer[bar])
        Min = MathMin(OpenBuffer[bar], CloseBuffer[bar])
        Min = MathMin(Min, LowBuffer[bar])
        Min = MathMin(Min, HighBuffer[bar])
        HighBuffer[bar] = Max
        LowBuffer[bar] = Min
        if VolumeType == VOLUME_TICK:
            vol = float(Tick_Volume[bar])
        else:
            vol = float(Volume[bar])
        OpenBuffer[bar] *= vol
        HighBuffer[bar] *= vol
        LowBuffer[bar] *= vol
        CloseBuffer[bar] *= vol
        OpenBuffer[bar] = XMAO.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, OpenBuffer[bar], bar, True)
        HighBuffer[bar] = XMAH.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, HighBuffer[bar], bar, True)
        LowBuffer[bar] = XMAL.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, LowBuffer[bar], bar, True)
        CloseBuffer[bar] = XMAC.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, CloseBuffer[bar], bar, True)
        xvol = XMAV.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, vol, bar, True)
        if MathAbs(Open[bar] - Close[bar]) <= Gap:
            OpenBuffer[bar] = CloseBuffer[bar + 1]
        UpCldIndBuffer[bar] = HighLevel * xvol
        UpIndBuffer[bar] = UpCldIndBuffer[bar]
        DnCldIndBuffer[bar] = LowLevel * xvol
        DnIndBuffer[bar] = DnCldIndBuffer[bar]
        clr = _int(2.0)
        if CloseBuffer[bar] > UpIndBuffer[bar]:
            if CloseBuffer[bar] >= OpenBuffer[bar]:
                clr = _int(0.0)
            else:
                clr = _int(1.0)
        elif CloseBuffer[bar] < DnIndBuffer[bar]:
            if CloseBuffer[bar] <= OpenBuffer[bar]:
                clr = _int(5.0)
            else:
                clr = _int(4.0)
        else:
            if CloseBuffer[bar] >= OpenBuffer[bar]:
                clr = _int(2.0)
            else:
                clr = _int(3.0)
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMAO = _alloc(CXMA)
XMAO.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAL = _alloc(CXMA)
XMAL.__init__()
XMAC = _alloc(CXMA)
XMAC.__init__()
XMAV = _alloc(CXMA)
XMAV.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XCCICandleVol(_MQL5Indicator):
    name = 'XCCI_Candle_Vol'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCIPeriod': 14,  # период индикатора
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'HighLevel': 50,  # уровень перекупленности
        'LowLevel': -50,  # уровень перепроданности
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения
        'MA_Length': 12,  # Глубина сглаживания
        'MA_Phase': 15,  # параметр первого сглаживания,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

