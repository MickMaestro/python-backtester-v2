"""NonLag — converted from MQL5: MQL5 Indicators/NonLag/NonLag.mq5

Non lag average indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [32768, 255, 8421504]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'NonLag'}, 'levels': [], 'description': ['Non lag average indicator'], 'name': 'NonLag', 'source': 'MQL5 Indicators/NonLag/NonLag.mq5', 'folder': 'NonLag', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpFilter', 'py': 'InpFilter', 'param': 'InpFilter', 'type': 'uint', 'default': 0, 'label': 'Filter', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 0.0, 'label': 'Deviation (price)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpFilter = _input('InpFilter', 0)  # Filter
InpDeviation = _input('InpDeviation', 0.0)  # Deviation (price)
BufferNonLag = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
deviation = 0.0
coeff = 0.0
phase = 0.0
len_ = 0.0
dt1 = 0.0
dt2 = 0.0
kd = 0.0
filter_ = 0.0
period = 0
handle_ma = 0

def OnInit():
    global coeff, deviation, dt1, dt2, filter_, handle_ma, kd, len_, period, phase
    period = (3 if (InpPeriod < 3) else InpPeriod)
    deviation = InpDeviation
    coeff = 3.0 * M_PI
    phase = period - 1
    len_ = (4.0 * period) + phase
    dt1 = _fdiv(7.0, (4.0 * period) - 1.0)
    dt2 = _fdiv(1.0, phase - 1.0)
    kd = 1.0 + (deviation / 100.0)
    filter_ = float(InpFilter) * Point()
    SetIndexBuffer(0, BufferNonLag, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Non lag average (' + _str(period) + ',' + _str(InpFilter) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferNonLag, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA (', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(len_ + period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - _int(len_ + period) - 2
        ArrayInitialize(BufferNonLag, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 0) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        weight = 0.0
        sum_ = 0.0
        t = 0.0
        j = 0
        while j < len_:
            g = _fdiv(1.0, (coeff * t) + 1)
            if t <= 0.5:
                g = 1.0
            beta = cos(M_PI * t)
            alpha = g * beta
            sum_ += alpha * BufferMA[i + j]
            weight += alpha
            if t < 1.0:
                t += dt2
            elif t < (len_ - 1):
                t = dt1
            j += 1
        if weight > 0:
            BufferNonLag[i] = _fdiv(kd * sum_, weight)
        if filter_ > 0 and fabs(BufferNonLag[i] - BufferNonLag[i + 1]) < filter_:
            BufferNonLag[i] = BufferNonLag[i + 1]
        BufferColors[i] = (0 if ((BufferNonLag[i] - BufferNonLag[i + 1]) > filter_) else 1 if ((BufferNonLag[i + 1] - BufferNonLag[i]) > filter_) else BufferColors[i + 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NonLag(_MQL5Indicator):
    name = 'NonLag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpFilter': 0,  # Filter
        'InpDeviation': 0.0,  # Deviation (price)
    }

