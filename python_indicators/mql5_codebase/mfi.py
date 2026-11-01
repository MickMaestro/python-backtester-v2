"""mfi — converted from MQL5: MQL5 Indicators/Money Flow Index (MFI)/mfi.mq5

Money Flow Index
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_maximum': 100.0, 'indicator_minimum': 0.0}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [20.0, 80.0], 'description': ['Money Flow Index'], 'name': 'mfi', 'source': 'MQL5 Indicators/Money Flow Index (MFI)/mfi.mq5', 'folder': 'Money Flow Index (MFI)', 'inputs': [{'mql': 'InpMFIPeriod', 'py': 'InpMFIPeriod', 'param': 'InpMFIPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpVolumeType', 'py': 'InpVolumeType', 'param': 'InpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMFIPeriod = _input('InpMFIPeriod', 14)  # Period
InpVolumeType = _input('InpVolumeType', VOLUME_TICK)  # Volumes
ExtMFIBuffer = Arr(0, 0.0)
ExtMFIPeriod = 0

def OnInit():
    global ExtMFIPeriod
    if InpMFIPeriod <= 0:
        ExtMFIPeriod = 14
        Print('Parameter InpMFIPeriod has wrong value. Indicator will use value ', ExtMFIPeriod)
    else:
        ExtMFIPeriod = InpMFIPeriod
    SetIndexBuffer(0, ExtMFIBuffer)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MFI' + '(' + _str(ExtMFIPeriod) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtMFIPeriod)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    CalcPosition = 0
    if rates_total < ExtMFIPeriod:
        return 0
    if prev_calculated < ExtMFIPeriod:
        CalcPosition = ExtMFIPeriod
    else:
        CalcPosition = prev_calculated - 1
    if InpVolumeType == VOLUME_TICK:
        CalculateMFI(CalcPosition, rates_total, High, Low, Close, TickVolume)
    else:
        CalculateMFI(CalcPosition, rates_total, High, Low, Close, Volume)
    return rates_total

def CalculateMFI(nPosition, nRatesCount, HiBuffer, LoBuffer, ClBuffer, VolBuffer):
    for i in range(nPosition, nRatesCount):
        dPositiveMF = 0.0
        dNegativeMF = 0.0
        dCurrentTP = TypicalPrice(HiBuffer[i], LoBuffer[i], ClBuffer[i])
        j = 1
        while j <= ExtMFIPeriod:
            index = i - j
            dPreviousTP = TypicalPrice(HiBuffer[index], LoBuffer[index], ClBuffer[index])
            if dCurrentTP > dPreviousTP:
                dPositiveMF += VolBuffer[index + 1] * dCurrentTP
            if dCurrentTP < dPreviousTP:
                dNegativeMF += VolBuffer[index + 1] * dCurrentTP
            dCurrentTP = dPreviousTP
            j += 1
        if dNegativeMF != 0.0:
            ExtMFIBuffer[i] = 100.0 - _fdiv(100.0, 1 + _fdiv(dPositiveMF, dNegativeMF))
        else:
            ExtMFIBuffer[i] = 100.0

def TypicalPrice(dHi, dLo, dCl):
    return (dHi + dLo + dCl) / 3


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Mfi(_MQL5Indicator):
    name = 'mfi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMFIPeriod': 14,  # Period
        'InpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
    }
    y_range = (0.0, 100.0)

