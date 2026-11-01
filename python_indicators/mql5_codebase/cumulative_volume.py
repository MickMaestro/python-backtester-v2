"""Cumulative_Volume — converted from MQL5: MQL5 Indicators/Cumulative_Volume/Cumulative_Volume.mq5

Cumulative Volume:
Relative and Absolute presentation.
Cumulative or Separated (Up/Down)
 data presentation.
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [3329330, 255], 2: [3329330, 255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Positive', 2: 'Negative'}, 'levels': [], 'description': ['Cumulative Volume:', 'Relative and Absolute presentation.', 'Cumulative or Separated (Up/Down)', ' data presentation.'], 'name': 'Cumulative_Volume', 'source': 'MQL5 Indicators/Cumulative_Volume/Cumulative_Volume.mq5', 'folder': 'Cumulative_Volume', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpCombined', 'py': 'InpCombined', 'param': 'InpCombined', 'type': 'int', 'default': 1, 'label': 'Combined', 'sinput': False}, {'mql': 'InpRelative', 'py': 'InpRelative', 'param': 'InpRelative', 'type': 'int', 'default': 0, 'label': 'Relative', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpCombined = _input('InpCombined', INPUT_YES)  # Combined
InpRelative = _input('InpRelative', INPUT_NO)  # Relative
BufferPOS = Arr(0, 0.0)
BufferColorsPOS = Arr(0, 0.0)
BufferNEG = Arr(0, 0.0)
BufferColorsNEG = Arr(0, 0.0)
BufferPosTMP = Arr(0, 0.0)
BufferNegTMP = Arr(0, 0.0)
period_ma = 0

def OnInit():
    global period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferPOS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColorsPOS, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferNEG, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColorsNEG, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferPosTMP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferNegTMP, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Cumulative Volume(' + _str(period_ma) + ')')
    ArraySetAsSeries(BufferPOS, True)
    ArraySetAsSeries(BufferColorsPOS, True)
    ArraySetAsSeries(BufferNEG, True)
    ArraySetAsSeries(BufferColorsNEG, True)
    ArraySetAsSeries(BufferPosTMP, True)
    ArraySetAsSeries(BufferNegTMP, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma:
        return 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 2
        ArrayInitialize(BufferPOS, 0)
        ArrayInitialize(BufferNEG, 0)
        ArrayInitialize(BufferPosTMP, 0)
        ArrayInitialize(BufferNegTMP, 0)
    for i in range(limit, 0 - 1, -1):
        if close[i] > close[i + 1]:
            BufferPosTMP[i] = float(tick_volume[i]) / 100
            BufferNegTMP[i] = 0.0
        else:
            BufferPosTMP[i] = 0.0
            BufferNegTMP[i] = float(tick_volume[i]) / 100
    for i in range(limit, 0 - 1, -1):
        pos = MAOnArray(BufferPosTMP, 0, period_ma, 0, MODE_SMA, i) * period_ma
        neg = MAOnArray(BufferNegTMP, 0, period_ma, 0, MODE_SMA, i) * period_ma
        vol = 0.0
        for j in range(0, period_ma):
            vol += float(tick_volume[i + j])
        vol = vol / 100
        if InpCombined:
            if InpRelative:
                res = _fdiv((pos - neg) * 1000, vol)
                BufferPOS[i] = (res if (res > 0) else 0)
                BufferNEG[i] = (res if (res <= 0) else 0)
                BufferColorsPOS[i] = (0 if (BufferPOS[i] > BufferPOS[i + 1]) else 1)
                BufferColorsNEG[i] = (0 if (BufferNEG[i] > BufferNEG[i + 1]) else 1)
            else:
                res = pos - neg
                BufferPOS[i] = (res if (res > 0) else 0)
                BufferNEG[i] = (res if (res <= 0) else 0)
                BufferColorsPOS[i] = (0 if (BufferPOS[i] > BufferPOS[i + 1]) else 1)
                BufferColorsNEG[i] = (0 if (BufferNEG[i] > BufferNEG[i + 1]) else 1)
        else:
            if InpRelative:
                BufferPOS[i] = _fdiv(pos * 1000, vol)
                BufferNEG[i] = _fdiv((-neg) * 1000, vol)
                BufferColorsPOS[i] = 0.0
                BufferColorsNEG[i] = 1.0
            else:
                BufferPOS[i] = pos
                BufferNEG[i] = -neg
                BufferColorsPOS[i] = 0.0
                BufferColorsNEG[i] = 1.0
    return rates_total

def MAOnArray(array, total, period, ma_shift, ma_method, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period - ma_shift):
        return 0.0
    _sw1 = ma_method
    if _sw1 == MODE_SMA:
        total = ArrayCopy(arr, array, 0, shift + ma_shift, period)
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        i = 0
        pos = total - 1
        i = 1
        while i < period:
            sum_ += arr[pos]
            i += 1
            pos -= 1
        while pos >= 0:
            sum_ += arr[pos]
            buf[pos] = _fdiv(sum_, period)
            sum_ -= arr[pos + period - 1]
            pos -= 1
        return buf[0]
    elif _sw1 == MODE_EMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        pr = _fdiv(2.0, period + 1)
        pos = total - 2
        while pos >= 0:
            if pos == (total - 2):
                buf[pos + 1] = array[pos + 1]
            buf[pos] = (array[pos] * pr) + (buf[pos + 1] * (1 - pr))
            pos -= 1
        return buf[shift + ma_shift]
    elif _sw1 == MODE_SMMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        i = 0
        k = 0
        pos = 0
        pos = total - period
        while pos >= 0:
            if pos == (total - period):
                i = 0
                k = pos
                while i < period:
                    sum_ += array[k]
                    buf[k] = 0.0
                    i += 1
                    k += 1
            else:
                sum_ = (buf[pos + 1] * (period - 1)) + array[pos]
            buf[pos] = _fdiv(sum_, period)
            pos -= 1
        return buf[shift + ma_shift]
    elif _sw1 == MODE_LWMA:
        if ArrayResize(buf, total) < 0:
            return 0.0
        sum_ = 0.0
        lsum = 0.0
        price = 0.0
        i = 0
        weight = 0
        pos = total - 1
        i = 1
        while i <= period:
            price = array[pos]
            sum_ += price * i
            lsum += price
            weight += i
            i += 1
            pos -= 1
        pos += 1
        i = pos + period
        while pos >= 0:
            buf[pos] = _fdiv(sum_, weight)
            if pos == 0:
                break
            pos -= 1
            i -= 1
            price = array[pos]
            sum_ = sum_ - lsum + (price * period)
            lsum -= array[i]
            lsum += price
        return buf[shift + ma_shift]
    else:
        return 0.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CumulativeVolume(_MQL5Indicator):
    name = 'Cumulative_Volume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpCombined': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Combined
        'InpRelative': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Relative
    }

