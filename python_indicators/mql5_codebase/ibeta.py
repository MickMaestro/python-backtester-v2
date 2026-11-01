"""ibeta — converted from MQL5: MQL5 Indicators/iBeta/ibeta.mq5

Copyright: Integer; Link: https://login.mql5.com/en/users/Integer; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'https://login.mql5.com/en/users/Integer', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'ibeta', 'source': 'MQL5 Indicators/iBeta/ibeta.mq5', 'folder': 'iBeta', 'inputs': [{'mql': 'Periods', 'py': 'Periods', 'param': 'Periods', 'type': 'int', 'default': 14, 'label': 'Period in bars', 'sinput': False}, {'mql': 'Symbol1', 'py': 'Symbol1', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'Symbol 1', 'sinput': False}, {'mql': 'Symbol2', 'py': 'Symbol2', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Symbol 2', 'sinput': False}, {'mql': 'Mode1', 'py': 'Mode1', 'param': 'Mode1', 'type': 'int', 'default': 1, 'label': 'Calculated value', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Mode2', 'py': 'Mode2', 'param': 'Mode2', 'type': 'int', 'default': 2, 'label': 'Mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum m1
Covariation = 0
Symbol1Beta = 1
Symbol2Beta = 2
Correlation = 3
_enum('m1', {0: 'Covariation', 1: 'Symbol1Beta', 2: 'Symbol2Beta', 3: 'Correlation'})

# enum m2
Price = 0
ROC = 1
ROC_Percents = 2
_enum('m2', {0: 'Price', 1: 'ROC', 2: 'ROC_Percents'})

# ---- inputs and global variables
Periods = _input('Periods', 14)  # Period in bars
Symbol1 = _input('Symbol1', 'EURUSD')  # Symbol 1
Symbol2 = _input('Symbol2', 'GBPUSD')  # Symbol 2
Mode1 = _input('Mode1', Symbol1Beta)  # Calculated value
Price = _input('Price', PRICE_CLOSE)
Mode2 = _input('Mode2', ROC_Percents)  # Mode
p1 = Arr(0, 0.0)
p2 = Arr(0, 0.0)
p12 = Arr(1, 0.0, dyn=False)
p22 = Arr(1, 0.0, dyn=False)
Label1Buffer = Arr(0, 0.0)
ma1h = 0
ma2h = 0
ma1h2 = 0
ma2h2 = 0
x = 0.0
y = 0.0
z1 = 0.0
z2 = 0.0

def OnInit():
    global ma1h, ma1h2, ma2h, ma2h2
    ArrayResize(p1, Periods + 1)
    ArrayResize(p2, Periods + 1)
    SetIndexBuffer(0, Label1Buffer, INDICATOR_DATA)
    ma1h = iMA(Symbol1, PERIOD_CURRENT, 1, 0, MODE_SMA, Price)
    ma2h = iMA(Symbol2, PERIOD_CURRENT, 1, 0, MODE_SMA, Price)
    ma1h2 = iMA(Symbol1, PERIOD_CURRENT, Periods, 0, MODE_SMA, Price)
    ma2h2 = iMA(Symbol2, PERIOD_CURRENT, Periods, 0, MODE_SMA, Price)
    if ((ma1h == INVALID_HANDLE or ma2h == INVALID_HANDLE) or ma1h2 == INVALID_HANDLE) or ma2h2 == INVALID_HANDLE:
        Alert('Failed to download МА, relaunch the indicator')
        return 1
    _sw1 = Mode1
    if _sw1 == 0:
        IndicatorSetString(INDICATOR_SHORTNAME, Symbol1 + ' ' + Symbol2 + ' covariation')
        PlotIndexSetString(0, PLOT_LABEL, Symbol1 + ' ' + Symbol2 + ' covariation')
    elif _sw1 == 1:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Beta of ' + Symbol1 + ' with ' + Symbol2)
        PlotIndexSetString(0, PLOT_LABEL, 'Beta of ' + Symbol1 + ' with ' + Symbol2)
    elif _sw1 == 2:
        IndicatorSetString(INDICATOR_SHORTNAME, 'Beta of ' + Symbol2 + ' with ' + Symbol1)
        PlotIndexSetString(0, PLOT_LABEL, 'Beta of ' + Symbol2 + ' with ' + Symbol1)
    elif _sw1 == 3:
        IndicatorSetString(INDICATOR_SHORTNAME, Symbol1 + ' ' + Symbol2 + ' correlation')
        PlotIndexSetString(0, PLOT_LABEL, Symbol1 + ' ' + Symbol2 + ' correlation')
    return 0

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_error, x, y, z1, z2
    start = 0
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = 0
        b1 = Bars(Symbol1, PERIOD_CURRENT)
        b2 = Bars(Symbol2, PERIOD_CURRENT)
        if b1 == 0 or b2 == 0:
            Comment('Waiting for data upload...')
            return 0
        if CopyRates(Symbol1, PERIOD_CURRENT, b1 - 1, 1, r1) == -1 or CopyRates(Symbol2, PERIOD_CURRENT, b2 - 1, 1, r2) == -1:
            Comment('Waiting for data upload...')
            return 0
        for i in range(0, rates_total):
            if time[i] > r1[0].time and time[i] > r2[0].time:
                start = i + Periods + 1
                break
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        Comment('')
        _s_OnCalculate_error = False
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        if ((CopyBuffer(ma1h, 0, _DT(time[i]), Periods + 1, p1) == -1 or CopyBuffer(ma2h, 0, _DT(time[i]), Periods + 1, p2) == -1) or CopyBuffer(ma1h2, 0, _DT(time[i]), 1, p12) == -1) or CopyBuffer(ma2h2, 0, _DT(time[i]), 1, p22) == -1:
            _s_OnCalculate_error = True
            return 0
        aver1 = p12[0]
        aver2 = p22[0]
        cov = 0.0
        d1 = 0.0
        d2 = 0.0
        _sw2 = Mode2
        if _sw2 == 0:
            for j in range(1, Periods + 1):
                x = p1[j]
                y = p2[j]
                z1 = x - aver1
                z2 = y - aver2
                cov += z1 * z2
                d1 += z1 * z1
                d2 += z2 * z2
        elif _sw2 == 1:
            for j in range(1, Periods + 1):
                x = p1[j] - p1[j - 1]
                y = p2[j] - p2[j - 1]
                z1 = x - aver1
                z2 = y - aver2
                cov += z1 * z2
                d1 += z1 * z1
                d2 += z2 * z2
        elif _sw2 == 2:
            for j in range(1, Periods + 1):
                x = _fdiv(p1[j] - p1[j - 1], p1[j - 1])
                y = _fdiv(p2[j] - p2[j - 1], p2[j - 1])
                z1 = x - aver1
                z2 = y - aver2
                cov += z1 * z2
                d1 += z1 * z1
                d2 += z2 * z2
        cov = cov / Periods
        d1 = MathSqrt(d1 / Periods)
        d2 = MathSqrt(d2 / Periods)
        _sw3 = Mode1
        if _sw3 == 0:
            Label1Buffer[i] = cov
        elif _sw3 == 1:
            Label1Buffer[i] = _fdiv(cov, d2)
        elif _sw3 == 2:
            Label1Buffer[i] = _fdiv(cov, d1)
        elif _sw3 == 3:
            Label1Buffer[i] = _fdiv(cov, d1 * d2)
    return rates_total

# ---- global variables initialised from expressions
r1 = Arr(1, 0, dyn=False, factory=MqlRates)
r2 = Arr(1, 0, dyn=False, factory=MqlRates)

# ---- static local variables
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ibeta(_MQL5Indicator):
    name = 'ibeta'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Periods': 14,  # Period in bars
        'Mode1': _Choice({0: 'Covariation', 1: 'Symbol1Beta', 2: 'Symbol2Beta', 3: 'Correlation'}, default=1),  # Calculated value
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Mode2': _Choice({0: 'Price', 1: 'ROC', 2: 'ROC_Percents'}, default=2),  # Mode
    }

