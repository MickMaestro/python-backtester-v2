"""dt_oscillator — converted from MQL5: MQL5 Indicators/DT Oscillator/dt_oscillator.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [15130800, 14804223], 2: [16760576], 3: [9662683]}, 'widths': {2: 2, 3: 1}, 'styles': {}, 'labels': {1: 'DT oscillator filling', 2: 'DT oscillator', 3: 'DT oscillator signal'}, 'levels': [70.0, 30.0], 'description': [], 'name': 'dt_oscillator', 'source': 'MQL5 Indicators/DT Oscillator/dt_oscillator.mq5', 'folder': 'DT Oscillator', 'inputs': [{'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 13, 'label': 'Rsi period', 'sinput': False}, {'mql': 'StochPeriod', 'py': 'StochPeriod', 'param': 'StochPeriod', 'type': 'int', 'default': 8, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'SlowingPeriod', 'py': 'SlowingPeriod', 'param': 'SlowingPeriod', 'type': 'int', 'default': 5, 'label': 'Slowing', 'sinput': False}, {'mql': 'SignalPeriod', 'py': 'SignalPeriod', 'param': 'SignalPeriod', 'type': 'int', 'default': 3, 'label': 'Signal period', 'sinput': False}, {'mql': 'TapeVisible', 'py': 'TapeVisible', 'param': 'TapeVisible', 'type': 'bool', 'default': True, 'label': 'Tape visibility', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RsiPeriod = _input('RsiPeriod', 13)  # Rsi period
StochPeriod = _input('StochPeriod', 8)  # Stochastic period
SlowingPeriod = _input('SlowingPeriod', 5)  # Slowing
SignalPeriod = _input('SignalPeriod', 3)  # Signal period
TapeVisible = _input('TapeVisible', True)  # Tape visibility
dtosc = Arr(0, 0.0)
dtoss = Arr(0, 0.0)
dtosf1 = Arr(0, 0.0)
dtosf2 = Arr(0, 0.0)
rsibuf = Arr(0, 0.0)
stobuf = Arr(0, 0.0)
rsiWork = Arr(0, 0.0, dims=(3,))

def OnInit():
    SetIndexBuffer(0, dtosf1, INDICATOR_DATA)
    SetIndexBuffer(1, dtosf2, INDICATOR_DATA)
    SetIndexBuffer(2, dtosc, INDICATOR_DATA)
    SetIndexBuffer(3, dtoss, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if ArraySize(rsibuf) != rates_total:
        ArrayResize(rsibuf, rates_total)
    if ArraySize(stobuf) != rates_total:
        ArrayResize(stobuf, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        rsibuf[i] = iRsi(Close[i], RsiPeriod, i, rates_total)
        min_ = rsibuf[i]
        max_ = rsibuf[i]
        k = 1
        while k < StochPeriod and (i - k) >= 0:
            min_ = MathMin(rsibuf[i - k], min_)
            max_ = MathMax(rsibuf[i - k], max_)
            k += 1
        if max_ != min_:
            stobuf[i] = _fdiv(100 * (rsibuf[i] - min_), max_ - min_)
        else:
            stobuf[i] = 0.0
        dtosc[i] = 0.0
        k = 0
        while k < SlowingPeriod and (i - k) >= 0:
            dtosc[i] += stobuf[i - k]
            k += 1
        dtosc[i] = dtosc[i] / SlowingPeriod
        dtoss[i] = 0.0
        k = 0
        while k < SignalPeriod and (i - k) >= 0:
            dtoss[i] += dtosc[i - k]
            k += 1
        dtoss[i] = dtoss[i] / SignalPeriod
        if TapeVisible:
            dtosf1[i] = dtosc[i]
            dtosf2[i] = dtoss[i]
        else:
            dtosf1[i] = EMPTY_VALUE
            dtosf2[i] = EMPTY_VALUE
    return rates_total

def iRsi(price, period, i, bars):
    if ArrayRange(rsiWork, 0) != bars:
        ArrayResize(rsiWork, bars)
    rsiWork[i][0] = price
    if i == 0:
        rsiWork[i][1] = 0.0
        rsiWork[i][2] = 0.0
        return 50.0
    sf = _fdiv(1.0, period)
    change = rsiWork[i][0] - rsiWork[i - 1][0]
    rsiWork[i][1] = rsiWork[i - 1][1] + (sf * (change - rsiWork[i - 1][1]))
    rsiWork[i][2] = rsiWork[i - 1][2] + (sf * (MathAbs(change) - rsiWork[i - 1][2]))
    changeRatio = (_fdiv(rsiWork[i][1], rsiWork[i][2]) if (rsiWork[i][2] != 0) else 0)
    return 50.0 * (changeRatio + 1.0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DtOscillator(_MQL5Indicator):
    name = 'dt_oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RsiPeriod': 13,  # Rsi period
        'StochPeriod': 8,  # Stochastic period
        'SlowingPeriod': 5,  # Slowing
        'SignalPeriod': 3,  # Signal period
        'TapeVisible': True,  # Tape visibility
    }

