"""e_checksampler — converted from MQL5: MQL5 Indicators/Sampler/e_checksampler.mq5

Copyright: Copyright 2012, her.human; Link: her.human@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- The program has no OnCalculate: it draws only chart objects or reacts to events.
- Functions not available here: OrderSendAsync
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, her.human', 'link': 'her.human@gmail.com', 'version': '1.00'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'e_checksampler', 'source': 'MQL5 Indicators/Sampler/e_checksampler.mq5', 'folder': 'Sampler', 'inputs': [{'mql': 'lot', 'py': 'lot', 'param': 'lot', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': False, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

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
POSITION_TIME_UPDATE_MSC = 0  # MQL5 constant unknown to the converter
SYMBOL_EXPIRATION_DAY = 0  # MQL5 constant unknown to the converter
SYMBOL_EXPIRATION_SPECIFIED = 0  # MQL5 constant unknown to the converter
SYMBOL_EXPIRATION_SPECIFIED_DAY = 0  # MQL5 constant unknown to the converter
SYMBOL_ORDER_SL = 0  # MQL5 constant unknown to the converter
SYMBOL_ORDER_STOP_LIMIT = 0  # MQL5 constant unknown to the converter
SYMBOL_ORDER_TP = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_EXECUTION_EXCHANGE = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_EXECUTION_INSTANT = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_EXECUTION_MARKET = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_EXECUTION_REQUEST = 0  # MQL5 constant unknown to the converter

# enum ENUM_LOG_LEVELS
LOG_LEVEL_NO = 0
LOG_LEVEL_ERRORS = 1
LOG_LEVEL_ALL = 2
_enum('ENUM_LOG_LEVELS', {0: 'LOG_LEVEL_NO', 1: 'LOG_LEVEL_ERRORS', 2: 'LOG_LEVEL_ALL'})

# ---- inputs and global variables
lot = _input('lot', 1.0)
signal = Arr(0, 0)
time = Arr(0, 0)
prevtime = 0

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
        _sw5 = type_
        if _sw5 == ORDER_TYPE_BUY:
            str_.v = 'buy'
        elif _sw5 == ORDER_TYPE_SELL:
            str_.v = 'sell'
        elif _sw5 == ORDER_TYPE_BUY_LIMIT:
            str_.v = 'buy limit'
        elif _sw5 == ORDER_TYPE_SELL_LIMIT:
            str_.v = 'sell limit'
        elif _sw5 == ORDER_TYPE_BUY_STOP:
            str_.v = 'buy stop'
        elif _sw5 == ORDER_TYPE_SELL_STOP:
            str_.v = 'sell stop'
        elif _sw5 == ORDER_TYPE_BUY_STOP_LIMIT:
            str_.v = 'buy stop limit'
        elif _sw5 == ORDER_TYPE_SELL_STOP_LIMIT:
            str_.v = 'sell stop limit'
        elif _sw5 == ORDER_TYPE_CLOSE_BY:
            str_.v = 'close by'
        else:
            str_.v = 'unknown order type ' + _str(type_)
        return str_.v
    def FormatStatus(self, str_, status):
        _sw6 = status
        if _sw6 == ORDER_STATE_STARTED:
            str_.v = 'started'
        elif _sw6 == ORDER_STATE_PLACED:
            str_.v = 'placed'
        elif _sw6 == ORDER_STATE_CANCELED:
            str_.v = 'canceled'
        elif _sw6 == ORDER_STATE_PARTIAL:
            str_.v = 'partial'
        elif _sw6 == ORDER_STATE_FILLED:
            str_.v = 'filled'
        elif _sw6 == ORDER_STATE_REJECTED:
            str_.v = 'rejected'
        elif _sw6 == ORDER_STATE_EXPIRED:
            str_.v = 'expired'
        else:
            str_.v = 'unknown order status ' + _str(status)
        return str_.v
    def FormatTypeFilling(self, str_, type_):
        _sw7 = type_
        if _sw7 == ORDER_FILLING_RETURN:
            str_.v = 'return remainder'
        elif _sw7 == ORDER_FILLING_IOC:
            str_.v = 'cancel remainder'
        elif _sw7 == ORDER_FILLING_FOK:
            str_.v = 'fill or kill'
        else:
            str_.v = 'unknown type filling ' + _str(type_)
        return str_.v
    def FormatTypeTime(self, str_, type_):
        _sw8 = type_
        if _sw8 == ORDER_TIME_GTC:
            str_.v = 'gtc'
        elif _sw8 == ORDER_TIME_DAY:
            str_.v = 'day'
        elif _sw8 == ORDER_TIME_SPECIFIED:
            str_.v = 'specified'
        elif _sw8 == ORDER_TIME_SPECIFIED_DAY:
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
        _sw9 = type_
        if _sw9 == POSITION_TYPE_BUY:
            str_.v = 'buy'
        elif _sw9 == POSITION_TYPE_SELL:
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
        _sw10 = self.DealType()
        if _sw10 == DEAL_TYPE_BUY:
            str_ = 'Buy type'
        elif _sw10 == DEAL_TYPE_SELL:
            str_ = 'Sell type'
        elif _sw10 == DEAL_TYPE_BALANCE:
            str_ = 'Balance type'
        elif _sw10 == DEAL_TYPE_CREDIT:
            str_ = 'Credit type'
        elif _sw10 == DEAL_TYPE_CHARGE:
            str_ = 'Charge type'
        elif _sw10 == DEAL_TYPE_CORRECTION:
            str_ = 'Correction type'
        elif _sw10 == DEAL_TYPE_BONUS:
            str_ = 'Bonus type'
        elif _sw10 == DEAL_TYPE_COMMISSION:
            str_ = 'Commission type'
        elif _sw10 == DEAL_TYPE_COMMISSION_DAILY:
            str_ = 'Daily Commission type'
        elif _sw10 == DEAL_TYPE_COMMISSION_MONTHLY:
            str_ = 'Monthly Commission type'
        elif _sw10 == DEAL_TYPE_COMMISSION_AGENT_DAILY:
            str_ = 'Daily Agent Commission type'
        elif _sw10 == DEAL_TYPE_COMMISSION_AGENT_MONTHLY:
            str_ = 'Monthly Agent Commission type'
        elif _sw10 == DEAL_TYPE_INTEREST:
            str_ = 'Interest Rate type'
        elif _sw10 == DEAL_TYPE_BUY_CANCELED:
            str_ = 'Canceled Buy type'
        elif _sw10 == DEAL_TYPE_SELL_CANCELED:
            str_ = 'Canceled Sell type'
        else:
            str_ = 'Unknown type'
        return str_
    def Entry(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_ENTRY)
    def EntryDescription(self):
        str_ = ""
        _sw11 = CDealInfo.Entry(self)
        if _sw11 == DEAL_ENTRY_IN:
            str_ = 'In entry'
        elif _sw11 == DEAL_ENTRY_OUT:
            str_ = 'Out entry'
        elif _sw11 == DEAL_ENTRY_INOUT:
            str_ = 'InOut entry'
        elif _sw11 == DEAL_ENTRY_STATE:
            str_ = 'Status record'
        elif _sw11 == DEAL_ENTRY_OUT_BY:
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
        _sw12 = action
        if _sw12 == DEAL_TYPE_BUY:
            str_.v = 'buy'
        elif _sw12 == DEAL_TYPE_SELL:
            str_.v = 'sell'
        elif _sw12 == DEAL_TYPE_BALANCE:
            str_.v = 'balance'
        elif _sw12 == DEAL_TYPE_CREDIT:
            str_.v = 'credit'
        elif _sw12 == DEAL_TYPE_CHARGE:
            str_.v = 'charge'
        elif _sw12 == DEAL_TYPE_CORRECTION:
            str_.v = 'correction'
        elif _sw12 == DEAL_TYPE_BONUS:
            str_.v = 'bonus'
        elif _sw12 == DEAL_TYPE_COMMISSION:
            str_.v = 'commission'
        elif _sw12 == DEAL_TYPE_COMMISSION_DAILY:
            str_.v = 'daily commission'
        elif _sw12 == DEAL_TYPE_COMMISSION_MONTHLY:
            str_.v = 'monthly commission'
        elif _sw12 == DEAL_TYPE_COMMISSION_AGENT_DAILY:
            str_.v = 'daily agent commission'
        elif _sw12 == DEAL_TYPE_COMMISSION_AGENT_MONTHLY:
            str_.v = 'monthly agent commission'
        elif _sw12 == DEAL_TYPE_INTEREST:
            str_.v = 'interest rate'
        elif _sw12 == DEAL_TYPE_BUY_CANCELED:
            str_.v = 'canceled buy'
        elif _sw12 == DEAL_TYPE_SELL_CANCELED:
            str_.v = 'canceled sell'
        else:
            str_.v = 'unknown deal type ' + _str(action)
        return str_.v
    def FormatEntry(self, str_, entry):
        _sw13 = entry
        if _sw13 == DEAL_ENTRY_IN:
            str_.v = 'in'
        elif _sw13 == DEAL_ENTRY_OUT:
            str_.v = 'out'
        elif _sw13 == DEAL_ENTRY_INOUT:
            str_.v = 'in/out'
        elif _sw13 == DEAL_ENTRY_OUT_BY:
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
        _sw14 = self.DealType()
        if _sw14 in (DEAL_TYPE_BUY, DEAL_TYPE_SELL):
            str_.v = StringFormat('#%I64u %s %s %s at %s', self.Ticket_0(), self.FormatAction(type_, self.DealType()), DoubleToString(self.Volume(), 2), symbol_name, DoubleToString(self.Price(), digits))
        elif _sw14 in (DEAL_TYPE_BALANCE, DEAL_TYPE_CREDIT, DEAL_TYPE_CHARGE, DEAL_TYPE_CORRECTION, DEAL_TYPE_BONUS, DEAL_TYPE_COMMISSION, DEAL_TYPE_COMMISSION_DAILY, DEAL_TYPE_COMMISSION_MONTHLY, DEAL_TYPE_COMMISSION_AGENT_DAILY, DEAL_TYPE_COMMISSION_AGENT_MONTHLY, DEAL_TYPE_INTEREST):
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

class CTrade(CObject):
    _q_fields = ('m_request', 'm_result', 'm_check_result', 'm_async_mode', 'm_magic', 'm_deviation', 'm_type_filling', 'm_margin_mode', 'm_log_level')
    def __init__(self):
        CObject.__init__(self)
        self.m_request = MqlTradeRequest()
        self.m_result = MqlTradeResult()
        self.m_check_result = MqlTradeCheckResult()
        self.m_async_mode = False
        self.m_magic = 0
        self.m_deviation = 0
        self.m_type_filling = 0
        self.m_margin_mode = 0
        self.m_log_level = 0
        self.m_async_mode = False
        self.m_magic = 0
        self.m_deviation = 10
        self.m_type_filling = ORDER_FILLING_FOK
        self.m_log_level = LOG_LEVEL_ERRORS
        self.SetMarginMode()
        self.ClearStructures()
        if MQLInfoInteger(MQL_TESTER):
            self.m_log_level = LOG_LEVEL_ALL
        if MQLInfoInteger(MQL_OPTIMIZATION):
            self.m_log_level = LOG_LEVEL_NO
    def _q_dtor(self):
        pass
    def LogLevel(self, log_level):
        self.m_log_level = log_level
    def Request(self, request):
        request.action = self.m_request.action
        request.magic = self.m_request.magic
        request.order = self.m_request.order
        request.symbol = self.m_request.symbol
        request.volume = self.m_request.volume
        request.price = self.m_request.price
        request.stoplimit = self.m_request.stoplimit
        request.sl = self.m_request.sl
        request.tp = self.m_request.tp
        request.deviation = self.m_request.deviation
        request.type = self.m_request.type
        request.type_filling = self.m_request.type_filling
        request.type_time = self.m_request.type_time
        request.expiration = self.m_request.expiration
        request.comment = self.m_request.comment
        request.position = self.m_request.position
        request.position_by = self.m_request.position_by
    def RequestAction(self):
        return _int(self.m_request.action)
    def RequestActionDescription(self):
        str_ = Box("")
        self.FormatRequest(str_, self.m_request)
        return str_.v
    def RequestMagic(self):
        return _ulong(self.m_request.magic)
    def RequestOrder(self):
        return _ulong(self.m_request.order)
    def RequestPosition(self):
        return _ulong(self.m_request.position)
    def RequestPositionBy(self):
        return _ulong(self.m_request.position_by)
    def RequestSymbol(self):
        return _str(self.m_request.symbol)
    def RequestVolume(self):
        return self.m_request.volume
    def RequestPrice(self):
        return self.m_request.price
    def RequestStopLimit(self):
        return self.m_request.stoplimit
    def RequestSL(self):
        return self.m_request.sl
    def RequestTP(self):
        return self.m_request.tp
    def RequestDeviation(self):
        return _ulong(self.m_request.deviation)
    def RequestType(self):
        return _int(self.m_request.type)
    def RequestTypeDescription(self):
        str_ = Box("")
        self.FormatOrderType(str_, _uint(self.m_request.order))
        return str_.v
    def RequestTypeFilling(self):
        return _int(self.m_request.type_filling)
    def RequestTypeFillingDescription(self):
        str_ = Box("")
        self.FormatOrderTypeFilling(str_, _uint(self.m_request.type_filling))
        return str_.v
    def RequestTypeTime(self):
        return _int(self.m_request.type_time)
    def RequestTypeTimeDescription(self):
        str_ = Box("")
        self.FormatOrderTypeTime(str_, _uint(self.m_request.type_time))
        return str_.v
    def RequestExpiration(self):
        return _long(self.m_request.expiration)
    def RequestComment(self):
        return _str(self.m_request.comment)
    def Result(self, result):
        result.retcode = self.m_result.retcode
        result.deal = self.m_result.deal
        result.order = self.m_result.order
        result.volume = self.m_result.volume
        result.price = self.m_result.price
        result.bid = self.m_result.bid
        result.ask = self.m_result.ask
        result.comment = self.m_result.comment
        result.request_id = self.m_result.request_id
        result.retcode_external = self.m_result.retcode_external
    def ResultRetcode(self):
        return _uint(self.m_result.retcode)
    def ResultRetcodeDescription(self):
        str_ = Box("")
        self.FormatRequestResult(str_, self.m_request, self.m_result)
        return str_.v
    def ResultRetcodeExternal(self):
        return _int(self.m_result.retcode_external)
    def ResultDeal(self):
        return _ulong(self.m_result.deal)
    def ResultOrder(self):
        return _ulong(self.m_result.order)
    def ResultVolume(self):
        return self.m_result.volume
    def ResultPrice(self):
        return self.m_result.price
    def ResultBid(self):
        return self.m_result.bid
    def ResultAsk(self):
        return self.m_result.ask
    def ResultComment(self):
        return _str(self.m_result.comment)
    def CheckResult(self, check_result):
        check_result.retcode = self.m_check_result.retcode
        check_result.balance = self.m_check_result.balance
        check_result.equity = self.m_check_result.equity
        check_result.profit = self.m_check_result.profit
        check_result.margin = self.m_check_result.margin
        check_result.margin_free = self.m_check_result.margin_free
        check_result.margin_level = self.m_check_result.margin_level
        check_result.comment = self.m_check_result.comment
    def CheckResultRetcode(self):
        return _uint(self.m_check_result.retcode)
    def CheckResultRetcodeDescription(self):
        str_ = Box("")
        result = MqlTradeResult()
        result.retcode = self.m_check_result.retcode
        self.FormatRequestResult(str_, self.m_request, result)
        return str_.v
    def CheckResultBalance(self):
        return self.m_check_result.balance
    def CheckResultEquity(self):
        return self.m_check_result.equity
    def CheckResultProfit(self):
        return self.m_check_result.profit
    def CheckResultMargin(self):
        return self.m_check_result.margin
    def CheckResultMarginFree(self):
        return self.m_check_result.margin_free
    def CheckResultMarginLevel(self):
        return self.m_check_result.margin_level
    def CheckResultComment(self):
        return _str(self.m_check_result.comment)
    def SetAsyncMode(self, mode):
        self.m_async_mode = mode
    def SetExpertMagicNumber(self, magic):
        self.m_magic = magic
    def SetDeviationInPoints(self, deviation):
        self.m_deviation = deviation
    def SetTypeFilling(self, filling):
        self.m_type_filling = filling
    def SetTypeFillingBySymbol(self, symbol):
        filling = _uint(SymbolInfoInteger(symbol, SYMBOL_FILLING_MODE))
        if (filling & SYMBOL_FILLING_FOK) == SYMBOL_FILLING_FOK:
            self.m_type_filling = ORDER_FILLING_FOK
            return True
        if (filling & SYMBOL_FILLING_IOC) == SYMBOL_FILLING_IOC:
            self.m_type_filling = ORDER_FILLING_IOC
            return True
        return False
    def SetMarginMode(self):
        self.m_margin_mode = AccountInfoInteger(ACCOUNT_MARGIN_MODE)
    def PositionOpen(self, symbol, order_type, volume, price, sl, tp, comment=''):
        if self.IsStopped('CTrade::PositionOpen'):
            return False
        self.ClearStructures()
        if order_type != ORDER_TYPE_BUY and order_type != ORDER_TYPE_SELL:
            self.m_result.retcode = TRADE_RETCODE_INVALID
            self.m_result.comment = 'Invalid order type'
            return False
        self.m_request.action = TRADE_ACTION_DEAL
        self.m_request.symbol = symbol
        self.m_request.magic = self.m_magic
        self.m_request.volume = volume
        self.m_request.type = order_type
        self.m_request.price = price
        self.m_request.sl = sl
        self.m_request.tp = tp
        self.m_request.deviation = self.m_deviation
        if not self.OrderTypeCheck(symbol):
            return False
        if not self.FillingCheck(symbol):
            return False
        self.m_request.comment = comment
        return self.OrderSend(self.m_request, self.m_result)
    def PositionModify_1(self, symbol, sl, tp):
        if self.IsStopped('CTrade::PositionModify'):
            return False
        if not self.SelectPosition(symbol):
            return False
        self.ClearStructures()
        self.m_request.action = TRADE_ACTION_SLTP
        self.m_request.symbol = symbol
        self.m_request.magic = self.m_magic
        self.m_request.sl = sl
        self.m_request.tp = tp
        self.m_request.position = PositionGetInteger(POSITION_TICKET)
        return self.OrderSend(self.m_request, self.m_result)
    def PositionModify_2(self, ticket, sl, tp):
        if self.IsStopped('CTrade::PositionModify'):
            return False
        if not PositionSelectByTicket(ticket):
            return False
        self.ClearStructures()
        self.m_request.action = TRADE_ACTION_SLTP
        self.m_request.position = ticket
        self.m_request.symbol = PositionGetString(POSITION_SYMBOL)
        self.m_request.magic = self.m_magic
        self.m_request.sl = sl
        self.m_request.tp = tp
        return self.OrderSend(self.m_request, self.m_result)
    def PositionClose_1(self, symbol, deviation=ULONG_MAX):
        partial_close = False
        retry_count = 10
        retcode = TRADE_RETCODE_REJECT
        if self.IsStopped('CTrade::PositionClose'):
            return False
        self.ClearStructures()
        if not self.FillingCheck(symbol):
            return False
        while True:
            if self.SelectPosition(symbol):
                if PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY:
                    self.m_request.type = ORDER_TYPE_SELL
                    self.m_request.price = SymbolInfoDouble(symbol, SYMBOL_BID)
                else:
                    self.m_request.type = ORDER_TYPE_BUY
                    self.m_request.price = SymbolInfoDouble(symbol, SYMBOL_ASK)
            else:
                self.m_result.retcode = retcode
                return False
            self.m_request.action = TRADE_ACTION_DEAL
            self.m_request.symbol = symbol
            self.m_request.volume = PositionGetDouble(POSITION_VOLUME)
            self.m_request.magic = self.m_magic
            self.m_request.deviation = (self.m_deviation if (deviation == ULONG_MAX) else deviation)
            self.m_request.position = PositionGetInteger(POSITION_TICKET)
            max_volume = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX)
            if self.m_request.volume > max_volume:
                self.m_request.volume = max_volume
                partial_close = True
            else:
                partial_close = False
            if self.IsHedging():
                return self.OrderSend(self.m_request, self.m_result)
            if not self.OrderSend(self.m_request, self.m_result):
                if (retry_count := retry_count - 1) != 0:
                    if not partial_close:
                        break
                    continue
                if retcode == TRADE_RETCODE_DONE_PARTIAL:
                    self.m_result.retcode = retcode
                return False
            if self.m_async_mode:
                break
            retcode = TRADE_RETCODE_DONE_PARTIAL
            if partial_close:
                Sleep(1000)
            if not partial_close:
                break
        return True
    def PositionClose_2(self, ticket, deviation=ULONG_MAX):
        if self.IsStopped('CTrade::PositionClose'):
            return False
        if not PositionSelectByTicket(ticket):
            return False
        symbol = PositionGetString(POSITION_SYMBOL)
        self.ClearStructures()
        if not self.FillingCheck(symbol):
            return False
        if PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY:
            self.m_request.type = ORDER_TYPE_SELL
            self.m_request.price = SymbolInfoDouble(symbol, SYMBOL_BID)
        else:
            self.m_request.type = ORDER_TYPE_BUY
            self.m_request.price = SymbolInfoDouble(symbol, SYMBOL_ASK)
        self.m_request.action = TRADE_ACTION_DEAL
        self.m_request.position = ticket
        self.m_request.symbol = symbol
        self.m_request.volume = PositionGetDouble(POSITION_VOLUME)
        self.m_request.magic = self.m_magic
        self.m_request.deviation = (self.m_deviation if (deviation == ULONG_MAX) else deviation)
        return self.OrderSend(self.m_request, self.m_result)
    def PositionCloseBy(self, ticket, ticket_by):
        if self.IsStopped('CTrade::PositionCloseBy'):
            return False
        if not self.IsHedging():
            return False
        if not PositionSelectByTicket(ticket):
            return False
        symbol = PositionGetString(POSITION_SYMBOL)
        type_ = PositionGetInteger(POSITION_TYPE)
        if not PositionSelectByTicket(ticket_by):
            return False
        symbol_by = PositionGetString(POSITION_SYMBOL)
        type_by = PositionGetInteger(POSITION_TYPE)
        if type_ == type_by:
            return False
        if symbol != symbol_by:
            return False
        self.ClearStructures()
        if not self.FillingCheck(symbol):
            return False
        self.m_request.action = TRADE_ACTION_CLOSE_BY
        self.m_request.position = ticket
        self.m_request.position_by = ticket_by
        self.m_request.magic = self.m_magic
        return self.OrderSend(self.m_request, self.m_result)
    def PositionClosePartial_1(self, symbol, volume, deviation=ULONG_MAX):
        retcode = TRADE_RETCODE_REJECT
        if self.IsStopped('CTrade::PositionClosePartial'):
            return False
        if not self.IsHedging():
            return False
        self.ClearStructures()
        if not self.FillingCheck(symbol):
            return False
        if self.SelectPosition(symbol):
            if PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY:
                self.m_request.type = ORDER_TYPE_SELL
                self.m_request.price = SymbolInfoDouble(symbol, SYMBOL_BID)
            else:
                self.m_request.type = ORDER_TYPE_BUY
                self.m_request.price = SymbolInfoDouble(symbol, SYMBOL_ASK)
        else:
            self.m_result.retcode = retcode
            return False
        position_volume = PositionGetDouble(POSITION_VOLUME)
        if position_volume > volume:
            position_volume = volume
        self.m_request.action = TRADE_ACTION_DEAL
        self.m_request.symbol = symbol
        self.m_request.volume = position_volume
        self.m_request.magic = self.m_magic
        self.m_request.deviation = (self.m_deviation if (deviation == ULONG_MAX) else deviation)
        self.m_request.position = PositionGetInteger(POSITION_TICKET)
        return self.OrderSend(self.m_request, self.m_result)
    def PositionClosePartial_2(self, ticket, volume, deviation=ULONG_MAX):
        if self.IsStopped('CTrade::PositionClosePartial'):
            return False
        if not self.IsHedging():
            return False
        if not PositionSelectByTicket(ticket):
            return False
        symbol = PositionGetString(POSITION_SYMBOL)
        self.ClearStructures()
        if not self.FillingCheck(symbol):
            return False
        if PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY:
            self.m_request.type = ORDER_TYPE_SELL
            self.m_request.price = SymbolInfoDouble(symbol, SYMBOL_BID)
        else:
            self.m_request.type = ORDER_TYPE_BUY
            self.m_request.price = SymbolInfoDouble(symbol, SYMBOL_ASK)
        position_volume = PositionGetDouble(POSITION_VOLUME)
        if position_volume > volume:
            position_volume = volume
        self.m_request.action = TRADE_ACTION_DEAL
        self.m_request.position = ticket
        self.m_request.symbol = symbol
        self.m_request.volume = position_volume
        self.m_request.magic = self.m_magic
        self.m_request.deviation = (self.m_deviation if (deviation == ULONG_MAX) else deviation)
        return self.OrderSend(self.m_request, self.m_result)
    def OrderOpen(self, symbol, order_type, volume, limit_price, price, sl, tp, type_time=ORDER_TIME_GTC, expiration=0, comment=''):
        if self.IsStopped('CTrade::OrderOpen'):
            return False
        self.ClearStructures()
        if not self.FillingCheck(symbol):
            return False
        if order_type == ORDER_TYPE_BUY or order_type == ORDER_TYPE_SELL:
            self.m_result.retcode = TRADE_RETCODE_INVALID
            self.m_result.comment = 'Invalid order type'
            return False
        if type_time == ORDER_TIME_GTC and expiration == 0:
            exp_ = _int(SymbolInfoInteger(symbol, SYMBOL_EXPIRATION_MODE))
            if (exp_ & SYMBOL_EXPIRATION_GTC) != SYMBOL_EXPIRATION_GTC:
                if (exp_ & SYMBOL_EXPIRATION_DAY) != SYMBOL_EXPIRATION_DAY:
                    Print('CTrade::OrderOpen', ': Error: Unable to place order without explicitly specified expiration time')
                    self.m_result.retcode = TRADE_RETCODE_INVALID_EXPIRATION
                    self.m_result.comment = 'Invalid expiration type'
                    return False
                type_time = ORDER_TIME_DAY
        self.m_request.action = TRADE_ACTION_PENDING
        self.m_request.symbol = symbol
        self.m_request.magic = self.m_magic
        self.m_request.volume = volume
        self.m_request.type = order_type
        self.m_request.stoplimit = limit_price
        self.m_request.price = price
        self.m_request.sl = sl
        self.m_request.tp = tp
        self.m_request.type_time = type_time
        self.m_request.expiration = expiration
        if not self.OrderTypeCheck(symbol):
            return False
        if not self.FillingCheck(symbol):
            self.m_result.retcode = TRADE_RETCODE_INVALID_FILL
            Print('CTrade::OrderOpen' + ': Invalid filling type')
            return False
        if not self.ExpirationCheck(symbol):
            self.m_result.retcode = TRADE_RETCODE_INVALID_EXPIRATION
            Print('CTrade::OrderOpen' + ': Invalid expiration type')
            return False
        self.m_request.comment = comment
        return self.OrderSend(self.m_request, self.m_result)
    def OrderModify(self, ticket, price, sl, tp, type_time, expiration, stoplimit=0.0):
        if self.IsStopped('CTrade::OrderModify'):
            return False
        if not OrderSelect(ticket):
            return False
        self.ClearStructures()
        self.m_request.symbol = OrderGetString(ORDER_SYMBOL)
        self.m_request.action = TRADE_ACTION_MODIFY
        self.m_request.magic = self.m_magic
        self.m_request.order = ticket
        self.m_request.price = price
        self.m_request.stoplimit = stoplimit
        self.m_request.sl = sl
        self.m_request.tp = tp
        self.m_request.type_time = type_time
        self.m_request.expiration = expiration
        return self.OrderSend(self.m_request, self.m_result)
    def OrderDelete(self, ticket):
        if self.IsStopped('CTrade::OrderDelete'):
            return False
        self.ClearStructures()
        self.m_request.action = TRADE_ACTION_REMOVE
        self.m_request.magic = self.m_magic
        self.m_request.order = ticket
        return self.OrderSend(self.m_request, self.m_result)
    def Buy(self, volume, symbol=None, price=0.0, sl=0.0, tp=0.0, comment=''):
        if volume <= 0.0:
            self.m_result.retcode = TRADE_RETCODE_INVALID_VOLUME
            return False
        symbol_name = (Symbol() if (symbol == "") else symbol)
        if price == 0.0:
            price = SymbolInfoDouble(symbol_name, SYMBOL_ASK)
        return self.PositionOpen(symbol_name, ORDER_TYPE_BUY, volume, price, sl, tp, comment)
    def Sell(self, volume, symbol=None, price=0.0, sl=0.0, tp=0.0, comment=''):
        if volume <= 0.0:
            self.m_result.retcode = TRADE_RETCODE_INVALID_VOLUME
            return False
        symbol_name = (Symbol() if (symbol == "") else symbol)
        if price == 0.0:
            price = SymbolInfoDouble(symbol_name, SYMBOL_BID)
        return self.PositionOpen(symbol_name, ORDER_TYPE_SELL, volume, price, sl, tp, comment)
    def BuyLimit(self, volume, price, symbol=None, sl=0.0, tp=0.0, type_time=ORDER_TIME_GTC, expiration=0, comment=''):
        symbol_name = ""
        if volume <= 0.0:
            self.m_result.retcode = TRADE_RETCODE_INVALID_VOLUME
            return False
        symbol_name = (Symbol() if (symbol == "") else symbol)
        return self.OrderOpen(symbol_name, ORDER_TYPE_BUY_LIMIT, volume, 0.0, price, sl, tp, type_time, expiration, comment)
    def BuyStop(self, volume, price, symbol=None, sl=0.0, tp=0.0, type_time=ORDER_TIME_GTC, expiration=0, comment=''):
        symbol_name = ""
        if volume <= 0.0:
            self.m_result.retcode = TRADE_RETCODE_INVALID_VOLUME
            return False
        symbol_name = (Symbol() if (symbol == "") else symbol)
        return self.OrderOpen(symbol_name, ORDER_TYPE_BUY_STOP, volume, 0.0, price, sl, tp, type_time, expiration, comment)
    def SellLimit(self, volume, price, symbol=None, sl=0.0, tp=0.0, type_time=ORDER_TIME_GTC, expiration=0, comment=''):
        symbol_name = ""
        if volume <= 0.0:
            self.m_result.retcode = TRADE_RETCODE_INVALID_VOLUME
            return False
        symbol_name = (Symbol() if (symbol == "") else symbol)
        return self.OrderOpen(symbol_name, ORDER_TYPE_SELL_LIMIT, volume, 0.0, price, sl, tp, type_time, expiration, comment)
    def SellStop(self, volume, price, symbol=None, sl=0.0, tp=0.0, type_time=ORDER_TIME_GTC, expiration=0, comment=''):
        symbol_name = ""
        if volume <= 0.0:
            self.m_result.retcode = TRADE_RETCODE_INVALID_VOLUME
            return False
        symbol_name = (Symbol() if (symbol == "") else symbol)
        return self.OrderOpen(symbol_name, ORDER_TYPE_SELL_STOP, volume, 0.0, price, sl, tp, type_time, expiration, comment)
    def CheckVolume(self, symbol, volume, price, order_type):
        if order_type != ORDER_TYPE_BUY and order_type != ORDER_TYPE_SELL:
            return 0.0
        free_margin = AccountInfoDouble(ACCOUNT_MARGIN_FREE)
        if free_margin <= 0.0:
            return 0.0
        self.ClearStructures()
        self.m_request.action = TRADE_ACTION_DEAL
        self.m_request.symbol = symbol
        self.m_request.volume = volume
        self.m_request.type = order_type
        self.m_request.price = price
        if (not OrderCheck(self.m_request, self.m_check_result)) and self.m_check_result.margin_free < 0.0:
            coeff = _fdiv(free_margin, free_margin - self.m_check_result.margin_free)
            lots = NormalizeDouble(volume * coeff, 2)
            if lots < volume:
                stepvol = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP)
                if stepvol > 0.0:
                    volume = stepvol * (MathFloor(_fdiv(lots, stepvol)) - 1)
                minvol = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN)
                if volume < minvol:
                    volume = 0.0
        return volume
    def OrderCheck(self, request, check_result):
        return OrderCheck(request, check_result)
    def OrderSend(self, request, result):
        res = False
        action = Box('')
        fmt = Box('')
        if self.m_async_mode:
            res = _bool(_missing('OrderSendAsync')(request, result))
        else:
            res = OrderSend(request, result)
        if res:
            if self.m_log_level > LOG_LEVEL_ERRORS:
                PrintFormat('CTrade::OrderSend' + ': %s [%s]', self.FormatRequest(action, request), self.FormatRequestResult(fmt, request, result))
        else:
            if self.m_log_level > LOG_LEVEL_NO:
                PrintFormat('CTrade::OrderSend' + ': %s [%s]', self.FormatRequest(action, request), self.FormatRequestResult(fmt, request, result))
        return res
    def PrintRequest(self):
        if self.m_log_level < LOG_LEVEL_ALL:
            return
        str_ = Box("")
        PrintFormat('%s', self.FormatRequest(str_, self.m_request))
    def PrintResult(self):
        if self.m_log_level < LOG_LEVEL_ALL:
            return
        str_ = Box("")
        PrintFormat('%s', self.FormatRequestResult(str_, self.m_request, self.m_result))
    def FormatPositionType(self, str_, type_):
        _sw15 = type_
        if _sw15 == POSITION_TYPE_BUY:
            str_.v = 'buy'
        elif _sw15 == POSITION_TYPE_SELL:
            str_.v = 'sell'
        else:
            str_.v = 'unknown position type ' + _str(type_)
        return str_.v
    def FormatOrderType(self, str_, type_):
        _sw16 = type_
        if _sw16 == ORDER_TYPE_BUY:
            str_.v = 'buy'
        elif _sw16 == ORDER_TYPE_SELL:
            str_.v = 'sell'
        elif _sw16 == ORDER_TYPE_BUY_LIMIT:
            str_.v = 'buy limit'
        elif _sw16 == ORDER_TYPE_SELL_LIMIT:
            str_.v = 'sell limit'
        elif _sw16 == ORDER_TYPE_BUY_STOP:
            str_.v = 'buy stop'
        elif _sw16 == ORDER_TYPE_SELL_STOP:
            str_.v = 'sell stop'
        elif _sw16 == ORDER_TYPE_BUY_STOP_LIMIT:
            str_.v = 'buy stop limit'
        elif _sw16 == ORDER_TYPE_SELL_STOP_LIMIT:
            str_.v = 'sell stop limit'
        else:
            str_.v = 'unknown order type ' + _str(type_)
        return str_.v
    def FormatOrderStatus(self, str_, status):
        pass
    def FormatOrderTypeFilling(self, str_, type_):
        _sw17 = type_
        if _sw17 == ORDER_FILLING_RETURN:
            str_.v = 'return remainder'
        elif _sw17 == ORDER_FILLING_IOC:
            str_.v = 'cancel remainder'
        elif _sw17 == ORDER_FILLING_FOK:
            str_.v = 'fill or kill'
        else:
            str_.v = 'unknown type filling ' + _str(type_)
        return str_.v
    def FormatOrderTypeTime(self, str_, type_):
        _sw18 = type_
        if _sw18 == ORDER_TIME_GTC:
            str_.v = 'gtc'
        elif _sw18 == ORDER_TIME_DAY:
            str_.v = 'day'
        elif _sw18 == ORDER_TIME_SPECIFIED:
            str_.v = 'specified'
        elif _sw18 == ORDER_TIME_SPECIFIED_DAY:
            str_.v = 'specified day'
        else:
            str_.v = 'unknown type time ' + _str(type_)
        return str_.v
    def FormatOrderPrice(self, str_, price_order, price_trigger, digits):
        price = ""
        trigger = ""
        if price_trigger:
            price = DoubleToString(price_order, digits)
            trigger = DoubleToString(price_trigger, digits)
            str_.v = StringFormat('%s (%s)', price, trigger)
        else:
            str_.v = DoubleToString(price_order, digits)
        return str_.v
    def FormatRequest(self, str_, request):
        type_ = Box("")
        price = Box("")
        price_new = Box("")
        tmp_string = ""
        tmp_long = Box(0)
        str_.v = ''
        symbol_name = (Symbol() if (request.symbol is None) else request.symbol)
        digits = Digits()
        trade_execution = 0
        if SymbolInfoInteger(symbol_name, SYMBOL_DIGITS, tmp_long):
            digits = _int(tmp_long.v)
        if SymbolInfoInteger(symbol_name, SYMBOL_TRADE_EXEMODE, tmp_long):
            trade_execution = tmp_long.v
        _sw19 = request.action
        if _sw19 == TRADE_ACTION_DEAL:
            _sw20 = trade_execution
            if _sw20 == SYMBOL_TRADE_EXECUTION_REQUEST:
                if self.IsHedging() and request.position != 0:
                    str_.v = StringFormat('request %s %s position #%I64u %s at %s', self.FormatOrderType(type_, _uint(request.type)), DoubleToString(request.volume, 2), request.position, request.symbol, DoubleToString(request.price, digits))
                else:
                    str_.v = StringFormat('request %s %s %s at %s', self.FormatOrderType(type_, _uint(request.type)), DoubleToString(request.volume, 2), request.symbol, DoubleToString(request.price, digits))
                if request.sl != 0.0:
                    tmp_string = StringFormat(' sl: %s', DoubleToString(request.sl, digits))
                    str_.v += tmp_string
                if request.tp != 0.0:
                    tmp_string = StringFormat(' tp: %s', DoubleToString(request.tp, digits))
                    str_.v += tmp_string
            elif _sw20 == SYMBOL_TRADE_EXECUTION_INSTANT:
                if self.IsHedging() and request.position != 0:
                    str_.v = StringFormat('instant %s %s position #%I64u %s at %s', self.FormatOrderType(type_, _uint(request.type)), DoubleToString(request.volume, 2), request.position, request.symbol, DoubleToString(request.price, digits))
                else:
                    str_.v = StringFormat('instant %s %s %s at %s', self.FormatOrderType(type_, _uint(request.type)), DoubleToString(request.volume, 2), request.symbol, DoubleToString(request.price, digits))
                if request.sl != 0.0:
                    tmp_string = StringFormat(' sl: %s', DoubleToString(request.sl, digits))
                    str_.v += tmp_string
                if request.tp != 0.0:
                    tmp_string = StringFormat(' tp: %s', DoubleToString(request.tp, digits))
                    str_.v += tmp_string
            elif _sw20 == SYMBOL_TRADE_EXECUTION_MARKET:
                if self.IsHedging() and request.position != 0:
                    str_.v = StringFormat('market %s %s position #%I64u %s', self.FormatOrderType(type_, _uint(request.type)), DoubleToString(request.volume, 2), request.position, request.symbol)
                else:
                    str_.v = StringFormat('market %s %s %s', self.FormatOrderType(type_, _uint(request.type)), DoubleToString(request.volume, 2), request.symbol)
                if request.sl != 0.0:
                    tmp_string = StringFormat(' sl: %s', DoubleToString(request.sl, digits))
                    str_.v += tmp_string
                if request.tp != 0.0:
                    tmp_string = StringFormat(' tp: %s', DoubleToString(request.tp, digits))
                    str_.v += tmp_string
            elif _sw20 == SYMBOL_TRADE_EXECUTION_EXCHANGE:
                if self.IsHedging() and request.position != 0:
                    str_.v = StringFormat('exchange %s %s position #%I64u %s', self.FormatOrderType(type_, _uint(request.type)), DoubleToString(request.volume, 2), request.position, request.symbol)
                else:
                    str_.v = StringFormat('exchange %s %s %s', self.FormatOrderType(type_, _uint(request.type)), DoubleToString(request.volume, 2), request.symbol)
                if request.sl != 0.0:
                    tmp_string = StringFormat(' sl: %s', DoubleToString(request.sl, digits))
                    str_.v += tmp_string
                if request.tp != 0.0:
                    tmp_string = StringFormat(' tp: %s', DoubleToString(request.tp, digits))
                    str_.v += tmp_string
        elif _sw19 == TRADE_ACTION_PENDING:
            str_.v = StringFormat('%s %s %s at %s', self.FormatOrderType(type_, _uint(request.type)), DoubleToString(request.volume, 2), request.symbol, self.FormatOrderPrice(price, request.price, request.stoplimit, digits))
            if request.sl != 0.0:
                tmp_string = StringFormat(' sl: %s', DoubleToString(request.sl, digits))
                str_.v += tmp_string
            if request.tp != 0.0:
                tmp_string = StringFormat(' tp: %s', DoubleToString(request.tp, digits))
                str_.v += tmp_string
        elif _sw19 == TRADE_ACTION_SLTP:
            if self.IsHedging() and request.position != 0:
                str_.v = StringFormat('modify position #%I64u %s (sl: %s, tp: %s)', request.position, request.symbol, DoubleToString(request.sl, digits), DoubleToString(request.tp, digits))
            else:
                str_.v = StringFormat('modify %s (sl: %s, tp: %s)', request.symbol, DoubleToString(request.sl, digits), DoubleToString(request.tp, digits))
        elif _sw19 == TRADE_ACTION_MODIFY:
            str_.v = StringFormat('modify #%I64u at %s (sl: %s tp: %s)', request.order, self.FormatOrderPrice(price_new, request.price, request.stoplimit, digits), DoubleToString(request.sl, digits), DoubleToString(request.tp, digits))
        elif _sw19 == TRADE_ACTION_REMOVE:
            str_.v = StringFormat('cancel #%I64u', request.order)
        elif _sw19 == TRADE_ACTION_CLOSE_BY:
            if self.IsHedging() and request.position != 0:
                str_.v = StringFormat('close position #%I64u by #%I64u', request.position, request.position_by)
            else:
                str_.v = StringFormat('wrong action close by (#%I64u by #%I64u)', request.position, request.position_by)
        else:
            str_.v = 'unknown action ' + _str(request.action)
        return str_.v
    def FormatRequestResult(self, str_, request, result):
        symbol_name = (Symbol() if (request.symbol is None) else request.symbol)
        digits = Digits()
        tmp_long = Box(0)
        trade_execution = 0
        if SymbolInfoInteger(symbol_name, SYMBOL_DIGITS, tmp_long):
            digits = _int(tmp_long.v)
        if SymbolInfoInteger(symbol_name, SYMBOL_TRADE_EXEMODE, tmp_long):
            trade_execution = tmp_long.v
        _sw21 = result.retcode
        if _sw21 == TRADE_RETCODE_REQUOTE:
            str_.v = StringFormat('requote (%s/%s)', DoubleToString(result.bid, digits), DoubleToString(result.ask, digits))
        elif _sw21 == TRADE_RETCODE_DONE:
            if request.action == TRADE_ACTION_DEAL and ((trade_execution == SYMBOL_TRADE_EXECUTION_REQUEST or trade_execution == SYMBOL_TRADE_EXECUTION_INSTANT) or trade_execution == SYMBOL_TRADE_EXECUTION_MARKET):
                str_.v = StringFormat('done at %s', DoubleToString(result.price, digits))
            else:
                str_.v = 'done'
        elif _sw21 == TRADE_RETCODE_DONE_PARTIAL:
            if request.action == TRADE_ACTION_DEAL and ((trade_execution == SYMBOL_TRADE_EXECUTION_REQUEST or trade_execution == SYMBOL_TRADE_EXECUTION_INSTANT) or trade_execution == SYMBOL_TRADE_EXECUTION_MARKET):
                str_.v = StringFormat('done partially %s at %s', DoubleToString(result.volume, 2), DoubleToString(result.price, digits))
            else:
                str_.v = StringFormat('done partially %s', DoubleToString(result.volume, 2))
        elif _sw21 == TRADE_RETCODE_REJECT:
            str_.v = 'rejected'
        elif _sw21 == TRADE_RETCODE_CANCEL:
            str_.v = 'canceled'
        elif _sw21 == TRADE_RETCODE_PLACED:
            str_.v = 'placed'
        elif _sw21 == TRADE_RETCODE_ERROR:
            str_.v = 'common error'
        elif _sw21 == TRADE_RETCODE_TIMEOUT:
            str_.v = 'timeout'
        elif _sw21 == TRADE_RETCODE_INVALID:
            str_.v = 'invalid request'
        elif _sw21 == TRADE_RETCODE_INVALID_VOLUME:
            str_.v = 'invalid volume'
        elif _sw21 == TRADE_RETCODE_INVALID_PRICE:
            str_.v = 'invalid price'
        elif _sw21 == TRADE_RETCODE_INVALID_STOPS:
            str_.v = 'invalid stops'
        elif _sw21 == TRADE_RETCODE_TRADE_DISABLED:
            str_.v = 'trade disabled'
        elif _sw21 == TRADE_RETCODE_MARKET_CLOSED:
            str_.v = 'market closed'
        elif _sw21 == TRADE_RETCODE_NO_MONEY:
            str_.v = 'not enough money'
        elif _sw21 == TRADE_RETCODE_PRICE_CHANGED:
            str_.v = 'price changed'
        elif _sw21 == TRADE_RETCODE_PRICE_OFF:
            str_.v = 'off quotes'
        elif _sw21 == TRADE_RETCODE_INVALID_EXPIRATION:
            str_.v = 'invalid expiration'
        elif _sw21 == TRADE_RETCODE_ORDER_CHANGED:
            str_.v = 'order changed'
        elif _sw21 == TRADE_RETCODE_TOO_MANY_REQUESTS:
            str_.v = 'too many requests'
        elif _sw21 == TRADE_RETCODE_NO_CHANGES:
            str_.v = 'no changes'
        elif _sw21 == TRADE_RETCODE_SERVER_DISABLES_AT:
            str_.v = 'auto trading disabled by server'
        elif _sw21 == TRADE_RETCODE_CLIENT_DISABLES_AT:
            str_.v = 'auto trading disabled by client'
        elif _sw21 == TRADE_RETCODE_LOCKED:
            str_.v = 'locked'
        elif _sw21 == TRADE_RETCODE_FROZEN:
            str_.v = 'frozen'
        elif _sw21 == TRADE_RETCODE_INVALID_FILL:
            str_.v = 'invalid fill'
        elif _sw21 == TRADE_RETCODE_CONNECTION:
            str_.v = 'no connection'
        elif _sw21 == TRADE_RETCODE_ONLY_REAL:
            str_.v = 'only real'
        elif _sw21 == TRADE_RETCODE_LIMIT_ORDERS:
            str_.v = 'limit orders'
        elif _sw21 == TRADE_RETCODE_LIMIT_VOLUME:
            str_.v = 'limit volume'
        elif _sw21 == TRADE_RETCODE_POSITION_CLOSED:
            str_.v = 'position closed'
        elif _sw21 == TRADE_RETCODE_INVALID_ORDER:
            str_.v = 'invalid order'
        elif _sw21 == TRADE_RETCODE_CLOSE_ORDER_EXIST:
            str_.v = 'close order already exists'
        elif _sw21 == TRADE_RETCODE_LIMIT_POSITIONS:
            str_.v = 'limit positions'
        else:
            str_.v = 'unknown retcode ' + _str(result.retcode)
        return str_.v
    def FillingCheck(self, symbol):
        exec = SymbolInfoInteger(symbol, SYMBOL_TRADE_EXEMODE)
        if exec == SYMBOL_TRADE_EXECUTION_REQUEST or exec == SYMBOL_TRADE_EXECUTION_INSTANT:
            return True
        filling = _uint(SymbolInfoInteger(symbol, SYMBOL_FILLING_MODE))
        if exec == SYMBOL_TRADE_EXECUTION_MARKET:
            if self.m_request.action != TRADE_ACTION_PENDING:
                if (filling & SYMBOL_FILLING_FOK) == SYMBOL_FILLING_FOK:
                    self.m_type_filling = ORDER_FILLING_FOK
                    self.m_request.type_filling = self.m_type_filling
                    return True
                if (filling & SYMBOL_FILLING_IOC) == SYMBOL_FILLING_IOC:
                    self.m_type_filling = ORDER_FILLING_IOC
                    self.m_request.type_filling = self.m_type_filling
                    return True
                self.m_result.retcode = TRADE_RETCODE_INVALID_FILL
                return False
            return True
        _sw22 = self.m_type_filling
        if _sw22 == ORDER_FILLING_FOK:
            if self.m_request.action == TRADE_ACTION_PENDING:
                if not self.ExpirationCheck(symbol):
                    self.m_request.type_time = ORDER_TIME_DAY
                if ((self.m_request.type == ORDER_TYPE_BUY_STOP or self.m_request.type == ORDER_TYPE_SELL_STOP) or self.m_request.type == ORDER_TYPE_BUY_LIMIT) or self.m_request.type == ORDER_TYPE_SELL_LIMIT:
                    self.m_request.type_filling = ORDER_FILLING_RETURN
                    return True
            if (filling & SYMBOL_FILLING_FOK) == SYMBOL_FILLING_FOK:
                self.m_request.type_filling = self.m_type_filling
                return True
            self.m_result.retcode = TRADE_RETCODE_INVALID_FILL
            return False
        elif _sw22 == ORDER_FILLING_IOC:
            if self.m_request.action == TRADE_ACTION_PENDING:
                if not self.ExpirationCheck(symbol):
                    self.m_request.type_time = ORDER_TIME_DAY
                if ((self.m_request.type == ORDER_TYPE_BUY_STOP or self.m_request.type == ORDER_TYPE_SELL_STOP) or self.m_request.type == ORDER_TYPE_BUY_LIMIT) or self.m_request.type == ORDER_TYPE_SELL_LIMIT:
                    self.m_request.type_filling = ORDER_FILLING_RETURN
                    return True
            if (filling & SYMBOL_FILLING_IOC) == SYMBOL_FILLING_IOC:
                self.m_request.type_filling = self.m_type_filling
                return True
            self.m_result.retcode = TRADE_RETCODE_INVALID_FILL
            return False
        elif _sw22 == ORDER_FILLING_RETURN:
            self.m_request.type_filling = self.m_type_filling
            return True
        self.m_result.retcode = TRADE_RETCODE_ERROR
        return False
    def ExpirationCheck(self, symbol):
        symbol_name = (Symbol() if (symbol == "") else symbol)
        tmp_long = Box(0)
        flags = 0
        if SymbolInfoInteger(symbol_name, SYMBOL_EXPIRATION_MODE, tmp_long):
            flags = _int(tmp_long.v)
        _sw23 = self.m_request.type_time
        if _sw23 == ORDER_TIME_GTC:
            if (flags & SYMBOL_EXPIRATION_GTC) != 0:
                return True
        elif _sw23 == ORDER_TIME_DAY:
            if (flags & SYMBOL_EXPIRATION_DAY) != 0:
                return True
        elif _sw23 == ORDER_TIME_SPECIFIED:
            if (flags & SYMBOL_EXPIRATION_SPECIFIED) != 0:
                return True
        elif _sw23 == ORDER_TIME_SPECIFIED_DAY:
            if (flags & SYMBOL_EXPIRATION_SPECIFIED_DAY) != 0:
                return True
        else:
            Print('CTrade::ExpirationCheck' + ': Unknown expiration type')
        return False
    def OrderTypeCheck(self, symbol):
        res = False
        symbol_name = (Symbol() if (symbol == "") else symbol)
        tmp_long = Box(0)
        flags = 0
        if SymbolInfoInteger(symbol_name, SYMBOL_ORDER_MODE, tmp_long):
            flags = _int(tmp_long.v)
        _sw24 = self.m_request.type
        if _sw24 in (ORDER_TYPE_BUY, ORDER_TYPE_SELL):
            res = (flags & SYMBOL_ORDER_MARKET) != 0
        elif _sw24 in (ORDER_TYPE_BUY_LIMIT, ORDER_TYPE_SELL_LIMIT):
            res = (flags & SYMBOL_ORDER_LIMIT) != 0
        elif _sw24 in (ORDER_TYPE_BUY_STOP, ORDER_TYPE_SELL_STOP):
            res = (flags & SYMBOL_ORDER_STOP) != 0
        elif _sw24 in (ORDER_TYPE_BUY_STOP_LIMIT, ORDER_TYPE_SELL_STOP_LIMIT):
            res = (flags & SYMBOL_ORDER_STOP_LIMIT) != 0
        if res:
            if self.m_request.sl != 0.0 or self.m_request.tp != 0.0:
                if (flags & SYMBOL_ORDER_SL) == 0:
                    self.m_request.sl = 0.0
                if (flags & SYMBOL_ORDER_TP) == 0:
                    self.m_request.tp = 0.0
        else:
            self.m_result.retcode = TRADE_RETCODE_INVALID_ORDER
            Print('CTrade::OrderTypeCheck' + ': Invalid order type')
        return res
    def ClearStructures(self):
        ZeroMemory(self.m_request)
        ZeroMemory(self.m_result)
        ZeroMemory(self.m_check_result)
    def IsStopped(self, function):
        if not False:
            return False
        PrintFormat('%s: MQL5 program is stopped. Trading is disabled', function)
        self.m_result.retcode = TRADE_RETCODE_CLIENT_DISABLES_AT
        return True
    def IsHedging(self):
        return self.m_margin_mode == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING
    def SelectPosition(self, symbol):
        res = False
        if self.IsHedging():
            total = PositionsTotal()
            for i in range(0, total):
                position_symbol = _str(PositionGetSymbol(i))
                if position_symbol == symbol and self.m_magic == PositionGetInteger(POSITION_MAGIC):
                    res = True
                    break
        else:
            res = PositionSelect(symbol)
        return res

def OnInit():
    ResetLastError()
    namefile = Box("")
    StringConcatenate(namefile, Symbol(), '_Sampler.BIN')
    filehandle = FileOpen(namefile.v, (FILE_READ | FILE_BIN) | FILE_COMMON)
    if filehandle != INVALID_HANDLE:
        FileReadArray(filehandle, signal, 0, WHOLE_ARRAY)
        FileClose(filehandle)
        Print(namefile.v, ' FileOpen OK')
    else:
        Print(namefile.v, '  FileOpen failed, error ', GetLastError())
    ArraySort(signal)
    return 0

def OnTick():
    global prevtime
    CopyTime(Symbol(), Period(), 0, 1, time)
    if time[0] == prevtime:
        return
    prevtime = time[0]
    sig = 0
    index = 0
    index = ArrayBsearch(signal, time[0])
    if signal[index] == time[0]:
        sig = 1
    index = ArrayBsearch(signal, -time[0])
    if signal[index] == (-time[0]):
        sig = -1
    SymbolInfoTick(Symbol(), tick)
    if sig == 1:
        if PositionSelect(Symbol()) and PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL:
            trade.PositionClose_1(Symbol())
        trade.Buy(lot, "", tick.ask)
    if sig == -1:
        if PositionSelect(Symbol()) and PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY:
            trade.PositionClose_1(Symbol())
        trade.Sell(lot, "", tick.bid)

# ---- global variables initialised from expressions
trade = _alloc(CTrade)
trade.__init__()
tick = MqlTick()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EChecksampler(_MQL5Indicator):
    name = 'e_checksampler'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'lot': 1.0,
    }

