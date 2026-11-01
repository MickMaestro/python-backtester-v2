"""gmma_htf — converted from MQL5: MQL5 Indicators/GMMA_HTF/gmma_htf.mq5

Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {1: [255], 2: [255], 3: [255], 4: [255], 5: [255], 6: [255], 7: [16711680], 8: [16711680], 9: [16711680], 10: [16711680], 11: [16711680], 12: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'gmma_htf', 'source': 'MQL5 Indicators/GMMA_HTF/gmma_htf.mq5', 'folder': 'GMMA_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'xMA_Method', 'py': 'xMA_Method', 'param': 'xMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'TrLength1', 'py': 'TrLength1', 'param': 'TrLength1', 'type': 'int', 'default': 3, 'label': 'Период усреднения 1 трейдерский', 'sinput': False}, {'mql': 'TrLength2', 'py': 'TrLength2', 'param': 'TrLength2', 'type': 'int', 'default': 5, 'label': 'Период усреднения 2 трейдерский', 'sinput': False}, {'mql': 'TrLength3', 'py': 'TrLength3', 'param': 'TrLength3', 'type': 'int', 'default': 8, 'label': 'Период усреднения 3 трейдерский', 'sinput': False}, {'mql': 'TrLength4', 'py': 'TrLength4', 'param': 'TrLength4', 'type': 'int', 'default': 10, 'label': 'Период усреднения 4 трейдерский', 'sinput': False}, {'mql': 'TrLength5', 'py': 'TrLength5', 'param': 'TrLength5', 'type': 'int', 'default': 12, 'label': 'Период усреднения 5 трейдерский', 'sinput': False}, {'mql': 'TrLength6', 'py': 'TrLength6', 'param': 'TrLength6', 'type': 'int', 'default': 15, 'label': 'Период усреднения 6 трейдерский', 'sinput': False}, {'mql': 'InvLength1', 'py': 'InvLength1', 'param': 'InvLength1', 'type': 'int', 'default': 30, 'label': 'Период усреднения 1 инвесторский', 'sinput': False}, {'mql': 'InvLength2', 'py': 'InvLength2', 'param': 'InvLength2', 'type': 'int', 'default': 35, 'label': 'Период усреднения 2 инвесторский', 'sinput': False}, {'mql': 'InvLength3', 'py': 'InvLength3', 'param': 'InvLength3', 'type': 'int', 'default': 40, 'label': 'Период усреднения 3 инвесторский', 'sinput': False}, {'mql': 'InvLength4', 'py': 'InvLength4', 'param': 'InvLength4', 'type': 'int', 'default': 45, 'label': 'Период усреднения 4 инвесторский', 'sinput': False}, {'mql': 'InvLength5', 'py': 'InvLength5', 'param': 'InvLength5', 'type': 'int', 'default': 50, 'label': 'Период усреднения 5 инвесторский', 'sinput': False}, {'mql': 'InvLength6', 'py': 'InvLength6', 'param': 'InvLength6', 'type': 'int', 'default': 60, 'label': 'Период усреднения 6 инвесторский', 'sinput': False}, {'mql': 'xPhase', 'py': 'xPhase', 'param': 'xPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
xMA_Method = _input('xMA_Method', MODE_EMA)  # Метод усреднения
TrLength1 = _input('TrLength1', 3)  # Период усреднения 1 трейдерский
TrLength2 = _input('TrLength2', 5)  # Период усреднения 2 трейдерский
TrLength3 = _input('TrLength3', 8)  # Период усреднения 3 трейдерский
TrLength4 = _input('TrLength4', 10)  # Период усреднения 4 трейдерский
TrLength5 = _input('TrLength5', 12)  # Период усреднения 5 трейдерский
TrLength6 = _input('TrLength6', 15)  # Период усреднения 6 трейдерский
InvLength1 = _input('InvLength1', 30)  # Период усреднения 1 инвесторский
InvLength2 = _input('InvLength2', 35)  # Период усреднения 2 инвесторский
InvLength3 = _input('InvLength3', 40)  # Период усреднения 3 инвесторский
InvLength4 = _input('InvLength4', 45)  # Период усреднения 4 инвесторский
InvLength5 = _input('InvLength5', 50)  # Период усреднения 5 инвесторский
InvLength6 = _input('InvLength6', 60)  # Период усреднения 6 инвесторский
xPhase = _input('xPhase', 100)  # Параметр сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора GMMA не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'GMMA' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol_, TimeFrame, 'GMMA', xMA_Method, TrLength1, TrLength2, TrLength3, TrLength4, TrLength5, TrLength6, InvLength1, InvLength2, InvLength3, InvLength4, InvLength5, InvLength6, xPhase, IPC, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора GMMA')
        return INIT_FAILED
    period = Arr(12, 0, dyn=False)
    period[0] = TrLength1
    period[1] = TrLength2
    period[2] = TrLength3
    period[3] = TrLength4
    period[4] = TrLength5
    period[5] = TrLength6
    period[6] = InvLength1
    period[7] = InvLength2
    period[8] = InvLength3
    period[9] = InvLength4
    period[10] = InvLength5
    period[11] = InvLength6
    for numb in range(0, 12):
        shortname = Box('')
        StringConcatenate(shortname, 'GMMA', numb, '(', period[numb], ')')
        PlotIndexSetString(numb, PLOT_LABEL, shortname.v)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb, PLOT_DRAW_BEGIN, min_rates_total)
        SetIndexBuffer(numb, Ind[numb].IndBuffer, INDICATOR_DATA)
        ArraySetAsSeries(Ind[numb].IndBuffer, True)
        PlotIndexSetInteger(numb, PLOT_DRAW_TYPE, PlotIndexGetInteger(0, PLOT_DRAW_TYPE))
        PlotIndexSetInteger(numb, PLOT_LINE_STYLE, PlotIndexGetInteger(0, PLOT_LINE_STYLE))
        PlotIndexSetInteger(numb, PLOT_LINE_WIDTH, PlotIndexGetInteger(0, PLOT_LINE_WIDTH))
    shortname = Box("")
    StringConcatenate(shortname, 'GMMA', 12, '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    for numb in range(0, 12):
        if not CountIndicator(numb, "", TimeFrame, Ind_Handle, numb, Ind[numb].IndBuffer, time, rates_total, prev_calculated, min_rates_total):
            return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol_, TimeFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

# ---- global variables initialised from expressions
Ind = Arr(12, 0, dyn=False, factory=CIndicatorsBuffers)

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(12, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GmmaHtf(_MQL5Indicator):
    name = 'gmma_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'xMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения
        'TrLength1': 3,  # Период усреднения 1 трейдерский
        'TrLength2': 5,  # Период усреднения 2 трейдерский
        'TrLength3': 8,  # Период усреднения 3 трейдерский
        'TrLength4': 10,  # Период усреднения 4 трейдерский
        'TrLength5': 12,  # Период усреднения 5 трейдерский
        'TrLength6': 15,  # Период усреднения 6 трейдерский
        'InvLength1': 30,  # Период усреднения 1 инвесторский
        'InvLength2': 35,  # Период усреднения 2 инвесторский
        'InvLength3': 40,  # Период усреднения 3 инвесторский
        'InvLength4': 45,  # Период усреднения 4 инвесторский
        'InvLength5': 50,  # Период усреднения 5 инвесторский
        'InvLength6': 60,  # Период усреднения 6 инвесторский
        'xPhase': 100,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

