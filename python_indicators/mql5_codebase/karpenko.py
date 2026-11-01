"""karpenko — converted from MQL5: MQL5 Indicators/Karpenko/karpenko.mq5

Karpenko
Copyright: Copyright © 2014, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [10025880, 12695295]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Karpenko'}, 'levels': [], 'description': ['Karpenko'], 'name': 'karpenko', 'source': 'MQL5 Indicators/Karpenko/karpenko.mq5', 'folder': 'Karpenko', 'inputs': [{'mql': 'Basic_MA', 'py': 'Basic_MA', 'param': 'Basic_MA', 'type': 'uint', 'default': 144, 'label': 'Период MA', 'sinput': False}, {'mql': 'History', 'py': 'History', 'param': 'History', 'type': 'uint', 'default': 500, 'label': 'Период истории', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Basic_MA = _input('Basic_MA', 144)  # Период MA
History = _input('History', 500)  # Период истории
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(MathMax(Basic_MA, History))
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Karpenko')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    sum_c = 0.0
    up = 0.0
    dw = 0.0
    base = 0.0
    limit = 0
    bar = 0
    k = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        k = 0
        sum_c = 0.0
        while k < _int(Basic_MA):
            sum_c += close[bar + k]
            k += 1
        base = sum_c / Basic_MA
        k = 0
        sum_c = 0.0
        while k < _int(History):
            sum_c += high[bar + k] - low[bar + k]
            k += 1
        up = sum_c / History
        dw = up
        Up = base
        while high[bar] > Up:
            up *= 1.618
            Up = base + up
        Dn = base
        while low[bar] < Dn:
            dw *= 1.618
            Dn = base - dw
        if base == Up:
            UpBuffer[bar] = base - dw
            DnBuffer[bar] = base
        else:
            UpBuffer[bar] = base + up
            DnBuffer[bar] = base
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Karpenko(_MQL5Indicator):
    name = 'karpenko'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Basic_MA': 144,  # Период MA
        'History': 500,  # Период истории
    }

