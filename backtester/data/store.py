"""Local dataset library: Parquet storage with a JSON catalog and CSV import/export."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .models import BAR_COLUMNS, DatasetInfo, Timeframe

DEFAULT_ROOT = Path(__file__).resolve().parents[2] / "data_library"

_REQUIRED_COLUMNS = ["time", "open", "high", "low", "close"]
_OPTIONAL_DEFAULTS = {"tick_volume": 0, "spread": 0, "real_volume": 0}

# Header aliases seen in CSVs from MT5 exports and other common sources.
_COLUMN_ALIASES = {
    "datetime": "time",
    "timestamp": "time",
    "vol": "tick_volume",
    "volume": "tick_volume",
    "tickvol": "tick_volume",
}


class StoreError(Exception):
    """Raised when a dataset cannot be stored, loaded, or parsed."""


def normalize_bars(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce a raw bar frame to the canonical schema (see ``BAR_COLUMNS``).

    Accepts frames straight from the MetaTrader5 API (unix-second ``time``) as
    well as CSV imports with MT5-style ``<DATE>``/``<TIME>`` headers or common
    alias column names. Sorts by time and drops duplicate bars.
    """
    df = df.rename(columns={c: str(c).strip().strip("<>").lower() for c in df.columns})
    df = df.rename(columns=_COLUMN_ALIASES)
    # MT5 exports carry both <TICKVOL> and <VOL>, which alias to the same
    # canonical name — keep the first occurrence (tick volume).
    df = df.loc[:, ~df.columns.duplicated(keep="first")]

    # MT5 CSV exports split the timestamp into <DATE> and <TIME> columns.
    if "date" in df.columns and "time" in df.columns:
        df["time"] = pd.to_datetime(
            df["date"].astype(str) + " " + df["time"].astype(str), format="mixed"
        )
        df = df.drop(columns=["date"])

    missing = [c for c in _REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise StoreError(f"Bar data is missing required column(s): {', '.join(missing)}")

    if pd.api.types.is_numeric_dtype(df["time"]):
        df["time"] = pd.to_datetime(df["time"], unit="s")
    else:
        df["time"] = pd.to_datetime(df["time"], format="mixed")
    if getattr(df["time"].dt, "tz", None) is not None:
        df["time"] = df["time"].dt.tz_convert("UTC").dt.tz_localize(None)

    for column, default in _OPTIONAL_DEFAULTS.items():
        if column not in df.columns:
            df[column] = default

    for column in ("open", "high", "low", "close"):
        df[column] = pd.to_numeric(df[column], errors="coerce").astype("float64")
    for column in ("tick_volume", "spread", "real_volume"):
        df[column] = (
            pd.to_numeric(df[column], errors="coerce").fillna(0).astype("int64")
        )

    df = df.dropna(subset=_REQUIRED_COLUMNS)
    if df.empty:
        raise StoreError("Bar data is empty after cleaning.")

    df = (
        df.sort_values("time")
        .drop_duplicates(subset="time", keep="last")
        .reset_index(drop=True)
    )
    return df[BAR_COLUMNS]


class DataStore:
    """Parquet-backed library of bar datasets, indexed by ``catalog.json``."""

    def __init__(self, root: Path | str | None = None):
        self.root = Path(root) if root else DEFAULT_ROOT
        self.root.mkdir(parents=True, exist_ok=True)
        self._catalog_path = self.root / "catalog.json"

    # ------------------------------------------------------------- catalog

    def datasets(self) -> list[DatasetInfo]:
        catalog = self._read_catalog()
        return sorted(catalog.values(), key=lambda i: i.key)

    def get(self, symbol: str, timeframe: str) -> DatasetInfo | None:
        return self._read_catalog().get(self._key(symbol, timeframe))

    def size_bytes(self, info: DatasetInfo) -> int:
        path = self.root / info.filename
        return path.stat().st_size if path.exists() else 0

    # ------------------------------------------------------- save / load

    def save_bars(
        self,
        symbol: str,
        timeframe: str,
        df: pd.DataFrame,
        source: str = "MT5",
    ) -> DatasetInfo:
        """Normalize and store bars, merging with any existing dataset."""
        symbol = symbol.strip().upper()
        if not symbol:
            raise StoreError("Symbol name is empty.")
        tf = Timeframe(timeframe)
        df = normalize_bars(df)

        path = self.root / f"{symbol}_{tf.value}.parquet"
        if path.exists():
            existing = pd.read_parquet(path)
            df = normalize_bars(pd.concat([existing, df], ignore_index=True))
        df.to_parquet(path, index=False)

        info = DatasetInfo(
            symbol=symbol,
            timeframe=tf.value,
            start=str(df["time"].iloc[0]),
            end=str(df["time"].iloc[-1]),
            bars=len(df),
            source=source,
            saved_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            filename=path.name,
        )
        catalog = self._read_catalog()
        catalog[info.key] = info
        self._write_catalog(catalog)
        return info

    def load_bars(self, symbol: str, timeframe: str) -> pd.DataFrame:
        info = self.get(symbol, timeframe)
        if info is None:
            raise StoreError(f"No dataset stored for {symbol} {timeframe}.")
        path = self.root / info.filename
        if not path.exists():
            raise StoreError(f"Dataset file missing on disk: {path}")
        return pd.read_parquet(path)

    def delete(self, symbol: str, timeframe: str) -> None:
        catalog = self._read_catalog()
        info = catalog.pop(self._key(symbol, timeframe), None)
        if info is None:
            raise StoreError(f"No dataset stored for {symbol} {timeframe}.")
        (self.root / info.filename).unlink(missing_ok=True)
        self._write_catalog(catalog)

    # --------------------------------------------------------------- CSV

    def export_csv(self, symbol: str, timeframe: str, dest: Path | str) -> Path:
        df = self.load_bars(symbol, timeframe)
        dest = Path(dest)
        df.to_csv(dest, index=False)
        return dest

    def import_csv(self, path: Path | str, symbol: str, timeframe: str) -> DatasetInfo:
        path = Path(path)
        try:
            # sep=None sniffs the delimiter (MT5 exports are tab-separated).
            df = pd.read_csv(path, sep=None, engine="python")
        except Exception as exc:
            raise StoreError(f"Could not read CSV {path.name}: {exc}") from exc
        return self.save_bars(symbol, timeframe, df, source=f"CSV import ({path.name})")

    # ----------------------------------------------------------- helpers

    @staticmethod
    def _key(symbol: str, timeframe: str) -> str:
        return f"{symbol.strip().upper()}_{Timeframe(timeframe).value}"

    def _read_catalog(self) -> dict[str, DatasetInfo]:
        if not self._catalog_path.exists():
            return {}
        try:
            raw = json.loads(self._catalog_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise StoreError(f"Catalog file is unreadable: {exc}") from exc
        return {key: DatasetInfo.from_dict(value) for key, value in raw.items()}

    def _write_catalog(self, catalog: dict[str, DatasetInfo]) -> None:
        payload = {key: info.to_dict() for key, info in catalog.items()}
        self._catalog_path.write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )
