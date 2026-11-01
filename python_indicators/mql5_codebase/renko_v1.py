"""renko_v1 — converted from MQL5: MQL5 Indicators/Renko_v1/renko_v1.mq5

Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: E-mail: igorad2004@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'E-mail: igorad2004@list.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [16711935]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper Renko', 2: 'Lower Renko'}, 'levels': [], 'description': [], 'name': 'renko_v1', 'source': 'MQL5 Indicators/Renko_v1/renko_v1.mq5', 'folder': 'Renko_v1', 'inputs': [{'mql': 'PeriodATR', 'py': 'PeriodATR', 'param': 'PeriodATR', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Katr', 'py': 'Katr', 'param': 'Katr', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodATR = _input('PeriodATR', 10)
Katr = _input('Katr', 1.0)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(PeriodATR)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Renko(', PeriodATR, ', ', DoubleToString(Katr, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_Brick_, _s_OnCalculate_Dn_, _s_OnCalculate_Up_
    if rates_total < min_rates_total:
        return 0
    limit = 0
    Up = 0.0
    Dn = 0.0
    Brick = 0.0
    AvgRange = 0.0
    dK = 0.0
    ATR = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_Up_ = High[limit]
        _s_OnCalculate_Dn_ = Low[limit]
        _s_OnCalculate_Brick_ = Katr * (High[limit] - Low[limit])
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    Up = _s_OnCalculate_Up_
    Dn = _s_OnCalculate_Dn_
    Brick = _s_OnCalculate_Brick_
    for bar in range(limit, 0 - 1, -1):
        AvgRange = 0.0
        for iii in range(_int(PeriodATR - 1), 0 - 1, -1):
            dK = 1.0
            AvgRange += dK * MathAbs(High[bar + iii] - Low[bar + iii])
        ATR = AvgRange / PeriodATR
        if Close[bar] > (Up + Brick):
            if Brick:
                Up += MathRound(_fdiv(Close[bar] - Up, Brick)) * Brick
            Brick = Katr * ATR
            Dn = Up - Brick
        if Close[bar] < (Dn - Brick):
            if Brick:
                Dn -= MathRound(_fdiv(Dn - Close[bar], Brick)) * Brick
            Brick = Katr * ATR
            Up = Dn + Brick
        UpBuffer[bar] = Up
        DnBuffer[bar] = Dn
        if bar:
            _s_OnCalculate_Up_ = Up
            _s_OnCalculate_Dn_ = Dn
            _s_OnCalculate_Brick_ = Brick
    return rates_total

# ---- static local variables
_s_OnCalculate_Up_ = 0.0
_s_OnCalculate_Dn_ = 0.0
_s_OnCalculate_Brick_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RenkoV1(_MQL5Indicator):
    name = 'renko_v1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'PeriodATR': 10,
        'Katr': 1.0,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

