"""Instrument contract specifications used for price and PnL arithmetic."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InstrumentSpec:
    """Contract math for one instrument.

    PnL is computed in the *quote* currency; the simulation assumes the
    account currency equals the quote currency (e.g. a USD account trading
    EURUSD). Cross-currency conversion is a later-phase feature.
    """

    symbol: str = "FX"
    digits: int = 5
    point: float = 1e-5        # smallest price increment (MT5 "point")
    pip: float = 1e-4          # conventional pip (10 points on 5-digit pairs)
    contract_size: float = 100_000.0  # units of base currency per 1.0 lot

    @classmethod
    def forex_major(cls, symbol: str = "FX") -> "InstrumentSpec":
        """5-digit non-JPY forex pair (EURUSD, GBPUSD, ...)."""
        return cls(symbol=symbol)

    @classmethod
    def forex_jpy(cls, symbol: str = "FX") -> "InstrumentSpec":
        """3-digit JPY pair (USDJPY, EURJPY, ...)."""
        return cls(symbol=symbol, digits=3, point=1e-3, pip=1e-2)

    @classmethod
    def from_meta(
        cls, symbol: str, point: float, digits: int, contract_size: float
    ) -> "InstrumentSpec":
        """Build from broker metadata (MT5 symbol_info). Pip = 10 points by
        convention; for non-forex instruments *_pips arguments are therefore
        denominated in tens of points."""
        return cls(
            symbol=symbol, digits=int(digits), point=float(point),
            pip=float(point) * 10, contract_size=float(contract_size),
        )
