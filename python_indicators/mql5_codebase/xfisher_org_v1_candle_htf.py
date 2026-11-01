"""XFisher_org_v1_Candle_HTF — converted from MQL5: MQL5 Indicators/XFisher_org_v1_Candle_HTF/XFisher_org_v1_Candle_HTF.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 8421504, 16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XFisher_org_v1_Candle_Open;XFisher_org_v1_Candle_High;XFisher_org_v1_Candle_Low;XFisher_org_v1_Candle_Close'}, 'levels': [1.5, 0.0, -1.5], 'description': [], 'name': 'XFisher_org_v1_Candle_HTF', 'source': 'MQL5 Indicators/XFisher_org_v1_Candle_HTF/XFisher_org_v1_Candle_HTF.mq5', 'folder': 'XFisher_org_v1_Candle_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'FLength', 'py': 'FLength', 'param': 'FLength', 'type': 'uint', 'default': 14, 'label': 'глубина усреднения', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
FLength = _input('FLength', 14)  # глубина усреднения
MA_SMethod = _input('MA_SMethod', MODE_JJMA)  # Метод сглаживания
MA_Length = _input('MA_Length', 5)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # параметр сглаживания,
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 2
    short_name = 'XFisher_org_v1_Candle' + ' ' + Symbol() + '(' + GetStringTimeframe(Period()) + ')'
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'XFisher_org_v1_Candle', FLength, MA_SMethod, MA_Length, MA_Phase, Gap, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XFisher_org_v1_Candle')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('XFisher_org_v1_Candle', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicatorBar("", TimeFrame, Ind_Handle, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicatorBar(Symb, TFrame, IndHandle, Time, Rates_Total, Prev_Calculated, Min_Rates_Total):
    global _s_CountIndicatorBar_LastCountBar
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicatorBar_LastCountBar = limit
    else:
        limit = _s_CountIndicatorBar_LastCountBar + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TimeFrame, _DT(Time[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if Time[bar] >= IndTime[0] and Time[bar + 1] < IndTime[0]:
            _s_CountIndicatorBar_LastCountBar = bar
            Col = Arr(1, 0.0, dyn=False)
            O = Arr(1, 0.0, dyn=False)
            H = Arr(1, 0.0, dyn=False)
            L = Arr(1, 0.0, dyn=False)
            C = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, 4, _DT(Time[bar]), 1, Col) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 0, _DT(Time[bar]), 1, O) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 1, _DT(Time[bar]), 1, H) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 2, _DT(Time[bar]), 1, L) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 3, _DT(Time[bar]), 1, C) <= 0:
                return (0 != 0)
            ExtColorBuffer[bar] = Col[0]
            ExtOpenBuffer[bar] = O[0]
            ExtLowBuffer[bar] = L[0]
            ExtHighBuffer[bar] = H[0]
            ExtCloseBuffer[bar] = C[0]
        else:
            ExtColorBuffer[bar] = ExtColorBuffer[bar + 1]
            ExtOpenBuffer[bar] = ExtOpenBuffer[bar + 1]
            ExtLowBuffer[bar] = ExtLowBuffer[bar + 1]
            ExtHighBuffer[bar] = ExtHighBuffer[bar + 1]
            ExtCloseBuffer[bar] = ExtCloseBuffer[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicatorBar_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XFisherOrgV1CandleHTF(_MQL5Indicator):
    name = 'XFisher_org_v1_Candle_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'FLength': 14,  # глубина усреднения
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания
        'MA_Length': 5,  # Глубина сглаживания
        'MA_Phase': 15,  # параметр сглаживания,
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

