"""colorzerolagtrixosmacandle — converted from MQL5: MQL5 Indicators/ColorZerolagTriXOSMACandle/colorzerolagtrixosmacandle.mq5

ColorZerolagTriXOSMACandle
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 16711680, 8421376]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ColorZerolagTriXOSMACandle Open;High;Low;Close'}, 'levels': [], 'description': ['ColorZerolagTriXOSMACandle'], 'name': 'colorzerolagtrixosmacandle', 'source': 'MQL5 Indicators/ColorZerolagTriXOSMACandle/colorzerolagtrixosmacandle.mq5', 'folder': 'ColorZerolagTriXOSMACandle', 'inputs': [{'mql': 'smoothing1', 'py': 'smoothing1', 'param': 'smoothing1', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'smoothing2', 'py': 'smoothing2', 'param': 'smoothing2', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Factor1', 'py': 'Factor1', 'param': 'Factor1', 'type': 'double', 'default': 0.05, 'label': '', 'sinput': False}, {'mql': 'TriX_period1', 'py': 'TriX_period1', 'param': 'TriX_period1', 'type': 'uint', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Factor2', 'py': 'Factor2', 'param': 'Factor2', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'TriX_period2', 'py': 'TriX_period2', 'param': 'TriX_period2', 'type': 'uint', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Factor3', 'py': 'Factor3', 'param': 'Factor3', 'type': 'double', 'default': 0.16, 'label': '', 'sinput': False}, {'mql': 'TriX_period3', 'py': 'TriX_period3', 'param': 'TriX_period3', 'type': 'uint', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'Factor4', 'py': 'Factor4', 'param': 'Factor4', 'type': 'double', 'default': 0.26, 'label': '', 'sinput': False}, {'mql': 'TriX_period4', 'py': 'TriX_period4', 'param': 'TriX_period4', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Factor5', 'py': 'Factor5', 'param': 'Factor5', 'type': 'double', 'default': 0.43, 'label': '', 'sinput': False}, {'mql': 'TriX_period5', 'py': 'TriX_period5', 'param': 'TriX_period5', 'type': 'uint', 'default': 89, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
smoothing1 = _input('smoothing1', 5)
smoothing2 = _input('smoothing2', 5)
Factor1 = _input('Factor1', 0.05)
TriX_period1 = _input('TriX_period1', 8)
Factor2 = _input('Factor2', 0.1)
TriX_period2 = _input('TriX_period2', 21)
Factor3 = _input('Factor3', 0.16)
TriX_period3 = _input('TriX_period3', 34)
Factor4 = _input('Factor4', 0.26)
TriX_period4 = _input('TriX_period4', 55)
Factor5 = _input('Factor5', 0.43)
TriX_period5 = _input('TriX_period5', 89)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    PeriodBuffer = Arr(5, 0, dyn=False)
    PeriodBuffer[0] = TriX_period1
    PeriodBuffer[1] = TriX_period2
    PeriodBuffer[2] = TriX_period3
    PeriodBuffer[3] = TriX_period4
    PeriodBuffer[4] = TriX_period5
    min_rates_total = _int(3 * PeriodBuffer[ArrayMaximum(PeriodBuffer, 0, WHOLE_ARRAY)]) + 2
    Ind_Handle[0] = iCustom(None, 0, 'ColorZerolagTriXOSMA', smoothing1, smoothing2, PRICE_OPEN, Factor1, TriX_period1, Factor2, TriX_period2, Factor3, TriX_period3, Factor4, TriX_period4, Factor5, TriX_period5)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iColorZerolagTriXOSMA[' + _str(0) + ']!')
    Ind_Handle[1] = iCustom(None, 0, 'ColorZerolagTriXOSMA', smoothing1, smoothing2, PRICE_HIGH, Factor1, TriX_period1, Factor2, TriX_period2, Factor3, TriX_period3, Factor4, TriX_period4, Factor5, TriX_period5)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iColorZerolagTriXOSMA[' + _str(1) + ']!')
    Ind_Handle[2] = iCustom(None, 0, 'ColorZerolagTriXOSMA', smoothing1, smoothing2, PRICE_LOW, Factor1, TriX_period1, Factor2, TriX_period2, Factor3, TriX_period3, Factor4, TriX_period4, Factor5, TriX_period5)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iColorZerolagTriXOSMA[' + _str(2) + ']!')
    Ind_Handle[3] = iCustom(None, 0, 'ColorZerolagTriXOSMA', smoothing1, smoothing2, PRICE_CLOSE, Factor1, TriX_period1, Factor2, TriX_period2, Factor3, TriX_period3, Factor4, TriX_period4, Factor5, TriX_period5)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iColorZerolagTriXOSMA[' + _str(3) + ']!')
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    short_name = 'ColorZerolagTriXOSMACandl'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(Ind_Handle[0]) < rates_total or BarsCalculated(Ind_Handle[1]) < rates_total) or BarsCalculated(Ind_Handle[2]) < rates_total) or BarsCalculated(Ind_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorzerolagtrixosmacandle(_MQL5Indicator):
    name = 'colorzerolagtrixosmacandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'smoothing1': 5,
        'smoothing2': 5,
        'Factor1': 0.05,
        'TriX_period1': 8,
        'Factor2': 0.1,
        'TriX_period2': 21,
        'Factor3': 0.16,
        'TriX_period3': 34,
        'Factor4': 0.26,
        'TriX_period4': 55,
        'Factor5': 0.43,
        'TriX_period5': 89,
    }

