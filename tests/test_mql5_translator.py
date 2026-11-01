"""Tests for the MQL5 -> Python translator (backtester/mql5).

Each test writes a small MQL5 program, converts it, runs it on synthetic bars
with the emulated terminal and checks the buffers.  No corpus files needed.
"""

import os
import textwrap

import numpy as np
import pandas as pd
import pytest

from backtester.mql5 import indicator as I
from backtester.mql5.convert import Converter
from backtester.mql5.lexer import tokenize_line as tokenize

HEAD = """
#property indicator_separate_window
#property indicator_buffers 2
#property indicator_plots   2
double B0[], B1[];
"""
CALC = ("int OnCalculate(const int rates_total,const int prev_calculated,const datetime &time[],"
        "const double &open[],const double &high[],const double &low[],const double &close[],"
        "const long &tick_volume[],const long &volume[],const int &spread[])")


def bars(n=300, seed=1):
    rng = np.random.default_rng(seed)
    close = 1.1 + np.cumsum(rng.normal(0, 0.001, n))
    open_ = np.r_[close[0], close[:-1]]
    high = np.maximum(open_, close) + 0.0005
    low = np.minimum(open_, close) - 0.0005
    t = pd.date_range("2024-01-01", periods=n, freq="h")
    return pd.DataFrame({"time": t, "open": open_, "high": high, "low": low, "close": close,
                         "tick_volume": 100, "volume": 0, "spread": 1})


def run(tmp_path, body, inputs=None, n=300):
    src = tmp_path / "t.mq5"
    src.write_text(textwrap.dedent(HEAD + body), encoding="utf-8")
    conv = Converter([str(tmp_path)])
    r = conv.convert(str(src), "t")
    assert r.ok, r.error
    py = tmp_path / "t.py"
    py.write_text(r.code, encoding="utf-8")
    m, sym, per = I.market_from_df(bars(n))
    res = I.run_program(str(py), m, sym, per, inputs or {})
    assert res.ok, res.error
    return res, r.code


def test_lexer_keeps_datetime_and_color_literals():
    toks = [t.value for t in tokenize("datetime d=D'2020.01.02 03:04'; color c=C'255,0,0';")]
    assert any("2020" in str(v) or v == 1577934240 for v in toks)


def test_sma_and_integer_division(tmp_path):
    res, _ = run(tmp_path, f"""
    input int P=10;
    int OnInit() {{ SetIndexBuffer(0,B0); SetIndexBuffer(1,B1); return(0); }}
    {CALC}
    {{
       for(int i=0;i<rates_total;i++)
         {{
          B1[i]=7/2 + (-7)/2 + 7%3 + (-7)%3;     // C semantics: 3 + -3 + 1 + -1 = 0
          if(i<P-1) {{ B0[i]=EMPTY_VALUE; continue; }}
          double s=0; for(int k=0;k<P;k++) s+=close[i-k];
          B0[i]=s/P;
         }}
       return(rates_total);
    }}
    """)
    df = bars()
    ref = df["close"].rolling(10).mean().to_numpy()
    got = np.asarray(res.buffer(0), dtype=float)
    ok = np.isfinite(ref) & np.isfinite(got)
    assert ok.sum() > 250
    assert np.allclose(got[ok], ref[ok], atol=1e-12)
    assert np.all(np.asarray(res.buffer(1), dtype=float) == 0)


def test_series_indexing_static_and_struct_copy(tmp_path):
    res, code = run(tmp_path, f"""
    struct S {{ double v; int n; }};
    int Counter() {{ static int c=0; c++; return c; }}
    int OnInit() {{ SetIndexBuffer(0,B0); SetIndexBuffer(1,B1); ArraySetAsSeries(B0,true); return(0); }}
    {CALC}
    {{
       ArraySetAsSeries(close,true);
       S a; a.v=1.5; a.n=2;
       S b=a; b.v=9;                     // value copy: a unchanged
       for(int i=0;i<rates_total;i++) {{ B0[i]=close[i]; B1[i]=Counter() + a.v; }}
       return(rates_total);
    }}
    """)
    df = bars()
    assert np.allclose(np.asarray(res.buffer(0), dtype=float), df["close"].to_numpy())
    b1 = np.asarray(res.buffer(1), dtype=float)
    assert b1[0] == 2.5 and b1[-1] == len(df) + 1.5
    assert "_s_Counter_c" in code


def test_switch_fallthrough_and_ternary(tmp_path):
    res, _ = run(tmp_path, f"""
    int F(int x)
      {{
       int r=0;
       switch(x)
         {{
          case 0: r+=1;
          case 1: r+=10; break;
          case 2: r+=100; break;
          default: r=-1;
         }}
       return r;
      }}
    int OnInit() {{ SetIndexBuffer(0,B0); SetIndexBuffer(1,B1); return(0); }}
    {CALC}
    {{
       for(int i=0;i<rates_total;i++) {{ B0[i]=F(i%4); B1[i]=(i%2==0 ? 1 : i%3==0 ? 2 : 3); }}
       return(rates_total);
    }}
    """)
    assert list(np.asarray(res.buffer(0), dtype=float)[:4]) == [11, 10, 100, -1]
    assert list(np.asarray(res.buffer(1), dtype=float)[:4]) == [1, 3, 1, 2]


def test_copytime_with_datetime_zero_finds_no_bar(tmp_path):
    res, code = run(tmp_path, f"""
    int OnInit() {{ SetIndexBuffer(0,B0); SetIndexBuffer(1,B1); return(0); }}
    {CALC}
    {{
       datetime t0=0; datetime arr[];
       int got=CopyTime(Symbol(),PERIOD_CURRENT,t0,1,arr);   // time overload: nothing at 1970
       int pos=CopyTime(Symbol(),PERIOD_CURRENT,0,1,arr);    // position overload: newest bar
       for(int i=0;i<rates_total;i++) {{ B0[i]=got; B1[i]=pos; }}
       return(rates_total);
    }}
    """)
    assert "_DT(" in code
    assert np.asarray(res.buffer(0), dtype=float)[0] <= 0
    assert np.asarray(res.buffer(1), dtype=float)[0] == 1


def test_builtin_ima_handle_matches_sma(tmp_path):
    res, _ = run(tmp_path, f"""
    int h;
    int OnInit() {{ SetIndexBuffer(0,B0); SetIndexBuffer(1,B1); h=iMA(NULL,0,14,0,MODE_SMA,PRICE_CLOSE); return(0); }}
    {CALC}
    {{
       if(CopyBuffer(h,0,0,rates_total,B0)<=0) return(0);
       return(rates_total);
    }}
    """)
    ref = bars()["close"].rolling(14).mean().to_numpy()
    got = np.asarray(res.buffer(0), dtype=float)
    assert np.allclose(got[20:], ref[20:], atol=1e-12)


def test_input_override(tmp_path):
    res, _ = run(tmp_path, f"""
    input double K=1.0;
    int OnInit() {{ SetIndexBuffer(0,B0); SetIndexBuffer(1,B1); return(0); }}
    {CALC}
    {{ for(int i=0;i<rates_total;i++) B0[i]=K; return(rates_total); }}
    """, inputs={"K": 3.5})
    assert np.asarray(res.buffer(0), dtype=float)[5] == 3.5


@pytest.mark.skipif(not os.path.isdir(os.path.join(os.path.dirname(__file__), "..", "python_indicators",
                                                   "mql5_codebase")), reason="converted codebase not present")
def test_some_converted_plugins_load_and_run():
    from backtester.indicators import loader
    d = os.path.join(os.path.dirname(__file__), "..", "python_indicators", "mql5_codebase")
    I.LIBRARY_DIRS[:] = [d]
    df = bars(600)
    for name in ("hlbands.py",):
        p = os.path.join(d, name)
        if not os.path.exists(p):
            continue
        cls = list(loader.load_indicators_from_file(p).values())[0]
        out = cls().calculate(df)
        assert any(np.isfinite(np.asarray(v, dtype=float)).any() for v in out.values())
