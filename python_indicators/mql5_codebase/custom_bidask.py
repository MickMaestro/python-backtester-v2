"""Custom BidAsk — converted from MQL5: MQL5 Indicators/Custom Bid Ask lines/Custom BidAsk.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Custom BidAsk', 'source': 'MQL5 Indicators/Custom Bid Ask lines/Custom BidAsk.mq5', 'folder': 'Custom Bid Ask lines', 'inputs': [{'mql': 'show_bid', 'py': 'show_bid', 'param': 'show_bid', 'type': 'bool', 'default': True, 'label': 'Show the bid', 'sinput': False}, {'mql': 'show_ask', 'py': 'show_ask', 'param': 'show_ask', 'type': 'bool', 'default': True, 'label': 'Show the ask', 'sinput': False}, {'mql': 'bid_line_width', 'py': 'bid_line_width', 'param': 'bid_line_width', 'type': 'int', 'default': 1, 'label': 'Size of Bid line', 'sinput': False}, {'mql': 'ask_line_width', 'py': 'ask_line_width', 'param': 'ask_line_width', 'type': 'int', 'default': 1, 'label': 'Size of Ask line', 'sinput': False}, {'mql': 'bid_line_color', 'py': 'bid_line_color', 'param': None, 'type': 'color', 'default': 12632256, 'label': 'Color of Bid line', 'sinput': False}, {'mql': 'ask_line_color', 'py': 'ask_line_color', 'param': None, 'type': 'color', 'default': 8388736, 'label': 'Color of Ask line', 'sinput': False}, {'mql': 'show_text', 'py': 'show_text', 'param': 'show_text', 'type': 'bool', 'default': True, 'label': 'Show Bid/Ask text', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
show_bid = _input('show_bid', True)  # Show the bid
show_ask = _input('show_ask', True)  # Show the ask
bid_line_width = _input('bid_line_width', 1)  # Size of Bid line
ask_line_width = _input('ask_line_width', 1)  # Size of Ask line
bid_line_color = _input('bid_line_color', clrSilver)  # Color of Bid line
ask_line_color = _input('ask_line_color', clrPurple)  # Color of Ask line
show_text = _input('show_text', True)  # Show Bid/Ask text
bid_text_size = 8  # Font size for Bid text
ask_text_size = 8  # Font size for Ask text
bid_obj_name = ""
bid_text_obj_name = ""
ask_obj_name = ""
ask_text_obj_name = ""

def OnInit():
    global ask_obj_name, ask_text_obj_name, bid_obj_name, bid_text_obj_name
    bid_obj_name = 'Bid'
    bid_text_obj_name = '_BidText'
    ask_obj_name = 'Ask'
    ask_text_obj_name = '_AskText'
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
    if show_bid:
        if ObjectFind(0, bid_obj_name) == -1:
            ObjectCreate(0, bid_obj_name, OBJ_HLINE, 0, 0, bid)
        ObjectSetDouble(0, bid_obj_name, OBJPROP_PRICE, bid)
        ObjectSetInteger(0, bid_obj_name, OBJPROP_STYLE, DRAW_LINE)
        ObjectSetInteger(0, bid_obj_name, OBJPROP_WIDTH, bid_line_width)
        ObjectSetInteger(0, bid_obj_name, OBJPROP_COLOR, bid_line_color)
        if show_text:
            Text(0, bid_text_obj_name, 'Bid', bid, bid_text_size, bid_line_color, time[70])
        else:
            if ObjectFind(0, bid_text_obj_name) != -1:
                ObjectDelete(0, bid_text_obj_name)
    else:
        if ObjectFind(0, bid_obj_name) != -1:
            ObjectDelete(0, bid_obj_name)
        if ObjectFind(0, bid_text_obj_name) != -1:
            ObjectDelete(0, bid_text_obj_name)
    if show_ask:
        if ObjectFind(0, ask_obj_name) == -1:
            ObjectCreate(0, ask_obj_name, OBJ_HLINE, 0, 0, ask)
        ObjectSetDouble(0, ask_obj_name, OBJPROP_PRICE, ask)
        ObjectSetInteger(0, ask_obj_name, OBJPROP_STYLE, DRAW_LINE)
        ObjectSetInteger(0, ask_obj_name, OBJPROP_WIDTH, ask_line_width)
        ObjectSetInteger(0, ask_obj_name, OBJPROP_COLOR, ask_line_color)
        dynamic_offset = (ChartGetDouble(0, CHART_PRICE_MAX) - ChartGetDouble(0, CHART_PRICE_MIN)) * 0.036
        if show_text:
            Text(0, ask_text_obj_name, 'Ask', ask + dynamic_offset, ask_text_size, ask_line_color, time[70])
        else:
            if ObjectFind(0, ask_text_obj_name) != -1:
                ObjectDelete(0, ask_text_obj_name)
    else:
        if ObjectFind(0, ask_obj_name) != -1:
            ObjectDelete(0, ask_obj_name)
        if ObjectFind(0, ask_text_obj_name) != -1:
            ObjectDelete(0, ask_text_obj_name)
    return rates_total

def Text(id_, name, text, distance, fontSize, fontColor, time):
    if ObjectFind(0, name) == -1:
        ObjectCreate(id_, name, OBJ_TEXT, 0, time, distance)
    ObjectSetInteger(id_, name, OBJPROP_CORNER, 0)
    ObjectSetInteger(id_, name, OBJPROP_FONTSIZE, fontSize)
    ObjectSetInteger(id_, name, OBJPROP_COLOR, fontColor)
    ObjectSetString(id_, name, OBJPROP_TEXT, text)
    ObjectSetDouble(id_, name, OBJPROP_PRICE, distance)

def OnDeinit(reason):
    ObjectDelete(0, bid_obj_name)
    ObjectDelete(0, bid_text_obj_name)
    ObjectDelete(0, ask_obj_name)
    ObjectDelete(0, ask_text_obj_name)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomBidAsk(_MQL5Indicator):
    name = 'Custom BidAsk'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'show_bid': True,  # Show the bid
        'show_ask': True,  # Show the ask
        'bid_line_width': 1,  # Size of Bid line
        'ask_line_width': 1,  # Size of Ask line
        'show_text': True,  # Show Bid/Ask text
    }

