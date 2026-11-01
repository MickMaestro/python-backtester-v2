"""hl — converted from MQL5: MQL5 Indicators/HL/hl.mq5

Resistance and support levels at a fixed timeframe
Copyright: Copyright © 2007, KCBT; Link: http://www.kcbt.ru/forum/index.php?; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, KCBT', 'link': 'http://www.kcbt.ru/forum/index.php?', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8421376], 2: [16748574], 3: [16711935]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'HL Up', 2: 'HL Pivot', 3: 'HL Down'}, 'levels': [], 'description': ['Resistance and support levels at a fixed timeframe'], 'name': 'hl', 'source': 'MQL5 Indicators/HL/hl.mq5', 'folder': 'HL', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16408, 'label': 'Chart period for calculating the levels', 'sinput': False}, {'mql': 'ShowComment', 'py': 'ShowComment', 'param': 'ShowComment', 'type': 'bool', 'default': True, 'label': 'Whether to draw comments', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_D1)  # Chart period for calculating the levels
ShowComment = _input('ShowComment', True)  # Whether to draw comments
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    if not TimeFramesCheck('HL', TimeFrame, Period()):
        return INIT_FAILED
    min_rates_total = 2
    IndInit(0, Ind1Buffer, 0.0, min_rates_total, Shift)
    IndInit(1, Ind2Buffer, 0.0, min_rates_total, Shift)
    IndInit(2, Ind3Buffer, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'HL(', EnumToString(TimeFrame, 'ENUM_TIMEFRAMES'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar, _s_OnCalculate_prev_high, _s_OnCalculate_prev_low
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    last_close = 0.0
    last_high = 0.0
    last_low = 0.0
    P = 0.0
    R = 0.0
    S = 0.0
    iTime_ = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
        _s_OnCalculate_prev_low = 999999999.0
        _s_OnCalculate_prev_high = 0.0
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Ind1Buffer[bar] = 0.0
        Ind2Buffer[bar] = 0.0
        Ind3Buffer[bar] = 0.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            _s_OnCalculate_LastCountBar = bar
            Ind1Buffer[bar + 1] = 0.0
            Ind2Buffer[bar + 1] = 0.0
            Ind3Buffer[bar + 1] = 0.0
            last_close = close[bar + 1]
            last_high = _s_OnCalculate_prev_high
            last_low = _s_OnCalculate_prev_low
            P = (last_high + last_low) / 2
            R = last_high
            S = last_low
            _s_OnCalculate_prev_high = high[bar]
            _s_OnCalculate_prev_low = low[bar]
        _s_OnCalculate_prev_high = MathMax(_s_OnCalculate_prev_high, high[bar])
        _s_OnCalculate_prev_low = MathMin(_s_OnCalculate_prev_low, low[bar])
        Ind1Buffer[bar] = R
        Ind2Buffer[bar] = P
        Ind3Buffer[bar] = S
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if ShowComment:
        Comment('Current H=', DoubleToString(R, Digits()), ', L=', DoubleToString(S, Digits()), ', HL/2=', DoubleToString(P, Digits()), ', H-L=', DoubleToString(_fdiv(R - S, Point()), 0))
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def TimeFramesCheck(IndName, inTFrame, outTFrame):
    if inTFrame <= outTFrame:
        Print('Chart period for indicator ' + IndName + ' cannot be less than ', GetStringTimeframe(inTFrame))
        return (0 != 0)
    return True

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

# ---- static local variables
_s_OnCalculate_LastCountBar = 0
_s_OnCalculate_prev_low = 0.0
_s_OnCalculate_prev_high = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Hl(_MQL5Indicator):
    name = 'hl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Chart period for calculating the levels
        'ShowComment': True,  # Whether to draw comments
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

