"""RSI_X20 — converted from MQL5: MQL5 Indicators/RSI_X20/RSI_X20.mq5

Двадцать индикаторов RSI в одном окне
Copyright: Copyright © 2010, Ivan Kornilov; Link: excelf@gmail.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Ivan Kornilov', 'link': 'excelf@gmail.com', 'version': '1.10', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [70.0, 50.0, 30.0], 'description': ['Двадцать индикаторов RSI в одном окне'], 'name': 'RSI_X20', 'source': 'MQL5 Indicators/RSI_X20/RSI_X20.mq5', 'folder': 'RSI_X20', 'inputs': [{'mql': 'StartRSIPeriod', 'py': 'StartRSIPeriod', 'param': 'StartRSIPeriod', 'type': 'uint', 'default': 5, 'label': 'стартовый период', 'sinput': False}, {'mql': 'step', 'py': 'step', 'param': 'step', 'type': 'uint', 'default': 1, 'label': 'шаг периода', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'цена', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StartRSIPeriod = _input('StartRSIPeriod', 5)  # стартовый период
step = _input('step', 1)  # шаг периода
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # цена
Ind_Handle = Arr(20, 0, dyn=False)
min_rates_total = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(StartRSIPeriod + (step * (20 - 1))) + 1
    Maxrange = StartRSIPeriod + (20 * (step - 1 + 1) * 2)
    period = StartRSIPeriod
    for numb in range(0, 20):
        period += step
        Ind_Handle[numb] = iRSI(Symbol(), 0, period, RSIPrice)
        if Ind_Handle[numb] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора iRSI ', numb)
        shortname = Box('')
        StringConcatenate(shortname, 'iRSI X', 20, '*', period, ')')
        PlotIndexSetString(numb, PLOT_LABEL, shortname.v)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb, PLOT_DRAW_BEGIN, min_rates_total)
        SetIndexBuffer(numb, Ind[numb].IndBuffer, INDICATOR_DATA)
        ArraySetAsSeries(Ind[numb].IndBuffer, True)
        PlotIndexSetInteger(numb, PLOT_DRAW_TYPE, PlotIndexGetInteger(0, PLOT_DRAW_TYPE))
        PlotIndexSetInteger(numb, PLOT_LINE_STYLE, PlotIndexGetInteger(0, PLOT_LINE_STYLE))
        PlotIndexSetInteger(numb, PLOT_LINE_WIDTH, PlotIndexGetInteger(0, PLOT_LINE_WIDTH))
        PlotIndexSetInteger(numb, PLOT_LINE_COLOR, PlotIndexGetInteger(0, PLOT_LINE_COLOR))
        PlotIndexSetInteger(numb, PLOT_SHOW_DATA, False)
    shortname = Box("")
    StringConcatenate(shortname, 'iRSI X', 20, '*', StartRSIPeriod, '(', step, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    for numb in range(0, 20):
        if BarsCalculated(Ind_Handle[numb]) < min_rates_total:
            return 0
    for numb in range(0, 20):
        if BarsCalculated(Ind_Handle[numb]) < rates_total:
            return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
    for numb in range(0, 20):
        if CopyBuffer(Ind_Handle[numb], 0, 0, to_copy, Ind[numb].IndBuffer) <= 0:
            return 0
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(20, 0, dyn=False, factory=CIndicatorsBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIX20(_MQL5Indicator):
    name = 'RSI_X20'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartRSIPeriod': 5,  # стартовый период
        'step': 1,  # шаг периода
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # цена
    }
    y_range = (0.0, 100.0)

