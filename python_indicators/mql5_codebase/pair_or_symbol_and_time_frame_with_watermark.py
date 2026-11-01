"""Pair Or Symbol And Time Frame With Watermark — converted from MQL5: MQL5 Indicators/Pair Or Symbol And Time Frame With Watermark/Pair Or Symbol And Time Frame With Watermark.mq5

Pair Or Symbol And Time Frame With Watermark
Copyright: Dwi Sudarsono; Link: https://t.me/DwiSudarsono; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Dwi Sudarsono', 'link': 'https://t.me/DwiSudarsono', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Pair Or Symbol And Time Frame With Watermark'], 'name': 'Pair Or Symbol And Time Frame With Watermark', 'source': 'MQL5 Indicators/Pair Or Symbol And Time Frame With Watermark/Pair Or Symbol And Time Frame With Watermark.mq5', 'folder': 'Pair Or Symbol And Time Frame With Watermark', 'inputs': [{'mql': 'BASE_CORNER', 'py': 'BASE_CORNER', 'param': 'BASE_CORNER', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 45, 'label': '', 'sinput': False}, {'mql': 'FontName', 'py': 'FontName', 'param': None, 'type': 'string', 'default': 'Times New Roman', 'label': '', 'sinput': False}, {'mql': 'NoteRedGreenBlue', 'py': 'NoteRedGreenBlue', 'param': None, 'type': 'string', 'default': 'Red/Green/Blue each 0..255', 'label': '', 'sinput': False}, {'mql': 'RGBRed', 'py': 'RGBRed', 'param': 'RGBRed', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'RGBGreen', 'py': 'RGBGreen', 'param': 'RGBGreen', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'RGBBlue', 'py': 'RGBBlue', 'param': 'RGBBlue', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'XPos', 'py': 'XPos', 'param': 'XPos', 'type': 'int', 'default': 400, 'label': '', 'sinput': False}, {'mql': 'YPos', 'py': 'YPos', 'param': 'YPos', 'type': 'int', 'default': 70, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BASE_CORNER = _input('BASE_CORNER', CORNER_RIGHT_LOWER)
FontSize = _input('FontSize', 45)
FontName = _input('FontName', 'Times New Roman')
NoteRedGreenBlue = _input('NoteRedGreenBlue', 'Red/Green/Blue each 0..255')
RGBRed = _input('RGBRed', 30)
RGBGreen = _input('RGBGreen', 30)
RGBBlue = _input('RGBBlue', 30)
XPos = _input('XPos', 400)
YPos = _input('YPos', 70)
Pair = 'Symbol'
RGB_v = 0
tf = ""

def OnInit():
    global RGB_v, tf
    ObjectsDeleteAll(0)
    Comment('')
    _sw1 = Period()
    if _sw1 == PERIOD_M1:
        tf = 'm1'
    elif _sw1 == PERIOD_M2:
        tf = 'm2'
    elif _sw1 == PERIOD_M3:
        tf = 'm3'
    elif _sw1 == PERIOD_M4:
        tf = 'm4'
    elif _sw1 == PERIOD_M5:
        tf = 'm5'
    elif _sw1 == PERIOD_M6:
        tf = 'm6'
    elif _sw1 == PERIOD_M10:
        tf = 'm10'
    elif _sw1 == PERIOD_M12:
        tf = 'm12'
    elif _sw1 == PERIOD_M15:
        tf = 'm15'
    elif _sw1 == PERIOD_M20:
        tf = 'm20'
    elif _sw1 == PERIOD_M30:
        tf = 'm30'
    elif _sw1 == PERIOD_H1:
        tf = 'h1'
    elif _sw1 == PERIOD_H2:
        tf = 'h2'
    elif _sw1 == PERIOD_H3:
        tf = 'h3'
    elif _sw1 == PERIOD_H4:
        tf = 'h4'
    elif _sw1 == PERIOD_H6:
        tf = 'h6'
    elif _sw1 == PERIOD_H8:
        tf = 'h8'
    elif _sw1 == PERIOD_H12:
        tf = 'h12'
    elif _sw1 == PERIOD_D1:
        tf = 'd1'
    elif _sw1 == PERIOD_W1:
        tf = 'w1'
    elif _sw1 == PERIOD_MN1:
        tf = 'mn1'
    else:
        tf = 'Unknown'
    if (RGBRed > 255 or RGBGreen > 255) or RGBBlue > 255:
        Alert('Watermark Red/Green/Blue components must each be in range 0..255')
    RGB_v = _int(RGBBlue << 16)
    RGB_v |= _int(RGBGreen << 8)
    RGB_v |= RGBRed
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    watermark(Pair, tf + Symbol(), FontSize, FontName, RGB_v, XPos, YPos)
    return rates_total

def watermark(obj, text, fontSize, fontName, colour, xPos, yPos):
    ObjectCreate(0, obj, OBJ_LABEL, 0, 0, 0)
    ObjectSetString(0, obj, OBJPROP_TEXT, text)
    ObjectSetInteger(0, obj, OBJPROP_COLOR, colour)
    ObjectSetString(0, obj, OBJPROP_FONT, fontName)
    ObjectSetInteger(0, obj, OBJPROP_FONTSIZE, fontSize)
    ObjectSetInteger(0, obj, OBJPROP_CORNER, BASE_CORNER)
    ObjectSetInteger(0, obj, OBJPROP_XDISTANCE, xPos)
    ObjectSetInteger(0, obj, OBJPROP_YDISTANCE, yPos)
    ObjectSetInteger(0, obj, OBJPROP_BACK, True)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PairOrSymbolAndTimeFrameWithWatermark(_MQL5Indicator):
    name = 'Pair Or Symbol And Time Frame With Watermark'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BASE_CORNER': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=2),
        'FontSize': 45,
        'RGBRed': 30,
        'RGBGreen': 30,
        'RGBBlue': 30,
        'XPos': 400,
        'YPos': 70,
    }

