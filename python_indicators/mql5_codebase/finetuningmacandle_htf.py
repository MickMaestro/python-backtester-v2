"""FineTuningMACandle_HTF — converted from MQL5: MQL5 Indicators/FineTuningMACandle_HTF/FineTuningMACandle_HTF.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 8421504, 15570276]}, 'widths': {}, 'styles': {}, 'labels': {1: 'FineTuningMACandle_Open;FineTuningMACandle_High;FineTuningMACandle_Low;FineTuningMACandle_Close'}, 'levels': [], 'description': [], 'name': 'FineTuningMACandle_HTF', 'source': 'MQL5 Indicators/FineTuningMACandle_HTF/FineTuningMACandle_HTF.mq5', 'folder': 'FineTuningMACandle_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'FTMA', 'py': 'FTMA', 'param': 'FTMA', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'rank1', 'py': 'rank1', 'param': 'rank1', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'rank2', 'py': 'rank2', 'param': 'rank2', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'rank3', 'py': 'rank3', 'param': 'rank3', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'shift1', 'py': 'shift1', 'param': 'shift1', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'shift2', 'py': 'shift2', 'param': 'shift2', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'shift3', 'py': 'shift3', 'param': 'shift3', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
FTMA = _input('FTMA', 10)
rank1 = _input('rank1', 2.0)
rank2 = _input('rank2', 2.0)
rank3 = _input('rank3', 2.0)
shift1 = _input('shift1', 1.0)
shift2 = _input('shift2', 1.0)
shift3 = _input('shift3', 1.0)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
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
    short_name = 'FineTuningMACandle' + ' ' + Symbol() + '(' + GetStringTimeframe(Period()) + ')'
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'FineTuningMACandle', FTMA, rank1, rank2, rank3, shift1, shift2, shift3, 0, PriceShift, Gap)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора FineTuningMACandle')
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
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('FineTuningMACandle', TimeFrame):
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


class FineTuningMACandleHTF(_MQL5Indicator):
    name = 'FineTuningMACandle_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'FTMA': 10,
        'rank1': 2.0,
        'rank2': 2.0,
        'rank3': 2.0,
        'shift1': 1.0,
        'shift2': 1.0,
        'shift3': 1.0,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
    }

