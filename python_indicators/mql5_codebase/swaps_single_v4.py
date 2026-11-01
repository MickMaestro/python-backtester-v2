"""Swaps_Single_v4 — converted from MQL5: MQL5 Indicators/Swaps Monitor for a Single Symbol/Swaps_Single_v4.mq5

Copyright: © 2024, Ryan Lawrence Johnson; Link: https://www.mql5.com/en/users/rjo/seller; Version: 4.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: FileReadLong, FileWriteLong, SymbolInfoMarginRate
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': '© 2024, Ryan Lawrence Johnson', 'link': 'https://www.mql5.com/en/users/rjo/seller', 'version': '4.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Swaps_Single_v4', 'source': 'MQL5 Indicators/Swaps Monitor for a Single Symbol/Swaps_Single_v4.mq5', 'folder': 'Swaps Monitor for a Single Symbol', 'inputs': [{'mql': 'UseSymbol', 'py': 'UseSymbol', 'param': None, 'type': 'string', 'default': 'GBPJPY', 'label': '0 means current chart symbol', 'sinput': False}, {'mql': 'XdistanceL', 'py': 'XdistanceL', 'param': 'XdistanceL', 'type': 'int', 'default': 70, 'label': '', 'sinput': False}, {'mql': 'YdistanceL', 'py': 'YdistanceL', 'param': 'YdistanceL', 'type': 'int', 'default': 160, 'label': '', 'sinput': False}, {'mql': 'XdistanceS', 'py': 'XdistanceS', 'param': 'XdistanceS', 'type': 'int', 'default': 70, 'label': '', 'sinput': False}, {'mql': 'YdistanceS', 'py': 'YdistanceS', 'param': 'YdistanceS', 'type': 'int', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'ExpertsTab', 'py': 'ExpertsTab', 'param': 'ExpertsTab', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

INT_VALUE = 0  # MQL5 constant unknown to the converter
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
UseSymbol = _input('UseSymbol', 'GBPJPY')  # 0 means current chart symbol
XdistanceL = _input('XdistanceL', 70)
YdistanceL = _input('YdistanceL', 160)
XdistanceS = _input('XdistanceS', 70)
YdistanceS = _input('YdistanceS', 200)
ExpertsTab = _input('ExpertsTab', False)
Sym = ""
SwapL = ""
SwapS = ""
PswapL = ""
PswapS = ""
swap_long = 0.0
swap_short = 0.0
norm_swap_long = 0.0
norm_swap_short = 0.0
curr_time = 0
last_time = 0

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

class CArray(CObject):
    _q_fields = ('m_step_resize', 'm_data_total', 'm_data_max', 'm_sort_mode')
    def __init__(self):
        CObject.__init__(self)
        self.m_step_resize = 0
        self.m_data_total = 0
        self.m_data_max = 0
        self.m_sort_mode = 0
        self.m_step_resize = 16
        self.m_data_total = 0
        self.m_data_max = 0
        self.m_sort_mode = -1
    def _q_dtor(self):
        pass
    def Step_0(self):
        return self.m_step_resize
    def Step_1(self, step):
        if step > 0:
            self.m_step_resize = step
            return True
        return False
    def Total(self):
        return self.m_data_total
    def Available(self):
        return self.m_data_max - self.m_data_total
    def Max(self):
        return self.m_data_max
    def IsSorted(self, mode=0):
        return self.m_sort_mode == mode
    def SortMode(self):
        return self.m_sort_mode
    def Clear(self):
        self.m_data_total = 0
    def Save(self, file_handle):
        if file_handle != INVALID_HANDLE:
            if _missing('FileWriteLong')(file_handle, -1) == 8:
                if FileWriteInteger(file_handle, self.Type(), INT_VALUE) == INT_VALUE:
                    return True
        return False
    def Load(self, file_handle):
        if file_handle != INVALID_HANDLE:
            if _missing('FileReadLong')(file_handle) == -1:
                if FileReadInteger(file_handle, INT_VALUE) == self.Type():
                    return True
        return False
    def Sort(self, mode=0):
        if self.IsSorted(mode):
            return
        self.m_sort_mode = mode
        if self.m_data_total <= 1:
            return
        self.QuickSort(0, self.m_data_total - 1, mode)
    def QuickSort(self, beg, end, mode=0):
        self.m_sort_mode = -1
    def Minimum(self, data, start, count):
        real_count = 0
        if self.m_data_total < 1:
            SetUserError(1000)
            return -1
        if start < 0 or start >= self.m_data_total:
            SetUserError(3)
            return -1
        real_count = ((self.m_data_total - start) if (count == WHOLE_ARRAY or (start + count) > self.m_data_total) else count)
        return ArrayMinimum(data, start, real_count)
    def Maximum(self, data, start, count):
        real_count = 0
        if self.m_data_total < 1:
            SetUserError(1000)
            return -1
        if start < 0 or start >= self.m_data_total:
            SetUserError(3)
            return -1
        real_count = ((self.m_data_total - start) if (count == WHOLE_ARRAY or (start + count) > self.m_data_total) else count)
        return ArrayMaximum(data, start, real_count)

class CArrayString(CArray):
    _q_fields = ('m_data',)
    def __init__(self):
        CArray.__init__(self)
        self.m_data = Arr(0, "")
        self.m_data_max = ArraySize(self.m_data)
    def _q_dtor(self):
        if self.m_data_max != 0:
            self.Shutdown()
    def Type(self):
        return TYPE_STRING
    def Save(self, file_handle):
        i = 0
        len_ = 0
        if not CArray.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, self.m_data_total):
            len_ = StringLen(self.m_data[i])
            if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
                return False
            if len_ != 0:
                if FileWriteString(file_handle, self.m_data[i], len_) != len_:
                    break
        else:
            i = _range_end(i, self.m_data_total, 1)
        return i == self.m_data_total
    def Load(self, file_handle):
        i = 0
        num = 0
        len_ = 0
        if not CArray.Load(self, file_handle):
            return False
        num = FileReadInteger(file_handle, INT_VALUE)
        self.Clear()
        if num != 0:
            if not self.Reserve(num):
                return False
            i = 0
            for i in range(i, num):
                len_ = FileReadInteger(file_handle, INT_VALUE)
                if len_ != 0:
                    self.m_data[i] = FileReadString(file_handle, len_)
                else:
                    self.m_data[i] = ''
                self.m_data_total += 1
                if FileIsEnding(file_handle):
                    break
            else:
                i = _range_end(i, num, 1)
        self.m_sort_mode = -1
        return self.m_data_total == num
    def Reserve(self, size):
        new_size = 0
        if size <= 0:
            return False
        if self.Available() < size:
            new_size = self.m_data_max + (self.m_step_resize * (1 + _idiv(size - self.Available(), self.m_step_resize)))
            if new_size < 0:
                return False
            if _setattr(self, 'm_data_max', ArrayResize(self.m_data, new_size)) == -1:
                self.m_data_max = ArraySize(self.m_data)
        return self.Available() >= size
    def Resize(self, size):
        new_size = 0
        if size < 0:
            return False
        new_size = self.m_step_resize * (1 + _idiv(size, self.m_step_resize))
        if self.m_data_max != new_size:
            if _setattr(self, 'm_data_max', ArrayResize(self.m_data, new_size)) == -1:
                self.m_data_max = ArraySize(self.m_data)
                return False
        if self.m_data_total > size:
            self.m_data_total = size
        return self.m_data_max == new_size
    def Shutdown(self):
        if self.m_data_max == 0:
            return True
        if ArrayResize(self.m_data, 0) == -1:
            return False
        self.m_data_total = 0
        self.m_data_max = 0
        return True
    def Add(self, element):
        if not self.Reserve(1):
            return False
        self.m_data[_incattr(self, 'm_data_total', 1, True)] = element
        self.m_sort_mode = -1
        return True
    def AddArray_1(self, src):
        num = ArraySize(src)
        if not self.Reserve(num):
            return False
        for i in range(0, num):
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = src[i]
        self.m_sort_mode = -1
        return True
    def AddArray_2(self, src):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.Total()
        if not self.Reserve(num):
            return False
        for i in range(0, num):
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = src.m_data[i]
        self.m_sort_mode = -1
        return True
    def Insert(self, element, pos):
        if pos < 0 or (not self.Reserve(1)):
            return False
        self.m_data_total += 1
        if pos < (self.m_data_total - 1):
            if self.MemMove(pos + 1, pos, self.m_data_total - pos - 1) < 0:
                return False
            self.m_data[pos] = element
        else:
            self.m_data[self.m_data_total - 1] = element
        self.m_sort_mode = -1
        return True
    def InsertArray_1(self, src, pos):
        num = ArraySize(src)
        if not self.Reserve(num):
            return False
        if self.MemMove(num + pos, pos, self.m_data_total - pos) < 0:
            return False
        for i in range(0, num):
            self.m_data[i + pos] = src[i]
        self.m_sort_mode = -1
        return True
    def InsertArray_2(self, src, pos):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.Total()
        if not self.Reserve(num):
            return False
        if self.MemMove(num + pos, pos, self.m_data_total - pos) < 0:
            return False
        for i in range(0, num):
            self.m_data[i + pos] = src.m_data[i]
        self.m_sort_mode = -1
        return True
    def AssignArray_1(self, src):
        num = ArraySize(src)
        self.Clear()
        if self.m_data_max < num:
            if not self.Reserve(num):
                return False
        else:
            self.Resize(num)
        for i in range(0, num):
            self.m_data[i] = src[i]
            self.m_data_total += 1
        self.m_sort_mode = -1
        return True
    def AssignArray_2(self, src):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.m_data_total
        self.Clear()
        if self.m_data_max < num:
            if not self.Reserve(num):
                return False
        else:
            self.Resize(num)
        for i in range(0, num):
            self.m_data[i] = src.m_data[i]
            self.m_data_total += 1
        self.m_sort_mode = src.SortMode()
        return True
    def At(self, index):
        if index < 0 or index >= self.m_data_total:
            return ''
        return self.m_data[index]
    def __getitem__(self, index):
        return self.At(index)
    def Update(self, index, element):
        if index < 0 or index >= self.m_data_total:
            return False
        self.m_data[index] = element
        self.m_sort_mode = -1
        return True
    def Shift(self, index, shift):
        tmp_string = ""
        if (index < 0 or (index + shift) < 0) or (index + shift) >= self.m_data_total:
            return False
        if shift == 0:
            return True
        tmp_string = self.m_data[index]
        if shift > 0:
            if self.MemMove(index, index + 1, shift) < 0:
                return False
        else:
            if self.MemMove(index + shift + 1, index + shift, -shift) < 0:
                return False
        self.m_data[index + shift] = tmp_string
        self.m_sort_mode = -1
        return True
    def Delete(self, index):
        if index < 0 or index >= self.m_data_total:
            return False
        if index < (self.m_data_total - 1) and self.MemMove(index, index + 1, self.m_data_total - index - 1) < 0:
            return False
        self.m_data_total -= 1
        return True
    def DeleteRange(self, from_, to):
        if from_ < 0 or to < 0:
            return False
        if from_ > to or from_ >= self.m_data_total:
            return False
        if to >= (self.m_data_total - 1):
            to = self.m_data_total - 1
        if self.MemMove(from_, to + 1, self.m_data_total - to - 1) < 0:
            return False
        self.m_data_total -= to - from_ + 1
        return True
    def CompareArray_1(self, array):
        if self.m_data_total != ArraySize(array):
            return False
        for i in range(0, self.m_data_total):
            if self.m_data[i] != array[i]:
                return False
        return True
    def CompareArray_2(self, array):
        if not CheckPointer(array):
            return False
        if self.m_data_total != array.m_data_total:
            return False
        for i in range(0, self.m_data_total):
            if self.m_data[i] != array.m_data[i]:
                return False
        return True
    def InsertSort(self, element):
        pos = 0
        if not self.IsSorted():
            return False
        if not self.Reserve(1):
            return False
        if self.m_data_total == 0:
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = element
            return True
        pos = self.QuickSearch(element)
        if self.m_data[pos] > element:
            self.Insert(element, pos)
        else:
            self.Insert(element, pos + 1)
        self.m_sort_mode = 0
        return True
    def Search(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos] == element:
            return pos
        return -1
    def SearchGreat(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos] <= element:
            if (pos := pos + 1) == self.m_data_total:
                return -1
        return pos
    def SearchLess(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos] >= element:
            if ((pos := pos - 1) + 1) == 0:
                return -1
        return pos
    def SearchGreatOrEqual(self, element):
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        for pos in range(self.QuickSearch(element), self.m_data_total):
            if self.m_data[pos] >= element:
                return pos
        return -1
    def SearchLessOrEqual(self, element):
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        for pos in range(self.QuickSearch(element), 0 - 1, -1):
            if self.m_data[pos] <= element:
                return pos
        return -1
    def SearchFirst(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos] == element:
            while self.m_data[pos] == element:
                if ((pos := pos - 1) + 1) == 0:
                    break
            return pos + 1
        return -1
    def SearchLast(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos] == element:
            while self.m_data[pos] == element:
                if (pos := pos + 1) == self.m_data_total:
                    break
            return pos - 1
        return -1
    def SearchLinear(self, element):
        if self.m_data_total == 0:
            return -1
        for i in range(0, self.m_data_total):
            if self.m_data[i] == element:
                return i
        return -1
    def QuickSort(self, beg, end, mode=0):
        i = 0
        j = 0
        p_string = ""
        t_string = ""
        if beg < 0 or end < 0:
            return
        i = beg
        j = end
        while i < end:
            p_string = self.m_data[(beg + end) >> 1]
            while i < j:
                while self.m_data[i] < p_string:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                while self.m_data[j] > p_string:
                    if j == 0:
                        break
                    j -= 1
                if i <= j:
                    t_string = self.m_data[i]
                    self.m_data[((i := i + 1) - 1)] = self.m_data[j]
                    self.m_data[j] = t_string
                    if j == 0:
                        break
                    j -= 1
            if beg < j:
                self.QuickSort(beg, j)
            beg = i
            j = end
    def QuickSearch(self, element):
        i = 0
        j = 0
        m = -1
        t_string = ""
        i = 0
        j = self.m_data_total - 1
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m >= self.m_data_total:
                break
            t_string = self.m_data[m]
            if t_string == element:
                break
            if t_string > element:
                j = m - 1
            else:
                i = m + 1
        return m
    def MemMove(self, dest, src, count):
        i = 0
        if (dest < 0 or src < 0) or count < 0:
            return -1
        if (src + count) > self.m_data_total:
            count = self.m_data_total - src
        if count < 0:
            return -1
        if dest == src or count == 0:
            return dest
        if (dest + count) > self.m_data_total:
            if self.m_data_max < (dest + count):
                return -1
            self.m_data_total = dest + count
        if dest < src:
            i = 0
            for i in range(i, count):
                self.m_data[dest + i] = self.m_data[src + i]
            else:
                i = _range_end(i, count, 1)
        else:
            i = count - 1
            for i in range(i, 0 - 1, -1):
                self.m_data[dest + i] = self.m_data[src + i]
            else:
                i = _range_end(i, 0 - 1, -1)
        return dest

def OnDeinit(reason):
    ObjectDelete(0, 'SwapL')
    ObjectDelete(0, 'SwapS')

def OnInit():
    global SwapL, SwapS, Sym, curr_time, last_time, norm_swap_long, norm_swap_short
    if UseSymbol == '0':
        Sym = Symbol()
    else:
        Sym = UseSymbol
    norm_swap_long = NormalizeDouble(swap_long, 2)
    norm_swap_short = NormalizeDouble(swap_short, 2)
    curr_time = TimeCurrent()
    s_curr_time = MqlDateTime()
    TimeToStruct(curr_time, s_curr_time)
    if s_curr_time.day_of_week == 3:
        norm_swap_long = NormalizeDouble(swap_long * 3, 2)
        norm_swap_short = NormalizeDouble(swap_short * 3, 2)
    SwapL = 'SwapL'
    SwapS = 'SwapS'
    ObjectCreate(0, SwapL, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, SwapL, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, SwapL, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, SwapL, OBJPROP_XDISTANCE, XdistanceL)
    ObjectSetInteger(0, SwapL, OBJPROP_YDISTANCE, YdistanceL)
    ObjectSetString(0, SwapL, OBJPROP_FONT, 'Arial')
    ObjectSetInteger(0, SwapL, OBJPROP_FONTSIZE, 12)
    ObjectSetInteger(0, SwapL, OBJPROP_COLOR, clrDodgerBlue)
    ObjectSetString(0, SwapL, OBJPROP_TEXT, 'Swap Long: ' + DoubleToString(norm_swap_long, 2))
    ObjectCreate(0, SwapS, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, SwapS, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, SwapS, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, SwapS, OBJPROP_XDISTANCE, XdistanceS)
    ObjectSetInteger(0, SwapS, OBJPROP_YDISTANCE, YdistanceS)
    ObjectSetString(0, SwapS, OBJPROP_FONT, 'Arial')
    ObjectSetInteger(0, SwapS, OBJPROP_FONTSIZE, 12)
    ObjectSetInteger(0, SwapS, OBJPROP_COLOR, clrOrangeRed)
    ObjectSetString(0, SwapS, OBJPROP_TEXT, 'Swap Short: ' + DoubleToString(norm_swap_short, 2))
    last_time = _ulong(iTime(Sym, PERIOD_M1, 0))
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global curr_time, last_time, norm_swap_long, norm_swap_short, swap_long, swap_short
    if last_time != _ulong(iTime(Sym, PERIOD_M1, 1)):
        symbol.Name_1(Sym)
        if symbol.SwapMode() == SYMBOL_SWAP_MODE_POINTS:
            swap_long = swap_value_currency(symbol.SwapLong(), symbol.TickValueProfit(), symbol.TickValueLoss())
            swap_short = swap_value_currency(symbol.SwapShort(), symbol.TickValueProfit(), symbol.TickValueLoss())
        norm_swap_long = NormalizeDouble(swap_long, 2)
        norm_swap_short = NormalizeDouble(swap_short, 2)
        curr_time = TimeCurrent()
        s_curr_time = MqlDateTime()
        TimeToStruct(curr_time, s_curr_time)
        if s_curr_time.day_of_week == 3:
            norm_swap_long = NormalizeDouble(swap_long * 3, 2)
            norm_swap_short = NormalizeDouble(swap_short * 3, 2)
        ObjectSetString(0, SwapL, OBJPROP_TEXT, 'Swap Long: ' + DoubleToString(norm_swap_long, 2))
        if ExpertsTab == True:
            Print('swap long updated')
        ObjectSetString(0, SwapS, OBJPROP_TEXT, 'Swap Short: ' + DoubleToString(norm_swap_short, 2))
        if ExpertsTab == True:
            Print('swap short updated')
        last_time = _ulong(iTime(Sym, PERIOD_M1, 1))
    return rates_total

def swap_value_currency(value_point, tickprofit, tickloss):
    if value_point == 0.0:
        return 0.0
    if value_point < 0.0:
        return value_point * tickloss
    return value_point * tickprofit

# ---- global variables initialised from expressions
symbol = _alloc(CSymbolInfo)  # symbol informations object
symbol.__init__()
astring = _alloc(CArrayString)  # string informations object
astring.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SwapsSingleV4(_MQL5Indicator):
    name = 'Swaps_Single_v4'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XdistanceL': 70,
        'YdistanceL': 160,
        'XdistanceS': 70,
        'YdistanceS': 200,
        'ExpertsTab': False,
    }

