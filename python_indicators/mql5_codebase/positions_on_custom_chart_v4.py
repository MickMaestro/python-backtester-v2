"""Positions_on_Custom_Chart_v4 — converted from MQL5: MQL5 Indicators/Show Positions on Custom Chart (or standard chart) for MT5/Positions_on_Custom_Chart_v4.mq5

Copyright: © 2023, Ryan Lawrence Johnson.; Link: https://www.mql5.com/en/users/rjo/seller; Version: 4.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': '© 2023, Ryan Lawrence Johnson.', 'link': 'https://www.mql5.com/en/users/rjo/seller', 'version': '4.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Positions_on_Custom_Chart_v4', 'source': 'MQL5 Indicators/Show Positions on Custom Chart (or standard chart) for MT5/Positions_on_Custom_Chart_v4.mq5', 'folder': 'Show Positions on Custom Chart (or standard chart) for MT5', 'inputs': [{'mql': 'BaseSymbol', 'py': 'BaseSymbol', 'param': None, 'type': 'string', 'default': 'GBPJPY', 'label': '', 'sinput': False}, {'mql': 'TextBarsBack', 'py': 'TextBarsBack', 'param': 'TextBarsBack', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

DEAL_ENTRY_STATE = 0  # MQL5 constant unknown to the converter
DEAL_EXTERNAL_ID = 0  # MQL5 constant unknown to the converter
DEAL_TYPE_BUY_CANCELED = 0  # MQL5 constant unknown to the converter
DEAL_TYPE_COMMISSION_AGENT_DAILY = 0  # MQL5 constant unknown to the converter
DEAL_TYPE_COMMISSION_AGENT_MONTHLY = 0  # MQL5 constant unknown to the converter
DEAL_TYPE_INTEREST = 0  # MQL5 constant unknown to the converter
DEAL_TYPE_SELL_CANCELED = 0  # MQL5 constant unknown to the converter
ORDER_EXTERNAL_ID = 0  # MQL5 constant unknown to the converter
ORDER_POSITION_BY_ID = 0  # MQL5 constant unknown to the converter
ORDER_STATE_REQUEST_ADD = 0  # MQL5 constant unknown to the converter
ORDER_STATE_REQUEST_CANCEL = 0  # MQL5 constant unknown to the converter
ORDER_STATE_REQUEST_MODIFY = 0  # MQL5 constant unknown to the converter
ORDER_TIME_DONE_MSC = 0  # MQL5 constant unknown to the converter
ORDER_TIME_SETUP_MSC = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
BaseSymbol = _input('BaseSymbol', 'GBPJPY')
TextBarsBack = _input('TextBarsBack', 100)
pos_id = 0
pos_id_str = ""
direction = ""
text = ""
ord_id = 0
ord_id_str = ""
pending = ""

class COrderInfo(CObject):
    _q_fields = ('m_ticket', 'm_type', 'm_state', 'm_expiration', 'm_volume_curr', 'm_price_open', 'm_stop_loss', 'm_take_profit')
    def __init__(self):
        CObject.__init__(self)
        self.m_ticket = 0
        self.m_type = 0
        self.m_state = 0
        self.m_expiration = 0
        self.m_volume_curr = 0.0
        self.m_price_open = 0.0
        self.m_stop_loss = 0.0
        self.m_take_profit = 0.0
        self.m_ticket = ULONG_MAX
        self.m_type = WRONG_VALUE
        self.m_state = WRONG_VALUE
        self.m_expiration = 0
        self.m_volume_curr = 0.0
        self.m_price_open = 0.0
        self.m_stop_loss = 0.0
        self.m_take_profit = 0.0
    def _q_dtor(self):
        pass
    def Ticket(self):
        return self.m_ticket
    def TimeSetup(self):
        return OrderGetInteger(ORDER_TIME_SETUP)
    def TimeSetupMsc(self):
        return OrderGetInteger(ORDER_TIME_SETUP_MSC)
    def TimeDone(self):
        return OrderGetInteger(ORDER_TIME_DONE)
    def TimeDoneMsc(self):
        return OrderGetInteger(ORDER_TIME_DONE_MSC)
    def OrderType(self):
        return OrderGetInteger(ORDER_TYPE)
    def TypeDescription(self):
        str_ = Box("")
        return self.FormatType(str_, self.OrderType())
    def State(self):
        return OrderGetInteger(ORDER_STATE)
    def StateDescription(self):
        str_ = Box("")
        return self.FormatStatus(str_, self.State())
    def TimeExpiration(self):
        return OrderGetInteger(ORDER_TIME_EXPIRATION)
    def TypeFilling(self):
        return OrderGetInteger(ORDER_TYPE_FILLING)
    def TypeFillingDescription(self):
        str_ = Box("")
        return self.FormatTypeFilling(str_, self.TypeFilling())
    def TypeTime(self):
        return OrderGetInteger(ORDER_TYPE_TIME)
    def TypeTimeDescription(self):
        str_ = Box("")
        return self.FormatTypeTime(str_, self.TypeFilling())
    def Magic(self):
        return OrderGetInteger(ORDER_MAGIC)
    def PositionId(self):
        return OrderGetInteger(ORDER_POSITION_ID)
    def PositionById(self):
        return OrderGetInteger(ORDER_POSITION_BY_ID)
    def VolumeInitial(self):
        return OrderGetDouble(ORDER_VOLUME_INITIAL)
    def VolumeCurrent(self):
        return OrderGetDouble(ORDER_VOLUME_CURRENT)
    def PriceOpen(self):
        return OrderGetDouble(ORDER_PRICE_OPEN)
    def StopLoss(self):
        return OrderGetDouble(ORDER_SL)
    def TakeProfit(self):
        return OrderGetDouble(ORDER_TP)
    def PriceCurrent(self):
        return OrderGetDouble(ORDER_PRICE_CURRENT)
    def PriceStopLimit(self):
        return OrderGetDouble(ORDER_PRICE_STOPLIMIT)
    def Symbol(self):
        return OrderGetString(ORDER_SYMBOL)
    def Comment(self):
        return OrderGetString(ORDER_COMMENT)
    def ExternalId(self):
        return OrderGetString(ORDER_EXTERNAL_ID)
    def InfoInteger(self, prop_id, var):
        return (OrderGetInteger(prop_id, var) != 0)
    def InfoDouble(self, prop_id, var):
        return (OrderGetDouble(prop_id, var) != 0)
    def InfoString(self, prop_id, var):
        return _bool(OrderGetString(prop_id, var))
    def FormatType(self, str_, type_):
        _sw1 = type_
        if _sw1 == ORDER_TYPE_BUY:
            str_.v = 'buy'
        elif _sw1 == ORDER_TYPE_SELL:
            str_.v = 'sell'
        elif _sw1 == ORDER_TYPE_BUY_LIMIT:
            str_.v = 'buy limit'
        elif _sw1 == ORDER_TYPE_SELL_LIMIT:
            str_.v = 'sell limit'
        elif _sw1 == ORDER_TYPE_BUY_STOP:
            str_.v = 'buy stop'
        elif _sw1 == ORDER_TYPE_SELL_STOP:
            str_.v = 'sell stop'
        elif _sw1 == ORDER_TYPE_BUY_STOP_LIMIT:
            str_.v = 'buy stop limit'
        elif _sw1 == ORDER_TYPE_SELL_STOP_LIMIT:
            str_.v = 'sell stop limit'
        elif _sw1 == ORDER_TYPE_CLOSE_BY:
            str_.v = 'close by'
        else:
            str_.v = 'unknown order type ' + _str(type_)
        return str_.v
    def FormatStatus(self, str_, status):
        _sw2 = status
        if _sw2 == ORDER_STATE_STARTED:
            str_.v = 'started'
        elif _sw2 == ORDER_STATE_PLACED:
            str_.v = 'placed'
        elif _sw2 == ORDER_STATE_CANCELED:
            str_.v = 'canceled'
        elif _sw2 == ORDER_STATE_PARTIAL:
            str_.v = 'partial'
        elif _sw2 == ORDER_STATE_FILLED:
            str_.v = 'filled'
        elif _sw2 == ORDER_STATE_REJECTED:
            str_.v = 'rejected'
        elif _sw2 == ORDER_STATE_EXPIRED:
            str_.v = 'expired'
        elif _sw2 == ORDER_STATE_REQUEST_ADD:
            str_.v = 'request adding'
        elif _sw2 == ORDER_STATE_REQUEST_MODIFY:
            str_.v = 'request modifying'
        elif _sw2 == ORDER_STATE_REQUEST_CANCEL:
            str_.v = 'request cancelling'
        else:
            str_.v = 'unknown order status ' + _str(status)
        return str_.v
    def FormatTypeFilling(self, str_, type_):
        _sw3 = type_
        if _sw3 == ORDER_FILLING_RETURN:
            str_.v = 'return remainder'
        elif _sw3 == ORDER_FILLING_IOC:
            str_.v = 'cancel remainder'
        elif _sw3 == ORDER_FILLING_FOK:
            str_.v = 'fill or kill'
        else:
            str_.v = 'unknown type filling ' + _str(type_)
        return str_.v
    def FormatTypeTime(self, str_, type_):
        _sw4 = type_
        if _sw4 == ORDER_TIME_GTC:
            str_.v = 'gtc'
        elif _sw4 == ORDER_TIME_DAY:
            str_.v = 'day'
        elif _sw4 == ORDER_TIME_SPECIFIED:
            str_.v = 'specified'
        elif _sw4 == ORDER_TIME_SPECIFIED_DAY:
            str_.v = 'specified day'
        else:
            str_.v = 'unknown type time ' + _str(type_)
        return str_.v
    def FormatOrder(self, str_):
        type_ = Box("")
        price = Box("")
        tmp_long = Box(0)
        symbol_name = self.Symbol()
        digits = Digits()
        if SymbolInfoInteger(symbol_name, SYMBOL_DIGITS, tmp_long):
            digits = _int(tmp_long.v)
        str_.v = StringFormat('#%I64u %s %s %s', self.Ticket(), self.FormatType(type_, self.OrderType()), DoubleToString(self.VolumeInitial(), 2), symbol_name)
        self.FormatPrice(price, self.PriceOpen(), self.PriceStopLimit(), digits)
        if price.v != '':
            str_.v += ' at '
            str_.v += price.v
        return str_.v
    def FormatPrice(self, str_, price_order, price_trigger, digits):
        price = ""
        trigger = ""
        if price_trigger:
            price = DoubleToString(price_order, digits)
            trigger = DoubleToString(price_trigger, digits)
            str_.v = StringFormat('%s (%s)', price, trigger)
        else:
            str_.v = DoubleToString(price_order, digits)
        return str_.v
    def Select_0(self):
        return OrderSelect(self.m_ticket)
    def Select_1(self, ticket):
        if OrderSelect(ticket):
            self.m_ticket = ticket
            return True
        self.m_ticket = ULONG_MAX
        return False
    def SelectByIndex(self, index):
        ticket = OrderGetTicket(index)
        if ticket == 0:
            self.m_ticket = ULONG_MAX
            return False
        self.m_ticket = ticket
        return True
    def StoreState(self):
        self.m_type = self.OrderType()
        self.m_state = self.State()
        self.m_expiration = self.TimeExpiration()
        self.m_volume_curr = self.VolumeCurrent()
        self.m_price_open = self.PriceOpen()
        self.m_stop_loss = self.StopLoss()
        self.m_take_profit = self.TakeProfit()
    def CheckState(self):
        if (((((self.m_type == self.OrderType() and self.m_state == self.State()) and self.m_expiration == self.TimeExpiration()) and self.m_volume_curr == self.VolumeCurrent()) and self.m_price_open == self.PriceOpen()) and self.m_stop_loss == self.StopLoss()) and self.m_take_profit == self.TakeProfit():
            return False
        return True

class CDealInfo(CObject):
    _q_fields = ('m_ticket',)
    def __init__(self):
        CObject.__init__(self)
        self.m_ticket = 0
    def _q_dtor(self):
        pass
    def Ticket_1(self, ticket):
        self.m_ticket = ticket
    def Ticket_0(self):
        return self.m_ticket
    def Order(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_ORDER)
    def Time(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_TIME)
    def TimeMsc(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_TIME_MSC)
    def DealType(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_TYPE)
    def TypeDescription(self):
        str_ = ""
        _sw5 = self.DealType()
        if _sw5 == DEAL_TYPE_BUY:
            str_ = 'Buy type'
        elif _sw5 == DEAL_TYPE_SELL:
            str_ = 'Sell type'
        elif _sw5 == DEAL_TYPE_BALANCE:
            str_ = 'Balance type'
        elif _sw5 == DEAL_TYPE_CREDIT:
            str_ = 'Credit type'
        elif _sw5 == DEAL_TYPE_CHARGE:
            str_ = 'Charge type'
        elif _sw5 == DEAL_TYPE_CORRECTION:
            str_ = 'Correction type'
        elif _sw5 == DEAL_TYPE_BONUS:
            str_ = 'Bonus type'
        elif _sw5 == DEAL_TYPE_COMMISSION:
            str_ = 'Commission type'
        elif _sw5 == DEAL_TYPE_COMMISSION_DAILY:
            str_ = 'Daily Commission type'
        elif _sw5 == DEAL_TYPE_COMMISSION_MONTHLY:
            str_ = 'Monthly Commission type'
        elif _sw5 == DEAL_TYPE_COMMISSION_AGENT_DAILY:
            str_ = 'Daily Agent Commission type'
        elif _sw5 == DEAL_TYPE_COMMISSION_AGENT_MONTHLY:
            str_ = 'Monthly Agent Commission type'
        elif _sw5 == DEAL_TYPE_INTEREST:
            str_ = 'Interest Rate type'
        elif _sw5 == DEAL_TYPE_BUY_CANCELED:
            str_ = 'Canceled Buy type'
        elif _sw5 == DEAL_TYPE_SELL_CANCELED:
            str_ = 'Canceled Sell type'
        else:
            str_ = 'Unknown type'
        return str_
    def Entry(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_ENTRY)
    def EntryDescription(self):
        str_ = ""
        _sw6 = CDealInfo.Entry(self)
        if _sw6 == DEAL_ENTRY_IN:
            str_ = 'In entry'
        elif _sw6 == DEAL_ENTRY_OUT:
            str_ = 'Out entry'
        elif _sw6 == DEAL_ENTRY_INOUT:
            str_ = 'InOut entry'
        elif _sw6 == DEAL_ENTRY_STATE:
            str_ = 'Status record'
        elif _sw6 == DEAL_ENTRY_OUT_BY:
            str_ = 'Out By entry'
        else:
            str_ = 'Unknown entry'
        return str_
    def Magic(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_MAGIC)
    def PositionId(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_POSITION_ID)
    def Volume(self):
        return HistoryDealGetDouble(self.m_ticket, DEAL_VOLUME)
    def Price(self):
        return HistoryDealGetDouble(self.m_ticket, DEAL_PRICE)
    def Commission(self):
        return HistoryDealGetDouble(self.m_ticket, DEAL_COMMISSION)
    def Swap(self):
        return HistoryDealGetDouble(self.m_ticket, DEAL_SWAP)
    def Profit(self):
        return HistoryDealGetDouble(self.m_ticket, DEAL_PROFIT)
    def Symbol(self):
        return HistoryDealGetString(self.m_ticket, DEAL_SYMBOL)
    def Comment(self):
        return HistoryDealGetString(self.m_ticket, DEAL_COMMENT)
    def ExternalId(self):
        return HistoryDealGetString(self.m_ticket, DEAL_EXTERNAL_ID)
    def InfoInteger(self, prop_id, var):
        return (HistoryDealGetInteger(self.m_ticket, prop_id, var) != 0)
    def InfoDouble(self, prop_id, var):
        return (HistoryDealGetDouble(self.m_ticket, prop_id, var) != 0)
    def InfoString(self, prop_id, var):
        return _bool(HistoryDealGetString(self.m_ticket, prop_id, var))
    def FormatAction(self, str_, action):
        _sw7 = action
        if _sw7 == DEAL_TYPE_BUY:
            str_.v = 'buy'
        elif _sw7 == DEAL_TYPE_SELL:
            str_.v = 'sell'
        elif _sw7 == DEAL_TYPE_BALANCE:
            str_.v = 'balance'
        elif _sw7 == DEAL_TYPE_CREDIT:
            str_.v = 'credit'
        elif _sw7 == DEAL_TYPE_CHARGE:
            str_.v = 'charge'
        elif _sw7 == DEAL_TYPE_CORRECTION:
            str_.v = 'correction'
        elif _sw7 == DEAL_TYPE_BONUS:
            str_.v = 'bonus'
        elif _sw7 == DEAL_TYPE_COMMISSION:
            str_.v = 'commission'
        elif _sw7 == DEAL_TYPE_COMMISSION_DAILY:
            str_.v = 'daily commission'
        elif _sw7 == DEAL_TYPE_COMMISSION_MONTHLY:
            str_.v = 'monthly commission'
        elif _sw7 == DEAL_TYPE_COMMISSION_AGENT_DAILY:
            str_.v = 'daily agent commission'
        elif _sw7 == DEAL_TYPE_COMMISSION_AGENT_MONTHLY:
            str_.v = 'monthly agent commission'
        elif _sw7 == DEAL_TYPE_INTEREST:
            str_.v = 'interest rate'
        elif _sw7 == DEAL_TYPE_BUY_CANCELED:
            str_.v = 'canceled buy'
        elif _sw7 == DEAL_TYPE_SELL_CANCELED:
            str_.v = 'canceled sell'
        else:
            str_.v = 'unknown deal type ' + _str(action)
        return str_.v
    def FormatEntry(self, str_, entry):
        _sw8 = entry
        if _sw8 == DEAL_ENTRY_IN:
            str_.v = 'in'
        elif _sw8 == DEAL_ENTRY_OUT:
            str_.v = 'out'
        elif _sw8 == DEAL_ENTRY_INOUT:
            str_.v = 'in/out'
        elif _sw8 == DEAL_ENTRY_OUT_BY:
            str_.v = 'out by'
        else:
            str_.v = 'unknown deal entry ' + _str(entry)
        return str_.v
    def FormatDeal(self, str_):
        type_ = Box("")
        tmp_long = Box(0)
        symbol_name = self.Symbol()
        digits = Digits()
        if SymbolInfoInteger(symbol_name, SYMBOL_DIGITS, tmp_long):
            digits = _int(tmp_long.v)
        _sw9 = self.DealType()
        if _sw9 in (DEAL_TYPE_BUY, DEAL_TYPE_SELL):
            str_.v = StringFormat('#%I64u %s %s %s at %s', self.Ticket_0(), self.FormatAction(type_, self.DealType()), DoubleToString(self.Volume(), 2), symbol_name, DoubleToString(self.Price(), digits))
        elif _sw9 in (DEAL_TYPE_BALANCE, DEAL_TYPE_CREDIT, DEAL_TYPE_CHARGE, DEAL_TYPE_CORRECTION, DEAL_TYPE_BONUS, DEAL_TYPE_COMMISSION, DEAL_TYPE_COMMISSION_DAILY, DEAL_TYPE_COMMISSION_MONTHLY, DEAL_TYPE_COMMISSION_AGENT_DAILY, DEAL_TYPE_COMMISSION_AGENT_MONTHLY, DEAL_TYPE_INTEREST):
            str_.v = StringFormat('#%I64u %s %s [%s]', self.Ticket_0(), self.FormatAction(type_, self.DealType()), DoubleToString(self.Profit(), 2), self.Comment())
        else:
            str_.v = 'unknown deal type ' + _str(self.DealType())
        return str_.v
    def SelectByIndex(self, index):
        ticket = HistoryDealGetTicket(index)
        if ticket == 0:
            return False
        self.Ticket_1(ticket)
        return True

class CHistoryOrderInfo(CObject):
    _q_fields = ('m_ticket',)
    def __init__(self):
        CObject.__init__(self)
        self.m_ticket = 0
        self.m_ticket = 0
    def _q_dtor(self):
        pass
    def Ticket_1(self, ticket):
        self.m_ticket = ticket
    def Ticket_0(self):
        return self.m_ticket
    def TimeSetup(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_TIME_SETUP)
    def TimeSetupMsc(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_TIME_SETUP_MSC)
    def TimeDone(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_TIME_DONE)
    def TimeDoneMsc(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_TIME_DONE_MSC)
    def OrderType(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_TYPE)
    def TypeDescription(self):
        str_ = Box("")
        return self.FormatType(str_, self.OrderType())
    def State(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_STATE)
    def StateDescription(self):
        str_ = Box("")
        return self.FormatStatus(str_, self.State())
    def TimeExpiration(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_TIME_EXPIRATION)
    def TypeFilling(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_TYPE_FILLING)
    def TypeFillingDescription(self):
        str_ = Box("")
        return self.FormatTypeFilling(str_, self.TypeFilling())
    def TypeTime(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_TYPE_TIME)
    def TypeTimeDescription(self):
        str_ = Box("")
        return self.FormatTypeTime(str_, self.TypeTime())
    def Magic(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_MAGIC)
    def PositionId(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_POSITION_ID)
    def PositionById(self):
        return HistoryOrderGetInteger(self.m_ticket, ORDER_POSITION_BY_ID)
    def VolumeInitial(self):
        return HistoryOrderGetDouble(self.m_ticket, ORDER_VOLUME_INITIAL)
    def VolumeCurrent(self):
        return HistoryOrderGetDouble(self.m_ticket, ORDER_VOLUME_CURRENT)
    def PriceOpen(self):
        return HistoryOrderGetDouble(self.m_ticket, ORDER_PRICE_OPEN)
    def StopLoss(self):
        return HistoryOrderGetDouble(self.m_ticket, ORDER_SL)
    def TakeProfit(self):
        return HistoryOrderGetDouble(self.m_ticket, ORDER_TP)
    def PriceCurrent(self):
        return HistoryOrderGetDouble(self.m_ticket, ORDER_PRICE_CURRENT)
    def PriceStopLimit(self):
        return HistoryOrderGetDouble(self.m_ticket, ORDER_PRICE_STOPLIMIT)
    def Symbol(self):
        return HistoryOrderGetString(self.m_ticket, ORDER_SYMBOL)
    def Comment(self):
        return HistoryOrderGetString(self.m_ticket, ORDER_COMMENT)
    def ExternalId(self):
        return HistoryOrderGetString(self.m_ticket, ORDER_EXTERNAL_ID)
    def InfoInteger(self, prop_id, var):
        return (HistoryOrderGetInteger(self.m_ticket, prop_id, var) != 0)
    def InfoDouble(self, prop_id, var):
        return (HistoryOrderGetDouble(self.m_ticket, prop_id, var) != 0)
    def InfoString(self, prop_id, var):
        return _bool(HistoryOrderGetString(self.m_ticket, prop_id, var))
    def FormatType(self, str_, type_):
        _sw10 = type_
        if _sw10 == ORDER_TYPE_BUY:
            str_.v = 'buy'
        elif _sw10 == ORDER_TYPE_SELL:
            str_.v = 'sell'
        elif _sw10 == ORDER_TYPE_BUY_LIMIT:
            str_.v = 'buy limit'
        elif _sw10 == ORDER_TYPE_SELL_LIMIT:
            str_.v = 'sell limit'
        elif _sw10 == ORDER_TYPE_BUY_STOP:
            str_.v = 'buy stop'
        elif _sw10 == ORDER_TYPE_SELL_STOP:
            str_.v = 'sell stop'
        elif _sw10 == ORDER_TYPE_BUY_STOP_LIMIT:
            str_.v = 'buy stop limit'
        elif _sw10 == ORDER_TYPE_SELL_STOP_LIMIT:
            str_.v = 'sell stop limit'
        elif _sw10 == ORDER_TYPE_CLOSE_BY:
            str_.v = 'close by'
        else:
            str_.v = 'unknown order type ' + _str(type_)
        return str_.v
    def FormatStatus(self, str_, status):
        _sw11 = status
        if _sw11 == ORDER_STATE_STARTED:
            str_.v = 'started'
        elif _sw11 == ORDER_STATE_PLACED:
            str_.v = 'placed'
        elif _sw11 == ORDER_STATE_CANCELED:
            str_.v = 'canceled'
        elif _sw11 == ORDER_STATE_PARTIAL:
            str_.v = 'partial'
        elif _sw11 == ORDER_STATE_FILLED:
            str_.v = 'filled'
        elif _sw11 == ORDER_STATE_REJECTED:
            str_.v = 'rejected'
        elif _sw11 == ORDER_STATE_EXPIRED:
            str_.v = 'expired'
        else:
            str_.v = 'unknown order status ' + _str(status)
        return str_.v
    def FormatTypeFilling(self, str_, type_):
        _sw12 = type_
        if _sw12 == ORDER_FILLING_RETURN:
            str_.v = 'return remainder'
        elif _sw12 == ORDER_FILLING_IOC:
            str_.v = 'cancel remainder'
        elif _sw12 == ORDER_FILLING_FOK:
            str_.v = 'fill or kill'
        else:
            str_.v = 'unknown type filling ' + _str(type_)
        return str_.v
    def FormatTypeTime(self, str_, type_):
        _sw13 = type_
        if _sw13 == ORDER_TIME_GTC:
            str_.v = 'gtc'
        elif _sw13 == ORDER_TIME_DAY:
            str_.v = 'day'
        elif _sw13 == ORDER_TIME_SPECIFIED:
            str_.v = 'specified'
        elif _sw13 == ORDER_TIME_SPECIFIED_DAY:
            str_.v = 'specified day'
        else:
            str_.v = 'unknown type time ' + _str(type_)
        return str_.v
    def FormatOrder(self, str_):
        type_ = Box("")
        price = Box("")
        tmp_long = Box(0)
        symbol_name = self.Symbol()
        digits = Digits()
        if SymbolInfoInteger(symbol_name, SYMBOL_DIGITS, tmp_long):
            digits = _int(tmp_long.v)
        str_.v = StringFormat('#%I64u %s %s %s', self.Ticket_0(), self.FormatType(type_, self.OrderType()), DoubleToString(self.VolumeInitial(), 2), symbol_name)
        self.FormatPrice(price, self.PriceOpen(), self.PriceStopLimit(), digits)
        if price.v != '':
            str_.v += ' at '
            str_.v += price.v
        return str_.v
    def FormatPrice(self, str_, price_order, price_trigger, digits):
        price = ""
        trigger = ""
        if price_trigger:
            price = DoubleToString(price_order, digits)
            trigger = DoubleToString(price_trigger, digits)
            str_.v = StringFormat('%s (%s)', price, trigger)
        else:
            str_.v = DoubleToString(price_order, digits)
        return str_.v
    def SelectByIndex(self, index):
        ticket = HistoryOrderGetTicket(index)
        if ticket == 0:
            return False
        self.Ticket_1(ticket)
        return True

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'BUY')
    ObjectsDeleteAll(0, 'SELL')
    ObjectsDeleteAll(0, 'SL')
    ObjectsDeleteAll(0, 'TP')
    ObjectsDeleteAll(0, 'BUY LIMIT')
    ObjectsDeleteAll(0, 'BUY STOP')
    ObjectsDeleteAll(0, 'BUY STOP LIMIT')
    ObjectsDeleteAll(0, 'SELL LIMIT')
    ObjectsDeleteAll(0, 'SELL STOP')
    ObjectsDeleteAll(0, 'SELL STOP LIMIT')

def OnInit():
    global text
    text = 'text'
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global direction, ord_id, ord_id_str, pending, pos_id, pos_id_str
    positions = PositionsTotal()
    for i in range(0, positions):
        ResetLastError()
        symbol = _str(PositionGetSymbol(i))
        if symbol != '':
            pos_id = PositionGetInteger(POSITION_IDENTIFIER)
            pos_id_str = _str(pos_id)
            price = PositionGetDouble(POSITION_PRICE_OPEN)
            lots = PositionGetDouble(POSITION_VOLUME)
            stoploss = PositionGetDouble(POSITION_SL)
            takeprofit = PositionGetDouble(POSITION_TP)
            type_ = PositionGetInteger(POSITION_TYPE)
            pos_magic = PositionGetInteger(POSITION_MAGIC)
            Comment_ = PositionGetString(POSITION_COMMENT)
            if symbol == BaseSymbol:
                if type_ == POSITION_TYPE_BUY:
                    direction = 'BUY'
                if type_ == POSITION_TYPE_SELL:
                    direction = 'SELL'
                ObjectCreate(0, direction + ' ' + pos_id_str, OBJ_HLINE, 0, 0, price)
                ObjectSetInteger(0, direction + ' ' + pos_id_str, OBJPROP_COLOR, clrLimeGreen)
                ObjectSetInteger(0, direction + ' ' + pos_id_str, OBJPROP_STYLE, STYLE_DOT)
                ObjectCreate(0, direction + text + ' ' + pos_id_str, OBJ_TEXT, 0, iTime(None, 0, TextBarsBack), price)
                ObjectSetString(0, direction + text + ' ' + pos_id_str, OBJPROP_TEXT, direction + '   ' + _str(lots) + ' lots   ' + '   price ' + DoubleToString(NormalizeDouble(price, Digits()), Digits()) + '     ticket# ' + pos_id_str)
                ObjectSetInteger(0, direction + text + ' ' + pos_id_str, OBJPROP_COLOR, clrWhite)
                ObjectSetString(0, direction + text + ' ' + pos_id_str, OBJPROP_FONT, 'Arial')
                ObjectSetInteger(0, direction + text + ' ' + pos_id_str, OBJPROP_FONTSIZE, 8)
                if stoploss > 0:
                    ObjectCreate(0, 'SL' + ' ' + pos_id_str, OBJ_HLINE, 0, 0, stoploss)
                    ObjectSetInteger(0, 'SL' + ' ' + pos_id_str, OBJPROP_COLOR, clrRed)
                    ObjectSetInteger(0, 'SL' + ' ' + pos_id_str, OBJPROP_STYLE, STYLE_DASHDOT)
                    ObjectCreate(0, 'SL' + text + ' ' + pos_id_str, OBJ_TEXT, 0, iTime(None, 0, TextBarsBack), stoploss)
                    ObjectSetString(0, 'SL' + text + ' ' + pos_id_str, OBJPROP_TEXT, 'SL' + '   ' + _str(lots) + ' lots   ' + '   price ' + DoubleToString(NormalizeDouble(stoploss, Digits()), Digits()) + '     ticket# ' + pos_id_str)
                    ObjectSetInteger(0, 'SL' + text + ' ' + pos_id_str, OBJPROP_COLOR, clrWhite)
                    ObjectSetString(0, 'SL' + text + ' ' + pos_id_str, OBJPROP_FONT, 'Arial')
                    ObjectSetInteger(0, 'SL' + text + ' ' + pos_id_str, OBJPROP_FONTSIZE, 8)
                if takeprofit > 0:
                    ObjectCreate(0, 'TP' + ' ' + pos_id_str, OBJ_HLINE, 0, 0, takeprofit)
                    ObjectSetInteger(0, 'TP' + ' ' + pos_id_str, OBJPROP_COLOR, clrRed)
                    ObjectSetInteger(0, 'TP' + ' ' + pos_id_str, OBJPROP_STYLE, STYLE_DASHDOT)
                    ObjectCreate(0, 'TP' + text + ' ' + pos_id_str, OBJ_TEXT, 0, iTime(None, 0, TextBarsBack), takeprofit)
                    ObjectSetString(0, 'TP' + text + ' ' + pos_id_str, OBJPROP_TEXT, 'TP' + '   ' + _str(lots) + ' lots   ' + '   price ' + DoubleToString(NormalizeDouble(takeprofit, Digits()), Digits()) + '     ticket# ' + pos_id_str)
                    ObjectSetInteger(0, 'TP' + text + ' ' + pos_id_str, OBJPROP_COLOR, clrWhite)
                    ObjectSetString(0, 'TP' + text + ' ' + pos_id_str, OBJPROP_FONT, 'Arial')
                    ObjectSetInteger(0, 'TP' + text + ' ' + pos_id_str, OBJPROP_FONTSIZE, 8)
    HistorySelect(0, TimeCurrent())
    deals = HistoryDealsTotal()
    for i in range(0, deals):
        if dealInfo.SelectByIndex(i):
            if dealInfo.PositionId() == pos_id and dealInfo.Entry() == DEAL_ENTRY_OUT:
                ObjectDelete(0, direction + ' ' + pos_id_str)
                ObjectDelete(0, direction + text + ' ' + pos_id_str)
                ObjectDelete(0, 'SL' + ' ' + pos_id_str)
                ObjectDelete(0, 'SL' + text + ' ' + pos_id_str)
                ObjectDelete(0, 'TP' + ' ' + pos_id_str)
                ObjectDelete(0, 'TP' + text + ' ' + pos_id_str)
        else:
            PrintFormat('Error when receiving into the cache position with index &d.' + ' Error code: %d', i, GetLastError())
    orders = OrdersTotal()
    for i in range(0, orders):
        ResetLastError()
        ticket = OrderGetTicket(i)
        if ticket != 0:
            osymbol = OrderGetString(ORDER_SYMBOL)
            ord_id = OrderGetInteger(ORDER_TICKET)
            ord_id_str = _str(ord_id)
            oprice = OrderGetDouble(ORDER_PRICE_OPEN)
            olots = OrderGetDouble(ORDER_VOLUME_INITIAL)
            ostoploss = OrderGetDouble(ORDER_SL)
            otakeprofit = OrderGetDouble(ORDER_TP)
            otype = OrderGetInteger(ORDER_TYPE)
            ord_magic = OrderGetInteger(ORDER_MAGIC)
            Comment_ = OrderGetString(ORDER_COMMENT)
            if osymbol == BaseSymbol:
                if otype == ORDER_TYPE_BUY_LIMIT:
                    pending = 'BUY LIMIT'
                if otype == ORDER_TYPE_BUY_STOP:
                    pending = 'BUY STOP'
                if otype == ORDER_TYPE_BUY_STOP_LIMIT:
                    pending = 'BUY STOP LIMIT'
                if otype == ORDER_TYPE_SELL_LIMIT:
                    pending = 'SELL LIMIT'
                if otype == ORDER_TYPE_SELL_STOP:
                    pending = 'SELL STOP'
                if otype == ORDER_TYPE_SELL_STOP_LIMIT:
                    pending = 'SELL STOP LIMIT'
                ObjectCreate(0, pending + ' ' + ord_id_str, OBJ_HLINE, 0, 0, oprice)
                ObjectSetInteger(0, pending + ' ' + ord_id_str, OBJPROP_COLOR, clrGreen)
                ObjectSetInteger(0, pending + ' ' + ord_id_str, OBJPROP_STYLE, STYLE_DASHDOT)
                ObjectCreate(0, pending + text + ' ' + ord_id_str, OBJ_TEXT, 0, iTime(None, 0, TextBarsBack), oprice)
                ObjectSetString(0, pending + text + ' ' + ord_id_str, OBJPROP_TEXT, pending + '   ' + _str(olots) + ' lots   ' + '   price ' + DoubleToString(NormalizeDouble(oprice, Digits()), Digits()) + '     ticket# ' + ord_id_str)
                ObjectSetInteger(0, pending + text + ' ' + ord_id_str, OBJPROP_COLOR, clrWhite)
                ObjectSetString(0, pending + text + ' ' + ord_id_str, OBJPROP_FONT, 'Arial')
                ObjectSetInteger(0, pending + text + ' ' + ord_id_str, OBJPROP_FONTSIZE, 8)
                if ostoploss > 0:
                    ObjectCreate(0, 'SL' + ' ' + ord_id_str, OBJ_HLINE, 0, 0, ostoploss)
                    ObjectSetInteger(0, 'SL' + ' ' + ord_id_str, OBJPROP_COLOR, clrRed)
                    ObjectSetInteger(0, 'SL' + ' ' + ord_id_str, OBJPROP_STYLE, STYLE_DASHDOT)
                    ObjectCreate(0, 'SL' + text + ' ' + ord_id_str, OBJ_TEXT, 0, iTime(None, 0, TextBarsBack), ostoploss)
                    ObjectSetString(0, 'SL' + text + ' ' + ord_id_str, OBJPROP_TEXT, 'SL' + '   ' + _str(olots) + ' lots   ' + '   price ' + _str(NormalizeDouble(ostoploss, Digits())) + '     ticket# ' + ord_id_str)
                    ObjectSetInteger(0, 'SL' + text + ' ' + ord_id_str, OBJPROP_COLOR, clrWhite)
                    ObjectSetString(0, 'SL' + text + ' ' + ord_id_str, OBJPROP_FONT, 'Arial')
                    ObjectSetInteger(0, 'SL' + text + ' ' + ord_id_str, OBJPROP_FONTSIZE, 8)
                if otakeprofit > 0:
                    ObjectCreate(0, 'TP' + ' ' + ord_id_str, OBJ_HLINE, 0, 0, otakeprofit)
                    ObjectSetInteger(0, 'TP' + ' ' + ord_id_str, OBJPROP_COLOR, clrRed)
                    ObjectSetInteger(0, 'TP' + ' ' + ord_id_str, OBJPROP_STYLE, STYLE_DASHDOT)
                    ObjectCreate(0, 'TP' + text + ' ' + ord_id_str, OBJ_TEXT, 0, iTime(None, 0, TextBarsBack), otakeprofit)
                    ObjectSetString(0, 'TP' + text + ' ' + ord_id_str, OBJPROP_TEXT, 'TP' + '   ' + _str(olots) + ' lots   ' + '   price ' + DoubleToString(NormalizeDouble(otakeprofit, Digits()), Digits()) + '     ticket# ' + ord_id_str)
                    ObjectSetInteger(0, 'TP' + text + ' ' + ord_id_str, OBJPROP_COLOR, clrWhite)
                    ObjectSetString(0, 'TP' + text + ' ' + ord_id_str, OBJPROP_FONT, 'Arial')
                    ObjectSetInteger(0, 'TP' + text + ' ' + ord_id_str, OBJPROP_FONTSIZE, 8)
    HistorySelect(0, TimeCurrent())
    horders = HistoryOrdersTotal()
    for i in range(0, horders):
        if historyOrderInfo.SelectByIndex(i):
            if historyOrderInfo.Ticket_0() == ord_id and ((((historyOrderInfo.State() == ORDER_STATE_CANCELED or historyOrderInfo.State() == ORDER_STATE_EXPIRED) or historyOrderInfo.State() == ORDER_STATE_FILLED) or historyOrderInfo.State() == ORDER_STATE_PARTIAL) or historyOrderInfo.State() == ORDER_STATE_REJECTED):
                ObjectDelete(0, pending + ' ' + ord_id_str)
                ObjectDelete(0, pending + text + ' ' + ord_id_str)
                ObjectDelete(0, 'SL' + ' ' + ord_id_str)
                ObjectDelete(0, 'SL' + text + ' ' + ord_id_str)
                ObjectDelete(0, 'TP' + ' ' + ord_id_str)
                ObjectDelete(0, 'TP' + text + ' ' + ord_id_str)
        else:
            PrintFormat('Error when receiving into the cache order with index &d.' + ' Error code: %d', i, GetLastError())
    return rates_total

# ---- global variables initialised from expressions
orderInfo = _alloc(COrderInfo)
orderInfo.__init__()
dealInfo = _alloc(CDealInfo)
dealInfo.__init__()
historyOrderInfo = _alloc(CHistoryOrderInfo)
historyOrderInfo.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PositionsOnCustomChartV4(_MQL5Indicator):
    name = 'Positions_on_Custom_Chart_v4'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TextBarsBack': 100,
    }

