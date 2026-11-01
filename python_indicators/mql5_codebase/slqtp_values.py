"""slqtp_values — converted from MQL5: MQL5 Indicators/SL-TP Values/slqtp_values.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'slqtp_values', 'source': 'MQL5 Indicators/SL-TP Values/slqtp_values.mq5', 'folder': 'SL-TP Values', 'inputs': [{'mql': 'Colors', 'py': 'Colors', 'param': 'Colors', 'type': 'int', 'default': 0, 'label': 'Colors', 'sinput': False}, {'mql': 'Offset', 'py': 'Offset', 'param': 'Offset', 'type': 'int', 'default': 25, 'label': 'Offset', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

POSITION_TIME_UPDATE_MSC = 0  # MQL5 constant unknown to the converter

# enum ColorSelect
COLOR_RED_GREEN = 0
COLOR_FOREGROUND = 1
_enum('ColorSelect', {0: 'COLOR_RED_GREEN', 1: 'COLOR_FOREGROUND'})

# ---- inputs and global variables
Colors = _input('Colors', COLOR_RED_GREEN)  # Colors
Offset = _input('Offset', 25)  # Offset
COLOR_SL = clrNONE
COLOR_TP = clrNONE

class CPositionInfo(CObject):
    _q_fields = ('m_type', 'm_volume', 'm_price', 'm_stop_loss', 'm_take_profit')
    def __init__(self):
        CObject.__init__(self)
        self.m_type = 0
        self.m_volume = 0.0
        self.m_price = 0.0
        self.m_stop_loss = 0.0
        self.m_take_profit = 0.0
        self.m_type = WRONG_VALUE
        self.m_volume = 0.0
        self.m_price = 0.0
        self.m_stop_loss = 0.0
        self.m_take_profit = 0.0
    def _q_dtor(self):
        pass
    def Ticket(self):
        return _ulong(PositionGetInteger(POSITION_TICKET))
    def Time(self):
        return PositionGetInteger(POSITION_TIME)
    def TimeMsc(self):
        return _ulong(PositionGetInteger(POSITION_TIME_MSC))
    def TimeUpdate(self):
        return PositionGetInteger(POSITION_TIME_UPDATE)
    def TimeUpdateMsc(self):
        return _ulong(PositionGetInteger(POSITION_TIME_UPDATE_MSC))
    def PositionType(self):
        return PositionGetInteger(POSITION_TYPE)
    def TypeDescription(self):
        str_ = Box("")
        return self.FormatType(str_, self.PositionType())
    def Magic(self):
        return PositionGetInteger(POSITION_MAGIC)
    def Identifier(self):
        return PositionGetInteger(POSITION_IDENTIFIER)
    def Volume(self):
        return PositionGetDouble(POSITION_VOLUME)
    def PriceOpen(self):
        return PositionGetDouble(POSITION_PRICE_OPEN)
    def StopLoss(self):
        return PositionGetDouble(POSITION_SL)
    def TakeProfit(self):
        return PositionGetDouble(POSITION_TP)
    def PriceCurrent(self):
        return PositionGetDouble(POSITION_PRICE_CURRENT)
    def Commission(self):
        SetUserError(ERR_FUNCTION_NOT_ALLOWED)
        return 0.0
    def Swap(self):
        return PositionGetDouble(POSITION_SWAP)
    def Profit(self):
        return PositionGetDouble(POSITION_PROFIT)
    def Symbol(self):
        return PositionGetString(POSITION_SYMBOL)
    def Comment(self):
        return PositionGetString(POSITION_COMMENT)
    def InfoInteger(self, prop_id, var):
        return (PositionGetInteger(prop_id, var) != 0)
    def InfoDouble(self, prop_id, var):
        return (PositionGetDouble(prop_id, var) != 0)
    def InfoString(self, prop_id, var):
        return _bool(PositionGetString(prop_id, var))
    def FormatType(self, str_, type_):
        _sw1 = type_
        if _sw1 == POSITION_TYPE_BUY:
            str_.v = 'buy'
        elif _sw1 == POSITION_TYPE_SELL:
            str_.v = 'sell'
        else:
            str_.v = 'unknown position type ' + _str(type_)
        return str_.v
    def FormatPosition(self, str_):
        tmp = ""
        type_ = Box("")
        tmp_long = Box(0)
        margin_mode = AccountInfoInteger(ACCOUNT_MARGIN_MODE)
        symbol_name = self.Symbol()
        digits = Digits()
        if SymbolInfoInteger(symbol_name, SYMBOL_DIGITS, tmp_long):
            digits = _int(tmp_long.v)
        if margin_mode == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING:
            str_.v = StringFormat('#%I64u %s %s %s %s', self.Ticket(), self.FormatType(type_, self.PositionType()), DoubleToString(self.Volume(), 2), symbol_name, DoubleToString(self.PriceOpen(), digits + 3))
        else:
            str_.v = StringFormat('%s %s %s %s', self.FormatType(type_, self.PositionType()), DoubleToString(self.Volume(), 2), symbol_name, DoubleToString(self.PriceOpen(), digits + 3))
        sl = self.StopLoss()
        tp = self.TakeProfit()
        if sl != 0.0:
            tmp = StringFormat(' sl: %s', DoubleToString(sl, digits))
            str_.v += tmp
        if tp != 0.0:
            tmp = StringFormat(' tp: %s', DoubleToString(tp, digits))
            str_.v += tmp
        return str_.v
    def Select(self, symbol):
        return PositionSelect(symbol)
    def SelectByMagic(self, symbol, magic):
        res = False
        total = PositionsTotal()
        for i in range(0, total):
            position_symbol = _str(PositionGetSymbol(i))
            if position_symbol == symbol and magic == PositionGetInteger(POSITION_MAGIC):
                res = True
                break
        return res
    def SelectByTicket(self, ticket):
        return PositionSelectByTicket(ticket)
    def SelectByIndex(self, index):
        ticket = PositionGetTicket(index)
        return ticket > 0
    def StoreState(self):
        self.m_type = self.PositionType()
        self.m_volume = self.Volume()
        self.m_price = self.PriceOpen()
        self.m_stop_loss = self.StopLoss()
        self.m_take_profit = self.TakeProfit()
    def CheckState(self):
        if (((self.m_type == self.PositionType() and self.m_volume == self.Volume()) and self.m_price == self.PriceOpen()) and self.m_stop_loss == self.StopLoss()) and self.m_take_profit == self.TakeProfit():
            return False
        return True

def OnInit():
    global COLOR_SL, COLOR_TP
    EventSetMillisecondTimer(250)
    if Colors != COLOR_RED_GREEN:
        COLOR_SL = ChartForeColor()
        COLOR_TP = ChartForeColor()
    else:
        COLOR_SL = clrRed
        COLOR_TP = clrLimeGreen
    return INIT_SUCCEEDED

def OnDeinit(reason):
    EventKillTimer()
    i = 0
    while i < PositionsTotal():
        ticket = PositionGetTicket(i)
        if m_position.SelectByIndex(i):
            if m_position.Symbol() == Symbol():
                if ObjectFind(0, '#' + IntegerToString(ticket, 0, 0) + ' sl') == 0:
                    ObjectDelete(0, '#' + IntegerToString(ticket, 0, 0) + ' sl')
                if ObjectFind(0, '#' + IntegerToString(ticket, 0, 0) + ' tp') == 0:
                    ObjectDelete(0, '#' + IntegerToString(ticket, 0, 0) + ' tp')
        i += 1

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def ChartForeColor():
    result = Box(clrNONE)
    ChartGetInteger(0, CHART_COLOR_FOREGROUND, 0, result)
    return _uint(result.v)

def _AccountCurrency():
    txt = ''
    if AccountInfoString(ACCOUNT_CURRENCY) == 'EUR':
        txt = '€'
    if AccountInfoString(ACCOUNT_CURRENCY) == 'USD':
        txt = '$'
    if AccountInfoString(ACCOUNT_CURRENCY) == 'GBP':
        txt = '£'
    if AccountInfoString(ACCOUNT_CURRENCY) == 'CHF':
        txt = 'Fr.'
    return txt

def TextCreate(chart_ID=0, name='Text', sub_window=0, time=0, price=0.0, text='Text', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    if ObjectFind(chart_ID, name) != 0:
        ResetLastError()
        if not ObjectCreate(chart_ID, name, OBJ_TEXT, sub_window, time, price):
            Print('TextCreate', ': failed to create "Text" object! Error code = ', GetLastError())
            return False
        ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
        ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
        ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
        ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
        ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def OnTimer():
    sl_dist = 0.0
    sl_val = 0.0
    tp_dist = 0.0
    tp_val = 0.0
    tick_val = 0.0
    sl_name = ''
    tp_name = ''
    sl_pn = ''
    anchor = 0
    i = 0
    while i < PositionsTotal():
        ticket = PositionGetTicket(i)
        if m_position.SelectByIndex(i):
            if PositionGetString(POSITION_SYMBOL) == Symbol():
                tick_val = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_VALUE)
                if ChartGetInteger(0, CHART_SHIFT, 0):
                    anchor = ANCHOR_LEFT
                else:
                    anchor = ANCHOR_RIGHT
                Time = Arr(0, 0)
                CopyTime(Symbol(), PERIOD_CURRENT, 0, 1, Time)
                if PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL:
                    sl_name = '#' + IntegerToString(ticket, 0, 0) + ' sl'
                    if m_position.StopLoss() > 0:
                        if m_position.StopLoss() < m_position.PriceOpen():
                            sl_pn = '   +'
                        else:
                            sl_pn = '   -'
                        sl_dist = _fdiv(m_position.StopLoss() - m_position.PriceOpen(), Point())
                        sl_val = sl_dist * tick_val * m_position.Volume()
                        TextCreate(0, sl_name, 0, Time[0], m_position.StopLoss() + (Offset * Point()), sl_pn + DoubleToString(MathAbs(sl_val), 2) + _AccountCurrency() + ' / ' + DoubleToString(MathAbs(sl_dist), 0) + 'p', 'Tahoma', 8, COLOR_SL, 0.0, anchor, False, False, True, 0)
                        if ObjectFind(0, sl_name) == 0:
                            if (ObjectGetDouble(0, sl_name, OBJPROP_PRICE, 0) - (m_position.StopLoss() + (Offset * Point()))) != 0 or ObjectGetInteger(0, sl_name, OBJPROP_TIME, 0) != Time[0]:
                                ObjectSetDouble(0, sl_name, OBJPROP_PRICE, m_position.StopLoss() + (Offset * Point()))
                                ObjectSetString(0, sl_name, OBJPROP_TEXT, 0, sl_pn + DoubleToString(MathAbs(sl_val), 2) + _AccountCurrency() + ' / ' + DoubleToString(MathAbs(sl_dist), 0) + 'p')
                                ObjectSetInteger(0, sl_name, OBJPROP_TIME, Time[0])
                    elif ObjectFind(0, sl_name) == 0:
                        ObjectDelete(0, sl_name)
                    tp_name = '#' + IntegerToString(ticket, 0, 0) + ' tp'
                    if m_position.TakeProfit() > 0:
                        tp_dist = _fdiv(m_position.PriceOpen() - m_position.TakeProfit(), Point())
                        tp_val = tp_dist * tick_val * m_position.Volume()
                        TextCreate(0, tp_name, 0, Time[0], m_position.TakeProfit() - (Offset * Point()), '   +' + DoubleToString(tp_val, 2) + _AccountCurrency() + ' / ' + DoubleToString(tp_dist, 0) + 'p', 'Tahoma', 8, COLOR_TP, 0.0, anchor, False, False, True, 0)
                        if ObjectFind(0, tp_name) == 0:
                            if (ObjectGetDouble(0, tp_name, OBJPROP_PRICE, 0) - (m_position.TakeProfit() - (Offset * Point()))) != 0 or ObjectGetInteger(0, tp_name, OBJPROP_TIME, 0) != Time[0]:
                                ObjectSetDouble(0, tp_name, OBJPROP_PRICE, m_position.TakeProfit() - (Offset * Point()))
                                ObjectSetString(0, tp_name, OBJPROP_TEXT, 0, '   +' + DoubleToString(tp_val, 2) + _AccountCurrency() + ' / ' + DoubleToString(tp_dist, 0) + 'p')
                                ObjectSetInteger(0, tp_name, OBJPROP_TIME, Time[0])
                    elif ObjectFind(0, tp_name) == 0:
                        ObjectDelete(0, tp_name)
                if PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY:
                    sl_name = '#' + IntegerToString(ticket, 0, 0) + ' sl'
                    if m_position.StopLoss() > 0:
                        if m_position.StopLoss() >= m_position.PriceOpen():
                            sl_pn = '   +'
                        else:
                            sl_pn = '   -'
                        sl_dist = _fdiv(m_position.PriceOpen() - m_position.StopLoss(), Point())
                        sl_val = sl_dist * tick_val * m_position.Volume()
                        TextCreate(0, sl_name, 0, Time[0], m_position.StopLoss() - (Offset * Point()), sl_pn + DoubleToString(MathAbs(sl_val), 2) + _AccountCurrency() + ' / ' + DoubleToString(MathAbs(sl_dist), 0) + 'p', 'Tahoma', 8, COLOR_SL, 0.0, anchor, False, False, True, 0)
                        if ObjectFind(0, sl_name) == 0:
                            if (ObjectGetDouble(0, sl_name, OBJPROP_PRICE, 0) - (m_position.StopLoss() - (Offset * Point()))) != 0 or ObjectGetInteger(0, sl_name, OBJPROP_TIME, 0) != Time[0]:
                                ObjectSetDouble(0, sl_name, OBJPROP_PRICE, m_position.StopLoss() - (Offset * Point()))
                                ObjectSetString(0, sl_name, OBJPROP_TEXT, 0, sl_pn + DoubleToString(MathAbs(sl_val), 2) + _AccountCurrency() + ' / ' + DoubleToString(MathAbs(sl_dist), 0) + 'p')
                                ObjectSetInteger(0, sl_name, OBJPROP_TIME, Time[0])
                    elif ObjectFind(0, sl_name) == 0:
                        ObjectDelete(0, sl_name)
                    tp_name = '#' + IntegerToString(ticket, 0, 0) + ' tp'
                    if m_position.TakeProfit() > 0:
                        tp_dist = _fdiv(m_position.TakeProfit() - m_position.PriceOpen(), Point())
                        tp_val = tp_dist * tick_val * m_position.Volume()
                        TextCreate(0, tp_name, 0, Time[0], m_position.TakeProfit() + (Offset * Point()), '   +' + DoubleToString(tp_val, 2) + _AccountCurrency() + ' / ' + DoubleToString(tp_dist, 0) + 'p', 'Tahoma', 8, COLOR_TP, 0.0, anchor, False, False, True, 0)
                        if ObjectFind(0, tp_name) == 0:
                            if (ObjectGetDouble(0, tp_name, OBJPROP_PRICE, 0) - (m_position.TakeProfit() + (Offset * Point()))) != 0 or ObjectGetInteger(0, tp_name, OBJPROP_TIME, 0) != Time[0]:
                                ObjectSetDouble(0, tp_name, OBJPROP_PRICE, m_position.TakeProfit() + (Offset * Point()))
                                ObjectSetString(0, tp_name, OBJPROP_TEXT, 0, '   +' + DoubleToString(tp_val, 2) + _AccountCurrency() + ' / ' + DoubleToString(tp_dist, 0) + 'p')
                                ObjectSetInteger(0, tp_name, OBJPROP_TIME, Time[0])
                    elif ObjectFind(0, tp_name) == 0:
                        ObjectDelete(0, tp_name)
        i += 1
    ticket = 0
    x = 0
    while x < ObjectsTotal(0):
        obj_name = ObjectName(0, x)
        if StringSubstr(obj_name, StringLen(obj_name) - 2, 2) == 'sl' or StringSubstr(obj_name, StringLen(obj_name) - 2, 2) == 'tp':
            i = 0
            while i < HistoryOrdersTotal():
                if (ticket := HistoryDealGetTicket(i)) > 0:
                    if HistoryDealGetString(ticket, DEAL_SYMBOL) == Symbol():
                        if ObjectFind(0, '#' + IntegerToString(ticket, 0, 0) + ' sl') == 0:
                            ObjectDelete(0, '#' + IntegerToString(ticket, 0, 0) + ' sl')
                        if ObjectFind(0, '#' + IntegerToString(ticket, 0, 0) + ' tp') == 0:
                            ObjectDelete(0, '#' + IntegerToString(ticket, 0, 0) + ' tp')
                i += 1
        x += 1

# ---- global variables initialised from expressions
m_position = _alloc(CPositionInfo)
m_position.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SlqtpValues(_MQL5Indicator):
    name = 'slqtp_values'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Colors': _Choice({0: 'Red/Green', 1: 'Foreground'}, default=0),  # Colors
        'Offset': 25,  # Offset
    }

