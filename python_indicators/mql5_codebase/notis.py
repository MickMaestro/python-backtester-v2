"""Notis — converted from MQL5: MQL5 Indicators/Notis/Notis.mq5

Notis% V indicators
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Plus', 2: 'Minus', 3: 'Notis'}, 'levels': [], 'description': ['Notis% V indicators'], 'name': 'Notis', 'source': 'MQL5 Indicators/Notis/Notis.mq5', 'folder': 'Notis', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpCumulative', 'py': 'InpCumulative', 'param': 'InpCumulative', 'type': 'int', 'default': 0, 'label': 'Cumulative mode', 'sinput': False}, {'mql': 'InpInverse', 'py': 'InpInverse', 'param': 'InpInverse', 'type': 'int', 'default': 0, 'label': 'Inverse in cumulative mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpCumulative = _input('InpCumulative', INPUT_NO)  # Cumulative mode
InpInverse = _input('InpInverse', INPUT_NO)  # Inverse in cumulative mode
BufferPlus = Arr(0, 0.0)
BufferMinus = Arr(0, 0.0)
BufferNotis = Arr(0, 0.0)
BufferP = Arr(0, 0.0)
BufferM = Arr(0, 0.0)
period_ind = 0
weight_sum = 0

def OnInit():
    global period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferPlus, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMinus, INDICATOR_DATA)
    SetIndexBuffer(2, BufferNotis, INDICATOR_DATA)
    SetIndexBuffer(3, BufferP, INDICATOR_DATA)
    SetIndexBuffer(4, BufferM, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Notis (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPlus, True)
    ArraySetAsSeries(BufferMinus, True)
    ArraySetAsSeries(BufferNotis, True)
    ArraySetAsSeries(BufferP, True)
    ArraySetAsSeries(BufferM, True)
    if InpCumulative:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
        PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
        PlotIndexSetInteger(2, PLOT_SHOW_DATA, True)
        ChartRedraw()
    else:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(0, PLOT_SHOW_DATA, True)
        PlotIndexSetInteger(1, PLOT_SHOW_DATA, True)
        PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
        ChartRedraw()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferPlus, EMPTY_VALUE)
        ArrayInitialize(BufferMinus, EMPTY_VALUE)
        ArrayInitialize(BufferNotis, EMPTY_VALUE)
        ArrayInitialize(BufferP, 0)
        ArrayInitialize(BufferM, 0)
    for i in range(limit, 0 - 1, -1):
        BufferP[i] = high[i] - close[i]
        BufferM[i] = close[i] - low[i]
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferP, BufferPlus)
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferM, BufferMinus)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferP, BufferPlus)
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferM, BufferMinus)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferP, BufferPlus, _GlobRef(globals(), 'weight_sum'))
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferM, BufferMinus, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferP, BufferPlus)
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferM, BufferMinus)
    for i in range(limit, 0 - 1, -1):
        Plus = BufferPlus[i]
        Minus = BufferMinus[i]
        if InpCumulative and (Plus + Minus) > 0:
            BufferNotis[i] = _fdiv(100.0 * Plus, Plus + Minus)
            if InpInverse:
                BufferNotis[i] = 100 - BufferNotis[i]
        else:
            BufferNotis[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Notis(_MQL5Indicator):
    name = 'Notis'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpCumulative': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Cumulative mode
        'InpInverse': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Inverse in cumulative mode
    }

