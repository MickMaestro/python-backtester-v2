"""riskrewardbox — converted from MQL5: MQL5 Indicators/Risk reward box/riskrewardbox.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'riskrewardbox', 'source': 'MQL5 Indicators/Risk reward box/riskrewardbox.mq5', 'folder': 'Risk reward box', 'inputs': [{'mql': 'DrawAllChart', 'py': 'DrawAllChart', 'param': 'DrawAllChart', 'type': 'bool', 'default': False, 'label': 'Draw Box on all opened charts', 'sinput': False}, {'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16385, 'label': 'Cart timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
DrawAllChart = _input('DrawAllChart', False)  # Draw Box on all opened charts
TimeFrame = _input('TimeFrame', PERIOD_H1)  # Cart timeframe
OBJprefix = 'ziwoxRSRW'

def OnInit():
    ChartDraw()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    chartID = ChartFirst()
    symb = ''
    ChartPer = 0
    if DrawAllChart:
        while chartID >= 0:
            ObjectsDeleteAll(chartID, OBJprefix, -1, -1)
            chartID = ChartNext(chartID)
    else:
        ObjectsDeleteAll(0, OBJprefix, -1, -1)
    ObjectDelete(0, 'Reset')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ButtonCreate(0, 'Reset', 0, 20, 30, 110, 25, CORNER_LEFT_UPPER, 'Reset All Box', 'Trebuchet MS', 10, clrWhite, clrMediumSeaGreen, clrMediumSeaGreen, False, False, False, True, 1, '')
    return 1

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_OBJECT_CLICK:
        if sparam == 'Reset':
            ChartClean()
    if id_ == CHARTEVENT_OBJECT_DRAG:
        pricePink1 = ObjectGetDouble(0, OBJprefix + '.Risk_Reward_Pink', OBJPROP_PRICE, 0)
        pricePink2 = ObjectGetDouble(0, OBJprefix + '.Risk_Reward_Pink', OBJPROP_PRICE, 1)
        priceGreen1 = ObjectGetDouble(0, OBJprefix + '.Risk_Reward_Green', OBJPROP_PRICE, 0)
        priceGreen2 = ObjectGetDouble(0, OBJprefix + '.Risk_Reward_Green', OBJPROP_PRICE, 1)
        maxPink = MathMax(pricePink1, pricePink2)
        minPink = MathMin(pricePink1, pricePink2)
        maxGreen = MathMax(priceGreen1, priceGreen2)
        minGreen = MathMin(priceGreen1, priceGreen2)
        if sparam == (OBJprefix + '.Risk_Reward_Green'):
            pinkSize = maxPink - minPink
            time1 = ObjectGetInteger(0, OBJprefix + '.Risk_Reward_Green', OBJPROP_TIME, 0)
            time2 = ObjectGetInteger(0, OBJprefix + '.Risk_Reward_Green', OBJPROP_TIME, 1)
            if maxPink > maxGreen:
                ObjectSetDouble(0, OBJprefix + '.Risk_Reward_Pink', OBJPROP_PRICE, 0, maxGreen)
                ObjectSetDouble(0, OBJprefix + '.Risk_Reward_Pink', OBJPROP_PRICE, 1, maxGreen + pinkSize)
            else:
                ObjectSetDouble(0, OBJprefix + '.Risk_Reward_Pink', OBJPROP_PRICE, 1, minGreen)
                ObjectSetDouble(0, OBJprefix + '.Risk_Reward_Pink', OBJPROP_PRICE, 0, minGreen - pinkSize)
            ObjectSetInteger(0, OBJprefix + '.Risk_Reward_Pink', OBJPROP_TIME, 0, time1)
            ObjectSetInteger(0, OBJprefix + '.Risk_Reward_Pink', OBJPROP_TIME, 1, time2)
            ChartRedraw(0)
        if sparam == (OBJprefix + '.Risk_Reward_Pink'):
            greeSize = maxGreen - minGreen
            time1 = ObjectGetInteger(0, OBJprefix + '.Risk_Reward_Pink', OBJPROP_TIME, 0)
            time2 = ObjectGetInteger(0, OBJprefix + '.Risk_Reward_Pink', OBJPROP_TIME, 1)
            if maxGreen > maxPink:
                ObjectSetDouble(0, OBJprefix + '.Risk_Reward_Green', OBJPROP_PRICE, 0, maxPink)
                ObjectSetDouble(0, OBJprefix + '.Risk_Reward_Green', OBJPROP_PRICE, 1, maxPink + greeSize)
            else:
                ObjectSetDouble(0, OBJprefix + '.Risk_Reward_Green', OBJPROP_PRICE, 1, minPink)
                ObjectSetDouble(0, OBJprefix + '.Risk_Reward_Green', OBJPROP_PRICE, 0, minPink - greeSize)
            ObjectSetInteger(0, OBJprefix + '.Risk_Reward_Green', OBJPROP_TIME, 0, time1)
            ObjectSetInteger(0, OBJprefix + '.Risk_Reward_Green', OBJPROP_TIME, 1, time2)
            ChartRedraw(0)

def ButtonCreate(chart_ID=0, name='Button', sub_window=0, x=0, y=0, width=50, height=18, corner=CORNER_LEFT_UPPER, text='Button', font='Arial', font_size=10, clr=clrBlack, back_clr=0xD8E9EC, border_clr=clrNONE, state=False, back=False, selection=False, hidden=True, z_order=0, tooltip='\n'):
    ResetLastError()
    if ObjectFind(chart_ID, name) != 0:
        if not ObjectCreate(chart_ID, name, OBJ_BUTTON, sub_window, 0, 0):
            Print('ButtonCreate', ': failed to create the button! Error code = ', GetLastError())
            return False
        ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
        ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
        ObjectSetInteger(chart_ID, name, OBJPROP_XSIZE, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_YSIZE, height)
        ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
        ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
        ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
        ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BGCOLOR, back_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BORDER_COLOR, border_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_STATE, state)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        ObjectSetString(chart_ID, name, OBJPROP_TOOLTIP, tooltip)
    else:
        ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
        ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
        ObjectSetInteger(chart_ID, name, OBJPROP_XSIZE, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_YSIZE, height)
        ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
        ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
        ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
        ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BGCOLOR, back_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BORDER_COLOR, border_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_STATE, state)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        ObjectSetString(chart_ID, name, OBJPROP_TOOLTIP, tooltip)
    return True

def ChartClean():
    chartID = ChartFirst()
    symb = ''
    ChartPer = 0
    if DrawAllChart:
        while chartID >= 0:
            ObjectsDeleteAll(chartID, OBJprefix, -1, -1)
            chartID = ChartNext(chartID)
    else:
        ObjectsDeleteAll(0, OBJprefix, -1, -1)
    ObjectSetInteger(0, 'Reset', OBJPROP_STATE, False)
    ChartDraw()

def ChartDraw():
    chart_ID = ChartFirst()
    symbl = ''
    chartperiod = 0
    if DrawAllChart:
        while chart_ID >= 0:
            symbl = ChartSymbol(chart_ID)
            chartperiod = ChartPeriod(chart_ID)
            name = OBJprefix + '.Risk_Reward_Pink'
            top = iHigh(symbl, chartperiod, iHighest(symbl, chartperiod, MODE_HIGH, 20, 0))
            low = iLow(symbl, chartperiod, iLowest(symbl, chartperiod, MODE_LOW, 20, 0))
            mid = SymbolInfoDouble(symbl, SYMBOL_ASK)
            if ObjectFind(chart_ID, name) < 0:
                ObjectCreate(chart_ID, name, OBJ_RECTANGLE, 0, iTime(symbl, chartperiod, 0), low, iTime(symbl, chartperiod, 0) + (PeriodSeconds() * 25), mid)
                ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clrPink)
                ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, STYLE_SOLID)
                ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, 2)
                ObjectSetInteger(chart_ID, name, OBJPROP_FILL, True)
                ObjectSetInteger(chart_ID, name, OBJPROP_BACK, True)
                ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, True)
                ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, True)
                ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, False)
                ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, 0)
            name = OBJprefix + '.Risk_Reward_Green'
            if ObjectFind(chart_ID, name) < 0:
                ObjectCreate(chart_ID, name, OBJ_RECTANGLE, 0, iTime(symbl, chartperiod, 0), mid, iTime(symbl, chartperiod, 0) + (PeriodSeconds() * 25), top)
                ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clrLightGreen)
                ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, STYLE_SOLID)
                ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, 2)
                ObjectSetInteger(chart_ID, name, OBJPROP_FILL, True)
                ObjectSetInteger(chart_ID, name, OBJPROP_BACK, True)
                ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, True)
                ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, True)
                ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, False)
                ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, 0)
            chart_ID = ChartNext(chart_ID)
    else:
        chart_ID = 0
        symbl = Symbol()
        chartperiod = PERIOD_CURRENT
        name = OBJprefix + '.Risk_Reward_Pink'
        top = iHigh(symbl, chartperiod, iHighest(symbl, chartperiod, MODE_HIGH, 20, 0))
        low = iLow(symbl, chartperiod, iLowest(symbl, chartperiod, MODE_LOW, 20, 0))
        mid = SymbolInfoDouble(symbl, SYMBOL_ASK)
        if ObjectFind(chart_ID, name) < 0:
            ObjectCreate(chart_ID, name, OBJ_RECTANGLE, 0, iTime(symbl, chartperiod, 0), low, iTime(symbl, chartperiod, 0) + (PeriodSeconds() * 25), mid)
            ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clrPink)
            ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, STYLE_SOLID)
            ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, 2)
            ObjectSetInteger(chart_ID, name, OBJPROP_FILL, True)
            ObjectSetInteger(chart_ID, name, OBJPROP_BACK, True)
            ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, True)
            ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, False)
            ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, 0)
        name = OBJprefix + '.Risk_Reward_Green'
        if ObjectFind(chart_ID, name) < 0:
            ObjectCreate(chart_ID, name, OBJ_RECTANGLE, 0, iTime(symbl, chartperiod, 0), mid, iTime(symbl, chartperiod, 0) + (PeriodSeconds() * 25), top)
            ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clrLightGreen)
            ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, STYLE_SOLID)
            ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, 2)
            ObjectSetInteger(chart_ID, name, OBJPROP_FILL, True)
            ObjectSetInteger(chart_ID, name, OBJPROP_BACK, True)
            ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, True)
            ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, True)
            ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, False)
            ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Riskrewardbox(_MQL5Indicator):
    name = 'riskrewardbox'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DrawAllChart': False,  # Draw Box on all opened charts
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Cart timeframe
    }

