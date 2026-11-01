"""SMI_Correct — converted from MQL5: MQL5 Indicators/SMI_Correct_HTF/SMI_Correct.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16776960, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'SMI_Correct'}, 'levels': [], 'description': [], 'name': 'SMI_Correct', 'source': 'MQL5 Indicators/SMI_Correct_HTF/SMI_Correct.mq5', 'folder': 'SMI_Correct_HTF', 'inputs': [{'mql': 'ExtrPeriod', 'py': 'ExtrPeriod', 'param': 'ExtrPeriod', 'type': 'uint', 'default': 13, 'label': 'период поиска экстремумов', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 1, 'label': 'метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 25, 'label': 'глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 3, 'label': 'глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'параметр второго сглаживания,', 'sinput': False}, {'mql': 'MA_Method3', 'py': 'MA_Method3', 'param': 'MA_Method3', 'type': 'int', 'default': 4, 'label': 'метод усреднения третьего сглаживания', 'sinput': False}, {'mql': 'Length3', 'py': 'Length3', 'param': 'Length3', 'type': 'uint', 'default': 5, 'label': 'глубина  третьего сглаживания', 'sinput': False}, {'mql': 'Phase3', 'py': 'Phase3', 'param': 'Phase3', 'type': 'int', 'default': 15, 'label': 'параметр третьего сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -50, 'label': '', 'sinput': False}, {'mql': 'HighLevelsColor', 'py': 'HighLevelsColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'MiddleLevelsColor', 'py': 'MiddleLevelsColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': '', 'sinput': False}, {'mql': 'LowLevelsColor', 'py': 'LowLevelsColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
ExtrPeriod = _input('ExtrPeriod', 13)  # период поиска экстремумов
MA_Method1 = _input('MA_Method1', MODE_EMA_)  # метод усреднения первого сглаживания
Length1 = _input('Length1', 25)  # глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # параметр первого сглаживания,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # метод усреднения второго сглаживания
Length2 = _input('Length2', 3)  # глубина  второго сглаживания
Phase2 = _input('Phase2', 15)  # параметр второго сглаживания,
MA_Method3 = _input('MA_Method3', MODE_JJMA)  # метод усреднения третьего сглаживания
Length3 = _input('Length3', 5)  # глубина  третьего сглаживания
Phase3 = _input('Phase3', 15)  # параметр третьего сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
HighLevel = _input('HighLevel', 50)
MiddleLevel = _input('MiddleLevel', 0)
LowLevel = _input('LowLevel', -50)
HighLevelsColor = _input('HighLevelsColor', clrBlue)
MiddleLevelsColor = _input('MiddleLevelsColor', clrGray)
LowLevelsColor = _input('LowLevelsColor', clrRed)
SMIBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_total
    min_rates_1 = _int(ExtrPeriod)
    min_rates_2 = min_rates_1 + GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_3 = min_rates_2 + GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total = min_rates_3 + GetStartBars(MA_Method3, Length3, Phase3)
    SetIndexBuffer(0, SMIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'SMI_Correct'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, HighLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, MiddleLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, LowLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    barx = 0
    HH = 0.0
    LL = 0.0
    price = 0.0
    SM = 0.0
    HQ = 0.0
    XSM = 0.0
    XHQ = 0.0
    XXSM = 0.0
    XXHQ = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        HH = -9999999999.0
        LL = 9999999999.0
        for index in range(0, _int(ExtrPeriod)):
            barx = bar - index
            if high[barx] > HH:
                HH = high[barx]
            if low[barx] < LL:
                LL = low[barx]
        price = PriceSeries(IPC, bar, open, low, high, close)
        SM = price - ((HH + LL) / 2.0)
        HQ = HH - LL
        XSM = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, SM, bar, False)
        XHQ = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, HQ, bar, False)
        XXSM = XMA3.XMASeries(min_rates_2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, XSM, bar, False)
        XXHQ = XMA4.XMASeries(min_rates_2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, XHQ, bar, False)
        if XXHQ:
            SMIBuffer[bar] = 100.0 * _fdiv(XXSM, XXHQ / 2)
        else:
            SMIBuffer[bar] = 100.0
        TriggerBuffer[bar] = XMA5.XMASeries(min_rates_3, prev_calculated, rates_total, MA_Method3, Phase3, Length3, SMIBuffer[bar], bar, False)
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
XMA4 = _alloc(CXMA)
XMA4.__init__()
XMA5 = _alloc(CXMA)
XMA5.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SMICorrect(_MQL5Indicator):
    name = 'SMI_Correct'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ExtrPeriod': 13,  # период поиска экстремумов
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод усреднения первого сглаживания
        'Length1': 25,  # глубина  первого сглаживания
        'Phase1': 15,  # параметр первого сглаживания,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения второго сглаживания
        'Length2': 3,  # глубина  второго сглаживания
        'Phase2': 15,  # параметр второго сглаживания,
        'MA_Method3': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения третьего сглаживания
        'Length3': 5,  # глубина  третьего сглаживания
        'Phase3': 15,  # параметр третьего сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'HighLevel': 50,
        'MiddleLevel': 0,
        'LowLevel': -50,
    }

