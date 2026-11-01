"""advanced_adx — converted from MQL5: MQL5 Indicators/Advanced ADX/advanced_adx.mq5

Copyright: Waddah Attar; Link: waddahattar@hotmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Waddah Attar', 'link': 'waddahattar@hotmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'advanced_adx', 'source': 'MQL5 Indicators/Advanced ADX/advanced_adx.mq5', 'folder': 'Advanced ADX', 'inputs': [{'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'uint', 'default': 13, 'label': 'ADX period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ADXPeriod = _input('ADXPeriod', 13)  # ADX period
ExtBuffer1 = Arr(0, 0.0)
ExtBuffer2 = Arr(0, 0.0)
ADX_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX_Handle, min_rates_total
    min_rates_total = _int(ADXPeriod + 1)
    ADX_Handle = iADX(None, 0, ADXPeriod)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of ADX indicator')
        return INIT_FAILED
    SetIndexBuffer(0, ExtBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtBuffer1, True)
    SetIndexBuffer(1, ExtBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtBuffer2, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Advanced_ADX (', ADXPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    if BarsCalculated(ADX_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    pADX0 = Arr(0, 0.0)
    pADX1 = Arr(0, 0.0)
    pADX2 = Arr(0, 0.0)
    ArraySetAsSeries(pADX0, True)
    ArraySetAsSeries(pADX1, True)
    ArraySetAsSeries(pADX2, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(ADX_Handle, MAIN_LINE, 0, to_copy, pADX0) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, PLUSDI_LINE, 0, to_copy, pADX1) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, MINUSDI_LINE, 0, to_copy, pADX2) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ADX0 = pADX0[bar]
        ADX1 = pADX1[bar]
        ADX2 = pADX2[bar]
        if ADX1 >= ADX2:
            ExtBuffer1[bar] = ADX0
            ExtBuffer2[bar] = 0.0
        else:
            ExtBuffer1[bar] = 0.0
            ExtBuffer2[bar] = ADX0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdvancedAdx(_MQL5Indicator):
    name = 'advanced_adx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ADXPeriod': 13,  # ADX period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

