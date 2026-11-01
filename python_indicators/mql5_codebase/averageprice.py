"""AveragePrice — converted from MQL5: MQL5 Indicators/AveragePrice/AveragePrice.mq5

Copyright: © 2025 Francisco Gomes. (mql5.com); Link: https://www.mql5.com/en/users/franciscogomes5/seller; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': '© 2025 Francisco Gomes. (mql5.com)', 'link': 'https://www.mql5.com/en/users/franciscogomes5/seller', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 0, 2: 1, 3: 1, 4: 1}, 'colors': {2: [16711680], 3: [255], 4: [16776960]}, 'widths': {2: 4, 3: 4, 4: 5}, 'styles': {4: 1}, 'labels': {1: 'Volume Balance', 2: 'Average Buy', 3: 'Average Sell', 4: 'Average Price'}, 'levels': [], 'description': [], 'name': 'AveragePrice', 'source': 'MQL5 Indicators/AveragePrice/AveragePrice.mq5', 'folder': 'AveragePrice', 'inputs': [{'mql': 'MagicNumber', 'py': 'MagicNumber', 'param': 'MagicNumber', 'type': 'long', 'default': 0, 'label': 'Magic', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

POSITION_TIME_UPDATE_MSC = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
bufferBuyAvgPrice = Arr(0, 0.0)
bufferSellAvgPrice = Arr(0, 0.0)
bufferAvgPrice = Arr(0, 0.0)
bufferNetVolume = Arr(0, 0.0)
MagicNumber = _input('MagicNumber', 0)  # Magic

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

def CalculateHedgeAveragePrice(symbol, magic, netVolume, buyAvgPrice, sellAvgPrice):
    pos = CPositionInfo()
    totalBuyVolume = 0.0
    totalBuyCost = 0.0
    totalSellVolume = 0.0
    totalSellCost = 0.0
    for i in range(PositionsTotal() - 1, 0 - 1, -1):
        if not pos.SelectByIndex(i):
            continue
        if magic != 0 and pos.Magic() != magic:
            continue
        if pos.Symbol() != symbol:
            continue
        volume = pos.Volume()
        price = pos.PriceOpen()
        if pos.PositionType() == POSITION_TYPE_BUY:
            totalBuyVolume += volume
            totalBuyCost += price * volume
        elif pos.PositionType() == POSITION_TYPE_SELL:
            totalSellVolume += volume
            totalSellCost += price * volume
    buyAvgPrice.v = (_fdiv(totalBuyCost, totalBuyVolume) if (totalBuyVolume > 0) else 0)
    sellAvgPrice.v = (_fdiv(totalSellCost, totalSellVolume) if (totalSellVolume > 0) else 0)
    netVolume.v = totalBuyVolume - totalSellVolume
    if netVolume.v > 0:
        return buyAvgPrice.v
    if netVolume.v < 0:
        return sellAvgPrice.v
    return 0.0

def OnInit():
    SetIndexBuffer(0, bufferNetVolume)
    SetIndexBuffer(1, bufferBuyAvgPrice)
    SetIndexBuffer(2, bufferSellAvgPrice)
    SetIndexBuffer(3, bufferAvgPrice)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AveragePrice')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    netVolume = Box(0.0)
    buyAvgPrice = Box(0.0)
    sellAvgPrice = Box(0.0)
    avgPrice = CalculateHedgeAveragePrice(Symbol(), MagicNumber, netVolume, buyAvgPrice, sellAvgPrice)
    ArrayFill(bufferBuyAvgPrice, 0, rates_total, buyAvgPrice.v)
    ArrayFill(bufferSellAvgPrice, 0, rates_total, sellAvgPrice.v)
    ArrayFill(bufferAvgPrice, 0, rates_total, avgPrice)
    ArrayFill(bufferNetVolume, 0, rates_total, netVolume.v)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AveragePrice(_MQL5Indicator):
    name = 'AveragePrice'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MagicNumber': 0,  # Magic
    }

