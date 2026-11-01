"""PEMA_2HTF — converted from MQL5: MQL5 Indicators/PEMA_2HTF/PEMA_2HTF.mq5

Цветное облако из мувингов PEMA с разных таймфреймов на одном графике.
Copyright: Copyright © 2006, lukas1; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, lukas1', 'link': '', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [10156544, 65535]}, 'widths': {}, 'styles': {}, 'labels': {1: 'PEMA_2HTF'}, 'levels': [], 'description': ['Цветное облако из мувингов PEMA с разных таймфреймов на одном графике.'], 'name': 'PEMA_2HTF', 'source': 'MQL5 Indicators/PEMA_2HTF/PEMA_2HTF.mq5', 'folder': 'PEMA_2HTF', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16386, 'label': 'Период графика индикатора 1 (младший таймфрейм)', 'sinput': False}, {'mql': 'EmaLength1', 'py': 'EmaLength1', 'param': 'EmaLength1', 'type': 'double', 'default': 50.01, 'label': 'глубина сглаживания индикатора 1', 'sinput': False}, {'mql': 'IPC1', 'py': 'IPC1', 'param': 'IPC1', 'type': 'int', 'default': 1, 'label': 'ценовая константа индикатора 1', 'sinput': False}, {'mql': 'PriceShift1', 'py': 'PriceShift1', 'param': 'PriceShift1', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора 1 по вертикали в пунктах', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16390, 'label': 'Период графика индикатора 2 (старший таймфрейм)', 'sinput': False}, {'mql': 'EmaLength2', 'py': 'EmaLength2', 'param': 'EmaLength2', 'type': 'double', 'default': 50.01, 'label': 'глубина сглаживания индикатора 2', 'sinput': False}, {'mql': 'IPC2', 'py': 'IPC2', 'param': 'IPC2', 'type': 'int', 'default': 1, 'label': 'ценовая константа индикатора 2', 'sinput': False}, {'mql': 'PriceShift2', 'py': 'PriceShift2', 'param': 'PriceShift2', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора 2 по вертикали в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг облака по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
TimeFrame1 = _input('TimeFrame1', PERIOD_H2)  # Период графика индикатора 1 (младший таймфрейм)
EmaLength1 = _input('EmaLength1', 50.01)  # глубина сглаживания индикатора 1
IPC1 = _input('IPC1', PRICE_CLOSE_)  # ценовая константа индикатора 1
PriceShift1 = _input('PriceShift1', 0)  # cдвиг индикатора 1 по вертикали в пунктах
TimeFrame2 = _input('TimeFrame2', PERIOD_H6)  # Период графика индикатора 2 (старший таймфрейм)
EmaLength2 = _input('EmaLength2', 50.01)  # глубина сглаживания индикатора 2
IPC2 = _input('IPC2', PRICE_CLOSE_)  # ценовая константа индикатора 2
PriceShift2 = _input('PriceShift2', 0)  # cдвиг индикатора 2 по вертикали в пунктах
Shift = _input('Shift', 0)  # Сдвиг облака по горизонтали в барах
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind1_Handle = 0
Ind2_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind1_Handle, Ind2_Handle, min_rates_total
    min_rates_total = 2
    Ind1_Handle = iCustom(Symbol(), TimeFrame1, 'PEMA', EmaLength1, IPC1, 0, PriceShift1)
    if Ind1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора PEMA 1')
        return INIT_FAILED
    Ind2_Handle = iCustom(Symbol(), TimeFrame2, 'PEMA', EmaLength2, IPC2, 0, PriceShift2)
    if Ind2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора PEMA 2')
        return INIT_FAILED
    IndInit(0, Ind1Buffer)
    IndInit(1, Ind2Buffer)
    PlotInit(0, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'PEMA', '(', GetStringTimeframe(TimeFrame1), ', ', GetStringTimeframe(TimeFrame2), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('PEMA', TimeFrame1, TimeFrame2):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind1_Handle) < Bars(Symbol(), TimeFrame1):
        return prev_calculated
    if BarsCalculated(Ind2_Handle) < Bars(Symbol(), TimeFrame2):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame1, Ind1_Handle, 0, Ind1Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame2, Ind2_Handle, 0, Ind2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def OnDeinit(reason):
    Comment('')
    ChartRedraw(0)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, nTime, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol(), TFrame, _DT(nTime[bar]), 1, IndTime) <= 0:
            return False
        if nTime[bar] >= IndTime[0] and nTime[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(nTime[bar]), 1, Arr_) <= 0:
                return False
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame1, TFrame2):
    if TFrame1 < Period() and TFrame1 != PERIOD_CURRENT:
        Comment('Период графика 1 для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return False
    if TFrame2 <= TFrame1:
        Comment('Период графика 2 для индикатора ' + IndName + ' должен быть больше периода графика 1! \n Следует изменить входные параметры индикатора!')
        return False
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(2, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PEMA2HTF(_MQL5Indicator):
    name = 'PEMA_2HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16386),  # Период графика индикатора 1 (младший таймфрейм)
        'EmaLength1': 50.01,  # глубина сглаживания индикатора 1
        'IPC1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа индикатора 1
        'PriceShift1': 0,  # cдвиг индикатора 1 по вертикали в пунктах
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Период графика индикатора 2 (старший таймфрейм)
        'EmaLength2': 50.01,  # глубина сглаживания индикатора 2
        'IPC2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа индикатора 2
        'PriceShift2': 0,  # cдвиг индикатора 2 по вертикали в пунктах
        'Shift': 0,  # Сдвиг облака по горизонтали в барах
    }

