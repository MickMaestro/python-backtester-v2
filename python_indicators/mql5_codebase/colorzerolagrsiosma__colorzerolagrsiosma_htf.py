"""colorzerolagrsiosma — converted from MQL5: MQL5 Indicators/ColorZerolagRSIOSMA_HTF/colorzerolagrsiosma.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [9639167, 42495, 8421504, 3329434, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ColorZerolagRSIOSMA'}, 'levels': [], 'description': [], 'name': 'colorzerolagrsiosma', 'source': 'MQL5 Indicators/ColorZerolagRSIOSMA_HTF/colorzerolagrsiosma.mq5', 'folder': 'ColorZerolagRSIOSMA_HTF', 'inputs': [{'mql': 'smoothing1', 'py': 'smoothing1', 'param': 'smoothing1', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'smoothing2', 'py': 'smoothing2', 'param': 'smoothing2', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Factor1', 'py': 'Factor1', 'param': 'Factor1', 'type': 'double', 'default': 0.05, 'label': '', 'sinput': False}, {'mql': 'RSI_period1', 'py': 'RSI_period1', 'param': 'RSI_period1', 'type': 'uint', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Factor2', 'py': 'Factor2', 'param': 'Factor2', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'RSI_period2', 'py': 'RSI_period2', 'param': 'RSI_period2', 'type': 'uint', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Factor3', 'py': 'Factor3', 'param': 'Factor3', 'type': 'double', 'default': 0.16, 'label': '', 'sinput': False}, {'mql': 'RSI_period3', 'py': 'RSI_period3', 'param': 'RSI_period3', 'type': 'uint', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'Factor4', 'py': 'Factor4', 'param': 'Factor4', 'type': 'double', 'default': 0.26, 'label': '', 'sinput': False}, {'mql': 'RSI_period4', 'py': 'RSI_period4', 'param': 'RSI_period4', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Factor5', 'py': 'Factor5', 'param': 'Factor5', 'type': 'double', 'default': 0.43, 'label': '', 'sinput': False}, {'mql': 'RSI_period5', 'py': 'RSI_period5', 'param': 'RSI_period5', 'type': 'uint', 'default': 89, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
smoothing1 = _input('smoothing1', 15)
smoothing2 = _input('smoothing2', 7)
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Factor1 = _input('Factor1', 0.05)
RSI_period1 = _input('RSI_period1', 8)
Factor2 = _input('Factor2', 0.1)
RSI_period2 = _input('RSI_period2', 21)
Factor3 = _input('Factor3', 0.16)
RSI_period3 = _input('RSI_period3', 34)
Factor4 = _input('Factor4', 0.26)
RSI_period4 = _input('RSI_period4', 55)
Factor5 = _input('Factor5', 0.43)
RSI_period5 = _input('RSI_period5', 89)
min_rates_total = 0
smoothConst1 = 0.0
smoothConst2 = 0.0
ExtBuffer = Arr(0, 0.0)
ColorExtBuffer = Arr(0, 0.0)
RSI1_Handle = 0
RSI2_Handle = 0
RSI3_Handle = 0
RSI4_Handle = 0
RSI5_Handle = 0

def OnInit():
    global RSI1_Handle, RSI2_Handle, RSI3_Handle, RSI4_Handle, RSI5_Handle, min_rates_total, smoothConst1, smoothConst2
    smoothConst1 = (smoothing1 - 1.0) / smoothing1
    smoothConst2 = (smoothing2 - 1.0) / smoothing2
    PeriodBuffer = Arr(5, 0, dyn=False)
    PeriodBuffer[0] = RSI_period1
    PeriodBuffer[1] = RSI_period2
    PeriodBuffer[2] = RSI_period3
    PeriodBuffer[3] = RSI_period4
    PeriodBuffer[4] = RSI_period5
    min_rates_total = _int(3 * PeriodBuffer[ArrayMaximum(PeriodBuffer, 0, WHOLE_ARRAY)]) + 2
    RSI1_Handle = iRSI(None, 0, RSI_period1, IPC)
    if RSI1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI1')
        return INIT_FAILED
    RSI2_Handle = iRSI(None, 0, RSI_period2, IPC)
    if RSI2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI2')
        return INIT_FAILED
    RSI3_Handle = iRSI(None, 0, RSI_period3, IPC)
    if RSI3_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI3')
        return INIT_FAILED
    RSI4_Handle = iRSI(None, 0, RSI_period4, IPC)
    if RSI4_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI4')
        return INIT_FAILED
    RSI5_Handle = iRSI(None, 0, RSI_period5, IPC)
    if RSI5_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI5')
        return INIT_FAILED
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, ColorExtBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorExtBuffer, True)
    shortname = 'ColorZerolagRSIOSMA'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_OSMA1, _s_OnCalculate_SlowTrend1
    if ((((BarsCalculated(RSI1_Handle) < rates_total or BarsCalculated(RSI2_Handle) < rates_total) or BarsCalculated(RSI3_Handle) < rates_total) or BarsCalculated(RSI4_Handle) < rates_total) or BarsCalculated(RSI5_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    Osc1 = 0.0
    Osc2 = 0.0
    Osc3 = 0.0
    Osc4 = 0.0
    Osc5 = 0.0
    FastTrend = 0.0
    SlowTrend = 0.0
    OSMA = 0.0
    diff = 0.0
    RSI1 = Arr(0, 0.0)
    RSI2 = Arr(0, 0.0)
    RSI3 = Arr(0, 0.0)
    RSI4 = Arr(0, 0.0)
    RSI5 = Arr(0, 0.0)
    limit = 0
    to_copy = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 2
        to_copy = limit + 2
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    ArraySetAsSeries(RSI1, True)
    ArraySetAsSeries(RSI2, True)
    ArraySetAsSeries(RSI3, True)
    ArraySetAsSeries(RSI4, True)
    ArraySetAsSeries(RSI5, True)
    if CopyBuffer(RSI1_Handle, 0, 0, to_copy, RSI1) <= 0:
        return 0
    if CopyBuffer(RSI2_Handle, 0, 0, to_copy, RSI2) <= 0:
        return 0
    if CopyBuffer(RSI3_Handle, 0, 0, to_copy, RSI3) <= 0:
        return 0
    if CopyBuffer(RSI4_Handle, 0, 0, to_copy, RSI4) <= 0:
        return 0
    if CopyBuffer(RSI5_Handle, 0, 0, to_copy, RSI5) <= 0:
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        bar = limit + 1
        Osc1 = Factor1 * RSI1[bar]
        Osc2 = Factor2 * RSI2[bar]
        Osc3 = Factor2 * RSI3[bar]
        Osc4 = Factor4 * RSI4[bar]
        Osc5 = Factor5 * RSI5[bar]
        FastTrend = Osc1 + Osc2 + Osc3 + Osc4 + Osc5
        _s_OnCalculate_SlowTrend1 = FastTrend / smoothing1
        _s_OnCalculate_OSMA1 = (FastTrend - _s_OnCalculate_SlowTrend1) / smoothing2
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Osc1 = Factor1 * RSI1[bar]
        Osc2 = Factor2 * RSI2[bar]
        Osc3 = Factor2 * RSI3[bar]
        Osc4 = Factor4 * RSI4[bar]
        Osc5 = Factor5 * RSI5[bar]
        FastTrend = Osc1 + Osc2 + Osc3 + Osc4 + Osc5
        SlowTrend = (FastTrend / smoothing1) + (_s_OnCalculate_SlowTrend1 * smoothConst1)
        OSMA = ((FastTrend - SlowTrend) / smoothing2) + (_s_OnCalculate_OSMA1 * smoothConst2)
        ExtBuffer[bar] = OSMA
        if bar:
            _s_OnCalculate_SlowTrend1 = SlowTrend
            _s_OnCalculate_OSMA1 = OSMA
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        diff = ExtBuffer[bar] - ExtBuffer[bar + 1]
        if ExtBuffer[bar] > 0:
            if diff > 0:
                clr = 4
            if diff < 0:
                clr = 3
        if ExtBuffer[bar] < 0:
            if diff < 0:
                clr = 0
            if diff > 0:
                clr = 1
        ColorExtBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_SlowTrend1 = 0.0
_s_OnCalculate_OSMA1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorzerolagrsiosma(_MQL5Indicator):
    name = 'colorzerolagrsiosma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'smoothing1': 15,
        'smoothing2': 7,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Ценовая константа
        'Factor1': 0.05,
        'RSI_period1': 8,
        'Factor2': 0.1,
        'RSI_period2': 21,
        'Factor3': 0.16,
        'RSI_period3': 34,
        'Factor4': 0.26,
        'RSI_period4': 55,
        'Factor5': 0.43,
        'RSI_period5': 89,
    }

