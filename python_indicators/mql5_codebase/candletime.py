"""candletime — converted from MQL5: MQL5 Indicators/Simple timer next candle/candletime.mq5

Copyright: Francesco Danti Copyright 2011, OracolTech.com; Link: http://blog.oracoltech.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Francesco Danti Copyright 2011, OracolTech.com', 'link': 'http://blog.oracoltech.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'candletime', 'source': 'MQL5 Indicators/Simple timer next candle/candletime.mq5', 'folder': 'Simple timer next candle', 'inputs': [{'mql': 'lblColor', 'py': 'lblColor', 'param': None, 'type': 'color', 'default': 6504960, 'label': 'Color of the label', 'sinput': False}, {'mql': 'fontSize', 'py': 'fontSize', 'param': 'fontSize', 'type': 'int', 'default': 8, 'label': 'Size of the label font', 'sinput': False}, {'mql': 'pAnchor', 'py': 'pAnchor', 'param': 'pAnchor', 'type': 'int', 'default': 2, 'label': 'Anchor of the label a sort of align', 'sinput': False}, {'mql': 'nextToPriceOrAnchor', 'py': 'nextToPriceOrAnchor', 'param': 'nextToPriceOrAnchor', 'type': 'bool', 'default': True, 'label': 'Position near the price close or to Corner', 'sinput': False}, {'mql': 'pCorner', 'py': 'pCorner', 'param': 'pCorner', 'type': 'int', 'default': 1, 'label': 'Corner position of the label', 'sinput': False}, {'mql': 'fontFamily', 'py': 'fontFamily', 'param': None, 'type': 'string', 'default': 'Tahoma', 'label': 'Font family of the label', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
idxLabel = 'lblNextCandle'
lblColor = _input('lblColor', 0x634200)  # Color of the label
fontSize = _input('fontSize', 8)  # Size of the label font
pAnchor = _input('pAnchor', ANCHOR_LEFT_LOWER)  # Anchor of the label a sort of align
nextToPriceOrAnchor = _input('nextToPriceOrAnchor', True)  # Position near the price close or to Corner
pCorner = _input('pCorner', CORNER_LEFT_LOWER)  # Corner position of the label
fontFamily = _input('fontFamily', 'Tahoma')  # Font family of the label

def OnInit():
    return 0

def OnDeinit(r):
    Comment('')
    ObjectDelete(0, idxLabel)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    idxLastBar = rates_total - 1
    tS = 0
    iS = 0
    iM = 0
    iH = 0
    sS = ""
    sM = ""
    sH = ""
    tS = _int(time[0]) + PeriodSeconds() - _int(TimeCurrent())
    iS = _imod(tS, 60)
    iM = tS - iS
    if iM != 0:
        iM = _idiv(iM, 60)
    iM -= iM - _imod(iM, 60)
    iH = tS - iS - (iM * 60)
    if iH != 0:
        iH = _idiv(iH, 60)
    if iH != 0:
        iH = _idiv(iH, 60)
    sS = IntegerToString(iS, 2, 48)
    sM = IntegerToString(iM, 2, 48)
    sH = IntegerToString(iH, 2, 48)
    cmt = sH + ':' + sM + ':' + sS
    if nextToPriceOrAnchor:
        if ObjectGetInteger(0, idxLabel, OBJPROP_TYPE) == OBJ_LABEL:
            ObjectDelete(0, idxLabel)
        ObjectCreate(0, idxLabel, OBJ_TEXT, 0, time[0] + (PeriodSeconds() * 2), close[0])
        ObjectSetInteger(0, idxLabel, OBJPROP_ANCHOR, pAnchor)
    else:
        if ObjectGetInteger(0, idxLabel, OBJPROP_TYPE) == OBJ_TEXT:
            ObjectDelete(0, idxLabel)
        ObjectCreate(0, idxLabel, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, idxLabel, OBJPROP_ANCHOR, pAnchor)
        ObjectSetInteger(0, idxLabel, OBJPROP_CORNER, pCorner)
    ObjectSetInteger(0, idxLabel, OBJPROP_COLOR, lblColor)
    ObjectSetString(0, idxLabel, OBJPROP_TEXT, cmt)
    ObjectSetInteger(0, idxLabel, OBJPROP_FONTSIZE, fontSize)
    ObjectSetString(0, idxLabel, OBJPROP_FONT, fontFamily)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Candletime(_MQL5Indicator):
    name = 'candletime'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'fontSize': 8,  # Size of the label font
        'pAnchor': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=2),  # Anchor of the label a sort of align
        'nextToPriceOrAnchor': True,  # Position near the price close or to Corner
        'pCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Corner position of the label
    }

