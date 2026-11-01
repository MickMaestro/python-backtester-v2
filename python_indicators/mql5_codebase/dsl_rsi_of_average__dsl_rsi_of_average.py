"""Dsl RSI of average — converted from MQL5: MQL5 Indicators/Dsl RSI of average/Dsl RSI of average.mq5

Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 8}, 'colors': {1: [3329330, 42495], 2: [3329330], 3: [42495], 4: [12632256, 3329330, 42495]}, 'widths': {4: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'up trend;down trend', 2: 'up level', 3: 'down level', 4: 'RSI'}, 'levels': [], 'description': [], 'name': 'Dsl RSI of average', 'source': 'MQL5 Indicators/Dsl RSI of average/Dsl RSI of average.mq5', 'folder': 'Dsl RSI of average', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 32, 'label': 'Average period (<= 1 for no average)', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'double', 'default': 9.0, 'label': 'Dsl signal period', 'sinput': False}, {'mql': 'inpZones', 'py': 'inpZones', 'param': 'inpZones', 'type': 'int', 'default': 1, 'label': 'Zones display mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDisplayZones
zones_yes = 1
zones_no = 0
_enum('enDisplayZones', {1: 'zones_yes', 0: 'zones_no'})

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpMaPeriod = _input('inpMaPeriod', 32)  # Average period (<= 1 for no average)
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpSignalPeriod = _input('inpSignalPeriod', 9.0)  # Dsl signal period
inpZones = _input('inpZones', zones_yes)  # Zones display mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
fillUp = Arr(0, 0.0)
fillDn = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('avgPeriod', 'avgHandle', 'rsiHandle', 'alphaSignal')
    def __init__(self, *args):
        self.avgPeriod = 0
        self.avgHandle = 0
        self.rsiHandle = 0
        self.alphaSignal = 0.0

def OnInit():
    SetIndexBuffer(0, fillUp, INDICATOR_DATA)
    SetIndexBuffer(1, fillDn, INDICATOR_DATA)
    SetIndexBuffer(2, levelUp, INDICATOR_DATA)
    SetIndexBuffer(3, levelDn, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    global_.avgPeriod = (inpMaPeriod if (inpMaPeriod > 0) else 1)
    global_.avgHandle = iMA(Symbol(), Period(), global_.avgPeriod, 0, inpMaMethod, inpPrice)
    global_.rsiHandle = iRSI(Symbol(), Period(), inpRsiPeriod, global_.avgHandle)
    global_.alphaSignal = _fdiv(2.0, 1.0 + MathMax(inpSignalPeriod, 1.0))
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('(dsl) rsi %s (%s,%s,%s)', StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5, -1), _str(inpRsiPeriod), _str(global_.avgPeriod), _str(inpSignalPeriod)))

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    copyLimit = ((rates_total - prev_calculated + 1) if (prev_calculated > 0) else rates_total)
    if CopyBuffer(global_.rsiHandle, 0, 0, copyLimit, val) != copyLimit:
        return prev_calculated
    for i in range(limit, rates_total):
        if val[i] == EMPTY_VALUE:
            val[i] = 50.0
        levelUp[i] = (((levelUp[i - 1] + (global_.alphaSignal * (val[i] - levelUp[i - 1]))) if (val[i] > 50) else levelUp[i - 1]) if (i > 0) else val[i])
        levelDn[i] = (((levelDn[i - 1] + (global_.alphaSignal * (val[i] - levelDn[i - 1]))) if (val[i] < 50) else levelDn[i - 1]) if (i > 0) else val[i])
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else 0)
        if inpZones:
            fillUp[i] = val[i]
            fillDn[i] = (levelUp[i] if (valc[i] == 1) else levelDn[i] if (valc[i] == 2) else val[i])
        else:
            fillDn[i] = EMPTY_VALUE
            fillUp[i] = fillDn[i]
    return rates_total

# ---- global variables initialised from expressions
global_ = _alloc(sGlobalStruct)
global_.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DslRSIOfAverage(_MQL5Indicator):
    name = 'Dsl RSI of average'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpMaPeriod': 32,  # Average period (<= 1 for no average)
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSignalPeriod': 9.0,  # Dsl signal period
        'inpZones': _Choice({1: 'Display filled zoned', 0: 'No filled zones display'}, default=1),  # Zones display mode
    }

