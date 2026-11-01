"""oracle — converted from MQL5: MQL5 Indicators/Oracle/oracle.mq5

Indicator of forecast on three bars ahead!
Copyright: Copyright © 2009, Ivan Kornilov; Link: excelf@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Ivan Kornilov', 'link': 'excelf@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711935], 2: [13828244]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Oracle', 2: 'Signal'}, 'levels': [], 'description': ['Indicator of forecast on three bars ahead!'], 'name': 'oracle', 'source': 'MQL5 Indicators/Oracle/oracle.mq5', 'folder': 'Oracle', 'inputs': [{'mql': 'OraclePeriod', 'py': 'OraclePeriod', 'param': 'OraclePeriod', 'type': 'uint', 'default': 55, 'label': 'Oracle period', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'uint', 'default': 8, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'Recount', 'py': 'Recount', 'param': 'Recount', 'type': 'bool', 'default': True, 'label': 'redrawing', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 3, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
OraclePeriod = _input('OraclePeriod', 55)  # Oracle period
applied_price = PRICE_CLOSE  # Price type
Smooth = _input('Smooth', 8)  # smoothing depth
Recount = _input('Recount', True)  # redrawing
Shift = _input('Shift', 3)  # horizontal shift of the indicator in bars
OracleBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
min_rates_total = 0
RSI_Handle = 0
CCI_Handle = 0

def OnInit():
    global CCI_Handle, RSI_Handle, min_rates_total
    min_rates_total = _int(OraclePeriod + Smooth + 1 + 4)
    RSI_Handle = iRSI(None, 0, OraclePeriod, applied_price)
    if RSI_Handle == INVALID_HANDLE:
        Print('Failed to get handle of the RSI indicator')
    CCI_Handle = iCCI(None, 0, OraclePeriod, applied_price)
    if CCI_Handle == INVALID_HANDLE:
        Print('Failed to get handle of the CCI indicator')
    SetIndexBuffer(0, OracleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, OraclePeriod + 4)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(OracleBuffer, True)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SignalBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Oracle(', OraclePeriod, ', ', Smooth, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(RSI_Handle) < rates_total or BarsCalculated(CCI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    iii = 0
    dDiv = 0.0
    Sum = 0.0
    RSI = Arr(0, 0.0)
    CCI = Arr(0, 0.0)
    Div = Arr(4, 0.0, dyn=False)
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(CCI, True)
    maxbar = _int(rates_total - OraclePeriod - 4 - 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
        if Recount:
            limit += 4
    to_copy = limit + 1 + 4
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    if Recount:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            Div[0] = CCI[bar] - RSI[bar]
            dDiv = Div[0]
            if bar > 0:
                Div[1] = CCI[bar - 1] - RSI[bar + 1] - dDiv
            else:
                Div[1] = CCI[bar] - RSI[bar + 1] - dDiv
            dDiv += Div[1]
            if bar > 1:
                Div[2] = CCI[bar - 2] - RSI[bar + 2] - dDiv
            elif bar > 0:
                Div[2] = CCI[bar - 1] - RSI[bar + 2] - dDiv
            else:
                Div[2] = CCI[bar] - RSI[bar + 2] - dDiv
            dDiv += Div[2]
            if bar > 2:
                Div[3] = CCI[bar - 3] - RSI[bar + 3] - dDiv
            elif bar > 1:
                Div[3] = CCI[bar - 2] - RSI[bar + 3] - dDiv
            elif bar > 0:
                Div[3] = CCI[bar - 1] - RSI[bar + 3] - dDiv
            else:
                Div[3] = CCI[bar] - RSI[bar + 3] - dDiv
            OracleBuffer[bar] = Div[ArrayMaximum(Div, 0, WHOLE_ARRAY)] + Div[ArrayMinimum(Div, 0, WHOLE_ARRAY)]
            if bar > maxbar:
                SignalBuffer[bar] = EMPTY_VALUE
            else:
                Sum = 0.0
                iii = 0
                for iii in range(iii, _int(Smooth)):
                    Sum += OracleBuffer[bar + iii]
                else:
                    iii = _range_end(iii, _int(Smooth), 1)
                SignalBuffer[bar] = Sum / Smooth
        else:
            bar = _range_end(bar, 0 - 1, -1)
    if not Recount:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            Div[0] = CCI[bar] - RSI[bar]
            dDiv = Div[0]
            Div[1] = CCI[bar] - RSI[bar + 1] - dDiv
            dDiv += Div[1]
            Div[2] = CCI[bar] - RSI[bar + 2] - dDiv
            dDiv += Div[2]
            Div[3] = CCI[bar] - RSI[bar + 3] - dDiv
            OracleBuffer[bar] = Div[ArrayMaximum(Div, 0, WHOLE_ARRAY)] + Div[ArrayMinimum(Div, 0, WHOLE_ARRAY)]
            if bar > maxbar:
                SignalBuffer[bar] = EMPTY_VALUE
            else:
                Sum = 0.0
                iii = 0
                for iii in range(iii, _int(Smooth)):
                    Sum += OracleBuffer[bar + iii]
                else:
                    iii = _range_end(iii, _int(Smooth), 1)
                SignalBuffer[bar] = Sum / Smooth
        else:
            bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Oracle(_MQL5Indicator):
    name = 'oracle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'OraclePeriod': 55,  # Oracle period
        'Smooth': 8,  # smoothing depth
        'Recount': True,  # redrawing
        'Shift': 3,  # horizontal shift of the indicator in bars
    }

