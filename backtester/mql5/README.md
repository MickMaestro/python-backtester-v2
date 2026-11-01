# backtester.mql5 — MQL5 → Python converter

Converts MetaTrader 5 custom indicators (`.mq5`) into indicator plugins for this
app. The output is ordinary Python that follows the MQL5 source statement by
statement, running on a small emulation of the MQL5 standard library.

```
lexer.py       tokens, #-directives, trailing comments (input/enum labels)
preprocess.py  #include / #define / #ifdef, #property collection
parser.py      recursive-descent parser -> nodes.py AST
translator.py  AST -> Python (types, references, overloads, classes, switch...)
convert.py     one .mq5 -> plugin module (metadata, inputs -> params, plots)
batch.py       convert a whole folder; test every result on synthetic bars
runtime.py     what generated code imports (rt_core, rt_term, rt_ind, rt_consts)
indicator.py   runs a converted program; MQL5Indicator plugin base class
```

## Running a converted indicator

`MQL5Indicator.calculate(df)` re-executes the module in a fresh namespace (so
globals and `static` locals start from their initial values, as when the
terminal loads an indicator), sets the inputs from the plugin parameters, calls
`OnInit()`, then `OnCalculate()` once over all bars with `prev_calculated = 0`
— exactly MetaTrader's first calculation. Indicator buffers are read back;
`EMPTY_VALUE` / `PLOT_EMPTY_VALUE`, bars before `PLOT_DRAW_BEGIN` and
non-finite values become NaN, `PLOT_SHIFT` is applied, and each MT5 plot is
mapped to the app's draw styles:

| MT5 | app |
|---|---|
| DRAW_LINE / SECTION / HISTOGRAM / ARROW / NONE | LINE / SECTION / HISTOGRAM / ARROW / NONE |
| DRAW_COLOR_LINE, _SECTION, _HISTOGRAM, _ARROW | one plot per colour (`p<k>_c<j>`), lines joined at colour changes |
| DRAW_FILLING | two FILL plots (`p<k>_up` where buffer1 ≥ buffer2, `p<k>_dn` otherwise) |
| DRAW_HISTOGRAM2 / COLOR_HISTOGRAM2 | HISTOGRAM2 (bars between the two buffers), per colour |
| DRAW_ZIGZAG / COLOR_ZIGZAG | ZIGZAG |
| DRAW_CANDLES / COLOR_CANDLES / BARS / COLOR_BARS | CANDLES (bars drawn as candles) |

Plot colours, widths, labels and arrow codes come from `#property` lines and
from the `PlotIndexSet*` calls `OnInit` makes.

## Conventions in generated code

* `Arr` — an MQL5 array. `ArraySetAsSeries(a, True)` flips indexing (0 = newest)
  without moving data. Index out of range raises `MqlRuntimeError`, which stops
  the indicator as in the terminal (the plugin then draws nothing and reports
  the error).
* `_idiv(a, b)` / `_imod(a, b)` — integer division / remainder truncating toward
  zero (C semantics); used when both operands are integer-typed.
* `_fdiv(a, b)` — double division giving ±inf/nan on division by zero.
* `_int(x)` (and `_uint`, `_long`, ...) — implicit or explicit conversion of a
  double to an integer type: truncation, with 32/64-bit wrap-around.
* `Box` — a scalar passed by reference (`double &x`): the callee reads and writes
  `x.v`. Callers pass a `Box` for locals, `_GlobRef`/`_AttrRef`/`_ElemRef` for
  globals, members and array elements.
* Structs and classes derive from `MqlObject`; assignment of struct values copies
  (`_assign`), pointers are plain references, `new` is a constructor call and
  `delete` calls the destructor (`_q_dtor`).
* Overloaded functions get suffixes (`Foo_1`, `Foo_2` or `Foo_<arity>`); calls
  are resolved at conversion time from argument count and types.
* `static` local variables become module globals named `_s_<function>_<name>`.
* `switch` becomes `if/elif`; a switch with fall-through uses an entry index and
  `_SwitchBreak`.
* `_DT(x)` marks a `datetime` argument of `CopyTime`/`CopyClose`/`CopyBuffer`…
  so the time-based overload is used even when the value is 0 (MQL5 picks the
  overload by type; Python cannot tell `datetime 0` from `int 0`).
* C `for` loops become `for … in range(…)` when the loop is a plain counter;
  otherwise `while` with the step repeated before every `continue`.

## What the runtime provides

Series access by symbol/timeframe (`Bars`, `iTime`…, `CopyRates`, `CopyClose`…,
`iBarShift`, `iHighest`…) on the chart's bars and on bars aggregated to any
higher timeframe (M1…MN1, weeks starting Sunday as in MT5); indicator handles
(`iMA`, `iRSI`, `iATR`, `iBands`, `iMACD`, `iStochastic`, `iADX`, `iSAR`,
`iCCI` … `iCustom`, `IndicatorCreate`) with `CopyBuffer`/`BarsCalculated`;
math, string, array, time and conversion functions; symbol/account info with
sensible values; chart objects kept in memory (`ObjectCreate`/`ObjectGet*`
work); arrows, horizontal/trend lines and rectangles are passed to the chart as
`obj_*` plots, other objects (labels, text, canvases, panels) are not drawn;
global variables; no-op alerts, sounds, mail, files.

`iCustom` runs another converted indicator, found by name in the
`_index.json` of the converted library (`python_indicators/mql5_codebase`
by default; `indicator.LIBRARY_DIRS` overrides it). Names are matched without
case, path or `.ex5`; Cyrillic look-alike letters (`JССX`) and a version suffix
(`CCI_withShift` -> `CCI_withShift_v1.01`) are tolerated. Results are cached per
data set. The built-in handles other than `iMA`,
`iWPR`, `iStochastic`, `iRVI`, `iChaikin`, `iBWMFI` run the converted
MetaQuotes example indicators (`rsi.mq5`, `atr.mq5`, `bb.mq5` ...), so their
values are the terminal sources' values.

Not available: DLL imports, trading, files, web requests, timers and chart
events (`OnTimer`/`OnChartEvent` are never called), other symbols than the
chart's.
