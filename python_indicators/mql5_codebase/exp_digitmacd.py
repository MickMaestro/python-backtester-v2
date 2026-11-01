"""exp_digitmacd — converted from MQL5: MQL5 Indicators/Exp_DigitMacd/exp_digitmacd.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- The program has no OnCalculate: it draws only chart objects or reacts to events.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'exp_digitmacd', 'source': 'MQL5 Indicators/Exp_DigitMacd/exp_digitmacd.mq5', 'folder': 'Exp_DigitMacd', 'inputs': [{'mql': 'MM', 'py': 'MM', 'param': 'MM', 'type': 'double', 'default': 0.1, 'label': 'Share of a deposit in a deal', 'sinput': False}, {'mql': 'MMMode', 'py': 'MMMode', 'param': 'MMMode', 'type': 'int', 'default': 4, 'label': 'Lot value calculation method', 'sinput': False}, {'mql': 'StopLoss_', 'py': 'StopLoss_', 'param': 'StopLoss_', 'type': 'int', 'default': 1000, 'label': 'Stop Loss in points', 'sinput': False}, {'mql': 'TakeProfit_', 'py': 'TakeProfit_', 'param': 'TakeProfit_', 'type': 'int', 'default': 2000, 'label': 'Take Profit in points', 'sinput': False}, {'mql': 'Deviation_', 'py': 'Deviation_', 'param': 'Deviation_', 'type': 'int', 'default': 10, 'label': 'Max. price deviation in points', 'sinput': False}, {'mql': 'BuyPosOpen', 'py': 'BuyPosOpen', 'param': 'BuyPosOpen', 'type': 'bool', 'default': True, 'label': 'Permission to buy', 'sinput': False}, {'mql': 'SellPosOpen', 'py': 'SellPosOpen', 'param': 'SellPosOpen', 'type': 'bool', 'default': True, 'label': 'Permission to sell', 'sinput': False}, {'mql': 'BuyPosClose', 'py': 'BuyPosClose', 'param': 'BuyPosClose', 'type': 'bool', 'default': True, 'label': 'Permission to exit long positions', 'sinput': False}, {'mql': 'SellPosClose', 'py': 'SellPosClose', 'param': 'SellPosClose', 'type': 'bool', 'default': True, 'label': 'Permission to exit short positions', 'sinput': False}, {'mql': 'InpInd_Timeframe', 'py': 'InpInd_Timeframe', 'param': 'InpInd_Timeframe', 'type': 'int', 'default': 16388, 'label': 'Indicator timeframe', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'Bar number for getting an entry signal', 'sinput': False}], 'short_form': False, 'has_oncalculate': False, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

ACCOUNT_FREEMARGIN = 0  # MQL5 constant unknown to the converter
MQL5_DEBUGGING = 0  # MQL5 constant unknown to the converter
MQL5_OPTIMIZATION = 0  # MQL5 constant unknown to the converter
MQL5_PROGRAM_TYPE = 0  # MQL5 constant unknown to the converter
MQL5_TESTING = 0  # MQL5 constant unknown to the converter

# enum MarginMode
FREEMARGIN = 0
BALANCE = 1
LOSSFREEMARGIN = 2
LOSSBALANCE = 3
LOT = 4
_enum('MarginMode', {0: 'FREEMARGIN', 1: 'BALANCE', 2: 'LOSSFREEMARGIN', 3: 'LOSSBALANCE', 4: 'LOT'})

# enum HOURS
ENUM_HOUR_0 = 0
ENUM_HOUR_1 = 1
ENUM_HOUR_2 = 2
ENUM_HOUR_3 = 3
ENUM_HOUR_4 = 4
ENUM_HOUR_5 = 5
ENUM_HOUR_6 = 6
ENUM_HOUR_7 = 7
ENUM_HOUR_8 = 8
ENUM_HOUR_9 = 9
ENUM_HOUR_10 = 10
ENUM_HOUR_11 = 11
ENUM_HOUR_12 = 12
ENUM_HOUR_13 = 13
ENUM_HOUR_14 = 14
ENUM_HOUR_15 = 15
ENUM_HOUR_16 = 16
ENUM_HOUR_17 = 17
ENUM_HOUR_18 = 18
ENUM_HOUR_19 = 19
ENUM_HOUR_20 = 20
ENUM_HOUR_21 = 21
ENUM_HOUR_22 = 22
ENUM_HOUR_23 = 23
_enum('HOURS', {0: 'ENUM_HOUR_0', 1: 'ENUM_HOUR_1', 2: 'ENUM_HOUR_2', 3: 'ENUM_HOUR_3', 4: 'ENUM_HOUR_4', 5: 'ENUM_HOUR_5', 6: 'ENUM_HOUR_6', 7: 'ENUM_HOUR_7', 8: 'ENUM_HOUR_8', 9: 'ENUM_HOUR_9', 10: 'ENUM_HOUR_10', 11: 'ENUM_HOUR_11', 12: 'ENUM_HOUR_12', 13: 'ENUM_HOUR_13', 14: 'ENUM_HOUR_14', 15: 'ENUM_HOUR_15', 16: 'ENUM_HOUR_16', 17: 'ENUM_HOUR_17', 18: 'ENUM_HOUR_18', 19: 'ENUM_HOUR_19', 20: 'ENUM_HOUR_20', 21: 'ENUM_HOUR_21', 22: 'ENUM_HOUR_22', 23: 'ENUM_HOUR_23'})

# enum MINUTS
ENUM_MINUT_0 = 0
ENUM_MINUT_1 = 1
ENUM_MINUT_2 = 2
ENUM_MINUT_3 = 3
ENUM_MINUT_4 = 4
ENUM_MINUT_5 = 5
ENUM_MINUT_6 = 6
ENUM_MINUT_7 = 7
ENUM_MINUT_8 = 8
ENUM_MINUT_9 = 9
ENUM_MINUT_10 = 10
ENUM_MINUT_11 = 11
ENUM_MINUT_12 = 12
ENUM_MINUT_13 = 13
ENUM_MINUT_14 = 14
ENUM_MINUT_15 = 15
ENUM_MINUT_16 = 16
ENUM_MINUT_17 = 17
ENUM_MINUT_18 = 18
ENUM_MINUT_19 = 19
ENUM_MINUT_20 = 20
ENUM_MINUT_21 = 21
ENUM_MINUT_22 = 22
ENUM_MINUT_23 = 23
ENUM_MINUT_24 = 24
ENUM_MINUT_25 = 25
ENUM_MINUT_26 = 26
ENUM_MINUT_27 = 27
ENUM_MINUT_28 = 28
ENUM_MINUT_29 = 29
ENUM_MINUT_30 = 30
ENUM_MINUT_31 = 31
ENUM_MINUT_32 = 32
ENUM_MINUT_33 = 33
ENUM_MINUT_34 = 34
ENUM_MINUT_35 = 35
ENUM_MINUT_36 = 36
ENUM_MINUT_37 = 37
ENUM_MINUT_38 = 38
ENUM_MINUT_39 = 39
ENUM_MINUT_40 = 40
ENUM_MINUT_41 = 41
ENUM_MINUT_42 = 42
ENUM_MINUT_43 = 43
ENUM_MINUT_44 = 44
ENUM_MINUT_45 = 45
ENUM_MINUT_46 = 46
ENUM_MINUT_47 = 47
ENUM_MINUT_48 = 48
ENUM_MINUT_49 = 49
ENUM_MINUT_50 = 50
ENUM_MINUT_51 = 51
ENUM_MINUT_52 = 52
ENUM_MINUT_53 = 53
ENUM_MINUT_54 = 54
ENUM_MINUT_55 = 55
ENUM_MINUT_56 = 56
ENUM_MINUT_57 = 57
ENUM_MINUT_58 = 58
ENUM_MINUT_59 = 59
_enum('MINUTS', {0: 'ENUM_MINUT_0', 1: 'ENUM_MINUT_1', 2: 'ENUM_MINUT_2', 3: 'ENUM_MINUT_3', 4: 'ENUM_MINUT_4', 5: 'ENUM_MINUT_5', 6: 'ENUM_MINUT_6', 7: 'ENUM_MINUT_7', 8: 'ENUM_MINUT_8', 9: 'ENUM_MINUT_9', 10: 'ENUM_MINUT_10', 11: 'ENUM_MINUT_11', 12: 'ENUM_MINUT_12', 13: 'ENUM_MINUT_13', 14: 'ENUM_MINUT_14', 15: 'ENUM_MINUT_15', 16: 'ENUM_MINUT_16', 17: 'ENUM_MINUT_17', 18: 'ENUM_MINUT_18', 19: 'ENUM_MINUT_19', 20: 'ENUM_MINUT_20', 21: 'ENUM_MINUT_21', 22: 'ENUM_MINUT_22', 23: 'ENUM_MINUT_23', 24: 'ENUM_MINUT_24', 25: 'ENUM_MINUT_25', 26: 'ENUM_MINUT_26', 27: 'ENUM_MINUT_27', 28: 'ENUM_MINUT_28', 29: 'ENUM_MINUT_29', 30: 'ENUM_MINUT_30', 31: 'ENUM_MINUT_31', 32: 'ENUM_MINUT_32', 33: 'ENUM_MINUT_33', 34: 'ENUM_MINUT_34', 35: 'ENUM_MINUT_35', 36: 'ENUM_MINUT_36', 37: 'ENUM_MINUT_37', 38: 'ENUM_MINUT_38', 39: 'ENUM_MINUT_39', 40: 'ENUM_MINUT_40', 41: 'ENUM_MINUT_41', 42: 'ENUM_MINUT_42', 43: 'ENUM_MINUT_43', 44: 'ENUM_MINUT_44', 45: 'ENUM_MINUT_45', 46: 'ENUM_MINUT_46', 47: 'ENUM_MINUT_47', 48: 'ENUM_MINUT_48', 49: 'ENUM_MINUT_49', 50: 'ENUM_MINUT_50', 51: 'ENUM_MINUT_51', 52: 'ENUM_MINUT_52', 53: 'ENUM_MINUT_53', 54: 'ENUM_MINUT_54', 55: 'ENUM_MINUT_55', 56: 'ENUM_MINUT_56', 57: 'ENUM_MINUT_57', 58: 'ENUM_MINUT_58', 59: 'ENUM_MINUT_59'})

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
MM = _input('MM', 0.1)  # Share of a deposit in a deal
MMMode = _input('MMMode', LOT)  # Lot value calculation method
StopLoss_ = _input('StopLoss_', 1000)  # Stop Loss in points
TakeProfit_ = _input('TakeProfit_', 2000)  # Take Profit in points
Deviation_ = _input('Deviation_', 10)  # Max. price deviation in points
BuyPosOpen = _input('BuyPosOpen', True)  # Permission to buy
SellPosOpen = _input('SellPosOpen', True)  # Permission to sell
BuyPosClose = _input('BuyPosClose', True)  # Permission to exit long positions
SellPosClose = _input('SellPosClose', True)  # Permission to exit short positions
InpInd_Timeframe = _input('InpInd_Timeframe', PERIOD_H4)  # Indicator timeframe
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Price constant
SignalBar = _input('SignalBar', 1)  # Bar number for getting an entry signal
TimeShiftSec = 0
InpInd_Handle = 0
min_rates_total = 0

class CIsNewBar(MqlObject):
    _q_fields = ('m_TOld',)
    def __init__(self):
        self.m_TOld = 0
        self.m_TOld = -1
    def IsNewBar(self, symbol, timeframe):
        TNew = SeriesInfoInteger(symbol, timeframe, SERIES_LASTBAR_DATE)
        if TNew != self.m_TOld and TNew:
            self.m_TOld = TNew
            return True
        return False

def BuyPositionOpen_1(BUY_Signal, symbol, TimeLevel, Money_Management, Margin_Mode, deviation, StopLoss, Takeprofit):
    StopLoss = Box(StopLoss)
    Takeprofit = Box(Takeprofit)
    if not BUY_Signal.v:
        return True
    PosType = POSITION_TYPE_BUY
    if not TradeTimeLevelCheck(symbol, PosType, TimeLevel):
        return True
    if PositionSelect(symbol):
        return True
    volume = BuyLotCount(symbol, Money_Management, Margin_Mode, StopLoss.v, deviation)
    if volume <= 0:
        Print('BuyPositionOpen', '(): Неверный объём для структуры торгового запроса')
        return False
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Ask = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_ASK, Ask):
        return True
    request.type = ORDER_TYPE_BUY
    request.price = Ask.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume
    if StopLoss.v:
        if not StopCorrect(symbol, StopLoss):
            return False
        dStopLoss = StopLoss.v * point.v
        request.sl = NormalizeDouble(request.price - dStopLoss, _int(digit.v))
    else:
        request.sl = 0.0
    if Takeprofit.v:
        if not StopCorrect(symbol, Takeprofit):
            return False
        dTakeprofit = Takeprofit.v * point.v
        request.tp = NormalizeDouble(request.price + dTakeprofit, _int(digit.v))
    else:
        request.tp = 0.0
    request.deviation = deviation
    if not OrderCheck(request, check):
        Print('BuyPositionOpen', '(): Неверные данные для структуры торгового запроса!')
        Print('BuyPositionOpen', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'BuyPositionOpen', '(): Открываем Buy позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('BuyPositionOpen', '(): Невозможно совершить сделку!')
        Print('BuyPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        TradeTimeLevelSet(symbol, PosType, TimeLevel)
        BUY_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'BuyPositionOpen', '(): Buy позиция по ', symbol, ' открыта ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    else:
        Print('BuyPositionOpen', '(): Невозможно совершить сделку!')
        Print('BuyPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
    return True

def BuyPositionOpen_2(BUY_Signal, symbol, TimeLevel, Money_Management, Margin_Mode, deviation, dStopLoss, dTakeprofit):
    dStopLoss = Box(dStopLoss)
    dTakeprofit = Box(dTakeprofit)
    if not BUY_Signal.v:
        return True
    PosType = POSITION_TYPE_BUY
    if not TradeTimeLevelCheck(symbol, PosType, TimeLevel):
        return True
    if PositionSelect(symbol):
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Ask = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_ASK, Ask):
        return True
    if not dStopCorrect(symbol, dStopLoss, dTakeprofit, PosType):
        return False
    StopLoss = _int(_fdiv(Ask.v - dStopLoss.v, point.v))
    volume = BuyLotCount(symbol, Money_Management, Margin_Mode, StopLoss, deviation)
    if volume <= 0:
        Print('BuyPositionOpen', '(): Неверный объём для структуры торгового запроса')
        return False
    request.type = ORDER_TYPE_BUY
    request.price = Ask.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume
    request.sl = dStopLoss.v
    request.tp = dTakeprofit.v
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    if not OrderCheck(request, check):
        Print('BuyPositionOpen', '(): Неверные данные для структуры торгового запроса!')
        Print('BuyPositionOpen', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'BuyPositionOpen', '(): Открываем Buy позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('BuyPositionOpen', '(): Невозможно совершить сделку!')
        Print('BuyPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        TradeTimeLevelSet(symbol, PosType, TimeLevel)
        BUY_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'BuyPositionOpen', '(): Buy позиция по ', symbol, ' открыта ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    else:
        Print('BuyPositionOpen', '(): Невозможно совершить сделку!')
        Print('BuyPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
    return True

def SellPositionOpen_1(SELL_Signal, symbol, TimeLevel, Money_Management, Margin_Mode, deviation, StopLoss, Takeprofit):
    StopLoss = Box(StopLoss)
    Takeprofit = Box(Takeprofit)
    if not SELL_Signal.v:
        return True
    PosType = POSITION_TYPE_SELL
    if not TradeTimeLevelCheck(symbol, PosType, TimeLevel):
        return True
    if PositionSelect(symbol):
        return True
    volume = SellLotCount(symbol, Money_Management, Margin_Mode, StopLoss.v, deviation)
    if volume <= 0:
        Print('SellPositionOpen', '(): Неверный объём для структуры торгового запроса')
        return False
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Bid = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_BID, Bid):
        return True
    request.type = ORDER_TYPE_SELL
    request.price = Bid.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume
    if StopLoss.v != 0:
        if not StopCorrect(symbol, StopLoss):
            return False
        dStopLoss = StopLoss.v * point.v
        request.sl = NormalizeDouble(request.price + dStopLoss, _int(digit.v))
    else:
        request.sl = 0.0
    if Takeprofit.v != 0:
        if not StopCorrect(symbol, Takeprofit):
            return False
        dTakeprofit = Takeprofit.v * point.v
        request.tp = NormalizeDouble(request.price - dTakeprofit, _int(digit.v))
    else:
        request.tp = 0.0
    request.deviation = deviation
    if not OrderCheck(request, check):
        Print('SellPositionOpen', '(): Неверные данные для структуры торгового запроса!')
        Print('SellPositionOpen', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'SellPositionOpen', '(): Открываем Sell позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('SellPositionOpen', '(): Невозможно совершить сделку!')
        Print('SellPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        TradeTimeLevelSet(symbol, PosType, TimeLevel)
        SELL_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'SellPositionOpen', '(): Sell позиция по ', symbol, ' открыта ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    else:
        Print('SellPositionOpen', '(): Невозможно совершить сделку!')
        Print('SellPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
    return True

def SellPositionOpen_2(SELL_Signal, symbol, TimeLevel, Money_Management, Margin_Mode, deviation, dStopLoss, dTakeprofit):
    dStopLoss = Box(dStopLoss)
    dTakeprofit = Box(dTakeprofit)
    if not SELL_Signal.v:
        return True
    PosType = POSITION_TYPE_SELL
    if not TradeTimeLevelCheck(symbol, PosType, TimeLevel):
        return True
    if PositionSelect(symbol):
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Bid = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_BID, Bid):
        return True
    if not dStopCorrect(symbol, dStopLoss, dTakeprofit, PosType):
        return False
    StopLoss = _int(_fdiv(dStopLoss.v - Bid.v, point.v))
    volume = SellLotCount(symbol, Money_Management, Margin_Mode, StopLoss, deviation)
    if volume <= 0:
        Print('SellPositionOpen', '(): Неверный объём для структуры торгового запроса')
        return False
    request.type = ORDER_TYPE_SELL
    request.price = Bid.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    if not OrderCheck(request, check):
        Print('SellPositionOpen', '(): OrderCheck(): Неверные данные для структуры торгового запроса!')
        Print('SellPositionOpen', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'SellPositionOpen', '(): Открываем Sell позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('SellPositionOpen', '(): OrderSend(): Невозможно совершить сделку!')
        Print('SellPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        TradeTimeLevelSet(symbol, PosType, TimeLevel)
        SELL_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'SellPositionOpen', '(): Sell позиция по ', symbol, ' открыта ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    else:
        Print('SellPositionOpen', '(): OrderSend(): Невозможно совершить сделку!')
        Print('SellPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
    return True

def BuyPositionClose(Signal, symbol, deviation):
    if not Signal.v:
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    if PositionSelect(symbol):
        if PositionGetInteger(POSITION_TYPE) != POSITION_TYPE_BUY:
            return False
    else:
        return False
    MaxLot = Box(0.0)
    volume = Box(0.0)
    Bid = Box(0.0)
    if not PositionGetDouble(POSITION_VOLUME, volume):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX, MaxLot):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_BID, Bid):
        return True
    if volume.v > MaxLot.v:
        volume.v = MaxLot.v
    request.type = ORDER_TYPE_SELL
    request.price = Bid.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume.v
    request.sl = 0.0
    request.tp = 0.0
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    request.position = PositionGetInteger(POSITION_TICKET)
    if not OrderCheck(request, check):
        Print('BuyPositionClose', '(): Неверные данные для структуры торгового запроса!')
        Print('BuyPositionClose', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'BuyPositionClose', '(): Закрываем Buy позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('BuyPositionClose', '(): Невозможно закрыть позицию!')
        Print('BuyPositionClose', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'BuyPositionClose', '(): Buy позиция по ', symbol, ' закрыта ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    else:
        Print('BuyPositionClose', '(): Невозможно закрыть позицию!')
        Print('BuyPositionClose', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
    return True

def SellPositionClose(Signal, symbol, deviation):
    if not Signal.v:
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    if PositionSelect(symbol):
        if PositionGetInteger(POSITION_TYPE) != POSITION_TYPE_SELL:
            return False
    else:
        return False
    MaxLot = Box(0.0)
    volume = Box(0.0)
    Ask = Box(0.0)
    if not PositionGetDouble(POSITION_VOLUME, volume):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX, MaxLot):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_ASK, Ask):
        return True
    if volume.v > MaxLot.v:
        volume.v = MaxLot.v
    request.type = ORDER_TYPE_BUY
    request.price = Ask.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume.v
    request.sl = 0.0
    request.tp = 0.0
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    request.position = PositionGetInteger(POSITION_TICKET)
    if not OrderCheck(request, check):
        Print('SellPositionClose', '(): Неверные данные для структуры торгового запроса!')
        Print('SellPositionClose', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'SellPositionClose', '(): Закрываем Sell позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('SellPositionClose', '(): Невозможно закрыть позицию!')
        Print('SellPositionClose', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        Signal.v = False
    else:
        Print('SellPositionClose', '(): Невозможно закрыть позицию!')
        Print('SellPositionClose', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'SellPositionClose', '(): Sell позиция по ', symbol, ' закрыта ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    return True

def ReBuyPositionOpen(BUY_Signal, symbol, TimeLevel, Money_Management, MaxPosVolume, deviation, StopLoss, Takeprofit):
    StopLoss = Box(StopLoss)
    Takeprofit = Box(Takeprofit)
    if not BUY_Signal.v:
        return True
    PosType = POSITION_TYPE_BUY
    if not TradeTimeLevelCheck(symbol, PosType, TimeLevel):
        return True
    if (not PositionSelect(symbol)) or PositionGetInteger(POSITION_TYPE) != POSITION_TYPE_BUY:
        return True
    volume = BuyLotCount(symbol, Money_Management, LOT, StopLoss.v, deviation)
    if volume <= 0:
        Print('ReBuyPositionOpen', '(): Неверный объём для структуры торгового запроса')
        Print('ReBuyPositionOpen', '(): Полученный объём = ', volume)
        return False
    maxvolume = BuyLotCount(symbol, MaxPosVolume, LOT, StopLoss.v, deviation)
    if (PositionGetDouble(POSITION_VOLUME) + volume) > MaxPosVolume:
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Ask = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_ASK, Ask):
        return True
    request.type = ORDER_TYPE_BUY
    request.price = Ask.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume
    if StopLoss.v:
        if not StopCorrect(symbol, StopLoss):
            return False
        dStopLoss = StopLoss.v * point.v
        request.sl = NormalizeDouble(request.price - dStopLoss, _int(digit.v))
    else:
        request.sl = 0.0
    if Takeprofit.v:
        if not StopCorrect(symbol, Takeprofit):
            return False
        dTakeprofit = Takeprofit.v * point.v
        request.tp = NormalizeDouble(request.price + dTakeprofit, _int(digit.v))
    else:
        request.tp = 0.0
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    if not OrderCheck(request, check):
        Print('ReBuyPositionOpen', '(): Неверные данные для структуры торгового запроса!')
        Print('ReBuyPositionOpen', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'ReBuyPositionOpen', '(): Доливаем Buy позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or (result.retcode != TRADE_RETCODE_DONE and result.retcode != TRADE_RETCODE_PLACED):
        Print('ReBuyPositionOpen', '(): Невозможно совершить сделку!')
        Print('ReBuyPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
        return False
    elif result.retcode == TRADE_RETCODE_DONE or result.retcode == TRADE_RETCODE_PLACED:
        TradeTimeLevelSet(symbol, PosType, TimeLevel)
        BUY_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'ReBuyPositionOpen', '(): Buy позиция по ', symbol, ' долита объёмом ', DoubleToString(request.volume, 4), ' ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
        Sleep(5000)
    else:
        Print('ReBuyPositionOpen', '(): Невозможно совершить сделку!')
        Print('ReBuyPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
    return True

def ReSellPositionOpen(SELL_Signal, symbol, TimeLevel, Money_Management, MaxPosVolume, deviation, StopLoss, Takeprofit):
    StopLoss = Box(StopLoss)
    Takeprofit = Box(Takeprofit)
    if not SELL_Signal.v:
        return True
    PosType = POSITION_TYPE_SELL
    if not TradeTimeLevelCheck(symbol, PosType, TimeLevel):
        return True
    if (not PositionSelect(symbol)) or PositionGetInteger(POSITION_TYPE) != POSITION_TYPE_SELL:
        return True
    volume = SellLotCount(symbol, Money_Management, LOT, StopLoss.v, deviation)
    if volume <= 0:
        Print('ReSellPositionOpen', '(): Неверный объём для структуры торгового запроса')
        Print('ReSellPositionOpen', '(): Полученный объём = ', volume)
        return False
    maxvolume = SellLotCount(symbol, MaxPosVolume, LOT, StopLoss.v, deviation)
    if (PositionGetDouble(POSITION_VOLUME) + volume) > MaxPosVolume:
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Bid = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_BID, Bid):
        return True
    request.type = ORDER_TYPE_SELL
    request.price = Bid.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume
    if StopLoss.v != 0:
        if not StopCorrect(symbol, StopLoss):
            return False
        dStopLoss = StopLoss.v * point.v
        request.sl = NormalizeDouble(request.price + dStopLoss, _int(digit.v))
    else:
        request.sl = 0.0
    if Takeprofit.v != 0:
        if not StopCorrect(symbol, Takeprofit):
            return False
        dTakeprofit = Takeprofit.v * point.v
        request.tp = NormalizeDouble(request.price - dTakeprofit, _int(digit.v))
    else:
        request.tp = 0.0
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    if not OrderCheck(request, check):
        Print('ReSellPositionOpen', '(): Неверные данные для структуры торгового запроса!')
        Print('ReSellPositionOpen', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'ReSellPositionOpen', '(): Доливаем Sell позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or (result.retcode != TRADE_RETCODE_DONE and result.retcode != TRADE_RETCODE_PLACED):
        Print('ReSellPositionOpen', '(): Невозможно совершить сделку!')
        Print('ReSellPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
        return False
    elif result.retcode == TRADE_RETCODE_DONE or result.retcode == TRADE_RETCODE_PLACED:
        TradeTimeLevelSet(symbol, PosType, TimeLevel)
        SELL_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'ReSellPositionOpen', '(): Sell позиция по ', symbol, ' долита объёмом ', DoubleToString(request.volume, 4), ' ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
        Sleep(5000)
    else:
        Print('ReSellPositionOpen', '(): Невозможно совершить сделку!')
        Print('ReSellPositionOpen', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
    return True

def ReBuyPositionOpen_X(BUY_Signal, symbol, TimeLevel, Money_Management, Margin_Mode, deviation, StopLoss, Takeprofit, PosComment):
    StopLoss = Box(StopLoss)
    Takeprofit = Box(Takeprofit)
    if not BUY_Signal.v:
        return True
    PosType = POSITION_TYPE_BUY
    if not TradeTimeLevelCheck(symbol, PosType, TimeLevel):
        return True
    if (not PositionSelect(symbol)) or PositionGetInteger(POSITION_TYPE) != POSITION_TYPE_BUY:
        return True
    volume = BuyLotCount(symbol, Money_Management, LOT, StopLoss.v, deviation)
    if volume <= 0:
        Print('ReBuyPositionOpen_X', '(1): Неверный объём для структуры торгового запроса')
        Print('ReBuyPositionOpen_X', '(1): Полученный объём = ', volume)
        Print('ReBuyPositionOpen_X', '(1): Исходное значение переменной Money_Management = ', Money_Management)
        return False
    LastVolume = PositionGetDouble(POSITION_VOLUME)
    LastOpenPrice = PositionGetDouble(POSITION_PRICE_OPEN)
    ResaltVolume = BuyLotCount(symbol, LastVolume + volume, 4, 0, deviation)
    if ResaltVolume <= LastVolume:
        Print('ReBuyPositionOpen_X', '(2): Неверный объём для структуры торгового запроса')
        Print('ReBuyPositionOpen_X', '(2): Полученный объём = ', ResaltVolume)
        return False
    volume = ResaltVolume - LastVolume
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Ask = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_ASK, Ask):
        return True
    request.type = ORDER_TYPE_BUY
    request.price = Ask.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume
    request.comment = PosComment + '/' + DoubleToString(volume, 3)
    if StopLoss.v:
        if not StopCorrect(symbol, StopLoss):
            return False
        dStopLoss = StopLoss.v * point.v
        request.sl = NormalizeDouble(request.price - dStopLoss, _int(digit.v))
    else:
        request.sl = 0.0
    if Takeprofit.v:
        if not StopCorrect(symbol, Takeprofit):
            return False
        dTakeprofit = Takeprofit.v * point.v
        request.tp = NormalizeDouble(request.price + dTakeprofit, _int(digit.v))
    else:
        request.tp = 0.0
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    if not OrderCheck(request, check):
        Print('ReBuyPositionOpen_X', '(): Неверные данные для структуры торгового запроса!')
        Print('ReBuyPositionOpen_X', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'ReBuyPositionOpen_X', '(): Доливаем Buy позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or (result.retcode != TRADE_RETCODE_DONE and result.retcode != TRADE_RETCODE_PLACED):
        Print('ReBuyPositionOpen_X', '(): Невозможно совершить сделку!')
        Print('ReBuyPositionOpen_X', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
        return False
    elif result.retcode == TRADE_RETCODE_DONE or result.retcode == TRADE_RETCODE_PLACED:
        TradeTimeLevelSet(symbol, PosType, TimeLevel)
        BUY_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'ReBuyPositionOpen_X', '(): Buy позиция по ', symbol, ' долита объёмом ', DoubleToString(request.volume, 4), ' ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
        Sleep(5000)
    else:
        Print('ReBuyPositionOpen_X', '(): Невозможно совершить сделку!')
        Print('ReBuyPositionOpen_X', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
    return True

def ReSellPositionOpen_X(SELL_Signal, symbol, TimeLevel, Money_Management, Margin_Mode, deviation, StopLoss, Takeprofit, PosComment):
    StopLoss = Box(StopLoss)
    Takeprofit = Box(Takeprofit)
    if not SELL_Signal.v:
        return True
    PosType = POSITION_TYPE_SELL
    if not TradeTimeLevelCheck(symbol, PosType, TimeLevel):
        return True
    if (not PositionSelect(symbol)) or PositionGetInteger(POSITION_TYPE) != POSITION_TYPE_SELL:
        return True
    volume = BuyLotCount(symbol, Money_Management, LOT, StopLoss.v, deviation)
    if volume <= 0:
        Print('ReSellPositionOpen_X', '(1): Неверный объём для структуры торгового запроса')
        Print('ReSellPositionOpen_X', '(1): Полученный объём = ', volume)
        Print('ReSellPositionOpen_X', '(1): Исходное значение переменной Money_Management = ', Money_Management)
        return False
    LastVolume = PositionGetDouble(POSITION_VOLUME)
    LastOpenPrice = PositionGetDouble(POSITION_PRICE_OPEN)
    ResaltVolume = BuyLotCount(symbol, LastVolume + volume, 4, 0, deviation)
    if ResaltVolume <= LastVolume:
        Print('ReSellPositionOpen_X', '(2): Неверный объём для структуры торгового запроса')
        Print('ReSellPositionOpen_X', '(2): Полученный объём = ', ResaltVolume)
        return False
    volume = ResaltVolume - LastVolume
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Bid = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_BID, Bid):
        return True
    request.type = ORDER_TYPE_SELL
    request.price = Bid.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume
    request.comment = PosComment + '/' + DoubleToString(volume, 3)
    if StopLoss.v != 0:
        if not StopCorrect(symbol, StopLoss):
            return False
        dStopLoss = StopLoss.v * point.v
        request.sl = NormalizeDouble(request.price + dStopLoss, _int(digit.v))
    else:
        request.sl = 0.0
    if Takeprofit.v != 0:
        if not StopCorrect(symbol, Takeprofit):
            return False
        dTakeprofit = Takeprofit.v * point.v
        request.tp = NormalizeDouble(request.price - dTakeprofit, _int(digit.v))
    else:
        request.tp = 0.0
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    if not OrderCheck(request, check):
        Print('ReSellPositionOpen_X', '(): Неверные данные для структуры торгового запроса!')
        Print('ReSellPositionOpen_X', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'ReSellPositionOpen_X', '(): Доливаем Sell позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or (result.retcode != TRADE_RETCODE_DONE and result.retcode != TRADE_RETCODE_PLACED):
        Print('ReSellPositionOpen_X', '(): Невозможно совершить сделку!')
        Print('ReSellPositionOpen_X', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
        return False
    elif result.retcode == TRADE_RETCODE_DONE or result.retcode == TRADE_RETCODE_PLACED:
        TradeTimeLevelSet(symbol, PosType, TimeLevel)
        SELL_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'ReSellPositionOpen_X', '(): Sell позиция по ', symbol, ' долита объёмом ', DoubleToString(request.volume, 4), ' ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
        Sleep(5000)
    else:
        Print('ReSellPositionOpen_X', '(): Невозможно совершить сделку!')
        Print('ReSellPositionOpen_X', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
    return True

def BuyPositionModify(Modify_Signal, symbol, deviation, StopLoss, Takeprofit):
    StopLoss = Box(StopLoss)
    Takeprofit = Box(Takeprofit)
    if not Modify_Signal.v:
        return True
    PosType = POSITION_TYPE_BUY
    if not PositionSelect(symbol):
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Ask = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_ASK, Ask):
        return True
    request.type = ORDER_TYPE_BUY
    request.price = Ask.v
    request.action = TRADE_ACTION_SLTP
    request.symbol = symbol
    if StopLoss.v:
        if not StopCorrect(symbol, StopLoss):
            return False
        dStopLoss = StopLoss.v * point.v
        request.sl = NormalizeDouble(request.price - dStopLoss, _int(digit.v))
        if request.sl < PositionGetDouble(POSITION_SL):
            request.sl = PositionGetDouble(POSITION_SL)
    else:
        request.sl = PositionGetDouble(POSITION_SL)
    if Takeprofit.v:
        if not StopCorrect(symbol, Takeprofit):
            return False
        dTakeprofit = Takeprofit.v * point.v
        request.tp = NormalizeDouble(request.price + dTakeprofit, _int(digit.v))
        if request.tp < PositionGetDouble(POSITION_TP):
            request.tp = PositionGetDouble(POSITION_TP)
    else:
        request.tp = PositionGetDouble(POSITION_TP)
    if request.tp == PositionGetDouble(POSITION_TP) and request.sl == PositionGetDouble(POSITION_SL):
        return True
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    if not OrderCheck(request, check):
        Print('BuyPositionModify', '(): Неверные данные для структуры торгового запроса!')
        Print('BuyPositionModify', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'BuyPositionModify', '(): Модифицируем Buy позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('BuyPositionModify', '(): Невозможно модифицировать позицию!')
        Print('BuyPositionModify', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        Modify_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'BuyPositionModify', '(): Buy позиция по ', symbol, ' модифицирована ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    else:
        Print('BuyPositionModify', '(): Невозможно модифицировать позицию!')
        Print('BuyPositionModify', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
    return True

def SellPositionModify(Modify_Signal, symbol, deviation, StopLoss, Takeprofit):
    StopLoss = Box(StopLoss)
    Takeprofit = Box(Takeprofit)
    if not Modify_Signal.v:
        return True
    PosType = POSITION_TYPE_SELL
    if not PositionSelect(symbol):
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Bid = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_BID, Bid):
        return True
    request.type = ORDER_TYPE_SELL
    request.price = Bid.v
    request.action = TRADE_ACTION_SLTP
    request.symbol = symbol
    if StopLoss.v != 0:
        if not StopCorrect(symbol, StopLoss):
            return False
        dStopLoss = StopLoss.v * point.v
        request.sl = NormalizeDouble(request.price + dStopLoss, _int(digit.v))
        laststop = PositionGetDouble(POSITION_SL)
        if request.sl > laststop and laststop:
            request.sl = PositionGetDouble(POSITION_SL)
    else:
        request.sl = PositionGetDouble(POSITION_SL)
    if Takeprofit.v != 0:
        if not StopCorrect(symbol, Takeprofit):
            return False
        dTakeprofit = Takeprofit.v * point.v
        request.tp = NormalizeDouble(request.price - dTakeprofit, _int(digit.v))
        lasttake = PositionGetDouble(POSITION_TP)
        if request.tp > lasttake and lasttake:
            request.tp = PositionGetDouble(POSITION_TP)
    else:
        request.tp = PositionGetDouble(POSITION_TP)
    if request.tp == PositionGetDouble(POSITION_TP) and request.sl == PositionGetDouble(POSITION_SL):
        return True
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    if not OrderCheck(request, check):
        Print('SellPositionModify', '(): Неверные данные для структуры торгового запроса!')
        Print('SellPositionModify', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'SellPositionModify', '(): Модифицируем Sell позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('SellPositionModify', '(): Невозможно модифицировать позицию!')
        Print('SellPositionModify', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        Modify_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'SellPositionModify', '(): Sell позиция по ', symbol, ' модифицирована ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    else:
        Print('SellPositionModify', '(): Невозможно модифицировать позицию!')
        Print('SellPositionModify', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
    return True

def dBuyPositionModify(Modify_Signal, symbol, deviation, StopLoss, Takeprofit):
    if not Modify_Signal.v:
        return True
    PosType = POSITION_TYPE_BUY
    if not PositionSelect(symbol):
        return True
    if PositionGetInteger(POSITION_TYPE) != PosType:
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = _int(SymbolInfoInteger(symbol, SYMBOL_DIGITS))
    point = SymbolInfoDouble(symbol, SYMBOL_POINT)
    Ask = SymbolInfoDouble(symbol, SYMBOL_ASK)
    if ((not digit) or (not point)) or (not Ask):
        return True
    request.type = ORDER_TYPE_BUY
    request.price = Ask
    request.action = TRADE_ACTION_SLTP
    request.symbol = symbol
    request.position = PositionGetInteger(POSITION_TICKET)
    if StopLoss:
        nStopLoss = Box(_int(_fdiv(Ask - StopLoss, point)))
        if nStopLoss.v < 0:
            return False
        if not StopCorrect(symbol, nStopLoss):
            return False
        dStopLoss = nStopLoss.v * point
        request.sl = NormalizeDouble(request.price - dStopLoss, digit)
        if request.sl < PositionGetDouble(POSITION_SL):
            request.sl = PositionGetDouble(POSITION_SL)
    else:
        request.sl = PositionGetDouble(POSITION_SL)
    if Takeprofit:
        nTakeprofit = Box(_int(_fdiv(Takeprofit - Ask, point)))
        if nTakeprofit.v < 0:
            return False
        if not StopCorrect(symbol, nTakeprofit):
            return False
        dTakeprofit = nTakeprofit.v * point
        request.tp = NormalizeDouble(request.price + dTakeprofit, digit)
        if request.tp < PositionGetDouble(POSITION_TP):
            request.tp = PositionGetDouble(POSITION_TP)
    else:
        request.tp = PositionGetDouble(POSITION_TP)
    if request.tp == PositionGetDouble(POSITION_TP) and request.sl == PositionGetDouble(POSITION_SL):
        return True
    request.deviation = deviation
    if not OrderCheck(request, check):
        Print('dBuyPositionModify', '(): Неверные данные для структуры торгового запроса!')
        Print('dBuyPositionModify', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'dBuyPositionModify', '(): Модифицируем Buy позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('dBuyPositionModify', '(): Невозможно модифицировать позицию!')
        Print('dBuyPositionModify', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        Modify_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'dBuyPositionModify', '(): Buy позиция по ', symbol, ' модифицирована ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    else:
        Print('dBuyPositionModify', '(): Невозможно модифицировать позицию!')
        Print('dBuyPositionModify', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
    return True

def dSellPositionModify(Modify_Signal, symbol, deviation, StopLoss, Takeprofit):
    if not Modify_Signal.v:
        return True
    PosType = POSITION_TYPE_SELL
    if not PositionSelect(symbol):
        return True
    if PositionGetInteger(POSITION_TYPE) != PosType:
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = _int(SymbolInfoInteger(symbol, SYMBOL_DIGITS))
    point = SymbolInfoDouble(symbol, SYMBOL_POINT)
    Ask = SymbolInfoDouble(symbol, SYMBOL_ASK)
    if ((not digit) or (not point)) or (not Ask):
        return True
    request.type = ORDER_TYPE_SELL
    request.price = Ask
    request.action = TRADE_ACTION_SLTP
    request.symbol = symbol
    request.position = PositionGetInteger(POSITION_TICKET)
    if StopLoss != 0:
        nStopLoss = Box(_int(_fdiv(StopLoss - Ask, point)))
        if nStopLoss.v < 0:
            return False
        if not StopCorrect(symbol, nStopLoss):
            return False
        dStopLoss = nStopLoss.v * point
        request.sl = NormalizeDouble(request.price + dStopLoss, digit)
        laststop = PositionGetDouble(POSITION_SL)
        if request.sl > laststop and laststop:
            request.sl = PositionGetDouble(POSITION_SL)
    else:
        request.sl = PositionGetDouble(POSITION_SL)
    if Takeprofit != 0:
        nTakeprofit = Box(_int(_fdiv(Ask - Takeprofit, point)))
        if nTakeprofit.v < 0:
            return False
        if not StopCorrect(symbol, nTakeprofit):
            return False
        dTakeprofit = nTakeprofit.v * point
        request.tp = NormalizeDouble(request.price - dTakeprofit, digit)
        lasttake = PositionGetDouble(POSITION_TP)
        if request.tp > lasttake and lasttake:
            request.tp = PositionGetDouble(POSITION_TP)
    else:
        request.tp = PositionGetDouble(POSITION_TP)
    if request.tp == PositionGetDouble(POSITION_TP) and request.sl == PositionGetDouble(POSITION_SL):
        return True
    request.deviation = deviation
    if not OrderCheck(request, check):
        Print('dSellPositionModify', '(): Неверные данные для структуры торгового запроса!')
        Print('dSellPositionModify', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'dSellPositionModify', '(): Модифицируем Sell позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('dSellPositionModify', '(): Невозможно модифицировать позицию!')
        Print('dSellPositionModify', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        Modify_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'dSellPositionModify', '(): Sell позиция по ', symbol, ' модифицирована ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    else:
        Print('dSellPositionModify', '(): Невозможно модифицировать позицию!')
        Print('dSellPositionModify', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
    return True

def GetTimeLevelName(symbol, trade_operation):
    G_Name_ = Box("")
    if (MQL5InfoInteger(MQL5_TESTING) or MQL5InfoInteger(MQL5_OPTIMIZATION)) or MQL5InfoInteger(MQL5_DEBUGGING):
        StringConcatenate(G_Name_, 'TimeLevel_', AccountInfoInteger(ACCOUNT_LOGIN), '_', symbol, '_', trade_operation, '_Test_')
    else:
        StringConcatenate(G_Name_, 'TimeLevel_', AccountInfoInteger(ACCOUNT_LOGIN), '_', symbol, '_', trade_operation)
    return G_Name_.v

def TradeTimeLevelCheck(symbol, trade_operation, TradeTimeLevel):
    if TradeTimeLevel > 0:
        if TimeCurrent() < GlobalVariableGet(GetTimeLevelName(symbol, trade_operation)):
            return False
    return True

def TradeTimeLevelSet(symbol, trade_operation, TradeTimeLevel):
    GlobalVariableSet(GetTimeLevelName(symbol, trade_operation), TradeTimeLevel)

def TradeTimeLevelGet(symbol, trade_operation):
    return _long(GlobalVariableGet(GetTimeLevelName(symbol, trade_operation)))

def TimeLevelGlobalVariableDel(symbol, trade_operation):
    if (MQL5InfoInteger(MQL5_TESTING) or MQL5InfoInteger(MQL5_OPTIMIZATION)) or MQL5InfoInteger(MQL5_DEBUGGING):
        GlobalVariableDel(GetTimeLevelName(symbol, trade_operation))

def GlobalVariableDel_(symbol):
    TimeLevelGlobalVariableDel(symbol, POSITION_TYPE_BUY)
    TimeLevelGlobalVariableDel(symbol, POSITION_TYPE_SELL)

def BuyPositionOpen_M1(BUY_Signal, symbol, TimeLevel, Money_Management, Margin_Mode, deviation, StopLoss, Takeprofit, Magic):
    StopLoss = Box(StopLoss)
    Takeprofit = Box(Takeprofit)
    if not BUY_Signal.v:
        return True
    PosType = POSITION_TYPE_BUY
    if not TradeTimeLevelCheckM(symbol, PosType, Magic, TimeLevel):
        return True
    if PositionSelectByMagice(symbol, Magic):
        return True
    volume = BuyLotCount(symbol, Money_Management, Margin_Mode, StopLoss.v, deviation)
    if volume <= 0:
        Print('BuyPositionOpen_M1', '(): Неверный объём для структуры торгового запроса')
        return False
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Ask = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_ASK, Ask):
        return True
    request.type = ORDER_TYPE_BUY
    request.price = Ask.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume
    request.magic = Magic
    if StopLoss.v:
        if not StopCorrect(symbol, StopLoss):
            return False
        dStopLoss = StopLoss.v * point.v
        request.sl = NormalizeDouble(request.price - dStopLoss, _int(digit.v))
    else:
        request.sl = 0.0
    if Takeprofit.v:
        if not StopCorrect(symbol, Takeprofit):
            return False
        dTakeprofit = Takeprofit.v * point.v
        request.tp = NormalizeDouble(request.price + dTakeprofit, _int(digit.v))
    else:
        request.tp = 0.0
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    if not OrderCheck(request, check):
        Print('BuyPositionOpen_M1', '(): Неверные данные для структуры торгового запроса!')
        Print('BuyPositionOpen_M1', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'BuyPositionOpen_M1', '(): Открываем Buy позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or (result.retcode != TRADE_RETCODE_DONE and result.retcode != TRADE_RETCODE_PLACED):
        Print('BuyPositionOpen_M1', '(): Невозможно совершить сделку!')
        Print('BuyPositionOpen_M1', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
        return False
    elif result.retcode == TRADE_RETCODE_DONE or result.retcode == TRADE_RETCODE_PLACED:
        TradeTimeLevelSetM(symbol, PosType, Magic, TimeLevel)
        BUY_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'BuyPositionOpen_M1', '(): Buy позиция по ', symbol, ' открыта объёмом ', DoubleToString(request.volume, 4), ' ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
        Sleep(5000)
    else:
        Print('BuyPositionOpen_M1', '(): Невозможно совершить сделку!')
        Print('BuyPositionOpen_M1', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
    return True

def SellPositionOpen_M1(SELL_Signal, symbol, TimeLevel, Money_Management, Margin_Mode, deviation, StopLoss, Takeprofit, Magic):
    StopLoss = Box(StopLoss)
    Takeprofit = Box(Takeprofit)
    if not SELL_Signal.v:
        return True
    PosType = POSITION_TYPE_SELL
    if not TradeTimeLevelCheckM(symbol, PosType, Magic, TimeLevel):
        return True
    if PositionSelectByMagice(symbol, Magic):
        return True
    volume = SellLotCount(symbol, Money_Management, Margin_Mode, StopLoss.v, deviation)
    if volume <= 0:
        Print('SellPositionOpen_M1', '(): Неверный объём для структуры торгового запроса')
        return False
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    digit = Box(0)
    point = Box(0.0)
    Bid = Box(0.0)
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_BID, Bid):
        return True
    request.type = ORDER_TYPE_SELL
    request.price = Bid.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume
    request.magic = Magic
    if StopLoss.v != 0:
        if not StopCorrect(symbol, StopLoss):
            return False
        dStopLoss = StopLoss.v * point.v
        request.sl = NormalizeDouble(request.price + dStopLoss, _int(digit.v))
    else:
        request.sl = 0.0
    if Takeprofit.v != 0:
        if not StopCorrect(symbol, Takeprofit):
            return False
        dTakeprofit = Takeprofit.v * point.v
        request.tp = NormalizeDouble(request.price - dTakeprofit, _int(digit.v))
    else:
        request.tp = 0.0
    request.deviation = deviation
    request.type_filling = ORDER_FILLING_FOK
    if not OrderCheck(request, check):
        Print('SellPositionOpen_M1', '(): Неверные данные для структуры торгового запроса!')
        Print('SellPositionOpen_M1', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'SellPositionOpen_M1', '(): Открываем Sell позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or (result.retcode != TRADE_RETCODE_DONE and result.retcode != TRADE_RETCODE_PLACED):
        Print('SellPositionOpen_M1', '(): Невозможно совершить сделку!')
        Print('SellPositionOpen_M1', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
        return False
    elif result.retcode == TRADE_RETCODE_DONE or result.retcode == TRADE_RETCODE_PLACED:
        TradeTimeLevelSetM(symbol, PosType, Magic, TimeLevel)
        SELL_Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'SellPositionOpen_M1', '(): Sell позиция по ', symbol, ' открыта объёмом ', DoubleToString(request.volume, 4), ' ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
        Sleep(5000)
    else:
        Print('SellPositionOpen_M1', '(): Невозможно совершить сделку!')
        Print('SellPositionOpen_M1', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        Sleep(5000)
    return True

def GetTimeLevelNameM(symbol, trade_operation, magic):
    G_Name_ = Box("")
    if (MQL5InfoInteger(MQL5_TESTING) or MQL5InfoInteger(MQL5_OPTIMIZATION)) or MQL5InfoInteger(MQL5_DEBUGGING):
        StringConcatenate(G_Name_, 'TimeLevelM_', AccountInfoInteger(ACCOUNT_LOGIN), '_', symbol, '_', trade_operation, '_', magic, '_Test_')
    else:
        StringConcatenate(G_Name_, 'TimeLevelM_', AccountInfoInteger(ACCOUNT_LOGIN), '_', symbol, '_', trade_operation, '_', magic)
    return G_Name_.v

def TradeTimeLevelCheckM(symbol, trade_operation, magic, TradeTimeLevel):
    if TradeTimeLevel > 0:
        if TimeCurrent() < GlobalVariableGet(GetTimeLevelNameM(symbol, trade_operation, magic)):
            return False
    return True

def TradeTimeLevelSetM(symbol, trade_operation, magic, TradeTimeLevel):
    GlobalVariableSet(GetTimeLevelNameM(symbol, trade_operation, magic), TradeTimeLevel)

def TradeTimeLevelGetM(symbol, trade_operation, magic):
    return _long(GlobalVariableGet(GetTimeLevelNameM(symbol, trade_operation, magic)))

def TimeLevelGlobalVariableDelM(symbol, trade_operation, magic):
    if (MQL5InfoInteger(MQL5_TESTING) or MQL5InfoInteger(MQL5_OPTIMIZATION)) or MQL5InfoInteger(MQL5_DEBUGGING):
        GlobalVariableDel(GetTimeLevelNameM(symbol, trade_operation, magic))

def GlobalVariableDel_M(symbol, magic):
    TimeLevelGlobalVariableDelM(symbol, POSITION_TYPE_BUY, magic)
    TimeLevelGlobalVariableDelM(symbol, POSITION_TYPE_SELL, magic)

def BuyPositionClose_M(Signal, symbol, deviation, Magic):
    if not Signal.v:
        return True
    if not PositionSelectByMagice(symbol, Magic):
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    MaxLot = Box(0.0)
    volume = Box(0.0)
    Bid = Box(0.0)
    ticket = Box(0)
    if not PositionGetDouble(POSITION_VOLUME, volume):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX, MaxLot):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_BID, Bid):
        return True
    if not PositionGetInteger(POSITION_TICKET, ticket):
        return True
    if volume.v > MaxLot.v:
        volume.v = MaxLot.v
    request.type = ORDER_TYPE_SELL
    request.price = Bid.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume.v
    request.sl = 0.0
    request.tp = 0.0
    request.deviation = deviation
    request.position = ticket.v
    if not OrderCheck(request, check):
        Print('BuyPositionClose_M', '(): Неверные данные для структуры торгового запроса!')
        Print('BuyPositionClose_M', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'BuyPositionClose_M', '(): Закрываем Buy позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('BuyPositionClose_M', '(): Невозможно закрыть позицию!')
        Print('BuyPositionClose_M', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        Signal.v = False
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'BuyPositionClose_M', '(): Buy позиция по ', symbol, ' закрыта ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    else:
        Print('BuyPositionClose_M', '(): Невозможно закрыть позицию!')
        Print('BuyPositionClose_M', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
    return True

def SellPositionClose_M(Signal, symbol, deviation, Magic):
    if not Signal.v:
        return True
    if not PositionSelectByMagice(symbol, Magic):
        return True
    request = MqlTradeRequest()
    result = MqlTradeResult()
    check = MqlTradeCheckResult()
    ZeroMemory(request)
    ZeroMemory(result)
    ZeroMemory(check)
    MaxLot = Box(0.0)
    volume = Box(0.0)
    Ask = Box(0.0)
    ticket = Box(0)
    if not PositionGetDouble(POSITION_VOLUME, volume):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX, MaxLot):
        return True
    if not SymbolInfoDouble(symbol, SYMBOL_ASK, Ask):
        return True
    if not PositionGetInteger(POSITION_TICKET, ticket):
        return True
    if volume.v > MaxLot.v:
        volume.v = MaxLot.v
    request.type = ORDER_TYPE_BUY
    request.price = Ask.v
    request.action = TRADE_ACTION_DEAL
    request.symbol = symbol
    request.volume = volume.v
    request.sl = 0.0
    request.tp = 0.0
    request.deviation = deviation
    request.position = ticket.v
    if not OrderCheck(request, check):
        Print('SellPositionClose_M', '(): Неверные данные для структуры торгового запроса!')
        Print('SellPositionClose_M', '(): OrderCheck(): ', ResultRetcodeDescription(_int(check.retcode)))
        return False
    comment = Box('')
    StringConcatenate(comment, '<<< ============ ', 'SellPositionClose_M', '(): Закрываем Sell позицию по ', symbol, ' ============ >>>')
    Print(comment.v)
    if (not OrderSend(request, result)) or result.retcode != TRADE_RETCODE_DONE:
        Print('SellPositionClose_M', '(): Невозможно закрыть позицию!')
        Print('SellPositionClose_M', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        return False
    elif result.retcode == TRADE_RETCODE_DONE:
        Signal.v = False
    else:
        Print('SellPositionClose_M', '(): Невозможно закрыть позицию!')
        Print('SellPositionClose_M', '(): OrderSend(): ', ResultRetcodeDescription(_int(result.retcode)))
        comment.v = ''
        StringConcatenate(comment, '<<< ============ ', 'SellPositionClose_M', '(): Sell позиция по ', symbol, ' закрыта ============ >>>')
        Print(comment.v)
        PlaySound('ok.wav')
    return True

def PositionSelectByMagice(symbol, Magic):
    deals = PositionsTotal()
    for pos in range(deals - 1, 0 - 1, -1):
        deal_ticket = PositionGetTicket(pos)
        if not PositionSelectByTicket(deal_ticket):
            continue
        if PositionGetString(POSITION_SYMBOL) != symbol:
            continue
        if PositionGetInteger(POSITION_MAGIC) == Magic:
            return True
    return False

def BuyLotCount(symbol, Money_Management, Margin_Mode, STOPLOSS, Slippage_):
    STOPLOSS = Box(STOPLOSS)
    margin = 0.0
    Lot = Box(0.0)
    if Money_Management < 0:
        Lot.v = MathAbs(Money_Management)
    else:
        _sw1 = Margin_Mode
        if _sw1 == 0:
            margin = AccountInfoDouble(ACCOUNT_FREEMARGIN) * Money_Management
            Lot.v = GetLotForOpeningPos(symbol, POSITION_TYPE_BUY, margin)
        elif _sw1 == 1:
            margin = AccountInfoDouble(ACCOUNT_BALANCE) * Money_Management
            Lot.v = GetLotForOpeningPos(symbol, POSITION_TYPE_BUY, margin)
        elif _sw1 == 2:
            if STOPLOSS.v <= 0:
                Print('BuyLotCount', ': Неверный стоплосс!!!')
                STOPLOSS.v = 0
            digit = Box(0)
            point = Box(0.0)
            price_open = Box(0.0)
            if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
                return -1.0
            if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
                return -1.0
            if not SymbolInfoDouble(symbol, SYMBOL_ASK, price_open):
                return -1.0
            if not StopCorrect(symbol, STOPLOSS):
                return TRADE_RETCODE_ERROR
            price_close = NormalizeDouble(price_open.v - (STOPLOSS.v * point.v), _int(digit.v))
            profit = 0.0
            if not OrderCalcProfit(ORDER_TYPE_BUY, symbol, 1, price_open.v, price_close, profit):
                return -1.0
            if not profit:
                return -1.0
            Loss = AccountInfoDouble(ACCOUNT_FREEMARGIN) * Money_Management
            if not Loss:
                return -1.0
            Lot.v = _fdiv(Loss, MathAbs(profit))
        elif _sw1 == 3:
            if STOPLOSS.v <= 0:
                Print('BuyLotCount', ': Неверный стоплосс!!!')
                STOPLOSS.v = 0
            digit = Box(0)
            point = Box(0.0)
            price_open = Box(0.0)
            if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
                return -1.0
            if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
                return -1.0
            if not SymbolInfoDouble(symbol, SYMBOL_ASK, price_open):
                return -1.0
            if not StopCorrect(symbol, STOPLOSS):
                return TRADE_RETCODE_ERROR
            price_close = NormalizeDouble(price_open.v - (STOPLOSS.v * point.v), _int(digit.v))
            profit = 0.0
            if not OrderCalcProfit(ORDER_TYPE_BUY, symbol, 1, price_open.v, price_close, profit):
                return -1.0
            if not profit:
                return -1.0
            Loss = AccountInfoDouble(ACCOUNT_BALANCE) * Money_Management
            if not Loss:
                return -1.0
            Lot.v = _fdiv(Loss, MathAbs(profit))
        elif _sw1 == 4:
            Lot.v = MathAbs(Money_Management)
        else:
            margin = AccountInfoDouble(ACCOUNT_FREEMARGIN) * Money_Management
            Lot.v = GetLotForOpeningPos(symbol, POSITION_TYPE_BUY, margin)
    if not LotCorrect(symbol, Lot, POSITION_TYPE_BUY):
        return -1.0
    return Lot.v

def SellLotCount(symbol, Money_Management, Margin_Mode, STOPLOSS, Slippage_):
    STOPLOSS = Box(STOPLOSS)
    margin = 0.0
    Lot = Box(0.0)
    if Money_Management < 0:
        Lot.v = MathAbs(Money_Management)
    else:
        _sw2 = Margin_Mode
        if _sw2 == 0:
            margin = AccountInfoDouble(ACCOUNT_FREEMARGIN) * Money_Management
            Lot.v = GetLotForOpeningPos(symbol, POSITION_TYPE_SELL, margin)
        elif _sw2 == 1:
            margin = AccountInfoDouble(ACCOUNT_BALANCE) * Money_Management
            Lot.v = GetLotForOpeningPos(symbol, POSITION_TYPE_SELL, margin)
        elif _sw2 == 2:
            if STOPLOSS.v <= 0:
                Print('SellLotCount', ': Неверный стоплосс!!!')
                STOPLOSS.v = 0
            digit = Box(0)
            point = Box(0.0)
            price_open = Box(0.0)
            if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
                return -1.0
            if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
                return -1.0
            if not SymbolInfoDouble(symbol, SYMBOL_BID, price_open):
                return -1.0
            if not StopCorrect(symbol, STOPLOSS):
                return TRADE_RETCODE_ERROR
            price_close = NormalizeDouble(price_open.v + (STOPLOSS.v * point.v), _int(digit.v))
            profit = 0.0
            if not OrderCalcProfit(ORDER_TYPE_SELL, symbol, 1, price_open.v, price_close, profit):
                return -1.0
            if not profit:
                return -1.0
            Loss = AccountInfoDouble(ACCOUNT_FREEMARGIN) * Money_Management
            if not Loss:
                return -1.0
            Lot.v = _fdiv(Loss, MathAbs(profit))
        elif _sw2 == 3:
            if STOPLOSS.v <= 0:
                Print('SellLotCount', ': Неверный стоплосс!!!')
                STOPLOSS.v = 0
            digit = Box(0)
            point = Box(0.0)
            price_open = Box(0.0)
            if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
                return -1.0
            if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
                return -1.0
            if not SymbolInfoDouble(symbol, SYMBOL_BID, price_open):
                return -1.0
            if not StopCorrect(symbol, STOPLOSS):
                return TRADE_RETCODE_ERROR
            price_close = NormalizeDouble(price_open.v + (STOPLOSS.v * point.v), _int(digit.v))
            profit = 0.0
            if not OrderCalcProfit(ORDER_TYPE_SELL, symbol, 1, price_open.v, price_close, profit):
                return -1.0
            if not profit:
                return -1.0
            Loss = AccountInfoDouble(ACCOUNT_BALANCE) * Money_Management
            if not Loss:
                return -1.0
            Lot.v = _fdiv(Loss, MathAbs(profit))
        elif _sw2 == 4:
            Lot.v = MathAbs(Money_Management)
        else:
            margin = AccountInfoDouble(ACCOUNT_FREEMARGIN) * Money_Management
            Lot.v = GetLotForOpeningPos(symbol, POSITION_TYPE_SELL, margin)
    if not LotCorrect(symbol, Lot, POSITION_TYPE_SELL):
        return -1.0
    return Lot.v

def StopCorrect(symbol, Stop):
    Extrem_Stop = Box(0)
    if not SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL, Extrem_Stop):
        return False
    if Stop.v < Extrem_Stop.v:
        Stop.v = _int(Extrem_Stop.v)
    return True

def dStopCorrect(symbol, dStopLoss, dTakeprofit, trade_operation):
    if (not dStopLoss.v) and (not dTakeprofit.v):
        return True
    if dStopLoss.v < 0:
        Print('dStopCorrect', '(): Отрицательное значение стоплосса!')
        return False
    if dTakeprofit.v < 0:
        Print('dStopCorrect', '(): Отрицательное значение тейкпрофита!')
        return False
    Stop = Box(0)
    digit = Box(0)
    point = Box(0.0)
    dStop = 0.0
    ExtrStop = 0.0
    ExtrTake = 0.0
    Stop.v = 0
    if not StopCorrect(symbol, Stop):
        return False
    if not SymbolInfoInteger(symbol, SYMBOL_DIGITS, digit):
        return False
    if not SymbolInfoDouble(symbol, SYMBOL_POINT, point):
        return False
    dStop = Stop.v * point.v
    if trade_operation == POSITION_TYPE_BUY:
        Ask = Box(0.0)
        if not SymbolInfoDouble(symbol, SYMBOL_ASK, Ask):
            return False
        ExtrStop = NormalizeDouble(Ask.v - dStop, _int(digit.v))
        ExtrTake = NormalizeDouble(Ask.v + dStop, _int(digit.v))
        if dStopLoss.v > ExtrStop and dStopLoss.v:
            dStopLoss.v = ExtrStop
        if dTakeprofit.v < ExtrTake and dTakeprofit.v:
            dTakeprofit.v = ExtrTake
    if trade_operation == POSITION_TYPE_SELL:
        Bid = Box(0.0)
        if not SymbolInfoDouble(symbol, SYMBOL_BID, Bid):
            return False
        ExtrStop = NormalizeDouble(Bid.v + dStop, _int(digit.v))
        ExtrTake = NormalizeDouble(Bid.v - dStop, _int(digit.v))
        if dStopLoss.v < ExtrStop and dStopLoss.v:
            dStopLoss.v = ExtrStop
        if dTakeprofit.v > ExtrTake and dTakeprofit.v:
            dTakeprofit.v = ExtrTake
    return True

def LotCorrect(symbol, Lot, trade_operation):
    Step = Box(0.0)
    MaxLot = Box(0.0)
    MinLot = Box(0.0)
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP, Step):
        return False
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX, MaxLot):
        return False
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN, MinLot):
        return False
    Lot.v = Step.v * MathFloor(_fdiv(Lot.v, Step.v))
    if Lot.v < MinLot.v:
        Lot.v = MinLot.v
    if Lot.v > MaxLot.v:
        Lot.v = MaxLot.v
    if not LotFreeMarginCorrect(symbol, Lot, trade_operation):
        return False
    return True

def LotFreeMarginCorrect(symbol, Lot, trade_operation):
    freemargin = AccountInfoDouble(ACCOUNT_FREEMARGIN)
    if freemargin <= 0:
        return False
    Step = Box(0.0)
    MaxLot = Box(0.0)
    MinLot = Box(0.0)
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP, Step):
        return False
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX, MaxLot):
        return False
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN, MinLot):
        return False
    ExtremLot = GetLotForOpeningPos(symbol, trade_operation, freemargin)
    ExtremLot = Step.v * MathFloor(_fdiv(ExtremLot, Step.v))
    if ExtremLot < MinLot.v:
        return False
    if Lot.v > ExtremLot:
        Lot.v = ExtremLot
    if Lot.v > MaxLot.v:
        Lot.v = MaxLot.v
    return True

def GetLotForOpeningPos(symbol, direction, lot_margin):
    price = Box(0.0)
    n_margin = 0.0
    if direction == POSITION_TYPE_BUY:
        if not SymbolInfoDouble(symbol, SYMBOL_ASK, price):
            return 0.0
    if direction == POSITION_TYPE_SELL:
        if not SymbolInfoDouble(symbol, SYMBOL_BID, price):
            return 0.0
    if not price.v:
        return 0.0
    if (not OrderCalcMargin(direction, symbol, 1, price.v, n_margin)) or (not n_margin):
        return 0.0
    lot = _fdiv(lot_margin, n_margin)
    LOTSTEP = Box(0.0)
    MaxLot = Box(0.0)
    MinLot = Box(0.0)
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP, LOTSTEP):
        return 0.0
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX, MaxLot):
        return 0.0
    if not SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN, MinLot):
        return 0.0
    lot = LOTSTEP.v * MathFloor(_fdiv(lot, LOTSTEP.v))
    if lot < MinLot.v:
        lot = 0.0
    if lot > MaxLot.v:
        lot = MaxLot.v
    return lot

def GetSymbolByCurrencies(margin_currency, profit_currency):
    total = SymbolsTotal(True)
    for numb in range(0, total):
        symbolname = SymbolName(numb, True)
        m_cur = SymbolInfoString(symbolname, SYMBOL_CURRENCY_MARGIN)
        p_cur = SymbolInfoString(symbolname, SYMBOL_CURRENCY_PROFIT)
        if m_cur == margin_currency and p_cur == profit_currency:
            return symbolname
    return ""

def ResultRetcodeDescription(retcode):
    str_ = ""
    _sw3 = retcode
    if _sw3 == TRADE_RETCODE_REQUOTE:
        str_ = 'Реквота'
    elif _sw3 == TRADE_RETCODE_REJECT:
        str_ = 'Запрос отвергнут'
    elif _sw3 == TRADE_RETCODE_CANCEL:
        str_ = 'Запрос отменен трейдером'
    elif _sw3 == TRADE_RETCODE_PLACED:
        str_ = 'Ордер размещен'
    elif _sw3 == TRADE_RETCODE_DONE:
        str_ = 'Заявка выполнена'
    elif _sw3 == TRADE_RETCODE_DONE_PARTIAL:
        str_ = 'Заявка выполнена частично'
    elif _sw3 == TRADE_RETCODE_ERROR:
        str_ = 'Ошибка обработки запроса'
    elif _sw3 == TRADE_RETCODE_TIMEOUT:
        str_ = 'Запрос отменен по истечению времени'
    elif _sw3 == TRADE_RETCODE_INVALID:
        str_ = 'Неправильный запрос'
    elif _sw3 == TRADE_RETCODE_INVALID_VOLUME:
        str_ = 'Неправильный объем в запросе'
    elif _sw3 == TRADE_RETCODE_INVALID_PRICE:
        str_ = 'Неправильная цена в запросе'
    elif _sw3 == TRADE_RETCODE_INVALID_STOPS:
        str_ = 'Неправильные стопы в запросе'
    elif _sw3 == TRADE_RETCODE_TRADE_DISABLED:
        str_ = 'Торговля запрещена'
    elif _sw3 == TRADE_RETCODE_MARKET_CLOSED:
        str_ = 'Рынок закрыт'
    elif _sw3 == TRADE_RETCODE_NO_MONEY:
        str_ = 'Нет достаточных денежных средств для выполнения запроса'
    elif _sw3 == TRADE_RETCODE_PRICE_CHANGED:
        str_ = 'Цены изменились'
    elif _sw3 == TRADE_RETCODE_PRICE_OFF:
        str_ = 'Отсутствуют котировки для обработки запроса'
    elif _sw3 == TRADE_RETCODE_INVALID_EXPIRATION:
        str_ = 'Неверная дата истечения ордера в запросе'
    elif _sw3 == TRADE_RETCODE_ORDER_CHANGED:
        str_ = 'Состояние ордера изменилось'
    elif _sw3 == TRADE_RETCODE_TOO_MANY_REQUESTS:
        str_ = 'Слишком частые запросы'
    elif _sw3 == TRADE_RETCODE_NO_CHANGES:
        str_ = 'В запросе нет изменений'
    elif _sw3 == TRADE_RETCODE_SERVER_DISABLES_AT:
        str_ = 'Автотрейдинг запрещен сервером'
    elif _sw3 == TRADE_RETCODE_CLIENT_DISABLES_AT:
        str_ = 'Автотрейдинг запрещен клиентским терминалом'
    elif _sw3 == TRADE_RETCODE_LOCKED:
        str_ = 'Запрос заблокирован для обработки'
    elif _sw3 == TRADE_RETCODE_FROZEN:
        str_ = 'Ордер или позиция заморожены'
    elif _sw3 == TRADE_RETCODE_INVALID_FILL:
        str_ = 'Указан неподдерживаемый тип исполнения ордера по остатку'
    elif _sw3 == TRADE_RETCODE_CONNECTION:
        str_ = 'Нет соединения с торговым сервером'
    elif _sw3 == TRADE_RETCODE_ONLY_REAL:
        str_ = 'Операция разрешена только для реальных счетов'
    elif _sw3 == TRADE_RETCODE_LIMIT_ORDERS:
        str_ = 'Достигнут лимит на количество отложенных ордеров'
    elif _sw3 == TRADE_RETCODE_LIMIT_VOLUME:
        str_ = 'Достигнут лимит на объем ордеров и позиций для данного символа'
    elif _sw3 == TRADE_RETCODE_INVALID_ORDER:
        str_ = 'Неверный или запрещённый тип ордера'
    elif _sw3 == TRADE_RETCODE_POSITION_CLOSED:
        str_ = 'Позиция с указанным POSITION_IDENTIFIER уже закрыта'
    elif _sw3 == TRADE_RETCODE_INVALID_CLOSE_VOLUME:
        str_ = 'Закрываемый объем превышает текущий объем позиции'
    elif _sw3 == TRADE_RETCODE_CLOSE_ORDER_EXIST:
        str_ = 'Для указанной позиции уже есть ордер на закрытие'
    elif _sw3 == TRADE_RETCODE_LIMIT_POSITIONS:
        str_ = 'Количество открытых позиций, которое можно одновременно иметь на счете, может быть ограничено настройками сервера'
    else:
        str_ = 'Неизвестный результат'
    return str_

def LoadHistory(StartDate, LoadedSymbol, LoadedPeriod):
    res = CheckLoadHistory(LoadedSymbol, LoadedPeriod, StartDate)
    _sw4 = res
    if _sw4 == -1:
        Print('LoadHistory', '(', LoadedSymbol, ' ', EnumToString(LoadedPeriod, 'ENUM_TIMEFRAMES'), '): Unknown symbol ', LoadedSymbol)
    elif _sw4 == -2:
        Print('LoadHistory', '(', LoadedSymbol, ' ', EnumToString(LoadedPeriod, 'ENUM_TIMEFRAMES'), '): Requested bars more than max bars in chart ')
    elif _sw4 == -3:
        Print('LoadHistory', '(', LoadedSymbol, ' ', EnumToString(LoadedPeriod, 'ENUM_TIMEFRAMES'), '): Program was stopped ')
    elif _sw4 == -4:
        Print('LoadHistory', '(', LoadedSymbol, ' ', EnumToString(LoadedPeriod, 'ENUM_TIMEFRAMES'), "): Indicator shouldn't load its own data ")
    elif _sw4 == -5:
        Print('LoadHistory', '(', LoadedSymbol, ' ', EnumToString(LoadedPeriod, 'ENUM_TIMEFRAMES'), '): Load failed ')
    elif _sw4 == 0:
        pass
    elif _sw4 == 1:
        pass
    elif _sw4 == 2:
        pass
    else:
        pass
    return res

def CheckLoadHistory(symbol, period, start_date):
    first_date = Box(0)
    times = Arr(100, 0, dyn=False)
    if symbol == "" or symbol == '':
        symbol = Symbol()
    if period == PERIOD_CURRENT:
        period = Period()
    if not SymbolInfoInteger(symbol, SYMBOL_SELECT):
        if GetLastError() == ERR_MARKET_UNKNOWN_SYMBOL:
            return -1
        if not SymbolSelect(symbol, True):
            Print('CheckLoadHistory', '(): Не удалось добавить символ ', symbol, ' в окно MarketWatch!!!')
    SeriesInfoInteger(symbol, period, SERIES_FIRSTDATE, first_date)
    if first_date.v > 0 and first_date.v <= start_date:
        return 1
    if (MQL5InfoInteger(MQL5_PROGRAM_TYPE) == PROGRAM_INDICATOR and Period() == period) and Symbol() == symbol:
        return -4
    if SeriesInfoInteger(symbol, PERIOD_M1, SERIES_TERMINAL_FIRSTDATE, first_date):
        if first_date.v > 0:
            CopyTime(symbol, period, first_date.v + PeriodSeconds(period), 1, times)
            if SeriesInfoInteger(symbol, period, SERIES_FIRSTDATE, first_date):
                if first_date.v > 0 and first_date.v <= start_date:
                    return 2
    max_bars = TerminalInfoInteger(TERMINAL_MAXBARS)
    first_server_date = Box(0)
    while not SeriesInfoInteger(symbol, PERIOD_M1, SERIES_SERVER_FIRSTDATE, first_server_date):
        Sleep(5)
    if first_server_date.v > start_date:
        start_date = first_server_date.v
    if first_date.v > 0 and first_date.v < first_server_date.v:
        Print('CheckLoadHistory', '(): Warning: first server date ', first_server_date.v, ' for ', symbol, ' does not match to first series date ', first_date.v)
    fail_cnt = 0
    while True:
        while not SeriesInfoInteger(symbol, period, SERIES_SYNCHRONIZED):
            Sleep(5)
        bars = Bars(symbol, period)
        if bars > 0:
            if bars >= max_bars:
                return -2
            if SeriesInfoInteger(symbol, period, SERIES_FIRSTDATE, first_date):
                if first_date.v > 0 and first_date.v <= start_date:
                    return 0
        copied = CopyTime(symbol, period, bars, 100, times)
        if copied > 0:
            if times[0] <= start_date:
                return 0
            if (bars + copied) >= max_bars:
                return -2
            fail_cnt = 0
        else:
            fail_cnt += 1
            if fail_cnt >= 100:
                return -5
            Sleep(10)
    return -3

def OnInit():
    global InpInd_Handle, TimeShiftSec, min_rates_total
    InpInd_Handle = iCustom(Symbol(), InpInd_Timeframe, 'DigitMacd', AppliedPrice)
    if InpInd_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the DigitMacd indicator')
        return INIT_FAILED
    TimeShiftSec = PeriodSeconds(InpInd_Timeframe)
    min_rates_total = 39 + 65 + 1
    min_rates_total += _int(3 + SignalBar)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    GlobalVariableDel_(Symbol())

def OnTick():
    global _s_OnTick_BUY_Close, _s_OnTick_BUY_Open, _s_OnTick_DnSignalTime, _s_OnTick_Recount, _s_OnTick_SELL_Close, _s_OnTick_SELL_Open, _s_OnTick_UpSignalTime
    if BarsCalculated(InpInd_Handle) < min_rates_total:
        return
    LoadHistory(TimeCurrent() - PeriodSeconds(InpInd_Timeframe) - 1, Symbol(), InpInd_Timeframe)
    Ind = Arr(2, 0.0, dyn=False)
    Sign = Arr(2, 0.0, dyn=False)
    if ((not SignalBar) or _s_OnTick_NB.IsNewBar(Symbol(), InpInd_Timeframe)) or _s_OnTick_Recount:
        _s_OnTick_BUY_Open = False
        _s_OnTick_SELL_Open = False
        _s_OnTick_BUY_Close = False
        _s_OnTick_SELL_Close = False
        _s_OnTick_Recount = False
        if CopyBuffer(InpInd_Handle, 0, SignalBar, 2, Ind) <= 0:
            _s_OnTick_Recount = True
            return
        if CopyBuffer(InpInd_Handle, 1, SignalBar, 2, Sign) <= 0:
            _s_OnTick_Recount = True
            return
        if Ind[1] > Sign[1]:
            if BuyPosOpen and Ind[0] <= Sign[0]:
                _s_OnTick_BUY_Open = True
            if SellPosClose:
                _s_OnTick_SELL_Close = True
            _s_OnTick_UpSignalTime = SeriesInfoInteger(Symbol(), InpInd_Timeframe, SERIES_LASTBAR_DATE) + TimeShiftSec
        if Ind[1] < Sign[1]:
            if SellPosOpen and Ind[0] >= Sign[0]:
                _s_OnTick_SELL_Open = True
            if BuyPosClose:
                _s_OnTick_BUY_Close = True
            _s_OnTick_DnSignalTime = SeriesInfoInteger(Symbol(), InpInd_Timeframe, SERIES_LASTBAR_DATE) + TimeShiftSec
    BuyPositionClose(_GlobRef(globals(), '_s_OnTick_BUY_Close'), Symbol(), Deviation_)
    SellPositionClose(_GlobRef(globals(), '_s_OnTick_SELL_Close'), Symbol(), Deviation_)
    BuyPositionOpen_1(_GlobRef(globals(), '_s_OnTick_BUY_Open'), Symbol(), _s_OnTick_UpSignalTime, MM, MMMode, Deviation_, StopLoss_, TakeProfit_)
    SellPositionOpen_1(_GlobRef(globals(), '_s_OnTick_SELL_Open'), Symbol(), _s_OnTick_DnSignalTime, MM, MMMode, Deviation_, StopLoss_, TakeProfit_)

# ---- static local variables
_s_OnTick_Recount = True
_s_OnTick_BUY_Open = False
_s_OnTick_BUY_Close = False
_s_OnTick_SELL_Open = False
_s_OnTick_SELL_Close = False
_s_OnTick_UpSignalTime = 0
_s_OnTick_DnSignalTime = 0
_s_OnTick_NB = CIsNewBar()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ExpDigitmacd(_MQL5Indicator):
    name = 'exp_digitmacd'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MM': 0.1,  # Share of a deposit in a deal
        'MMMode': _Choice({0: 'MM от свободных средств на счёте', 1: 'MM от баланса средств на счёте', 2: 'MM по убыткам от свободных средств на счёте', 3: 'MM по убыткам от баланса средств на счёте', 4: 'Лот без изменения'}, default=4),  # Lot value calculation method
        'StopLoss_': 1000,  # Stop Loss in points
        'TakeProfit_': 2000,  # Take Profit in points
        'Deviation_': 10,  # Max. price deviation in points
        'BuyPosOpen': True,  # Permission to buy
        'SellPosOpen': True,  # Permission to sell
        'BuyPosClose': True,  # Permission to exit long positions
        'SellPosClose': True,  # Permission to exit short positions
        'InpInd_Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator timeframe
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Price constant
        'SignalBar': 1,  # Bar number for getting an entry signal
    }

