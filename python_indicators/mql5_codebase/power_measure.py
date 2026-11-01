"""Power_Measure — converted from MQL5: MQL5 Indicators/Power_Measure/Power_Measure.mq5

Power measure oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2237106]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'PM'}, 'levels': [], 'description': ['Power measure oscillator'], 'name': 'Power_Measure', 'source': 'MQL5 Indicators/Power_Measure/Power_Measure.mq5', 'folder': 'Power_Measure', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
BufferPM = Arr(0, 0.0)
BufferCC = Arr(0, 0.0)
BufferHL = Arr(0, 0.0)
period_ma = 0

def OnInit():
    global period_ma
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferPM, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferHL, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Power measure (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPM, True)
    ArraySetAsSeries(BufferCC, True)
    ArraySetAsSeries(BufferHL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 2
        ArrayInitialize(BufferPM, EMPTY_VALUE)
        ArrayInitialize(BufferCC, 0)
        ArrayInitialize(BufferHL, 0)
    for i in range(limit, 0 - 1, -1):
        BufferCC[i] = _fdiv(100.0 * (close[i] - close[i + 1]), (close[i + 1] if (close[i + 1] != 0) else 1.0))
        BufferHL[i] = _fdiv(100.0 * (high[i] - low[i + 1]), (low[i + 1] if (low[i + 1] != 0) else 1.0))
    for i in range(limit, 0 - 1, -1):
        ma_cc = GetSMA(rates_total, i, period_ma, BufferCC)
        ma_hl = GetSMA(rates_total, i, period_ma, BufferHL)
        sum_ = 0.0
        sum_cc2 = 0.0
        sum_hl2 = 0.0
        for j in range(0, period_ma):
            sum_ += (BufferCC[i + j] - ma_cc) * (BufferHL[i + j] - ma_hl)
            sum_cc2 += (BufferCC[i + j] - ma_cc) * (BufferCC[i + j] - ma_cc)
            sum_hl2 += (BufferHL[i + j] - ma_hl) * (BufferHL[i + j] - ma_hl)
        BufferPM[i] = (_fdiv(sum_, sqrt(sum_cc2 * sum_hl2)) if (sum_cc2 != 0 and sum_hl2 != 0) else 0)
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PowerMeasure(_MQL5Indicator):
    name = 'Power_Measure'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
    }

