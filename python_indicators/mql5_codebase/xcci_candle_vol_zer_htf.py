"""XCCI_Candle_Vol_Zer_HTF — converted from MQL5: MQL5 Indicators/XCCI_Candle_Vol_Zer_HTF/XCCI_Candle_Vol_Zer_HTF.mq5

XCCI_Candle_Vol_Zer с фиксированным во входных параметрах таймфреймом
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 17, 4: 1, 5: 12}, 'colors': {1: [16443110], 2: [8421376], 3: [16776960, 16711680, 8421376, 17919, 2763429, 55295], 4: [3937500], 5: [3329330, 9639167]}, 'widths': {2: 1, 4: 1, 5: 1}, 'styles': {2: 4, 4: 4}, 'labels': {1: 'XCCI_Candle_Vol Channel', 2: 'XCCI_Candle_Vol Res', 3: 'XCCI_Candle_Vol Open;XCCI_Candle_Vol High;XCCI_Candle_Vol Low;XCCI_Candle_Vol Close', 4: 'XCCI_Candle_Vol Supr', 5: 'XCCI_Candle_Vol ZeroSignal'}, 'levels': [0.0], 'description': ['XCCI_Candle_Vol_Zer с фиксированным во входных параметрах таймфреймом'], 'name': 'XCCI_Candle_Vol_Zer_HTF', 'source': 'MQL5 Indicators/XCCI_Candle_Vol_Zer_HTF/XCCI_Candle_Vol_Zer_HTF.mq5', 'folder': 'XCCI_Candle_Vol_Zer_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 50, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -50, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 7, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'SignTotal', 'py': 'SignTotal', 'param': 'SignTotal', 'type': 'uint', 'default': 3, 'label': 'Количество звуковых сигналов при побое свечкой нуля', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'номер бара для получения сигнала пробоя свечкой нуля', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
CCIPeriod = _input('CCIPeriod', 14)  # период индикатора
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
HighLevel = _input('HighLevel', 50)  # уровень перекупленности
LowLevel = _input('LowLevel', -50)  # уровень перепроданности
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
MA_SMethod = _input('MA_SMethod', MODE_T3)  # Метод усреднения
MA_Length = _input('MA_Length', 12)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # параметр первого сглаживания,
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SignTotal = _input('SignTotal', 3)  # Количество звуковых сигналов при побое свечкой нуля
SignalBar = _input('SignalBar', 1)  # номер бара для получения сигнала пробоя свечкой нуля
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
UpCldIndBuffer = Arr(0, 0.0)
DnCldIndBuffer = Arr(0, 0.0)
ZrSigBuffer = Arr(0, 0.0)
ColorZrSigBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('XCCI_Candle_Vol_Zer', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    AtrPeriod = 15
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'XCCI_Candle_Vol_Zer', CCIPeriod, VolumeType, HighLevel, LowLevel, Gap, MA_SMethod, MA_Length, MA_Phase, 0, SignTotal, SignalBar)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XCCI_Candle_Vol_Zer')
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
    SetIndexBuffer(9, ZrSigBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total + AtrPeriod)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(4, PLOT_ARROW, 124)
    ArraySetAsSeries(ZrSigBuffer, True)
    SetIndexBuffer(10, ColorZrSigBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorZrSigBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'XCCI_Candle_Vol_Zer', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, UpCldIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, DnCldIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, UpIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, OpenBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(4, "", TimeFrame, Ind_Handle, 4, HighBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(5, "", TimeFrame, Ind_Handle, 5, LowBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(6, "", TimeFrame, Ind_Handle, 6, CloseBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(7, "", TimeFrame, Ind_Handle, 7, ColorBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(8, "", TimeFrame, Ind_Handle, 8, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(9, "", TimeFrame, Ind_Handle, 9, ZrSigBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(10, "", TimeFrame, Ind_Handle, 10, ColorZrSigBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, Time, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(Time[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if Time[bar] >= IndTime[0] and Time[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(Time[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

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

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(11, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XCCICandleVolZerHTF(_MQL5Indicator):
    name = 'XCCI_Candle_Vol_Zer_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'CCIPeriod': 14,  # период индикатора
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'HighLevel': 50,  # уровень перекупленности
        'LowLevel': -50,  # уровень перепроданности
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения
        'MA_Length': 12,  # Глубина сглаживания
        'MA_Phase': 15,  # параметр первого сглаживания,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'SignTotal': 3,  # Количество звуковых сигналов при побое свечкой нуля
        'SignalBar': 1,  # номер бара для получения сигнала пробоя свечкой нуля
    }

