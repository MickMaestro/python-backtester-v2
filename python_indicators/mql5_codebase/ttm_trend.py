"""TTM trend — converted from MQL5: MQL5 Indicators/TTM trend/TTM trend.mq5

TTM trend
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [11119017, 16760576, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TTM trend'}, 'levels': [], 'description': ['TTM trend'], 'name': 'TTM trend', 'source': 'MQL5 Indicators/TTM trend/TTM trend.mq5', 'folder': 'TTM trend', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 10, 'label': 'Look back period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 10)  # Look back period
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
valc = Arr(0, 0.0)
haOpen = Arr(0, 0.0)
haClose = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, valu, INDICATOR_DATA)
    SetIndexBuffer(1, vald, INDICATOR_DATA)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, haOpen, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, haClose, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TTP trend (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        haOpen[i] = (((haOpen[i - 1] + haClose[i - 1]) / 2.0) if (i > 0) else ((open[i] + close[i]) / 2.0))
        haClose[i] = (open[i] + high[i] + low[i] + close[i]) / 4.0
        valu[i] = high[i]
        vald[i] = low[i]
        valc[i] = (1 if (haClose[i] > haOpen[i]) else 2 if (haClose[i] < haOpen[i]) else valc[i - 1] if (i > (0 - 1)) else 0)
        k = 1
        while k <= inpPeriod and (i - k) >= 0:
            if ((haOpen[i] <= MathMax(haOpen[i - k], haClose[i - k]) and haOpen[i] >= MathMin(haOpen[i - k], haClose[i - k])) and haClose[i] <= MathMax(haOpen[i - k], haClose[i - k])) and haClose[i] >= MathMin(haOpen[i - k], haClose[i - k]):
                valc[i] = valc[i - k]
            k += 1
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TTMTrend(_MQL5Indicator):
    name = 'TTM trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 10,  # Look back period
    }

