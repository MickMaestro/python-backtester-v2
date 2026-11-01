"""iSpread — converted from MQL5: MQL5 Indicators/iSpread/iSpread.mq5

Copyright: Copyright 2015, Serj_Che.; Link: https://www.mql5.com/ru/users/serj_che; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, Serj_Che.', 'link': 'https://www.mql5.com/ru/users/serj_che', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': 0.0}, 'types': {1: 10}, 'colors': {1: [9639167, 14772545]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'iSpread', 'source': 'MQL5 Indicators/iSpread/iSpread.mq5', 'folder': 'iSpread', 'inputs': [{'mql': 'Count', 'py': 'Count', 'param': 'Count', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

LimeGreen = 0x32CD32  # MQL4 colour name

# ---- inputs and global variables
Count = _input('Count', 20)
ExtSpreadBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtSpreadBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Spread(' + IntegerToString(Count) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, LimeGreen)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.1)

def OnDeinit(reason):
    ObjectDelete(0, 'spread')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 2:
        return 0
    start = prev_calculated - 1
    if start < 1:
        start = 1
    CalculateSpread(start, rates_total, spread)
    minimum = ArrayMinimum(ExtSpreadBuffer, rates_total - Count, Count)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, spread[minimum])
    SymbolInfoTick(Symbol(), tick)
    if ObjectFind(0, 'spread') < 0:
        sub_wnd = ChartWindowFind()
        ObjectCreate(0, 'spread', OBJ_LABEL, sub_wnd, 0, 0)
        ObjectSetInteger(0, 'spread', OBJPROP_XDISTANCE, 10)
        ObjectSetInteger(0, 'spread', OBJPROP_YDISTANCE, 5)
        ObjectSetInteger(0, 'spread', OBJPROP_COLOR, clrRed)
        ObjectSetInteger(0, 'spread', OBJPROP_FONTSIZE, 12)
        ObjectSetString(0, 'spread', OBJPROP_FONT, 'Courier New')
        ObjectSetInteger(0, 'spread', OBJPROP_CORNER, CORNER_RIGHT_UPPER)
        ObjectSetInteger(0, 'spread', OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
        ObjectSetInteger(0, 'spread', OBJPROP_SELECTABLE, False)
    ObjectSetString(0, 'spread', OBJPROP_TEXT, StringFormat('Current Spread:%3i', _int(_fdiv(tick.ask - tick.bid, Point())), 0))
    return rates_total

def CalculateSpread(nPosition, nRatesCount, SrcBuffer):
    ExtSpreadBuffer[0] = float(SrcBuffer[0])
    ExtColorsBuffer[0] = 0.0
    for i in range(nPosition, nRatesCount):
        dCurrSpread = float(SrcBuffer[i])
        dPrevSpread = float(SrcBuffer[i - 1])
        ExtSpreadBuffer[i] = dCurrSpread
        if dCurrSpread > dPrevSpread:
            ExtColorsBuffer[i] = 0.0
        else:
            ExtColorsBuffer[i] = 1.0

# ---- global variables initialised from expressions
tick = MqlTick()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ISpread(_MQL5Indicator):
    name = 'iSpread'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Count': 20,
    }

