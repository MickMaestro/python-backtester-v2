"""Candle_Range_Envelop — converted from MQL5: MQL5 Indicators/Candle_Range_Envelop/Candle_Range_Envelop.mq5

Candle Range Envelop
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 10, 2: 1, 3: 1, 4: 1}, 'colors': {1: [32768, 255, 11119017], 2: [11119017], 3: [11119017], 4: [11119017]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Range', 2: 'Signal', 3: 'Top', 4: 'Bottom'}, 'levels': [], 'description': ['Candle Range Envelop'], 'name': 'Candle_Range_Envelop', 'source': 'MQL5 Indicators/Candle_Range_Envelop/Candle_Range_Envelop.mq5', 'folder': 'Candle_Range_Envelop', 'inputs': [{'mql': 'InpPeriodRng', 'py': 'InpPeriodRng', 'param': 'InpPeriodRng', 'type': 'uint', 'default': 1, 'label': 'Range period', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 14, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpPeriodDev', 'py': 'InpPeriodDev', 'param': 'InpPeriodDev', 'type': 'uint', 'default': 14, 'label': 'Deviation period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation multiplier', 'sinput': False}, {'mql': 'InpEnvPrcTop', 'py': 'InpEnvPrcTop', 'param': 'InpEnvPrcTop', 'type': 'double', 'default': 20.0, 'label': 'Percent top envelope', 'sinput': False}, {'mql': 'InpEnvPrcBottom', 'py': 'InpEnvPrcBottom', 'param': 'InpEnvPrcBottom', 'type': 'double', 'default': 20.0, 'label': 'Percent bottom envelope', 'sinput': False}, {'mql': 'InpMethodEnv', 'py': 'InpMethodEnv', 'param': 'InpMethodEnv', 'type': 'int', 'default': 0, 'label': 'Envelop method', 'sinput': False}, {'mql': 'InpMethodPrc', 'py': 'InpMethodPrc', 'param': 'InpMethodPrc', 'type': 'int', 'default': 0, 'label': 'Price method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE_ENV
MODE_ENV_DEV = 0
MODE_ENV_PRC = 1
_enum('ENUM_MODE_ENV', {0: 'MODE_ENV_DEV', 1: 'MODE_ENV_PRC'})

# enum ENUM_MODE_PRC
MODE_PRC_HL = 0
MODE_PRC_OC = 1
_enum('ENUM_MODE_PRC', {0: 'MODE_PRC_HL', 1: 'MODE_PRC_OC'})

# ---- inputs and global variables
InpPeriodRng = _input('InpPeriodRng', 1)  # Range period
InpPeriodSig = _input('InpPeriodSig', 14)  # Signal period
InpPeriodDev = _input('InpPeriodDev', 14)  # Deviation period
InpDeviation = _input('InpDeviation', 2.0)  # Deviation multiplier
InpEnvPrcTop = _input('InpEnvPrcTop', 20.0)  # Percent top envelope
InpEnvPrcBottom = _input('InpEnvPrcBottom', 20.0)  # Percent bottom envelope
InpMethodEnv = _input('InpMethodEnv', MODE_ENV_DEV)  # Envelop method
InpMethodPrc = _input('InpMethodPrc', MODE_PRC_HL)  # Price method
BufferRange = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
deviation = 0.0
percent_t = 0.0
percent_b = 0.0
period_rng = 0
period_sig = 0
period_dev = 0
period_max = 0

def OnInit():
    global deviation, percent_b, percent_t, period_dev, period_max, period_rng, period_sig
    period_rng = (1 if (InpPeriodRng < 1) else InpPeriodRng)
    period_sig = (1 if (InpPeriodSig < 1) else InpPeriodSig)
    period_dev = (1 if (InpPeriodDev < 1) else InpPeriodDev)
    period_max = fmax(period_dev, fmax(period_rng, period_sig))
    percent_b = InpEnvPrcBottom
    percent_t = InpEnvPrcTop
    deviation = InpDeviation
    SetIndexBuffer(0, BufferRange, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(3, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(4, BufferBottom, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Candle Range Envelop')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRange, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferRange, 0)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        if InpMethodPrc == MODE_PRC_HL:
            bh = Highest(period_rng, i)
            bl = Lowest(period_rng, i)
            if bh == WRONG_VALUE or bl == WRONG_VALUE:
                continue
            BufferRange[i] = _fdiv(high[bh] - low[bl], Point())
        else:
            BufferRange[i] = _fdiv(fabs(open[i + period_rng] - close[i]), Point())
        BufferSignal[i] = SMA(rates_total, BufferRange, period_sig, i)
        delta_t = 0.0
        delta_b = 0.0
        if InpMethodEnv == MODE_ENV_DEV:
            delta_t = StdDevSMA(BufferSignal, period_dev, i) * deviation
            delta_b = delta_t
        else:
            delta_t = (BufferSignal[i] / 100.0) * percent_t
            delta_b = (BufferSignal[i] / 100.0) * percent_b
        BufferTop[i] = BufferSignal[i] + delta_t
        BufferBottom[i] = BufferSignal[i] - delta_b
        BufferColors[i] = (0 if (BufferRange[i] > BufferTop[i]) else 1 if (BufferRange[i] < BufferBottom[i]) else 2)
    return rates_total

def SMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return array_src[shift]
    sum_ = 0.0
    for i in range(0, period):
        sum_ += array_src[shift + i]
    return _fdiv(sum_, period)

def Highest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def StdDevSMA(array, period, index):
    avg = 0.0
    for i in range(0, period):
        avg += array[index + i]
    avg = _fdiv(avg, period)
    SD = 0.0
    for i in range(0, period):
        SD += (avg - array[index + i]) * (avg - array[index + i])
    SD = sqrt(_fdiv(SD, period))
    return SD


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleRangeEnvelop(_MQL5Indicator):
    name = 'Candle_Range_Envelop'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRng': 1,  # Range period
        'InpPeriodSig': 14,  # Signal period
        'InpPeriodDev': 14,  # Deviation period
        'InpDeviation': 2.0,  # Deviation multiplier
        'InpEnvPrcTop': 20.0,  # Percent top envelope
        'InpEnvPrcBottom': 20.0,  # Percent bottom envelope
        'InpMethodEnv': _Choice({0: 'Deviation', 1: 'Percentage'}, default=0),  # Envelop method
        'InpMethodPrc': _Choice({0: 'High/Low', 1: 'Open/Close'}, default=0),  # Price method
    }

