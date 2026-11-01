"""Batch conversion of an MQL5 codebase folder with automated checks.

    python -m backtester.mql5.batch convert <src_root> <out_dir> --include <dir> [--include <dir>]
    python -m backtester.mql5.batch test <out_dir> [--jobs 2]

``convert`` writes one plugin module per ``.mq5`` plus ``_index.json`` (used by
``iCustom``) and ``_convert.json`` (per-file conversion results). ``test``
runs every module on synthetic bars and records ``_test.json``: whether it
computed, how long it took, whether it drew anything, and whether the values
on a shortened history equal the full-history values (no look-ahead).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import signal
import sys
import time
import traceback


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^0-9a-z\u0080-￿]+", "_", s).strip("_")
    s = re.sub(r"[^\w]", "_", s)
    if not s or s[0].isdigit():
        s = "i_" + s
    return s[:80]


def find_sources(root: str) -> list[str]:
    out = []
    for dp, _dn, fs in os.walk(root):
        for f in fs:
            if f.lower().endswith(".mq5"):
                out.append(os.path.join(dp, f))
    return sorted(out)


def _norm_hash(path):
    from .preprocess import read_source
    t = read_source(path)
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"//[^\n]*", "", t)
    return hashlib.md5(re.sub(r"\s+", "", t).encode()).hexdigest()


def cmd_convert(args):
    from .convert import Converter
    conv = Converter(args.include, lib_dir=args.libdir or None)
    os.makedirs(args.out, exist_ok=True)
    sources = []
    for root in args.src:
        base = os.path.dirname(os.path.abspath(root))
        for p in find_sources(root):
            sources.append((p, os.path.relpath(p, base)))
    if args.only:
        pat = re.compile(args.only, re.I)
        sources = [s for s in sources if pat.search(s[1])]
    results_path = os.path.join(args.out, "_convert.json")
    results = {}
    if os.path.exists(results_path) and args.only:
        results = json.load(open(results_path, encoding="utf-8"))
    used = {r["module"] for r in results.values() if r.get("module")}
    t0 = time.time()
    for k, (path, rel) in enumerate(sources):
        stem = os.path.splitext(os.path.basename(path))[0]
        folder = os.path.basename(os.path.dirname(path))
        prev = results.get(rel)
        slug = prev["module"][:-3] if prev and prev.get("module") else slugify(stem)
        if not prev or not prev.get("module"):
            if slug + ".py" in used:
                slug = f"{slug}__{slugify(folder)}"
            n = 2
            base_slug = slug
            while slug + ".py" in used:
                slug = f"{base_slug}_{n}"
                n += 1
        t = time.time()
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(120)
        try:
            r = conv.convert(path, rel.replace(os.sep, "/"), folder)
        except _Timeout:
            r = None
            err = "converter timeout (over 120 s)"
        except Exception as e:   # converter bug
            r = None
            err = f"converter crash: {type(e).__name__}: {e} | " + " / ".join(traceback.format_exc().splitlines()[-3:])
        signal.alarm(0)
        rec = {"source": rel.replace(os.sep, "/"), "folder": folder, "stem": stem, "hash": _norm_hash(path)}
        if r is not None and r.ok:
            mod = slug + ".py"
            with open(os.path.join(args.out, mod), "w", encoding="utf-8") as fh:
                fh.write(r.code)
            used.add(mod)
            rec.update({"module": mod, "class": r.class_name, "ok": True, "notes": r.notes,
                        "warnings": [f"line {ln}: {m}" for ln, m in r.report.warnings][:20],
                        "short_form": r.meta.get("short_form"), "plots": r.meta["props"].get("indicator_plots", 0),
                        "lines": r.code.count("\n")})
        else:
            rec.update({"module": None, "ok": False, "error": err if r is None else r.error})
        rec["convert_time"] = round(time.time() - t, 3)
        results[rel] = rec
        if (k + 1) % 100 == 0:
            print(f"{k + 1}/{len(sources)} converted, {time.time() - t0:.0f}s", flush=True)
            json.dump(results, open(results_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(results, open(results_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # index for iCustom
    index: dict[str, list] = {}
    for rec in results.values():
        if rec.get("module"):
            index.setdefault(rec["stem"].lower(), []).append(
                {"module": rec["module"], "source": rec["source"], "folder": rec["folder"]})
    json.dump(index, open(os.path.join(args.out, "_index.json"), "w", encoding="utf-8"), indent=0, ensure_ascii=False)
    ok = sum(1 for r in results.values() if r["ok"])
    print(f"converted {ok}/{len(results)} in {time.time() - t0:.0f}s")


# ------------------------------------------------------------------ testing

def synthetic_df(n=3000, seed=7, start="2024-01-01", freq="1h"):
    import numpy as np
    import pandas as pd
    rng = np.random.default_rng(seed)
    times = pd.date_range(start, periods=int(n * 1.5), freq=freq)
    times = times[times.dayofweek < 5][:n]
    close = 1.10 + rng.normal(0, 0.0012, n).cumsum() + 0.006 * np.sin(np.arange(n) / 60)
    open_ = np.r_[close[0], close[:-1]] + rng.normal(0, 0.00005, n)
    high = np.maximum(open_, close) + rng.uniform(0, 0.0012, n)
    low = np.minimum(open_, close) - rng.uniform(0, 0.0012, n)
    df = pd.DataFrame({"time": times, "open": open_.round(5), "high": high.round(5), "low": low.round(5),
                       "close": close.round(5), "tick_volume": rng.integers(100, 3000, n),
                       "spread": rng.integers(5, 20, n), "real_volume": rng.integers(1000, 30000, n)})
    df.attrs["symbol"] = "EURUSD"
    df.attrs["point"] = 0.00001
    df.attrs["digits"] = 5
    return df


class _Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise _Timeout()


def test_one(out_dir, rec, df, df_short, timeout=90):
    import numpy as np
    from backtester.indicators import loader
    from . import indicator as I
    I.LIBRARY_DIRS[:] = [out_dir]
    res = {"status": "ok"}
    path = os.path.join(out_dir, rec["module"])
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(timeout)
    try:
        t = time.time()
        classes = loader.load_indicators_from_file(path)
        res["load_time"] = round(time.time() - t, 3)
        if not classes:
            return {"status": "no_class"}
        cls = list(classes.values())[0]
        ind = cls()
        res["plots"] = len(ind.plots)
        t = time.time()
        full = ind.calculate(df)
        res["calc_time"] = round(time.time() - t, 3)
        err = getattr(ind, "last_error", None)
        if err:
            res["status"] = "runtime_error"
            res["error"] = err
            return res
        drawn = {k: int(np.isfinite(v).sum()) for k, v in full.items()}
        res["finite"] = drawn
        if not ind.plots:
            res["status"] = "no_plots"
        elif not any(drawn.values()):
            res["status"] = "empty"
        # look-ahead check
        n2 = len(df_short)
        part = ind.calculate(df_short)
        if getattr(ind, "last_error", None):
            res["short_error"] = ind.last_error
        diff = 0
        for k, v in part.items():
            if k not in full or k.startswith("obj_"):
                continue
            a = np.asarray(v, dtype=float)
            b = np.asarray(full[k][:n2], dtype=float)
            both = np.isfinite(a) & np.isfinite(b)
            mism = (np.isfinite(a) != np.isfinite(b)) | (both & ~np.isclose(a, b, rtol=1e-7, atol=1e-9))
            diff += int(mism.sum())
        res["lookahead_diffs"] = diff
    except _Timeout:
        res = {"status": "timeout"}
    except Exception as e:
        tb = traceback.format_exc().splitlines()
        loc = [ln for ln in tb if rec["module"] in ln]
        res = {"status": "exception", "error": f"{type(e).__name__}: {e}"[:300],
               "where": (loc[-1].strip() if loc else tb[-3].strip())[:200]}
    finally:
        signal.alarm(0)
    return res


_M5 = []


def _worker(args):
    out_dir, recs = args
    df = synthetic_df()
    df_short = df.iloc[:2000].reset_index(drop=True)
    df_short.attrs.update(df.attrs)
    out = {}
    for rel, rec in recs:
        res = test_one(out_dir, rec, df, df_short)
        if res.get("status") == "runtime_error" and str(res.get("error", "")).startswith("OnInit returned"):
            # e.g. multi-timeframe indicators whose lowest timeframe is below H1
            if not _M5:
                d5 = synthetic_df(freq="5min")
                s5 = d5.iloc[:2000].reset_index(drop=True)
                s5.attrs.update(d5.attrs)
                _M5.append((d5, s5))
            r5 = test_one(out_dir, rec, *_M5[0])
            if r5.get("status") != "runtime_error":
                r5["chart"] = "M5"
                r5["h1_error"] = res.get("error")
                res = r5
        out[rel] = res
    return out


def cmd_test(args):
    import multiprocessing as mp
    out_dir = args.out
    conv = json.load(open(os.path.join(out_dir, "_convert.json"), encoding="utf-8"))
    items = [(rel, rec) for rel, rec in conv.items() if rec.get("module")]
    if args.only:
        pat = re.compile(args.only, re.I)
        items = [it for it in items if pat.search(it[0])]
    if args.limit:
        step = max(1, len(items) // args.limit)
        items = items[::step][: args.limit]
    test_path = os.path.join(out_dir, "_test.json")
    results = json.load(open(test_path, encoding="utf-8")) if os.path.exists(test_path) else {}
    chunks = [items[i:i + 10] for i in range(0, len(items), 10)]
    t0 = time.time()
    done = 0
    with mp.Pool(args.jobs, maxtasksperchild=20) as pool:
        for res in pool.imap_unordered(_worker, [(out_dir, c) for c in chunks]):
            results.update(res)
            done += len(res)
            if done % 200 < 10:
                print(f"{done}/{len(items)} tested, {time.time() - t0:.0f}s", flush=True)
                json.dump(results, open(test_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(results, open(test_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    from collections import Counter
    c = Counter(results[rel]["status"] for rel, _ in items)
    print(dict(c), f"{time.time() - t0:.0f}s")


def cmd_finalize(args):
    """Mark indicators whose past values change with new bars (repaint_window),
    so the replay recomputes them on the revealed bars instead of leaking the future."""
    out_dir = args.out
    conv = json.load(open(os.path.join(out_dir, "_convert.json"), encoding="utf-8"))
    test = json.load(open(os.path.join(out_dir, "_test.json"), encoding="utf-8"))
    n = 0
    for rel, rec in conv.items():
        t = test.get(rel)
        if not rec.get("module") or not t:
            continue
        path = os.path.join(out_dir, rec["module"])
        src = open(path, encoding="utf-8").read()
        want = args.window if t.get("lookahead_diffs") else 0
        new = re.sub(r"\n    repaint_window = \d+", "", src)
        if want:
            new = new.replace("    meta = MQL5_META\n", f"    meta = MQL5_META\n    repaint_window = {want}\n", 1)
        if new != src:
            open(path, "w", encoding="utf-8").write(new)
            n += 1
    print(f"updated {n} modules")


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("convert")
    c.add_argument("src", nargs="+")
    c.add_argument("--out", required=True)
    c.add_argument("--include", action="append", default=[])
    c.add_argument("--only", default="")
    c.add_argument("--libdir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
    t = sub.add_parser("test")
    t.add_argument("out")
    t.add_argument("--jobs", type=int, default=2)
    t.add_argument("--only", default="")
    t.add_argument("--limit", type=int, default=0)
    f = sub.add_parser("finalize")
    f.add_argument("out")
    f.add_argument("--window", type=int, default=300)
    a = ap.parse_args(argv)
    if a.cmd == "convert":
        cmd_convert(a)
    elif a.cmd == "test":
        cmd_test(a)
    elif a.cmd == "finalize":
        cmd_finalize(a)
    else:
        ap.print_help()


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
