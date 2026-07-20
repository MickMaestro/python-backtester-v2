"""Headless backtest runner.

Examples:
    python run_backtest.py EURUSD H1
    python run_backtest.py EURUSD H1 --strategy ma_cross --param fast=12 --param slow=48
    python run_backtest.py XAUUSD M15 --strategy rsi_reversion --spread 20 --trades 10
"""

from __future__ import annotations

import argparse
import sys

from backtester.data.store import DataStore, StoreError
from backtester.engine.backtester import BacktestConfig, Backtester
from backtester.engine.instrument import InstrumentSpec
from backtester.engine.stats import format_stats
from backtester.strategy import loader


def _resolve_instrument(store: DataStore, args) -> InstrumentSpec:
    """Dataset's stored broker spec, patched by CLI overrides; forex default."""
    info = store.get(args.symbol, args.timeframe)
    point = args.point
    digits = args.digits
    contract = args.contract
    if info is not None:
        point = point if point is not None else info.point
        digits = digits if digits is not None else info.digits
        contract = contract if contract is not None else info.contract_size
    if point is None or contract is None:
        print(
            "note: no stored contract spec for this dataset (re-download it to "
            "capture one, or pass --point/--contract); assuming a 5-digit forex pair.",
            file=sys.stderr,
        )
        return InstrumentSpec.forex_major(args.symbol.upper())
    return InstrumentSpec.from_meta(
        args.symbol.upper(), point, digits if digits is not None else 5, contract
    )


def parse_param(text: str) -> tuple[str, object]:
    if "=" not in text:
        raise argparse.ArgumentTypeError(f"--param expects key=value, got {text!r}")
    key, raw = text.split("=", 1)
    try:
        value: object = int(raw)
    except ValueError:
        try:
            value = float(raw)
        except ValueError:
            value = raw
    return key.strip(), value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a backtest on stored data.")
    parser.add_argument("symbol")
    parser.add_argument("timeframe", help="M1, M5, M15, M30, H1, H4, D1, W1, MN1")
    parser.add_argument(
        "--strategy", default="ma_cross",
        help="built-in name or <file>.<Class> from the strategies/ folder",
    )
    parser.add_argument(
        "--intrabar", default=None, metavar="TF",
        help="finer stored timeframe of the same symbol for intrabar SL/TP "
             "resolution (e.g. M1)",
    )
    parser.add_argument(
        "--param", action="append", type=parse_param, default=[], metavar="KEY=VALUE",
        help="strategy parameter override (repeatable)",
    )
    parser.add_argument("--balance", type=float, default=10_000.0)
    parser.add_argument(
        "--spread", type=int, default=None, metavar="POINTS",
        help="fixed spread in points (default: use the data's spread column)",
    )
    parser.add_argument("--commission", type=float, default=0.0, metavar="PER_LOT_SIDE")
    parser.add_argument(
        "--trades", type=int, default=0, metavar="N", help="print the last N trades"
    )
    parser.add_argument(
        "--point", type=float, default=None,
        help="instrument point size override (default: from the dataset's stored spec)",
    )
    parser.add_argument("--digits", type=int, default=None)
    parser.add_argument("--contract", type=float, default=None, metavar="SIZE")
    args = parser.parse_args(argv)

    store = DataStore()
    try:
        df = store.load_bars(args.symbol, args.timeframe)
    except (StoreError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        available = ", ".join(i.key for i in store.datasets()) or "none"
        print(f"Available datasets: {available}", file=sys.stderr)
        return 1

    strategies, load_errors = loader.discover()
    for error in load_errors:
        print(f"warning: {error}", file=sys.stderr)
    if args.strategy not in strategies:
        print(
            f"error: unknown strategy {args.strategy!r}. "
            f"Available: {', '.join(sorted(strategies))}",
            file=sys.stderr,
        )
        return 1

    intrabar_df = None
    if args.intrabar:
        try:
            intrabar_df = store.load_bars(args.symbol, args.intrabar)
        except (StoreError, ValueError) as exc:
            print(f"error: intrabar data: {exc}", file=sys.stderr)
            return 1

    instrument = _resolve_instrument(store, args)
    strategy = strategies[args.strategy][0](**dict(args.param))
    config = BacktestConfig(
        initial_balance=args.balance,
        spread_points=args.spread,
        commission_per_lot=args.commission,
        instrument=instrument,
    )
    result = Backtester(df, strategy, config, intrabar_df=intrabar_df).run_all()

    print(f"\n{args.strategy} on {args.symbol} {args.timeframe} "
          f"({len(df):,} bars, {df['time'].iloc[0]} .. {df['time'].iloc[-1]})")
    print(f"Instrument: point={instrument.point} digits={instrument.digits} "
          f"contract={instrument.contract_size:,.0f} (1 pip = {instrument.pip})")
    print(f"Params: {vars(strategy.p)}\n")
    print(format_stats(result.stats))

    if args.trades and result.trades:
        print(f"\nLast {min(args.trades, len(result.trades))} trades:")
        for trade in result.trades[-args.trades:]:
            side = "buy " if trade.direction > 0 else "sell"
            print(
                f"  #{trade.id:<4} {side} {trade.lots:.2f}  "
                f"{trade.entry_time} @ {trade.entry_price:.5f} -> "
                f"{trade.exit_time} @ {trade.exit_price:.5f}  "
                f"net {trade.net:+,.2f}  ({trade.reason.value})"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
