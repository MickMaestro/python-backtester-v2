"""stochasticrsi — converted from MQL5: MQL5 Indicators/Stochastic RSI/stochasticrsi.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Stochastic RSI', 2: 'Trigger'}, 'levels': [0.7, 0.5, 0.3], 'description': [], 'name': 'stochasticrsi', 'source': 'MQL5 Indicators/Stochastic RSI/stochasticrsi.mq5', 'folder': 'Stochastic RSI', 'inputs': [{'mql': 'RSILength', 'py': 'RSILength', 'param': 'RSILength', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'StocLength', 'py': 'StocLength', 'param': 'StocLength', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'WMALength', 'py': 'WMALength', 'param': 'WMALength', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
RSILength = _input('RSILength', 8)
StocLength = _input('StocLength', 8)
WMALength = _input('WMALength', 8)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
StoRSIBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
RSI_Handle = 0
rsi_rates_total = 0
sto_rates_total = 0
min_rates_total = 0

def OnInit():
    global RSI_Handle, min_rates_total, rsi_rates_total, sto_rates_total
    rsi_rates_total = RSILength
    sto_rates_total = rsi_rates_total + StocLength
    min_rates_total = sto_rates_total + WMALength + 1
    RSI_Handle = iRSI(None, 0, RSILength, PRICE_CLOSE)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the RSI indicator')
    SetIndexBuffer(0, StoRSIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(StoRSIBuffer, True)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    ArraySetAsSeries(TriggerBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Stochastic RSI(', RSILength, ', ', StocLength, ', ', WMALength, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(RSI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    maxbar = 0
    bar = 0
    tmp = 0.0
    hh = 0.0
    ll = 0.0
    Value1 = 0.0
    Value2 = 0.0
    Value3 = 0.0
    RSI = Arr(0, 0.0)
    ArraySetAsSeries(RSI, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - rsi_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + min_rates_total + 1
    maxbar = rates_total - 1 - sto_rates_total
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        hh = RSI[bar]
        ll = RSI[bar]
        for iii in range(0, StocLength):
            tmp = RSI[bar + iii]
            hh = MathMax(hh, tmp)
            ll = MathMin(ll, tmp)
        Value1 = RSI[bar] - ll
        Value2 = hh - ll
        if Value2 != 0.0:
            Value3 = _fdiv(Value1, Value2)
        else:
            Value3 = 0.0
        StoRSIBuffer[bar] = _s_OnCalculate_MA.MASeries(maxbar, prev_calculated, rates_total, WMALength, MODE_LWMA, Value3, bar, True)
        TriggerBuffer[bar] = StoRSIBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_MA = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stochasticrsi(_MQL5Indicator):
    name = 'stochasticrsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSILength': 8,
        'StocLength': 8,
        'WMALength': 8,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }
    y_range = (0.0, 1.0)

