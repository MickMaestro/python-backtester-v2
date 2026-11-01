"""FractalChannel_Cloud_HTF — converted from MQL5: MQL5 Indicators/FractalChannel_Cloud_HTF/FractalChannel_Cloud_HTF.mq5

FractalChannel_Cloud с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.70

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.70', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16252904], 2: [16773375], 3: [5737262], 4: [8421504], 5: [255]}, 'widths': {3: 1, 4: 1, 5: 1}, 'styles': {3: 4, 4: 4, 5: 4}, 'labels': {1: 'Upper FractalChannel cloud', 2: 'Lower FractalChannel cloud', 3: 'Upper FractalChannel', 4: 'Middle FractalChannel', 5: 'Lower FractalChannel'}, 'levels': [], 'description': ['FractalChannel_Cloud с фиксированным во входных параметрах таймфреймом'], 'name': 'FractalChannel_Cloud_HTF', 'source': 'MQL5 Indicators/FractalChannel_Cloud_HTF/FractalChannel_Cloud_HTF.mq5', 'folder': 'FractalChannel_Cloud_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'ChannelType', 'py': 'ChannelType', 'param': 'ChannelType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Margins', 'py': 'Margins', 'param': 'Margins', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'Prices', 'py': 'Prices', 'param': 'Prices', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Type
Type_1 = 1
Type_2 = 2
Type_3 = 3
_enum('Type', {1: 'Type_1', 2: 'Type_2', 3: 'Type_3'})

# enum PriceType
OpenClose = 0
LowHigh = 1
_enum('PriceType', {0: 'OpenClose', 1: 'LowHigh'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
ChannelType = _input('ChannelType', Type_1)
Margins = _input('Margins', 0.0)
Prices = _input('Prices', OpenClose)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'FractalChannel_Cloud', ChannelType, Margins, Prices, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора FractalChannel_Cloud')
        return INIT_FAILED
    IndInit_1(0, UpUpBuffer, INDICATOR_DATA)
    IndInit_1(1, UpDnBuffer, INDICATOR_DATA)
    IndInit_1(2, DnUpBuffer, INDICATOR_DATA)
    IndInit_1(3, DnDnBuffer, INDICATOR_DATA)
    IndInit_1(4, UpperBuffer, INDICATOR_DATA)
    IndInit_1(5, MiddleBuffer, INDICATOR_DATA)
    IndInit_1(6, LowerBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, min_rates_total, Shift)
    PlotInit(1, 0.0, min_rates_total, Shift)
    PlotInit(2, 0.0, min_rates_total, Shift)
    PlotInit(3, 0.0, min_rates_total, Shift)
    PlotInit(4, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'FractalChannel_Cloud', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def IndInit_1(Number, Buffer, BufferType):
    SetIndexBuffer(Number, Buffer, BufferType)
    ArraySetAsSeries(Buffer, True)

def IndInit_2(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('FractalChannel_Cloud', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, UpUpBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, UpDnBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, DnUpBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, DnDnBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(4, "", TimeFrame, Ind_Handle, 4, UpperBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(5, "", TimeFrame, Ind_Handle, 5, MiddleBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(6, "", TimeFrame, Ind_Handle, 6, LowerBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

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
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(7, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalChannelCloudHTF(_MQL5Indicator):
    name = 'FractalChannel_Cloud_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'ChannelType': _Choice({1: 'Type_1', 2: 'Type_2', 3: 'Type_3'}, default=1),
        'Margins': 0.0,
        'Prices': _Choice({0: 'OpenClose', 1: 'LowHigh'}, default=0),
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

