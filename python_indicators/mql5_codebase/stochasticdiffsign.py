"""stochasticdiffsign — converted from MQL5: MQL5 Indicators/StochasticDiffSign/stochasticdiffsign.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [3329330]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'StochasticDiffSign Sell', 2: 'StochasticDiffSign Buy'}, 'levels': [], 'description': [], 'name': 'stochasticdiffsign', 'source': 'MQL5 Indicators/StochasticDiffSign/stochasticdiffsign.mq5', 'folder': 'StochasticDiffSign', 'inputs': [{'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'iMA_Method', 'py': 'iMA_Method', 'param': 'iMA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'метод сглаживания индикатора', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 13, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
iMA_Method = _input('iMA_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
XMA_Method = _input('XMA_Method', MODE_T3)  # метод сглаживания индикатора
XLength = _input('XLength', 13)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
min_rates_1 = 0
min_rates_total = 0
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
Stochastic_Handle = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, Stochastic_Handle, min_rates_1, min_rates_total
    ATR_Period = 15
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iATR')
        return INIT_FAILED
    Stochastic_Handle = iStochastic(None, 0, KPeriod, DPeriod, Slowing, iMA_Method, Price_field)
    if Stochastic_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iStochastic')
        return INIT_FAILED
    min_rates_1 = KPeriod + DPeriod + Slowing
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method, XLength, XPhase) + 3
    min_rates_total = MathMax(ATR_Period, min_rates_total) + 1
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_ARROW, 176)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 176)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'StochasticDiffSign(' + _str(KPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_xdiff1, _s_OnCalculate_xdiff2
    if (BarsCalculated(Stochastic_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    Sto = Arr(0, 0.0)
    Sign = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    diff = 0.0
    xdiff = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_1 - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    maxbar = rates_total - 1 - min_rates_1
    if CopyBuffer(Stochastic_Handle, MAIN_LINE, 0, to_copy, Sto) <= 0:
        return 0
    if CopyBuffer(Stochastic_Handle, SIGNAL_LINE, 0, to_copy, Sign) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, MAIN_LINE, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(Sto, True)
    ArraySetAsSeries(Sign, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        diff = Sto[bar] - Sign[bar]
        xdiff = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, diff, bar, True)
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_xdiff2 > _s_OnCalculate_xdiff1 and _s_OnCalculate_xdiff1 < xdiff:
            BuyBuffer[bar] = Low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_xdiff2 < _s_OnCalculate_xdiff1 and _s_OnCalculate_xdiff1 > xdiff:
            SellBuffer[bar] = High[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_xdiff2 = _s_OnCalculate_xdiff1
            _s_OnCalculate_xdiff1 = xdiff
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_OnCalculate_xdiff1 = 0.0
_s_OnCalculate_xdiff2 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stochasticdiffsign(_MQL5Indicator):
    name = 'stochasticdiffsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'iMA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод сглаживания индикатора
        'XLength': 13,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
    }

