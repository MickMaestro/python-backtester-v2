"""Damiani_Volatmeter — converted from MQL5: MQL5 Indicators/Stable Damiani Volatmeter/Damiani_Volatmeter.mq5

Damiani volatmeter oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65280], 2: [17919]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'P', 2: 'M'}, 'levels': [], 'description': ['Damiani volatmeter oscillator'], 'name': 'Damiani_Volatmeter', 'source': 'MQL5 Indicators/Stable Damiani Volatmeter/Damiani_Volatmeter.mq5', 'folder': 'Stable Damiani Volatmeter', 'inputs': [{'mql': 'InpViscosity', 'py': 'InpViscosity', 'param': 'InpViscosity', 'type': 'uint', 'default': 7, 'label': 'Viscosity', 'sinput': False}, {'mql': 'InpSedimentation', 'py': 'InpSedimentation', 'param': 'InpSedimentation', 'type': 'uint', 'default': 50, 'label': 'Sedimentation', 'sinput': False}, {'mql': 'InpThreshold', 'py': 'InpThreshold', 'param': 'InpThreshold', 'type': 'double', 'default': 1.1, 'label': 'Threshold', 'sinput': False}, {'mql': 'InpLagSuppressor', 'py': 'InpLagSuppressor', 'param': 'InpLagSuppressor', 'type': 'bool', 'default': True, 'label': 'Lag suppressor', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpViscosity = _input('InpViscosity', 7)  # Viscosity
InpSedimentation = _input('InpSedimentation', 50)  # Sedimentation
InpThreshold = _input('InpThreshold', 1.1)  # Threshold
InpLagSuppressor = _input('InpLagSuppressor', True)  # Lag suppressor
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferP = Arr(0, 0.0)
BufferM = Arr(0, 0.0)
BufferATRV = Arr(0, 0.0)
BufferATRS = Arr(0, 0.0)
BufferDevV = Arr(0, 0.0)
BufferDevS = Arr(0, 0.0)
threshold = 0.0
viscosity = 0
sedimentation = 0
handle_atrv = 0
handle_atrs = 0
handle_devv = 0
handle_devs = 0
period_max = 0

def OnInit():
    global handle_atrs, handle_atrv, handle_devs, handle_devv, period_max, sedimentation, threshold, viscosity
    viscosity = (1 if (InpViscosity < 1) else InpViscosity)
    sedimentation = (2 if (InpSedimentation < 2) else InpSedimentation)
    period_max = fmax(viscosity, sedimentation)
    threshold = InpThreshold
    SetIndexBuffer(0, BufferP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferM, INDICATOR_DATA)
    SetIndexBuffer(2, BufferATRV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferATRS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDevV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferDevS, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Damiani volatmeter (' + _str(viscosity) + ',' + _str(sedimentation) + ',' + DoubleToString(threshold, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 8)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferP, True)
    ArraySetAsSeries(BufferM, True)
    ArraySetAsSeries(BufferATRV, True)
    ArraySetAsSeries(BufferATRS, True)
    ArraySetAsSeries(BufferDevV, True)
    ArraySetAsSeries(BufferDevS, True)
    ResetLastError()
    handle_atrv = iATR(None, PERIOD_CURRENT, viscosity)
    if handle_atrv == INVALID_HANDLE:
        Print('The iATR(', _str(viscosity), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_atrs = iATR(None, PERIOD_CURRENT, sedimentation)
    if handle_atrs == INVALID_HANDLE:
        Print('The iATR(', _str(sedimentation), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_devv = iStdDev(None, PERIOD_CURRENT, viscosity, 0, MODE_LWMA, InpAppliedPrice)
    if handle_devv == INVALID_HANDLE:
        Print('The iStdDev(', _str(viscosity), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_devs = iStdDev(None, PERIOD_CURRENT, sedimentation, 0, MODE_LWMA, InpAppliedPrice)
    if handle_devs == INVALID_HANDLE:
        Print('The iStdDev(', _str(sedimentation), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = MathMin(rates_total - prev_calculated, rates_total - period_max - 4)
    if limit >= (rates_total - period_max - 4):
        ArrayInitialize(BufferP, 0)
        ArrayInitialize(BufferM, 0)
        ArrayInitialize(BufferATRV, 0)
        ArrayInitialize(BufferATRS, 0)
        ArrayInitialize(BufferDevV, 0)
        ArrayInitialize(BufferDevS, 0)
    count = (rates_total if (limit >= (rates_total - period_max - 4)) else (limit + 1))
    copied = 0
    copied = CopyBuffer(handle_atrs, 0, 0, count, BufferATRS)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atrv, 0, 0, count, BufferATRV)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_devs, 0, 0, count, BufferDevS)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_devv, 0, 0, count, BufferDevV)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        ATR_V = BufferATRV[i]
        ATR_S = BufferATRS[i]
        StdDev_V = BufferDevV[i]
        StdDev_S = BufferDevS[i]
        if ATR_S != 0.0 and StdDev_S != 0.0:
            s1 = BufferP[i + 1]
            s3 = BufferP[i + 3]
            BufferP[i] = ((_fdiv(ATR_V, ATR_S) + ((s1 - s3) / 2.0)) if InpLagSuppressor else _fdiv(ATR_V, ATR_S))
            BufferM[i] = threshold - _fdiv(StdDev_V, StdDev_S)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DamianiVolatmeter(_MQL5Indicator):
    name = 'Damiani_Volatmeter'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpViscosity': 7,  # Viscosity
        'InpSedimentation': 50,  # Sedimentation
        'InpThreshold': 1.1,  # Threshold
        'InpLagSuppressor': True,  # Lag suppressor
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

