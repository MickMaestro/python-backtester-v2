"""Dollar index — converted from MQL5: MQL5 Indicators/Dollar Index/Dollar index.mq5

Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Dollar index'}, 'levels': [], 'description': [], 'name': 'Dollar index', 'source': 'MQL5 Indicators/Dollar Index/Dollar index.mq5', 'folder': 'Dollar Index', 'inputs': [{'mql': 'inpBarsToCalculate', 'py': 'inpBarsToCalculate', 'param': 'inpBarsToCalculate', 'type': 'int', 'default': 500, 'label': 'Bars to calculate', 'sinput': False}, {'mql': 'inpSymbolsPrefix', 'py': 'inpSymbolsPrefix', 'param': None, 'type': 'string', 'default': '', 'label': 'Symbols prefix', 'sinput': False}, {'mql': 'inpSymbolsSuffix', 'py': 'inpSymbolsSuffix', 'param': None, 'type': 'string', 'default': '', 'label': 'Symbols suffix', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpBarsToCalculate = _input('inpBarsToCalculate', 500)  # Bars to calculate
inpSymbolsPrefix = _input('inpSymbolsPrefix', '')  # Symbols prefix
inpSymbolsSuffix = _input('inpSymbolsSuffix', '')  # Symbols suffix
ic = Arr(0, 0.0)
icolor = Arr(0, 0.0)
symbols = Arr.of(['EURUSD', 'USDJPY', 'GBPUSD', 'USDCAD', 'USDSEK', 'USDCHF'], fill="")
pows = Arr.of([-0.576, 0.136, -0.119, 0.091, 0.042, 0.036], fill=0.0)

def OnInit():
    SetIndexBuffer(0, ic)
    SetIndexBuffer(1, icolor, INDICATOR_COLOR_INDEX)
    for i in range(0, 6):
        symbols[i] = inpSymbolsPrefix + symbols[i] + inpSymbolsSuffix
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _bars = _int(MathMax(inpBarsToCalculate, ChartGetInteger(0, CHART_VISIBLE_BARS)))
    i = MathMax(prev_calculated - _bars + 1, 0)
    while i < rates_total:
        if i < (rates_total - _bars):
            ic[i] = EMPTY_VALUE
            icolor[i] = 0.0
            i += 1
            continue
        dxyClose = 50.14348112
        for k in range(0, 6):
            _rates = Arr(0, 0, factory=MqlRates)
            _ratesCopied = CopyRates(symbols[k], 0, _DT(time[i]), 1, _rates)
            if _ratesCopied == 1:
                dxyClose *= MathPow(_rates[0].close, pows[k])
        ic[i] = dxyClose
        icolor[i] = ((1 if (ic[i] > ic[i - 1]) else 2 if (ic[i] < ic[i - 1]) else 0) if (i > 0) else 0)
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DollarIndex(_MQL5Indicator):
    name = 'Dollar index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpBarsToCalculate': 500,  # Bars to calculate
    }

