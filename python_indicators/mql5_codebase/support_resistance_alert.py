"""Support_Resistance_Alert — converted from MQL5: MQL5 Indicators/Support Resistance Line Alert/Support_Resistance_Alert.mq5

Copyright: Copyright 2022, D4rk Ryd3r; Link: https://twitter.com/DarkRyd3r; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, D4rk Ryd3r', 'link': 'https://twitter.com/DarkRyd3r', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Support_Resistance_Alert', 'source': 'MQL5 Indicators/Support Resistance Line Alert/Support_Resistance_Alert.mq5', 'folder': 'Support Resistance Line Alert', 'inputs': [{'mql': 'popup_alerts', 'py': 'popup_alerts', 'param': 'popup_alerts', 'type': 'bool', 'default': True, 'label': 'Enable PopUp Alerts', 'sinput': False}, {'mql': 'send_push', 'py': 'send_push', 'param': 'send_push', 'type': 'bool', 'default': False, 'label': 'Enable Push Notification', 'sinput': False}, {'mql': 'InpColorSupport', 'py': 'InpColorSupport', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Support Color', 'sinput': False}, {'mql': 'InpColorResistance', 'py': 'InpColorResistance', 'param': None, 'type': 'color', 'default': 3937500, 'label': 'Resistance Color', 'sinput': False}, {'mql': 'InpSupportStyle', 'py': 'InpSupportStyle', 'param': 'InpSupportStyle', 'type': 'int', 'default': 0, 'label': 'Support Line Style', 'sinput': False}, {'mql': 'InpResistanceStyle', 'py': 'InpResistanceStyle', 'param': 'InpResistanceStyle', 'type': 'int', 'default': 0, 'label': 'Resistance Line Style', 'sinput': False}, {'mql': 'SupportWidth', 'py': 'SupportWidth', 'param': 'SupportWidth', 'type': 'int', 'default': 3, 'label': 'Support Width', 'sinput': False}, {'mql': 'ResistanceWidth', 'py': 'ResistanceWidth', 'param': 'ResistanceWidth', 'type': 'int', 'default': 3, 'label': 'Resistance Width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
popup_alerts = _input('popup_alerts', True)  # Enable PopUp Alerts
send_push = _input('send_push', False)  # Enable Push Notification
InpColorSupport = _input('InpColorSupport', clrLimeGreen)  # Support Color
InpColorResistance = _input('InpColorResistance', clrCrimson)  # Resistance Color
InpSupportStyle = _input('InpSupportStyle', STYLE_SOLID)  # Support Line Style
InpResistanceStyle = _input('InpResistanceStyle', STYLE_SOLID)  # Resistance Line Style
SupportWidth = _input('SupportWidth', 3)  # Support Width
ResistanceWidth = _input('ResistanceWidth', 3)  # Resistance Width
now = ""

def OnInit():
    EventSetTimer(1)
    if not SymbolInfoTick(Symbol(), m_tick):
        return INIT_SUCCEEDED
    if m_tick.bid == 0.0:
        return INIT_SUCCEEDED
    HLineCreate(0, 'Resistance', 0, m_tick.bid + (50 * Point()), InpColorResistance, InpResistanceStyle, ResistanceWidth)
    HLineCreate(0, 'Support', 0, m_tick.bid - (50 * Point()), InpColorSupport, InpSupportStyle, SupportWidth)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    EventKillTimer()
    HLineDelete(0, 'Resistance')
    HLineDelete(0, 'Support')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnTimer():
    global now
    now = TimeToString(TimeLocal(), TIME_SECONDS)
    High = iHigh(Symbol(), PERIOD_M1, 0)
    Low = iLow(Symbol(), PERIOD_M1, 0)
    if ObjectFind(0, 'Resistance') < 0:
        HLineCreate(0, 'Resistance', 0, m_tick.bid + (50 * Point()), InpColorResistance, InpResistanceStyle, ResistanceWidth)
    if ObjectFind(0, 'Support') < 0:
        HLineCreate(0, 'Support', 0, m_tick.bid - (50 * Point()), InpColorSupport, InpSupportStyle, SupportWidth)
    if High >= ObjectGetDouble(0, 'Resistance', OBJPROP_PRICE, 0) and Low <= ObjectGetDouble(0, 'Resistance', OBJPROP_PRICE, 0):
        DoAlert(Symbol() + ' Resistance touched at ' + DoubleToString(m_tick.bid, _int(SymbolInfoInteger(Symbol(), SYMBOL_DIGITS))) + ' ' + now)
        HLineDelete(0, 'Resistance')
    if High >= ObjectGetDouble(0, 'Support', OBJPROP_PRICE, 0) and Low <= ObjectGetDouble(0, 'Support', OBJPROP_PRICE, 0):
        DoAlert(Symbol() + ' Support touched at ' + DoubleToString(m_tick.bid, _int(SymbolInfoInteger(Symbol(), SYMBOL_DIGITS))) + ' ' + now)
        HLineDelete(0, 'Support')

def HLineCreate(chart_ID=0, name='HLine', sub_window=0, price=0.0, clr=clrRed, style=STYLE_DASHDOTDOT, width=1, back=False, selection=True, hidden=True, z_order=0):
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_HLINE, sub_window, 0, price):
        Print('HLineCreate', ': failed to create a horizontal line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def HLineDelete(chart_ID=0, name='HLine'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('HLineDelete', ': failed to delete a horizontal line! Error code = ', GetLastError())
        return False
    return True

def DoAlert(text):
    if popup_alerts == True:
        Alert(text)
    if send_push == True:
        SendNotification(text)

# ---- global variables initialised from expressions
m_tick = MqlTick()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SupportResistanceAlert(_MQL5Indicator):
    name = 'Support_Resistance_Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'popup_alerts': True,  # Enable PopUp Alerts
        'send_push': False,  # Enable Push Notification
        'InpSupportStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Support Line Style
        'InpResistanceStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Resistance Line Style
        'SupportWidth': 3,  # Support Width
        'ResistanceWidth': 3,  # Resistance Width
    }

