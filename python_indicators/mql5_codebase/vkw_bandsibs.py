"""VKW_BandsIBS — converted from MQL5: MQL5 Indicators/WKBIBS/VKW_BandsIBS.mq5

Internal Bar Strength
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [3329330], 3: [9639167]}, 'widths': {1: 1, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Internal Bar Strength', 2: 'VKW_Bands Upper', 3: 'VKW_Bands Lower'}, 'levels': [60.0, 40.0], 'description': ['Internal Bar Strength'], 'name': 'VKW_BandsIBS', 'source': 'MQL5 Indicators/WKBIBS/VKW_BandsIBS.mq5', 'folder': 'WKBIBS', 'inputs': [{'mql': 'IMA_Method', 'py': 'IMA_Method', 'param': 'IMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения IBS', 'sinput': False}, {'mql': 'ILength', 'py': 'ILength', 'param': 'ILength', 'type': 'int', 'default': 5, 'label': 'Глубина усреднения IBS', 'sinput': False}, {'mql': 'IPhase', 'py': 'IPhase', 'param': 'IPhase', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения IBS', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа IBS', 'sinput': False}, {'mql': 'IShift', 'py': 'IShift', 'param': 'IShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора IBS по горизонтали в барах', 'sinput': False}, {'mql': 'IDirect', 'py': 'IDirect', 'param': 'IDirect', 'type': 'bool', 'default': True, 'label': 'Переворот индикатора по вертикали', 'sinput': False}, {'mql': 'SmMA_Method', 'py': 'SmMA_Method', 'param': 'SmMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'SLength', 'py': 'SLength', 'param': 'SLength', 'type': 'int', 'default': 3, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'SShift', 'py': 'SShift', 'param': 'SShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора канала по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_LOW = 0
PRICE_HIGH_CLOSE = 1
_enum('Applied_price_', {0: 'PRICE_CLOSE_LOW', 1: 'PRICE_HIGH_CLOSE'})

# ---- inputs and global variables
IMA_Method = _input('IMA_Method', MODE_SMA_)  # Метод усреднения IBS
ILength = _input('ILength', 5)  # Глубина усреднения IBS
IPhase = _input('IPhase', 15)  # Параметр усреднения IBS
IPC = _input('IPC', PRICE_HIGH_CLOSE)  # Ценовая константа IBS
IShift = _input('IShift', 0)  # Сдвиг индикатора IBS по горизонтали в барах
IDirect = _input('IDirect', True)  # Переворот индикатора по вертикали
RPeriod = 25  # Период поиска экстремумов
SmMA_Method = _input('SmMA_Method', MODE_SMA_)  # Метод сглаживания
SLength = _input('SLength', 3)  # Глубина сглаживания
SPhase = _input('SPhase', 100)  # Параметр сглаживания
SShift = _input('SShift', 0)  # Сдвиг индикатора канала по горизонтали в барах
XIBS = Arr(0, 0.0)
UpVKWB = Arr(0, 0.0)
DnVKWB = Arr(0, 0.0)
min_rates_total = 0
min_rates_ibs = 0
min_rates_extr = 0

def OnInit():
    global min_rates_extr, min_rates_ibs, min_rates_total
    min_rates_ibs = XMA1.GetStartBars(IMA_Method, ILength, IPhase)
    min_rates_extr = _int(min_rates_ibs + RPeriod)
    min_rates_total = min_rates_extr + XMA1.GetStartBars(SmMA_Method, SLength, SPhase)
    XMA1.XMALengthCheck('ILength', ILength)
    XMA1.XMAPhaseCheck('IPhase', IPhase, IMA_Method)
    XMA1.XMALengthCheck('SLength', SLength)
    XMA1.XMAPhaseCheck('SPhase', SPhase, SmMA_Method)
    SetIndexBuffer(0, XIBS, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, IShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_ibs)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, UpVKWB, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, SShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, DnVKWB, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, SShift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    shortname = 'VKW_BandsIBS'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    range_ = 0.0
    dprice = 0.0
    ibs = 0.0
    n_max = 0.0
    n_min = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if IPC:
            dprice = close[bar] - low[bar]
        else:
            dprice = high[bar] - close[bar]
        range_ = high[bar] - low[bar]
        if range_:
            ibs = _fdiv(dprice, range_)
        else:
            ibs = _fdiv(dprice, Point())
        XIBS[bar] = 100 * XMA1.XMASeries(0, prev_calculated, rates_total, IMA_Method, IPhase, ILength, ibs, bar, False)
        if not IDirect:
            XIBS[bar] *= -1
        if bar > (min_rates_extr + 1):
            ArraySetAsSeries(XIBS, True)
            rate_ = rates_total - 1 - bar
            n_max = XIBS[ArrayMaximum(XIBS, rate_, RPeriod)]
            n_min = XIBS[ArrayMinimum(XIBS, rate_, RPeriod)]
            ArraySetAsSeries(XIBS, False)
        UpVKWB[bar] = XMA2.XMASeries(min_rates_extr, prev_calculated, rates_total, SmMA_Method, SPhase, SLength, n_max, bar, False)
        DnVKWB[bar] = XMA3.XMASeries(min_rates_extr, prev_calculated, rates_total, SmMA_Method, SPhase, SLength, n_min, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VKWBandsIBS(_MQL5Indicator):
    name = 'VKW_BandsIBS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения IBS
        'ILength': 5,  # Глубина усреднения IBS
        'IPhase': 15,  # Параметр усреднения IBS
        'IPC': _Choice({0: 'Close-Low', 1: 'High-Close'}, default=1),  # Ценовая константа IBS
        'IShift': 0,  # Сдвиг индикатора IBS по горизонтали в барах
        'IDirect': True,  # Переворот индикатора по вертикали
        'SmMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания
        'SLength': 3,  # Глубина сглаживания
        'SPhase': 100,  # Параметр сглаживания
        'SShift': 0,  # Сдвиг индикатора канала по горизонтали в барах
    }

