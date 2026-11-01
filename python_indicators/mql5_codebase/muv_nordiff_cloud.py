"""muv_nordiff_cloud — converted from MQL5: MQL5 Indicators/MUV_NorDIFF_Cloud/muv_nordiff_cloud.mq5

Copyright: Copyright © 2008, svm-d; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, svm-d', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [6333684, 16760576], 2: [16711680], 3: [255], 4: [65280], 5: [16711935]}, 'widths': {2: 1, 3: 1, 4: 4, 5: 4}, 'styles': {}, 'labels': {1: 'MUV_DIFF % Down; MUV_DIFF % Up', 2: 'MUV_DIFF % Sma', 3: 'MUV_DIFF % Ema', 4: 'MUV_DIFF % Buy', 5: 'MUV_DIFF % Sell'}, 'levels': [100.0, -100.0], 'description': [], 'name': 'muv_nordiff_cloud', 'source': 'MQL5 Indicators/MUV_NorDIFF_Cloud/muv_nordiff_cloud.mq5', 'folder': 'MUV_NorDIFF_Cloud', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 14, 'label': 'XMUV indicator period', 'sinput': False}, {'mql': 'Momentum', 'py': 'Momentum', 'param': 'Momentum', 'type': 'uint', 'default': 1, 'label': 'Momentum period', 'sinput': False}, {'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'uint', 'default': 14, 'label': 'extremums searching period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 14)  # XMUV indicator period
Momentum = _input('Momentum', 1)  # Momentum period
KPeriod = _input('KPeriod', 14)  # extremums searching period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
SmaDiffBuffer = Arr(0, 0.0)
EmaDiffBuffer = Arr(0, 0.0)
SmaDiffBuffer_ = Arr(0, 0.0)
EmaDiffBuffer_ = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
E_Handle = 0
S_Handle = 0
min_rates_total = 0
Count = Arr(0, 0)
SmaValue = Arr(0, 0.0)
EmaValue = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global E_Handle, S_Handle, min_rates_total
    min_rates_total = _int(MAPeriod + Momentum + KPeriod)
    S_Handle = iCustom(None, 0, 'XMUV', 0, MAPeriod, 0, 0, 0)
    if S_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of XMUV SMA indicator')
    E_Handle = iCustom(None, 0, 'XMUV', 1, MAPeriod, 0, 0, 0)
    if E_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of XMUV EMA indicator')
    ArrayResize(Count, KPeriod)
    ArrayResize(SmaValue, KPeriod)
    ArrayResize(EmaValue, KPeriod)
    ArrayInitialize(Count, 0)
    ArrayInitialize(SmaValue, 0.0)
    ArrayInitialize(EmaValue, 0.0)
    SetIndexBuffer(0, SmaDiffBuffer, INDICATOR_DATA)
    ArraySetAsSeries(SmaDiffBuffer, True)
    SetIndexBuffer(1, EmaDiffBuffer, INDICATOR_DATA)
    ArraySetAsSeries(EmaDiffBuffer, True)
    SetIndexBuffer(2, SmaDiffBuffer_, INDICATOR_DATA)
    ArraySetAsSeries(SmaDiffBuffer_, True)
    SetIndexBuffer(3, EmaDiffBuffer_, INDICATOR_DATA)
    ArraySetAsSeries(EmaDiffBuffer_, True)
    SetIndexBuffer(4, BuyBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BuyBuffer, True)
    SetIndexBuffer(5, SellBuffer, INDICATOR_DATA)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'MUV_DIFF %(', MAPeriod, ', ', Momentum, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(S_Handle) < rates_total or BarsCalculated(E_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    SDiff = Arr(0, 0.0)
    EDiff = Arr(0, 0.0)
    SmaMax = 0.0
    SmaMin = 0.0
    EmaMax = 0.0
    EmaMin = 0.0
    SmaRange = 0.0
    EmaRange = 0.0
    SmaRes = 0.0
    EmaRes = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1 + _int(Momentum)
    if CopyBuffer(S_Handle, 0, 0, to_copy, SDiff) <= 0:
        return 0
    if CopyBuffer(E_Handle, 0, 0, to_copy, EDiff) <= 0:
        return 0
    ArraySetAsSeries(SDiff, True)
    ArraySetAsSeries(EDiff, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SmaValue[Count[0]] = SDiff[bar] - SDiff[bar + Momentum]
        EmaValue[Count[0]] = EDiff[bar] - EDiff[bar + Momentum]
        SmaMax = SmaValue[ArrayMaximum(SmaValue, 0, KPeriod)]
        SmaMin = SmaValue[ArrayMinimum(SmaValue, 0, KPeriod)]
        SmaRange = SmaMax - SmaMin
        EmaMax = EmaValue[ArrayMaximum(EmaValue, 0, KPeriod)]
        EmaMin = EmaValue[ArrayMinimum(EmaValue, 0, KPeriod)]
        EmaRange = EmaMax - EmaMin
        if SmaRange > 0:
            SmaRes = 100 - _fdiv(200 * (SmaMax - SmaValue[Count[0]]), SmaRange)
        else:
            SmaRes = 100.0
        if EmaRange > 0:
            EmaRes = 100 - _fdiv(200 * (EmaMax - EmaValue[Count[0]]), EmaRange)
        else:
            EmaRes = 100.0
        SmaDiffBuffer[bar] = SmaRes
        SmaDiffBuffer_[bar] = SmaRes
        EmaDiffBuffer[bar] = EmaRes
        EmaDiffBuffer_[bar] = EmaRes
        if SmaRes == 100 or EmaRes == 100:
            BuyBuffer[bar] = 100.0
        else:
            BuyBuffer[bar] = EMPTY_VALUE
        if SmaRes == -100 or EmaRes == -100:
            SellBuffer[bar] = -100.0
        else:
            SellBuffer[bar] = EMPTY_VALUE
        if bar:
            Recount_ArrayZeroPos(Count, KPeriod)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MuvNordiffCloud(_MQL5Indicator):
    name = 'muv_nordiff_cloud'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 14,  # XMUV indicator period
        'Momentum': 1,  # Momentum period
        'KPeriod': 14,  # extremums searching period
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

