"""``TradeAlgorithms.mqh`` (Nikolay Kositsin, 2013, v1.50) and its older copy
``tradealgorithms_.mqh`` — port of the non-trading parts.

The library is the order layer of Kositsin's ``Exp_*`` Expert Advisors:
``BuyPositionOpen``/``SellPositionOpen``/``…Close``/``…Modify`` (and the
``_M``/``_X``/``Re…`` variants) send orders through ``OrderSend`` against a
live or tester account. Those have no meaning inside an indicator; an EA
converted for this app places orders through the backtester's
:class:`backtester.strategy.base.Strategy` API instead, so they are not
ported here (the conversion log lists them).

Ported: the enums (``MarginMode``, ``HOURS``, ``MINUTS``), ``CIsNewBar``
(:mod:`.new_bar`), the time-level bookkeeping that blocks re-entry until a
given time (terminal *global variables* → a module dict), stop/lot
corrections against the symbol's limits, ``GetSymbolByCurrencies`` and
``ResultRetcodeDescription`` (the source's Russian texts, plus an English
rendering with ``english=True``).
"""

from __future__ import annotations

import math

from . import terminal as T
from .mql_runtime import NormalizeDouble
from .new_bar import CIsNewBar  # noqa: F401 — part of this include

# enum MarginMode
FREEMARGIN, BALANCE, LOSSFREEMARGIN, LOSSBALANCE, LOT = range(5)
# enum HOURS / MINUTS
for _h in range(24):
    globals()[f"ENUM_HOUR_{_h}"] = _h
for _m in range(60):
    globals()[f"ENUM_MINUT_{_m}"] = _m

POSITION_TYPE_BUY, POSITION_TYPE_SELL = 0, 1

TRADE_RETCODE_REQUOTE = 10004
TRADE_RETCODE_REJECT = 10006
TRADE_RETCODE_CANCEL = 10007
TRADE_RETCODE_PLACED = 10008
TRADE_RETCODE_DONE = 10009
TRADE_RETCODE_DONE_PARTIAL = 10010
TRADE_RETCODE_ERROR = 10011
TRADE_RETCODE_TIMEOUT = 10012
TRADE_RETCODE_INVALID = 10013
TRADE_RETCODE_INVALID_VOLUME = 10014
TRADE_RETCODE_INVALID_PRICE = 10015
TRADE_RETCODE_INVALID_STOPS = 10016
TRADE_RETCODE_TRADE_DISABLED = 10017
TRADE_RETCODE_MARKET_CLOSED = 10018
TRADE_RETCODE_NO_MONEY = 10019
TRADE_RETCODE_PRICE_CHANGED = 10020
TRADE_RETCODE_PRICE_OFF = 10021
TRADE_RETCODE_INVALID_EXPIRATION = 10022
TRADE_RETCODE_ORDER_CHANGED = 10023
TRADE_RETCODE_TOO_MANY_REQUESTS = 10024
TRADE_RETCODE_NO_CHANGES = 10025
TRADE_RETCODE_SERVER_DISABLES_AT = 10026
TRADE_RETCODE_CLIENT_DISABLES_AT = 10027
TRADE_RETCODE_LOCKED = 10028
TRADE_RETCODE_FROZEN = 10029
TRADE_RETCODE_INVALID_FILL = 10030
TRADE_RETCODE_CONNECTION = 10031
TRADE_RETCODE_ONLY_REAL = 10032
TRADE_RETCODE_LIMIT_ORDERS = 10033
TRADE_RETCODE_LIMIT_VOLUME = 10034
TRADE_RETCODE_INVALID_ORDER = 10035
TRADE_RETCODE_POSITION_CLOSED = 10036
TRADE_RETCODE_INVALID_CLOSE_VOLUME = 10038
TRADE_RETCODE_CLOSE_ORDER_EXIST = 10039
TRADE_RETCODE_LIMIT_POSITIONS = 10040

_RETCODE_TEXT_RU = {
    TRADE_RETCODE_REQUOTE: 'Реквота',
    TRADE_RETCODE_REJECT: 'Запрос отвергнут',
    TRADE_RETCODE_CANCEL: 'Запрос отменен трейдером',
    TRADE_RETCODE_PLACED: 'Ордер размещен',
    TRADE_RETCODE_DONE: 'Заявка выполнена',
    TRADE_RETCODE_DONE_PARTIAL: 'Заявка выполнена частично',
    TRADE_RETCODE_ERROR: 'Ошибка обработки запроса',
    TRADE_RETCODE_TIMEOUT: 'Запрос отменен по истечению времени',
    TRADE_RETCODE_INVALID: 'Неправильный запрос',
    TRADE_RETCODE_INVALID_VOLUME: 'Неправильный объем в запросе',
    TRADE_RETCODE_INVALID_PRICE: 'Неправильная цена в запросе',
    TRADE_RETCODE_INVALID_STOPS: 'Неправильные стопы в запросе',
    TRADE_RETCODE_TRADE_DISABLED: 'Торговля запрещена',
    TRADE_RETCODE_MARKET_CLOSED: 'Рынок закрыт',
    TRADE_RETCODE_NO_MONEY: 'Нет достаточных денежных средств для выполнения запроса',
    TRADE_RETCODE_PRICE_CHANGED: 'Цены изменились',
    TRADE_RETCODE_PRICE_OFF: 'Отсутствуют котировки для обработки запроса',
    TRADE_RETCODE_INVALID_EXPIRATION: 'Неверная дата истечения ордера в запросе',
    TRADE_RETCODE_ORDER_CHANGED: 'Состояние ордера изменилось',
    TRADE_RETCODE_TOO_MANY_REQUESTS: 'Слишком частые запросы',
    TRADE_RETCODE_NO_CHANGES: 'В запросе нет изменений',
    TRADE_RETCODE_SERVER_DISABLES_AT: 'Автотрейдинг запрещен сервером',
    TRADE_RETCODE_CLIENT_DISABLES_AT: 'Автотрейдинг запрещен клиентским терминалом',
    TRADE_RETCODE_LOCKED: 'Запрос заблокирован для обработки',
    TRADE_RETCODE_FROZEN: 'Ордер или позиция заморожены',
    TRADE_RETCODE_INVALID_FILL: 'Указан неподдерживаемый тип исполнения ордера по остатку',
    TRADE_RETCODE_CONNECTION: 'Нет соединения с торговым сервером',
    TRADE_RETCODE_ONLY_REAL: 'Операция разрешена только для реальных счетов',
    TRADE_RETCODE_LIMIT_ORDERS: 'Достигнут лимит на количество отложенных ордеров',
    TRADE_RETCODE_LIMIT_VOLUME: 'Достигнут лимит на объем ордеров и позиций для данного символа',
    TRADE_RETCODE_INVALID_ORDER: 'Неверный или запрещённый тип ордера',
    TRADE_RETCODE_POSITION_CLOSED: 'Позиция с указанным POSITION_IDENTIFIER уже закрыта',
    TRADE_RETCODE_INVALID_CLOSE_VOLUME: 'Закрываемый объем превышает текущий объем позиции',
    TRADE_RETCODE_CLOSE_ORDER_EXIST: 'Для указанной позиции уже есть ордер на закрытие',
    TRADE_RETCODE_LIMIT_POSITIONS: 'Количество открытых позиций, которое можно одновременно иметь на счете, может быть ограничено настройками сервера',
}

_RETCODE_TEXT_EN = {
    TRADE_RETCODE_REQUOTE: "Requote", TRADE_RETCODE_REJECT: "Request rejected",
    TRADE_RETCODE_CANCEL: "Request canceled by trader", TRADE_RETCODE_PLACED: "Order placed",
    TRADE_RETCODE_DONE: "Request completed", TRADE_RETCODE_DONE_PARTIAL: "Only part of the request was completed",
    TRADE_RETCODE_ERROR: "Request processing error", TRADE_RETCODE_TIMEOUT: "Request canceled by timeout",
    TRADE_RETCODE_INVALID: "Invalid request", TRADE_RETCODE_INVALID_VOLUME: "Invalid volume in the request",
    TRADE_RETCODE_INVALID_PRICE: "Invalid price in the request",
    TRADE_RETCODE_INVALID_STOPS: "Invalid stops in the request",
    TRADE_RETCODE_TRADE_DISABLED: "Trade is disabled", TRADE_RETCODE_MARKET_CLOSED: "Market is closed",
    TRADE_RETCODE_NO_MONEY: "There is not enough money to complete the request",
    TRADE_RETCODE_PRICE_CHANGED: "Prices changed",
    TRADE_RETCODE_PRICE_OFF: "There are no quotes to process the request",
    TRADE_RETCODE_INVALID_EXPIRATION: "Invalid order expiration date in the request",
    TRADE_RETCODE_ORDER_CHANGED: "Order state changed", TRADE_RETCODE_TOO_MANY_REQUESTS: "Too frequent requests",
    TRADE_RETCODE_NO_CHANGES: "No changes in request",
    TRADE_RETCODE_SERVER_DISABLES_AT: "Autotrading disabled by server",
    TRADE_RETCODE_CLIENT_DISABLES_AT: "Autotrading disabled by client terminal",
    TRADE_RETCODE_LOCKED: "Request locked for processing", TRADE_RETCODE_FROZEN: "Order or position frozen",
    TRADE_RETCODE_INVALID_FILL: "Invalid order filling type",
    TRADE_RETCODE_CONNECTION: "No connection with the trade server",
    TRADE_RETCODE_ONLY_REAL: "Operation is allowed only for live accounts",
    TRADE_RETCODE_LIMIT_ORDERS: "The number of pending orders has reached the limit",
    TRADE_RETCODE_LIMIT_VOLUME: "The volume of orders and positions for the symbol has reached the limit",
    TRADE_RETCODE_INVALID_ORDER: "Incorrect or prohibited order type",
    TRADE_RETCODE_POSITION_CLOSED: "Position with the specified POSITION_IDENTIFIER has already been closed",
    TRADE_RETCODE_INVALID_CLOSE_VOLUME: "A close volume exceeds the current position volume",
    TRADE_RETCODE_CLOSE_ORDER_EXIST: "A close order already exists for the specified position",
    TRADE_RETCODE_LIMIT_POSITIONS: "The number of open positions has reached the server's limit",
}


def ResultRetcodeDescription(retcode: int, english: bool = False) -> str:
    table = _RETCODE_TEXT_EN if english else _RETCODE_TEXT_RU
    return table.get(int(retcode), "Unknown result" if english else "Неизвестный результат")


# ------------------------------------------------------- time levels

#: Stand-in for the terminal's global variables.
GLOBAL_VARIABLES: dict[str, float] = {}
ACCOUNT_LOGIN = 0
TESTING = True          # offline is always the tester's situation


def _now() -> int:
    chart = T.current().chart
    return int(chart.time[-1]) if chart is not None and len(chart) else 0


def GetTimeLevelName(symbol: str, trade_operation: int) -> str:
    name = f"TimeLevel_{ACCOUNT_LOGIN}_{symbol}_{trade_operation}"
    return name + "_Test_" if TESTING else name


def TradeTimeLevelCheck(symbol, trade_operation, TradeTimeLevel) -> bool:
    if TradeTimeLevel > 0:
        if _now() < GLOBAL_VARIABLES.get(GetTimeLevelName(symbol, trade_operation), 0):
            return False
    return True


def TradeTimeLevelSet(symbol, trade_operation, TradeTimeLevel) -> None:
    GLOBAL_VARIABLES[GetTimeLevelName(symbol, trade_operation)] = TradeTimeLevel


def TradeTimeLevelGet(symbol, trade_operation) -> int:
    return int(GLOBAL_VARIABLES.get(GetTimeLevelName(symbol, trade_operation), 0))


def TimeLevelGlobalVariableDel(symbol, trade_operation) -> None:
    if TESTING:
        GLOBAL_VARIABLES.pop(GetTimeLevelName(symbol, trade_operation), None)


def GlobalVariableDel_(symbol) -> None:
    TimeLevelGlobalVariableDel(symbol, POSITION_TYPE_BUY)
    TimeLevelGlobalVariableDel(symbol, POSITION_TYPE_SELL)


def GetTimeLevelNameM(symbol, trade_operation, magic) -> str:
    name = f"TimeLevelM_{ACCOUNT_LOGIN}_{symbol}_{trade_operation}_{magic}"
    return name + "_Test_" if TESTING else name


def TradeTimeLevelCheckM(symbol, trade_operation, TradeTimeLevel, magic) -> bool:
    if TradeTimeLevel > 0:
        if _now() < GLOBAL_VARIABLES.get(GetTimeLevelNameM(symbol, trade_operation, magic), 0):
            return False
    return True


def TradeTimeLevelSetM(symbol, trade_operation, TradeTimeLevel, magic) -> None:
    GLOBAL_VARIABLES[GetTimeLevelNameM(symbol, trade_operation, magic)] = TradeTimeLevel


def TimeLevelGlobalVariableDelM(symbol, trade_operation, magic) -> None:
    if TESTING:
        GLOBAL_VARIABLES.pop(GetTimeLevelNameM(symbol, trade_operation, magic), None)


def GlobalVariableDel_M(symbol, magic) -> None:
    TimeLevelGlobalVariableDelM(symbol, POSITION_TYPE_BUY, magic)
    TimeLevelGlobalVariableDelM(symbol, POSITION_TYPE_SELL, magic)


#: ``tradealgorithms_.mqh`` (the older copy) names it with a trailing underscore.
ResultRetcodeDescription_ = None  # set below


# ------------------------------------------------------- corrections


def StopCorrect(symbol, Stop: int):
    """→ ``(ok, Stop)`` raised to the symbol's stops level (spec
    ``stops_level``, 0 when unknown)."""
    r = T.rates_for(symbol)
    if r is None:
        return False, Stop
    level = int(r.spec.get("stops_level", 0))
    return True, max(int(Stop), level)


def dStopCorrect(symbol, dStopLoss: float, dTakeprofit: float, trade_operation: int):
    """→ ``(ok, dStopLoss, dTakeprofit)`` pushed outside the stops level
    around the current Ask/Bid (the latest close offline)."""
    if not dStopLoss and not dTakeprofit:
        return True, dStopLoss, dTakeprofit
    if dStopLoss < 0 or dTakeprofit < 0:
        return False, dStopLoss, dTakeprofit
    ok, Stop = StopCorrect(symbol, 0)
    r = T.rates_for(symbol)
    if not ok or r is None:
        return False, dStopLoss, dTakeprofit
    digit = r.SymbolInfoInteger(T.SYMBOL_DIGITS)
    dStop = Stop * r.SymbolInfoDouble(T.SYMBOL_POINT)
    price = r.SymbolInfoDouble(T.SYMBOL_ASK if trade_operation == POSITION_TYPE_BUY else T.SYMBOL_BID)
    if trade_operation == POSITION_TYPE_BUY:
        ExtrStop = NormalizeDouble(price - dStop, digit)
        ExtrTake = NormalizeDouble(price + dStop, digit)
        if dStopLoss > ExtrStop and dStopLoss:
            dStopLoss = ExtrStop
        if dTakeprofit < ExtrTake and dTakeprofit:
            dTakeprofit = ExtrTake
    if trade_operation == POSITION_TYPE_SELL:
        ExtrStop = NormalizeDouble(price + dStop, digit)
        ExtrTake = NormalizeDouble(price - dStop, digit)
        if dStopLoss < ExtrStop and dStopLoss:
            dStopLoss = ExtrStop
        if dTakeprofit > ExtrTake and dTakeprofit:
            dTakeprofit = ExtrTake
    return True, dStopLoss, dTakeprofit


def LotCorrect(symbol, Lot: float, trade_operation: int):
    """→ ``(ok, Lot)`` snapped to the volume step and clamped to min/max
    (spec ``volume_step``/``volume_min``/``volume_max``). The source's
    free-margin check (``LotFreeMarginCorrect``) needs an account and is
    skipped."""
    r = T.rates_for(symbol)
    if r is None:
        return False, Lot
    step = float(r.spec.get("volume_step", 0.01))
    mn = float(r.spec.get("volume_min", 0.01))
    mx = float(r.spec.get("volume_max", 100.0))
    Lot = step * math.floor(Lot / step)
    Lot = max(Lot, mn)
    Lot = min(Lot, mx)
    return True, Lot


def GetSymbolByCurrencies(margin_currency: str, profit_currency: str):
    for (sym, _per), r in T.current()._rates.items():
        if (r.spec.get("currency_margin") == margin_currency
                and r.spec.get("currency_profit") == profit_currency):
            return sym
    return None


ResultRetcodeDescription_ = ResultRetcodeDescription
