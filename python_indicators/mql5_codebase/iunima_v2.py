"""iunima_v2 — converted from MQL5: MQL5 Indicators/iUniMA/iunima_v2.mq5

Copyright: Integer; Link: http://dmffx.com; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'http://dmffx.com', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MA'}, 'levels': [], 'description': [], 'name': 'iunima_v2', 'source': 'MQL5 Indicators/iUniMA/iunima_v2.mq5', 'folder': 'iUniMA', 'inputs': [{'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'AMAFast', 'py': 'AMAFast', 'param': 'AMAFast', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'AMASlow', 'py': 'AMASlow', 'param': 'AMASlow', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'CMOPeriod', 'py': 'CMOPeriod', 'param': 'CMOPeriod', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MAMethods
Simple = 0
Exponential = 1
Smoothed = 2
LinearWeighted = 3
AMA = 5
DEMA = 15
FRAMA = 20
TEMA = 34
VIDYA = 36
_enum('MAMethods', {0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'LinearWeighted', 5: 'AMA', 15: 'DEMA', 20: 'FRAMA', 34: 'TEMA', 36: 'VIDYA'})

# ---- inputs and global variables
MAMethod = _input('MAMethod', Simple)
MAPeriod = _input('MAPeriod', 14)
MAPrice = _input('MAPrice', PRICE_CLOSE)
AMAFast = _input('AMAFast', 2)
AMASlow = _input('AMASlow', 30)
CMOPeriod = _input('CMOPeriod', 9)
Handle_v = 0
MABuffer = Arr(0, 0.0)

def OnInit():
    global Handle_v
    SetIndexBuffer(0, MABuffer, INDICATOR_DATA)
    _sw1 = MAMethod
    if _sw1 == Simple:
        Handle_v = iMA(None, PERIOD_CURRENT, MAPeriod, 0, MODE_SMA, MAPrice)
    elif _sw1 == Exponential:
        Handle_v = iMA(None, PERIOD_CURRENT, MAPeriod, 0, MODE_EMA, MAPrice)
    elif _sw1 == Smoothed:
        Handle_v = iMA(None, PERIOD_CURRENT, MAPeriod, 0, MODE_SMMA, MAPrice)
    elif _sw1 == LinearWeighted:
        Handle_v = iMA(None, PERIOD_CURRENT, MAPeriod, 0, MODE_LWMA, MAPrice)
    elif _sw1 == AMA:
        Handle_v = iAMA(None, PERIOD_CURRENT, MAPeriod, AMAFast, AMASlow, 0, MAPrice)
    elif _sw1 == DEMA:
        Handle_v = iDEMA(None, PERIOD_CURRENT, MAPeriod, 0, MAPrice)
    elif _sw1 == FRAMA:
        Handle_v = iFrAMA(None, PERIOD_CURRENT, MAPeriod, 0, MAPrice)
    elif _sw1 == TEMA:
        Handle_v = iTEMA(None, PERIOD_CURRENT, MAPeriod, 0, MAPrice)
    elif _sw1 == VIDYA:
        Handle_v = iVIDyA(None, PERIOD_CURRENT, CMOPeriod, MAPeriod, 0, MAPrice)
    Label = ""
    _sw2 = MAMethod
    if _sw2 == Simple:
        Label = 'SMA(' + ITS(MAPeriod) + ',' + fNamePriceShort(MAPrice) + ')'
    elif _sw2 == Exponential:
        Label = 'EMA(' + ITS(MAPeriod) + ',' + fNamePriceShort(MAPrice) + ')'
    elif _sw2 == Smoothed:
        Label = 'SMMA(' + ITS(MAPeriod) + ',' + fNamePriceShort(MAPrice) + ')'
    elif _sw2 == LinearWeighted:
        Label = 'LWMA(' + ITS(MAPeriod) + ',' + fNamePriceShort(MAPrice) + ')'
    elif _sw2 == AMA:
        Label = 'AMA(' + ITS(MAPeriod) + ',' + ITS(AMAFast) + ',' + ITS(AMASlow) + ',' + fNamePriceShort(MAPrice) + ')'
    elif _sw2 == DEMA:
        Label = 'DEMA(' + ITS(MAPeriod) + ',' + fNamePriceShort(MAPrice) + ')'
    elif _sw2 == FRAMA:
        Label = 'FRAM(' + ITS(MAPeriod) + ',' + fNamePriceShort(MAPrice) + ')'
    elif _sw2 == TEMA:
        Label = 'TEMA(' + ITS(MAPeriod) + ',' + fNamePriceShort(MAPrice) + ')'
    elif _sw2 == VIDYA:
        Label = 'VIDYA(' + ITS(MAPeriod) + ',' + ITS(CMOPeriod) + ',' + fNamePriceShort(MAPrice) + ')'
    PlotIndexSetString(0, PLOT_LABEL, Label)
    return 0

def fNamePriceShort(aPrice):
    _sw3 = aPrice
    if _sw3 == PRICE_CLOSE:
        return 'C'
    elif _sw3 == PRICE_HIGH:
        return 'H'
    elif _sw3 == PRICE_LOW:
        return 'L'
    elif _sw3 == PRICE_MEDIAN:
        return 'M'
    elif _sw3 == PRICE_OPEN:
        return 'O'
    elif _sw3 == PRICE_TYPICAL:
        return 'T'
    elif _sw3 == PRICE_WEIGHTED:
        return 'W'
    return '?'

def ITS(aValue):
    return IntegerToString(aValue)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_error
    start = 0
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = 0
        _s_OnCalculate_error = False
    else:
        start = prev_calculated - 1
    if CopyBuffer(Handle_v, 0, 0, rates_total - start, MABuffer) == -1:
        _s_OnCalculate_error = True
        return rates_total
    return rates_total

# ---- static local variables
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IunimaV2(_MQL5Indicator):
    name = 'iunima_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAMethod': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'LinearWeighted', 5: 'AMA', 15: 'DEMA', 20: 'FRAMA', 34: 'TEMA', 36: 'VIDYA'}, default=0),
        'MAPeriod': 14,
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'AMAFast': 2,
        'AMASlow': 30,
        'CMOPeriod': 9,
    }

