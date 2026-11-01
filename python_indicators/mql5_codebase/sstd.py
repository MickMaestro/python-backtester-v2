"""sstd — converted from MQL5: MQL5 Indicators/Smoothed Simple Trend Detector/sstd.mq5

Copyright: Copyright © 2004, MetaQuotes Software Corp., BECEMAL 2010; Link: http://www.becemal.ru/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, MetaQuotes Software Corp., BECEMAL 2010', 'link': 'http://www.becemal.ru/', 'version': '1.01', 'window': 'separate', 'indicator_minimum': -1.0, 'indicator_maximum': 1.0, 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [55295]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'STD'}, 'levels': [], 'description': [], 'name': 'sstd', 'source': 'MQL5 Indicators/Smoothed Simple Trend Detector/sstd.mq5', 'folder': 'Smoothed Simple Trend Detector', 'inputs': [{'mql': 'inSTDPeriod', 'py': 'inSTDPeriod', 'param': 'inSTDPeriod', 'type': 'int', 'default': 15, 'label': 'Period Of \tSmoothed Simple Trend Detector', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inSTDPeriod = _input('inSTDPeriod', 15)  # Period Of 	Smoothed Simple Trend Detector
STDPeriod = 0
sSTDPeriod = 0
Buffer = Arr(0, 0.0)
PosBuffer = Arr(0, 0.0)
NegBuffer = Arr(0, 0.0)
A1 = 0.0
A2 = 0.0
A3 = 0.0
A4 = 0.0

def TPBF(InPeriod, R1, R2, R3, R4):
    CutOffPeriod = InPeriod
    if CutOffPeriod < 4.0:
        CutOffPeriod = 4.0
    a1 = MathExp(_fdiv(-1.0 * M_PI, CutOffPeriod))
    b1 = 2.0 * a1 * MathCos(_fdiv(M_PI * MathSqrt(3.0), CutOffPeriod))
    c1 = a1 * a1
    R2.v = b1 + c1
    R3.v = -(c1 + (b1 * c1))
    R4.v = c1 * c1
    R1.v = 1.0 - R2.v - R3.v - R4.v

def OnInit():
    global STDPeriod, sSTDPeriod
    if inSTDPeriod < 8:
        sSTDPeriod = 16
        Print('Incorrect Period Of Simple Trend Detector = ', inSTDPeriod, '. Indicator use STDPeriod = ', sSTDPeriod)
    else:
        sSTDPeriod = inSTDPeriod
    TPBF(sSTDPeriod, _GlobRef(globals(), 'A1'), _GlobRef(globals(), 'A2'), _GlobRef(globals(), 'A3'), _GlobRef(globals(), 'A4'))
    STDPeriod = (_idiv(sSTDPeriod, 4) if (sSTDPeriod > 16) else 4)
    SetIndexBuffer(0, Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, PosBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, NegBuffer, INDICATOR_CALCULATIONS)
    if ((not ArraySetAsSeries(Buffer, False)) or (not ArraySetAsSeries(PosBuffer, False))) or (not ArraySetAsSeries(NegBuffer, False)):
        Print('ArraySetAsSeries Error ', GetLastError())
        return -1
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    if rates_total <= STDPeriod:
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        i = begin
        for i in range(i, STDPeriod):
            PosBuffer[i] = 0.0
        else:
            i = _range_end(i, STDPeriod, 1)
        i = begin
        for i in range(i, STDPeriod):
            NegBuffer[i] = 0.0
        else:
            i = _range_end(i, STDPeriod, 1)
        i = begin
        for i in range(i, STDPeriod):
            Buffer[i] = 0.0
        else:
            i = _range_end(i, STDPeriod, 1)
        limit = STDPeriod
    else:
        limit = prev_calculated - 2
    i = limit
    for i in range(i, rates_total):
        positive = 0.0
        negative = 0.0
        rel = price[i] - price[i - 1]
        if rel > 0.0:
            positive = rel
        else:
            negative = -rel
        PosBuffer[i] = positive
        NegBuffer[i] = negative
    else:
        i = _range_end(i, rates_total, 1)
    if False:
        return 0
    i = limit
    for i in range(i, rates_total):
        positive = 0.0
        negative = 0.0
        for j in range(0, STDPeriod):
            Norm = STDPeriod - j
            positive += Norm * PosBuffer[i - j]
            negative += Norm * NegBuffer[i - j]
        Den = positive + negative
        STD = 0.0
        if Den == 0.0:
            STD = 0.0
        else:
            STD = _fdiv(2.0 * positive, Den) - 1.0
        Buffer[i] = (A1 * STD) + (A2 * Buffer[i - 1]) + (A3 * Buffer[i - 2]) + (A4 * Buffer[i - 3])
    else:
        i = _range_end(i, rates_total, 1)
    if False:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Sstd(_MQL5Indicator):
    name = 'sstd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inSTDPeriod': 15,  # Period Of 	Smoothed Simple Trend Detector
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (-1.0, 1.0)

