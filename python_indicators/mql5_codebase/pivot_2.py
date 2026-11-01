"""pivot-2 — converted from MQL5: MQL5 Indicators/Pivot-2/pivot-2.mq5

Support and resistance lines
Copyright: Copyright © 2004, Aborigen; Link: http://forex.kbpauk.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, Aborigen', 'link': 'http://forex.kbpauk.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [8421376], 2: [16748574], 3: [65280], 4: [14822282], 5: [255], 6: [16711935], 7: [2763429]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 4, 5: 2, 6: 2, 7: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {1: 'Res 3', 2: 'Res 2', 3: 'Res 1', 4: 'Pivot', 5: 'Sup 1', 6: 'Sup 2', 7: 'Sup 3'}, 'levels': [], 'description': ['Support and resistance lines'], 'name': 'pivot-2', 'source': 'MQL5 Indicators/Pivot-2/pivot-2.mq5', 'folder': 'Pivot-2', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
Ind4Buffer = Arr(0, 0.0)
Ind5Buffer = Arr(0, 0.0)
Ind6Buffer = Arr(0, 0.0)
Ind7Buffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    if not TimeFramesCheck('Pivot-2', Period()):
        return INIT_FAILED
    min_rates_total = _idiv(2 * PeriodSeconds(PERIOD_D1), PeriodSeconds(Period()))
    IndInit(0, Ind1Buffer, 0.0, min_rates_total, Shift)
    IndInit(1, Ind2Buffer, 0.0, min_rates_total, Shift)
    IndInit(2, Ind3Buffer, 0.0, min_rates_total, Shift)
    IndInit(3, Ind4Buffer, 0.0, min_rates_total, Shift)
    IndInit(4, Ind5Buffer, 0.0, min_rates_total, Shift)
    IndInit(5, Ind6Buffer, 0.0, min_rates_total, Shift)
    IndInit(6, Ind7Buffer, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Pivot-2', '(', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar, _s_OnCalculate_LastHigh, _s_OnCalculate_LastLow
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    P = 0.0
    S1 = 0.0
    R1 = 0.0
    S2 = 0.0
    R2 = 0.0
    S3 = 0.0
    R3 = 0.0
    iTime_ = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
        _s_OnCalculate_LastHigh = 0.0
        _s_OnCalculate_LastLow = 999999999.0
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Ind1Buffer[bar] = 0.0
        Ind2Buffer[bar] = 0.0
        Ind3Buffer[bar] = 0.0
        Ind4Buffer[bar] = 0.0
        Ind5Buffer[bar] = 0.0
        Ind6Buffer[bar] = 0.0
        Ind7Buffer[bar] = 0.0
        if high[bar + 1] > _s_OnCalculate_LastHigh:
            _s_OnCalculate_LastHigh = high[bar + 1]
        if low[bar + 1] < _s_OnCalculate_LastLow:
            _s_OnCalculate_LastLow = low[bar + 1]
        if CopyTime(Symbol(), PERIOD_D1, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            _s_OnCalculate_LastCountBar = bar
            Ind1Buffer[bar + 1] = 0.0
            Ind2Buffer[bar + 1] = 0.0
            Ind3Buffer[bar + 1] = 0.0
            Ind4Buffer[bar + 1] = 0.0
            Ind5Buffer[bar + 1] = 0.0
            Ind6Buffer[bar + 1] = 0.0
            Ind7Buffer[bar + 1] = 0.0
            P = (_s_OnCalculate_LastHigh + _s_OnCalculate_LastLow + close[bar + 1]) / 3
            P2 = 2 * P
            R1 = P2 - _s_OnCalculate_LastLow
            S1 = P2 - _s_OnCalculate_LastHigh
            diff = _s_OnCalculate_LastHigh - _s_OnCalculate_LastLow
            R2 = P + diff
            S2 = P - diff
            R3 = P2 + (_s_OnCalculate_LastHigh - (2 * _s_OnCalculate_LastLow))
            S3 = P2 - ((2 * _s_OnCalculate_LastHigh) - _s_OnCalculate_LastLow)
            _s_OnCalculate_LastLow = open[bar]
            _s_OnCalculate_LastHigh = open[bar]
            Ind1Buffer[bar] = R3
            Ind2Buffer[bar] = R2
            Ind3Buffer[bar] = R1
            Ind4Buffer[bar] = P
            Ind5Buffer[bar] = S1
            Ind6Buffer[bar] = S2
            Ind7Buffer[bar] = S3
            Comment('\n', 'Res3=', DoubleToString(R3, Digits()), '\n', 'Res2=', DoubleToString(R2, Digits()), '\n', 'Res1=', DoubleToString(R1, Digits()), '\n', 'Pivot=', DoubleToString(P, Digits()), '\n', 'Sup1=', DoubleToString(S1, Digits()), '\n', 'Sup2=', DoubleToString(S2, Digits()), '\n', 'Sup3=', DoubleToString(S3, Digits()))
        if Ind1Buffer[bar + 1] and (not Ind1Buffer[bar]):
            Ind1Buffer[bar] = Ind1Buffer[bar + 1]
            Ind2Buffer[bar] = Ind2Buffer[bar + 1]
            Ind3Buffer[bar] = Ind3Buffer[bar + 1]
            Ind4Buffer[bar] = Ind4Buffer[bar + 1]
            Ind5Buffer[bar] = Ind5Buffer[bar + 1]
            Ind6Buffer[bar] = Ind6Buffer[bar + 1]
            Ind7Buffer[bar] = Ind7Buffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def TimeFramesCheck(IndName, TFrame):
    if TFrame >= PERIOD_H12:
        Print('Chart period for indicator ' + IndName + ' cannot be greater than H12')
        return (0 != 0)
    return True

# ---- static local variables
_s_OnCalculate_LastHigh = 0.0
_s_OnCalculate_LastLow = 0.0
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pivot2(_MQL5Indicator):
    name = 'pivot-2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

