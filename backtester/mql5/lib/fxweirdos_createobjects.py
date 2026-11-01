"""createObjects.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

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

def vSetBackground(sName, sub_window, xx, yy, width, height):
    ObjectCreate(0, sName, OBJ_RECTANGLE_LABEL, sub_window, 0, 0)
    ObjectSetInteger(0, sName, OBJPROP_XDISTANCE, xx)
    ObjectSetInteger(0, sName, OBJPROP_YDISTANCE, yy)
    ObjectSetInteger(0, sName, OBJPROP_XSIZE, width)
    ObjectSetInteger(0, sName, OBJPROP_YSIZE, height)
    ObjectSetInteger(0, sName, OBJPROP_BGCOLOR, 0x1F1613)
    ObjectSetInteger(0, sName, OBJPROP_SELECTABLE, False)

def vSetArrow(lChartid, sName, sub_window, dtTime, dPrice, iFontWidth, cFontColor, iArrowCode):
    ObjectCreate(lChartid, sName, OBJ_ARROW, sub_window, dtTime, dPrice)
    ObjectSetInteger(lChartid, sName, OBJPROP_ARROWCODE, iArrowCode)
    ObjectSetInteger(lChartid, sName, OBJPROP_WIDTH, iFontWidth)
    ObjectSetInteger(lChartid, sName, OBJPROP_COLOR, cFontColor)

def vSetText(lChartid, sName, sub_window, dtTime, dPrice, iFontWidth, cFontColor, sText):
    ObjectCreate(lChartid, sName, OBJ_TEXT, sub_window, dtTime, dPrice)
    ObjectSetString(lChartid, sName, OBJPROP_TEXT, sText)
    ObjectSetInteger(lChartid, sName, OBJPROP_FONTSIZE, iFontWidth)
    ObjectSetInteger(lChartid, sName, OBJPROP_COLOR, cFontColor)

def vSetLabel(lChartid, sName, sub_window, xx, yy, iFontSize, cFontColor, sText):
    ObjectCreate(lChartid, sName, OBJ_LABEL, sub_window, 0, 0)
    ObjectSetInteger(lChartid, sName, OBJPROP_YDISTANCE, xx)
    ObjectSetInteger(lChartid, sName, OBJPROP_XDISTANCE, yy)
    ObjectSetInteger(lChartid, sName, OBJPROP_COLOR, cFontColor)
    ObjectSetInteger(lChartid, sName, OBJPROP_FONTSIZE, iFontSize)
    ObjectSetString(lChartid, sName, OBJPROP_TEXT, 0, sText)

__all__ = ['vSetRectangle', 'vSetBackground', 'vSetArrow', 'vSetText', 'vSetLabel']
