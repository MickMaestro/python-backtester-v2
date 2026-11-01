"""vroc — converted from MQL5: MQL5 Indicators/Volume Rate of Change (VROC)/vroc.mq5

Volume Rate of Change
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Volume Rate of Change'], 'name': 'vroc', 'source': 'MQL5 Indicators/Volume Rate of Change (VROC)/vroc.mq5', 'folder': 'Volume Rate of Change (VROC)', 'inputs': [{'mql': 'InpPeriodVROC', 'py': 'InpPeriodVROC', 'param': 'InpPeriodVROC', 'type': 'int', 'default': 25, 'label': 'Period', 'sinput': False}, {'mql': 'InpVolumeType', 'py': 'InpVolumeType', 'param': 'InpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodVROC = _input('InpPeriodVROC', 25)  # Period
InpVolumeType = _input('InpVolumeType', VOLUME_TICK)  # Volumes
ExtVROCBuffer = Arr(0, 0.0)
ExtPeriodVROC = 0

def OnInit():
    global ExtPeriodVROC
    if InpPeriodVROC <= 1:
        ExtPeriodVROC = 25
        printf('Incorrect value for input variable InpPeriodVROC=%d. Indicator will use value=%d for calculations.', InpPeriodVROC, ExtPeriodVROC)
    else:
        ExtPeriodVROC = InpPeriodVROC
    SetIndexBuffer(0, ExtVROCBuffer)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VROC(' + _str(ExtPeriodVROC) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodVROC - 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < ExtPeriodVROC:
        return 0
    pos = prev_calculated - 1
    if pos < (ExtPeriodVROC - 1):
        pos = ExtPeriodVROC - 1
    if InpVolumeType == VOLUME_TICK:
        CalculateVROC(pos, rates_total, TickVolume)
    else:
        CalculateVROC(pos, rates_total, Volume)
    return rates_total

def CalculateVROC(nPosition, nRatesCount, VolBuffer):
    for i in range(nPosition, nRatesCount):
        PrevVolume = float(VolBuffer[i - (ExtPeriodVROC - 1)])
        CurrVolume = float(VolBuffer[i])
        if PrevVolume != 0.0:
            ExtVROCBuffer[i] = _fdiv(100.0 * (CurrVolume - PrevVolume), PrevVolume)
        else:
            ExtVROCBuffer[i] = ExtVROCBuffer[i - 1]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vroc(_MQL5Indicator):
    name = 'vroc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodVROC': 25,  # Period
        'InpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
    }

