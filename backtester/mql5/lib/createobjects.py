"""CreateObjects.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


def vSetRectangle(name, sub_window, xx, yy, width, height, bg_color, border_clr, border_width):
    ObjectCreate(0, name, OBJ_RECTANGLE_LABEL, sub_window, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, xx)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, yy)
    ObjectSetInteger(0, name, OBJPROP_XSIZE, width)
    ObjectSetInteger(0, name, OBJPROP_YSIZE, height)
    ObjectSetInteger(0, name, OBJPROP_COLOR, border_clr)
    ObjectSetInteger(0, name, OBJPROP_BGCOLOR, bg_color)
    ObjectSetInteger(0, name, OBJPROP_BORDER_TYPE, BORDER_FLAT)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, border_width)
    ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER)
    ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(0, name, OBJPROP_BACK, False)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, 0)
    ObjectSetInteger(0, name, OBJPROP_SELECTED, 0)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, False)
    ObjectSetInteger(0, name, OBJPROP_ZORDER, 0)

def vSetLabel(sName, sub_window, xx, yy, cFontColor, iFontSize, sText):
    ObjectCreate(0, sName, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, sName, OBJPROP_YDISTANCE, xx)
    ObjectSetInteger(0, sName, OBJPROP_XDISTANCE, yy)
    ObjectSetInteger(0, sName, OBJPROP_COLOR, cFontColor)
    ObjectSetInteger(0, sName, OBJPROP_WIDTH, FW_BOLD)
    ObjectSetInteger(0, sName, OBJPROP_FONTSIZE, iFontSize)
    ObjectSetString(0, sName, OBJPROP_TEXT, 0, sText)

__all__ = ['vSetRectangle', 'vSetLabel']
