"""AccountInfo.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh


class CAccountInfo(CObject):
    _q_fields = ()
    def __init__(self):
        CObject.__init__(self)
    def _q_dtor(self):
        pass
    def Login(self):
        return AccountInfoInteger(ACCOUNT_LOGIN)
    def TradeMode(self):
        return AccountInfoInteger(ACCOUNT_TRADE_MODE)
    def TradeModeDescription(self):
        str_ = ""
        _sw1 = self.TradeMode()
        if _sw1 == ACCOUNT_TRADE_MODE_DEMO:
            str_ = 'Demo trading account'
        elif _sw1 == ACCOUNT_TRADE_MODE_CONTEST:
            str_ = 'Contest trading account'
        elif _sw1 == ACCOUNT_TRADE_MODE_REAL:
            str_ = 'Real trading account'
        else:
            str_ = 'Unknown trade account'
        return str_
    def Leverage(self):
        return AccountInfoInteger(ACCOUNT_LEVERAGE)
    def StopoutMode(self):
        return AccountInfoInteger(ACCOUNT_MARGIN_SO_MODE)
    def StopoutModeDescription(self):
        str_ = ""
        _sw2 = self.StopoutMode()
        if _sw2 == ACCOUNT_STOPOUT_MODE_PERCENT:
            str_ = 'Level is specified in percentage'
        elif _sw2 == ACCOUNT_STOPOUT_MODE_MONEY:
            str_ = 'Level is specified in money'
        else:
            str_ = 'Unknown stopout mode'
        return str_
    def MarginMode(self):
        return AccountInfoInteger(ACCOUNT_MARGIN_MODE)
    def MarginModeDescription(self):
        str_ = ""
        _sw3 = self.MarginMode()
        if _sw3 == ACCOUNT_MARGIN_MODE_RETAIL_NETTING:
            str_ = 'Netting'
        elif _sw3 == ACCOUNT_MARGIN_MODE_EXCHANGE:
            str_ = 'Exchange'
        elif _sw3 == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING:
            str_ = 'Hedging'
        else:
            str_ = 'Unknown margin mode'
        return str_
    def TradeAllowed(self):
        return _bool(AccountInfoInteger(ACCOUNT_TRADE_ALLOWED))
    def TradeExpert(self):
        return _bool(AccountInfoInteger(ACCOUNT_TRADE_EXPERT))
    def LimitOrders(self):
        return _int(AccountInfoInteger(ACCOUNT_LIMIT_ORDERS))
    def Balance(self):
        return AccountInfoDouble(ACCOUNT_BALANCE)
    def Credit(self):
        return AccountInfoDouble(ACCOUNT_CREDIT)
    def Profit(self):
        return AccountInfoDouble(ACCOUNT_PROFIT)
    def Equity(self):
        return AccountInfoDouble(ACCOUNT_EQUITY)
    def Margin(self):
        return AccountInfoDouble(ACCOUNT_MARGIN)
    def FreeMargin(self):
        return AccountInfoDouble(ACCOUNT_MARGIN_FREE)
    def MarginLevel(self):
        return AccountInfoDouble(ACCOUNT_MARGIN_LEVEL)
    def MarginCall(self):
        return AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL)
    def MarginStopOut(self):
        return AccountInfoDouble(ACCOUNT_MARGIN_SO_SO)
    def Name(self):
        return AccountInfoString(ACCOUNT_NAME)
    def Server(self):
        return AccountInfoString(ACCOUNT_SERVER)
    def Currency(self):
        return AccountInfoString(ACCOUNT_CURRENCY)
    def Company(self):
        return AccountInfoString(ACCOUNT_COMPANY)
    def InfoInteger(self, prop_id):
        return AccountInfoInteger(prop_id)
    def InfoDouble(self, prop_id):
        return AccountInfoDouble(prop_id)
    def InfoString(self, prop_id):
        return AccountInfoString(prop_id)
    def OrderProfitCheck(self, symbol, trade_operation, volume, price_open, price_close):
        profit = EMPTY_VALUE
        if not OrderCalcProfit(trade_operation, symbol, volume, price_open, price_close, profit):
            return EMPTY_VALUE
        return profit
    def MarginCheck(self, symbol, trade_operation, volume, price):
        margin = EMPTY_VALUE
        if not OrderCalcMargin(trade_operation, symbol, volume, price, margin):
            return EMPTY_VALUE
        return margin
    def FreeMarginCheck(self, symbol, trade_operation, volume, price):
        return self.FreeMargin() - self.MarginCheck(symbol, trade_operation, volume, price)
    def MaxLotCheck(self, symbol, trade_operation, price, percent=100.0):
        margin = 0.0
        if ((symbol == '' or price <= 0.0) or percent < 1) or percent > 100:
            Print('CAccountInfo::MaxLotCheck invalid parameters')
            return 0.0
        if (not OrderCalcMargin(trade_operation, symbol, 1.0, price, margin)) or margin < 0.0:
            Print('CAccountInfo::MaxLotCheck margin calculation failed')
            return 0.0
        if margin == 0.0:
            return SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX)
        volume = NormalizeDouble(_fdiv((self.FreeMargin() * percent) / 100.0, margin), 2)
        stepvol = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP)
        if stepvol > 0.0:
            volume = stepvol * MathFloor(_fdiv(volume, stepvol))
        minvol = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN)
        if volume < minvol:
            volume = 0.0
        maxvol = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX)
        if volume > maxvol:
            volume = maxvol
        return volume

__all__ = ['CAccountInfo']
