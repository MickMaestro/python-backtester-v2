"""Python ports of the MQL5 include libraries (``.mqh``) that the codebase
indicators ``#include``.

Each module is a faithful, line-by-line port: MQL class / function names and
signatures are kept, MQL5 semantics (C integer division, EMPTY_VALUE,
series indexing) come from :mod:`.mql_runtime`, and source bugs that change
the numbers are reproduced and documented in the module docstring. The full
file-by-file record is ``python_indicators/CONVERSION_LOG.txt``.

Runtime support
    mql_runtime        MQL5 language semantics (EMPTY_VALUE, idiv, fdiv, ...)
    terminal           bar data by symbol/timeframe (Copy*, iBarShift, ...)
    mql4_compat        Define/Enum/functions/MT4Bridge/DateTime/mymql helpers
    mql_error          MQL5Book/MqlError.mqh error table, E2S
    mql5book           MQL5Book TimeServerDST, StringUtils, MapArray, sorting...

Smoothing / math
    moving_averages    MT5 standard MovingAverages.mqh (SimpleMA..., *OnBuffer)
    smooth_algorithms  SmoothAlgorithms.mqh (+ identical SmoothAlgorithms45)
    indicators_algorithms  IndicatorsAlgorithms.mqh (LRMA, Vidya/BB bands)
    william_blau       WilliamBlau.mqh
    inc_on_ring_buffer IncOnRingBuffer/* (MA, EMA, DEMA, TEMA, AMA, RSI, ...)
    one_side_gaussian  OneSideGaussian.mqh + OneSideGaussianLibrary.mqh
    fast_frama         fastframa.mqh
    calc_frac          calcfrac.mqh
    dt_fft             dt_fft.mqh (ALGLIB FFT, DCT, DST)
    ssa                ssa.mqh
    caterpillar        SSA/CCaterpillar.mqh
    bpnn               BPNN_MQL.mqh + BPNN_MQL_IMPL.mqh (RPROP network)
    my_math            MyMath extremum / pattern classes

Bars / patterns / misc
    new_bar            libcisnewbar, onnewbarcalculate, CIsNewBar
    outside_bar        AlexSTAL_OutsideBar.mqh
    candlestick        Candlestick.mqh
    renko              RenkoCharts.mqh brick engine
    price_changes      fxsaber/PriceChanges
    aiv                AIV/Resources + AIV/Matrices
    metacot, metacot_enums  MetaCOT ToolBox / Enums / Version
    swisseph           swisseph.mqh (needs the ``pyswisseph`` package)
    pip_value          FxWeirdos/pipValue.mqh
    trade_algorithms   TradeAlgorithms.mqh non-order parts
    containers         HashMapTemplate, IndArray
    array_utils        ArrayUtils.mqh
    font_name          getfontname.mqh
"""
