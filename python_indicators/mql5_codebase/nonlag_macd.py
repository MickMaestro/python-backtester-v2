"""NonLag_MACD — converted from MQL5: MQL5 Indicators/NonLag_MACD/NonLag_MACD.mq5

Non lag MACD oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [3329330, 16748574, 255, 16711935, 11119017], 2: [16748574, 17919, 9470064]}, 'widths': {1: 8, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'NonLag MACD', 2: 'NL MACD Signal'}, 'levels': [], 'description': ['Non lag MACD oscillator'], 'name': 'NonLag_MACD', 'source': 'MQL5 Indicators/NonLag_MACD/NonLag_MACD.mq5', 'folder': 'NonLag_MACD', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 5, 'label': 'Fast NonLag period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 11, 'label': 'Slow NonLag period', 'sinput': False}, {'mql': 'InpPeriodSignal', 'py': 'InpPeriodSignal', 'param': 'InpPeriodSignal', 'type': 'uint', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpMethodFast', 'py': 'InpMethodFast', 'param': 'InpMethodFast', 'type': 'int', 'default': 0, 'label': 'Fast NonLag method', 'sinput': False}, {'mql': 'InpMethodSlow', 'py': 'InpMethodSlow', 'param': 'InpMethodSlow', 'type': 'int', 'default': 0, 'label': 'Slow NonLag method', 'sinput': False}, {'mql': 'InpMethodSignal', 'py': 'InpMethodSignal', 'param': 'InpMethodSignal', 'type': 'int', 'default': 0, 'label': 'Signal method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpFilter', 'py': 'InpFilter', 'param': 'InpFilter', 'type': 'uint', 'default': 0, 'label': 'Filter', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 0.0, 'label': 'Deviation (price)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 5)  # Fast NonLag period
InpPeriodSlow = _input('InpPeriodSlow', 11)  # Slow NonLag period
InpPeriodSignal = _input('InpPeriodSignal', 9)  # Signal period
InpMethodFast = _input('InpMethodFast', MODE_SMA)  # Fast NonLag method
InpMethodSlow = _input('InpMethodSlow', MODE_SMA)  # Slow NonLag method
InpMethodSignal = _input('InpMethodSignal', MODE_SMA)  # Signal method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpFilter = _input('InpFilter', 0)  # Filter
InpDeviation = _input('InpDeviation', 0.0)  # Deviation (price)
BufferMACD = Arr(0, 0.0)
BufferColorsMACD = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferColorsSignal = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferFNL = Arr(0, 0.0)
BufferSNL = Arr(0, 0.0)
deviation = 0.0
coeff = 0.0
phase_fast = 0.0
len_fast = 0.0
dt1_fast = 0.0
dt2_fast = 0.0
phase_slow = 0.0
len_slow = 0.0
dt1_slow = 0.0
dt2_slow = 0.0
kd = 0.0
filter_ = 0.0
period_fast = 0
period_slow = 0
period_sig = 0
handle_fma = 0
handle_sma = 0
period_max = 0
weight_sum = 0

def OnInit():
    global coeff, deviation, dt1_fast, dt1_slow, dt2_fast, dt2_slow, filter_, handle_fma, handle_sma, kd, len_fast, len_slow, period_fast, period_max, period_sig, period_slow, phase_fast, phase_slow
    period_fast = (3 if (InpPeriodFast < 3) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 3 if (InpPeriodSlow < 3) else InpPeriodSlow)
    period_sig = (2 if (InpPeriodSignal < 2) else InpPeriodSignal)
    deviation = InpDeviation
    filter_ = float(InpFilter) * Point()
    coeff = 3.0 * M_PI
    kd = 1.0 + (deviation / 100.0)
    phase_fast = period_fast - 1
    len_fast = (4.0 * period_fast) + phase_fast
    dt1_fast = _fdiv(7.0, (4.0 * period_fast) - 1.0)
    dt2_fast = _fdiv(1.0, phase_fast - 1.0)
    phase_slow = period_sig - 1
    len_slow = (4.0 * period_slow) + phase_slow
    dt1_slow = _fdiv(7.0, (4.0 * period_slow) - 1.0)
    dt2_slow = _fdiv(1.0, phase_slow - 1.0)
    period_max = _int(fmax(period_sig, fmax(len_fast + period_fast, len_slow + period_slow)))
    SetIndexBuffer(0, BufferMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColorsMACD, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColorsSignal, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferFNL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSNL, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Non lag MACD (' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_sig) + ',' + _str(InpFilter) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferColorsMACD, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferColorsSignal, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferFNL, True)
    ArraySetAsSeries(BufferSNL, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fast, 0, InpMethodFast, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA (', _str(period_fast), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_slow, 0, InpMethodSlow, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA (', _str(period_slow), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferMACD, 0)
        ArrayInitialize(BufferColorsMACD, 4)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferColorsSignal, 2)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferFNL, 0)
        ArrayInitialize(BufferSNL, 0)
    count = (rates_total if (limit > 0) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        NonLag(rates_total, i, _int(len_fast), dt1_fast, dt2_fast, BufferFMA, BufferFNL)
        NonLag(rates_total, i, _int(len_slow), dt1_slow, dt2_slow, BufferSMA, BufferSNL)
        BufferMACD[i] = BufferFNL[i] - BufferSNL[i]
        BufferColorsMACD[i] = ((0 if (BufferMACD[i] > BufferMACD[i + 1]) else 1 if (BufferMACD[i] < BufferMACD[i + 1]) else BufferColorsMACD[i + 1] if (filter_ > 0) else 4) if (BufferMACD[i] > 0) else (2 if (BufferMACD[i] < BufferMACD[i + 1]) else 3 if (BufferMACD[i] > BufferMACD[i + 1]) else BufferColorsMACD[i + 1] if (filter_ > 0) else 4) if (BufferMACD[i] < 0) else 4)
    _sw1 = InpMethodSignal
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferMACD, BufferSignal) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferMACD, BufferSignal) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sig, BufferMACD, BufferSignal, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferMACD, BufferSignal) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferColorsSignal[i] = (0 if (BufferSignal[i] > BufferSignal[i + 1]) else 1 if (BufferSignal[i] < BufferSignal[i + 1]) else 2)
    return rates_total

def NonLag(rates_total, shift, length, dt1, dt2, buffer_ma, buffer_nl):
    weight = 0.0
    sum_ = 0.0
    t = 0.0
    if (shift + length) > (rates_total - 1):
        return
    for j in range(0, length):
        g = _fdiv(1.0, (coeff * t) + 1)
        if t <= 0.5:
            g = 1.0
        beta = cos(M_PI * t)
        alpha = g * beta
        sum_ += alpha * buffer_ma[shift + j]
        weight += alpha
        if t < 1.0:
            t += dt2
        elif t < (length - 1):
            t = dt1
    if weight > 0:
        buffer_nl[shift] = _fdiv(kd * sum_, weight)
    if filter_ > 0 and fabs(buffer_nl[shift] - buffer_nl[shift + 1]) < filter_:
        buffer_nl[shift] = buffer_nl[shift + 1]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NonLagMACD(_MQL5Indicator):
    name = 'NonLag_MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 5,  # Fast NonLag period
        'InpPeriodSlow': 11,  # Slow NonLag period
        'InpPeriodSignal': 9,  # Signal period
        'InpMethodFast': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Fast NonLag method
        'InpMethodSlow': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Slow NonLag method
        'InpMethodSignal': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpFilter': 0,  # Filter
        'InpDeviation': 0.0,  # Deviation (price)
    }

