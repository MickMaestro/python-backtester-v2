"""Dsl MACD — converted from MQL5: MQL5 Indicators/Dsl MACD 2/Dsl MACD.mq5

Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '2.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 8}, 'colors': {1: [3329330, 42495], 2: [3329330], 3: [42495], 4: [12632256, 3329330, 42495]}, 'widths': {4: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'up trend;down trend', 2: 'up level', 3: 'down level', 4: 'MACD'}, 'levels': [], 'description': [], 'name': 'Dsl MACD', 'source': 'MQL5 Indicators/Dsl MACD 2/Dsl MACD.mq5', 'folder': 'Dsl MACD 2', 'inputs': [{'mql': 'inpFastEma', 'py': 'inpFastEma', 'param': 'inpFastEma', 'type': 'double', 'default': 12.0, 'label': 'Fast ema period', 'sinput': False}, {'mql': 'inpSlowEma', 'py': 'inpSlowEma', 'param': 'inpSlowEma', 'type': 'double', 'default': 26.0, 'label': 'Slow ema period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'double', 'default': 9.0, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpZones', 'py': 'inpZones', 'param': 'inpZones', 'type': 'int', 'default': 1, 'label': 'Zones display mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDisplayZones
zones_yes = 1
zones_no = 0
_enum('enDisplayZones', {1: 'zones_yes', 0: 'zones_no'})

# ---- inputs and global variables
inpFastEma = _input('inpFastEma', 12.0)  # Fast ema period
inpSlowEma = _input('inpSlowEma', 26.0)  # Slow ema period
inpSignalPeriod = _input('inpSignalPeriod', 9.0)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpZones = _input('inpZones', zones_yes)  # Zones display mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
fillUp = Arr(0, 0.0)
fillDn = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('alphaFast', 'alphaSlow', 'alphaSignal')
    def __init__(self, *args):
        self.alphaFast = 0.0
        self.alphaSlow = 0.0
        self.alphaSignal = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('fastEma', 'slowEma')
    def __init__(self, *args):
        self.fastEma = 0.0
        self.slowEma = 0.0

def OnInit():
    SetIndexBuffer(0, fillUp, INDICATOR_DATA)
    SetIndexBuffer(1, fillDn, INDICATOR_DATA)
    SetIndexBuffer(2, levelUp, INDICATOR_DATA)
    SetIndexBuffer(3, levelDn, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    global_.alphaFast = _fdiv(2.0, 1.0 + MathMax(inpFastEma, 1.0))
    global_.alphaSlow = _fdiv(2.0, 1.0 + MathMax(inpSlowEma, 1.0))
    global_.alphaSignal = _fdiv(2.0, 1.0 + MathMax(inpSignalPeriod, 1.0))
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('(dsl) MACD (%s,%s,%s)', _str(inpFastEma), _str(inpSlowEma), _str(inpSignalPeriod)))

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        _price = getPrice(inpPrice, open, high, low, close, i)
        _s_OnCalculate_m_work[i].fastEma = ((_s_OnCalculate_m_work[i - 1].fastEma + (global_.alphaFast * (_price - _s_OnCalculate_m_work[i - 1].fastEma))) if (i > 0) else _price)
        _s_OnCalculate_m_work[i].slowEma = ((_s_OnCalculate_m_work[i - 1].slowEma + (global_.alphaSlow * (_price - _s_OnCalculate_m_work[i - 1].slowEma))) if (i > 0) else _price)
        val[i] = _s_OnCalculate_m_work[i].fastEma - _s_OnCalculate_m_work[i].slowEma
        levelUp[i] = (((levelUp[i - 1] + (global_.alphaSignal * (val[i] - levelUp[i - 1]))) if (val[i] > 0) else levelUp[i - 1]) if (i > 0) else 0)
        levelDn[i] = (((levelDn[i - 1] + (global_.alphaSignal * (val[i] - levelDn[i - 1]))) if (val[i] < 0) else levelDn[i - 1]) if (i > 0) else 0)
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else 0)
        if inpZones:
            fillUp[i] = val[i]
            fillDn[i] = (levelUp[i] if (valc[i] == 1) else levelDn[i] if (valc[i] == 2) else val[i])
        else:
            fillDn[i] = EMPTY_VALUE
            fillUp[i] = fillDn[i]
    return rates_total

def getPrice(tprice, open, high, low, close, i):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

# ---- global variables initialised from expressions
global_ = _alloc(sGlobalStruct)
global_.__init__()

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DslMACD(_MQL5Indicator):
    name = 'Dsl MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastEma': 12.0,  # Fast ema period
        'inpSlowEma': 26.0,  # Slow ema period
        'inpSignalPeriod': 9.0,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpZones': _Choice({1: 'Display filled zoned', 0: 'No filled zones display'}, default=1),  # Zones display mode
    }

