"""colorzerolagstochs — converted from MQL5: MQL5 Indicators/ZerolagStochs/colorzerolagstochs.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 7}, 'colors': {1: [8388352], 2: [14822282], 3: [16711680, 255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'FastTrendLine', 2: 'SlowTrendLine', 3: 'ZerolagStochs'}, 'levels': [], 'description': [], 'name': 'colorzerolagstochs', 'source': 'MQL5 Indicators/ZerolagStochs/colorzerolagstochs.mq5', 'folder': 'ZerolagStochs', 'inputs': [{'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'smoothing', 'py': 'smoothing', 'param': 'smoothing', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Factor1', 'py': 'Factor1', 'param': 'Factor1', 'type': 'double', 'default': 0.05, 'label': '', 'sinput': False}, {'mql': 'Kperiod1', 'py': 'Kperiod1', 'param': 'Kperiod1', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Dperiod1', 'py': 'Dperiod1', 'param': 'Dperiod1', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Factor2', 'py': 'Factor2', 'param': 'Factor2', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Kperiod2', 'py': 'Kperiod2', 'param': 'Kperiod2', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Dperiod2', 'py': 'Dperiod2', 'param': 'Dperiod2', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Factor3', 'py': 'Factor3', 'param': 'Factor3', 'type': 'double', 'default': 0.16, 'label': '', 'sinput': False}, {'mql': 'Kperiod3', 'py': 'Kperiod3', 'param': 'Kperiod3', 'type': 'int', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'Dperiod3', 'py': 'Dperiod3', 'param': 'Dperiod3', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Factor4', 'py': 'Factor4', 'param': 'Factor4', 'type': 'double', 'default': 0.26, 'label': '', 'sinput': False}, {'mql': 'Kperiod4', 'py': 'Kperiod4', 'param': 'Kperiod4', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Dperiod4', 'py': 'Dperiod4', 'param': 'Dperiod4', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'Factor5', 'py': 'Factor5', 'param': 'Factor5', 'type': 'double', 'default': 0.43, 'label': '', 'sinput': False}, {'mql': 'Kperiod5', 'py': 'Kperiod5', 'param': 'Kperiod5', 'type': 'int', 'default': 89, 'label': '', 'sinput': False}, {'mql': 'Dperiod5', 'py': 'Dperiod5', 'param': 'Dperiod5', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Slowing = _input('Slowing', 3)
smoothing = _input('smoothing', 15)
MA_Method = _input('MA_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
Factor1 = _input('Factor1', 0.05)
Kperiod1 = _input('Kperiod1', 8)
Dperiod1 = _input('Dperiod1', 3)
Factor2 = _input('Factor2', 0.1)
Kperiod2 = _input('Kperiod2', 21)
Dperiod2 = _input('Dperiod2', 5)
Factor3 = _input('Factor3', 0.16)
Kperiod3 = _input('Kperiod3', 34)
Dperiod3 = _input('Dperiod3', 8)
Factor4 = _input('Factor4', 0.26)
Kperiod4 = _input('Kperiod4', 55)
Dperiod4 = _input('Dperiod4', 13)
Factor5 = _input('Factor5', 0.43)
Kperiod5 = _input('Kperiod5', 89)
Dperiod5 = _input('Dperiod5', 21)
StartBar = 0
smoothConst = 0.0
FastBuffer = Arr(0, 0.0)
SlowBuffer = Arr(0, 0.0)
FastBuffer_ = Arr(0, 0.0)
SlowBuffer_ = Arr(0, 0.0)
STO1_Handle = 0
STO2_Handle = 0
STO3_Handle = 0
STO4_Handle = 0
STO5_Handle = 0

def OnInit():
    global STO1_Handle, STO2_Handle, STO3_Handle, STO4_Handle, STO5_Handle, StartBar, smoothConst
    smoothConst = (smoothing - 1.0) / smoothing
    PeriodBuffer = Arr(5, 0, dyn=False)
    PeriodBuffer[0] = Kperiod1 + Dperiod1
    PeriodBuffer[1] = Kperiod2 + Dperiod2
    PeriodBuffer[2] = Kperiod3 + Dperiod3
    PeriodBuffer[3] = Kperiod4 + Dperiod4
    PeriodBuffer[4] = Kperiod5 + Dperiod5
    StartBar = PeriodBuffer[ArrayMaximum(PeriodBuffer, 0, WHOLE_ARRAY)] + 1
    STO1_Handle = iStochastic(None, 0, Kperiod1, Dperiod1, Slowing, MA_Method, Price_field)
    if STO1_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic1 indicator')
    STO2_Handle = iStochastic(None, 0, Kperiod2, Dperiod2, Slowing, MA_Method, Price_field)
    if STO2_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic2 indicator')
    STO3_Handle = iStochastic(None, 0, Kperiod3, Dperiod3, Slowing, MA_Method, Price_field)
    if STO3_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic3 indicator')
    STO4_Handle = iStochastic(None, 0, Kperiod4, Dperiod4, Slowing, MA_Method, Price_field)
    if STO4_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic4 indicator')
    STO5_Handle = iStochastic(None, 0, Kperiod5, Dperiod5, Slowing, MA_Method, Price_field)
    if STO5_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic5 indicator')
    SetIndexBuffer(0, FastBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBar)
    PlotIndexSetString(0, PLOT_LABEL, 'FastTrendLine')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(FastBuffer, True)
    SetIndexBuffer(1, SlowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBar)
    PlotIndexSetString(1, PLOT_LABEL, 'SlowTrendLine')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SlowBuffer, True)
    SetIndexBuffer(2, FastBuffer_, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBar)
    PlotIndexSetString(2, PLOT_LABEL, 'FastTrendLine')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(FastBuffer_, True)
    SetIndexBuffer(3, SlowBuffer_, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBar)
    PlotIndexSetString(3, PLOT_LABEL, 'SlowTrendLine')
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SlowBuffer_, True)
    shortname = 'ZerolagStochs'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(STO1_Handle) < rates_total or BarsCalculated(STO2_Handle) < rates_total) or BarsCalculated(STO3_Handle) < rates_total) or BarsCalculated(STO4_Handle) < rates_total) or BarsCalculated(STO5_Handle) < rates_total) or rates_total < StartBar:
        return 0
    Sto1 = 0.0
    Sto2 = 0.0
    Sto3 = 0.0
    Sto4 = 0.0
    Sto5 = 0.0
    FastTrend = 0.0
    SlowTrend = 0.0
    Stoch1 = Arr(0, 0.0)
    Stoch2 = Arr(0, 0.0)
    Stoch3 = Arr(0, 0.0)
    Stoch4 = Arr(0, 0.0)
    Stoch5 = Arr(0, 0.0)
    limit = 0
    to_copy = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBar - 2
        to_copy = rates_total
    else:
        limit = rates_total - prev_calculated
        to_copy = rates_total - prev_calculated + 1
    ArraySetAsSeries(Stoch1, True)
    ArraySetAsSeries(Stoch2, True)
    ArraySetAsSeries(Stoch3, True)
    ArraySetAsSeries(Stoch4, True)
    ArraySetAsSeries(Stoch5, True)
    if CopyBuffer(STO1_Handle, 0, 0, to_copy, Stoch1) <= 0:
        return 0
    if CopyBuffer(STO2_Handle, 0, 0, to_copy, Stoch2) <= 0:
        return 0
    if CopyBuffer(STO3_Handle, 0, 0, to_copy, Stoch3) <= 0:
        return 0
    if CopyBuffer(STO4_Handle, 0, 0, to_copy, Stoch4) <= 0:
        return 0
    if CopyBuffer(STO5_Handle, 0, 0, to_copy, Stoch5) <= 0:
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        Sto1 = Factor1 * Stoch1[limit + 1]
        Sto2 = Factor2 * Stoch2[limit + 1]
        Sto3 = Factor2 * Stoch3[limit + 1]
        Sto4 = Factor4 * Stoch4[limit + 1]
        Sto5 = Factor5 * Stoch5[limit + 1]
        FastTrend = Sto1 + Sto2 + Sto3 + Sto4 + Sto5
        FastBuffer[limit + 1] = FastTrend
        FastBuffer_[limit + 1] = FastTrend
        SlowBuffer[limit + 1] = FastTrend / smoothing
        SlowBuffer_[limit + 1] = SlowBuffer[limit + 1]
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Sto1 = Factor1 * Stoch1[bar]
        Sto2 = Factor2 * Stoch2[bar]
        Sto3 = Factor2 * Stoch3[bar]
        Sto4 = Factor4 * Stoch4[bar]
        Sto5 = Factor5 * Stoch5[bar]
        FastTrend = Sto1 + Sto2 + Sto3 + Sto4 + Sto5
        SlowTrend = (FastTrend / smoothing) + (SlowBuffer[bar + 1] * smoothConst)
        SlowBuffer[bar] = SlowTrend
        FastBuffer[bar] = FastTrend
        SlowBuffer_[bar] = SlowTrend
        FastBuffer_[bar] = FastTrend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorzerolagstochs(_MQL5Indicator):
    name = 'colorzerolagstochs'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Slowing': 3,
        'smoothing': 15,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'Factor1': 0.05,
        'Kperiod1': 8,
        'Dperiod1': 3,
        'Factor2': 0.1,
        'Kperiod2': 21,
        'Dperiod2': 5,
        'Factor3': 0.16,
        'Kperiod3': 34,
        'Dperiod3': 8,
        'Factor4': 0.26,
        'Kperiod4': 55,
        'Dperiod4': 13,
        'Factor5': 0.43,
        'Kperiod5': 89,
        'Dperiod5': 21,
    }

