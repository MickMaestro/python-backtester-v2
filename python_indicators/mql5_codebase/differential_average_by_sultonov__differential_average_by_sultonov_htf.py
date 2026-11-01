"""Differential_Average_By_Sultonov — converted from MQL5: MQL5 Indicators/Differential_Average_By_Sultonov_HTF/Differential_Average_By_Sultonov.mq5

English: Sultonovs Differential Indicator
Russian: Дифференциальный индикатор Султонова
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16711680, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Differential_Average_By_Sultonov'}, 'levels': [], 'description': ['English: Sultonovs Differential Indicator', 'Russian: Дифференциальный индикатор Султонова'], 'name': 'Differential_Average_By_Sultonov', 'source': 'MQL5 Indicators/Differential_Average_By_Sultonov_HTF/Differential_Average_By_Sultonov.mq5', 'folder': 'Differential_Average_By_Sultonov_HTF', 'inputs': [{'mql': 'i_nPeriod', 'py': 'i_nPeriod', 'param': 'i_nPeriod', 'type': 'uint', 'default': 1000, 'label': 'Calculate period / Период расчета', 'sinput': False}, {'mql': 'XMethod', 'py': 'XMethod', 'param': 'XMethod', 'type': 'int', 'default': 0, 'label': 'метод усреднения сглаживания', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
i_nPeriod = _input('i_nPeriod', 1000)  # Calculate period / Период расчета
XMethod = _input('XMethod', MODE_SMA_)  # метод усреднения сглаживания
XLength = _input('XLength', 12)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
g_fPoint = 0.0
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global g_fPoint, min_rates_1, min_rates_total
    min_rates_1 = _int(i_nPeriod)
    min_rates_total = min_rates_1 + GetStartBars(XMethod, XLength, XPhase)
    g_fPoint = Point() / 10.0
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(XMethod)
    StringConcatenate(shortname, 'Differential_Average_By_Sultonov(', i_nPeriod, ', ', Smooth, ', ', XLength, ', ', XPhase, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        fBullsSumm = 0.0
        fBearsSumm = 0.0
        nBullsCnt = 0
        nBearsCnt = 0
        for index in range(0, _int(i_nPeriod)):
            fCloseCur = PriceSeries(IPC, bar - index, open, low, high, close)
            fClosePrev = PriceSeries(IPC, bar - index - 1, open, low, high, close)
            fPower = fCloseCur - fClosePrev
            if fPower > (2 * DBL_EPSILON):
                fBullsSumm += fPower
                nBullsCnt += 1
            if fPower < (-2 * DBL_EPSILON):
                fBearsSumm -= fPower
                nBearsCnt += 1
        farrBulls = (0.0 if (nBullsCnt == 0) else _fdiv(_fdiv(fBullsSumm, nBullsCnt), g_fPoint))
        farrBears = (0.0 if (nBearsCnt == 0) else _fdiv(_fdiv(fBearsSumm, nBearsCnt), g_fPoint))
        UpIndBuffer[bar] = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMethod, XPhase, XLength, farrBulls, bar, False)
        DnIndBuffer[bar] = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, XMethod, XPhase, XLength, farrBears, bar, False)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DifferentialAverageBySultonov(_MQL5Indicator):
    name = 'Differential_Average_By_Sultonov'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'i_nPeriod': 1000,  # Calculate period / Период расчета
        'XMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения сглаживания
        'XLength': 12,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

