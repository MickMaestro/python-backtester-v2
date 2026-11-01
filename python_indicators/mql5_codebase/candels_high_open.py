"""Candels_High_Open — converted from MQL5: MQL5 Indicators/Candels High Open/Candels_High_Open.mq5

Comparison of four previous candles
Copyright: Copyright © 2016, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.002

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.002', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Comparison of four previous candles'], 'name': 'Candels_High_Open', 'source': 'MQL5 Indicators/Candels High Open/Candels_High_Open.mq5', 'folder': 'Candels High Open', 'inputs': [{'mql': 'InpReverse', 'py': 'InpReverse', 'param': 'InpReverse', 'type': 'bool', 'default': False, 'label': 'Reverse signals', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpReverse = _input('InpReverse', False)  # Reverse signals
ExtLineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    short_name = 'Candels High Open'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + ' (Reverge signals ' + _str(InpReverse) + ')')
    ArraySetAsSeries(ExtLineBuffer, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(open, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated + 1
    if prev_calculated == 0:
        limit = rates_total - 5
    for i in range(limit, 0 - 1, -1):
        if ((((high[i + 1] > high[i + 2] and high[i + 2] > high[i + 3]) and high[i + 3] > high[i + 4]) and open[i + 1] > open[i + 2]) and open[i + 2] > open[i + 3]) and open[i + 3] > open[i + 4]:
            if not InpReverse:
                ExtLineBuffer[i] = 1.0
            else:
                ExtLineBuffer[i] = -1.0
        if ((((high[i + 1] < high[i + 2] and high[i + 2] < high[i + 3]) and high[i + 3] < high[i + 4]) and open[i + 1] < open[i + 2]) and open[i + 2] < open[i + 3]) and open[i + 3] < open[i + 4]:
            if not InpReverse:
                ExtLineBuffer[i] = -1.0
            else:
                ExtLineBuffer[i] = 1.0
        else:
            ExtLineBuffer[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandelsHighOpen(_MQL5Indicator):
    name = 'Candels_High_Open'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpReverse': False,  # Reverse signals
    }

