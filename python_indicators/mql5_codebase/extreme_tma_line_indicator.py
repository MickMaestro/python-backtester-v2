"""Extreme_TMA_line_indicator — converted from MQL5: MQL5 Indicators/Extreme_TMA_line_indicator/Extreme_TMA_line_indicator.mq5

Extreme TMA Line indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 8, 2: 1, 3: 1}, 'colors': {1: [32768, 255, 11119017], 2: [11119017], 3: [11119017]}, 'widths': {1: 2, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'TMA', 2: 'Top', 3: 'Bottom'}, 'levels': [], 'description': ['Extreme TMA Line indicator'], 'name': 'Extreme_TMA_line_indicator', 'source': 'MQL5 Indicators/Extreme_TMA_line_indicator/Extreme_TMA_line_indicator.mq5', 'folder': 'Extreme_TMA_line_indicator', 'inputs': [{'mql': 'InpPeriodTMA', 'py': 'InpPeriodTMA', 'param': 'InpPeriodTMA', 'type': 'uint', 'default': 56, 'label': 'TMA period', 'sinput': False}, {'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 100, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpMultiplierATR', 'py': 'InpMultiplierATR', 'param': 'InpMultiplierATR', 'type': 'double', 'default': 2.0, 'label': 'ATR multiplier', 'sinput': False}, {'mql': 'InpThreshold', 'py': 'InpThreshold', 'param': 'InpThreshold', 'type': 'double', 'default': 0.5, 'label': 'Trend threshold', 'sinput': False}, {'mql': 'InpRedraw', 'py': 'InpRedraw', 'param': 'InpRedraw', 'type': 'int', 'default': 1, 'label': 'Redraw', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodTMA = _input('InpPeriodTMA', 56)  # TMA period
InpPeriodATR = _input('InpPeriodATR', 100)  # ATR period
InpMultiplierATR = _input('InpMultiplierATR', 2.0)  # ATR multiplier
InpThreshold = _input('InpThreshold', 0.5)  # Trend threshold
InpRedraw = _input('InpRedraw', INPUT_YES)  # Redraw
BufferTMA = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
multiplier = 0.0
threshold = 0.0
period_tma = 0
period_atr = 0
period_max = 0
handle_atr = 0

def OnInit():
    global handle_atr, multiplier, period_atr, period_max, period_tma, threshold
    period_tma = (1 if (InpPeriodTMA < 1) else InpPeriodTMA)
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    period_max = fmax(period_atr, period_tma)
    multiplier = InpMultiplierATR
    threshold = InpThreshold
    SetIndexBuffer(0, BufferTMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(3, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(4, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Extreme TMA Line (' + _str(period_tma) + ',' + _str(period_atr) + ',' + DoubleToString(multiplier, 1) + ',' + DoubleToString(threshold, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTMA, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferTMA, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferATR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        tcount = period_tma
        period_last = (True if (i == 0) else False)
        while tcount > 0:
            tcount = (0 if (not period_last) else (tcount - 1))
            sum_ = 0.0
            sumw = _idiv((period_tma + 2) * (period_tma + 1), 2)
            for j in range(0, period_tma + 1):
                sum_ += (period_tma - j + 1) * close[i + j]
                if InpRedraw:
                    if (i - j) > 0:
                        sum_ += (period_tma - j + 1) * close[i - j]
                        sumw += period_tma - j + 1
            if sumw != 0:
                BufferTMA[i] = _fdiv(sum_, sumw)
    for i in range(limit, 0 - 1, -1):
        slope = _fdiv(BufferTMA[i] - BufferTMA[i + 1], 0.1 * BufferATR[i])
        range_ = BufferATR[i] * multiplier
        BufferTop[i] = BufferTMA[i] + range_
        BufferBottom[i] = BufferTMA[i] - range_
        if slope > threshold:
            BufferColors[i + 1] = 0.0
            BufferColors[i] = BufferColors[i + 1]
        elif slope < (-threshold):
            BufferColors[i + 1] = 1.0
            BufferColors[i] = BufferColors[i + 1]
        else:
            BufferColors[i + 1] = 2.0
            BufferColors[i] = BufferColors[i + 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ExtremeTMALineIndicator(_MQL5Indicator):
    name = 'Extreme_TMA_line_indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriodTMA': 56,  # TMA period
        'InpPeriodATR': 100,  # ATR period
        'InpMultiplierATR': 2.0,  # ATR multiplier
        'InpThreshold': 0.5,  # Trend threshold
        'InpRedraw': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Redraw
    }

