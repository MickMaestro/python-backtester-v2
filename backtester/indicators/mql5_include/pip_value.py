"""``FxWeirdos/pipValue.mqh`` (Mario Gharib, 2021) — port.

Pip size and pip-value arithmetic for stop-loss / take-profit / position
sizing. Symbol properties come from :func:`.mql4_compat.MarketInfoMQL4`
(digits and point from the dataset; tick value from the ``Rates`` spec,
``tick_value=``, 0 when unknown). The three percent-of-balance helpers read
``AccountInfoDouble(ACCOUNT_BALANCE)`` in MQL5; here the balance is an
argument (``balance``), since an offline chart has no trading account.
"""

from __future__ import annotations

from .mql4_compat import MODE_DIGITS, MODE_POINT, MODE_PROFITCALCMODE, MODE_TICKSIZE, \
    MODE_TICKVALUE, MarketInfoMQL4
from .mql_runtime import NormalizeDouble, fdiv


def dpipPos(sSymbol) -> float:
    if MarketInfoMQL4(sSymbol, MODE_PROFITCALCMODE) == 0:
        if MarketInfoMQL4(sSymbol, MODE_DIGITS) in (1, 3, 5):
            return MarketInfoMQL4(sSymbol, MODE_POINT) * 10
        return MarketInfoMQL4(sSymbol, MODE_POINT)
    return 1.0


def dNbPips(sSymbol, dPrice1, dPrice2) -> float:
    return NormalizeDouble(abs(fdiv(dPrice1 - dPrice2, dpipPos(sSymbol))), 5)


def _pip_value(sSymbol) -> float:
    return fdiv(MarketInfoMQL4(sSymbol, MODE_TICKVALUE) * dpipPos(sSymbol),
                MarketInfoMQL4(sSymbol, MODE_TICKSIZE))


def dValuePips(sSymbol, dPrice1, dPrice2, dVolume) -> float:
    return NormalizeDouble(dNbPips(sSymbol, dPrice1, dPrice2) * _pip_value(sSymbol) * dVolume, 2)


def _direction(iTradeType: int, buy: int, sell: int) -> int:
    if iTradeType in (0, 2, 4):
        return buy
    if iTradeType in (1, 3, 5):
        return sell
    return 1


def dPriceSL(sSymbol, dPrice, iTradeType, dnbPips) -> float:
    return NormalizeDouble(dPrice + _direction(iTradeType, -1, 1) * dnbPips * dpipPos(sSymbol), 5)


def dPriceTP(sSymbol, dPrice, iTradeType, dnbPips) -> float:
    return NormalizeDouble(dPrice + _direction(iTradeType, 1, -1) * dnbPips * dpipPos(sSymbol), 5)


def dPercentSL(sSymbol, dPrice, iTradeType, dVol, dPercent, *, balance: float) -> float:
    pip = dpipPos(sSymbol)
    pips = fdiv(balance * dPercent / 100, _pip_value(sSymbol) * dVol)
    if iTradeType in (0, 2, 4):
        return dPrice - pips * pip
    if iTradeType in (1, 3, 5):
        return dPrice + pips * pip
    return 0.0                                   # the source's return(false)


def dPercentTP(sSymbol, dPrice, iTradeType, dVol, dPercent, *, balance: float) -> float:
    pip = dpipPos(sSymbol)
    pips = fdiv(balance * dPercent / 100, _pip_value(sSymbol) * dVol)
    if iTradeType in (0, 2, 4):
        return dPrice + pips * pip
    if iTradeType in (1, 3, 5):
        return dPrice - pips * pip
    return 0.0


def dPercentVol(sSymbol, dPrice, dPriceSL_, dPercent, *, balance: float) -> float:
    return fdiv(balance * dPercent / 100, dNbPips(sSymbol, dPrice, dPriceSL_) * _pip_value(sSymbol))
