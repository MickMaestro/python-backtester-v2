import numpy as np
import pandas as pd
import pytest

from backtester.data.store import DataStore, StoreError, normalize_bars


def make_bars(n: int = 100, start: str = "2024-01-01", freq: str = "1h") -> pd.DataFrame:
    times = pd.date_range(start, periods=n, freq=freq)
    base = np.linspace(1.10, 1.12, n)
    return pd.DataFrame(
        {
            "time": times,
            "open": base,
            "high": base + 0.001,
            "low": base - 0.001,
            "close": base + 0.0005,
            "tick_volume": np.arange(n) + 1,
            "spread": 2,
            "real_volume": 0,
        }
    )


@pytest.fixture
def store(tmp_path):
    return DataStore(tmp_path)


def test_save_and_load_roundtrip(store):
    df = make_bars(50)
    info = store.save_bars("eurusd", "H1", df)

    assert info.symbol == "EURUSD"
    assert info.timeframe == "H1"
    assert info.bars == 50

    loaded = store.load_bars("EURUSD", "H1")
    assert len(loaded) == 50
    assert list(loaded.columns) == list(df.columns)
    pd.testing.assert_series_equal(loaded["close"], df["close"])


def test_incremental_merge_dedupes_and_sorts(store):
    store.save_bars("EURUSD", "H1", make_bars(50, start="2024-01-01"))
    # Overlapping batch: starts 25 hours in, extends past the first batch.
    info = store.save_bars("EURUSD", "H1", make_bars(50, start="2024-01-02 01:00"))

    loaded = store.load_bars("EURUSD", "H1")
    assert info.bars == len(loaded) == 75  # 50 + 50 - 25 overlapping
    assert loaded["time"].is_monotonic_increasing
    assert not loaded["time"].duplicated().any()


def test_unix_seconds_time_accepted():
    df = make_bars(10)
    # Convert to unix seconds (like MT5) without assuming the dtype resolution.
    df["time"] = (df["time"] - pd.Timestamp("1970-01-01")) // pd.Timedelta(seconds=1)
    out = normalize_bars(df)
    assert out["time"].iloc[0] == pd.Timestamp("2024-01-01 00:00:00")


def test_csv_roundtrip(store, tmp_path):
    store.save_bars("GBPUSD", "M15", make_bars(30))
    csv_path = store.export_csv("GBPUSD", "M15", tmp_path / "out.csv")

    imported = store.import_csv(csv_path, "GBPJPY", "M15")
    assert imported.symbol == "GBPJPY"
    assert imported.bars == 30
    pd.testing.assert_frame_equal(
        store.load_bars("GBPJPY", "M15"), store.load_bars("GBPUSD", "M15")
    )


def test_mt5_style_csv_import(store, tmp_path):
    csv_path = tmp_path / "XAUUSD_D1.csv"
    csv_path.write_text(
        "<DATE>\t<TIME>\t<OPEN>\t<HIGH>\t<LOW>\t<CLOSE>\t<TICKVOL>\t<VOL>\t<SPREAD>\n"
        "2024.01.02\t00:00:00\t2064.5\t2088.2\t2062.9\t2077.6\t180943\t0\t23\n"
        "2024.01.03\t00:00:00\t2077.4\t2079.8\t2030.1\t2041.4\t195214\t0\t23\n",
        encoding="utf-8",
    )
    info = store.import_csv(csv_path, "XAUUSD", "D1")
    assert info.bars == 2

    loaded = store.load_bars("XAUUSD", "D1")
    assert loaded["time"].iloc[0] == pd.Timestamp("2024-01-02 00:00:00")
    assert loaded["close"].iloc[1] == pytest.approx(2041.4)
    assert loaded["tick_volume"].iloc[0] == 180943


def test_spec_persisted_and_preserved_on_merge(store):
    spec = {"point": 0.01, "digits": 2, "contract_size": 1.0}
    info = store.save_bars("GER40", "H1", make_bars(20), spec=spec)
    assert (info.point, info.digits, info.contract_size) == (0.01, 2, 1.0)

    # A later save without a spec (e.g. CSV append) keeps the stored one.
    info = store.save_bars("GER40", "H1", make_bars(10, start="2024-02-01"))
    assert (info.point, info.digits, info.contract_size) == (0.01, 2, 1.0)


def test_delete_removes_file_and_catalog(store):
    store.save_bars("EURUSD", "H1", make_bars(10))
    filename = store.get("EURUSD", "H1").filename
    assert (store.root / filename).exists()

    store.delete("EURUSD", "H1")
    assert store.get("EURUSD", "H1") is None
    assert not (store.root / filename).exists()
    assert store.datasets() == []


def test_missing_columns_rejected(store):
    bad = pd.DataFrame({"time": pd.date_range("2024-01-01", periods=3, freq="1h")})
    with pytest.raises(StoreError, match="missing required column"):
        store.save_bars("EURUSD", "H1", bad)


def test_unknown_timeframe_rejected(store):
    with pytest.raises(ValueError):
        store.save_bars("EURUSD", "H7", make_bars(5))


def test_load_missing_dataset_raises(store):
    with pytest.raises(StoreError, match="No dataset stored"):
        store.load_bars("USDJPY", "H1")
