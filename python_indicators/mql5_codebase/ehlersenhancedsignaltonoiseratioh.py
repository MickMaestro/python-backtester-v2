"""EhlersEnhancedSignalToNoiseRatioH — converted from MQL5: MQL5 Indicators/The Enhanced Signal To Noise Ratio/EhlersEnhancedSignalToNoiseRatioH.mq5

The Enhanced Signal To Noise Ratio:\\nJohn Ehlers, \\"Rocket Science for Traders.\\", pg.87-88
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 17, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [32768, 255, 3329330]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['The Enhanced Signal To Noise Ratio:\\nJohn Ehlers, \\"Rocket Science for Traders.\\", pg.87-88'], 'name': 'EhlersEnhancedSignalToNoiseRatioH', 'source': 'MQL5 Indicators/The Enhanced Signal To Noise Ratio/EhlersEnhancedSignalToNoiseRatioH.mq5', 'folder': 'The Enhanced Signal To Noise Ratio', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
snr = Arr(0, 0.0)
cf = Arr(0, 0.0)
q3 = Arr(0, 0.0)
noise = Arr(0, 0.0)
Smooth = Arr(0, 0.0)
Detrender = Arr(0, 0.0)
I1 = Arr(0, 0.0)
Q1 = Arr(0, 0.0)
jI = Arr(0, 0.0)
jQ = Arr(0, 0.0)
I2 = Arr(0, 0.0)
Q2 = Arr(0, 0.0)
Re = Arr(0, 0.0)
Im = Arr(0, 0.0)
Per = Arr(0, 0.0)
SmoothPeriod = Arr(0, 0.0)
price = Arr(0, 0.0)
MINBAR = 7

def OnInit():
    SetIndexBuffer(0, snr, INDICATOR_DATA)
    SetIndexBuffer(1, cf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, q3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, noise, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, Smooth, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, Detrender, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, I1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, Q1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, jI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, jQ, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, I2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, Q2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, Re, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, Im, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, Per, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, SmoothPeriod, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, price, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(snr, True)
    ArraySetAsSeries(cf, True)
    ArraySetAsSeries(q3, True)
    ArraySetAsSeries(noise, True)
    ArraySetAsSeries(Smooth, True)
    ArraySetAsSeries(Detrender, True)
    ArraySetAsSeries(I1, True)
    ArraySetAsSeries(Q1, True)
    ArraySetAsSeries(jI, True)
    ArraySetAsSeries(jQ, True)
    ArraySetAsSeries(I2, True)
    ArraySetAsSeries(Q2, True)
    ArraySetAsSeries(Re, True)
    ArraySetAsSeries(Im, True)
    ArraySetAsSeries(Per, True)
    ArraySetAsSeries(SmoothPeriod, True)
    ArraySetAsSeries(price, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EnhancedSignalToNoiseRatioH')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def GetValue(h, l, i):
    q3[i] = 0.5 * (Smooth[i] - Smooth[i + 2]) * ((0.1759 * SmoothPeriod[i]) + 0.4607)
    i3 = 0.0
    sp = _int(MathCeil(SmoothPeriod[i] / 2))
    if sp == 0:
        sp = 1
    for j in range(0, sp):
        i3 += q3[j + i]
    i3 = _fdiv(1.57 * i3, sp)
    signal = MathPow(i3, 2) + MathPow(q3[i], 2)
    noise[i] = (0.1 * MathPow(h[i] - l[i], 2) * 0.25) + (0.9 * noise[i + 1])
    if noise[i] != 0.0 and signal != 0:
        s = ZerroIfEmpty(snr[i + 1])
        snr[i] = _fdiv(3.3 * MathLog(_fdiv(signal, noise[i])), MathLog(10)) + (0.67 * s)
    else:
        snr[i] = 0.0
    if price[i] > Smooth[i]:
        cf[i] = 2.0
    elif price[i] < Smooth[i]:
        cf[i] = 1.0
    return snr[i]

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= 4:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        price[1] = (high[1] + low[1]) / 2
        Hilbert(1)
        GetValue(high, low, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(snr, EMPTY_VALUE)
        ArrayInitialize(cf, 0)
        ArrayInitialize(q3, 0)
        ArrayInitialize(noise, 0)
        ArrayInitialize(Smooth, 0)
        ArrayInitialize(Detrender, 0)
        ArrayInitialize(I1, 0)
        ArrayInitialize(Q1, 0)
        ArrayInitialize(jI, 0)
        ArrayInitialize(jQ, 0)
        ArrayInitialize(I2, 0)
        ArrayInitialize(Q2, 0)
        ArrayInitialize(Re, 0)
        ArrayInitialize(Im, 0)
        ArrayInitialize(Per, 0)
        ArrayInitialize(SmoothPeriod, 0)
        ArrayInitialize(price, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            price[i] = (high[i] + low[i]) / 2
            Hilbert(i)
            GetValue(high, low, i)
        return rates_total
    price[0] = (high[0] + low[0]) / 2
    Hilbert(0)
    GetValue(high, low, 0)
    return rates_total

def ZerroIfEmpty(value):
    if value >= EMPTY_VALUE or value <= (-EMPTY_VALUE):
        return 0.0
    return value

def Hilbert(i):
    Smooth[i] = ((4 * price[i]) + (3 * price[i + 1]) + (2 * price[i + 2]) + price[i + 3]) / 10
    Detrender[i] = ((0.0962 * Smooth[i]) + (0.5769 * Smooth[i + 2]) - (0.5769 * Smooth[i + 4]) - (0.0962 * Smooth[i + 6])) * ((0.075 * Per[i + 1]) + 0.54)
    Q1[i] = ((0.0962 * Detrender[i]) + (0.5769 * Detrender[i + 2]) - (0.5769 * Detrender[i + 4]) - (0.0962 * Detrender[i + 6])) * ((0.075 * Per[i + 1]) + 0.54)
    I1[i] = Detrender[i + 3]
    jI[i] = ((0.0962 * I1[i]) + (0.5769 * I1[i + 2]) - (0.5769 * I1[i + 4]) - (0.0962 * I1[i + 6])) * ((0.075 * Per[i + 1]) + 0.54)
    jQ[i] = ((0.0962 * Q1[i]) + (0.5769 * Q1[i + 2]) - (0.5769 * Q1[i + 4]) - (0.0962 * Q1[i + 6])) * ((0.075 * Per[i + 1]) + 0.54)
    I2[i] = I1[i] - jQ[i]
    Q2[i] = Q1[i] + jI[i]
    I2[i] = (0.2 * I2[i]) + (0.8 * I2[i + 1])
    Q2[i] = (0.2 * Q2[i]) + (0.8 * Q2[i + 1])
    Re[i] = (I2[i] * I2[i]) + (Q2[i] * Q2[i + 1])
    Im[i] = (I2[i] * Q2[i + 1]) - (Q2[i] * I2[i + 1])
    Re[i] = (0.2 * Re[i]) + (0.8 * Re[i + 1])
    Im[i] = (0.2 * Im[i]) + (0.8 * Im[i + 1])
    if Im[i] != 0 and Re[i] != 0:
        Per[i] = _fdiv(2 * M_PI, MathArctan(_fdiv(Im[i], Re[i])))
    else:
        Per[i] = 0.0
    if Per[i] > (1.5 * Per[i + 1]):
        Per[i] = 1.5 * Per[i + 1]
    if Per[i] < (0.67 * Per[i + 1]):
        Per[i] = 0.67 * Per[i + 1]
    if Per[i] < 6:
        Per[i] = 6.0
    if Per[i] > 50:
        Per[i] = 50.0
    Per[i] = (0.2 * Per[i]) + (0.8 * Per[i + 1])
    SmoothPeriod[i] = (0.33 * Per[i]) + (0.67 * SmoothPeriod[i + 1])


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersEnhancedSignalToNoiseRatioH(_MQL5Indicator):
    name = 'EhlersEnhancedSignalToNoiseRatioH'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

