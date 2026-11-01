"""IND_RiskOverall — converted from MQL5: MQL5 Indicators/IND - The Overall Percent Risk - MT5/IND_RiskOverall.mq5

Copyright: Copyright 2021, FxWeirdos. Mario Gharib. Forex Jarvis. info@fxweirdos.com; Link: https://fxweirdos.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, FxWeirdos. Mario Gharib. Forex Jarvis. info@fxweirdos.com', 'link': 'https://fxweirdos.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'IND_RiskOverall', 'source': 'MQL5 Indicators/IND - The Overall Percent Risk - MT5/IND_RiskOverall.mq5', 'folder': 'IND - The Overall Percent Risk - MT5', 'inputs': [{'mql': 'cFontClr', 'py': 'cFontClr', 'param': None, 'type': 'color', 'default': 2402047, 'label': 'FONT COLOR', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
dAmtRisking = 0.0
dAmtRewarding = 0.0
cFontClr = _input('cFontClr', 0x24A6FF)  # FONT COLOR
dp = 0.0
pipPos = 0.0
dNbPips = 0.0
PipValue = 0.0

def vSetLabel(sName, sub_window, xx, yy, cFontColor, iFontSize, sText):
    ObjectCreate(0, sName, OBJ_LABEL, sub_window, 0, 0)
    ObjectSetInteger(0, sName, OBJPROP_YDISTANCE, xx)
    ObjectSetInteger(0, sName, OBJPROP_XDISTANCE, yy)
    ObjectSetInteger(0, sName, OBJPROP_COLOR, cFontColor)
    ObjectSetInteger(0, sName, OBJPROP_WIDTH, FW_BOLD)
    ObjectSetInteger(0, sName, OBJPROP_FONTSIZE, iFontSize)
    ObjectSetString(0, sName, OBJPROP_TEXT, 0, sText)
    ObjectSetInteger(0, sName, OBJPROP_SELECTABLE, False)

def vSetBackground(sName, sub_window, xx, yy, width, height):
    ObjectCreate(0, sName, OBJ_RECTANGLE_LABEL, sub_window, 0, 0)
    ObjectSetInteger(0, sName, OBJPROP_XDISTANCE, xx)
    ObjectSetInteger(0, sName, OBJPROP_YDISTANCE, yy)
    ObjectSetInteger(0, sName, OBJPROP_XSIZE, width)
    ObjectSetInteger(0, sName, OBJPROP_YSIZE, height)
    ObjectSetInteger(0, sName, OBJPROP_BGCOLOR, 0x1F1613)
    ObjectSetInteger(0, sName, OBJPROP_SELECTABLE, False)

def dValuePips(sSymbol, dPrice, dSLTP, dVolume):
    global PipValue, dNbPips, dp, pipPos
    dp = 0.0
    if (SymbolInfoInteger(sSymbol, SYMBOL_DIGITS) == 1 or SymbolInfoInteger(sSymbol, SYMBOL_DIGITS) == 3) or SymbolInfoInteger(sSymbol, SYMBOL_DIGITS) == 5:
        dp = 10.0
    else:
        dp = 1.0
    pipPos = SymbolInfoDouble(sSymbol, SYMBOL_POINT) * dp
    dNbPips = NormalizeDouble(MathAbs(_fdiv(dPrice - dSLTP, pipPos)), 1)
    PipValue = _fdiv(SymbolInfoDouble(sSymbol, SYMBOL_TRADE_TICK_VALUE) * pipPos, SymbolInfoDouble(sSymbol, SYMBOL_TRADE_TICK_SIZE))
    if (StringFind(sSymbol, 'XAU') >= 0 and StringFind(sSymbol, 'USD') >= 0) and PipValue == 0.1:
        PipValue = PipValue * 10
    elif (StringFind(sSymbol, 'XAG') >= 0 and StringFind(sSymbol, 'USD') >= 0) and PipValue == 5.0:
        PipValue = PipValue * 10
    return NormalizeDouble(dNbPips * PipValue * dVolume, 2)

def OnInit():
    ChartSetInteger(0, CHART_COLOR_BID, 0x1F1613)
    ChartSetInteger(0, CHART_COLOR_ASK, 0x1F1613)
    ChartSetInteger(0, CHART_COLOR_BACKGROUND, 0x1F1613)
    ChartSetInteger(0, CHART_COLOR_FOREGROUND, 0x1F1613)
    ChartSetInteger(0, CHART_COLOR_CANDLE_BEAR, 0x1F1613)
    ChartSetInteger(0, CHART_COLOR_CANDLE_BULL, 0x1F1613)
    ChartSetInteger(0, CHART_COLOR_CHART_DOWN, 0x1F1613)
    ChartSetInteger(0, CHART_COLOR_CHART_UP, 0x1F1613)
    ChartSetInteger(0, CHART_COLOR_CHART_LINE, 0x1F1613)
    ChartSetInteger(0, CHART_COLOR_GRID, 0x1F1613)
    ChartSetInteger(0, CHART_SHOW_ONE_CLICK, False)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global dAmtRewarding, dAmtRisking
    dAmtRisking = 0.0
    dAmtRewarding = 0.0
    j = 0
    while j < PositionsTotal():
        PositionTicket = PositionGetTicket(j)
        if PositionSelectByTicket(PositionTicket):
            if OrderGetInteger(ORDER_TYPE) == 0 or OrderGetInteger(ORDER_TYPE) == 1:
                dAmtRisking = dAmtRisking + dValuePips(PositionGetString(POSITION_SYMBOL), PositionGetDouble(POSITION_PRICE_OPEN), PositionGetDouble(POSITION_SL), PositionGetDouble(POSITION_VOLUME))
                dAmtRewarding = dAmtRewarding + dValuePips(PositionGetString(POSITION_SYMBOL), PositionGetDouble(POSITION_PRICE_OPEN), PositionGetDouble(POSITION_TP), PositionGetDouble(POSITION_VOLUME))
        j += 1
    vSetLabel('OVERALLRISK', 0, 25, 20, cFontClr, 10, 'Overall Risk: ' + DoubleToString(_fdiv(dAmtRisking, AccountInfoDouble(ACCOUNT_BALANCE)) * 100, 2) + '%')
    vSetLabel('OVERALLTARGET', 0, 45, 20, cFontClr, 10, 'Overall Target: ' + DoubleToString(_fdiv(dAmtRewarding, AccountInfoDouble(ACCOUNT_BALANCE)) * 100, 2) + '%')
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class INDRiskOverall(_MQL5Indicator):
    name = 'IND_RiskOverall'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

