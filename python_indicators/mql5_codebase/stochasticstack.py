"""stochasticstack — converted from MQL5: MQL5 Indicators/StochasticStack/stochasticstack.mq5

StochasticStack
Copyright: Copyright © 2010, Ivan Kornilov; Link: E-mail: excelf@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Ivan Kornilov', 'link': 'E-mail: excelf@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2, 'indicator_minimum': -50.0, 'indicator_maximum': 50.0}, 'types': {1: 7, 2: 1}, 'colors': {1: [16711935, 16748574], 2: [9125192]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'StochasticStack', 2: 'StochasticStack Line'}, 'levels': [25.0, 0.0, -25.0], 'description': ['StochasticStack'], 'name': 'stochasticstack', 'source': 'MQL5 Indicators/StochasticStack/stochasticstack.mq5', 'folder': 'StochasticStack', 'inputs': [{'mql': 'nextPeriod', 'py': 'nextPeriod', 'param': 'nextPeriod', 'type': 'double', 'default': 1.2, 'label': '', 'sinput': False}, {'mql': 'kPeriod1', 'py': 'kPeriod1', 'param': 'kPeriod1', 'type': 'uint', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'level', 'py': 'level', 'param': 'level', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 1, 'label': 'smoothing type', 'sinput': False}, {'mql': 'price_field', 'py': 'price_field', 'param': 'price_field', 'type': 'int', 'default': 0, 'label': 'stochastic calculation method', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
nextPeriod = _input('nextPeriod', 1.2)
kPeriod1 = _input('kPeriod1', 34)
level = _input('level', 10)
ma_method = _input('ma_method', MODE_EMA)  # smoothing type
price_field = _input('price_field', STO_LOWHIGH)  # stochastic calculation method
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
Line1Buffer = Arr(0, 0.0)
Line2Buffer = Arr(0, 0.0)
Line3Buffer = Arr(0, 0.0)
Sto_Handle = Arr(8, 0, dyn=False)
min_rates_total = 0

def OnInit():
    global min_rates_total
    dPeriod1 = 0
    slowing1 = 0
    kPeriod2 = 0
    dPeriod2 = 0
    slowing2 = 0
    kPeriod3 = 0
    dPeriod3 = 0
    slowing3 = 0
    kPeriod4 = 0
    dPeriod4 = 0
    slowing4 = 0
    kPeriod5 = 0
    dPeriod5 = 0
    slowing5 = 0
    kPeriod6 = 0
    dPeriod6 = 0
    slowing6 = 0
    kPeriod7 = 0
    dPeriod7 = 0
    slowing7 = 0
    kPeriod8 = 0
    dPeriod8 = 0
    slowing8 = 0
    if nextPeriod:
        kPeriod2 = _int(kPeriod1 * nextPeriod)
        kPeriod3 = _int(kPeriod2 * nextPeriod)
        kPeriod4 = _int(kPeriod3 * nextPeriod)
        kPeriod5 = _int(kPeriod4 * nextPeriod)
        kPeriod6 = _int(kPeriod5 * nextPeriod)
        kPeriod7 = _int(kPeriod6 * nextPeriod)
        kPeriod8 = _int(kPeriod7 * nextPeriod)
    if (not dPeriod1) and (not slowing1):
        dPeriod1 = _int(_idiv(kPeriod1, 2))
        slowing1 = _idiv(dPeriod1, 2)
    if (not dPeriod2) and (not slowing2):
        dPeriod2 = _idiv(kPeriod2, 2)
        slowing2 = _idiv(dPeriod2, 2)
    if (not dPeriod3) and (not slowing3):
        dPeriod3 = _idiv(kPeriod3, 2)
        slowing3 = _idiv(dPeriod3, 2)
    if (not dPeriod4) and (not slowing4):
        dPeriod4 = _idiv(kPeriod4, 2)
        slowing4 = _idiv(dPeriod4, 2)
    if (not dPeriod5) and (not slowing5):
        dPeriod5 = _idiv(kPeriod5, 2)
        slowing5 = _idiv(dPeriod5, 2)
    if (not dPeriod6) and (not slowing6):
        dPeriod6 = _idiv(kPeriod6, 2)
        slowing6 = _idiv(dPeriod6, 2)
    if (not dPeriod7) and (not slowing7):
        dPeriod7 = _idiv(kPeriod7, 2)
        slowing7 = _idiv(dPeriod7, 2)
    if (not dPeriod8) and (not slowing8):
        dPeriod8 = _idiv(kPeriod8, 2)
        slowing8 = _idiv(dPeriod8, 2)
    min_rates_total = kPeriod8 + dPeriod8 + slowing8
    Sto_Handle[0] = iStochastic(None, 0, kPeriod1, dPeriod1, slowing1, ma_method, price_field)
    if Sto_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 1 indicator')
    Sto_Handle[1] = iStochastic(None, 0, kPeriod2, dPeriod2, slowing2, ma_method, price_field)
    if Sto_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 2 indicator')
    Sto_Handle[2] = iStochastic(None, 0, kPeriod3, dPeriod3, slowing3, ma_method, price_field)
    if Sto_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 3 indicator')
    Sto_Handle[3] = iStochastic(None, 0, kPeriod4, dPeriod4, slowing4, ma_method, price_field)
    if Sto_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 4 indicator')
    Sto_Handle[4] = iStochastic(None, 0, kPeriod5, dPeriod5, slowing5, ma_method, price_field)
    if Sto_Handle[4] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 5 indicator')
    Sto_Handle[5] = iStochastic(None, 0, kPeriod6, dPeriod6, slowing6, ma_method, price_field)
    if Sto_Handle[5] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 6 indicator')
    Sto_Handle[6] = iStochastic(None, 0, kPeriod7, dPeriod7, slowing7, ma_method, price_field)
    if Sto_Handle[6] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 7 indicator')
    Sto_Handle[7] = iStochastic(None, 0, kPeriod8, dPeriod8, slowing8, ma_method, price_field)
    if Sto_Handle[7] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 8 indicator')
    SetIndexBuffer(0, Line2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line2Buffer, True)
    SetIndexBuffer(1, Line3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line3Buffer, True)
    SetIndexBuffer(2, Line1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line1Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'StochasticStack(', DoubleToString(nextPeriod, 2), ', ', kPeriod1, ', ', level, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    for numb in range(0, 8):
        if BarsCalculated(Sto_Handle[numb]) < rates_total:
            return 0
    limit = 0
    to_copy = 0
    bar = 0
    sum_ = 0.0
    iSto1 = Arr(0, 0.0)
    iSto2 = Arr(0, 0.0)
    iSto3 = Arr(0, 0.0)
    iSto4 = Arr(0, 0.0)
    iSto5 = Arr(0, 0.0)
    iSto6 = Arr(0, 0.0)
    iSto7 = Arr(0, 0.0)
    iSto8 = Arr(0, 0.0)
    ArraySetAsSeries(iSto1, True)
    ArraySetAsSeries(iSto2, True)
    ArraySetAsSeries(iSto3, True)
    ArraySetAsSeries(iSto4, True)
    ArraySetAsSeries(iSto5, True)
    ArraySetAsSeries(iSto6, True)
    ArraySetAsSeries(iSto7, True)
    ArraySetAsSeries(iSto8, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Sto_Handle[0], MAIN_LINE, 0, to_copy, iSto1) <= 0:
        return 0
    if CopyBuffer(Sto_Handle[1], MAIN_LINE, 0, to_copy, iSto2) <= 0:
        return 0
    if CopyBuffer(Sto_Handle[2], MAIN_LINE, 0, to_copy, iSto3) <= 0:
        return 0
    if CopyBuffer(Sto_Handle[3], MAIN_LINE, 0, to_copy, iSto4) <= 0:
        return 0
    if CopyBuffer(Sto_Handle[4], MAIN_LINE, 0, to_copy, iSto5) <= 0:
        return 0
    if CopyBuffer(Sto_Handle[5], MAIN_LINE, 0, to_copy, iSto6) <= 0:
        return 0
    if CopyBuffer(Sto_Handle[6], MAIN_LINE, 0, to_copy, iSto7) <= 0:
        return 0
    if CopyBuffer(Sto_Handle[7], MAIN_LINE, 0, to_copy, iSto8) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        sum_ = 0.0
        sum_ += iSto1[bar] - iSto2[bar]
        sum_ += iSto3[bar] - iSto4[bar]
        sum_ += iSto5[bar] - iSto6[bar]
        sum_ += iSto7[bar] - iSto8[bar]
        Line1Buffer[bar] = sum_
        Line3Buffer[bar] = sum_
        Line2Buffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stochasticstack(_MQL5Indicator):
    name = 'stochasticstack'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'nextPeriod': 1.2,
        'kPeriod1': 34,
        'level': 10,
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # smoothing type
        'price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # stochastic calculation method
        'Shift': 0,  # horizontal shift of the indicator in bars
    }
    y_range = (-50.0, 50.0)

