"""FractalSystem — converted from MQL5: MQL5 Indicators/FractalSystem/FractalSystem.mq5

Copyright: Copyright © 2005, Maloma; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Maloma', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 2, 6: 2}, 'colors': {1: [255], 2: [16711680], 3: [17919], 4: [15570276], 5: [16711935], 6: [8421376]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Fractal Up', 2: 'Fractal Down', 3: 'Signal Up', 4: 'Signal Down', 5: 'Diapazon Up', 6: 'Diapazon Down'}, 'levels': [], 'description': [], 'name': 'FractalSystem', 'source': 'MQL5 Indicators/FractalSystem/FractalSystem.mq5', 'folder': 'FractalSystem', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
dUpFractalsBuffer = Arr(0, 0.0)
dDownFractalsBuffer = Arr(0, 0.0)
dUpSignalBuffer = Arr(0, 0.0)
dDownSignalBuffer = Arr(0, 0.0)
UpDiapazonBuffer = Arr(0, 0.0)
DnDiapazonBuffer = Arr(0, 0.0)
min_rates_total = 0
Point3 = 0.0

def OnInit():
    global Point3, min_rates_total
    min_rates_total = 6
    Point3 = 3 * Point()
    shortname = Box("")
    StringConcatenate(shortname, 'FractalsmSignal6diapazon(', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, dUpFractalsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    ArraySetAsSeries(dUpFractalsBuffer, True)
    SetIndexBuffer(1, dDownFractalsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    ArraySetAsSeries(dDownFractalsBuffer, True)
    SetIndexBuffer(2, dUpSignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(dUpSignalBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_ARROW, 241)
    SetIndexBuffer(3, dDownSignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(dDownSignalBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(3, PLOT_ARROW, 242)
    SetIndexBuffer(4, UpDiapazonBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpDiapazonBuffer, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(5, DnDiapazonBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnDiapazonBuffer, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 6
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        dUpSignalBuffer[bar] = 0.0
        UpDiapazonBuffer[bar] = 0.0
        dUpFractalsBuffer[bar] = 0.0
        dDownSignalBuffer[bar] = 0.0
        DnDiapazonBuffer[bar] = 0.0
        dDownFractalsBuffer[bar] = 0.0
        if ((High[bar + 3] > High[bar + 3 + 1] and High[bar + 3] > High[bar + 3 + 2]) and High[bar + 3] > High[bar + 3 - 1]) and High[bar + 3] > High[bar + 3 - 2]:
            dUpSignalBuffer[bar] = Low[bar] - Point3
            dUpFractalsBuffer[bar + 3] = High[bar + 3]
            UpDiapazonBuffer[bar] = Open[bar]
            UpDiapazonBuffer[bar + 3] = High[bar + 3]
        if ((Low[bar + 3] < Low[bar + 3 + 1] and Low[bar + 3] < Low[bar + 3 + 2]) and Low[bar + 3] < Low[bar + 3 - 1]) and Low[bar + 3] < Low[bar + 3 - 2]:
            dDownSignalBuffer[bar] = High[bar] + Point3
            dDownFractalsBuffer[bar + 3] = Low[bar + 3]
            DnDiapazonBuffer[bar] = Open[bar]
            DnDiapazonBuffer[bar + 3] = Low[bar + 3]
            continue
        if (((High[bar + 3] == High[bar + 3 + 1] and High[bar + 3] > High[bar + 3 + 2]) and High[bar + 3] > High[bar + 3 + 3]) and High[bar + 3] > High[bar + 3 - 1]) and High[bar + 3] > High[bar + 3 - 2]:
            dUpSignalBuffer[bar] = Low[bar] - Point3
            dUpFractalsBuffer[bar + 3] = High[bar + 3]
            UpDiapazonBuffer[bar] = Open[bar]
            UpDiapazonBuffer[bar + 3] = High[bar + 3]
        if (((Low[bar + 3] == Low[bar + 3 + 1] and Low[bar + 3] < Low[bar + 3 + 2]) and Low[bar + 3] < Low[bar + 3 + 3]) and Low[bar + 3] < Low[bar + 3 - 1]) and Low[bar + 3] < Low[bar + 3 - 2]:
            dDownSignalBuffer[bar] = High[bar] + Point3
            dDownFractalsBuffer[bar + 3] = Low[bar + 3]
            DnDiapazonBuffer[bar] = Open[bar]
            DnDiapazonBuffer[bar + 3] = Low[bar + 3]
            continue
        if ((((High[bar + 3] >= High[bar + 3 + 1] and High[bar + 3] == High[bar + 3 + 2]) and High[bar + 3] > High[bar + 3 + 3]) and High[bar + 3] > High[bar + 3 + 4]) and High[bar + 3] > High[bar + 3 - 1]) and High[bar + 3] > High[bar + 3 - 2]:
            dUpSignalBuffer[bar] = Low[bar] - Point3
            dUpFractalsBuffer[bar + 3] = High[bar + 3]
            UpDiapazonBuffer[bar] = Open[bar]
            UpDiapazonBuffer[bar + 3] = High[bar + 3]
        if ((((Low[bar + 3] <= Low[bar + 3 + 1] and Low[bar + 3] == Low[bar + 3 + 2]) and Low[bar + 3] < Low[bar + 3 + 3]) and Low[bar + 3] < Low[bar + 3 + 4]) and Low[bar + 3] < Low[bar + 3 - 1]) and Low[bar + 3] < Low[bar + 3 - 2]:
            dDownSignalBuffer[bar] = High[bar] + Point3
            dDownFractalsBuffer[bar + 3] = Low[bar + 3]
            DnDiapazonBuffer[bar] = Open[bar]
            DnDiapazonBuffer[bar + 3] = Low[bar + 3]
            continue
        if (((((High[bar + 3] >= High[bar + 3 + 1] and High[bar + 3] == High[bar + 3 + 2]) and High[bar + 3] == High[bar + 3 + 3]) and High[bar + 3] > High[bar + 3 + 4]) and High[bar + 3] > High[bar + 3 + 5]) and High[bar + 3] > High[bar + 3 - 1]) and High[bar + 3] > High[bar + 3 - 2]:
            dUpSignalBuffer[bar] = Low[bar] - Point3
            dUpFractalsBuffer[bar + 3] = High[bar + 3]
            UpDiapazonBuffer[bar] = Open[bar]
            UpDiapazonBuffer[bar + 3] = High[bar + 3]
        if (((((Low[bar + 3] <= Low[bar + 3 + 1] and Low[bar + 3] == Low[bar + 3 + 2]) and Low[bar + 3] == Low[bar + 3 + 3]) and Low[bar + 3] < Low[bar + 3 + 4]) and Low[bar + 3] < Low[bar + 3 + 5]) and Low[bar + 3] < Low[bar + 3 - 1]) and Low[bar + 3] < Low[bar + 3 - 2]:
            dDownSignalBuffer[bar] = High[bar] + Point3
            dDownFractalsBuffer[bar + 3] = Low[bar + 3]
            DnDiapazonBuffer[bar] = Open[bar]
            DnDiapazonBuffer[bar + 3] = Low[bar + 3]
            continue
        if ((((((High[bar + 3] >= High[bar + 3 + 1] and High[bar + 3] == High[bar + 3 + 2]) and High[bar + 3] >= High[bar + 3 + 3]) and High[bar + 3] == High[bar + 3 + 4]) and High[bar + 3] > High[bar + 3 + 5]) and High[bar + 3] > High[bar + 3 + 6]) and High[bar + 3] > High[bar + 3 - 1]) and High[bar + 3] > High[bar + 3 - 2]:
            dUpSignalBuffer[bar] = Low[bar] - Point3
            dUpFractalsBuffer[bar + 3] = High[bar + 3]
            UpDiapazonBuffer[bar] = Open[bar]
            UpDiapazonBuffer[bar + 3] = High[bar + 3]
        if ((((((Low[bar + 3] <= Low[bar + 3 + 1] and Low[bar + 3] == Low[bar + 3 + 2]) and Low[bar + 3] <= Low[bar + 3 + 3]) and Low[bar + 3] == Low[bar + 3 + 4]) and Low[bar + 3] < Low[bar + 3 + 5]) and Low[bar + 3] < Low[bar + 3 + 6]) and Low[bar + 3] < Low[bar + 3 - 1]) and Low[bar + 3] < Low[bar + 3 - 2]:
            dDownSignalBuffer[bar] = High[bar] + Point3
            dDownFractalsBuffer[bar + 3] = Low[bar + 3]
            DnDiapazonBuffer[bar] = Open[bar]
            DnDiapazonBuffer[bar + 3] = Low[bar + 3]
            continue
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalSystem(_MQL5Indicator):
    name = 'FractalSystem'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

