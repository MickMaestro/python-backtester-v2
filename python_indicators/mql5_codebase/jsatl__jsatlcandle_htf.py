"""JSatl — converted from MQL5: MQL5 Indicators/JSatlCandle_HTF/JSatl.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9639167]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'JSatl'}, 'levels': [], 'description': [], 'name': 'JSatl', 'source': 'MQL5 Indicators/JSatlCandle_HTF/JSatl.mq5', 'folder': 'JSatlCandle_HTF', 'inputs': [{'mql': 'iLength', 'py': 'iLength', 'param': 'iLength', 'type': 'uint', 'default': 5, 'label': 'глубина JMA сглаживания', 'sinput': False}, {'mql': 'iPhase', 'py': 'iPhase', 'param': 'iPhase', 'type': 'int', 'default': 100, 'label': 'параметр JMA сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'SATLShift', 'py': 'SATLShift', 'param': 'SATLShift', 'type': 'int', 'default': 0, 'label': 'сдвиг Фатла по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг Фатла по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
iLength = _input('iLength', 5)  # глубина JMA сглаживания
iPhase = _input('iPhase', 100)  # параметр JMA сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
SATLShift = _input('SATLShift', 0)  # сдвиг Фатла по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг Фатла по вертикали в пунктах
SATLPeriod = 65
ExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0
fstart = 0
SATLSize = 0
dPriceShift = 0.0

def OnInit():
    global dPriceShift, min_rates_total
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, SATLShift)
    min_rates_total = SATLSize + 30
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'JSatl(', iLength, ' ,', iPhase, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    dPriceShift = Point() * PriceShift
    JMA.JJMALengthCheck('iLength', iLength)
    JMA.JJMAPhaseCheck('iPhase', iPhase)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global fstart
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    satl = 0.0
    jsatl = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = SATLPeriod - 1
        fstart = first
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        satl = STL.SATLSeries(0, prev_calculated, rates_total, price, bar, False)
        jsatl = JMA.JJMASeries(fstart, prev_calculated, rates_total, 0, iPhase, iLength, satl, bar, False)
        ExtLineBuffer[bar] = jsatl + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
JMA = _alloc(CJJMA)
JMA.__init__()
STL = _alloc(CSATL)
STL.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JSatl(_MQL5Indicator):
    name = 'JSatl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iLength': 5,  # глубина JMA сглаживания
        'iPhase': 100,  # параметр JMA сглаживания,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'SATLShift': 0,  # сдвиг Фатла по горизонтали в барах
        'PriceShift': 0,  # cдвиг Фатла по вертикали в пунктах
    }

