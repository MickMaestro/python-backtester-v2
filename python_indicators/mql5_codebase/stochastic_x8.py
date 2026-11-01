"""stochastic-x8 — converted from MQL5: MQL5 Indicators/Stochastic-X8/stochastic-x8.mq5

Stochastic-X8
Copyright: Copyright © 2010, lukas1; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, lukas1', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Stochastic-X8'], 'name': 'stochastic-x8', 'source': 'MQL5 Indicators/Stochastic-X8/stochastic-x8.mq5', 'folder': 'Stochastic-X8', 'inputs': [{'mql': 'Stoch_K', 'py': 'Stoch_K', 'param': 'Stoch_K', 'type': 'int', 'default': 12, 'label': 'the K period (the number of bars) for %K line calculation', 'sinput': False}, {'mql': 'Stoch_D', 'py': 'Stoch_D', 'param': 'Stoch_D', 'type': 'int', 'default': 8, 'label': 'smoothing period for %D line calculation', 'sinput': False}, {'mql': 'Stoch_S', 'py': 'Stoch_S', 'param': 'Stoch_S', 'type': 'int', 'default': 5, 'label': 'Deceleration value', 'sinput': False}, {'mql': 'Koef', 'py': 'Koef', 'param': 'Koef', 'type': 'double', 'default': 1.2, 'label': 'Periods additional multiplying ratio', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 3, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'price_field', 'py': 'price_field', 'param': 'price_field', 'type': 'int', 'default': 1, 'label': 'Stochastic calculation method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Stoch_K = _input('Stoch_K', 12)  # the K period (the number of bars) for %K line calculation
Stoch_D = _input('Stoch_D', 8)  # smoothing period for %D line calculation
Stoch_S = _input('Stoch_S', 5)  # Deceleration value
Koef = _input('Koef', 1.2)  # Periods additional multiplying ratio
ma_method = _input('ma_method', MODE_LWMA)  # Smoothing type
price_field = _input('price_field', STO_CLOSECLOSE)  # Stochastic calculation method
Stoch_Handle = Arr(8, 0, dyn=False)
min_rates_total = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int((Stoch_K + Stoch_D + Stoch_S) * MathPow(Koef, 8 - 1))
    for numb in range(0, 8):
        K = MathPow(Koef, numb)
        period = _int(Stoch_K * K)
        Kperiod = _int(Stoch_D * K)
        Dperiod = _int(Stoch_S * K)
        Stoch_Handle[numb] = iStochastic(None, 0, period, Kperiod, Dperiod, ma_method, price_field)
        if Stoch_Handle[numb] == INVALID_HANDLE:
            Print(' Failed to get handle of the iStochastic indicator ', numb)
        shortname = Box('')
        StringConcatenate(shortname, 'Stochastic X', 8, '*', DoubleToString(Koef, 1), '(', period, Kperiod, Dperiod, ')')
        PlotIndexSetString(numb, PLOT_LABEL, shortname.v)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb, PLOT_DRAW_BEGIN, min_rates_total)
        SetIndexBuffer(numb, Ind[numb].IndBuffer, INDICATOR_DATA)
        ArraySetAsSeries(Ind[numb].IndBuffer, True)
        PlotIndexSetInteger(numb, PLOT_DRAW_TYPE, PlotIndexGetInteger(0, PLOT_DRAW_TYPE))
        PlotIndexSetInteger(numb, PLOT_LINE_STYLE, PlotIndexGetInteger(0, PLOT_LINE_STYLE))
        PlotIndexSetInteger(numb, PLOT_LINE_WIDTH, PlotIndexGetInteger(0, PLOT_LINE_WIDTH))
        PlotIndexSetInteger(numb, PLOT_LINE_COLOR, PlotIndexGetInteger(0, PLOT_LINE_COLOR))
    shortname = Box("")
    StringConcatenate(shortname, 'Stochastic X', 8, '*', DoubleToString(Koef, 1), '(', EnumToString(ma_method, 'ENUM_MA_METHOD'), ', ', EnumToString(price_field, 'ENUM_STO_PRICE'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    for numb in range(0, 8):
        if BarsCalculated(Stoch_Handle[numb]) < min_rates_total:
            return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total - 1
    else:
        to_copy = rates_total - prev_calculated + 1
    for numb in range(0, 8):
        if CopyBuffer(Stoch_Handle[numb], 0, 0, to_copy, Ind[numb].IndBuffer) <= 0:
            return 0
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(8, 0, dyn=False, factory=CIndicatorsBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticX8(_MQL5Indicator):
    name = 'stochastic-x8'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Stoch_K': 12,  # the K period (the number of bars) for %K line calculation
        'Stoch_D': 8,  # smoothing period for %D line calculation
        'Stoch_S': 5,  # Deceleration value
        'Koef': 1.2,  # Periods additional multiplying ratio
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Smoothing type
        'price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=1),  # Stochastic calculation method
    }

