"""Daily Drawdown — converted from MQL5: MQL5 Indicators/daily drawdown/Daily Drawdown.mq5

Speed, Accuracy, Intelligence
Three Essential Components for Scalp Trading
Using this tool, we allow you to manage capital, send orders quickly and save automatic profits. 
\\nStay in touch with us
\\nWe are programming for you for free
\\nTelegram(@SAI_Programmer)
WhatsApp(+989198824764)
Instagram(@SAI_Forex)
Copyright: Copyright 2021, SAI_Programmer.; Link: https://www.mql5.com/en/users/sai_programmer/seller

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, SAI_Programmer.', 'link': 'https://www.mql5.com/en/users/sai_programmer/seller', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Speed, Accuracy, Intelligence', 'Three Essential Components for Scalp Trading', 'Using this tool, we allow you to manage capital, send orders quickly and save automatic profits. ', '\\nStay in touch with us', '\\nWe are programming for you for free', '\\nTelegram(@SAI_Programmer)', 'WhatsApp(+989198824764)', 'Instagram(@SAI_Forex)'], 'name': 'Daily Drawdown', 'source': 'MQL5 Indicators/daily drawdown/Daily Drawdown.mq5', 'folder': 'daily drawdown', 'inputs': [{'mql': 'InpDDD', 'py': 'InpDDD', 'param': 'InpDDD', 'type': 'bool', 'default': True, 'label': 'Daily drowdown active:', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpDDD = _input('InpDDD', True)  # Daily drowdown active:

def OnInit():
    CreateEdit('Daily DD', 200, 68, 98, 30, 'Daily DD', clrWhite, clrBlack, 12)
    CreateEdit('Daily DD V', 100, 68, 98, 30, '', clrWhite, clrBlack, 12)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, 'Daily DD')
    ObjectDelete(0, 'Daily DD V')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    w = MqlDateTime()
    TimeToStruct(TimeCurrent(), w)
    md = IntegerToString(w.year) + '.' + IntegerToString(w.mon) + '.01'
    historyProfit = 0.0
    deposit = 0.0
    HistorySelect(0, TimeCurrent())
    ticket_history_deal = 0
    i = 0
    while i < HistoryDealsTotal():
        if (ticket_history_deal := HistoryDealGetTicket(i)) > 0:
            timeeee = HistoryDealGetInteger(ticket_history_deal, DEAL_TIME)
            if timeeee > StringToTime(TimeToString(TimeCurrent(), TIME_DATE)):
                if HistoryDealGetInteger(ticket_history_deal, DEAL_TYPE) == DEAL_TYPE_BUY or HistoryDealGetInteger(ticket_history_deal, DEAL_TYPE) == DEAL_TYPE_SELL:
                    historyProfit += HistoryDealGetDouble(ticket_history_deal, DEAL_PROFIT) + HistoryDealGetDouble(ticket_history_deal, DEAL_COMMISSION) + HistoryDealGetDouble(ticket_history_deal, DEAL_SWAP)
                else:
                    deposit += HistoryDealGetDouble(ticket_history_deal, DEAL_PROFIT)
        i += 1
    startBalnce = AccountInfoDouble(ACCOUNT_BALANCE) - historyProfit
    text = ''
    dd = _fdiv((historyProfit + AccountInfoDouble(ACCOUNT_PROFIT)) * 100, startBalnce)
    text = DoubleToString(dd, 2) + ' %'
    ObjectSetString(0, 'Daily DD V', OBJPROP_TEXT, text)
    ChartRedraw()
    return rates_total

def CreateEdit(name, x=0, y=0, width=50, height=18, text='Text', clr=clrWhite, back_clr=clrBlack, fontSize=8, align=ALIGN_CENTER, border_clr=clrBlack, back=False):
    chartID = 0
    windowID = 0
    ObjectDelete(chartID, name)
    ResetLastError()
    if not ObjectCreate(chartID, name, OBJ_EDIT, windowID, 0, 0):
        Print('CreateEdit', ': failed to create "Edit" object! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chartID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chartID, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(chartID, name, OBJPROP_XSIZE, width)
    ObjectSetInteger(chartID, name, OBJPROP_YSIZE, height)
    ObjectSetString(chartID, name, OBJPROP_TEXT, text)
    ObjectSetString(chartID, name, OBJPROP_FONT, 'Arial')
    ObjectSetInteger(chartID, name, OBJPROP_FONTSIZE, fontSize)
    ObjectSetInteger(chartID, name, OBJPROP_ALIGN, align)
    ObjectSetInteger(chartID, name, OBJPROP_READONLY, True)
    ObjectSetInteger(chartID, name, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(chartID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartID, name, OBJPROP_BGCOLOR, back_clr)
    ObjectSetInteger(chartID, name, OBJPROP_BORDER_COLOR, border_clr)
    ObjectSetInteger(chartID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chartID, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(chartID, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chartID, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(chartID, name, OBJPROP_ZORDER, 0)
    return True

def CreateRectLabel(name, x=0, y=0, width=50, height=18, back_clr=clrBlack, border=BORDER_SUNKEN, clr=clrWhite, style=STYLE_SOLID, line_width=0, back=False):
    chartID = 0
    windowID = 0
    ObjectDelete(chartID, name)
    ResetLastError()
    if not ObjectCreate(chartID, name, OBJ_RECTANGLE_LABEL, windowID, 0, 0):
        Print('CreateRectLabel', ': failed to create a rectangle label! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chartID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chartID, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(chartID, name, OBJPROP_XSIZE, width)
    ObjectSetInteger(chartID, name, OBJPROP_YSIZE, height)
    ObjectSetInteger(chartID, name, OBJPROP_BGCOLOR, back_clr)
    ObjectSetInteger(chartID, name, OBJPROP_BORDER_TYPE, border)
    ObjectSetInteger(chartID, name, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(chartID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chartID, name, OBJPROP_WIDTH, line_width)
    ObjectSetInteger(chartID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chartID, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(chartID, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chartID, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(chartID, name, OBJPROP_ZORDER, 0)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyDrawdown(_MQL5Indicator):
    name = 'Daily Drawdown'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDDD': True,  # Daily drowdown active:
    }

