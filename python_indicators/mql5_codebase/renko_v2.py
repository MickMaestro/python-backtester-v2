"""renko_v2 — converted from MQL5: MQL5 Indicators/Renko_v2/renko_v2.mq5

Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: E-mail: igorad2004@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'E-mail: igorad2004@list.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 11}, 'colors': {1: [16443110], 2: [14822282], 3: [16711935], 4: [255, 8388736, 8421504, 8421376, 65280]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Renko_v2', 2: 'Upper Renko', 3: 'Lower Renko', 4: 'Renko_BARS'}, 'levels': [], 'description': [], 'name': 'renko_v2', 'source': 'MQL5 Indicators/Renko_v2/renko_v2.mq5', 'folder': 'Renko_v2', 'inputs': [{'mql': 'PeriodATR', 'py': 'PeriodATR', 'param': 'PeriodATR', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Katr', 'py': 'Katr', 'param': 'Katr', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 1, 'label': 'Horizontal shift of the channel in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodATR = _input('PeriodATR', 10)
Katr = _input('Katr', 1.0)
Shift = _input('Shift', 1)  # Horizontal shift of the channel in bars
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Up2Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(PeriodATR + Shift)
    SetIndexBuffer(0, Up1Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Up1Buffer, True)
    SetIndexBuffer(1, Dn1Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn1Buffer, True)
    SetIndexBuffer(2, Up2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Up2Buffer, True)
    SetIndexBuffer(3, Dn2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn2Buffer, True)
    SetIndexBuffer(4, UpIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(5, DnIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(6, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_SHIFT, 0)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
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
    ArraySetAsSeries(Open, True)
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
        Up1Buffer[bar] = Up
        Dn1Buffer[bar] = Dn
        Up2Buffer[bar] = Up
        Dn2Buffer[bar] = Dn
        if bar:
            _s_OnCalculate_Up_ = Up
            _s_OnCalculate_Dn_ = Dn
            _s_OnCalculate_Brick_ = Brick
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= _int(Shift)
    for bar in range(limit, 0 - 1, -1):
        clr = 2
        UpIndBuffer[bar] = 0.0
        DnIndBuffer[bar] = 0.0
        if Close[bar] > Up1Buffer[bar + Shift]:
            if Open[bar] < Close[bar]:
                clr = 4
            else:
                clr = 3
            UpIndBuffer[bar] = High[bar]
            DnIndBuffer[bar] = Low[bar]
        if Close[bar] < Dn1Buffer[bar + Shift]:
            if Open[bar] > Close[bar]:
                clr = 0
            else:
                clr = 1
            UpIndBuffer[bar] = High[bar]
            DnIndBuffer[bar] = Low[bar]
        ColorIndBuffer[bar] = clr
    return rates_total

# ---- static local variables
_s_OnCalculate_Up_ = 0.0
_s_OnCalculate_Dn_ = 0.0
_s_OnCalculate_Brick_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RenkoV2(_MQL5Indicator):
    name = 'renko_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'PeriodATR': 10,
        'Katr': 1.0,
        'Shift': 1,  # Horizontal shift of the channel in bars
    }

