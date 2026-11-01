"""rsi_floating_levels_2 — converted from MQL5: MQL5 Indicators/RSI Floating Levels/rsi_floating_levels_2.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [14546909, 14804223], 2: [3329330], 3: [6908265], 4: [9662683], 5: [11119017]}, 'widths': {5: 2}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'rsi OB/OS zone', 2: 'rsi up level', 3: 'rsi middle level', 4: 'rsi down level', 5: 'rsi'}, 'levels': [], 'description': [], 'name': 'rsi_floating_levels_2', 'source': 'MQL5 Indicators/RSI Floating Levels/rsi_floating_levels_2.mq5', 'folder': 'RSI Floating Levels', 'inputs': [{'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'int', 'default': 14, 'label': 'Rsi period', 'sinput': False}, {'mql': 'RsiMethod', 'py': 'RsiMethod', 'param': 'RsiMethod', 'type': 'int', 'default': 0, 'label': 'Rsi method', 'sinput': False}, {'mql': 'MinMaxPeriod', 'py': 'MinMaxPeriod', 'param': 'MinMaxPeriod', 'type': 'int', 'default': 100, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 80.0, 'label': 'Up level %', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 20.0, 'label': 'Down level %', 'sinput': False}, {'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'double', 'default': 8.0, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'SmoothPhase', 'py': 'SmoothPhase', 'param': 'SmoothPhase', 'type': 'double', 'default': 0.0, 'label': 'Smoothing phase', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum rsiMethods
_rsi = 0
_wil = 1
_rsx = 2
_cut = 3
_enum('rsiMethods', {0: '_rsi', 1: '_wil', 2: '_rsx', 3: '_cut'})

# ---- inputs and global variables
RsiPeriod = _input('RsiPeriod', 14)  # Rsi period
RsiMethod = _input('RsiMethod', _rsi)  # Rsi method
MinMaxPeriod = _input('MinMaxPeriod', 100)  # Floating levels period
LevelUp = _input('LevelUp', 80.0)  # Up level %
LevelDown = _input('LevelDown', 20.0)  # Down level %
SmoothPeriod = _input('SmoothPeriod', 8.0)  # Smoothing period
SmoothPhase = _input('SmoothPhase', 0.0)  # Smoothing phase
rsi = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelMi = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
workRsi = Arr(0, 0.0, dims=(13,))
workSmma = Arr(0, 0.0, dims=(2,))
wrk = Arr(0, 0.0, dims=(10,))

def OnInit():
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, levelUp, INDICATOR_DATA)
    SetIndexBuffer(3, levelMi, INDICATOR_DATA)
    SetIndexBuffer(4, levelDn, INDICATOR_DATA)
    SetIndexBuffer(5, rsi, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, ' RSI floating levels (' + _str(RsiPeriod) + ',' + _str(MinMaxPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        rsi[i] = iSmooth(iRsi(price[i], RsiPeriod, RsiMethod, i, rates_total), SmoothPeriod, SmoothPhase, i, rates_total)
        min_ = rsi[i]
        max_ = rsi[i]
        k = 1
        while k < MinMaxPeriod and (i - k) >= 0:
            min_ = (rsi[i - k] if (rsi[i - k] < min_) else min_)
            max_ = (rsi[i - k] if (rsi[i - k] > max_) else max_)
            k += 1
        range_ = max_ - min_
        levelDn[i] = min_ + ((range_ * LevelDown) / 100.0)
        levelMi[i] = min_ + (range_ * 0.5)
        levelUp[i] = min_ + ((range_ * LevelUp) / 100.0)
        fill1[i] = rsi[i]
        fill2[i] = rsi[i]
        if rsi[i] > levelUp[i]:
            fill2[i] = levelUp[i]
        if rsi[i] < levelDn[i]:
            fill2[i] = levelDn[i]
    return rates_total

def iRsi(price, period, rsiMode, r, bars, instanceNo=0):
    if ArrayRange(workRsi, 0) != bars:
        ArrayResize(workRsi, bars)
    z = instanceNo * 13
    workRsi[r][z + 0] = price
    _sw1 = rsiMode
    if _sw1 == _rsi:
        if r < period:
            k = 0
            sum_ = 0.0
            k = 0
            while k < period and (r - k - 1) >= 0:
                sum_ += MathAbs(workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0])
                k += 1
            workRsi[r][z + 1] = _fdiv(workRsi[r][z + 0] - workRsi[0][z + 0], MathMax(k, 1))
            workRsi[r][z + 2] = _fdiv(sum_, MathMax(k, 1))
        else:
            alpha = _fdiv(1.0, period)
            change = workRsi[r][z + 0] - workRsi[r - 1][z + 0]
            workRsi[r][z + 1] = workRsi[r - 1][z + 1] + (alpha * (change - workRsi[r - 1][z + 1]))
            workRsi[r][z + 2] = workRsi[r - 1][z + 2] + (alpha * (MathAbs(change) - workRsi[r - 1][z + 2]))
        if workRsi[r][z + 2] != 0:
            return 50.0 * (_fdiv(workRsi[r][z + 1], workRsi[r][z + 2]) + 1)
        else:
            return 50.0
    elif _sw1 == _wil:
        if r > 0:
            workRsi[r][z + 1] = iSmma(0.5 * (MathAbs(workRsi[r][z + 0] - workRsi[r - 1][z + 0]) + (workRsi[r][z + 0] - workRsi[r - 1][z + 0])), 0.5 * (period - 1), r, bars, (instanceNo * 2) + 0)
            workRsi[r][z + 2] = iSmma(0.5 * (MathAbs(workRsi[r][z + 0] - workRsi[r - 1][z + 0]) - (workRsi[r][z + 0] - workRsi[r - 1][z + 0])), 0.5 * (period - 1), r, bars, (instanceNo * 2) + 1)
            if (workRsi[r][z + 1] + workRsi[r][z + 2]) != 0:
                return _fdiv(100.0 * workRsi[r][z + 1], workRsi[r][z + 1] + workRsi[r][z + 2])
            else:
                return 50.0
        else:
            return 50.0
    elif _sw1 == _rsx:
        if r < period:
            for k in range(1, 13):
                workRsi[r][k + z] = 0.0
            return 50.0
        Kg = _fdiv(3.0, 2.0 + period)
        Hg = 1.0 - Kg
        mom = workRsi[r][0 + z] - workRsi[r - 1][0 + z]
        moa = MathAbs(mom)
        for k in range(0, 3):
            kk = k * 2
            workRsi[r][z + kk + 1] = (Kg * mom) + (Hg * workRsi[r - 1][z + kk + 1])
            workRsi[r][z + kk + 2] = (Kg * workRsi[r][z + kk + 1]) + (Hg * workRsi[r - 1][z + kk + 2])
            mom = (1.5 * workRsi[r][z + kk + 1]) - (0.5 * workRsi[r][z + kk + 2])
            workRsi[r][z + kk + 7] = (Kg * moa) + (Hg * workRsi[r - 1][z + kk + 7])
            workRsi[r][z + kk + 8] = (Kg * workRsi[r][z + kk + 7]) + (Hg * workRsi[r - 1][z + kk + 8])
            moa = (1.5 * workRsi[r][z + kk + 7]) - (0.5 * workRsi[r][z + kk + 8])
        if moa != 0:
            return MathMax(MathMin((_fdiv(mom, moa) + 1.0) * 50.0, 100.0), 0.0)
        else:
            return 50.0
    elif _sw1 == _cut:
        sump = 0.0
        sumn = 0.0
        k = 0
        while k < period and (r - k - 1) >= 0:
            diff = workRsi[r - k][z + 0] - workRsi[r - k - 1][z + 0]
            if diff > 0:
                sump += diff
            if diff < 0:
                sumn -= diff
            k += 1
        if sumn > 0:
            return 100.0 - _fdiv(100.0, 1.0 + _fdiv(sump, sumn))
        else:
            return 50.0
    return price

def iSmma(price, period, r, bars, instanceNo=0):
    if ArrayRange(workSmma, 0) != bars:
        ArrayResize(workSmma, bars)
    if r < period:
        workSmma[r][instanceNo] = price
    else:
        workSmma[r][instanceNo] = workSmma[r - 1][instanceNo] + _fdiv(price - workSmma[r - 1][instanceNo], period)
    return workSmma[r][instanceNo]

def iSmooth(price, length, phase, r, bars, s=0):
    if length <= 1:
        return price
    if ArrayRange(wrk, 0) != bars:
        ArrayResize(wrk, bars)
    s *= 10
    if r == 0:
        k = 0
        k = 0
        for k in range(k, 7):
            wrk[r][k + s] = price
        else:
            k = _range_end(k, 7, 1)
        while k < 10:
            wrk[r][k + s] = 0.0
            k += 1
        return price
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = price - wrk[r - 1][5 + s]
    del2 = price - wrk[r - 1][6 + s]
    div = _fdiv(1.0, 10.0 + ((10.0 * MathMin(MathMax(length - 10, 0), 100)) / 100))
    forBar = MathMin(r, 10)
    wrk[r][7 + s] = 0.0
    if MathAbs(del1) > MathAbs(del2):
        wrk[r][7 + s] = MathAbs(del1)
    if MathAbs(del1) < MathAbs(del2):
        wrk[r][7 + s] = MathAbs(del2)
    wrk[r][8 + s] = wrk[r - 1][8 + s] + ((wrk[r][7 + s] - wrk[r - forBar][7 + s]) * div)
    wrk[r][9 + s] = wrk[r - 1][9 + s] + (_fdiv(2.0, MathMax(4.0 * length, 30) + 1.0) * (wrk[r][8 + s] - wrk[r - 1][9 + s]))
    dVolty = 0.0
    if wrk[r][9 + s] > 0:
        dVolty = _fdiv(wrk[r][7 + s], wrk[r][9 + s])
    if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
        dVolty = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty < 1:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    if del1 > 0:
        wrk[r][5 + s] = price
    else:
        wrk[r][5 + s] = price - (Kv * del1)
    if del2 < 0:
        wrk[r][6 + s] = price
    else:
        wrk[r][6 + s] = price - (Kv * del2)
    R = (MathMax(MathMin(phase, 100), -100) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1), (0.45 * (length - 1)) + 2)
    alpha = MathPow(beta, pow2)
    wrk[r][0 + s] = price + (alpha * (wrk[r - 1][0 + s] - price))
    wrk[r][1 + s] = ((price - wrk[r][0 + s]) * (1 - beta)) + (beta * wrk[r - 1][1 + s])
    wrk[r][2 + s] = wrk[r][0 + s] + (R * wrk[r][1 + s])
    wrk[r][3 + s] = ((wrk[r][2 + s] - wrk[r - 1][4 + s]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * wrk[r - 1][3 + s])
    wrk[r][4 + s] = wrk[r - 1][4 + s] + wrk[r][3 + s]
    return wrk[r][4 + s]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiFloatingLevels2(_MQL5Indicator):
    name = 'rsi_floating_levels_2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RsiPeriod': 14,  # Rsi period
        'RsiMethod': _Choice({0: 'rsi', 1: "Wilder's rsi", 2: 'rsx', 3: "Cuttler's rsi"}, default=0),  # Rsi method
        'MinMaxPeriod': 100,  # Floating levels period
        'LevelUp': 80.0,  # Up level %
        'LevelDown': 20.0,  # Down level %
        'SmoothPeriod': 8.0,  # Smoothing period
        'SmoothPhase': 0.0,  # Smoothing phase
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

