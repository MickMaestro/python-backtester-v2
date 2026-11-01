"""Moving PriceLine — converted from MQL5: MQL5 Indicators/Moving Price Line Indicator MT5/Moving PriceLine.mq5

MovingPriceLine - To show current server time on the last candle
Copyright: 2003-2025, Opengates Success International Org.; Link: https://www.mql5.com/en/users/opengates2012/seller

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2003-2025, Opengates Success International Org.', 'link': 'https://www.mql5.com/en/users/opengates2012/seller', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['MovingPriceLine - To show current server time on the last candle'], 'name': 'Moving PriceLine', 'source': 'MQL5 Indicators/Moving Price Line Indicator MT5/Moving PriceLine.mq5', 'folder': 'Moving Price Line Indicator MT5', 'inputs': [{'mql': 'LineColor', 'py': 'LineColor', 'param': None, 'type': 'color', 'default': 5197615, 'label': 'Color for the line', 'sinput': False}, {'mql': 'TextColor', 'py': 'TextColor', 'param': None, 'type': 'color', 'default': 14599344, 'label': 'Color for the time text', 'sinput': False}, {'mql': 'LineWidth', 'py': 'LineWidth', 'param': 'LineWidth', 'type': 'int', 'default': 1, 'label': 'The width of the line', 'sinput': False}, {'mql': 'LineStyle', 'py': 'LineStyle', 'param': 'LineStyle', 'type': 'int', 'default': 0, 'label': 'The style of the line', 'sinput': False}, {'mql': 'BufferPips', 'py': 'BufferPips', 'param': 'BufferPips', 'type': 'double', 'default': 3.0, 'label': 'Distance above candle high in pips', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LineColor = _input('LineColor', clrDarkSlateGray)  # Color for the line
TextColor = _input('TextColor', clrLightSteelBlue)  # Color for the time text
LineWidth = _input('LineWidth', 1)  # The width of the line
LineStyle = _input('LineStyle', STYLE_SOLID)  # The style of the line
BufferPips = _input('BufferPips', 3.0)  # Distance above candle high in pips
LineName = 'MovingPriceLine_Timer'
TextName = 'MovingPriceLine_Name'

def OnInit():
    if not ObjectCreate(0, LineName, OBJ_VLINE, 0, TimeCurrent(), 0):
        Print('Failed to create vertical line. Error: ', GetLastError())
        return INIT_FAILED
    ObjectSetInteger(0, LineName, OBJPROP_COLOR, LineColor)
    ObjectSetInteger(0, LineName, OBJPROP_WIDTH, LineWidth)
    ObjectSetInteger(0, LineName, OBJPROP_STYLE, LineStyle)
    ObjectSetInteger(0, LineName, OBJPROP_BACK, True)
    ObjectSetInteger(0, LineName, OBJPROP_SELECTABLE, False)
    ObjectCreate(0, TextName, OBJ_TEXT, 0, TimeCurrent(), 0)
    ObjectSetInteger(0, TextName, OBJPROP_COLOR, TextColor)
    ObjectSetInteger(0, TextName, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, TextName, OBJPROP_SELECTABLE, False)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, LineName)
    ObjectDelete(0, TextName)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    now = TimeCurrent()
    currentCandleIndex = rates_total - 1
    candleTime = time[currentCandleIndex]
    candleHigh = high[currentCandleIndex]
    pipSize = Point() * 10 * (10 if (Digits() == 3 or Digits() == 5) else 1)
    bufferPrice = BufferPips * pipSize
    textY = candleHigh + bufferPrice
    add = ""
    ObjectMove(0, LineName, 0, now, 0)
    if now < 12.0:
        add = 'AM'
    else:
        add = 'PM'
    label = TimeToString(now, TIME_SECONDS) + ' ' + add
    ObjectMove(0, TextName, 0, now, textY)
    ObjectSetString(0, TextName, OBJPROP_TEXT, label)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MovingPriceLine(_MQL5Indicator):
    name = 'Moving PriceLine'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LineWidth': 1,  # The width of the line
        'LineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # The style of the line
        'BufferPips': 3.0,  # Distance above candle high in pips
    }

