"""showimportantparams — converted from MQL5: MQL5 Indicators/ShowImportantParams/showimportantparams.mq5

Indicator shows important params for current symbol and account
Copyright: Copyright 2016 June 30, Alexey Volchanskiy; Link: https://mql.gnomio.com/; Version: 1.03

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Functions not available here: SymbolInfoMarginRate
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh
from backtester.mql5.lib.trade_accountinfo import *  # #include AccountInfo.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2016 June 30, Alexey Volchanskiy', 'link': 'https://mql.gnomio.com/', 'version': '1.03', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Indicator shows important params for current symbol and account'], 'name': 'showimportantparams', 'source': 'MQL5 Indicators/ShowImportantParams/showimportantparams.mq5', 'folder': 'ShowImportantParams', 'inputs': [{'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'FontColor', 'py': 'FontColor', 'param': None, 'type': 'color', 'default': 65535, 'label': '', 'sinput': False}, {'mql': 'FontName', 'py': 'FontName', 'param': None, 'type': 'string', 'default': 'Tahoma', 'label': '', 'sinput': False}, {'mql': 'XOffset', 'py': 'XOffset', 'param': 'XOffset', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'YOffset', 'py': 'YOffset', 'param': 'YOffset', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'SpreadSmoothTicks', 'py': 'SpreadSmoothTicks', 'param': 'SpreadSmoothTicks', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh', 'AccountInfo.mqh']}

SYMBOL_EXPIRATION_TIME = 0  # MQL5 constant unknown to the converter
SYMBOL_MARGIN_HEDGED = 0  # MQL5 constant unknown to the converter
SYMBOL_MARGIN_HEDGED_USE_LEG = 0  # MQL5 constant unknown to the converter
SYMBOL_MARGIN_MAINTENANCE = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_AW = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_BUY_ORDERS = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_BUY_ORDERS_VOLUME = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_CLOSE = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_DEALS = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_INTEREST = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_OPEN = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_PRICE_LIMIT_MAX = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_PRICE_LIMIT_MIN = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_PRICE_SETTLEMENT = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_SELL_ORDERS = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_SELL_ORDERS_VOLUME = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_TURNOVER = 0  # MQL5 constant unknown to the converter
SYMBOL_START_TIME = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_MODE = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_MODE_CURRENCY_DEPOSIT = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_MODE_CURRENCY_MARGIN = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_MODE_CURRENCY_SYMBOL = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_MODE_INTEREST_CURRENT = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_MODE_INTEREST_OPEN = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_MODE_REOPEN_BID = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_MODE_REOPEN_CURRENT = 0  # MQL5 constant unknown to the converter
SYMBOL_SWAP_ROLLOVER3DAYS = 0  # MQL5 constant unknown to the converter
SYMBOL_TICKS_BOOKDEPTH = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_EXECUTION_EXCHANGE = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_EXECUTION_INSTANT = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_EXECUTION_MARKET = 0  # MQL5 constant unknown to the converter
SYMBOL_TRADE_EXECUTION_REQUEST = 0  # MQL5 constant unknown to the converter
SYMBOL_VOLUME_LIMIT = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
FontSize = _input('FontSize', 10)
FontColor = _input('FontColor', clrYellow)
FontName = _input('FontName', 'Tahoma')
XOffset = _input('XOffset', 10)
YOffset = _input('YOffset', 15)
SpreadSmoothTicks = _input('SpreadSmoothTicks', 20)
lNames = Arr.of(['PointPrice=', 'Leverage=1:', 'SpreadSmooth=', 'SpreadPrice=', 'StopLevel=', 'MarginCall=', 'StopOut='], fill="")  # "Margin4lot",
SpreadBuf = Arr(0, 0.0)
SpreadBufIdx = 0

class CSymbolInfo(CObject):
    _q_fields = ('m_name', 'm_tick', 'm_point', 'm_tick_value', 'm_tick_value_profit', 'm_tick_value_loss', 'm_tick_size', 'm_contract_size', 'm_lots_min', 'm_lots_max', 'm_lots_step', 'm_lots_limit', 'm_swap_long', 'm_swap_short', 'm_digits', 'm_order_mode', 'm_trade_execution', 'm_trade_calcmode', 'm_trade_mode', 'm_swap_mode', 'm_swap3', 'm_margin_initial', 'm_margin_maintenance', 'm_margin_hedged_use_leg', 'm_margin_hedged', 'm_trade_time_flags', 'm_trade_fill_flags')
    def __init__(self):
        CObject.__init__(self)
        self.m_name = ""
        self.m_tick = MqlTick()
        self.m_point = 0.0
        self.m_tick_value = 0.0
        self.m_tick_value_profit = 0.0
        self.m_tick_value_loss = 0.0
        self.m_tick_size = 0.0
        self.m_contract_size = 0.0
        self.m_lots_min = 0.0
        self.m_lots_max = 0.0
        self.m_lots_step = 0.0
        self.m_lots_limit = 0.0
        self.m_swap_long = 0.0
        self.m_swap_short = 0.0
        self.m_digits = 0
        self.m_order_mode = 0
        self.m_trade_execution = 0
        self.m_trade_calcmode = 0
        self.m_trade_mode = 0
        self.m_swap_mode = 0
        self.m_swap3 = 0
        self.m_margin_initial = 0.0
        self.m_margin_maintenance = 0.0
        self.m_margin_hedged_use_leg = False
        self.m_margin_hedged = 0.0
        self.m_trade_time_flags = 0
        self.m_trade_fill_flags = 0
        self.m_name = ""
        self.m_point = 0.0
        self.m_tick_value = 0.0
        self.m_tick_value_profit = 0.0
        self.m_tick_value_loss = 0.0
        self.m_tick_size = 0.0
        self.m_contract_size = 0.0
        self.m_lots_min = 0.0
        self.m_lots_max = 0.0
        self.m_lots_step = 0.0
        self.m_swap_long = 0.0
        self.m_swap_short = 0.0
        self.m_digits = 0
        self.m_order_mode = 0
        self.m_trade_execution = 0
        self.m_trade_calcmode = 0
        self.m_trade_mode = 0
        self.m_swap_mode = 0
        self.m_swap3 = 0
        self.m_margin_initial = 0.0
        self.m_margin_maintenance = 0.0
        self.m_margin_hedged_use_leg = False
        self.m_margin_hedged = 0.0
        self.m_trade_time_flags = 0
        self.m_trade_fill_flags = 0
    def _q_dtor(self):
        pass
    def Name_0(self):
        return self.m_name
    def Name_1(self, name):
        symbol_name = (name if (StringLen(name) > 0) else Symbol())
        if self.m_name != symbol_name:
            self.m_name = symbol_name
            if not self.CheckMarketWatch():
                return False
            if not self.Refresh():
                self.m_name = ''
                Print('CSymbolInfo::Name' + ": invalid data of symbol '" + symbol_name + "'")
                return False
        return True
    def Refresh(self):
        tmp_long = Box(0)
        if not SymbolInfoDouble(self.m_name, SYMBOL_POINT, _AttrRef(self, 'm_point')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_TRADE_TICK_VALUE, _AttrRef(self, 'm_tick_value')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_TRADE_TICK_VALUE_PROFIT, _AttrRef(self, 'm_tick_value_profit')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_TRADE_TICK_VALUE_LOSS, _AttrRef(self, 'm_tick_value_loss')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_TRADE_TICK_SIZE, _AttrRef(self, 'm_tick_size')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_TRADE_CONTRACT_SIZE, _AttrRef(self, 'm_contract_size')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_VOLUME_MIN, _AttrRef(self, 'm_lots_min')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_VOLUME_MAX, _AttrRef(self, 'm_lots_max')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_VOLUME_STEP, _AttrRef(self, 'm_lots_step')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_VOLUME_LIMIT, _AttrRef(self, 'm_lots_limit')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_SWAP_LONG, _AttrRef(self, 'm_swap_long')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_SWAP_SHORT, _AttrRef(self, 'm_swap_short')):
            return False
        if not SymbolInfoInteger(self.m_name, SYMBOL_DIGITS, tmp_long):
            return False
        self.m_digits = _int(tmp_long.v)
        if not SymbolInfoInteger(self.m_name, SYMBOL_ORDER_MODE, tmp_long):
            return False
        self.m_order_mode = _int(tmp_long.v)
        if not SymbolInfoInteger(self.m_name, SYMBOL_TRADE_EXEMODE, tmp_long):
            return False
        self.m_trade_execution = tmp_long.v
        if not SymbolInfoInteger(self.m_name, SYMBOL_TRADE_CALC_MODE, tmp_long):
            return False
        self.m_trade_calcmode = tmp_long.v
        if not SymbolInfoInteger(self.m_name, SYMBOL_TRADE_MODE, tmp_long):
            return False
        self.m_trade_mode = tmp_long.v
        if not SymbolInfoInteger(self.m_name, SYMBOL_SWAP_MODE, tmp_long):
            return False
        self.m_swap_mode = tmp_long.v
        if not SymbolInfoInteger(self.m_name, SYMBOL_SWAP_ROLLOVER3DAYS, tmp_long):
            return False
        self.m_swap3 = tmp_long.v
        if not SymbolInfoDouble(self.m_name, SYMBOL_MARGIN_INITIAL, _AttrRef(self, 'm_margin_initial')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_MARGIN_MAINTENANCE, _AttrRef(self, 'm_margin_maintenance')):
            return False
        if not SymbolInfoDouble(self.m_name, SYMBOL_MARGIN_HEDGED, _AttrRef(self, 'm_margin_hedged')):
            return False
        if not SymbolInfoInteger(self.m_name, SYMBOL_MARGIN_HEDGED_USE_LEG, tmp_long):
            return False
        self.m_margin_hedged_use_leg = _bool(tmp_long.v)
        if not SymbolInfoInteger(self.m_name, SYMBOL_EXPIRATION_MODE, tmp_long):
            return False
        self.m_trade_time_flags = _int(tmp_long.v)
        if not SymbolInfoInteger(self.m_name, SYMBOL_FILLING_MODE, tmp_long):
            return False
        self.m_trade_fill_flags = _int(tmp_long.v)
        return True
    def RefreshRates(self):
        return SymbolInfoTick(self.m_name, self.m_tick)
    def Select_0(self):
        return _bool(SymbolInfoInteger(self.m_name, SYMBOL_SELECT))
    def Select_1(self, select):
        return SymbolSelect(self.m_name, select)
    def IsSynchronized(self):
        return SymbolIsSynchronized(self.m_name)
    def Volume(self):
        return self.m_tick.volume
    def VolumeHigh(self):
        return SymbolInfoInteger(self.m_name, SYMBOL_VOLUMEHIGH)
    def VolumeLow(self):
        return SymbolInfoInteger(self.m_name, SYMBOL_VOLUMELOW)
    def Time(self):
        return self.m_tick.time
    def Spread(self):
        return _int(SymbolInfoInteger(self.m_name, SYMBOL_SPREAD))
    def SpreadFloat(self):
        return _bool(SymbolInfoInteger(self.m_name, SYMBOL_SPREAD_FLOAT))
    def TicksBookDepth(self):
        return _int(SymbolInfoInteger(self.m_name, SYMBOL_TICKS_BOOKDEPTH))
    def StopsLevel(self):
        return _int(SymbolInfoInteger(self.m_name, SYMBOL_TRADE_STOPS_LEVEL))
    def FreezeLevel(self):
        return _int(SymbolInfoInteger(self.m_name, SYMBOL_TRADE_FREEZE_LEVEL))
    def Bid(self):
        return self.m_tick.bid
    def BidHigh(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_BIDHIGH)
    def BidLow(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_BIDLOW)
    def Ask(self):
        return self.m_tick.ask
    def AskHigh(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_ASKHIGH)
    def AskLow(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_ASKLOW)
    def Last(self):
        return self.m_tick.last
    def LastHigh(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_LASTHIGH)
    def LastLow(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_LASTLOW)
    def OrderMode(self):
        return self.m_order_mode
    def TradeCalcMode(self):
        return self.m_trade_calcmode
    def TradeCalcModeDescription(self):
        str_ = ""
        _sw1 = self.m_trade_calcmode
        if _sw1 == SYMBOL_CALC_MODE_FOREX:
            str_ = 'Calculation of profit and margin for Forex'
        elif _sw1 == SYMBOL_CALC_MODE_CFD:
            str_ = 'Calculation of collateral and earnings for CFD'
        elif _sw1 == SYMBOL_CALC_MODE_FUTURES:
            str_ = 'Calculation of collateral and profits for futures'
        elif _sw1 == SYMBOL_CALC_MODE_CFDINDEX:
            str_ = 'Calculation of collateral and earnings for CFD on indices'
        elif _sw1 == SYMBOL_CALC_MODE_CFDLEVERAGE:
            str_ = 'Calculation of collateral and earnings for the CFD when trading with leverage'
        elif _sw1 == SYMBOL_CALC_MODE_EXCH_STOCKS:
            str_ = 'Calculation for exchange stocks'
        elif _sw1 == SYMBOL_CALC_MODE_EXCH_FUTURES:
            str_ = 'Calculation for exchange futures'
        elif _sw1 == SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS:
            str_ = 'Calculation for FORTS futures'
        else:
            str_ = 'Unknown calculation mode'
        return str_
    def TradeMode(self):
        return self.m_trade_mode
    def TradeModeDescription(self):
        str_ = ""
        _sw2 = self.m_trade_mode
        if _sw2 == SYMBOL_TRADE_MODE_DISABLED:
            str_ = 'Disabled'
        elif _sw2 == SYMBOL_TRADE_MODE_LONGONLY:
            str_ = 'Long only'
        elif _sw2 == SYMBOL_TRADE_MODE_SHORTONLY:
            str_ = 'Short only'
        elif _sw2 == SYMBOL_TRADE_MODE_CLOSEONLY:
            str_ = 'Close only'
        elif _sw2 == SYMBOL_TRADE_MODE_FULL:
            str_ = 'Full access'
        else:
            str_ = 'Unknown trade mode'
        return str_
    def TradeExecution(self):
        return self.m_trade_execution
    def TradeExecutionDescription(self):
        str_ = ""
        _sw3 = self.m_trade_execution
        if _sw3 == SYMBOL_TRADE_EXECUTION_REQUEST:
            str_ = 'Trading on request'
        elif _sw3 == SYMBOL_TRADE_EXECUTION_INSTANT:
            str_ = 'Trading on live streaming prices'
        elif _sw3 == SYMBOL_TRADE_EXECUTION_MARKET:
            str_ = 'Execution of orders on the market'
        elif _sw3 == SYMBOL_TRADE_EXECUTION_EXCHANGE:
            str_ = 'Exchange execution'
        else:
            str_ = 'Unknown trade execution'
        return str_
    def SwapMode(self):
        return self.m_swap_mode
    def SwapModeDescription(self):
        str_ = ""
        _sw4 = self.m_swap_mode
        if _sw4 == SYMBOL_SWAP_MODE_DISABLED:
            str_ = 'No swaps'
        elif _sw4 == SYMBOL_SWAP_MODE_POINTS:
            str_ = 'Swaps are calculated in points'
        elif _sw4 == SYMBOL_SWAP_MODE_CURRENCY_SYMBOL:
            str_ = 'Swaps are calculated in base currency'
        elif _sw4 == SYMBOL_SWAP_MODE_CURRENCY_MARGIN:
            str_ = 'Swaps are calculated in margin currency'
        elif _sw4 == SYMBOL_SWAP_MODE_CURRENCY_DEPOSIT:
            str_ = 'Swaps are calculated in deposit currency'
        elif _sw4 == SYMBOL_SWAP_MODE_INTEREST_CURRENT:
            str_ = 'Swaps are calculated as annual interest using the current price'
        elif _sw4 == SYMBOL_SWAP_MODE_INTEREST_OPEN:
            str_ = 'Swaps are calculated as annual interest using the open price'
        elif _sw4 == SYMBOL_SWAP_MODE_REOPEN_CURRENT:
            str_ = 'Swaps are charged by reopening positions at the close price'
        elif _sw4 == SYMBOL_SWAP_MODE_REOPEN_BID:
            str_ = 'Swaps are charged by reopening positions at the Bid price'
        else:
            str_ = 'Unknown swap mode'
        return str_
    def SwapRollover3days(self):
        return self.m_swap3
    def SwapRollover3daysDescription(self):
        str_ = ""
        _sw5 = self.m_swap3
        if _sw5 == SUNDAY:
            str_ = 'Sunday'
        elif _sw5 == MONDAY:
            str_ = 'Monday'
        elif _sw5 == TUESDAY:
            str_ = 'Tuesday'
        elif _sw5 == WEDNESDAY:
            str_ = 'Wednesday'
        elif _sw5 == THURSDAY:
            str_ = 'Thursday'
        elif _sw5 == FRIDAY:
            str_ = 'Friday'
        elif _sw5 == SATURDAY:
            str_ = 'Saturday'
        else:
            str_ = 'Unknown'
        return str_
    def StartTime(self):
        return SymbolInfoInteger(self.m_name, SYMBOL_START_TIME)
    def ExpirationTime(self):
        return SymbolInfoInteger(self.m_name, SYMBOL_EXPIRATION_TIME)
    def MarginInitial(self):
        return self.m_margin_initial
    def MarginMaintenance(self):
        return self.m_margin_maintenance
    def MarginHedgedUseLeg(self):
        return self.m_margin_hedged_use_leg
    def MarginHedged(self):
        return self.m_margin_hedged
    def MarginLong(self):
        return 0.0
    def MarginShort(self):
        return 0.0
    def MarginLimit(self):
        return 0.0
    def MarginStop(self):
        return 0.0
    def MarginStopLimit(self):
        return 0.0
    def TradeTimeFlags(self):
        return self.m_trade_time_flags
    def TradeFillFlags(self):
        return self.m_trade_fill_flags
    def Digits(self):
        return self.m_digits
    def Point(self):
        return self.m_point
    def TickValue(self):
        return self.m_tick_value
    def TickValueProfit(self):
        return self.m_tick_value_profit
    def TickValueLoss(self):
        return self.m_tick_value_loss
    def TickSize(self):
        return self.m_tick_size
    def ContractSize(self):
        return self.m_contract_size
    def LotsMin(self):
        return self.m_lots_min
    def LotsMax(self):
        return self.m_lots_max
    def LotsStep(self):
        return self.m_lots_step
    def LotsLimit(self):
        return self.m_lots_limit
    def SwapLong(self):
        return self.m_swap_long
    def SwapShort(self):
        return self.m_swap_short
    def CurrencyBase(self):
        return SymbolInfoString(self.m_name, SYMBOL_CURRENCY_BASE)
    def CurrencyProfit(self):
        return SymbolInfoString(self.m_name, SYMBOL_CURRENCY_PROFIT)
    def CurrencyMargin(self):
        return SymbolInfoString(self.m_name, SYMBOL_CURRENCY_MARGIN)
    def Bank(self):
        return SymbolInfoString(self.m_name, SYMBOL_BANK)
    def Description(self):
        return SymbolInfoString(self.m_name, SYMBOL_DESCRIPTION)
    def Path(self):
        return SymbolInfoString(self.m_name, SYMBOL_PATH)
    def SessionDeals(self):
        return SymbolInfoInteger(self.m_name, SYMBOL_SESSION_DEALS)
    def SessionBuyOrders(self):
        return SymbolInfoInteger(self.m_name, SYMBOL_SESSION_BUY_ORDERS)
    def SessionSellOrders(self):
        return SymbolInfoInteger(self.m_name, SYMBOL_SESSION_SELL_ORDERS)
    def SessionTurnover(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_SESSION_TURNOVER)
    def SessionInterest(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_SESSION_INTEREST)
    def SessionBuyOrdersVolume(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_SESSION_BUY_ORDERS_VOLUME)
    def SessionSellOrdersVolume(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_SESSION_SELL_ORDERS_VOLUME)
    def SessionOpen(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_SESSION_OPEN)
    def SessionClose(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_SESSION_CLOSE)
    def SessionAW(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_SESSION_AW)
    def SessionPriceSettlement(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_SESSION_PRICE_SETTLEMENT)
    def SessionPriceLimitMin(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_SESSION_PRICE_LIMIT_MIN)
    def SessionPriceLimitMax(self):
        return SymbolInfoDouble(self.m_name, SYMBOL_SESSION_PRICE_LIMIT_MAX)
    def InfoInteger(self, prop_id, var):
        return (SymbolInfoInteger(self.m_name, prop_id, var) != 0)
    def InfoDouble(self, prop_id, var):
        return (SymbolInfoDouble(self.m_name, prop_id, var) != 0)
    def InfoString(self, prop_id, var):
        return _bool(SymbolInfoString(self.m_name, prop_id, var))
    def InfoMarginRate(self, order_type, initial_margin_rate, maintenance_margin_rate):
        return _bool(_missing('SymbolInfoMarginRate')(self.m_name, order_type, initial_margin_rate.v, maintenance_margin_rate.v))
    def NormalizePrice(self, price):
        if self.m_tick_size != 0:
            return NormalizeDouble(MathRound(_fdiv(price, self.m_tick_size)) * self.m_tick_size, self.m_digits)
        return NormalizeDouble(price, self.m_digits)
    def CheckMarketWatch(self):
        if not self.Select_0():
            if GetLastError() == ERR_MARKET_UNKNOWN_SYMBOL:
                printf('CSymbolInfo::CheckMarketWatch' + ": Unknown symbol '%s'", self.m_name)
                return False
            if not self.Select_1(True):
                printf('CSymbolInfo::CheckMarketWatch' + ': Error adding symbol %d', GetLastError())
                return False
        return True

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'SIP')

def OnInit():
    global SpreadBufIdx
    ArrayResize(SpreadBuf, SpreadSmoothTicks)
    for n in range(0, SpreadSmoothTicks):
        SpreadBuf[n] = 0.0
    SpreadBufIdx = 0
    if not m_symbolInfo.Name_1(Symbol()):
        Print('Symbol ', Symbol(), ' initialization false')
    if not m_symbolInfo.Select_1(True):
        Print('Symbol ', Symbol(), ' selection false')
    ObjectsDeleteAll(0, 'SIP')
    Sleep(200)
    ChartRedraw()
    Sleep(200)
    for n in range(ArraySize(lNames) - 1, 0 - 1, -1):
        if not CreateLabel('SIP_' + lNames[ArraySize(lNames) - 1 - n], XOffset, (YOffset * n) + YOffset):
            Print('CreateLabel returns false, n = ', IntegerToString(n))
    Sleep(200)
    ChartRedraw()

def GetMargin(symbol, volume):
    leverage = AccountInfoInteger(ACCOUNT_LEVERAGE)
    contract = SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE) * volume
    margin = _fdiv(volume * contract, leverage)
    return margin

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global SpreadBufIdx
    m_symbolInfo.Refresh()
    m_symbolInfo.RefreshRates()
    SpreadBuf[((SpreadBufIdx := SpreadBufIdx + 1) - 1)] = m_symbolInfo.Ask() - m_symbolInfo.Bid()
    if SpreadBufIdx >= SpreadSmoothTicks:
        SpreadBufIdx = 0
    sprd = 0.0
    for n in range(0, SpreadSmoothTicks):
        sprd += SpreadBuf[n]
    sprd = sprd / float(SpreadSmoothTicks)
    ResetLastError()
    price4lot = Box(0.0)
    Quote2Price(sprd, price4lot, Symbol())
    m_symbolInfo.Refresh()
    marginBuy = 0.0
    marginSell = 0.0
    m_symbolInfo.RefreshRates()
    m_symbolInfo.Refresh()
    ResetLastError()
    ObjectSetString(0, 'SIP_' + lNames[0], OBJPROP_TEXT, lNames[0] + DoubleToString(m_symbolInfo.TickValue(), 2))
    ObjectSetString(0, 'SIP_' + lNames[1], OBJPROP_TEXT, lNames[1] + IntegerToString(m_accountInfo.Leverage()))
    ObjectSetString(0, 'SIP_' + lNames[2], OBJPROP_TEXT, lNames[2] + DoubleToString(sprd, Digits()) + ',  RealSpread=' + DoubleToString(m_symbolInfo.Ask() - m_symbolInfo.Bid(), Digits()))
    ObjectSetString(0, 'SIP_' + lNames[3], OBJPROP_TEXT, lNames[3] + DoubleToString(price4lot.v, 2))
    ObjectSetString(0, 'SIP_' + lNames[4], OBJPROP_TEXT, lNames[4] + DoubleToString(m_symbolInfo.StopsLevel(), 0))
    stop_out_mode = AccountInfoInteger(ACCOUNT_MARGIN_SO_MODE)
    s = (' %' if (stop_out_mode == ACCOUNT_STOPOUT_MODE_PERCENT) else '')
    ObjectSetString(0, 'SIP_' + lNames[5], OBJPROP_TEXT, lNames[5] + DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL), 0) + s)
    ObjectSetString(0, 'SIP_' + lNames[6], OBJPROP_TEXT, lNames[6] + DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_SO_SO), 0) + s)
    return rates_total

def Quote2Price(diff, price4lot, symbol='EURUSD'):
    dig = m_symbolInfo.Digits()
    if dig == 0:
        return False
    tickSize = m_symbolInfo.TickSize()
    tickValue = m_symbolInfo.TickValue()
    price = _fdiv(diff, _fdiv(tickSize, tickValue))
    price4lot.v = NormalizeDouble(price, 2)
    return True

def Price2Quote(diff, price4lot, symbol='EURUSD'):
    dig = Box(0)
    tickSize = Box(0.0)
    tickValue = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, dig):
        return False
    if not SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE, tickSize):
        return False
    if not SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE, tickValue):
        return False
    if tickValue.v > 0:
        diff.v = _fdiv(price4lot * tickSize.v, tickValue.v)
        diff.v = NormalizeDouble(diff.v, _int(dig.v))
    else:
        return False
    return True

def CreateLabel(name, x, y=10):
    if not ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0):
        return False
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
    ObjectSetInteger(0, name, OBJPROP_COLOR, FontColor)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, True)
    ObjectSetString(0, name, OBJPROP_FONT, FontName)
    ChartRedraw()
    return True

def OnTimer():
    pass

def OnChartEvent(id_, lparam, dparam, sparam):
    pass

# ---- global variables initialised from expressions
m_symbolInfo = _alloc(CSymbolInfo)
m_symbolInfo.__init__()
m_accountInfo = _alloc(CAccountInfo)
m_accountInfo.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Showimportantparams(_MQL5Indicator):
    name = 'showimportantparams'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FontSize': 10,
        'XOffset': 10,
        'YOffset': 15,
        'SpreadSmoothTicks': 20,
    }

