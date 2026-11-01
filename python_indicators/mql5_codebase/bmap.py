"""bmap — converted from MQL5: MQL5 Indicators/Customised bmap chart/bmap.mq5

========================================================
DESARROLLADO POR OSCAR MANTILLA
========================================================
Copyright: Copyright 2025, MetaQuotes Ltd.; Link: https://www.mql5.com/es/users/popar; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, MetaQuotes Ltd.', 'link': 'https://www.mql5.com/es/users/popar', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1}, 'types': {}, 'colors': {1: [4294967295]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['========================================================', 'DESARROLLADO POR OSCAR MANTILLA', '========================================================'], 'name': 'bmap', 'source': 'MQL5 Indicators/Customised bmap chart/bmap.mq5', 'folder': 'Customised bmap chart', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
emptyBuffer = Arr(0, 0.0)
width_center = -240  # Ancho de la imagen (negativo para tomar dimensiones reales del archivo BMP)
height_center = 450  # Alto de la imagen

def OnInit():
    if not ObjectCreate(0, 'centerImage', OBJ_BITMAP_LABEL, 0, 0, 0):
        Print('Failed to create center image object. Error code = ', GetLastError())
        return INIT_FAILED
    ObjectSetString(0, 'centerImage', OBJPROP_BMPFILE, '\\Images\\2.bmp')
    ObjectSetInteger(0, 'centerImage', OBJPROP_BACK, True)
    ObjectSetInteger(0, 'centerImage', OBJPROP_CORNER, 3)
    UpdateBitmapPosition()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    UpdateBitmapPosition()
    return rates_total

def UpdateBitmapPosition():
    x_distance = Box(0)
    y_distance = Box(0)
    if not ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0, x_distance):
        Print('Failed to get the chart width! Error code = ', GetLastError())
        return
    if not ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, 0, y_distance):
        Print('Failed to get the chart height! Error code = ', GetLastError())
        return
    x_center = _idiv(_int(x_distance.v - width_center), 2)
    y_center = _idiv(_int(y_distance.v - height_center), 2)
    ObjectSetInteger(0, 'centerImage', OBJPROP_XDISTANCE, x_center)
    ObjectSetInteger(0, 'centerImage', OBJPROP_YDISTANCE, y_center)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bmap(_MQL5Indicator):
    name = 'bmap'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

