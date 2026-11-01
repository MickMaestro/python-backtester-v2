"""Lyapunov_HP — converted from MQL5: MQL5 Indicators/Lyapunov_HP/Lyapunov_HP.mq5

Lyapunov HP oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'HP'}, 'levels': [], 'description': ['Lyapunov HP oscillator'], 'name': 'Lyapunov_HP', 'source': 'MQL5 Indicators/Lyapunov_HP/Lyapunov_HP.mq5', 'folder': 'Lyapunov_HP', 'inputs': [{'mql': 'InpFilter', 'py': 'InpFilter', 'param': 'InpFilter', 'type': 'uint', 'default': 7, 'label': 'Filter', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFilter = _input('InpFilter', 7)  # Filter
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferHP = Arr(0, 0.0)
BufferH = Arr(0, 0.0)
BufferA = Arr(0, 0.0)
BufferB = Arr(0, 0.0)
BufferC = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
filter_ = 0
handle_ma = 0
lambda_ = 0.0

def OnInit():
    global filter_, handle_ma, lambda_
    filter_ = (2 if (InpFilter < 2) else InpFilter)
    lambda_ = _fdiv(0.0625, pow(sin(_fdiv(M_PI, filter_)), 4))
    SetIndexBuffer(0, BufferHP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferB, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LHPosc(' + _str(filter_) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferHP, True)
    ArraySetAsSeries(BufferH, True)
    ArraySetAsSeries(BufferA, True)
    ArraySetAsSeries(BufferB, True)
    ArraySetAsSeries(BufferC, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    limit = rates_total - prev_calculated
    limit1 = rates_total - 2
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferHP, EMPTY_VALUE)
        ArrayInitialize(BufferH, 0)
        ArrayInitialize(BufferA, (6 * lambda_) + 1)
        ArrayInitialize(BufferB, -4 * lambda_)
        ArrayInitialize(BufferC, lambda_)
        ArrayInitialize(BufferMA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    BufferA[0] = 1 + lambda_
    BufferB[0] = -2 * lambda_
    BufferC[0] = lambda_
    for i in range(limit1, 0, -1):
        BufferA[i] = (6 * lambda_) + 1
        BufferB[i] = -4 * lambda_
        BufferC[i] = lambda_
    BufferA[1] = (5 * lambda_) + 1
    BufferA[limit1] = 1 + lambda_
    BufferA[limit1 - 1] = (5 * lambda_) + 1
    BufferB[limit1 - 1] = -2 * lambda_
    BufferB[limit1] = 0.0
    BufferC[limit1 - 1] = 0.0
    BufferC[limit1] = 0.0
    H1 = 0.0
    H2 = 0.0
    H3 = 0.0
    H4 = 0.0
    H5 = 0.0
    HH1 = 0.0
    HH2 = 0.0
    HH3 = 0.0
    HH4 = 0.0
    HH5 = 0.0
    HB = 0.0
    HC = 0.0
    Z = 0.0
    for i in range(0, limit1 + 1):
        Z = BufferA[i] - (H4 * H1) - (HH5 * HH2)
        HB = BufferB[i]
        HH1 = H1
        H1 = _fdiv(HB - (H4 * H2), (Z if (Z != 0) else DBL_MIN))
        BufferB[i] = H1
        HC = BufferC[i]
        HH2 = H2
        H2 = _fdiv(HC, (Z if (Z != 0) else DBL_MIN))
        BufferC[i] = H2
        BufferA[i] = _fdiv(BufferMA[i] - (HH3 * HH5) - (H3 * H4), (Z if (Z != 0) else DBL_MIN))
        HH3 = H3
        H3 = BufferA[i]
        H4 = HB - (H5 * HH1)
        HH5 = H5
        H5 = HC
    H2 = 0.0
    H1 = BufferA[limit1 - 1]
    BufferH[limit1 - 1] = H1
    for i in range(limit1 - 2, 0 - 1, -1):
        BufferH[i] = BufferA[i] - (BufferB[i] * H1) - (BufferC[i] * H2)
        H2 = H1
        H1 = BufferH[i]
    for i in range(0, limit1 - 2):
        v = BufferH[i + 1]
        BufferHP[i] = MathLog(MathAbs(_fdiv(BufferH[i], (v if (v != 0) else DBL_MIN)))) * 100000
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LyapunovHP(_MQL5Indicator):
    name = 'Lyapunov_HP'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpFilter': 7,  # Filter
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

